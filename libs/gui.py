import os
import asyncio
from libs.config import Config

os.environ["KIVY_NO_ARGS"] = "1"

from kivy.app import App  # noqa: F401
from kivy.uix.image import Image  # noqa: F401

imageFolder = "./assets/"


class Gui(App):
    def __init__(self, listener, **kwargs):
        super().__init__(**kwargs)
        self.conf = Config()
        self.listener = listener

    def on_start(self):
        asyncio.create_task(self.updateLayer())

    def build(self):
        self.title = "Keyboard Layers App companion"
        self.img = Image(source=imageFolder + self.conf.layers[0], allow_stretch=True)
        return self.img

    async def updateLayer(self, dt=None):
        while True:
            try:
                layer = self.listener.notify_changes()
                if layer is not None:
                    self.img.source = imageFolder + self.conf.layers[layer]
                    print(f"Switched to layer {layer}: {self.conf.layers[layer]}")
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error: {e}")

    def on_stop(self, **kwargs):
        print("App closing..(did you press ESC?)")
        super().on_stop(**kwargs)

    async def start(self):
        await super().async_run()
