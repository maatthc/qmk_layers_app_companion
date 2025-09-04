import keyboard


def key_listener(send_keystroke):
    keyboard.add_hotkey(183, lambda: send_keystroke("base"))
    keyboard.add_hotkey(184, lambda: send_keystroke("nav"))
    keyboard.add_hotkey(185, lambda: send_keystroke("mouse"))
    keyboard.add_hotkey(186, lambda: send_keystroke("media"))
    keyboard.add_hotkey(187, lambda: send_keystroke("num"))
    keyboard.add_hotkey(188, lambda: send_keystroke("sym"))
    keyboard.add_hotkey(189, lambda: send_keystroke("fun"))
