from code.Entity import Entity
from code.Const import ENEMY_SPEED


class Enemy(Entity):

    def __init__(self, x, y):
        super().__init__("Enemy", x, y, ENEMY_SPEED)

    def move(self):
        self.x -= self.speed