import curses

class Console:
  debug = False

  def draw(self, world):
    self.screen.clear()

    self.draw_pos(world.ship, 'W')

    if self.debug:
      self.screen.addstr(0, 0, f'h{self.cols}')
      self.screen.addstr(0, 3, f'w{self.rows}')

    self.screen.refresh()
    if curses.is_term_resized(self.rows, self.cols):
      self.rows, self.cols = self.screen.getmaxyx()
      curses.resizeterm(self.rows, self.cols)

  def draw_pos(self, p, c):
    self.screen.addch(p.y, p.x, c)

  def __enter__(self):
    self.screen = curses.initscr()

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    self.screen.keypad(True)

    self.rows, self.cols = self.screen.getmaxyx()
    #curses.start_color()
    #curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    return self

  def __exit__(self, type, value, traceback):
    self.screen.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
