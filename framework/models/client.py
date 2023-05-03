from dataclasses import dataclass
from typing import List
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Addr():
    ip: str = None
    port: int = None

    def __init__(self, ip: str = None, port: int = None):
        self.ip = ip
        self.port = port


@dataclass_json
@dataclass
class Instance():
    raddr: Addr = None

    def __init__(self, raddr: Addr = None):
        self.raddr = raddr


@dataclass_json
@dataclass
class Client():
    laddr: Addr = None
    instances: List[Instance] = None

    def __init__(self, laddr: Addr = None):
        self.laddr = laddr
        self.instances = []

