from libs.gui import Gui
from libs.sender import Sender
from libs.client import Client
from libs.args import parser
from libs.keyboard_hid import Keyboard

gui = None
sender = None


def send_keystroke(key):
    if sender is not None:
        sender.notify(key)
    if gui is not None:
        gui.on_function_key(key)


def main():
    global gui, sender
    args = parser()

    if args.client:
        gui = Gui()
        Client(gui, args.client_port)
        gui.run()
        return

    keyboard = Keyboard(send_keystroke)

    if args.remote:
        sender = Sender(args)
        sender.connect()
    else:
        gui = Gui()
        keyboard.set_gui(gui)
        gui.run()


if __name__ == "__main__":
    main()
