import pygame

class Player:

    def __init__(self, x, y, player_id=1):
        self.x = x
        self.y = y
        self.player_id = player_id

        # escolher imagem conforme o jogador
        if self.player_id == 1:
            img_path = "asset/Imagens/player1.png"
        else:
            img_path = "asset/Imagens/player2.png"

        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (50, 30))

    def move(self, direction):

        if direction == "UP":
            self.y -= 5

        if direction == "DOWN":
            self.y += 5

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))