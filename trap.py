import pygame


class Trap:
    def __init__(self, x, y, size):
        self.frames = []
        self.load_frames()

        self.index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.anim_speed = 0.2

    def load_frames(self):
        for i in range(1, 4):  # 1.png, 2.png, 3.png
            img = pygame.image.load(
                f"assets/trap/blade/{i}.png"
            ).convert_alpha()

            img = pygame.transform.scale(img, (50, 50))
            self.frames.append(img)

    def update(self):
        self.index += self.anim_speed
        if self.index >= len(self.frames):
            self.index = 0

        self.image = self.frames[int(self.index)]

    def draw(self, screen, camera_x):
        screen.blit(
            self.image,
            (self.rect.x - camera_x, self.rect.y)
        )
