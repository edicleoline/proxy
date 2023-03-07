from ast import Not
from pickle import TRUE
import requests
import sys
import sys
import argparse

from framework.models.installation import InstallationModel
from framework.models.server import ServerModel, ServerModemModel
from framework.models.modem import ModemModel

from framework.infra.modem import Modem as IModem

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

def get_args():
    parser = argparse.ArgumentParser(description='')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--modem', dest='modem_id', help='Modem ID')
    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument('--diagnose', dest='diagnose', help='Execute diagnose', action='store_true')
    group2.add_argument('--rotate', dest='rotate', help='Rotate IPv4', action='store_true')
    group2.add_argument('--usb-reboot', dest='usb_reboot', help='Reboot USB', action='store_true')
    group2.add_argument('--usb-turn-off', dest='usb_turn_off', help='Turn off USB', action='store_true')
    group2.add_argument('--info', dest='info', help='Show details about modem status, connection and proxy', action='store_true')

    parser.add_argument('--hard-reset', dest='hard_reset', help='Use USB hard reset', action='store_true')
    parser.add_argument('--user', dest='user', help='User email')
    parser.add_argument('--match', dest='ip_match', help='IPv4 match')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

def main():
    global _args, server, modem
    
    _args = get_args()

    server = ServerModel.find_by_id(1)
    server_modem = ServerModemModel.find_by_modem_id(_args.modem_id)
    modem = server_modem.modem()

    imodem = IModem(server_modem)
    
    if _args.diagnose:
        pass

    elif _args.usb_reboot:
        imodem.hard_reboot()

    elif _args.usb_turn_off:
        imodem.hard_turn_off()

    elif _args.info:        
        is_connected = imodem.is_connected()    
        device = modem.device()
        server_modem_usb_port = server_modem.usb_port()  

        sys.stdout.write('{0}[*] Device model: {1}{2}\n'.format(CBLUE, device.model, CEND))
        sys.stdout.write('{0}[*] Device type: {1}{2}\n'.format(CBLUE, device.type, CEND))
        sys.stdout.write('{0}[*] Addr id: {1}{2}\n'.format(CBLUE, modem.addr_id, CEND))
        sys.stdout.write('{0}[*] USB port: {1}{2}\n'.format(CBLUE, server_modem_usb_port.port, CEND))
        sys.stdout.write('{0}[*] USB port status: {1}{2}\n'.format(CBLUE, server_modem_usb_port.status, CEND))
        sys.stdout.write('{0}[*] Proxy port: {1}{2}\n'.format(CBLUE, server_modem.proxy_port, CEND))
        sys.stdout.write('{0}[*] Status: {1}{2}\n'.format(CBLUE, CGREEN if is_connected else CRED, 'connected' if is_connected else 'disconnected', CEND))

        if is_connected == True:
            device_middleware = imodem.get_device_middleware()

            device_details = device_middleware.details()
            network_type = device_details['network_type'] if device_details else None
            network_provider = device_details['network_provider'] if device_details else None
            signalbar = device_details['signalbar'] if device_details else None
            
            imodem_iface = imodem.iface()
            modem_ifaddress = imodem_iface.ifaddresses[0]

            sys.stdout.write('{0}[*] Interface: {1}{2}\n'.format(CBLUE, imodem_iface.interface, CEND))
            sys.stdout.write('{0}[*] Internal IP: {1}{2}\n'.format(CBLUE, modem_ifaddress['addr'], CEND))
            sys.stdout.write('{0}[*] Device network type: {1}{2}\n'.format(CBLUE, network_type, CEND))
            sys.stdout.write('{0}[*] Device network provider: {1}{2}\n'.format(CBLUE, network_provider, CEND))
            sys.stdout.write('{0}[*] Device network signalbar: {1}{2}\n'.format(CBLUE, signalbar, CEND))
            sys.stdout.write('{0}[*] External IP (through device): {1}{2}\n'.format(CBLUE, imodem.external_ip_through_device(silence_mode=True), CEND))        

            external_ip_proxy = None
            proxy_alive = False
            try:
                external_ip_proxy = imodem.external_ip_through_proxy()
                sys.stdout.write('{0}[*] External IP (through proxy): {1}{2}\n'.format(CBLUE, external_ip_proxy, CEND))
                proxy_alive = True
            except requests.exceptions.ConnectionError as e:
                external_ip_proxy = '[ERROR]: ' + str(e)
                sys.stdout.write('{0}[*] External IP (through proxy): {1}{2}\n'.format(CBLUE, CRED, external_ip_proxy, CEND))

            sys.stdout.write('{0}[*] Proxy status: {1}{2}\n'.format(CBLUE, (CBLUE if proxy_alive else CRED), ('up' if proxy_alive else 'down'), CEND))
            
            proxy_dns = '8.8.8.8, 8.8.4.4'
            sys.stdout.write('{0}[*] Proxy DNS: {1}{2}\n'.format(CBLUE, proxy_dns, CEND))

        sys.stdout.flush()
        
    elif _args.rotate:
        imodem.rotate(_args.ip_match, _args.user, _args.hard_reset)



if __name__ == '__main__':
	main()

#SELECT uip.*, iih.* FROM user_ip_history uip JOIN modem_ip_history iih ON (iih.id = uip.modem_ip_history_id)