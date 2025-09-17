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
        consumer = Gui(Client(args))
    elif args.server:
        consumer = Server(Keyboard(), args)
    else:
        consumer = Gui(Keyboard())

    try:
        await consumer.start()
    except KeyboardInterrupt:
        consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
