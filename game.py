import time

class Pos:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.dx = 0
    self.dy = 0
  
  def __repr__(self):
    xy = f"{self.x},{self.y}"
    if self.dx or self.dy:
      return f"{xy} + {self.dx},{self.dy}"
    return xy

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
    self.updateShip()

  def updateShip(self):
    if self.controls.left():
      self.ship.x -= 1
    if self.controls.right():
      self.ship.x += 1
    if self.controls.up():
      self.ship.y -= 1
    if self.controls.down():
      self.ship.y += 1

    # Clamping necessary if display dims changed to exclude ship
    self.ship.x = sorted((0, self.ship.x, self.display.cols - 1))[1]
    self.ship.y = sorted((0, self.ship.y, self.display.rows - 1))[1]
