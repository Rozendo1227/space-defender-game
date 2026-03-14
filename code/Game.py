import pygame
import random

from code.Const import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from code.Player import Player
from code.Enemy import Enemy
from code.PlayerShot import PlayerShot
from code.Score import Score
from code.Menu import Menu


class Game:

    def __init__(self):

        pygame.init()

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        menu = Menu(self.window)
        menu.run()
        pygame.display.set_caption("Space Defender")

        self.clock = pygame.time.Clock()
        self.running = True

        # jogador
        self.player = Player(100, 200)
        self.score = Score()

        # inimigos
        self.enemies = []

        for i in range(5):
            x = random.randint(500, 800)
            y = random.randint(50, 400)
            self.enemies.append(Enemy(x, y))

        # tiros
        self.shots = []

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                # disparar tiro
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        shot = PlayerShot(self.player.x + 40, self.player.y + 10)
                        self.shots.append(shot)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.player.move("UP")

            if keys[pygame.K_DOWN]:
                self.player.move("DOWN")

            self.update()
            self.draw()

        pygame.quit()

    def update(self):

        # mover inimigos
        for enemy in self.enemies:
            enemy.move()
            # colisão com o inimigo x jogador
            if abs(enemy.x - self.player.x) < 40 and abs(enemy.y - self.player.y) < 40:
                print("GAME OVER")
                self.running = False

            if enemy.x < -40:
                enemy.x = random.randint(500, 800)
                enemy.y = random.randint(50, 400)

        # mover tiros
        for shot in self.shots:
            shot.move()

        # verificar colisão tiro x inimigo
        for enemy in self.enemies:
            for shot in self.shots:

                if abs(enemy.x - shot.x) < 30 and abs(enemy.y - shot.y) < 30:
                    # reposicionar inimigo
                    enemy.x = random.randint(500, 800)
                    enemy.y = random.randint(50, 400)
                    self.score.add(1)
                    # remover tiro
                    self.shots.remove(shot)

                    break

    def draw(self):

        self.window.fill((10, 10, 40))

        # jogador
        pygame.draw.rect(self.window, (0, 255, 0), (self.player.x, self.player.y, 40, 20))

        # inimigos
        for enemy in self.enemies:
            pygame.draw.rect(self.window, (255, 0, 0), (enemy.x, enemy.y, 40, 20))

        # tiros
        for shot in self.shots:
            pygame.draw.rect(self.window, (255, 255, 0), (shot.x, shot.y, 10, 4))
            font = pygame.font.SysFont(None, 30)
            text = font.render("Score: " + str(self.score.value), True, (255, 255, 255))
            self.window.blit(text, (10, 10))

        pygame.display.update()