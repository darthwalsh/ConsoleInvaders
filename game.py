import time

class Pos:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.dx = 0
    self.dy = 0

class Game:
  def __init__(self, display, controls):
    self.display = display
    self.controls = controls
    self.over = False

    self.ship = Pos()

  def on_quit(self):
    self.over = True

  def run(self):
    while not self.controls.stop:
      self.update()
      self.display.draw(self)
      time.sleep(0.1)

  def update(self):
    # TODO handle the outer bounds first checking curses.is_term_resized

    if self.ship.x > 0 and self.controls.left():
      self.ship.x -= 1
    if self.controls.right():
      self.ship.x += 1
    if self.ship.y > 0 and self.controls.up():
      self.ship.y -= 1
    if self.controls.down():
      self.ship.y += 1
