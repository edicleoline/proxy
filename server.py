import sys
import os
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='')
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument('--modem', dest='modem_id', help='Modem ID')
    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument('--status', dest='status', help='Show server status', action='store_true')
    # group2.add_argument('--rotate', dest='rotate', help='Rotate IPv4', action='store_true')
    # group2.add_argument('--usb-reboot', dest='usb_reboot', help='Reboot USB', action='store_true')
    # group2.add_argument('--info', dest='info', help='Show details about modem, connection and proxy', action='store_true')

    # parser.add_argument('--hard-reset', dest='hard_reset', help='Use USB hard reset', action='store_true')
    # parser.add_argument('--user', dest='user', help='User email')
    # parser.add_argument('--match', dest='ip_match', help='IPv4 match')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

def main():
    global _args, server
    
    _args = get_args()



if __name__ == '__main__':
	main()