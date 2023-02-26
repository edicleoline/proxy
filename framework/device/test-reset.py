import fcntl, sys, os
from zte.mf79s import MF79S


USBDEVFS_RESET = 21780

with open(sys.argv[1], "wb") as fd:
  fcntl.ioctl(fd, USBDEVFS_RESET, 0)


# os.system('sudo ifconfig enx00a0c6000000 192.168.1.157/24')

# zte = MF79S(interface = 'enx00a0c6000000', host = '192.168.1.1', password = 'vivo', retries = 5, retries_ip = 10)
# zte.reboot()