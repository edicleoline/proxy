from ast import Not
import requests
import time
import sys
import base64
import os
import pymysql
import configparser
import fcntl, sys
import argparse

from framework.util.config import Config
from framework.util.database import Database

from framework.models.installation import Installation
from framework.models.server import Server
from framework.models.modem import Modem
from framework.models.modemserver import ModemServer
from framework.models.modemiphistory import ModemIpHistory

from framework.infra.netiface import NetIface
from framework.infra.modem import Modem as InfraModem
from framework.infra.usb import USB
from framework.infra.route import Route
from framework.infra.proxyservice import ProxyService

from framework.device.zte.mf79s import MF79S
from framework.device.zte.error.exception import ConnectException
from framework.util.lan import Lan


CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

class UserIpHistory:
    def __init__(self):
        self.database = database

    def is_ip_reserved_for_other(self, ip, user_email):
        connection = self.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select iih.*, uih.* from modem_ip_history iih left join user_ip_history uih ON (uih.modem_ip_history_id = iih.id) where iih.ip = %s and uih.user <> %s', (ip, user_email))
        rows = cursor.fetchall()
        exists = len(rows) > 0
        connection.close()
        return exists

    def get_last_ip(self, user_email):
        connection = self.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('select iih.id, iih.ip from user_ip_history uih join modem_ip_history iih ON (iih.id = uih.modem_ip_history_id) where uih.user = %s order by uih.id desc limit 1', (user_email))
        row = cursor.fetchone()
        connection.close()
        return row[1] if row else None
        

    def add(self, user_email, modem_ip_history_id):
        connection = self.database.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO user_ip_history (user, modem_ip_history_id) VALUES (%s, %s)', (user_email, modem_ip_history_id))
        id = cursor.lastrowid
        connection.commit()
        connection.close()
        return id

def get_device_middleware(device, interface, gateway, username, password):
    middleware = None
    if True:#device != None:
        if True:#modem.model == 'MF79S':
            device = MF79S(interface = interface, gateway = gateway, password = password, retries = 5, retries_ip = 15)

    return device

def wait_until_modem_connection(inframodem, print_alert = False):
    write_alert = True
    while(True):
        inframodem_iface = inframodem.iface()

        if inframodem_iface != None:
            break
        else:
            if print_alert and write_alert:
                sys.stdout.write('{0}[!] This modem is offline. Let''s wait until get online back...{1}\n'.format(CRED, CEND))
                sys.stdout.flush()

        write_alert = False
        time.sleep(1)

def get_args():
    parser = argparse.ArgumentParser(description='')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--modem', dest='modem_id', help='Modem ID')
    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument('--diagnose', dest='diagnose', help='Execute diagnose []', action='store_true')
    group2.add_argument('--rotate', dest='rotate', help='Rotate IPv4', action='store_true')
    group2.add_argument('--usb-reboot', dest='usb_reboot', help='Reboot USB', action='store_true')
    group2.add_argument('--info', dest='info', help='Show details about modem, connection and proxy', action='store_true')

    parser.add_argument('--hard-reset', dest='hard_reset', help='Use USB hard reset', action='store_true')
    parser.add_argument('--user', dest='user', help='User email')
    parser.add_argument('--match', dest='ip_match', help='IPv4 match')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

def main():
    global _args, server, modem, database
    
    _args = get_args()

    database = Database.get_database()

    server = Server.get_by_id(1)
    modem = Modem.get_by_id(_args.modem_id)
    modemserver = ModemServer.get_by_server_and_modem(server, modem)
    modem_usb_port = modemserver.usb_port
    proxy_port = modemserver.proxy_port

    inframodem = InfraModem(modemserver)
    
    user_ip_history = UserIpHistory()    
    
    if _args.diagnose:    
        pass

    elif _args.usb_reboot:
        sys.stdout.write('{0}[!] Let''s reboot USB port {1}...{2}'.format(CYELLOW, modem_usb_port, CEND))
        sys.stdout.flush()
        USB().hard_reboot(modem_usb_port)
        sys.stdout.write('{0} OK{1}\n'.format(CGREEN, CEND))
        sys.stdout.flush()

    elif _args.rotate:
        inframodem_iface, device_middleware, modem_ifaddress = None, None, None
        user_email = _args.user
        ip_match = _args.ip_match

        if ip_match == None and user_email:
            user_last_ip = user_ip_history.get_last_ip(user_email)
            if user_last_ip:
                ip_match = ".".join(user_last_ip.split(".", 2)[:2])  
                sys.stdout.write('{0}[!] IPv4 match auto enabled for [{1}]{2}\n\n'.format(CGREEN, ip_match, CEND))
                sys.stdout.flush()
        
        while True:
            ip = None            
        
            if _args.hard_reset:
                sys.stdout.write('{0}[!] Let''s reboot USB port {1}...{2}'.format(CYELLOW, modem_usb_port, CEND))
                sys.stdout.flush()
                USB().hard_reboot(modem_usb_port)
                sys.stdout.write('{0} OK{1}\n'.format(CGREEN, CEND))
                sys.stdout.write('{0}[!] Reboot signal sent. Now, let''s wait modem reboot (about 1 minute)...{1}\n'.format(CBLUE, CEND))
                sys.stdout.flush()

                wait_until_modem_connection(inframodem, False)
                sys.stdout.write('{0}[!] Modem rebooted. Wait until to get external IP...{1}\n'.format(CBLUE, CEND))
                sys.stdout.flush()
                time.sleep(30)

                wait_until_modem_connection(inframodem, True)
                inframodem_iface = inframodem.iface()
                modem_ifaddress = inframodem_iface.ifaddresses[0]
                modem_gateway = NetIface.get_gateway_from_ipv4(ipv4 = modem_ifaddress['addr'])

                device_middleware = get_device_middleware(device = None, interface = inframodem_iface.interface, gateway = modem_gateway, username = "vivo", password = "vivo")
                ip = device_middleware.wan.try_get_current_ip(device_middleware.interface, 30)

            else:
                wait_until_modem_connection(inframodem, True)
                inframodem_iface = inframodem.iface()
                modem_ifaddress = inframodem_iface.ifaddresses[0]
                modem_gateway = NetIface.get_gateway_from_ipv4(ipv4 = modem_ifaddress['addr'])
                device_middleware = get_device_middleware(device = None, interface = inframodem_iface.interface, gateway = modem_gateway, username = "vivo", password = "vivo")

                try:                    
                    ip = device_middleware.release()
                except ConnectException as e:
                    sys.stdout.write('{0}[!] Run diagnose and try to fix{1}\n'.format(CBLUE, CEND))
                    sys.stdout.flush()
                    sys.exit(1)

            if ip != None:
                modem_details = device_middleware.details()
                network_type = modem_details['network_type'] if modem_details else None
                network_provider = modem_details['network_provider'] if modem_details else None
                signalbar = modem_details['signalbar'] if modem_details else None
                ip_history_id = ModemIpHistory.add(modem.id, ip, network_type, network_provider, signalbar)

                if user_email:
                    is_ip_reserved_for_other = user_ip_history.is_ip_reserved_for_other(ip, user_email)
                    if is_ip_reserved_for_other:
                        sys.stdout.write('{0}[!] Lets rotate again because this IP is reserved for another user{1}\n'.format(CBLUE, CEND))
                        sys.stdout.flush()
                        time.sleep(1)
                        print('\n')
                        continue 

                if ip_match:
                    if ip.startswith(ip_match):
                        if user_email:
                            user_ip_history.add(user_email, ip_history_id)

                        #/usr/local/3proxy/conf/3proxy.cfg
                        #sudo sh /etc/3proxy/conf/add3proxyuser.sh test 123                        

                        proxyService = ProxyService(ip=modem_ifaddress['addr'], port=proxy_port)
                        proxyService.resolve_proxy()

                        route = Route(gateway=modem_gateway, interface=inframodem_iface.interface, ip=modem_ifaddress['addr'], table=modem.id)
                        route.resolve_route()

                        sys.exit(1)
                    else:
                        sys.stdout.write('{0}[!] Lets rotate again because this IP does not match [{1}] {2}\n'.format(CBLUE, ip_match, CEND))
                        sys.stdout.flush()
                        time.sleep(1)
                        print('\n')
                        continue

                if user_email:
                    user_ip_history.add(user_email, ip_history_id)
                    break

            print('\n')
            time.sleep(1)



if __name__ == '__main__':
	main()


#SELECT uip.*, iih.* FROM user_ip_history uip JOIN modem_ip_history iih ON (iih.id = uip.modem_ip_history_id)