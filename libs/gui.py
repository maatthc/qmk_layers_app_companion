import os
from libs.config import Config

os.environ["KIVY_NO_ARGS"] = "1"

from kivy.app import App  # noqa: F401
from kivy.uix.image import Image  # noqa: F401
from kivy.clock import Clock  # noqa: F401

imageFolder = "./assets/"


class Gui(App):
    def __init__(self, listener, **kwargs):
        super().__init__(**kwargs)
        self.conf = Config()
        self.listener = listener

    def on_start(self):
        Clock.schedule_interval(self.updateLayer, 0.5)

    def build(self):
        self.title = "Keyboard Layers App companion"
        self.img = Image(source=imageFolder + self.conf.layers[0], allow_stretch=True)
        return self.img

    def updateLayer(self, dt):  # dt is the time since the last call, can be ignored
        layer = self.listener.notify_changes()
        if layer is None:
            return
        print(f"Switched to layer {layer}: {self.conf.layers[layer]}")
        self.img.source = imageFolder + self.conf.layers[layer]

    def on_stop(self, **kwargs):
        print("App closing..(did you press ESC?)")
        super().on_stop(**kwargs)

    async def start(self):
        super().run()
