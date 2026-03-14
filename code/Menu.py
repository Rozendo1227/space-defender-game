import pygame


class Menu:

    def __init__(self, window):
        self.window = window
        self.running = True

    def run(self):

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        self.running = False

            self.draw()

    def draw(self):

        self.window.fill((5, 5, 30))

        font_title = pygame.font.SysFont(None, 60)
        font_text = pygame.font.SysFont(None, 30)

        title = font_title.render("SPACE DEFENDER", True, (255,255,255))
        text = font_text.render("Pressione ENTER para jogar", True, (200,200,200))

        self.window.blit(title, (180,150))
        self.window.blit(text, (200,250))

        pygame.display.update()