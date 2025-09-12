import os
from config import Config

os.environ["KIVY_NO_ARGS"] = "1"

from kivy.app import App  # noqa: F401
from kivy.uix.image import AsyncImage  # noqa: F401

imageFolder = "./assets/"


class Gui(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.thread_event = None
        self.conf = Config()

    def set_thread_event(self, thr):
        self.thread_event = thr

    def build(self):
        self.title = "Keyboard : Miryoku Layouts"
        self.img = AsyncImage(
            source=imageFolder + self.conf.layers[0], allow_stretch=True
        )
        return self.img

    def on_function_key(self, layer):
        print(f"Switched to layer {layer}: {self.conf.layers[layer]}")
        self.img.source = imageFolder + self.conf.layers[layer]

    def on_stop(self, **kwargs):
        print("App closing..")
        if self.thread_event is not None:
            self.thread_event.set()
        super().on_stop(**kwargs)
