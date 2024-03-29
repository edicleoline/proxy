import copy
from datetime import datetime, timedelta
from typing import List
from framework.error.exception import TimeoutException
from framework.manager.modem import ModemManager, ModemManagerSubscriberEvent, ModemThreadData
from framework.models.client import Addr, Client, Instance
from framework.models.modemlog import ModemLogModel, ModemLogOwner, ModemLogType
from framework.models.server import ServerModel, ServerModemModel
from framework.models.schedule import ModemsAutoRotateAgendaItem
from framework.infra.modem import Modem as IModem
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from threading import Thread, Event, Lock
from framework.service.Cloacker import Cloacker, CloackerService
from framework.service.common.commonservice import CommonService, CommonServiceSubscriberEvent
from framework.service.server.servereventservice import EventType, Event as ServerEvent
from framework.util.format import HumanBytes
from time import sleep
from framework.settings import Settings
from enum import Enum

EXTERNAL_IP_CLACKER_ID = 'modem_observer.modem_state.modem.id.{0}'

class ModemServiceSubscriberEvent(Enum):
    ON_MODEMS_RELOAD                = 'on_modems_reload'
    ON_MODEMS_STATUS_UPDATED        = 'on_modems_status_updated'
    ON_MODEMS_CONNECTIVITY_UPDATED  = 'on_modems_connectivity_updated'

class ModemServiceSubscriber:
    event: ModemServiceSubscriberEvent
    callback: None

    def __init__(self, event: ModemServiceSubscriberEvent, callback):
        self.event = event
        self.callback = callback

@dataclass_json
@dataclass
class ModemConnectivityData():
    bytes: int
    formatted: str

    def __init__(self, bytes: int, formatted: str):
        self.bytes = bytes
        self.formatted = formatted


@dataclass_json
@dataclass
class ModemConnectivityTraffic():
    receive: ModemConnectivityData
    transmit: ModemConnectivityData

    def __init__(self, receive: ModemConnectivityData, transmit: ModemConnectivityData):
        self.receive = receive
        self.transmit = transmit


@dataclass_json
@dataclass
class ModemConnectivity():
    interface: str
    internal_ip: str
    network_type: str
    network_provider: str 
    network_signalbar: str
    external_ip: str
    data_traffic: ModemConnectivityTraffic

    def __init__(
            self,
            interface: str,
            internal_ip: str,
            network_type: str,
            network_provider: str, 
            network_signalbar: str,
            external_ip: str,
            data_traffic: ModemConnectivityTraffic
    ):
        self.interface = interface
        self.internal_ip = internal_ip
        self.network_type = network_type
        self.network_provider = network_provider
        self.network_signalbar = network_signalbar
        self.external_ip = external_ip
        self.data_traffic = data_traffic


@dataclass_json
@dataclass
class ModemSms():
    total_count: int
    unread_count: int

    def __init__(
            self,
            total_count: int,
            unread_count: int
    ):
        self.total_count = total_count
        self.unread_count = unread_count


@dataclass_json
@dataclass
class ModemState():
    modem: ServerModemModel
    lock: ModemThreadData
    is_connected: bool    
    connectivity: ModemConnectivity
    sms: ModemSms
    clients: List[Client] = None

    def __init__(
            self, 
            modem: ServerModemModel, 
            infra_modem: IModem = None, 
            lock: ModemThreadData = None,
            is_connected: bool = None,
            connectivity: ModemConnectivity = None,
            sms: ModemSms = None,
            clients: List[Client] = None
    ):
        self.modem = modem
        self.infra_modem = infra_modem
        self.lock = lock
        self.is_connected = is_connected
        self.connectivity = connectivity
        self.sms = sms
        self.clients = clients


class ModemsEventObserver():
    def __init__(self, server_event, settings: Settings, cloacker_service: CloackerService):
        self._observers = None
        self.server_event = server_event
        self.settings = settings
        self.cloacker_service = cloacker_service

    def observe(self, observers):
        json_observers = ModemState.schema().dump(observers, many=True)
        
        if self._observers == None:
            self._observers = json_observers
            return
        
        self._observe_connected(json_observers)  
        self._observers = json_observers

    def _index_by_id(self, array, id):
        for index, item in enumerate(array):
            if item['modem']['id'] == id: return index

        return -1

    def _observe_connected(self, observers):  
        for observer in observers:            
            old_observer_index = self._index_by_id(self._observers, observer['modem']['id'])

            if old_observer_index < 0: continue       

            if self._observers[old_observer_index]['is_connected'] == None:
                self._observers[old_observer_index]['is_connected'] = observer['is_connected']
                continue
            
            if self._observers[old_observer_index]['lock'] == None and observer['lock'] == None:
                if self._observers[old_observer_index]['is_connected'] == True and observer['is_connected'] == False:
                    self._observers[old_observer_index]['is_connected'] = observer['is_connected']                    
                    self.notify(EventType.UNEXPECTED_MODEM_DISCONNECT, observer)
                    continue

                if self._observers[old_observer_index]['is_connected'] == False and observer['is_connected'] == True:
                    self._observers[old_observer_index]['is_connected'] = observer['is_connected']

                    external_ip_cloacker_id = EXTERNAL_IP_CLACKER_ID.format(self._observers[old_observer_index]['modem']['id'])
                    external_ip_cloacker = self.cloacker_service.cloacker_by_id(external_ip_cloacker_id)
                    if external_ip_cloacker: external_ip_cloacker.invert()

                    self.notify(EventType.MODEM_CONNECT, observer)                    
                    continue  

    def notify(self, type: EventType, data):
        event_message = 'app.notification.modem.unexpectedDisconnect'
        event_log_type = ModemLogType.ERROR

        if type == EventType.MODEM_CONNECT:
            event_message = 'app.notification.modem.connect'
            event_log_type = ModemLogType.SUCCESS

        event_modem_log_model = ModemLogModel(
            modem_id = data['modem']['id'],
            owner = ModemLogOwner.SYSTEM, 
            type = event_log_type, 
            message = event_message,
            logged_at = datetime.now()
        )
        self.server_event.emit(ServerEvent(type = type, data = event_modem_log_model))

        modem_log_message = 'app.log.modem.unexpectedDisconnect'
        modem_log_type = ModemLogType.ERROR

        if type == EventType.MODEM_CONNECT:
            modem_log_message = 'app.log.modem.connect'
            modem_log_type = ModemLogType.SUCCESS

        modem_log_model = ModemLogModel(
            modem_id = data['modem']['id'],
            owner = ModemLogOwner.SYSTEM, 
            type = modem_log_type, 
            message = modem_log_message,
            logged_at = datetime.now()
        )
        modem_log_model.save_to_db()            
        self.server_event.emit(ServerEvent(type = EventType.MODEM_LOG, data = modem_log_model))


class ModemsObserver():
    def __init__(
        self, 
        server: ServerModel, 
        modems_manager: ModemManager, 
        settings: Settings, 
        cloacker_service: CloackerService, 
        common_service: CommonService,
        subscribers: List[ModemServiceSubscriber]
    ):       
        self.server = server        
        self.modems_manager = modems_manager  
        self.settings = settings
        self.cloacker_service = cloacker_service
        self.common_service = common_service
        self.server_modems = []
        self.modems_states = []
        self.subscribers = subscribers        
        self.modems_manager.subscribe(ModemManagerSubscriberEvent.ON_ROTATE_SUCCESS, self.on_modems_manager_rotate)
        self.common_service.subscribe(CommonServiceSubscriberEvent.ON_NET_CONNECTIONS_UPDATED, lambda connections: self.on_net_connections_updated_callback(connections))
        self.reload_modems()

    def notify_subscribers(self, event: ModemServiceSubscriberEvent = None):
        if event:
            for subscriber in self.subscribers:
                if subscriber.event == event: subscriber.callback(self.modems_states)    

    def on_modems_manager_rotate(self, data):
        if data and 'connectivity' in data:
            if self.modems_states:
                modem_state = None
                for ms in self.modems_states:
                    if ms.modem.id == data['modem']['id']:
                        modem_state = ms
                        break
                if modem_state and modem_state.connectivity:
                    modem_state.connectivity.external_ip = data['connectivity']['external_ip']

    def reload_modems(self):
        self.server_modems = self.server.modems()

        copied_modems_states = copy.copy(self.modems_states)

        modems_states = []
        for server_modem in self.server_modems:            
            modem_state = ModemState(modem = server_modem)
            copied_modem_state_index = self.modem_state_index_by_server_modem_id(copied_modems_states, server_modem.id)
            if copied_modem_state_index > -1:
                modem_state.connectivity = copied_modems_states[copied_modem_state_index].connectivity
                modem_state.lock = copied_modems_states[copied_modem_state_index].lock
                modem_state.is_connected = copied_modems_states[copied_modem_state_index].is_connected

            modems_states.append(modem_state)

        self.modems_states = modems_states
        self.invert_external_ip_cloackers()
        self.notify_subscribers(ModemServiceSubscriberEvent.ON_MODEMS_RELOAD)

    def invert_external_ip_cloackers(self):
        for modem_state in self.modems_states:
            external_ip_cloacker_id = EXTERNAL_IP_CLACKER_ID.format(modem_state.modem.id)
            external_ip_cloacker = self.cloacker_service.cloacker_by_id(external_ip_cloacker_id)
            if external_ip_cloacker: external_ip_cloacker.invert()

    def modem_state_index_by_server_modem_id(self, modems_states, server_modem_id):
        if not modems_states: return -1        
        for index, modem_state in enumerate(modems_states): 
            if modem_state.modem.id == server_modem_id: return index
        return -1       
    
    def on_net_connections_updated_callback(self, connections):
        if not self.server_modems: return []

        for server_modem in self.server_modems:
            modem_state_index = self.modem_state_index_by_server_modem_id(self.modems_states, server_modem.id)
            modem_state = self.modems_states[modem_state_index] if modem_state_index > -1 else None

            if modem_state == None: continue

            clients: List[Client] = []
            for connection in connections:
                if connection.laddr.port != modem_state.modem.proxy_ipv4_http_port \
                    and connection.laddr.port != modem_state.modem.proxy_ipv4_socks_port \
                    and connection.laddr.port != modem_state.modem.proxy_ipv6_http_port \
                    and connection.laddr.port != modem_state.modem.proxy_ipv6_socks_port: continue
                if connection.status != 'ESTABLISHED': continue

                client_already_exist = False
                for client in clients:
                    if client.ip == connection.raddr.ip:
                        client_already_exist = True
                        client.instances.append(
                            Instance(raddr = Addr(ip = connection.raddr.ip, port = connection.raddr.port))
                        )

                if client_already_exist == False: clients.append(
                    Client(ip = connection.raddr.ip, port = connection.laddr.port)
                )

            modem_state.clients = clients

    def observe_status(self):
        if not self.server_modems: return []

        for server_modem in self.server_modems:
            modem_state_index = self.modem_state_index_by_server_modem_id(self.modems_states, server_modem.id)
            modem_state = self.modems_states[modem_state_index] if modem_state_index > -1 else None

            if modem_state == None: continue

            if modem_state.infra_modem == None: modem_state.infra_modem = IModem(server_modem_model = modem_state.modem, settings = self.settings)
                
            modem_state.is_connected = modem_state.infra_modem.is_connected()
            modem_state.lock = self.get_lock(modem_state.infra_modem)
            modem_state.modem.schedule = server_modem.schedule

            if modem_state.is_connected != True:
                modem_state.connectivity = None

        self.notify_subscribers(ModemServiceSubscriberEvent.ON_MODEMS_STATUS_UPDATED)

        return self.modems_states
    
    def get_lock(self, infra_modem: IModem):
        return self.modems_manager.running(infra_modem)

    def observe_connectivity(self):
        if not self.server_modems: return []

        any_updated = False
        for server_modem in self.server_modems:
            modem_state_index = self.modem_state_index_by_server_modem_id(self.modems_states, server_modem.id)
            modem_state = self.modems_states[modem_state_index] if modem_state_index > -1 else None

            if modem_state == None or modem_state.infra_modem == None or modem_state.is_connected != True: continue

            imodem_iface = modem_state.infra_modem.iface()
            if imodem_iface == None or imodem_iface.interface == None: continue

            device_middleware = modem_state.infra_modem.get_device_middleware()
            if device_middleware == None: continue

            any_updated = True
            device_details = device_middleware.details()
            network_type = device_details['network_type'] if device_details else None
            network_provider = device_details['network_provider'] if device_details else None
            network_signalbar = device_details['signalbar'] if device_details else None             

            modem_ifaddresses = imodem_iface.ifaddresses

            external_ip = modem_state.connectivity.external_ip if modem_state.connectivity else None

            external_ip_cloacker_id = EXTERNAL_IP_CLACKER_ID.format(modem_state.modem.id)
            external_ip_cloacker = self.cloacker_service.cloacker_by_id(external_ip_cloacker_id)
            if external_ip_cloacker == None:
                self.cloacker_service.add_or_update(Cloacker(id = external_ip_cloacker_id, interval = self.settings.modem_status_external_ip_interval))

            if (
                modem_state.connectivity == None or 
                modem_state.connectivity and modem_state.connectivity.external_ip == None or
                external_ip_cloacker == None or
                external_ip_cloacker and external_ip_cloacker.ready()
            ):
                try:
                    external_ip = modem_state.infra_modem.external_ip_through_device(timeout = self.settings.modem_status_external_ip_timeout)
                    if external_ip:
                        self.cloacker_service.add_or_update(Cloacker(id = external_ip_cloacker_id, interval = self.settings.modem_status_external_ip_interval))                    
                except Exception: pass

            if modem_state.is_connected != True: continue

            modem_state.connectivity = ModemConnectivity(
                interface = imodem_iface.interface,
                internal_ip = modem_ifaddresses[0]['addr'] if modem_ifaddresses else None,
                network_type = network_type,
                network_provider = network_provider,
                network_signalbar = network_signalbar,
                external_ip = external_ip,
                data_traffic = ModemConnectivityTraffic(
                    receive = ModemConnectivityData(bytes = None, formatted = HumanBytes.format(imodem_iface.rx_bytes, True, 1)),
                    transmit = ModemConnectivityData(bytes = None, formatted = HumanBytes.format(imodem_iface.tx_bytes, True, 1))
                )
            )  

        if any_updated == True:
            self.notify_subscribers(ModemServiceSubscriberEvent.ON_MODEMS_CONNECTIVITY_UPDATED)
    
    def modem_state_index_by_id(self, server_modem_model_id):
        if not self.modems_states: return -1
        
        for index, modem_state in enumerate(self.modems_states):
            if modem_state.modem.id == server_modem_model_id: return index

        return -1
    

class ModemsObserveStatusThread(Thread):
    def __init__(self, modems_observer: ModemsObserver = None, stop_event: Event = None):
        self.delay = 1
        self.modems_observer = modems_observer
        self.stop_event = stop_event
        super(ModemsObserveStatusThread, self).__init__()

    def run_forever(self):
        try:
            while not self.stop_event.is_set():
                self.modems_observer.observe_status()             
                sleep(self.delay)
        except KeyboardInterrupt:
            # kill()
            pass

    def run(self):
        self.run_forever()


class ModemsObserveConnectivityThread(Thread):
    def __init__(self, modems_observer: ModemsObserver = None, stop_event: Event = None):
        self.delay = 1
        self.modems_observer = modems_observer
        self.stop_event = stop_event
        super(ModemsObserveConnectivityThread, self).__init__()

    def run_forever(self):
        try:
            while not self.stop_event.is_set():
                self.modems_observer.observe_connectivity()       
                sleep(self.delay)
        except KeyboardInterrupt:
            # kill()
            pass

    def run(self):
        self.run_forever()


class ModemsService():
    def __init__(
        self, 
        server: ServerModel, 
        modems_manager: ModemManager, 
        settings: Settings, 
        cloacker_service: CloackerService, 
        common_service: CommonService,
        subscribers: List[ModemServiceSubscriber] = []
    ):                
        self.server = server        
        self.modems_manager = modems_manager
        self.settings = settings
        self.cloacker_service = cloacker_service
        self.common_service = common_service
        self.subscribers = subscribers
        self.modems_observer = ModemsObserver(server, modems_manager, settings, cloacker_service, common_service, self.subscribers)        
        self._modems_observe_status_lock = Lock()
        self._modems_observe_status_stop_event = Event()
        self._modems_observe_status_thread = None
        self._modems_observe_connectivity_lock = Lock()
        self._modems_observe_connectivity_stop_event = Event()
        self._modems_observe_connectivity_thread = None          

    def observe(self):
        with self._modems_observe_status_lock:
            if not self._modems_observe_status_thread or not self._modems_observe_status_thread.is_alive():
                self._modems_observe_status_thread = ModemsObserveStatusThread(
                    modems_observer = self.modems_observer, 
                    stop_event = self._modems_observe_status_stop_event
                )
                self._modems_observe_status_thread.start()

        sleep(0.2)

        with self._modems_observe_connectivity_lock:
            if not self._modems_observe_connectivity_thread or not self._modems_observe_connectivity_thread.is_alive():
                self._modems_observe_connectivity_thread = ModemsObserveConnectivityThread(
                    modems_observer = self.modems_observer, 
                    stop_event = self._modems_observe_connectivity_stop_event
                )
                self._modems_observe_connectivity_thread.start()

    def stop_observe(self):
        self._modems_observe_status_stop_event.set()
        self._modems_observe_connectivity_stop_event.set()

    def reload_modems(self):
        self.modems_observer.reload_modems()
    
    def subscribe(self, event: ModemServiceSubscriberEvent, callback):
        self.subscribers.append(ModemServiceSubscriber(event, callback))
        

class ModemsAutoRotateSchedule():
    def __init__(self, modems_service: ModemsService, modems_manager):
        self.modems_service = modems_service
        self.modems_manager = modems_manager
        self.agenda_items = []

    def get_lock(self, infra_modem: IModem):
        return self.modems_manager.running(infra_modem)

    def check(self):
        modems_states = self.modems_service.modems_observer.modems_states
        if modems_states == None: return []
        
        for modem_state in modems_states:
            if not modem_state.modem.auto_rotate or not isinstance(modem_state.modem.auto_rotate_time, int):
                self.remove_from_agenda_items(modem_state)
                continue

            in_agenda = self.in_agenda_items(modem_state)   

            if modem_state.lock != None:
                if in_agenda: self.remove_from_agenda_items(in_agenda.modem_state)
                continue        

            if in_agenda and in_agenda.modem_state.modem.auto_rotate_time != modem_state.modem.auto_rotate_time:
                print('removed from agenda because changed {0}'.format(modem_state.modem.id))
                self.remove_from_agenda_items(modem_state)

            if modem_state.modem.auto_rotate_time <= 0:
                continue

            if in_agenda:
                in_agenda.modem_state = modem_state

            self.add_to_agenda_items(modem_state)

        return self.agenda_items

    def calc_time_to_run(self, date_time: datetime, modem_state):
        run_at = date_time + timedelta(seconds=modem_state.modem.auto_rotate_time)
        return run_at

    def in_agenda_items(self, modem_state):
        return self.in_agenda_items_by_server_modem_model_id(modem_state.modem.id)
    
    def in_agenda_items_by_server_modem_model_id(self, server_modem_model_id):
        if not self.agenda_items: return None

        for agenda_item in self.agenda_items:
            if agenda_item.modem_state.modem.id == server_modem_model_id:
                return agenda_item

        return None    

    def add_to_agenda_items(self, modem_state):
        if self.in_agenda_items(modem_state): return False

        now = datetime.now()
        self.agenda_items.append(
            ModemsAutoRotateAgendaItem(
                modem_state = modem_state,
                added_at = now,
                run_at = self.calc_time_to_run(date_time = now, modem_state = modem_state)
            )
        )
        # print('added in agenda {0}'.format(server_modem_model.id))
        return True

    def remove_from_agenda_items(self, modem_state):
        if not self.agenda_items or not self.in_agenda_items(modem_state): return False

        # print('removed from agenda {0}'.format(server_modem_model.id))
        self.agenda_items[:] = [x for x in self.agenda_items if not x.modem_state.modem.id == modem_state.modem.id]
        return True    


class ModemsAutoRotateObserver():
    def __init__(self, modems_service: ModemsService, modems_manager: ModemManager, server_event: ServerEvent):
        self.modems_service = modems_service        
        self.modems_manager = modems_manager
        self.server_event = server_event
        self.schedule = ModemsAutoRotateSchedule(modems_service=modems_service, modems_manager=modems_manager)

    def check_and_rotate(self):
        agenda_items = self.schedule.check()
        for agenda_item in agenda_items:
            ready_to_run = agenda_item.ready_to_run()  

            if ready_to_run == True:
                self.schedule.remove_from_agenda_items(agenda_item.modem_state)
                self.rotate(agenda_item.modem_state.modem, agenda_item.modem_state.infra_modem)
            else:
                index = self.modems_service.modems_observer.modem_state_index_by_id(agenda_item.modem_state.modem.id)
                if index > -1:
                    self.modems_service.modems_observer.server_modems[index].schedule = agenda_item                    

    def rotate(self, server_modem_model, infra_modem):
        modem_log_model = ModemLogModel(
            modem_id=server_modem_model.modem.id,
            owner=ModemLogOwner.USER, 
            type=ModemLogType.INFO, 
            message='app.log.modem.rotate.start',
            auto=True,
            description='app.log.modem.rotate.automated',
            logged_at = datetime.now()
        )
        modem_log_model.save_to_db()

        callback = None
        
        self.server_event.emit(ServerEvent(
            type = EventType.MODEM_LOG,
            data = modem_log_model
        ))

        callback = lambda modem_log_model: self.server_event.emit(ServerEvent(type = EventType.MODEM_LOG, data = modem_log_model))
                
        infra_modem.callback = callback
        
        self.modems_manager.rotate(
            infra_modem = infra_modem, 
            proxy_user_id = None,
            proxy_username = None,
            filters = server_modem_model.auto_rotate_filter, 
            hard_reset = server_modem_model.auto_rotate_hard_reset, 
            not_changed_try_count = 3, 
            not_ip_try_count = 6
        )


class ModemsAutoRotateObserveThread(Thread):
    def __init__(self, modems_auto_rotate_observer: ModemsAutoRotateObserver = None, stop_event: Event = None):
        self.delay = 1
        self.modems_auto_rotate_observer = modems_auto_rotate_observer
        self.stop_event = stop_event
        super(ModemsAutoRotateObserveThread, self).__init__()

    def run_forever(self):
        try:
            while not self.stop_event.is_set():
                self.modems_auto_rotate_observer.check_and_rotate()
                sleep(self.delay)
        except KeyboardInterrupt:
            # kill()
            pass

    def run(self):
        self.run_forever()


class ModemsAutoRotateService():
    def __init__(self, modems_service: ModemsService, modems_manager: ModemManager, server_event: ServerEvent, settings: Settings):
        self.modems_service = modems_service        
        self.modems_manager = modems_manager
        self.server_event = server_event
        self.settings = settings
        self.modems_auto_rotate_observer = ModemsAutoRotateObserver(
            modems_service = modems_service, modems_manager = modems_manager, server_event = server_event)

        self._modems_auto_rotate_observe_lock = Lock()
        self._modems_auto_rotate_observe_stop_event = Event()
        self._modems_auto_rotate_observe_thread = None

    def check_and_rotate(self):
        self.modems_auto_rotate_observer.check_and_rotate()

    def observe(self):
        with self._modems_auto_rotate_observe_lock:
            if not self._modems_auto_rotate_observe_thread or not self._modems_auto_rotate_observe_thread.is_alive():
                self._modems_auto_rotate_observe_thread = ModemsAutoRotateObserveThread(
                    modems_auto_rotate_observer = self.modems_auto_rotate_observer, 
                    stop_event = self._modems_auto_rotate_observe_stop_event
                )
                self._modems_auto_rotate_observe_thread.start()