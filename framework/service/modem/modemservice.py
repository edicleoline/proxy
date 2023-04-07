from framework.manager.modem import ModemThreadData
from framework.models.server import ServerModemModel
from framework.infra.modem import Modem as IModem
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class ModemConnectivityData():
    bytes: int
    formatted: str

    def __init__(self, bytes: int, formatted: str):
        self.bytes = bytes
        self.formatted = formatted

@dataclass_json
@dataclass
class ModemConnectivityTraffic():
    receive: ModemConnectivityData
    transmit: ModemConnectivityData

    def __init__(self, receive: ModemConnectivityData, transmit: ModemConnectivityData):
        self.receive = receive
        self.transmit = transmit

@dataclass_json
@dataclass
class ModemConnectivity():
    interface: str
    internal_ip: str
    network_type: str
    network_provider: str 
    network_signalbar: str
    external_ip: str
    data_traffic: ModemConnectivityTraffic

    def __init__(
            self,
            interface: str,
            internal_ip: str,
            network_type: str,
            network_provider: str, 
            network_signalbar: str,
            external_ip: str,
            data_traffic: ModemConnectivityTraffic
    ):
        self.interface = interface
        self.internal_ip = internal_ip
        self.network_type = network_type
        self.network_provider = network_provider
        self.network_signalbar = network_signalbar
        self.external_ip = external_ip
        self.data_traffic = data_traffic

@dataclass_json
@dataclass
class ModemState():
    modem: ServerModemModel
    lock: ModemThreadData
    is_connected: bool    
    connectivity: ModemConnectivity

    def __init__(
            self, 
            modem: ServerModemModel, 
            infra_modem: IModem = None, 
            lock: ModemThreadData = None,
            is_connected: bool = None,
            connectivity: ModemConnectivity = None
    ):
        self.modem = modem
        self.infra_modem = infra_modem
        self.lock = lock
        self.is_connected = is_connected
        self.connectivity = connectivity