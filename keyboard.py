import threading
from pynput import keyboard

class Keyboard():
  def __init__(self, on_quit):
    self.on_quit = on_quit
    self.lock = threading.Lock()
    self.pressed = set()

  def on_press(self, key):
    with self.lock:
      self.pressed.add(key)

  def on_release(self, key):
    with self.lock:
      self.pressed.remove(key)

    if key == keyboard.Key.esc:
      self.on_quit()

  def left(self):
    with self.lock:
      return keyboard.Key.left in self.pressed

  def right(self):
    with self.lock:
      return keyboard.Key.right in self.pressed

  def up(self):
    with self.lock:
      return keyboard.Key.up in self.pressed

  def down(self):
    with self.lock:
      return keyboard.Key.down in self.pressed

  def fire(self):
    with self.lock:
      return keyboard.Key.shift in self.pressed

  def __enter__(self):
    self.listener = keyboard.Listener(
        on_press=self.on_press,
        on_release=self.on_release)
    self.listener.start()

    return self

  def __exit__(self, type, value, traceback):
    self.listener.stop()

