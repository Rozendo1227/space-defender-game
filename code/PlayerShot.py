import pygame

class PlayerShot:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

        self.image = pygame.image.load("asset/Imagens/shot.png")
        self.image = pygame.transform.scale(self.image, (20, 8))  # ajuste tamanho aqui

    def move(self):
        self.x += self.speed

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))