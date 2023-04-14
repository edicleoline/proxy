import ipaddress

class Ipv4Validation():
    @staticmethod
    def is_valid(ipv4: str):
        try:
            ipaddress.ip_address(ipv4)
            return True
        except ValueError:
            return False