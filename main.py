from gui import Gui
from server import Server
from client import Client
from args import parser
from keyboard_hid import Keyboard


def main():
    args = parser()

    if args.client:
        gui = Gui()
        Client(gui, args)
        gui.run()
        return

    listener = None

    if args.remote:
        listener = Server()
    else:
        listener = Gui()

    Keyboard(listener)


if __name__ == "__main__":
    main()
