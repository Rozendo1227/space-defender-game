from code.Entity import Entity


class PlayerShot(Entity):

    def __init__(self, x, y):
        super().__init__("PlayerShot", x, y, 10)

    def move(self):
        self.x += self.speed