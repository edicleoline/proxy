from datetime import datetime
import os
import requests
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from framework.manager.error.exception import ModemLockedByOtherThreadException, NoTaskRunningException
from framework.models.modemlog import ModemLogModel, ModemLogOwner, ModemLogType
from framework.models.proxyuser import ProxyUserModel
from framework.models.proxyuseripfilter import ProxyUserIPFilterModel
from framework.models.server import ServerModel, ServerModemModel
from framework.infra.modem import Modem as IModem
from time import sleep
import threading
from flask import request
import json

from app import app

class ServerModem(Resource):
    # @jwt_required()
    def get(self, modem_id):
        
        server = ServerModel.find_by_id(1)

        if not server:
            return {"message": "Item not found"}, 404

        server_modem = ServerModemModel.find_by_modem_id(modem_id)
        imodem = IModem(server_modem)           

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


_server_modem_reboot_parser = reqparse.RequestParser()
_server_modem_reboot_parser.add_argument(
    "hard_reset", type=bool, required=True, help=""
)
class ServerModemReboot(Resource):
    # @jwt_required()
    def post(self, modem_id): 
        server = ServerModel.find_by_id(1)

        if not server:
            return {"message": "Item not found"}, 404

        server_modem = ServerModemModel.find_by_modem_id(modem_id)
        imodem = IModem(server_modem)   

        data = _server_modem_reboot_parser.parse_args()

        try:
            app.modems_manager.reboot(
                infra_modem = imodem, 
                hard_reset = data['hard_reset'], 
                callback = None
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
    

def filters_type(value, name):
    full_json_data = request.get_json()
    filters_json = full_json_data[name]

    if(not isinstance(filters_json, (list))):
        raise ValueError("The parameter " + name + " is not a valid array")
    
    filters = ProxyUserIPFilterModel.schema().load(filters_json, many=True)
    return filters

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
class ServerModemRotate(Resource):
    def delete(self, modem_id):
        server_modem = ServerModemModel.find_by_modem_id(modem_id)
        imodem = IModem(server_modem)
        try:
            app.modems_manager.stop_task(infra_modem = imodem, callback = None)

            modem_log_model = ModemLogModel(
                modem_id=modem_id,
                owner=ModemLogOwner.USER, 
                type=ModemLogType.WARNING, 
                message='Cancelar rotacionamento',
                logged_at = datetime.now()
            )
            modem_log_model.save_to_db()
            app.socketio.emit('modem_log', json.loads(modem_log_model.to_json()), broadcast=True)
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
        server = ServerModel.find_by_id(1)

        if not server:
            return {"message": "Item not found"}, 404
        
        server_modem_model = ServerModemModel.find_by_modem_id(modem_id)

        modem_log_model = ModemLogModel(
            modem_id=modem_id,
            owner=ModemLogOwner.USER, 
            type=ModemLogType.INFO, 
            message='Iniciar rotacionamento',
            logged_at = datetime.now()
        )
        modem_log_model.save_to_db()
        app.socketio.emit('modem_log', json.loads(modem_log_model.to_json()), broadcast=True)

        callback = lambda modem_log_model: app.socketio.emit('modem_log', json.loads(modem_log_model.to_json()), broadcast=True)
        imodem = IModem(server_modem_model=server_modem_model, callback=callback)   

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

    