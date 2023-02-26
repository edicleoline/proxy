import sys
import os

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

class ProxyService:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def resolve_proxy(self):        
        sys.stdout.write('{0}[+] Use "sudo nano /etc/3proxy/conf/p{1}.cfg{2}\n'.format(CBLUE, self.port, CEND))
        sys.stdout.write('{0}[+] Use "proxy -p{1} -a -n -i0.0.0.0 -e{2}"{3}\n'.format(CBLUE, self.port, self.ip, CEND))
        sys.stdout.flush()

        cfg = '/usr/local/3proxy/conf/3proxy.cfg'
        print("sudo sed 's/proxy -p{0}.*/proxy -p{0} -a -n -i0.0.0.0 -e{1}/' {2} > {2}".format(self.port, self.ip, cfg))
        # os.system("sudo sed 's/proxy -p{0}.*/proxy -p{0} -a -n -i0.0.0.0 -e{1}/' {2} > {2}".format(self.port, self.ip, cfg))

    
    