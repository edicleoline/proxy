import pcf8574_io
import time
import sys

from framework.models.server import Server

class USB:
    def __init__(self, port: int, server: Server):
        self.p1 = pcf8574_io.PCF(0x22)
        self.port = port - 1
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

    def hard_reboot(self):
        # for i in range(0, 8):
        #     self.write("p" + str(i), "HIGH")

        self.write("p" + str(self.port), "LOW")
        time.sleep(1)
        self.write("p" + str(self.port), "HIGH")

    def hard_turn_off(self):
        # for i in range(0, 8):
        #     self.write("p" + str(i), "HIGH")

        self.write("p" + str(self.port), "LOW")


# USB().hard_reboot(1)