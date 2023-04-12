import copy
from datetime import datetime, timedelta
from framework.error.exception import TimeoutException
from framework.manager.modem import ModemManager, ModemThreadData
from framework.models.modemlog import ModemLogModel, ModemLogOwner, ModemLogType
from framework.models.server import ServerModel, ServerModemModel
from framework.models.schedule import ModemsAutoRotateAgendaItem
from framework.infra.modem import Modem as IModem
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from threading import Thread, Event, Lock
from framework.service.route.routeservice import RouteService
from framework.service.server.servereventservice import EventType, Event as ServerEvent
from framework.util.format import HumanBytes
from time import sleep
from framework.settings import Settings

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
class ModemState():
    modem: ServerModemModel
    lock: ModemThreadData
    is_connected: bool    
    connectivity: ModemConnectivity

    def __init__(
            self, 
            modem: ServerModemModel, 
            infra_modem: IModem = None, 
            lock: ModemThreadData = None,
            is_connected: bool = None,
            connectivity: ModemConnectivity = None
    ):
        self.modem = modem
        self.infra_modem = infra_modem
        self.lock = lock
        self.is_connected = is_connected
        self.connectivity = connectivity


class ModemsEventObserver():
    def __init__(self, server_event, settings: Settings):
        self._observers = None
        self.server_event = server_event
        self.settings = settings

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
                    self.notify(EventType.MODEM_CONNECT, observer)                    
                    continue  

    def notify(self, type: EventType, data):
        self.server_event.emit(ServerEvent(type = type, data = data))

        if type == EventType.UNEXPECTED_MODEM_DISCONNECT:
            modem_log_model = ModemLogModel(
                modem_id=data['modem']['id'],
                owner=ModemLogOwner.SYSTEM, 
                type=ModemLogType.ERROR, 
                message='app.log.modem.unexpectedDisconnect',
                logged_at = datetime.now()
            )
            modem_log_model.save_to_db()
            self.server_event.emit(ServerEvent(type = EventType.MODEM_LOG, data = modem_log_model))

        elif type == EventType.MODEM_CONNECT:
            modem_log_model = ModemLogModel(
                modem_id=data['modem']['id'],
                owner=ModemLogOwner.SYSTEM, 
                type=ModemLogType.SUCCESS, 
                message='app.log.modem.connect',
                logged_at = datetime.now()
            )
            modem_log_model.save_to_db()
            self.server_event.emit(ServerEvent(type = EventType.MODEM_LOG, data = modem_log_model))


class ModemsObserver():
    def __init__(self, server: ServerModel, modems_manager: ModemManager):       
        self.server = server        
        self.modems_manager = modems_manager       
        self.server_modems = []
        self.modems_states = []
        self.modems_states_subscribers = []
        self.modems_connectivity_subscribers = []
        self.reload_modems()

    def subscribe_modems_states(self, callback):
        self.modems_states_subscribers.append(callback)

    def subscribe_modems_connectivity(self, callback):
        self.modems_connectivity_subscribers.append(callback)

    def notify_modems_states_subscribers(self):
        for callback in self.modems_states_subscribers: callback(self.modems_states)

    def notify_modems_connectivity_subscribers(self):
        for callback in self.modems_connectivity_subscribers: callback(self.modems_states)

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
        self.notify_modems_states_subscribers()

    def modem_state_index_by_server_modem_id(self, modems_states, server_modem_id):
        if not modems_states: return -1        
        for index, modem_state in enumerate(modems_states): 
            if modem_state.modem.id == server_modem_id: return index
        return -1       

    def observe_status(self):
        if not self.server_modems: return []

        for server_modem in self.server_modems:
            modem_state_index = self.modem_state_index_by_server_modem_id(self.modems_states, server_modem.id)
            modem_state = self.modems_states[modem_state_index] if modem_state_index > -1 else None

            if modem_state == None: continue

            if modem_state.infra_modem == None: modem_state.infra_modem = IModem(server_modem_model = modem_state.modem)
                
            modem_state.is_connected = modem_state.infra_modem.is_connected()
            modem_state.lock = self.get_lock(modem_state.infra_modem)
            modem_state.modem.schedule = server_modem.schedule

            if modem_state.is_connected != True:
                modem_state.connectivity = None

        self.notify_modems_connectivity_subscribers()

        return self.modems_states
    
    def get_lock(self, infra_modem: IModem):
        return self.modems_manager.running(infra_modem)

    def observe_connectivity(self):
        if not self.server_modems: return []

        for server_modem in self.server_modems:
            modem_state_index = self.modem_state_index_by_server_modem_id(self.modems_states, server_modem.id)
            modem_state = self.modems_states[modem_state_index] if modem_state_index > -1 else None

            if modem_state == None or modem_state.infra_modem == None or modem_state.is_connected != True: continue

            imodem_iface = modem_state.infra_modem.iface()
            if imodem_iface == None or imodem_iface.interface == None: continue

            device_middleware = modem_state.infra_modem.get_device_middleware()
            if device_middleware == None: continue

            device_details = device_middleware.details()
            network_type = device_details['network_type'] if device_details else None
            network_provider = device_details['network_provider'] if device_details else None
            network_signalbar = device_details['signalbar'] if device_details else None  

            modem_ifaddresses = imodem_iface.ifaddresses

            external_ip = None
            try: external_ip = modem_state.infra_modem.external_ip_through_device(timeout = 5)
            except TimeoutException: pass

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

        self.notify_modems_states_subscribers()
    
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
    def __init__(self, server: ServerModel, modems_manager: ModemManager, settings: Settings):                
        self.server = server        
        self.modems_manager = modems_manager
        self.modems_observer = ModemsObserver(server = server, modems_manager = modems_manager)
        self.settings = settings

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

        sleep(0.5)

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

    def subscribe_status(self, callback):
        self.modems_observer.subscribe_modems_states(callback)

    def subscribe_connectivity(self, callback):
        self.modems_observer.subscribe_modems_connectivity(callback)

    def reload_modems(self):
        self.modems_observer.reload_modems()
        

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