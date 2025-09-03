import argparse

def parser():
    parser = argparse.ArgumentParser(description="Keyboard companion gui")
    parser.add_argument('-r', '--remote', action='store_true', help='Send keystrokes to remote host that will display Keyboard layout')
    parser.add_argument('-i', '--client_ip', action='store_true', help='IP address of the remote host - if not provided, local network discovery will be used.')
    parser.add_argument('-c', '--client', action='store_true', help='Receives keystrokes from remote host to display Keyboard layout')
    args = parser.parse_args()

    if args.client_ip and not args.remote:
        parser.error('--client_ip requires --remote')

    if args.client and  args.remote:
        parser.error('Use --client or --remote')

    return args
