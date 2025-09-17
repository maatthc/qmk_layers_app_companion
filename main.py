import asyncio
from libs.gui import Gui
from libs.server import Server
from libs.client import Client
from libs.args import parser
from libs.keyboard_hid import Keyboard
from libs.consumer import ConsumerInterface


async def main():
    consumer: ConsumerInterface = None
    args = parser()

    if args.client:
        cli = Client(args)
        await cli.start()
        consumer = Gui(cli)
    elif args.server:
        consumer = Server(Keyboard(), args)
    else:
        consumer = Gui(Keyboard())

    try:
        await consumer.start()
    except KeyboardInterrupt:
        consumer.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by KeyboardInterrupt.")
