import requests
import sys
import time
import socket

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

class HTTPAdapterWithSocketOptions(requests.adapters.HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.socket_options = kwargs.pop("socket_options", None)
        super(HTTPAdapterWithSocketOptions, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.socket_options is not None:
            kwargs["socket_options"] = self.socket_options
        super(HTTPAdapterWithSocketOptions, self).init_poolmanager(*args, **kwargs)

class Wan:
    def __init__(self, interface):
        self.interface = interface

    def get_current_ip(self, silence_mode = False):
        try:
            if silence_mode == False:
                sys.stdout.write('{0}[*] Getting IPv4... {1}'.format(CMAGENTA, CEND))
                sys.stdout.flush()
            adapter = HTTPAdapterWithSocketOptions(socket_options=[(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, self.interface.encode('utf-8'))])
            session = requests.session()
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            resp = session.get('https://ipecho.net/plain', timeout=5).text
            if silence_mode == False:
                sys.stdout.write('{0}{1}{2}\n'.format(CGREEN, resp, CEND))
                sys.stdout.flush()
            return resp
        except:
            if silence_mode == False:
                sys.stdout.write('{0}FAIL{1}\n'.format(CRED, CEND))
                sys.stdout.flush()


    def try_get_current_ip(self, retries = 3, silence_mode = False):
        ip = None
        retry_ip = 0
        while True:
            retry_ip = retry_ip + 1
            ip = self.get_current_ip(silence_mode=silence_mode)    
            
            if ip != None or retry_ip >= retries:
                break

            time.sleep(1)

        return ip