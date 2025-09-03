import os
os.environ["KIVY_NO_ARGS"] = "1"

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage

imageFolder = './assets/'

class Gui(App):
  def build(self):
    self.title = 'Keyboard : Miryoku Layouts'
    self.img = AsyncImage(source= imageFolder + 'miryoku-kle-base.png',  allow_stretch=True)
    return self.img

  def on_function_key(self, layer):
      self.img.source = imageFolder + 'miryoku-kle-' + layer + '.png'
  
