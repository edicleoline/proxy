import pcf8574_io
import time
import sys

from framework.models.server_ import Server, USBPort, USBPortStatus

IO_ON  = 'HIGH'
IO_OFF = 'LOW'

class USB:
    def __init__(self, server: Server):
        self.p1 = pcf8574_io.PCF(0x22)
        self.server = server

    def write(self, id, mode):
        self.p1.pin_mode(id, "OUTPUT")
        self.p1.write(id, mode)
        #p1.write(id, "LOW")

    def read(self, id, mode):
        self.p1.pin_mode(id, mode)
        t = self.p1.read(id)
        print(t)
        return t

    def preserve_others_ports_status(self):
        usb_ports = self.server.usb_ports
        for usb_port in usb_ports:
            if usb_port.get_status() == USBPortStatus.ON:
                self.hard_turn_on(usb_port)
            else:
                self.hard_turn_off(usb_port)

    def hard_reboot(self, usb_port: USBPort):
        self.preserve_others_ports_status()

        self.hard_turn_off(usb_port, update_status=False)
        time.sleep(1)
        self.hard_turn_on(usb_port)

    def hard_turn_off(self, usb_port: USBPort, update_status = True):
        self.write("p" + str(usb_port.get_real_port()), IO_OFF)
        if update_status == True:
            usb_port.set_status(USBPortStatus.OFF)

    def hard_turn_on(self, usb_port: USBPort, update_status = True):
        self.write("p" + str(usb_port.get_real_port()), IO_ON)
        if update_status == True:
            usb_port.set_status(USBPortStatus.ON)