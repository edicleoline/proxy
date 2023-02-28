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
        #check routes > ip route list

        sys.stdout.write('{0}[+] Setting up the route...{1}\n'.format(CBLUE, CEND)) 
        sys.stdout.flush()
        
        table = self.table
        while True:
            expr = 'ip route add default via {0} dev {1} src {2} table {3}'.format(self.gateway, self.interface, self.ip, str(table))

            sys.stdout.write('{0}[+] Executing "{1}"...{2}\n'.format(CBLUE, expr, CEND))
            sys.stdout.flush()

            proc = subprocess.Popen(['sudo', 'ip', 'route', 'add', 'default', 'via', self.gateway, 'dev', self.interface, 'src', self.ip, 'table', str(table)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            o, e = proc.communicate()

            if proc.returncode != 0:
                sys.stdout.write('{0}[!] Error: {1}{2}\n'.format(CRED, e.decode('ascii'), CEND))
                sys.stdout.flush()
                table = table + 1
                continue        

            proc = subprocess.Popen(['sudo', 'ip', 'rule', 'add', 'from', self.ip, 'table', str(table)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            o, e = proc.communicate()
            break

