import curses

class Console:
  def draw(self, world):
    self.screen.clear()

    self.draw_pos(world.ship, 'W')

    self.screen.refresh()

  def draw_pos(self, p, c):
    self.screen.addch(p.y, p.x, c)

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
