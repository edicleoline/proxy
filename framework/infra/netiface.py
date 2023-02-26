import netifaces

class NetIface:
    def __init__(self, interface, ifaddresses):
        self.interface = interface
        self.ifaddresses = ifaddresses

    @staticmethod
    def get_all():
        interfaces = []
        for interface in netifaces.interfaces():
            try:
                interfaces.append(
                    NetIface(
                        interface = interface,
                        ifaddresses = netifaces.ifaddresses(interface)[netifaces.AF_INET]
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