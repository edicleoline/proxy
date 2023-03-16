from framework.models.server import ServerModel
from framework.infra.modem import Modem as IModem
import json, hashlib
import random
from app import app

class ModemsService():
    def __init__(self, server_model: ServerModel):
        self.server_model = server_model
        self.server_modems = self.server_model.modems()

    def get_lock(self, infra_modem: IModem):
        return app.modems_manager.running(infra_modem)

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
                    'task': lock.action.name
                }

        return items

    def modems_details(self):
        items = [item.json() for item in self.server_modems]
        result = []

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

    # def equals(self, modem_list_1, modem_list_2):
    #     if modem_list_1 == None or modem_list_2 == None:
    #         return False

    #     modem_list_1_hash = hashlib.md5(json.dumps(modem_list_1).encode("utf-8")).hexdigest()
    #     modem_list_2_hash = hashlib.md5(json.dumps(modem_list_2).encode("utf-8")).hexdigest()
        
    #     return True if modem_list_1_hash == modem_list_2_hash else False