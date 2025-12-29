# main.py
import pygame
from settings import WIDTH, HEIGHT, FPS
from menu import Menu
from map import MapSelection
from play import Play

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("New Game")
    clock = pygame.time.Clock()

    running = True
    current_screen = "menu"
    while running:
        if current_screen == "menu":
            menu = Menu(screen)
            action = menu.run()

            if action == "quit":
                running = False
            elif action == "map":
                current_screen = "map"

        elif current_screen == "map":
            map_screen = MapSelection(screen)
            map_file = map_screen.run()

            if map_file == "quit":
                running = False
            elif map_file == "menu":
                current_screen = "menu"
            else:
                current_screen = "play"

        elif current_screen == "play":
            play_screen = Play(screen, map_file)
            result, next_map_file = play_screen.run()

            if result == "menu":
                current_screen = "menu"

            elif result == "map":
                current_screen = "map"

            elif result in ("win", "next") and next_map_file:
                map_file = next_map_file
                current_screen = "play"

            else:
                current_screen = "map"


    pygame.quit()

if __name__ == "__main__":
    main()
