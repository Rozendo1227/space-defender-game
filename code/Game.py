import pygame
import random
from datetime import datetime

from code.Const import *
from code.Player import Player
from code.Enemy import Enemy
from code.PlayerShot import PlayerShot
from code.Score import Score
from code.Menu import Menu


class EnemyShot:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.x -= self.speed


class Game:

    def __init__(self):

        pygame.init()
        pygame.mixer.init()  # 🔊 Inicializa o mixer de som

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Defender")

        self.clock = pygame.time.Clock()
        self.running = True

        self.state = "menu"
        self.menu = Menu(self.window)

        # 🔊 EFEITOS SONOROS
        self.sound_shoot = pygame.mixer.Sound("asset/Sons/shoot.wav")
        self.sound_explosion = pygame.mixer.Sound("asset/Sons/explosion.wav")

        # 🎵 MÚSICA DE FUNDO (começa no menu)
        pygame.mixer.music.load("asset/Sons/menu.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # PLAYER
        self.current_player = 1
        self.player = Player(100, 250, self.current_player)

        self.score = Score()

        self.enemies = []
        self.shots = []
        self.enemy_shots = []
        self.powerups = []

        self.player_health = 100
        self.shot_level = 1

        # MODES
        self.mode = "1P"
        self.player1_score = 0
        self.player2_score = 0

        # SCORE
        self.player_name = ""
        self.final_score = 0

        # WINNER
        self.winner = ""

        # LEVEL/TIME
        self.level = 1
        self.level_duration = 60
        self.level_start_time = pygame.time.get_ticks()

        # POWERUP TIMER
        self.last_powerup = pygame.time.get_ticks()

        # BACKGROUND
        self.bg_menu = pygame.image.load("asset/Imagens/background1.png")
        self.bg_menu = pygame.transform.scale(self.bg_menu, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.bg_game = pygame.image.load("asset/Imagens/background2.png")
        self.bg_game = pygame.transform.scale(self.bg_game, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.bg_x1 = 0
        self.bg_x2 = WINDOW_WIDTH

        # IMAGES
        self.enemy_img = pygame.image.load("asset/Imagens/enemy.png")
        self.enemy_img = pygame.transform.scale(self.enemy_img, (40, 30))

        self.enemy_shot_img = pygame.image.load("asset/Imagens/shot.png")
        self.enemy_shot_img = pygame.transform.scale(self.enemy_shot_img, (20, 8))

    # ================= BACKGROUND =================

    def get_bg(self):
        return self.bg_menu if self.state == "menu" else self.bg_game

    def update_bg(self):
        speed = 2
        self.bg_x1 -= speed
        self.bg_x2 -= speed

        if self.bg_x1 <= -WINDOW_WIDTH:
            self.bg_x1 = self.bg_x2 + WINDOW_WIDTH

        if self.bg_x2 <= -WINDOW_WIDTH:
            self.bg_x2 = self.bg_x1 + WINDOW_WIDTH

    def draw_bg(self):
        bg = self.get_bg()
        self.window.blit(bg, (self.bg_x1, 0))
        self.window.blit(bg, (self.bg_x2, 0))

    # ================= SCORE =================

    def load_scores(self):
        scores = []
        try:
            with open("scores.txt", "r") as f:
                for line in f:
                    name, score, date = line.strip().split(",")
                    scores.append((name, int(score), date))
        except:
            pass

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:10]

    def save_score(self, name, score):
        scores = self.load_scores()
        date = datetime.now().strftime("%d/%m/%y")

        scores.append((name, score, date))
        scores.sort(key=lambda x: x[1], reverse=True)
        scores = scores[:10]

        with open("scores.txt", "w") as f:
            for s in scores:
                f.write(f"{s[0]},{s[1]},{s[2]}\n")

    # ================= RESET =================

    def restart(self):
        self.player_health = 100
        self.shot_level = 1
        self.player_name = ""

        self.enemies.clear()
        self.shots.clear()
        self.enemy_shots.clear()
        self.powerups.clear()

        self.player = Player(100, 250, self.current_player)

        self.level = 1
        self.level_start_time = pygame.time.get_ticks()

    # ================= TROCA DE MÚSICA =================

    def play_music(self, state):
        """Troca a música de fundo conforme o estado do jogo."""
        try:
            if state == "menu":
                pygame.mixer.music.load("asset/Sons/menu.wav")
            elif state == "game":
                pygame.mixer.music.load("asset/Sons/game.wav")
            else:
                return  # Outras telas não têm música específica

            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erro ao carregar música ({state}):", e)

    # ================= LOOP =================

    def run(self):

        last_state = self.state

        while self.running:

            self.clock.tick(FPS)

            # 🎵 Troca música ao mudar de estado
            if self.state != last_state:
                self.play_music(self.state)
                last_state = self.state

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE and self.state != "enter_name":
                        self.state = "menu"

                    # MENU
                    if self.state == "menu":

                        if event.key == pygame.K_UP:
                            self.menu.move_up()

                        if event.key == pygame.K_DOWN:
                            self.menu.move_down()

                        if event.key == pygame.K_RETURN:

                            if self.menu.selected == 0:
                                self.mode = "1P"
                                self.score.value = 0
                                self.current_player = 1
                                self.restart()
                                self.state = "game"

                            elif self.menu.selected == 1:
                                self.mode = "coop"
                                self.current_player = 1
                                self.score.value = 0
                                self.restart()
                                self.state = "game"

                            elif self.menu.selected == 2:
                                self.mode = "versus"
                                self.current_player = 1
                                self.player1_score = 0
                                self.player2_score = 0
                                self.score.value = 0
                                self.restart()
                                self.state = "game"

                            elif self.menu.selected == 3:
                                self.state = "score"

                            elif self.menu.selected == 4:
                                self.running = False

                    # GAME
                    elif self.state == "game":

                        if event.key == pygame.K_SPACE:
                            self.sound_shoot.play()  # 🔫 Som de tiro

                            for i in range(self.shot_level):
                                self.shots.append(
                                    PlayerShot(
                                        self.player.x + 40,
                                        self.player.y + 10 + (i * 10)
                                    )
                                )

                    # ENTER NAME
                    elif self.state == "enter_name":

                        if event.key == pygame.K_RETURN and len(self.player_name) > 0:
                            self.save_score(self.player_name, self.final_score)
                            self.player_name = ""
                            self.state = "menu"

                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]

                        else:
                            if len(self.player_name) < 3 and event.unicode.isalpha():
                                self.player_name += event.unicode.upper()

                    # WINNER
                    elif self.state == "winner":

                        if event.key == pygame.K_RETURN:
                            self.player_name = ""
                            self.state = "enter_name"

            self.update_bg()

            if self.state == "game":

                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP]:
                    self.player.move("UP")

                if keys[pygame.K_DOWN]:
                    self.player.move("DOWN")

                self.update()
                self.draw()

            elif self.state == "menu":
                self.draw_bg()
                self.menu.draw()

            elif self.state == "score":
                self.draw_score()

            elif self.state == "enter_name":
                self.draw_enter_name()

            elif self.state == "winner":
                self.draw_winner()

        pygame.quit()

    # ================= UPDATE =================

    def update(self):

        elapsed = (pygame.time.get_ticks() - self.level_start_time) / 1000
        if elapsed >= self.level_duration:
            self.level += 1
            self.level_start_time = pygame.time.get_ticks()

        while len(self.enemies) < 5:
            self.enemies.append(Enemy(random.randint(600, 900),
                                      random.randint(50, 500)))

        for enemy in self.enemies[:]:
            enemy.move()

            if enemy.x < -50:
                self.enemies.remove(enemy)
                continue

            if random.randint(1, 80) == 1:
                self.enemy_shots.append(
                    EnemyShot(enemy.x, enemy.y + 10, 6)
                )

            if abs(enemy.x - self.player.x) < 40 and abs(enemy.y - self.player.y) < 40:
                self.handle_game_over()

        for shot in self.shots[:]:
            shot.move()

            for enemy in self.enemies[:]:
                if abs(shot.x - enemy.x) < 30 and abs(shot.y - enemy.y) < 30:
                    self.sound_explosion.play()  # 💥 Som de explosão ao matar inimigo
                    self.enemies.remove(enemy)
                    self.shots.remove(shot)
                    self.score.add(100)
                    break

        for shot in self.enemy_shots[:]:
            shot.move()

            if abs(shot.x - self.player.x) < 30 and abs(shot.y - self.player.y) < 30:
                self.sound_explosion.play()  # 💥 Som ao levar dano
                self.enemy_shots.remove(shot)
                self.player_health -= 20

                if self.player_health <= 0:
                    self.handle_game_over()

        # POWERUP
        now = pygame.time.get_ticks()
        if now - self.last_powerup > 15000:
            self.powerups.append([random.randint(400, 800), random.randint(100, 400)])
            self.last_powerup = now

    # ================= GAME OVER =================

    def handle_game_over(self):

        self.player_name = ""

        if self.mode == "1P":
            self.final_score = self.score.value
            self.state = "enter_name"

        elif self.mode == "coop":

            if self.current_player == 1:
                self.current_player = 2
                self.restart()
            else:
                self.final_score = self.score.value
                self.state = "enter_name"

        elif self.mode == "versus":

            if self.current_player == 1:
                self.player1_score = self.score.value
                self.current_player = 2
                self.score.value = 0
                self.restart()

            else:
                self.player2_score = self.score.value

                if self.player1_score > self.player2_score:
                    self.winner = "PLAYER 1 WINS"
                    self.final_score = self.player1_score
                elif self.player2_score > self.player1_score:
                    self.winner = "PLAYER 2 WINS"
                    self.final_score = self.player2_score
                else:
                    self.winner = "DRAW"
                    self.final_score = self.player1_score

                self.state = "winner"

    # ================= DRAW =================

    def draw(self):

        self.draw_bg()

        self.player.draw(self.window)

        for enemy in self.enemies:
            self.window.blit(self.enemy_img, (enemy.x, enemy.y))

        for shot in self.shots:
            shot.draw(self.window)

        for shot in self.enemy_shots:
            img = pygame.transform.flip(self.enemy_shot_img, True, False)
            self.window.blit(img, (shot.x, shot.y))

        # HUD
        elapsed = (pygame.time.get_ticks() - self.level_start_time) / 1000
        time_left = int(self.level_duration - elapsed)

        font = pygame.font.SysFont(None, 28)

        hud1 = font.render(
            f"Player {self.current_player} | Level {self.level} | Time: {time_left}s",
            True, (0, 255, 0)
        )

        hud2 = font.render(
            f"Health: {self.player_health} | Score: {self.score.value}",
            True, (0, 255, 0)
        )

        self.window.blit(hud1, (10, 10))
        self.window.blit(hud2, (10, 40))

        pygame.display.update()

    # ================= SCREENS =================

    def draw_score(self):

        self.draw_bg()

        title_font = pygame.font.SysFont(None, 60)
        font = pygame.font.SysFont(None, 35)

        title = title_font.render("TOP 10 SCORE", True, (255, 215, 0))
        self.window.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 80))

        y = 160
        for name, score, date in self.load_scores():
            text = font.render(f"{name}   {str(score).zfill(5)}   {date}",
                               True, (255, 255, 255))
            self.window.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, y))
            y += 40

        pygame.display.update()

    def draw_enter_name(self):

        self.draw_bg()

        font_big = pygame.font.SysFont(None, 60)
        font = pygame.font.SysFont(None, 40)

        title = font_big.render("ENTER YOUR INITIALS", True, (255, 255, 255))
        self.window.blit(title, (200, 150))

        name = self.player_name.ljust(3, "_")
        name_text = font_big.render(name, True, (255, 255, 0))
        self.window.blit(name_text, (350, 250))

        score_text = font.render(f"SCORE: {self.final_score}",
                                 True, (255, 255, 255))
        self.window.blit(score_text, (320, 330))

        pygame.display.update()

    def draw_winner(self):

        self.draw_bg()

        font_big = pygame.font.SysFont(None, 70)
        font = pygame.font.SysFont(None, 40)

        title = font_big.render(self.winner, True, (255, 215, 0))
        self.window.blit(title,
                         (WINDOW_WIDTH//2 - title.get_width()//2, 150))

        s1 = font.render(f"Player 1: {self.player1_score}", True, (255, 255, 255))
        s2 = font.render(f"Player 2: {self.player2_score}", True, (255, 255, 255))

        self.window.blit(s1, (WINDOW_WIDTH//2 - s1.get_width()//2, 260))
        self.window.blit(s2, (WINDOW_WIDTH//2 - s2.get_width()//2, 310))

        info = font.render("PRESS ENTER", True, (200, 200, 200))
        self.window.blit(info, (WINDOW_WIDTH//2 - info.get_width()//2, 420))

        pygame.display.update()