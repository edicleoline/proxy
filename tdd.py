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

from framework.models.server import ServerModel, ServerModemModel, USBPortModel, USBPortStatus
from framework.models.modem import ModemModel

from framework.models.useriphistory import UserIPHistory
from framework.models.installation import InstallationModel
from framework.models.user import UserModel

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

server = ServerModel.find_by_id(1)
print(server.json())

# usb_port = USBPortModel.find_by_id(2)
# print(usb_port.json())

# for port in server.usb_ports():
#     print(port.server_id)

# server_modem = ServerModemModel.find_by_id(5)
# # server_modem = ServerModemModel.find_by_modem_id(6)
# print(server_modem.server().name)

# installation = USBPortModel.find_by_id(1)
# print(installation.json())

for modem in server.modems():
    print(modem.modem().addr_id)


sys.exit()

# t = UserIPHistory.is_ip_reserved_for_other(ip="187.119.228.144", user="carlos_antonio_santos")
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