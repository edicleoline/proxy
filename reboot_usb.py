import sys
from framework.infra.usb import USB

USB().hard_reboot(int(sys.argv[1]))