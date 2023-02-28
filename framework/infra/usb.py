import pcf8574_io
import time
import sys

class USB:
    def __init__(self):
        self.p1 = pcf8574_io.PCF(0x22)

    def write(self, id, mode):
        self.p1.pin_mode(id, "OUTPUT")
        self.p1.write(id, mode)
        #p1.write(id, "LOW")


    def read(self, id, mode):
        self.p1.pin_mode(id, mode)
        t = self.p1.read(id)
        print(t)
        return t


    def hard_reboot(self, port):
        for i in range(0, 8):
            self.write("p" + str(i), "HIGH")

        real_port = str(port - 1)
        self.write("p" + real_port, "LOW")
        time.sleep(1)
        self.write("p" + real_port, "HIGH")

    def hard_turn_off(self, port):
        for i in range(0, 8):
            self.write("p" + str(i), "HIGH")

        real_port = str(port - 1)
        self.write("p" + real_port, "LOW")


# USB().hard_reboot(1)