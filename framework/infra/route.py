import sys
import subprocess

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

class Route:
    def __init__(self, gateway, interface, ip, table):
        self.gateway = gateway
        self.interface = interface
        self.ip = ip
        self.table = str(table)

    def resolve_route(self):
        sys.stdout.write('{0}[+] Use "sudo ip route add default via {1} dev {2} src {3} table {4}"{5}\n'.format(CBLUE, self.gateway, self.interface, self.ip, self.table, CEND))
        sys.stdout.write('{0}[+] Use "sudo ip rule add from {1} table {2}"{3}\n'.format(CBLUE, self.ip, self.table, CEND)) 
        sys.stdout.flush()

        #check routes > ip route list

        #TODO
        #loop table until no error 
        
        proc = subprocess.Popen(['sudo', 'ip', 'route', 'add', 'default', 'via', self.gateway, 'dev', self.interface, 'src', self.ip, 'table', str(self.table)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()
        print('Output: ' + o.decode('ascii'))
        print('Error: '  + e.decode('ascii'))
        print('code: ' + str(proc.returncode))

        proc = subprocess.Popen(['sudo', 'ip', 'rule', 'add', 'from', self.ip, 'table', str(self.table)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()
        print('Output: ' + o.decode('ascii'))
        print('Error: '  + e.decode('ascii'))
        print('code: ' + str(proc.returncode))

