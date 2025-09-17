from libs.gui import Gui
from libs.server import Server
from libs.client import Client
from libs.args import parser
from libs.keyboard_hid import Keyboard
from libs.consumer import ConsumerInterface


def main():
    args = parser()

    if args.client:
        gui = Gui()
        Client(gui, args)
        gui.run()
        return

    consumer: ConsumerInterface = None
    if args.server:
        consumer = Server(Keyboard(), args)
    else:
        consumer = Gui(Keyboard())

    try:
        consumer.run()
    except KeyboardInterrupt:
        consumer.stop()


if __name__ == "__main__":
    main()
