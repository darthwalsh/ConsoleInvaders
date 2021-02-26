import time

INITIAL_HEALTH = 9
SHOT_COOLDOWN = 3

class Pos:
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y
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

    self.ship = Pos(display.cols // 2, self.ship_min_y())
    self.shot_cooldown = 0

    self.bunkers = [Pos(-1, self.ship_min_y() - 1) for _ in range(4)]
    for b in self.bunkers:
      b.health = INITIAL_HEALTH

    self.bullets: list[Pos] = []

  def ship_min_y(self):
    return 3 * self.display.rows // 4

  def bunker_min_y(self):
    return min(2 * self.display.rows // 3, self.ship_min_y() - 1)

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
    self.updateBunkers()
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
    self.ship.y = sorted((self.ship_min_y(), self.ship.y, self.display.rows - 1))[1]

  def updateBunkers(self):
    self.all_bunkers = []
    for x in range(0, self.display.cols):
      i = 9 * x // self.display.cols
      if i % 2 == 0: continue
      i //= 2

      bunker = self.bunkers[i]
      if bunker.health <= 0: continue

      for y in range(self.bunker_min_y(), self.ship_min_y()):
        p = Pos(x, y)
        p.bunk = bunker
        self.all_bunkers.append(p)

  def updateBullets(self):
    if self.shot_cooldown:
      self.shot_cooldown -= 1
    elif self.controls.fire():
      self.shot_cooldown = SHOT_COOLDOWN

      shot = Pos()
      shot.x = self.ship.x
      shot.y = self.ship.y
      shot.dy = -1
      self.bullets.append(shot)

    grid = {}
    for p in self.all_bunkers:
      grid[p.x, p.y] = p.bunk

    next_bullets = []
    for b in self.bullets:
      b.update()

      if b.y < 0: continue

      p = b.x, b.y
      if p in grid:
        bunker = grid[p]
        bunker.health -= 1
        continue

      next_bullets.append(b)

    self.bullets = next_bullets
