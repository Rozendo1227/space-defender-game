import pygame
import random

class Enemy:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(3, 6)

        self.image = pygame.image.load("asset/Imagens/enemy.png")
        self.image = pygame.transform.scale(self.image, (40, 30))

    def move(self):
        self.x -= self.speed

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))