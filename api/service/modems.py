from datetime import datetime, timedelta
import json
from framework.models.modemlog import ModemLogModel, ModemLogOwner, ModemLogType
from framework.models.server import ServerModel
from framework.infra.modem import Modem as IModem

class ModemsService():
    def __init__(self, server_model: ServerModel, modems_manager):
        self.server_model = server_model        
        self.modems_manager = modems_manager
        self.reload_modems()
        self.auto_rotate_service = None

    def reload_modems(self):
        self.server_modems = self.server_model.modems()

    def get_lock(self, infra_modem: IModem):
        return self.modems_manager.running(infra_modem)

    def modems_status(self):
        items = [item.json() for item in self.server_modems]
        for x, item in enumerate(items):
            imodem = IModem(self.server_modems[x])
            item['is_connected'] = imodem.is_connected()

            lock = self.get_lock(imodem)
            if lock == None:
                item['lock'] = None
            else:
                item['lock'] = {
                    'task': {
                        'name': lock.action.name,
                        'stopping': lock.event_stop.is_set()
                    }
                }

        return items

    def modems_details(self):
        items = [item.json() for item in self.server_modems]
        result = []

        # if self.auto_rotate_service:
        #     print('auto_rotate_service')
        #TODO add future auto rotate alert

        for x, item in enumerate(items):
            imodem = IModem(self.server_modems[x])
            item['is_connected'] = imodem.is_connected()

            if item['is_connected'] == False:
                continue

            imodem_iface = imodem.iface()

            if imodem_iface == None or imodem_iface.interface == None:
                continue

            device_middleware = imodem.get_device_middleware()

            device_details = device_middleware.details()
            network_type = device_details['network_type'] if device_details else None
            network_provider = device_details['network_provider'] if device_details else None
            signalbar = device_details['signalbar'] if device_details else None                                

            item['interface'] = imodem_iface.interface

            modem_ifaddresses = imodem_iface.ifaddresses
            if modem_ifaddresses:
                modem_ifaddress = modem_ifaddresses[0]                           
                item['internal_ip'] = modem_ifaddress['addr']

            item['device_network_type'] = network_type
            item['device_network_provider'] = network_provider
            item['device_network_signalbar'] = signalbar

            item['external_ip_through_device'] = imodem.external_ip_through_device(silence_mode=True, retries=1)

            item['data'] = {
                'receive': {
                    'bytes': imodem_iface.rx_bytes              
                },
                'transmit': {
                    'bytes': imodem_iface.tx_bytes      
                }
            }

            item['is_connected'] = imodem.is_connected()

            if item['is_connected'] == False:
                continue

            result.append(item)

        return result


class ModemsAutoRotateAgendaItem():
    def __init__(self, server_modem_model, added_at, run_at):
        self.server_modem_model = server_modem_model
        self.added_at = added_at
        self.run_at = run_at

    def ready_to_run(self):
        difference = self.run_at - datetime.now()
        return True if difference.total_seconds() <= 0 else False
    

class ModemsAutoRotateSchedule():
    def __init__(self, modems_service: ModemsService, modems_manager):
        self.modems_service = modems_service
        self.modems_manager = modems_manager
        self.agenda_items = []

    def check(self):
        server_modems = self.modems_service.server_modems
        if server_modems == None:
            return []
        
        for server_modem in server_modems:
            if not server_modem.auto_rotate or not isinstance(server_modem.auto_rotate_time, int):
                self.remove_from_agenda_items(server_modem)
                continue

            in_agenda = self.in_agenda_items(server_modem)

            if in_agenda:
                in_agenda.server_modem_model = server_modem

            if in_agenda and in_agenda.server_modem_model.auto_rotate_time != server_modem.auto_rotate_time:
                print('removed from agenda because changed {0}'.format(server_modem.id))
                self.remove_from_agenda_items(server_modem)

            if server_modem.auto_rotate_time <= 0:
                continue

            self.add_to_agenda_items(server_modem)

        return self.agenda_items

    def calc_time_to_run(self, date_time: datetime, server_modem_model):
        run_at = date_time + timedelta(seconds=server_modem_model.auto_rotate_time)
        print('modem {0}'.format(server_modem_model.id))
        print('now: {0}'.format(date_time))
        print('run: {0}'.format(run_at))
        return run_at

    def in_agenda_items(self, server_modem_model):
        if not self.agenda_items: return None

        for agenda_item in self.agenda_items:
            if agenda_item.server_modem_model.id == server_modem_model.id:
                # print('in agenda {0}'.format(server_modem_model.id))
                return agenda_item

        return None    

    def add_to_agenda_items(self, server_modem_model):
        if self.in_agenda_items(server_modem_model): return False

        now = datetime.now()
        self.agenda_items.append(
            ModemsAutoRotateAgendaItem(
                server_modem_model=server_modem_model, 
                added_at=now, 
                run_at=self.calc_time_to_run(date_time=now, server_modem_model=server_modem_model)
            )
        )
        # print('added in agenda {0}'.format(server_modem_model.id))

        return True

    def remove_from_agenda_items(self, server_modem_model):
        if not self.agenda_items or not self.in_agenda_items(server_modem_model): return False

        # print('removed from agenda {0}'.format(server_modem_model.id))
        self.agenda_items[:] = [x for x in self.agenda_items if not x.server_modem_model.id == server_modem_model.id]
        return True


class ModemsAutoRotateService():
    def __init__(self, modems_service: ModemsService, modems_manager, socketio):
        self.modems_service = modems_service        
        self.modems_manager = modems_manager
        self.socketio = socketio
        self.schedule = ModemsAutoRotateSchedule(modems_service=modems_service, modems_manager=modems_manager)

    def get_lock(self, infra_modem: IModem):
        return self.modems_manager.running(infra_modem)

    def check_and_rotate(self):
        agenda_items = self.schedule.check()
        for agenda_item in agenda_items:
            ready_to_run = agenda_item.ready_to_run()  
            # print('agenda_item {0} auto_rotate_hard_reset = {1}'.format(agenda_item.server_modem_model.id, agenda_item.server_modem_model.auto_rotate_hard_reset))          
            # print('agenda_item {0} auto_rotate_filter = {1}'.format(agenda_item.server_modem_model.id, agenda_item.server_modem_model.auto_rotate_filter))          
            # print('\n')

            if ready_to_run == True:
                self.schedule.remove_from_agenda_items(agenda_item.server_modem_model)
                self.rotate(agenda_item.server_modem_model)

    def rotate(self, server_modem_model):        
        infra_modem = IModem(server_modem_model=server_modem_model)        
        
        lock = self.get_lock(infra_modem)
        if lock != None:
            print('no rotate because is locked')
            return False
        
        if infra_modem.is_connected() == False:
            print('no rotate because is offline')
            return False

        modem = server_modem_model.modem()
        modem_log_model = ModemLogModel(
            modem_id=modem.id,
            owner=ModemLogOwner.USER, 
            type=ModemLogType.INFO, 
            message='app.log.modem.rotate.start',
            auto=True,
            description='app.log.modem.rotate.automated',
            logged_at = datetime.now()
        )
        modem_log_model.save_to_db()

        socketio = self.socketio()

        callback = None
        if socketio:
            socketio.emit('modem_log', json.loads(modem_log_model.to_json()), broadcast=True)
            callback = lambda modem_log_model: socketio.emit('modem_log', json.loads(modem_log_model.to_json()), broadcast=True)
                
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