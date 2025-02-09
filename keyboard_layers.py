import keyboard
import tkinter as tk
from PIL import Image, ImageTk

def on_function_key(layer):
    print('Layer:', layer)
    app.updateImage(layer)

imageFolder = '/home/maat/Pictures/'

class Resizable:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x400")
        self.master.title("Miryoku Layouts")
        self.growCanvas = tk.Canvas(self.master)
        self.growCanvas.pack(fill = tk.BOTH, expand = tk.YES)
        picture = imageFolder + 'miryoku-kle-base.png'
        self.image = Image.open(picture)
        self.image_copy = self.image.copy()
        self.background = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(
            self.growCanvas, image = self.background, borderwidth = 0)
        self.label.bind('<Configure>', self.resizeImage)
        self.label.pack(fill = tk.BOTH, expand = tk.YES, padx = 2, pady = 2)
    def resizeImage(self, event):
        image = self.image_copy.resize(
            (self.master.winfo_width(), self.master.winfo_height()))
        self.newimage = ImageTk.PhotoImage(image)
        self.label.config(image = self.newimage)
    def updateImage(self, picture):
        self.image = Image.open(imageFolder + 'miryoku-kle-' + picture + '.png')
        self.image_copy = self.image.copy()
        self.resizeImage(None)

try:
    app = Resizable(tk.Tk())

    keyboard.add_hotkey(183, lambda: on_function_key('base'))
    keyboard.add_hotkey(184, lambda: on_function_key('nav'))
    keyboard.add_hotkey(185, lambda: on_function_key('mouse'))
    keyboard.add_hotkey(186, lambda: on_function_key('media'))
    keyboard.add_hotkey(187, lambda: on_function_key('num'))
    keyboard.add_hotkey(188, lambda: on_function_key('sym'))
    keyboard.add_hotkey(189, lambda: on_function_key('fun'))

    app.master.mainloop()
except Exception as error:
    print("An error occurred:", type(error).__name__)
