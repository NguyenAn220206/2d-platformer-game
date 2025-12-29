# menu.py
import pygame
from settings import GRAY
from utils import draw_button


def draw_text_center(screen, text, rect, font, color=(255, 255, 255)):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.play_btn = pygame.Rect(400, 200, 200, 50)
        self.tutorial_btn = pygame.Rect(400, 270, 200, 50)
        self.exit_btn = pygame.Rect(400, 340, 200, 50)
        self.font = pygame.font.SysFont(None, 36)

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_btn.collidepoint(event.pos):
                        return "map"
                    if self.exit_btn.collidepoint(event.pos):
                        return "quit"

            self.screen.fill((0, 0, 0))

            def get_color(rect):
                return (170, 170, 170) if rect.collidepoint(mouse_pos) else GRAY

            play_color = get_color(self.play_btn)
            tutorial_color = get_color(self.tutorial_btn)
            exit_color = get_color(self.exit_btn)

            draw_button(self.screen, self.play_btn, play_color)
            draw_button(self.screen, self.tutorial_btn, tutorial_color)
            draw_button(self.screen, self.exit_btn, exit_color)

            draw_text_center(self.screen, "Play", self.play_btn, self.font)
            draw_text_center(self.screen, "Tutorial", self.tutorial_btn, self.font)
            draw_text_center(self.screen, "Exit", self.exit_btn, self.font)

            pygame.display.flip()
