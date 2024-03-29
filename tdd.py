from math import floor, log
import string
from weakref import proxy
import netifaces
import sys
import os
import subprocess

from framework.models.installation import InstallationModel
# from framework.models.server import Server
# from framework.models.modem import Modem

from framework.infra.netiface import NetIface
from framework.infra.modem import Modem as InfraModem
from framework.infra.route import Route
from framework.models.modemiphistory import ModemIpHistoryModel
from framework.models.iplabelfilter import IpLabelFilterModel

from framework.models.server import ServerModel, ServerModemModel, USBPortModel, USBPortStatus
from framework.models.modem import ModemModel

from framework.models.iplabelhistory import IpLabelHistoryModel
from framework.models.installation import InstallationModel
from framework.models.user import UserModel
from framework.models.iplabel import IpLabelModel
from framework.models.modemlog import ModemLogModel, ModemLogOwner, ModemLogType

from datetime import datetime

from framework.util.format import HumanBytes

import psutil

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'


# session = Session(engine)
# stmt = select(ServerModel).where(ServerModel.name.in_(["raspberry-pi", "thifani"]))
# for user in session.scalars(stmt):
#     print(user.name)

# server = ServerModel.find_by_id(1)
# print(server.json())

# usb_port = USBPortModel.find_by_id(2)
# print(usb_port.json())

# for port in server.usb_ports():
#     print(port.server_id)

# server_modem = ServerModemModel.find_by_id(5)
# # server_modem = ServerModemModel.find_by_modem_id(6)
# print(server_modem.server().name)

# installation = USBPortModel.find_by_id(1)
# print(installation.json())

#for modem in server.modems():
#    print(modem.modem().addr_id)

#proxy_user = ProxyUserModel()
#proxy_user.username = 'João'
#proxy_user.save_to_db()

#proxy_user = ProxyUserModel()
#proxy_user.username = 'Maria'
#proxy_user.save_to_db()

#print(ProxyUserModel.find_by_username('João').id)

# modem_ip_history_model = ModemIPHistoryModel(modem_id = 1, ip = '177.10.11.12', network_type = '4g', network_provider = 'Vivo', signalbar = 5)
# modem_ip_history_model.save_to_db()

# proxy_user_ip_history_model = ProxyUserIPHistoryModel()
# proxy_user_ip_history_model.proxy_user_id = 1
# proxy_user_ip_history_model.modem_ip_history_id = 1
# proxy_user_ip_history_model.save_to_db()

# is_ip_reserved_for_other = ProxyUserIPHistoryModel.is_ip_reserved_for_other('177.10.11.123', 2)
# print(is_ip_reserved_for_other)

# proxy_user_ip_filter_model = IpLabelFilterModel(proxy_user_id = 1, modem_id = 1, type = 'ip', value = '179.')
# proxy_user_ip_filter_model.save_to_db()
# proxy_user_ip_filter_model = IpLabelFilterModel(proxy_user_id = 1, modem_id = 2, type = 'ip', value = '200.173')
# proxy_user_ip_filter_model.save_to_db()

# print(IpLabelFilterModel.find_by_id(2).filter_value)

# filters = IpLabelFilterModel.find_by_proxy_user(1)
# filters = IpLabelFilterModel.find_by_proxy_user_and_modem(1, 2)
# if filters:
#     for filter in filters:
#         print(filter.value)

# def bytesToSize(bytes):
#     sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
#     if bytes == 0:
#         return 'n/a'
#     print(floor(log(abs(bytes)) / log(1024)), 10)
#     i = int(floor(log(abs(bytes)) / log(1024)), 10)
#     if i == 0:
#         return '{0} {1}'.format(bytes, sizes[i])
    
#     # return `${(bytes / 1024 ** i).toFixed(1)} ${sizes[i]}`;
#     return sizes[i]

# # bytesToSize(123421)
# print(HumanBytes.format(12342125, True, 0))

clients = []
connections = psutil.net_connections()
for connection in connections:
    if connection.laddr.port != 1026: continue
    if connection.status != 'ESTABLISHED': continue

    client_already_exist = False
    for client in clients:
        if client.raddr.ip == connection.raddr.ip: client_already_exist = True

    if client_already_exist == False:
        clients.append(connection)

print(clients)

sys.exit(0)

modem_log_model = ModemLogModel(
    modem_id=1, 
    owner=ModemLogOwner.SYSTEM, 
    type=ModemLogType.INFO, 
    message='log msg test', 
    code='102532', 
    params=[{'param1': 'param_value'}, {'param2': 'param2_value'}], 
    logged_at=datetime.now()
)
modem_log_model.save_to_db()
print(modem_log_model.to_json())
sys.exit()

# t = ProxyUserIPHistoryModel.is_ip_reserved_for_other(ip="187.119.228.144", user="carlos_antonio_santos")
# print(t)

# test = ['test1', 'test2']
# test = 'test'
# test = '10.1.1.1, 10.2.2.2 '
# test = test.split(',')
# print('|' + test[1].strip() + '|')
# # print(test.split(','))

# t = type(test) in (tuple, list)
# print(t)

user_model = UserModel()
user_model.username = 'berners'
user_model.password = '123'
user_model.save_to_db()

# print(Installation.find_by_id(2).name)

sys.exit(0)

server = ServerModel.find_by_id(1)
print(server.json())

# modem = ServerModemModel.find_by_id(2)
# print(modem.proxy_port)

# modems = server.modems
# for m in modems:
#     print(str(m.proxy_port) + ' > ' + m.modem.addr_id + ' > ' + str(m.usb_port.port))

# modem = ModemModel.find_by_id(2)
# print(modem.addr_id)

# usbport = USBPortModel.find_by_id(4)
# print(usbport.get_status())
# usbport.set_status(USBPortStatus.OFF)

usb_ports = server.usb_ports
for usb_port in usb_ports:
    print(usb_port.get_status())

sys.exit(0)
# installation = Installation.get_by_name('barueri-test')
# print(installation.id)

# server = Server.get_by_id(1)
# print('server > ' + server.external_ip)


# route = Route(gateway='10.56.74.1', interface='eth3', ip='10.56.74.157', table=5)
# route.resolve_route()

# os.system("sudo sed 's/proxy -p1028.*/proxy -p1028 -a -n -i0.0.0.0 -e10.56.74.1570000/' /usr/local/3proxy/conf/3proxy.cfg")

table = 1
while True:
    print('testing ' + str(table))
    proc = subprocess.Popen(['sudo', 'ip', 'route', 'add', 'default', 'via', '10.56.71.1', 'dev', 'eth2', 'src', '10.56.71.5', 'table', str(table)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    if proc.returncode != 0: #or not empty e.decode('ascii')
        print('error! ' + e.decode('ascii'))
        table = table + 1
        continue        

    print('executing second exp')
    break

sys.exit(0)

modems = server.get_modems()
for modem in modems:
    sys.stdout.write('{0}[*] Let''s check modem {1} on USB port {2} with addr_id {3}{4}\n'.format(CYELLOW, modem.id, modem.usb_port, modem.get_modem().addr_id, CEND))
    sys.stdout.flush()

    inframodem = InfraModem(modem).iface()
    if inframodem == None:
        sys.stdout.write('{0}[*] No, not present{1}\n\n'.format(CRED, CEND))
        sys.stdout.flush()
        continue

    ifaddress = inframodem.ifaddresses[0]
    ipv4 = ifaddress['addr']

    sys.stdout.write('{0}[*] Yes, present with interface {1} and internal IPv4 {2}{3}\n\n'.format(CGREEN, inframodem.interface, ipv4, CEND))
    sys.stdout.flush()

    # print(modem.proxy_port)


# modem = Modem.get_by_id(1)
# print('modem > ' + modem.addr_id)

# modemserver = ModemServer.get_by_server_and_modem(server, modem)
# print(modemserver.proxy_port)

# interfaces = NetIface.get_all()
# for interface in interfaces:
#     print(interface.interface)
#     print(interface.ifaddresses[0]['addr'])