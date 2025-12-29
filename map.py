# map.py
import pygame
from settings import GRAY, DARK_GRAY, GREEN
from utils import draw_button
from game_data import MAPS


class MapSelection:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)
        self.back_btn = pygame.Rect(20, 20, 100, 40)
        self.map_buttons = []
        self.create_buttons()

    def create_buttons(self):
        x_start, y_start = 150, 150
        gap = 160
        for i, map_data in enumerate(MAPS):
            rect = pygame.Rect(x_start + i*gap, y_start, 120, 60)
            self.map_buttons.append((rect, map_data))

    def draw_text_center(self, text, rect):
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_btn.collidepoint(event.pos):
                        return "menu"

                    for rect, map_data in self.map_buttons:
                        if rect.collidepoint(event.pos) and map_data["unlocked"]:
                            return map_data["file"]  # ✅ CHỈ TRẢ FILE

            self.screen.fill((0, 0, 0))

            back_color = (170, 170, 170) if self.back_btn.collidepoint(mouse_pos) else GRAY
            draw_button(self.screen, self.back_btn, back_color)
            self.draw_text_center("Back", self.back_btn)

            for rect, map_data in self.map_buttons:
                if map_data["completed"]:
                    color = GREEN
                elif map_data["unlocked"]:
                    color = GRAY
                else:
                    color = DARK_GRAY

                if rect.collidepoint(mouse_pos) and map_data["unlocked"]:
                    color = (200, 200, 200)

                draw_button(self.screen, rect, color)
                self.draw_text_center(f"Map {map_data['id']}", rect)

            pygame.display.flip()

