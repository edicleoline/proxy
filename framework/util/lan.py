import os
import subprocess, platform
import sys

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CBLUE = '\033[94m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLAC = '\033[90m'
CEND = '\033[0m'

class Lan:
    def __init__(self):
        pass

    def check_ping(self, hostname, attempts = 1, silent = True):
        parameter = '-n' if platform.system().lower()=='windows' else '-c'
        filter = ' | findstr /i "TTL"' if platform.system().lower()=='windows' else ' | grep "ttl"'
        if (silent):
            silent = ' > NUL' if platform.system().lower()=='windows' else ' >/dev/null'
        else:
            silent = ''

        sys.stdout.write('{0}[!] Pinging... {1}'.format(CYELLOW, CEND))
        sys.stdout.flush()
        response = os.system('ping ' + parameter + ' ' + str(attempts) + ' ' + hostname + filter + silent)

        if response == 0:
            sys.stdout.write('{0}SUCCESS{1}\n'.format(CGREEN, CEND))
            sys.stdout.flush()
            return True
        else:
            sys.stdout.write('{0}FAIL{1}\n'.format(CRED, CEND))
            sys.stdout.flush()
            return False