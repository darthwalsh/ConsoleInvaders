from console import Console
from keyboard import Keyboard
from game import Game

def main():
  with Console() as console:
    with Keyboard() as keyboard:
      game = Game(console, keyboard)
      game.run()

if __name__ == "__main__":
  main()
