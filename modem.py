from ast import Not
from pickle import TRUE
import requests
import sys
import sys
import argparse

from framework.models.installation import Installation
from framework.models.server import Server
from framework.models.modem import Modem
from framework.models.modemserver import ModemServer

from framework.infra.modem import Modem as InfraModem

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

    server = Server.get_by_id(1)
    modem = Modem.get_by_id(_args.modem_id)
    modemserver = ModemServer.get_by_server_and_modem(server, modem)

    inframodem = InfraModem(modemserver)
    
    if _args.diagnose:
        pass

    elif _args.usb_reboot:
        inframodem.hard_reboot()

    elif _args.usb_turn_off:
        inframodem.hard_turn_off()

    elif _args.info:        
        is_connected = inframodem.is_connected()    
        device = modem.get_device()        

        sys.stdout.write('{0}[*] Device model: {1}{2}\n'.format(CBLUE, device.model, CEND))
        sys.stdout.write('{0}[*] Device type: {1}{2}\n'.format(CBLUE, device.type, CEND))
        sys.stdout.write('{0}[*] Addr id: {1}{2}\n'.format(CBLUE, modem.addr_id, CEND))
        sys.stdout.write('{0}[*] USB port: {1}{2}\n'.format(CBLUE, modemserver.usb_port, CEND))
        sys.stdout.write('{0}[*] Proxy port: {1}{2}\n'.format(CBLUE, modemserver.get_usb_port().port, CEND))
        sys.stdout.write('{0}[*] Status: {1}{2}\n'.format(CBLUE, CGREEN if is_connected else CRED, 'connected' if is_connected else 'disconnected', CEND))

        if is_connected == True:
            device_middleware = inframodem.get_device_middleware()

            device_details = device_middleware.details()
            network_type = device_details['network_type'] if device_details else None
            network_provider = device_details['network_provider'] if device_details else None
            signalbar = device_details['signalbar'] if device_details else None
            
            inframodem_iface = inframodem.iface()
            modem_ifaddress = inframodem_iface.ifaddresses[0]

            sys.stdout.write('{0}[*] Interface: {1}{2}\n'.format(CBLUE, inframodem_iface.interface, CEND))
            sys.stdout.write('{0}[*] Internal IP: {1}{2}\n'.format(CBLUE, modem_ifaddress['addr'], CEND))
            sys.stdout.write('{0}[*] Device network type: {1}{2}\n'.format(CBLUE, network_type, CEND))
            sys.stdout.write('{0}[*] Device network provider: {1}{2}\n'.format(CBLUE, network_provider, CEND))
            sys.stdout.write('{0}[*] Device network signalbar: {1}{2}\n'.format(CBLUE, signalbar, CEND))
            sys.stdout.write('{0}[*] External IP (through device): {1}{2}\n'.format(CBLUE, inframodem.external_ip_through_device(silence_mode=True), CEND))        

            external_ip_proxy = None
            proxy_alive = False
            try:
                external_ip_proxy = inframodem.external_ip_through_proxy()
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
        inframodem.rotate(_args.ip_match, _args.user, _args.hard_reset)



if __name__ == '__main__':
	main()


#SELECT uip.*, iih.* FROM user_ip_history uip JOIN modem_ip_history iih ON (iih.id = uip.modem_ip_history_id)