import sys
import os
os.environ["KIVY_NO_ARGS"] = "1"

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage

imageFolder = './assets/'

class Gui(App):
  def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.thread_event=None

  def set_thread_event(self,thr):
        self.thread_event=thr

  def build(self):
    self.title = 'Keyboard : Miryoku Layouts'
    self.img = AsyncImage(source= imageFolder + 'miryoku-kle-base.png',  allow_stretch=True)
    return self.img

  def on_function_key(self, layer):
      self.img.source = imageFolder + 'miryoku-kle-' + layer + '.png'

  def on_stop(self):
        print('App closing..')
        if self.thread_event is not None:
            self.thread_event.set()
            sys.exit()
