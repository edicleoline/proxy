from framework.infra.netiface import NetIface

class Modem:
    def __init__(self, modemserver):
        self.modemserver = modemserver
        self.modem = self.modemserver.get_modem()

    def iface(self):
        addr_id = self.modem.addr_id
        return NetIface.get_iface_by_addr_id(addr_id)    

    def install(self):
        pass

    def hard_reboot(self):
        """Reboot USB port by cut power.       
        """
        pass

    def rotate(self):
        pass

    def details(self):
        """Connection and SIM details like network provider, network type and signalbar.
        """
        pass

    def external_ip(self):
        pass
    
    def ussd(self):
        """Send USSD to SIM card.
        """
        pass

    def uninstall(self):
        pass