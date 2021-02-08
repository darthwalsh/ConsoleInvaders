from console import Console
from keyboard import Keyboard
import time

stop = False
def on_quit():
  global stop
  stop = True

def main():
  with Console() as console:
    with Keyboard(on_quit) as keyboard:
      for i in range(29, -1, -1):
        if keyboard.left() or stop: break
        console.draw(i % 10)
        time.sleep(0.1)

if __name__ == "__main__":
  main()
