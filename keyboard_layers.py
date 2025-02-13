import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
import keyboard

imageFolder = './assets/'

class MyApp(App):
  def build(self):
    self.title = 'Miryoku Layouts'
    self.img = AsyncImage(source= imageFolder + 'miryoku-kle-base.png',  allow_stretch=True)
    return self.img

  def on_function_key(self, layer):
      print('Layer:', layer)
      self.img.source = imageFolder + 'miryoku-kle-' + layer + '.png'
  
app = MyApp()
keyboard.add_hotkey(183, lambda: app.on_function_key('base'))
keyboard.add_hotkey(184, lambda: app.on_function_key('nav'))
keyboard.add_hotkey(185, lambda: app.on_function_key('mouse'))
keyboard.add_hotkey(186, lambda: app.on_function_key('media'))
keyboard.add_hotkey(187, lambda: app.on_function_key('num'))
keyboard.add_hotkey(188, lambda: app.on_function_key('sym'))
keyboard.add_hotkey(189, lambda: app.on_function_key('fun'))

app.run()
