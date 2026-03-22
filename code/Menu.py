import pygame
from code.Const import WINDOW_WIDTH


class Menu:

    def __init__(self, window):

        self.window = window

        self.options = [
            "NEW GAME 1P",
            "NEW GAME 2P (COOPERATIVE)",
            "NEW GAME 2P (COMPETITIVE)",
            "SCORE",
            "EXIT"
        ]

        self.selected = 0

    def move_up(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.options) - 1

    def move_down(self):
        self.selected += 1
        if self.selected >= len(self.options):
            self.selected = 0

    def draw(self):

        font = pygame.font.SysFont(None, 50)

        y = 220

        for i, option in enumerate(self.options):

            color = (255, 255, 0) if i == self.selected else (255, 255, 255)

            text = font.render(option, True, color)

            x = WINDOW_WIDTH // 2 - text.get_width() // 2

            self.window.blit(text, (x, y))

            y += 60

        pygame.display.update()