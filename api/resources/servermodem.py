import os
import requests
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from framework.manager.error.exception import ModemLockedByOtherThreadException
from framework.models.server import ServerModel, ServerModemModel
from framework.infra.modem import Modem as IModem
from time import sleep
import threading

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
    

_server_modem_rotate_parser = reqparse.RequestParser()
_server_modem_rotate_parser.add_argument(
    "hard_reset", type=bool, required=True, help=""
)
_server_modem_rotate_parser.add_argument(
    "user", type=str, required=False, help=""
)
_server_modem_rotate_parser.add_argument(
    "ipv4_filter", type=str, required=False, help=""
)
class ServerModemRotate(Resource):
    # @jwt_required()
    def post(self, modem_id): 
        server = ServerModel.find_by_id(1)

        if not server:
            return {"message": "Item not found"}, 404

        server_modem = ServerModemModel.find_by_modem_id(modem_id)
        imodem = IModem(server_modem)   

        data = _server_modem_rotate_parser.parse_args() 

        try:
            app.modems_manager.rotate(
                infra_modem = imodem, 
                user = data['user'] if data['user'] else None,
                filter_ip = data['ipv4_filter'] if data['ipv4_filter'] else None, 
                hard_reset = data['hard_reset'], 
                not_changed_try_count = 3, 
                not_ip_try_count = 3, 
                callback = lambda modem_id, message, datetime, error_code: 
                        app.socketio.emit(
                            'message', {
                                'modem_id': modem_id, 
                                'message': message, 
                                'datetime': datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                'error_code': int(error_code.value) if error_code != None else None
                            }, broadcast=True
                        )
            )     
        except ModemLockedByOtherThreadException as err:
            return {
                "error": {
                    "code": 780,
                    "message": str(err)
                }                
            }, 400        

        return {"message": "OK"}, 200

    