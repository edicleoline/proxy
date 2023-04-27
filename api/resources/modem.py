from flask_restful import Resource, reqparse, request
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
import requests
from api.service.servercontrol import ServerControlAction, ServerControlEvent
from framework.enum.proxyauthtype import ProxyAuthType
from framework.models.modemdiagnose import ModemDiagnoseModel, ModemDiagnoseOwner, ModemDiagnoseType
from framework.models.schedule import ModemsAutoRotateAgendaItem
from framework.service.server.servereventservice import Event, EventType
from framework.helper.database.pagination import PaginateDirection, PaginateOrder
from framework.models.modem import ModemModel
from framework.models.modemlog import ModemLogModel, ModemLogOwner, ModemLogType
from framework.models.server import ServerModel, ServerModemModel
from framework.infra.modem import Modem as IModem
from framework.models.server import ServerModel, ServerModemModel
from flask import request
import json
from app import app
from datetime import datetime
from framework.manager.error.exception import ModemLockedByOtherThreadException, NoTaskRunningException
from framework.models.proxyuser import ProxyUserModel
from framework.models.proxyuseripfilter import ProxyUserIPFilterModel

def filters_type(value, name):
    full_json_data = request.get_json()
    filters_json = full_json_data[name]

    if(not isinstance(filters_json, (list))):
        raise ValueError("The parameter " + name + " is not a valid array")
    
    filters = ProxyUserIPFilterModel.schema().load(filters_json, many=True)
    return filters

class Modems(Resource):
    # @jwt_required()
    def get(self):
        server = ServerModel.find_by_id(1)

        if not server:
            return {"message": "Item not found"}, 404

        modems = server.modems()
        
        items = [item.json() for item in modems]

        for x, item in enumerate(items):
            imodem = IModem(server_modem_model = modems[x], settings = app.settings)
            item['is_connected'] = imodem.is_connected()
    
        return {"items": items}, 200
    

_modem_put_parser = reqparse.RequestParser()
_modem_put_parser.add_argument("proxy", type=dict, required=False)
_modem_put_parser.add_argument("modem", type=dict, required=False)
_modem_put_parser.add_argument("usb", type=dict, required=False)
_modem_put_parser.add_argument("prevent_same_ip_users", type=bool, required=False)
_modem_put_parser.add_argument("auto_rotate", type=bool, required=False)
_modem_put_parser.add_argument("auto_rotate_time", type=int, required=False)
_modem_put_parser.add_argument("auto_rotate_hard_reset", type=bool, required=False)
_modem_put_parser.add_argument("auto_rotate_filter", type=filters_type, location="json", required=False)

class Modem(Resource):
    # @jwt_required()
    def get(self, modem_id):
        server_modem = ServerModemModel.find_by_modem_id(modem_id)
        imodem = IModem(server_modem_model = server_modem, settings = app.settings)           

        json = server_modem.json()

        imodem_is_connected = imodem.is_connected()

        json['is_connected'] = imodem_is_connected

        if imodem_is_connected != True:
            return json

        device_middleware = imodem.get_device_middleware()

        device_details = device_middleware.details()
        network_type = device_details['network_type'] if device_details else None
        network_provider = device_details['network_provider'] if device_details else None
        signalbar = device_details['signalbar'] if device_details else None
        
        imodem_iface = imodem.iface()
        modem_ifaddress = imodem_iface.ifaddresses[0]   
            
        json['interface'] = imodem_iface.interface
        json['internal_ip'] = modem_ifaddress['addr']

        json['device_network_type'] = network_type
        json['device_network_provider'] = network_provider
        json['device_network_signalbar'] = signalbar

        json['data'] = {
            'receive': {
                'bytes': 9123381                
            },
            'transmit': {
                'bytes': 3790765
            }
        }

        json['external_ip_through_device'] = imodem.external_ip_through_device(silence_mode=True)

        proxy_is_alive = False
        try:
            json['external_ip_through_proxy'] = imodem.external_ip_through_proxy()
            proxy_is_alive = True
        except requests.exceptions.ConnectionError as e:
            json['external_ip_through_proxy'] = None
            json['external_ip_through_proxy_error'] = str(e)            

        json['proxy_is_alive'] = True if proxy_is_alive == True else False

        if proxy_is_alive == True:
            json['proxy_dns'] = ['8.8.8.8', '8.8.4.4']

        return json

    # @jwt_required()
    def put(self, modem_id):
        server_modem = ServerModemModel.find_by_modem_id(modem_id)

        data = _modem_put_parser.parse_args()

        data_modem = data['modem']
        if data_modem != None:
            if 'addr_id' in data_modem and data_modem['addr_id'] != None:
                server_modem.modem.addr_id = data_modem['addr_id']
                
            server_modem.modem.save_to_db()

        data_proxy = data['proxy']
        if data_proxy != None:
            if 'ipv4' in data_proxy and 'http' in data_proxy['ipv4'] and 'port' in data_proxy['ipv4']['http'] and data_proxy['ipv4']['http']['port'] != None:
                server_modem.proxy_ipv4_http_port = data_proxy['ipv4']['http']['port']

            if 'ipv4' in data_proxy and 'socks' in data_proxy['ipv4'] and 'port' in data_proxy['ipv4']['socks'] and data_proxy['ipv4']['socks']['port'] != None:
                server_modem.proxy_ipv4_socks_port = data_proxy['ipv4']['socks']['port']

            if 'auth_type' in data_proxy and data_proxy['auth_type'] != None:
                server_modem.proxy_auth_type = ProxyAuthType(data_proxy['auth_type'])
        
        data_usb = data['usb']
        if data_usb != None:
            if 'id' in data_usb and data_usb['id'] != None:
                server_modem.usb_port_id = data_usb['id']

        data_prevent_same_ip_users = data['prevent_same_ip_users']
        if data_prevent_same_ip_users != None:
            server_modem.prevent_same_ip_users = data_prevent_same_ip_users

        data_auto_rotate = data['auto_rotate']
        if data_auto_rotate != None:
            server_modem.auto_rotate = data_auto_rotate

        data_auto_rotate_time = data['auto_rotate_time']
        if data_auto_rotate_time != None:
            server_modem.auto_rotate_time = data_auto_rotate_time

        data_auto_rotate_hard_reset = data['auto_rotate_hard_reset']
        if data_auto_rotate_hard_reset != None:
            server_modem.auto_rotate_hard_reset = data_auto_rotate_hard_reset

        data_auto_rotate_filter = data['auto_rotate_filter']
        server_modem.auto_rotate_filter = data_auto_rotate_filter

        server_modem.save_to_db()

        app.modems_service.reload_modems()
        
        app.server_control.emit(ServerControlEvent(action = ServerControlAction.MODEM_RELOAD, data = {'modem': {'id': modem_id}}))

        return {"message": "OK"}, 200


_server_modem_reboot_parser = reqparse.RequestParser()
_server_modem_reboot_parser.add_argument(
    "hard_reset", type=bool, required=True, help=""
)
class ModemReboot(Resource):
    # @jwt_required()
    def post(self, modem_id): 
        server_modem_model = ServerModemModel.find_by_modem_id(modem_id)

        modem_log_model = ModemLogModel(
            modem_id=modem_id,
            owner=ModemLogOwner.USER, 
            type=ModemLogType.INFO, 
            message='app.log.modem.reboot.start',
            logged_at = datetime.now()
        )
        modem_log_model.save_to_db()

        app.server_event.emit(Event(type = EventType.MODEM_LOG, data = modem_log_model))

        callback = lambda modem_log_model: app.server_event.emit(Event(type = EventType.MODEM_LOG, data = modem_log_model))
        imodem = IModem(server_modem_model = server_modem_model, callback = callback, settings = app.settings)

        data = _server_modem_reboot_parser.parse_args()

        try:
            app.modems_manager.reboot(
                infra_modem = imodem, 
                hard_reset = data['hard_reset']
            )     
        except ModemLockedByOtherThreadException as err:
            return {
                "error": {
                    "code": 780,
                    "message": str(err)
                }                
            }, 400 
        except OSError as error:
            return {
                "error": {
                    "code": error.errno,
                    "message": str(error)
                }                
            }, 500

        return {"message": "OK"}, 200


_server_modem_rotate_parser = reqparse.RequestParser()
_server_modem_rotate_parser.add_argument(
    "hard_reset", type=bool, required=True, help=""
)
_server_modem_rotate_parser.add_argument(
    "proxy_username", type=str, required=False, help=""
)
_server_modem_rotate_parser.add_argument(
    "filters", type=filters_type, location="json", required=False, help=""
)
class ModemRotate(Resource):
    def delete(self, modem_id):
        server_modem = ServerModemModel.find_by_modem_id(modem_id)
        imodem = IModem(server_modem_model = server_modem, settings = app.settings)
        try:
            app.modems_manager.stop_task(infra_modem = imodem, callback = None)

            modem_log_model = ModemLogModel(
                modem_id=modem_id,
                owner=ModemLogOwner.USER, 
                type=ModemLogType.INFO, 
                message='app.log.modem.rotate.stop.by_user',
                logged_at = datetime.now()
            )
            modem_log_model.save_to_db()

            app.server_event.emit(Event(type = EventType.MODEM_LOG, data = modem_log_model))
        except NoTaskRunningException as err:
            return {
                "error": {
                    "code": 790,
                    "message": str(err)
                }                
            }, 400        

        return {"message": "OK"}, 200

    # @jwt_required()
    def post(self, modem_id): 
        server_modem_model = ServerModemModel.find_by_modem_id(modem_id)

        modem_log_model = ModemLogModel(
            modem_id=modem_id,
            owner=ModemLogOwner.USER, 
            type=ModemLogType.INFO, 
            message='app.log.modem.rotate.start',
            logged_at = datetime.now()
        )
        modem_log_model.save_to_db()
        
        app.server_event.emit(Event(type = EventType.MODEM_LOG, data = modem_log_model))

        callback = lambda modem_log_model: app.server_event.emit(Event(type = EventType.MODEM_LOG, data = modem_log_model))
        imodem = IModem(server_modem_model = server_modem_model, callback = callback, settings = app.settings)   

        data = _server_modem_rotate_parser.parse_args() 

        filters = data['filters']

        proxy_username = data['proxy_username']
        proxy_user_id = None
        if proxy_username:
            proxy_user = ProxyUserModel.find_by_username(proxy_username)
            if proxy_user:
                proxy_user_id = proxy_user.id
            else:
                proxy_user_model = ProxyUserModel(username = proxy_username)
                proxy_user_model.save_to_db()
                proxy_user_id = proxy_user_model.id

        if proxy_user_id and filters:
            for filter in filters:
                filter.proxy_user_id = proxy_user_id
                filter.modem_id = modem_id
                filter.save_to_db()
        
        try:
            app.modems_manager.rotate(
                infra_modem = imodem, 
                proxy_user_id = proxy_user_id,
                proxy_username = proxy_username,
                filters = filters, 
                hard_reset = data['hard_reset'], 
                not_changed_try_count = 3, 
                not_ip_try_count = 3
            )     
        except ModemLockedByOtherThreadException as err:
            return {
                "error": {
                    "code": 780,
                    "message": str(err)
                }                
            }, 400        

        return {"message": "OK"}, 200


_server_modem_diagnose_parser = reqparse.RequestParser()
# _server_modem_diagnose_parser.add_argument(
#     "hard_reset", type=bool, required=True, help=""
# )
class ModemDiagnose(Resource):
    def delete(self, modem_id):
        server_modem = ServerModemModel.find_by_modem_id(modem_id)
        imodem = IModem(server_modem_model = server_modem, settings = app.settings)
        try:
            app.modems_manager.stop_task(infra_modem = imodem, callback = None)

            # modem_log_model = ModemLogModel(
            #     modem_id=modem_id,
            #     owner=ModemLogOwner.USER, 
            #     type=ModemLogType.INFO, 
            #     message='app.log.modem.rotate.stop.by_user',
            #     logged_at = datetime.now()
            # )
            # modem_log_model.save_to_db()

            # app.server_event.emit(Event(type = EventType.MODEM_LOG, data = modem_log_model))
        except NoTaskRunningException as err:
            return {
                "error": {
                    "code": 790,
                    "message": str(err)
                }                
            }, 400        

        return {"message": "OK"}, 200
    
    # @jwt_required()
    def post(self, modem_id): 
        server_modem_model = ServerModemModel.find_by_modem_id(modem_id)

        modem_diagnose_model = ModemDiagnoseModel(
            modem_id=modem_id,
            owner=ModemDiagnoseOwner.USER, 
            type=ModemDiagnoseType.INFO, 
            message='app.modem.diagnose.start',
            logged_at = datetime.now()
        )
        app.server_event.emit(Event(type = EventType.MODEM_DIAGNOSE, data = modem_diagnose_model))

        callback = lambda modem_diagnose_model: app.server_event.emit(Event(type = EventType.MODEM_DIAGNOSE, data = modem_diagnose_model))
        imodem = IModem(server_modem_model = server_modem_model, callback = callback, settings = app.settings)

        data = _server_modem_diagnose_parser.parse_args()

        try:
            app.modems_manager.diagnose(
                infra_modem = imodem 
                # hard_reset = data['hard_reset']
            )     
        except ModemLockedByOtherThreadException as err:
            return {
                "error": {
                    "code": 780,
                    "message": str(err)
                }                
            }, 400 
        except OSError as error:
            return {
                "error": {
                    "code": error.errno,
                    "message": str(error)
                }                
            }, 500

        return {"message": "OK"}, 200
    

class ModemLogs(Resource):
    # @jwt_required()
    def get(self, modem_id):
        modem_model = ModemModel.find_by_id(modem_id)

        if not modem_model:
            return {"message": "Modem not found"}, 404
        
        args = request.args
        cursor = args['cursor'] if 'cursor' in args else None
        limit = args['limit'] if 'limit' in args else None
        direction = PaginateDirection(args['direction']) if 'direction' in args else PaginateDirection.NEXT
        order = PaginateOrder(args['order']) if 'order' in args else PaginateOrder.DESC
        
        logs = ModemLogModel.paginate_by_id(id = modem_id, cursor = cursor, limit = limit, direction = direction, order = order)

        items = ModemLogModel.schema().dump(logs, many=True)
    
        return {"items": items}, 200

        
class ModemScheduleAutoRotate(Resource):
    # @jwt_required()
    def get(self, modem_id):
        server_modem_model = ServerModemModel.find_by_modem_id(modem_id)

        if not server_modem_model:
            return {"message": "Modem not found"}, 404
        
        agenda_item = app.modems_auto_rotate_service.schedule.in_agenda_items(server_modem_model)

        if not agenda_item:
            return None, 200
        
        agenda_item.now = datetime.now()
        return ModemsAutoRotateAgendaItem.schema().dump(agenda_item), 200
    

# _modem_lock_wizard_step_response_parser = reqparse.RequestParser()

class ModemLockWizardStepResponse(Resource):
    # @jwt_required()
    def post(self, modem_id, lock_id, step_id):
        server_modem_model = ServerModemModel.find_by_modem_id(modem_id)

        if not server_modem_model:
            return {"message": "Modem not found"}, 404
        
        thread = app.modems_manager.thread_by_id(lock_id)
        step = thread.wizard.step_by_id(step_id)

        data = request.get_json(force=True)
        step.response = data

        return {"message": "OK"}, 200