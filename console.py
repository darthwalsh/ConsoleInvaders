import curses

class Console:
  def draw(self, world):
    self.screen.clear()

    self.screen.addch(world, 1, '^')

    self.screen.refresh()

  def __enter__(self):
    self.screen = curses.initscr() 
    
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    self.screen.keypad(True)
    #curses.start_color()
    #curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    return self

  def __exit__(self, type, value, traceback):
    self.screen.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
