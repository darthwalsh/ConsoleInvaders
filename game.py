import time

class Pos:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.dx = 0
    self.dy = 0

  def update(self):
    self.x += self.dx
    self.y += self.dy
  
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
    self.ship.x = display.cols // 2
    self.ship.y = 3 * display.rows // 4
    self.bullets: list[Pos] = []

  def on_quit(self):
    self.over = True

  def run(self):
    while not self.controls.stop:
      self.update()
      self.display.draw(self)
      try:
        time.sleep(0.1)
      except KeyboardInterrupt:
        break

  def update(self):
    self.updateShip()
    self.updateBullets()

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

  def updateBullets(self):
    if self.controls.fire():
      shot = Pos()
      shot.x = self.ship.x
      shot.y = self.ship.y
      shot.dy = -1
      self.bullets.append(shot)

    for b in self.bullets:
      b.update()

    self.bullets[:] = [b for b in self.bullets if b.y >= 0]
