import keyboard
from gui import Gui
from sender import Sender
from client import Client
from args import parser
from hotkeys import key_listener

gui = None
sender = None

args = parser()

def send_keystroke(key):
    if sender is not None:
        sender.notify(key)
    else:
        gui.on_function_key(key)

if args.client:
    gui = Gui()
    Client(gui)
    gui.run()

else:
    key_listener(send_keystroke)

    if args.remote:
        sender = Sender()
        sender.connect()
        keyboard.wait()
    else:
        gui = Gui()
        gui.run()
