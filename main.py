import asyncio
import sys
from libs.gui import Gui
from libs.server import Server
from libs.client import Client
from libs.webserver import WebServer
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
    else:
        keyboard = Keyboard()
        if args.server:
            consumer = Server(keyboard, args)
        elif args.web:
            consumer = WebServer(keyboard, args)
        else:
            consumer = Gui(keyboard)

    try:
        await consumer.start()
    except KeyboardInterrupt:
        if hasattr(consumer, "cleanup"):
            await consumer.cleanup()
        else:
            consumer.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user (Ctrl+C)")
    except SystemExit as e:
        sys.exit(e.code)
