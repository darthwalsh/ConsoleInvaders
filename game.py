import random
import time
from enum import Enum

FPS = 30
BUNKER_INITIAL_HEALTH = 9
BUNKER_DAMAGE_CHANCE = 0.3
SHOT_COOLDOWN = 6
ENEMY_MOVE_COOLDOWN = 2
BOMB_CHANCE = 0.01

class Pos:

  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y
    self.dx = 0
    self.dy = 0

  def update(self):
    self.x += self.dx
    self.y += self.dy

  def xy(self):
    return self.x, self.y

  def __repr__(self):
    xy = f"{self.x},{self.y}"
    if self.dx or self.dy:
      return f"{xy} + {self.dx},{self.dy}"
    return xy

class EnemyState(Enum):
  RIGHT = 1
  AT_RIGHT_DOWN = 2
  LEFT = 3
  AT_LEFT_DOWN = 4

class Game:

  def __init__(self, display, controls):
    self.display = display
    self.controls = controls
    self.over = False

    self.ship = Pos(display.cols // 2, self.ship_min_y())
    self.shot_cooldown = 0

    self.bunkers = [Pos(-1, self.bunker_min_y() - 5) for _ in range(4)]
    for b in self.bunkers:
      b.health = BUNKER_INITIAL_HEALTH

    self.enemies: list[Pos] = [
        Pos(x, y) for x in range(0, self.display.cols - 4, 8) for y in range(0,
                                                                             self.bunker_min_y() - 2, 6)
    ]
    for e in self.enemies:
      e.dead = False
      e.dx = 1
    self.enemy_move_cooldown = 0
    self.enemyState = EnemyState.RIGHT

    self.bombs: list[Pos] = []

    self.bullets: list[Pos] = []

  def ship_min_y(self):
    return 3 * self.display.rows // 4

  def bunker_min_y(self):
    return min(2 * self.display.rows // 3, self.ship_min_y() - 1)

  def on_quit(self):
    self.over = True

  def run(self):
    while not self.controls.stop and not self.over:
      self.update()
      self.display.draw(self)
      try:
        time.sleep(1 / FPS)
      except KeyboardInterrupt:
        break

  def update(self):
    self.updateShip()
    self.updateBunkers()
    self.updateEnemies()
    self.updateBullets()

    if not self.enemies:
      self.over = True

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
      if i % 2 == 0:
        continue
      i //= 2

      bunker = self.bunkers[i]
      if bunker.health <= 0:
        continue

      for y in range(self.bunker_min_y(), self.ship_min_y()):
        p = Pos(x, y)
        p.bunk = bunker
        self.all_bunkers.append(p)

  def damage_bunker(self, bunker):
    if not bunker.health:
      return

    if random.random() < BUNKER_DAMAGE_CHANCE:
      bunker.health -= 1

  def updateEnemies(self):
    dx, dy = self.enemies[0].dx, self.enemies[0].dy

    if self.enemy_move_cooldown:
      self.enemy_move_cooldown -= 1
    else:
      self.enemy_move_cooldown = ENEMY_MOVE_COOLDOWN

      new_dxy = self.moveEnemies()
      if new_dxy:
        dx, dy = new_dxy

    next_enemies = []
    for e in self.enemies:
      if e.dead:
        continue
      e.dx = dx
      e.dy = dy
      next_enemies.append(e)

      if random.random() < BOMB_CHANCE:
        bomb = Pos(*e.xy())
        bomb.dy = 1
        self.bombs.append(bomb)

    self.enemies = next_enemies

  def moveEnemies(self):
    at_edge = False
    for e in self.enemies:
      e.update()
      if e.x == 0 or e.x == self.display.cols - 1:
        at_edge = True
      if e.y >= self.display.rows - 2:
        self.over = True

    if self.enemyState == EnemyState.RIGHT:
      if at_edge:
        self.enemyState = EnemyState.AT_RIGHT_DOWN
        return 0, 1
    elif self.enemyState == EnemyState.AT_RIGHT_DOWN:
      self.enemyState = EnemyState.LEFT
      return -1, 0
    elif self.enemyState == EnemyState.LEFT:
      if at_edge:
        self.enemyState = EnemyState.AT_LEFT_DOWN
        return 0, 1
    elif self.enemyState == EnemyState.AT_LEFT_DOWN:
      self.enemyState = EnemyState.RIGHT
      return 1, 0
    else:
      raise ValueError("unknown state!")

  def updateBullets(self):
    if self.shot_cooldown:
      self.shot_cooldown -= 1
    elif self.controls.fire():
      self.shot_cooldown = SHOT_COOLDOWN

      shot = Pos(*self.ship.xy())
      shot.dy = -1
      self.bullets.append(shot)

    grid = {}
    for p in self.all_bunkers:
      grid[p.xy()] = "B", p.bunk

    for e in self.enemies:
      # Make the hitbox 3 wide
      for xx in (e.x - 1, e.x, e.x + 1):
        p = xx, e.y
        if p in grid:
          _, bunker = grid[p]
          self.damage_bunker(bunker)
          e.dead = True
          continue
        grid[p] = "E", e

    grid[self.ship.xy()] = "P", self.ship

    next_bullets = []
    for b in self.bullets:
      b.update()

      if b.y < 0:
        continue

      if b.xy() in grid:
        kind, o = grid[b.xy()]
        if kind == 'B':
          self.damage_bunker(o)
        elif kind == 'E':
          o.dead = True
        elif kind == 'P':
          pass
        else:
          raise ValueError(f"Unknown kind {kind}")
        continue

      next_bullets.append(b)
    self.bullets = next_bullets

    next_bombs = []
    for b in self.bombs:
      b.update()

      if b.y >= self.display.rows:
        continue

      if b.xy() in grid:
        kind, o = grid[b.xy()]
        if kind == 'B':
          self.damage_bunker(o)
        elif kind == 'E':
          next_bombs.append(b)
        elif kind == 'P':
          self.over = True
        else:
          raise ValueError(f"Unknown kind {kind}")
        continue
      next_bombs.append(b)
    self.bombs = next_bombs
