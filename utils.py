# utils.py
import pygame

def draw_button(screen, rect, color, radius=12):
    pygame.draw.rect(screen, color, rect, border_radius=radius)
