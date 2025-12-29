import pygame
from settings import FPS
from game_data import MAPS
from level import Level


class Play:
    def __init__(self, screen, map_file):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.map_file = map_file

        # ===== MAP INFO =====
        self.map_id = None
        for m in MAPS:
            if m["file"] == map_file:
                self.map_id = m["id"]
                break

        self.running = True
        self.result = None
        self.next_map_file = None
        self.show_end_buttons = False

        self.camera_x = 0

        # ===== LOAD ASSETS + LEVEL =====
        self.load_assets()
        self.level = Level(map_file)

        self.load_player()
        self.player_rect.topleft = self.level.player_start

        # ===== FONTS =====
        self.font = pygame.font.SysFont(None, 40)
        self.map_font = pygame.font.SysFont("arial", 28, bold=True)

        # ===== BUTTONS =====
        cx = self.screen.get_width() // 2
        cy = self.screen.get_height() // 2

        self.next_btn = pygame.Rect(0, 0, 220, 50)
        self.next_btn.center = (cx, cy)

        self.restart_btn = pygame.Rect(0, 0, 220, 50)
        self.restart_btn.center = (cx, cy + 70)

        self.menu_btn = pygame.Rect(0, 0, 220, 50)
        self.menu_btn.center = (cx, cy + 140)

    # ================= ASSETS =================
    def load_assets(self):
        self.background = pygame.image.load("assets/terrain/ground.png").convert()
        self.stone_img = pygame.transform.scale(
            pygame.image.load("assets/terrain/stone.png").convert_alpha(), (50, 50)
        )
        self.key_img = pygame.transform.scale(
            pygame.image.load("assets/terrain/key.png").convert_alpha(), (50, 50)
        )

    # ================= PLAYER =================
    def load_player(self):
        self.anim = {"idle": [], "walk": [], "jump": [], "fall": []}

        def load(cur, path, n):
            for i in range(1, n + 1):
                img = pygame.image.load(f"{path}_{i}.png").convert_alpha()
                self.anim[cur].append(pygame.transform.scale(img, (50, 50)))

        load("idle", "assets/player/idle/idle", 1)
        load("walk", "assets/player/walk/walk", 4)
        load("jump", "assets/player/jump/jump", 2)
        load("fall", "assets/player/fall/fall", 1)

        self.player_rect = self.anim["idle"][0].get_rect()
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -18
        self.gravity = 0.7
        self.face_right = True
        self.action = "idle"
        self.frame = 0

    # ================= LOGIC =================
    def on_ground(self):
        for t in self.level.terrain:
            if (
                self.player_rect.bottom == t.top
                and self.player_rect.right > t.left
                and self.player_rect.left < t.right
            ):
                return True
        return False

    def handle_events(self):
        mouse = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
                self.result = "menu"

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.running = False
                self.result = "menu"

            if e.type == pygame.MOUSEBUTTONDOWN and self.show_end_buttons:
                if self.restart_btn.collidepoint(mouse):
                    self.__init__(self.screen, self.map_file)

                elif self.result == "win" and self.next_btn.collidepoint(mouse):
                    self.next_map_file = self.get_next_map()
                    self.running = False

                elif self.menu_btn.collidepoint(mouse):
                    self.running = False
                    self.result = "map"

    def get_next_map(self):
        for i, m in enumerate(MAPS):
            if m["file"] == self.map_file and i + 1 < len(MAPS):
                return MAPS[i + 1]["file"]
        return None

    def update(self):
        if self.show_end_buttons:
            return

        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.face_right = False
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            self.face_right = True

        # ===== MOVE PLAYER HORIZONTALLY =====
        self.player_rect.x += dx
        for t in self.level.terrain:
            if self.player_rect.colliderect(t):
                if dx > 0:
                    self.player_rect.right = t.left
                elif dx < 0:
                    self.player_rect.left = t.right

        # ===== JUMP =====
        if keys[pygame.K_SPACE] and self.on_ground():
            self.vel_y = self.jump_power

        # ===== APPLY GRAVITY =====
        self.vel_y += self.gravity
        self.player_rect.y += self.vel_y

        # ===== VERTICAL COLLISION =====
        for t in self.level.terrain:
            if self.player_rect.colliderect(t):
                if self.vel_y > 0:  # rơi xuống
                    self.player_rect.bottom = t.top
                    self.vel_y = 0
                elif self.vel_y < 0:  # nhảy lên
                    self.player_rect.top = t.bottom
                    self.vel_y = 0

        # ===== WIN =====
        if self.player_rect.colliderect(self.level.key_rect):
            self.result = "win"
            self.show_end_buttons = True

            # UPDATE MAP STATUS
            for m in MAPS:
                if m["file"] == self.map_file:
                    m["completed"] = True
                    idx = m["id"] - 1
                    if idx + 1 < len(MAPS):
                        MAPS[idx + 1]["unlocked"] = True
                    break

        # ===== LOSE =====
        if self.player_rect.top > self.screen.get_height():
            self.result = "lose"
            self.show_end_buttons = True

        # ===== TRAPS =====
        for trap in self.level.traps:
            if trap.rect.right > self.camera_x and trap.rect.left < self.camera_x + self.screen.get_width():
                trap.update()
                if self.player_rect.colliderect(trap.rect):
                    self.result = "lose"
                    self.show_end_buttons = True
                    return

        # ===== ENEMIES =====
        for enemy in self.level.enemies:
            if enemy.rect.right > self.camera_x and enemy.rect.left < self.camera_x + self.screen.get_width():
                enemy.update(self.level.terrain, self.level.traps)
                if self.player_rect.colliderect(enemy.rect):
                    self.result = "lose"
                    self.show_end_buttons = True
                    return

        # ===== ANIMATION =====
        if self.vel_y < 0:
            self.action = "jump"
        elif self.vel_y > 1:
            self.action = "fall"
        elif dx != 0:
            self.action = "walk"
        else:
            self.action = "idle"

        self.frame = (self.frame + 0.2) % len(self.anim[self.action])

        # ===== CAMERA =====
        max_cam = self.level.map_width - self.screen.get_width()
        self.camera_x = max(0, min(self.player_rect.centerx - 400, max_cam))

    # ================= DRAW =================
    def draw(self):
        # ===== BACKGROUND =====
        bg_w = self.background.get_width()
        for x in range(-self.camera_x // bg_w * bg_w,
                       self.camera_x + self.screen.get_width(), bg_w):
            self.screen.blit(self.background, (x - self.camera_x, 0))

        # ===== TERRAIN =====
        for t in self.level.terrain:
            if t.right > self.camera_x and t.left < self.camera_x + self.screen.get_width():
                self.screen.blit(self.stone_img, (t.x - self.camera_x, t.y))

        # ===== TRAPS =====
        for trap in self.level.traps:
            if trap.rect.right > self.camera_x and trap.rect.left < self.camera_x + self.screen.get_width():
                trap.draw(self.screen, self.camera_x)

        # ===== KEY =====
        self.screen.blit(
            self.key_img,
            (self.level.key_rect.x - self.camera_x, self.level.key_rect.y),
        )

        # ===== MAP NAME =====
        if self.map_id is not None:
            map_text = self.map_font.render(f"Map {self.map_id}", True, (255, 255, 255))
            self.screen.blit(map_text, map_text.get_rect(midtop=(self.screen.get_width() // 2, 10)))

        # ===== ENEMIES =====
        for enemy in self.level.enemies:
            if enemy.rect.right > self.camera_x and enemy.rect.left < self.camera_x + self.screen.get_width():
                enemy.draw(self.screen, self.camera_x)

        # ===== PLAYER =====
        img = self.anim[self.action][int(self.frame)]
        if not self.face_right:
            img = pygame.transform.flip(img, True, False)
        self.screen.blit(img, (self.player_rect.x - self.camera_x, self.player_rect.y))

        # ===== END BUTTONS =====
        if not self.show_end_buttons:
            return

        cx = self.screen.get_width() // 2
        cy = self.screen.get_height() // 2 - 120

        text = "YOU WIN" if self.result == "win" else "YOU LOSE"
        color = (255, 255, 0) if self.result == "win" else (255, 0, 0)

        t = self.font.render(text, True, color)
        self.screen.blit(t, t.get_rect(center=(cx, cy)))

        mouse = pygame.mouse.get_pos()

        def draw_btn(btn, label):
            c = (180, 180, 180) if btn.collidepoint(mouse) else (120, 120, 120)
            pygame.draw.rect(self.screen, c, btn, border_radius=10)
            txt = self.font.render(label, True, (255, 255, 255))
            self.screen.blit(txt, txt.get_rect(center=btn.center))

        if self.result == "win" and self.get_next_map():
            draw_btn(self.next_btn, "Next Level")

        draw_btn(self.restart_btn, "Restart")
        draw_btn(self.menu_btn, "Choose Map")

    # ================= LOOP =================
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()

        return self.result, self.next_map_file
