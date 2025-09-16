import argparse


def parser():
    parser = argparse.ArgumentParser(description="Keyboard companion app")
    parser.add_argument(
        "-s",
        "--server",
        action="store_true",
        help="Send keystrokes to remote host that will display Keyboard layout",
    )
    parser.add_argument(
        "-i",
        "--server_ip",
        help="IP address of the server - if not provided, local network discovery will be used.",
    )
    parser.add_argument(
        "-p",
        "--server_port",
        type=int,
        default=1977,
        help="Port to be used by the server - Default : 1977",
    )
    parser.add_argument(
        "-c",
        "--client",
        action="store_true",
        help="Receives keystrokes from remote server to display Keyboard layout",
    )
    args = parser.parse_args()

    if args.server_ip and not args.client:
        parser.error("--server_ip requires --client")

    if args.client and args.server:
        parser.error("Use --client or --server, not both")

    return args
