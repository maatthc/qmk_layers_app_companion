from libs.gui import Gui
from libs.sender import Sender
from libs.client import Client
from libs.args import parser
from libs.keyboard_hid import Keyboard


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
