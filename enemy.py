import pygame

class Enemy:
    def __init__(self, x, y, width=50, height=50, speed=2, move_auto=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.start_x = x
        self.width = width
        self.height = height
        self.speed = speed
        self.move_auto = move_auto  # Nếu True thì di chuyển tự động

        self.direction = 1  # 1 = sang phải, -1 = sang trái
        self.vel_y = 0
        self.gravity = 0.8

        # ===== LOAD ANIMATION =====
        self.animations = {"idle": [], "walk": []}
        self.action = "idle"
        self.frame = 0

        idle_img = pygame.image.load("assets/enemy/idle/idle_1.png").convert_alpha()
        self.animations["idle"].append(pygame.transform.scale(idle_img, (width, height)))

        for i in range(1, 3):  # walk_1.png, walk_2.png
            img = pygame.image.load(f"assets/enemy/walk/walk_{i}.png").convert_alpha()
            self.animations["walk"].append(pygame.transform.scale(img, (width, height)))

    def update(self, terrain, traps):
        # ===== GRAVITY =====
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # ===== CHECK TERRAIN COLLISION VERTICAL =====
        for t in terrain:
            if self.rect.colliderect(t) and self.vel_y > 0:
                self.rect.bottom = t.top
                self.vel_y = 0

        # ===== MOVEMENT =====
        if self.move_auto:
            self.rect.x += self.speed * self.direction
            # Đổi hướng nếu chạm terrain hoặc trap
            collision = False
            for t in terrain + [trap.rect for trap in traps]:
                if self.rect.colliderect(t):
                    collision = True
                    break
            if collision:
                self.direction *= -1
                self.rect.x += self.speed * self.direction  # di chuyển ngược lại ngay lập tức

            self.action = "walk"
        else:
            self.action = "idle"

        # ===== ANIMATION =====
        self.frame += 0.15
        if self.frame >= len(self.animations[self.action]):
            self.frame = 0

    def draw(self, screen, camera_x):
        img = self.animations[self.action][int(self.frame)]
        if self.direction < 0:  # nhìn sang trái
            img = pygame.transform.flip(img, True, False)
        screen.blit(img, (self.rect.x - camera_x, self.rect.y))
