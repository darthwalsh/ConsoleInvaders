import curses

class Console:
  debug = False

  def draw(self, world):
    self.screen.clear()

    self.draw_pos(world.ship, 'W')

    for b in world.all_bunkers:
      self.draw_pos(b, str(b.bunk.health))

    for b in world.bombs:
      self.draw_pos(b, 'o')

    for e in world.enemies:
      self.draw_pos(e, '!')

    for b in world.bullets:
      self.draw_pos(b, '^')

    if self.debug:
      self.screen.addstr(0, 0, f'h{self.cols}')
      self.screen.addstr(0, 3, f'w{self.rows}')

    self.screen.refresh()
    if curses.is_term_resized(self.rows, self.cols):
      self.rows, self.cols = self.screen.getmaxyx()
      curses.resizeterm(self.rows, self.cols)

  def draw_pos(self, p, c):
    try:
      self.screen.addch(p.y, p.x, c)
    except curses.error as e:
      if 0 <= p.y < self.rows and 0 <= p.x < self.cols:
        return
      raise ValueError(f"{p} was out of bounds {self.cols},{self.rows}", e)

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
