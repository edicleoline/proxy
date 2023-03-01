import requests
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from framework.models.server import Server as ServerModel, ServerModem as ServerModemModel
from models.serverstatus import ServerStatus as ServerStatusModel

from framework.infra.modem import Modem as IModem

class ServerModem(Resource):
    @jwt_required()
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


        

    