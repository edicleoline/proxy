from typing import List
from framework.models.server import ServerModel, ServerModemModel

class Proxy():
    service_config_path: str = '/usr/local/3proxy/conf/3proxy.cfg'
    nscache: int = 65536
    nservers: List[str] = ['8.8.8.8', '8.8.4.4']
    config_path: str = '/conf/3proxy.cfg'
    monitor_path: str = '/conf/3proxy.cfg'
    log_path: str = '/logs/3proxy-%y%m%d.log D'
    rotate: int = 60
    counter_path: str = '/count/3proxy.3cf'
    users_path: str = '$/conf/passwd'
    includes: List[str] = ['/conf/counters', '/conf/bandlimiters']

    def __init__(self):
        pass

    def resolve_header(self):
        pass

    def resolve_proxies(self, modems: List[ServerModemModel]):
        pass