import requests
import sys
import time
import socket
from datetime import datetime, timedelta

from framework.error.exception import TimeoutException

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

        return None


    def try_get_current_ip(self, event_stop = None, timeout = 60 * 2):
        timeout_at = datetime.now() + timedelta(seconds=timeout)

        while True:
            ip = self.get_current_ip()
            if ip != None: return ip
            
            if event_stop and event_stop.is_set(): break

            diff_timeout_now = int((datetime.now() - timeout_at).total_seconds())
            print('timeout_diff {0}'.format(diff_timeout_now))
            if diff_timeout_now >= timeout:
                raise TimeoutException('Timeout exception')

            time.sleep(1)

        return None