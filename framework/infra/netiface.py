import netifaces
import psutil
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class NetIface:
    interface: str = None

    def __init__(self, interface, ifaddresses, rx_bytes = None, tx_bytes = None):
        self.interface = interface
        self.ifaddresses = ifaddresses
        self.rx_bytes = rx_bytes
        self.tx_bytes = tx_bytes

    @staticmethod
    def get_all():
        interfaces = []
        netifaces_interfaces = [iface for iface in netifaces.interfaces() if iface != 'lo']
        data = psutil.net_io_counters(pernic=True)        
        
        for interface in netifaces_interfaces:
            try:
                io_counter = data[interface] if type(data) == dict else None
                tx_bytes, rx_bytes = None, None
                if io_counter:
                    tx_bytes, rx_bytes = io_counter[0], io_counter[1]
                    # print("{0} RX: {1}, TX: {2}".format(interface, rx, tx))

                interfaces.append(
                    NetIface(
                        interface = interface,
                        ifaddresses = netifaces.ifaddresses(interface)[netifaces.AF_INET],
                        rx_bytes = rx_bytes,
                        tx_bytes = tx_bytes
                    )        
                )
            except:
                pass

        return interfaces

    @staticmethod
    def get_iface_by_addr_id(addr_id):
        ifaces = NetIface.get_all()
        for iface in ifaces:
            for ifaddress in iface.ifaddresses:
                if ifaddress['addr'].startswith(addr_id):
                    return iface

        return None

    @staticmethod
    def get_gateway_from_ipv4(ipv4):
        return ipv4.rsplit('.', 1)[0] + '.1'
    
    @staticmethod
    def possible_modem_interfaces():
        all = NetIface.get_all()

    @staticmethod
    def possible_available_modem_interfaces():
        pass