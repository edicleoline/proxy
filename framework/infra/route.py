import sys
import subprocess
import time

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
        self.table = table

    def ip_route_table(self):
        #ip route show table all
        #default via 10.56.72.157 dev eth1 table 31 src 10.56.72.157
        proc = subprocess.Popen(['ip', 'route', 'show', 'table', 'all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()
        lines = o.decode().splitlines()

        for line in lines:
            if 'default via {0} dev {1} table'.format(self.ip, self.interface) in line:
                return line.split('table', 1)[1].split('src')[0].strip()
            
            if 'default via {0} dev {1} table'.format(self.gateway, self.interface) in line:
                return line.split('table', 1)[1].split('src')[0].strip()
        
        return None


    def resolve_route(self):
        table = int(self.table)
        while True:
            routed_table = self.ip_route_table()
            
            if routed_table == None:
                print('table not found. lets try resolve route {0}'.format(self.ip))

                proc = subprocess.Popen(['sudo', 'ip', 'route', 'add', 'default', 'via', self.gateway, 'dev', self.interface, 'src', self.ip, 'table', str(table)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                o, e = proc.communicate()

                if proc.returncode != 0:
                    sys.stdout.write('{0}[!] Error: {1}{2}\n'.format(CRED, e.decode('ascii').rstrip(), CEND))
                    sys.stdout.flush()

                proc = subprocess.Popen(['sudo', 'ip', 'rule', 'add', 'from', self.ip, 'table', str(table)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                o, e = proc.communicate()

                time.sleep(1)

                routed_table = self.ip_route_table()
                if routed_table != None:
                    break

            table = table + 1            
            break

