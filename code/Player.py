from code.Entity import Entity
from code.Const import PLAYER_SPEED


class Player(Entity):

    def __init__(self, x, y):
        super().__init__("Player", x, y, PLAYER_SPEED)

    def move(self, direction):

        if direction == "UP":
            self.y -= self.speed

        if direction == "DOWN":
            self.y += self.speed