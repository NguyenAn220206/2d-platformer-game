import pygame
import importlib
from trap import Trap
from enemy import Enemy

class Level:
    TILE_SIZE = 50

    def __init__(self, map_file):
        self.map_file = map_file

        self.terrain = []
        self.traps = []
        self.enemies = []       # ✅ khai báo enemy
        self.player_start = None
        self.key_rect = None

        self.map_width = 0
        self.map_height = 0

        self.load_map()

    def load_map(self):
        # import module map
        module_path = self.map_file.replace("/", ".").replace(".py", "")
        level_module = importlib.import_module(module_path)
        world_map = level_module.world_map

        # reset các list
        self.terrain.clear()
        self.traps.clear()
        self.enemies.clear()
        self.player_start = None
        self.key_rect = None

        rows = len(world_map)
        cols = max(len(row) for row in world_map)

        self.map_width = cols * self.TILE_SIZE
        self.map_height = rows * self.TILE_SIZE

        for row_idx, row in enumerate(world_map):
            for col_idx, tile in enumerate(row):
                x = col_idx * self.TILE_SIZE
                y = row_idx * self.TILE_SIZE

                if tile == "X":
                    self.terrain.append(
                        pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                    )
                elif tile == "P":
                    self.player_start = (x, y)
                elif tile == "G":
                    self.key_rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                elif tile == "T":
                    self.traps.append(Trap(x, y, self.TILE_SIZE))
                elif tile == "E":
                    self.enemies.append(Enemy(x, y))

        # kiểm tra bắt buộc
        if self.player_start is None:
            raise ValueError("Map chưa có P (Player start)")
        if self.key_rect is None:
            raise ValueError("Map chưa có G (Goal)")
