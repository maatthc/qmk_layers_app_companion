import keyboard
from gui import Gui
from sender import Sender
from client import Client
from args import parser
from hotkeys import key_listener

gui = None
sender = None

def send_keystroke(key):
    if sender is not None:
        sender.notify(key)
    else:
        gui.on_function_key(key)

def main():
    global gui,sender
    args = parser()

    if args.client:
        gui = Gui()
        Client(gui,args.client_port)
        gui.run()
        return

    key_listener(send_keystroke)

    if args.remote:
        sender = Sender(args)
        sender.connect()
        keyboard.wait()
    else:
        gui = Gui()
        gui.run()

if __name__ == '__main__':
    main()
