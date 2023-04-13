import requests
import sys
import time
import socket
from datetime import datetime, timedelta
from framework.error.exception import TimeoutException

class HTTPAdapterWithSocketOptions(requests.adapters.HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.socket_options = kwargs.pop("socket_options", None)
        super(HTTPAdapterWithSocketOptions, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        if self.socket_options is not None:
            kwargs["socket_options"] = self.socket_options
        super(HTTPAdapterWithSocketOptions, self).init_poolmanager(*args, **kwargs)

class Wan:
    def __init__(self, settings, interface):
        self.settings = settings
        self.interface = interface

    def get_current_ip(self):
        print(self.settings)
        try:
            adapter = HTTPAdapterWithSocketOptions(socket_options=[(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, self.interface.encode('utf-8'))])
            session = requests.session()
            session.mount("http://", adapter)
            session.mount("https://", adapter)
            resp = session.get(self.settings.external_ip_url, timeout=5).text
            return resp
        except Exception:
            pass

    def try_get_current_ip(self, event_stop = None, timeout = 60 * 2):
        timeout_at = datetime.now() + timedelta(seconds=timeout)

        while True:
            ip = self.get_current_ip()
            if ip != None: return ip
            
            if event_stop and event_stop.is_set(): break

            diff_timeout_now = int((datetime.now() - timeout_at).total_seconds())
            if diff_timeout_now >= timeout:
                raise TimeoutException('Timeout exception')

            time.sleep(1)

        return None