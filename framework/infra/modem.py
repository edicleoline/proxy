import sys, time
import requests

from framework.models.server import ServerModemModel
from framework.models.modemiphistory import ModemIPHistoryModel
from framework.models.proxyuseriphistory import ProxyUserIPHistoryModel

from framework.infra.netiface import NetIface
from framework.infra.usb import USB
from framework.infra.route import Route
from framework.infra.proxyservice import ProxyService

from framework.device.zte.mf79s import MF79S
from framework.device.zte.error.exception import ConnectException

from datetime import datetime
from enum import Enum

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

class RotateError(Enum):
    IP_NOT_CHANGED  = 300
    NO_PUBLIC_IP    = 301

class Modem:
    def __init__(self, server_modem_model: ServerModemModel):
        self.server_modem_model = server_modem_model
        self.modem = self.server_modem_model.modem()

    def iface(self):
        addr_id = self.modem.addr_id
        return NetIface.get_iface_by_addr_id(addr_id)        

    def hard_reboot(self):
        """Reboot USB port by cut power.       
        """                
        usb_port = self.server_modem_model.usb_port()
        sys.stdout.write('{0}[!] Let''s reboot USB port {1}...{2}'.format(CYELLOW, usb_port.port, CEND))
        sys.stdout.flush()
        USB(server=self.server_modem_model.server()).hard_reboot(usb_port=usb_port)
        sys.stdout.write('{0} OK{1}\n'.format(CGREEN, CEND))
        sys.stdout.flush()

    def hard_reboot_and_wait(self):
        self.hard_reboot()
        self.wait_until_modem_connection(print_alert = False)

    def hard_turn_off(self):
        """Turn off USB port.
        """        
        usb_port = self.server_modem_model.usb_port()
        sys.stdout.write('{0}[!] Let''s turn off USB port {1}...{2}'.format(CYELLOW, usb_port.port, CEND))
        sys.stdout.flush()
        USB(server=self.server_modem_model.server()).hard_turn_off(usb_port=usb_port)
        sys.stdout.write('{0} OK{1}\n'.format(CGREEN, CEND))
        sys.stdout.flush()

    def get_device_middleware(self, retries_ip = 5):
        middleware = None

        iface = self.iface()
        if iface == None:
            return None

        if iface.ifaddresses == None:
            return None

        ifaddress = iface.ifaddresses[0]
        gateway = NetIface.get_gateway_from_ipv4(ipv4 = ifaddress['addr'])

        if True:#device != None:
            if True:#modem.model == 'MF79S':
                middleware = MF79S(addr_id = self.modem.addr_id, interface = iface.interface, gateway = gateway, password = 'vivo', retries_ip = retries_ip)

        return middleware

    def wait_until_modem_connection(self, print_alert = False):
        write_alert = True
        while(True):
            inframodem_iface = self.iface()

            if inframodem_iface != None:
                break
            else:
                if print_alert and write_alert:
                    sys.stdout.write('{0}[!] This modem is offline. Let''s wait until get online back...{1}\n'.format(CRED, CEND))
                    sys.stdout.flush()

            write_alert = False
            time.sleep(1)

    def rotate(self, filters = None, proxy_user_id = None, hard_reset = False, not_changed_try_count = 3, not_ip_try_count = 3, callback = None):
        r"""
        Rotate IP

        ip_match: stops when match IP addr. Use multiple IPs separate by comma.
        """ 

        device_middleware = None

        # if ip_match == None and user:
        #     user_last_ip = ProxyUserIPHistoryModel.get_last_ip(user)
        #     if user_last_ip:
        #         ip_match = ".".join(user_last_ip.split(".", 2)[:2])  
        #         sys.stdout.write('{0}[!] IPv4 match auto enabled for [{1}]{2}\n\n'.format(CGREEN, ip_match, CEND))
        #         sys.stdout.flush()
        
        not_changed_count, not_ip_count = 0, 0
        while True:            
            old_ip, new_ip, done = None, None, False

            device_middleware = self.get_device_middleware()
            if device_middleware:
                old_ip = device_middleware.wan.try_get_current_ip(retries=2)
        
            if hard_reset == True:
                self.hard_reboot()
                sys.stdout.write('{0}[!] Reboot signal sent. Now, let''s wait modem reboot (about 1 minute)...{1}\n'.format(CBLUE, CEND))
                sys.stdout.flush()
                self.wait_until_modem_connection(False)
                sys.stdout.write('{0}[!] Modem rebooted. Wait until to get external IP...{1}\n'.format(CBLUE, CEND))
                sys.stdout.flush()
                time.sleep(30)

                self.wait_until_modem_connection(True)
                
                device_middleware = self.get_device_middleware()
                new_ip = device_middleware.wan.try_get_current_ip(retries=30)

            else:
                self.wait_until_modem_connection(True)                                

                device_middleware = self.get_device_middleware()

                if callback: callback(self.modem.id, "Releasing", datetime.now(), None)
                try:                    
                    new_ip = device_middleware.release()
                except ConnectException as e:
                    sys.stdout.write('{0}[!] Run diagnose and try to fix{1}\n'.format(CBLUE, CEND))
                    sys.stdout.flush()
                    sys.exit(1)

                # new_ip = '189.40.89.35' #TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
                if callback: callback(self.modem.id, "Released with IPv4 {0}".format(new_ip), datetime.now(), None)

            if new_ip != None and new_ip != old_ip:
                modem_details = device_middleware.details()
                network_type = modem_details['network_type'] if modem_details else None
                network_provider = modem_details['network_provider'] if modem_details else None
                signalbar = modem_details['signalbar'] if modem_details else None

                modem_ip_history = ModemIPHistoryModel(modem_id = self.modem.id, ip = new_ip, network_type = network_type, network_provider = network_provider, signalbar = signalbar)
                modem_ip_history.save_to_db()

                inframodem_iface = self.iface()
                modem_ifaddress = inframodem_iface.ifaddresses[0]
                modem_gateway = NetIface.get_gateway_from_ipv4(ipv4 = modem_ifaddress['addr'])

                if proxy_user_id:
                    is_ip_reserved_for_other = ProxyUserIPHistoryModel.is_ip_reserved_for_other(ip=new_ip, proxy_user_id=proxy_user_id)
                    if is_ip_reserved_for_other:
                        sys.stdout.write('{0}[!] Lets rotate again because this IP is reserved for another user{1}\n'.format(CBLUE, CEND))
                        sys.stdout.flush()
                        time.sleep(1)
                        print('\n')
                        continue 

                if filters != None and len(filters) > 0:
                    ip_match_found = False
                    for filter in filters:                        
                        if filter.type == 'ip' and new_ip.startswith(filter.value.strip()):
                            done = True
                            ip_match_found = True
                        
                    if ip_match_found == False:
                        sys.stdout.write('{0}[!] Lets rotate again because this IP does not match with filter {1}\n'.format(CBLUE, CEND))
                        sys.stdout.flush()
                        time.sleep(1)
                        print('\n')
                        continue
                else:
                    done = True
            
                if done == True:
                    if proxy_user_id:
                        proxy_user_ip_history_model = ProxyUserIPHistoryModel(proxy_user_id = proxy_user_id, modem_ip_history_id = modem_ip_history.id)
                        proxy_user_ip_history_model.save_to_db()

                    proxyService = ProxyService(ip=modem_ifaddress['addr'], proxy_ipv4_http_port=self.server_modem_model.proxy_ipv4_http_port)
                    proxyService.resolve_proxy()

                    route = Route(gateway=modem_gateway, interface=inframodem_iface.interface, ip=modem_ifaddress['addr'], table=self.modem.id)
                    route.resolve_route()

                    break

            elif new_ip != None and new_ip == old_ip:
                not_changed_count = not_changed_count + 1
                if callback: callback(self.modem.id, "Lets release again because IP not changed", datetime.now(), None)
                sys.stdout.write('{0}[!] Lets rotate again because this IP does not changed{1}\n'.format(CBLUE, CEND))
                sys.stdout.flush()

            elif new_ip == None:
                not_ip_count = not_ip_count + 1
                if callback: callback(self.modem.id, "Lets try release again because there is no IP", datetime.now(), None)

            if not_changed_count >= not_changed_try_count:
                if callback: callback(self.modem.id, "Stopping threading because your IP not changed after {0} times".format(not_changed_try_count), datetime.now(), RotateError.IP_NOT_CHANGED)
                sys.stdout.write('{0}[!] Stopping threading because your IP not changed after {1} times{2}\n'.format(CBLUE, not_changed_try_count, CEND))
                sys.stdout.flush()
                break

            if not_ip_count >= not_ip_try_count:
                if callback: callback(self.modem.id, "Stopping threading because there is no IP. Check your SIM data plan.", datetime.now(), RotateError.NO_PUBLIC_IP)
                break

            print('\n')
            time.sleep(1)

    def external_ip_through_device(self, silence_mode = False, retries=2):
        device_middleware = self.get_device_middleware()
        if device_middleware == None:
            return None
        return device_middleware.wan.try_get_current_ip(retries=retries, silence_mode=silence_mode)

    def external_ip_through_proxy(self):
        proxies = { 
              "http" : 'http://{0}:{1}'.format('127.0.0.1', self.server_modem_model.proxy_ipv4_http_port), 
              "https": 'https://{0}:{1}'.format('127.0.0.1', self.server_modem_model.proxy_ipv4_http_port), 
        }

        r = requests.get('https://ipecho.net/plain', headers=None, proxies=proxies, timeout=3)
        return r.text
    
    def is_connected(self):
        inframodem_iface = self.iface()
        return True if inframodem_iface != None else False

    def ussd(self):
        """Send USSD to SIM card.
        """
        pass

    def install(self):
        pass

    def uninstall(self):
        pass