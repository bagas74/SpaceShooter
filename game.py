import math
import sys
import os # Untuk memeriksa keberadaan file gambar
import random # Modul ini wajib di-import
import pygame

# --- Inisialisasi Pygame SEBELUM memuat aset ---
pygame.init()
pygame.mixer.init()

# --- Variabel Lokal untuk Game ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN_ENEMY = (0, 200, 50)
FPS = 60 # Dibutuhkan untuk timer

# --- Warna-warna detail (Pesawat Dicerahkan) ---
COLOR_JET_BODY = (180, 190, 200)
COLOR_JET_OUTLINE = (40, 50, 60)
COLOR_JET_WING = (140, 150, 165)
COLOR_COCKPIT_BLUE = (0, 150, 255)
COLOR_COCKPIT_HIGHLIGHT = (200, 230, 255)
COLOR_ENGINE_POD = (100, 100, 100)
COLOR_RED_ACCENT = (200, 0, 0)
COLOR_STAR_RED = (200, 0, 0)

# Warna UFO Default
UFO_GREY_LIGHT = (180, 180, 180)
UFO_GREY_DARK = (100, 100, 100)
UFO_BLUE_DOME = (100, 200, 255)
UFO_BLUE_DOME_HIGHLIGHT = (200, 240, 255)
UFO_YELLOW_LIGHT = (255, 255, 0)
UFO_RED_FEET = (200, 0, 0)
UFO_OUTLINE = (50, 50, 50)

# Warna Musuh Penembak Lvl 2
ALIEN_BODY_DARK = (80, 0, 120)
ALIEN_BODY_LIGHT = (120, 0, 180)
ALIEN_ACCENT_GREEN = (0, 255, 150)
ALIEN_OUTLINE = (30, 0, 40)
ALIEN_GUN_RED = (255, 50, 50)
ALIEN_EYE_YELLOW = (255, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Font
font = pygame.font.SysFont(None, 55)
font_powerup = pygame.font.SysFont('arial', 22, bold=True)
font_ui = pygame.font.SysFont('arial', 24)
font_indicator = pygame.font.SysFont('arial', 36, bold=True)

# --- Warna Powerup ---
POWERUP_BLUE = (0, 191, 255)
POWERUP_ORANGE = (255, 165, 0)
POWERUP_RED = (200, 0, 0)
POWERUP_GREEN = (0, 255, 0)
POWERUP_PINK = (255, 105, 180)
POWERUP_YELLOW_LIGHT = (255, 255, 200)
POWERUP_YELLOW_DARK = (204, 204, 0)

# --- Coba muat file suara ---
try:
    suara_tembak = pygame.mixer.Sound("laser.wav")
    suara_ledakan = pygame.mixer.Sound("explosion.wav")
    suara_powerup = pygame.mixer.Sound("powerup.wav")
    suara_shield = pygame.mixer.Sound("powerup_shield.wav")
    suara_shockwave = pygame.mixer.Sound("shockwave.wav")
    suara_tembak_musuh = pygame.mixer.Sound("enemy_laser.wav")
    suara_laser = pygame.mixer.Sound("laser_beam.wav")
    suara_player_terkena = pygame.mixer.Sound("player_hit.wav")
    suara_player_terkena.set_volume(0.4)

    suara_tembak.set_volume(0.2)
    suara_ledakan.set_volume(0.1)
    suara_powerup.set_volume(0.3)
    suara_shield.set_volume(0.3)
    suara_shockwave.set_volume(0.4)
    suara_tembak_musuh.set_volume(0.1)
    suara_laser.set_volume(0.5)
except FileNotFoundError:
    print("Peringatan: File suara .wav tidak ditemukan. Game akan hening.")

    class NoSound:
        def play(self, *args, **kwargs): pass
        def stop(self): pass

    suara_tembak = NoSound()
    suara_ledakan = NoSound()
    suara_powerup = NoSound()
    suara_shield = NoSound()
    suara_shockwave = NoSound()
    suara_tembak_musuh = NoSound()
    suara_laser = NoSound()
    suara_player_terkena = suara_ledakan


# --- Muat gambar Musuh Lvl 1 (UFO Baru) ---
UFO_IMAGE_PATH = "enemy_ship1.png"
UFO_IMAGE = None
UFO_IMAGE_SIZE = (110,90) # Ukuran UFO default

if os.path.exists(UFO_IMAGE_PATH):
    try:
        UFO_IMAGE = pygame.image.load(UFO_IMAGE_PATH).convert_alpha()
        UFO_IMAGE = pygame.transform.scale(UFO_IMAGE, UFO_IMAGE_SIZE)
        print(f"Gambar musuh UFO '{UFO_IMAGE_PATH}' berhasil dimuat (Musuh Lvl 1).")
    except pygame.error as e:
        print(f"Error memuat gambar musuh UFO '{UFO_IMAGE_PATH}': {e}")
        UFO_IMAGE = None
else:
    print(f"Peringatan: Gambar musuh UFO '{UFO_IMAGE_PATH}' tidak ditemukan. Menggunakan bentuk default.")

# --- Muat gambar Musuh Penembak Lvl 2 ---
SHOOTER_IMAGE_PATH = "enemy_ship.png"
SHOOTER_IMAGE = None
SHOOTER_IMAGE_SIZE = (140, 85) 

if os.path.exists(SHOOTER_IMAGE_PATH):
    try:
        SHOOTER_IMAGE = pygame.image.load(SHOOTER_IMAGE_PATH).convert_alpha()
        SHOOTER_IMAGE = pygame.transform.scale(SHOOTER_IMAGE, SHOOTER_IMAGE_SIZE)
        print(f"Gambar musuh Penembak '{SHOOTER_IMAGE_PATH}' berhasil dimuat (Musuh Lvl 2).")
    except pygame.error as e:
        print(f"Error memuat gambar musuh Penembak '{SHOOTER_IMAGE_PATH}': {e}")
        SHOOTER_IMAGE = None
else:
    print(f"Peringatan: Gambar musuh Penembak '{SHOOTER_IMAGE_PATH}' tidak ditemukan. Menggunakan bentuk default.")

# --- Muat gambar Musuh Laser Lvl 3 (Bos Mini Baru) ---
LASER_BOSS_IMAGE_PATH = "enemy_ship_leser.png"
LASER_BOSS_IMAGE = None
LASER_BOSS_IMAGE_SIZE = (120, 100) # Ukuran Laser Boss default

if os.path.exists(LASER_BOSS_IMAGE_PATH):
    try:
        LASER_BOSS_IMAGE = pygame.image.load(LASER_BOSS_IMAGE_PATH).convert_alpha()
        LASER_BOSS_IMAGE = pygame.transform.scale(LASER_BOSS_IMAGE, LASER_BOSS_IMAGE_SIZE)
        print(f"Gambar musuh Laser Boss '{LASER_BOSS_IMAGE_PATH}' berhasil dimuat (Musuh Lvl 3).")
    except pygame.error as e:
        print(f"Error memuat gambar musuh Laser Boss '{LASER_BOSS_IMAGE_PATH}': {e}")
        LASER_BOSS_IMAGE = None
else:
    print(f"Peringatan: Gambar musuh Laser Boss '{LASER_BOSS_IMAGE_PATH}' tidak ditemukan. Menggunakan bentuk default.")

# Muat Gambar Player
PLAYER_IMAGE_PATH = "player_ship.png"
PLAYER_IMAGE = None
PLAYER_IMAGE_SIZE = (110, 80)

if os.path.exists(PLAYER_IMAGE_PATH):
    try:
        PLAYER_IMAGE = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
        PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, PLAYER_IMAGE_SIZE)
        print(f"Gambar player '{PLAYER_IMAGE_PATH}' berhasil dimuat.")
    except pygame.error as e:
        print(f"Error memuat gambar player '{PLAYER_IMAGE_PATH}': {e}")
        PLAYER_IMAGE = None
else:
    print(f"Peringatan: Gambar player '{PLAYER_IMAGE_PATH}' tidak ditemukan. Menggunakan bentuk default.")

# Variabel file high score
HIGHSCORE_FILE = "highscore.txt"

# --- Fungsi Helper (tetap sama) ---

def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                return int(f.read().strip())
        except ValueError:
            return 0
    return 0

def save_high_score(new_score):
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            f.write(str(new_score))
    except IOError as e:
        print(f"Tidak dapat menyimpan high score: {e}")


def draw_star(surface, color, center, outer_radius, inner_radius, num_points):
    points = []
    for i in range(num_points * 2):
        angle = i * math.pi / num_points
        radius = outer_radius if i % 2 == 0 else inner_radius
        angle_adjusted = angle - (math.pi / 2)
        x = center[0] + radius * math.cos(angle_adjusted)
        y = center[1] + radius * math.sin(angle_adjusted)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, COLOR_JET_OUTLINE, points, 2)


def draw_regular_polygon(surface, color, center, radius, num_points, rotation=0, width=0):
    points = []
    for i in range(num_points):
        angle = (i * 2 * math.pi / num_points) + rotation
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, width)


# Fungsi untuk menggambar UFO (musuh standar Lvl 1)
# --- MENGHAPUS LOGIKA GAMBAR DEFAULT DARI SINI, AKAN DIPINDAHKAN KE KELAS MUSUH ---
def draw_enemy_ufo(surface, rect):
    cx, cy = rect.centerx, rect.centery
    w, h = rect.width, rect.height
    l, r, t, b = rect.left, rect.right, rect.top, rect.bottom
    # Gambar Default UFO (digunakan jika UFO_IMAGE gagal dimuat)
    pygame.draw.ellipse(surface, UFO_GREY_DARK, [l, t + int(h * 0.4), w, int(h * 0.4)])
    pygame.draw.ellipse(surface, UFO_OUTLINE, [l, t + int(h * 0.4), w, int(h * 0.4)], 2)
    pygame.draw.ellipse(surface, UFO_GREY_LIGHT, [l, t + int(h * 0.3), w, int(h * 0.3)])
    pygame.draw.ellipse(surface, UFO_OUTLINE, [l, t + int(h * 0.3), w, int(h * 0.3)], 2)
    dome_rect = pygame.Rect(cx - int(w * 0.3), t, int(w * 0.6), int(h * 0.6))
    pygame.draw.ellipse(surface, UFO_BLUE_DOME, dome_rect)
    pygame.draw.ellipse(surface, UFO_OUTLINE, dome_rect, 2)
    highlight_rect = pygame.Rect(cx - int(w * 0.2), t + int(h * 0.1), int(w * 0.4), int(h * 0.3))
    pygame.draw.ellipse(surface, UFO_BLUE_DOME_HIGHLIGHT, highlight_rect)
    light_radius = int(w * 0.06)
    pygame.draw.circle(surface, UFO_YELLOW_LIGHT, (int(cx - w * 0.35), int(t + h * 0.45)), light_radius)
    pygame.draw.circle(surface, UFO_OUTLINE, (int(cx - w * 0.35), int(t + h * 0.45)), light_radius, 1)
    pygame.draw.circle(surface, UFO_YELLOW_LIGHT, (cx, int(t + h * 0.45)), light_radius)
    pygame.draw.circle(surface, UFO_OUTLINE, (cx, int(t + h * 0.45)), light_radius, 1)
    pygame.draw.circle(surface, UFO_YELLOW_LIGHT, (int(cx + w * 0.35), int(t + h * 0.45)), light_radius)
    pygame.draw.circle(surface, UFO_OUTLINE, (int(cx + w * 0.35), int(t + h * 0.45)), light_radius, 1)
    foot_y_start = t + int(h * 0.8)
    foot_y_end = b
    pygame.draw.polygon(surface, UFO_RED_FEET, [(cx - int(w*0.25), foot_y_start), (cx - int(w*0.3), foot_y_end), (cx - int(w*0.2), foot_y_end)])
    pygame.draw.polygon(surface, UFO_RED_FEET, [(cx, foot_y_start), (cx - int(w*0.05), foot_y_end), (cx + int(w*0.05), foot_y_end)])
    pygame.draw.polygon(surface, UFO_RED_FEET, [(cx + int(w*0.25), foot_y_start), (cx + int(w*0.2), foot_y_end), (cx + int(w*0.3), foot_y_end)])

# Fungsi untuk menggambar musuh penembak (Level 2)
# --- MENGHAPUS LOGIKA GAMBAR DEFAULT DARI SINI, AKAN DIPINDAHKAN KE KELAS MUSUH ---
def draw_shooter_enemy_default(surface, rect):
    cx, cy = rect.centerx, rect.centery
    w, h = rect.width, rect.height
    l, r, t, b = rect.left, rect.right, rect.top, rect.bottom
    body_points = [ (cx, t + h*0.1), (l + w*0.1, cy - h*0.2), (l, cy + h*0.1), (l + w*0.1, b - h*0.1), (cx, b), (r - w*0.1, b - h*0.1), (r, cy + h*0.1), (r - w*0.1, cy - h*0.2) ]
    pygame.draw.polygon(surface, ALIEN_BODY_DARK, body_points)
    pygame.draw.polygon(surface, ALIEN_OUTLINE, body_points, 2)
    core_rect = pygame.Rect(cx - w*0.25, cy - h*0.2, w*0.5, h*0.4)
    pygame.draw.ellipse(surface, ALIEN_BODY_LIGHT, core_rect)
    pygame.draw.ellipse(surface, ALIEN_OUTLINE, core_rect, 2)
    pygame.draw.circle(surface, ALIEN_EYE_YELLOW, (cx, cy), int(w*0.1))
    pygame.draw.circle(surface, ALIEN_OUTLINE, (cx, cy), int(w*0.1), 1)
    wing_width = w * 0.2
    wing_height = h * 0.15
    wing_left_points = [ (l + w*0.05, cy - wing_height/2), (l - w*0.05, cy), (l + w*0.05, cy + wing_height/2) ]
    pygame.draw.polygon(surface, ALIEN_ACCENT_GREEN, wing_left_points)
    pygame.draw.polygon(surface, ALIEN_OUTLINE, wing_left_points, 2)
    wing_right_points = [ (r - w*0.05, cy - wing_height/2), (r + w*0.05, cy), (r - w*0.05, cy + wing_height/2) ]
    pygame.draw.polygon(surface, ALIEN_ACCENT_GREEN, wing_right_points)
    pygame.draw.polygon(surface, ALIEN_OUTLINE, wing_right_points, 2)
    gun_radius = int(w * 0.08)
    gun_offset_x = w * 0.2
    gun_offset_y = h * 0.1
    pygame.draw.circle(surface, ALIEN_GUN_RED, (cx - gun_offset_x, b - gun_offset_y), gun_radius)
    pygame.draw.circle(surface, ALIEN_OUTLINE, (cx - gun_offset_x, b - gun_offset_y), gun_radius, 1)
    pygame.draw.circle(surface, ALIEN_GUN_RED, (cx + gun_offset_x, b - gun_offset_y), gun_radius)
    pygame.draw.circle(surface, ALIEN_OUTLINE, (cx + gun_offset_x, b - gun_offset_y), gun_radius, 1)
    

# Fungsi untuk menggambar musuh laser (Level 3 - Bos Mini)
# --- MENGHAPUS LOGIKA GAMBAR DEFAULT DARI SINI, AKAN DIPINDAHKAN KE KELAS MUSUH ---
def draw_boss_laser_ship_default(surface, rect):
    cx, cy = rect.centerx, rect.centery
    w, h = rect.width, rect.height
    l, r, t, b = rect.left, rect.right, rect.top, rect.bottom
    BOSS_DARK = (80, 80, 100)
    BOSS_LIGHT = (150, 150, 170)
    BOSS_OUTLINE = (30, 30, 40)
    BOSS_RED = (200, 0, 0)
    BOSS_YELLOW = (255, 255, 0)
    body_points = [ (l + w*0.1, t + h*0.2), (r - w*0.1, t + h*0.2), (r, b - h*0.1), (l, b - h*0.1) ]
    pygame.draw.polygon(surface, BOSS_DARK, body_points)
    pygame.draw.polygon(surface, BOSS_OUTLINE, body_points, 3)
    wing_left = [(l, b - h*0.1), (l - w*0.1, b - h*0.1), (l, b - h*0.4)]
    pygame.draw.polygon(surface, BOSS_LIGHT, wing_left)
    pygame.draw.polygon(surface, BOSS_OUTLINE, wing_left, 2)
    wing_right = [(r, b - h*0.1), (r + w*0.1, b - h*0.1), (r, b - h*0.4)]
    pygame.draw.polygon(surface, BOSS_LIGHT, wing_right)
    pygame.draw.polygon(surface, BOSS_OUTLINE, wing_right, 2)
    cockpit_rect = pygame.Rect(cx - w*0.2, t, w*0.4, h*0.3)
    pygame.draw.rect(surface, BOSS_LIGHT, cockpit_rect)
    pygame.draw.rect(surface, BOSS_OUTLINE, cockpit_rect, 2)
    cockpit_eye = pygame.Rect(cx - w*0.15, t + h*0.05, w*0.3, h*0.2)
    pygame.draw.rect(surface, BOSS_RED, cockpit_eye)
    emitter_rect = pygame.Rect(cx - w*0.1, b - h*0.2, w*0.2, h*0.2)
    pygame.draw.rect(surface, BOSS_RED, emitter_rect, 0, border_radius=4)
    pygame.draw.rect(surface, BOSS_YELLOW, emitter_rect, 2, border_radius=4)


# --- Kelas Sprite: Musuh (Dengan State Machine Bos) ---
class Musuh(pygame.sprite.Sprite):
    def __init__(self, width, height, speed, enemy_type="UFO", 
                 all_sprites_group=None, enemy_bullet_group=None, enemy_laser_group=None):
        super().__init__()
        self.enemy_type = enemy_type
        
        self.all_sprites_group = all_sprites_group
        self.enemy_bullet_group = enemy_bullet_group
        self.enemy_laser_group = enemy_laser_group

        # Periksa jenis musuh untuk menentukan gambar/bentuk dan ukuran
        if self.enemy_type == "LASER":
            if LASER_BOSS_IMAGE:
                self.image = LASER_BOSS_IMAGE.copy()
                self.rect = self.image.get_rect()
            else:
                self.image = pygame.Surface((width, height), pygame.SRCALPHA)
                draw_boss_laser_ship_default(self.image, self.image.get_rect())
                self.rect = self.image.get_rect()

            self.speed_y = speed
            self.speed_x = 4
            self.state = "ENTERING"
            self.target_y = 100
            self.target_x = random.randint(100, SCREEN_WIDTH - 100)
            self.laser_active = False
            self.laser_timer = 0
            self.laser_duration = 2 * FPS
            self.laser_sprite = None
            
        elif self.enemy_type == "SHOOTER":
            if SHOOTER_IMAGE:
                self.image = SHOOTER_IMAGE.copy()
                self.rect = self.image.get_rect()
            else:
                self.image = pygame.Surface((width, height), pygame.SRCALPHA)
                draw_shooter_enemy_default(self.image, self.image.get_rect())
                self.rect = self.image.get_rect()

            self.speed_y = 3
            self.shoot_delay = 80
            self.shoot_timer = random.randrange(0, self.shoot_delay) 

        else: # "UFO" (Musuh Lvl 1)
            if UFO_IMAGE:
                self.image = UFO_IMAGE.copy()
                self.rect = self.image.get_rect()
            else:
                self.image = pygame.Surface((width, height), pygame.SRCALPHA)
                draw_enemy_ufo(self.image, self.image.get_rect())
                self.rect = self.image.get_rect()
            
            self.speed_y = speed

        if self.enemy_type != "LASER":
            self.rect.y = random.randrange(-100, -40)
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        else:
            self.rect.bottom = 0
            self.rect.centerx = SCREEN_WIDTH // 2

    def activate_laser(self):
        if self.laser_active or self.enemy_laser_group is None or self.all_sprites_group is None:
            return
        self.laser_active = True
        self.laser_timer = self.laser_duration
        self.laser_sprite = MusuhLaser(self.rect)
        self.all_sprites_group.add(self.laser_sprite)
        self.enemy_laser_group.add(self.laser_sprite)
        suara_tembak_musuh.play()

    def deactivate_laser(self):
        self.laser_active = False
        if self.laser_sprite:
            self.laser_sprite.kill()
            self.laser_sprite = None
        suara_laser.stop()

    def update(self):
        if self.enemy_type == "UFO":
            self.rect.y += self.speed_y
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()

        elif self.enemy_type == "SHOOTER":
            self.rect.y += self.speed_y
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_delay:
                self.shoot_timer = 0
                if self.all_sprites_group is not None and self.enemy_bullet_group is not None:
                    self.shoot()

        elif self.enemy_type == "LASER":
            if self.state == "ENTERING":
                if self.rect.top < self.target_y: self.rect.y += self.speed_y
                else: self.rect.top = self.target_y
                
                if abs(self.rect.centerx - self.target_x) > self.speed_x:
                    if self.rect.centerx < self.target_x: self.rect.x += self.speed_x
                    else: self.rect.x -= self.speed_x
                else: self.rect.centerx = self.target_x
                
                if self.rect.top == self.target_y and self.rect.centerx == self.target_x:
                    self.state = "FIRING_1"
                    self.activate_laser()

            elif self.state == "FIRING_1":
                if self.laser_sprite: self.laser_sprite.update(self.rect)
                self.laser_timer -= 1
                if self.laser_timer <= 0:
                    self.deactivate_laser()
                    self.state = "MOVING"
                    self.target_x = random.randint(100, SCREEN_WIDTH - 100)

            elif self.state == "MOVING":
                if abs(self.rect.centerx - self.target_x) > self.speed_x:
                    if self.rect.centerx < self.target_x: self.rect.x += self.speed_x
                    else: self.rect.x -= self.speed_x
                else:
                    self.rect.centerx = self.target_x
                    self.state = "FIRING_2"
                    self.activate_laser()

            elif self.state == "FIRING_2":
                if self.laser_sprite: self.laser_sprite.update(self.rect)
                self.laser_timer -= 1
                if self.laser_timer <= 0:
                    self.deactivate_laser()
                    self.state = "EXITING"

            elif self.state == "EXITING":
                self.rect.y -= self.speed_y
                if self.rect.bottom < 0:
                    self.kill()

    def shoot(self):
        peluru = PeluruMusuh(self.rect.centerx, self.rect.bottom)
        self.all_sprites_group.add(peluru)
        self.enemy_bullet_group.add(peluru)
        suara_tembak_musuh.play()

    def kill(self):
        if self.enemy_type == "LASER":
            self.deactivate_laser()
        super().kill()


# --- Kelas Sprite: Player (tetap sama) ---
class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        if PLAYER_IMAGE:
            self.image = PLAYER_IMAGE.copy()
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            draw_player_spaceship_default(self.image, self.image.get_rect())

        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 2 * FPS
        self.speed_multiplier = 1.0
        self.trishot_active = False
        self.trishot_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        self.fire_delay = 15
        self.last_shot_time = 0
        self.laser_active = False
        self.laser_timer = 0
        self.laser_duration = 5 * FPS
        self.laser_sprite = None
        self.speed_indicator_timer = 0
        self.speed_powerup_collected = False

    def update_timers(self):
        if self.trishot_active:
            self.trishot_timer -= 1
            if self.trishot_timer <= 0: self.trishot_active = False
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0: self.shield_active = False
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0: self.invincible = False
        if self.laser_active:
            self.laser_timer -= 1
            if self.laser_timer <= 0:
                self.laser_active = False
                suara_laser.stop()
                if self.laser_sprite:
                    self.laser_sprite.kill()
                    self.laser_sprite = None
            elif self.laser_sprite:
                self.laser_sprite.update(self.rect)
        if self.speed_indicator_timer > 0:
            self.speed_indicator_timer -= 1

    def can_shoot(self, current_frame):
        if self.laser_active: return False
        return current_frame - self.last_shot_time > self.fire_delay

    def shoot(self, current_frame, grup_peluru, grup_semua):
        self.last_shot_time = current_frame
        suara_tembak.play()
        bullet_speed = -6 * self.speed_multiplier
        if self.trishot_active:
            peluru1 = Peluru(self.rect.centerx, self.rect.top, bullet_speed)
            peluru2 = Peluru(self.rect.left + self.rect.width * 0.15, self.rect.centery + self.rect.height * 0.1, bullet_speed)
            peluru3 = Peluru(self.rect.right - self.rect.width * 0.15, self.rect.centery + self.rect.height * 0.1, bullet_speed)
            grup_peluru.add(peluru1, peluru2, peluru3)
            grup_semua.add(peluru1, peluru2, peluru3)
        else:
            peluru = Peluru(self.rect.centerx, self.rect.top, bullet_speed)
            grup_peluru.add(peluru)
            grup_semua.add(peluru)

    def activate_trishot(self):
        self.trishot_active = True
        self.trishot_timer = 5 * FPS
        suara_powerup.play()

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = 5 * FPS
        suara_shield.play()

    def activate_speedup(self):
        self.speed_multiplier += 0.5
        self.speed_indicator_timer = 2 * FPS
        suara_powerup.play()
        self.speed_powerup_collected = True
        
    def add_life(self):
        if self.lives < 3:
            self.lives += 1
            suara_powerup.play()

    def activate_invincibility(self):
        self.invincible = True
        self.invincible_timer = self.invincible_duration

    def activate_laser(self, all_sprites_group, laser_group):
        if self.laser_active: return
        self.laser_active = True
        self.laser_timer = self.laser_duration
        self.laser_sprite = PlayerLaser(self.rect)
        all_sprites_group.add(self.laser_sprite)
        laser_group.add(self.laser_sprite)
        suara_laser.play(loops=-1)


# --- Kelas Sprite: Peluru, PeluruMusuh, Powerup, Shockwave, PlayerLaser, MusuhLaser (tetap sama) ---

class Peluru(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = speed_y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0: self.kill()


# --- Kelas Sprite: Peluru Musuh ---
class PeluruMusuh(pygame.sprite.Sprite):
    def __init__(self, center_x, bottom_y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.top = bottom_y
        self.speed_y = 8

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT: self.kill()


# --- Kelas Sprite: Powerup ---
class Powerup(pygame.sprite.Sprite):
    def __init__(self, tipe):
        super().__init__()
        self.type = tipe
        self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        center = (self.rect.width // 2, self.rect.height // 2)
        radius_luar = 16
        radius_dalam = 10
        rotasi_segidelapan = math.pi / 8
        if self.type == 'P': color, text, text_color = POWERUP_BLUE, "P", WHITE
        elif self.type == 'T': color, text, text_color = POWERUP_ORANGE, "T", WHITE
        elif self.type == 'S': color, text, text_color = POWERUP_RED, "S", WHITE
        elif self.type == 'K': color, text, text_color = POWERUP_GREEN, "K", WHITE
        elif self.type == 'L': color, text, text_color = POWERUP_PINK, "L", POWERUP_PINK
        draw_regular_polygon(self.image, color, center, radius_luar, 8, rotasi_segidelapan)
        draw_regular_polygon(self.image, WHITE, center, radius_luar, 8, rotasi_segidelapan, width=2)
        draw_regular_polygon(self.image, WHITE, center, radius_dalam, 8, rotasi_segidelapan, width=1)
        if self.type == 'L':
            cross_width, cross_height, arm_thickness = 20, 20, 6
            horiz_y, horiz_x = center[1] - (arm_thickness // 2), center[0] - (cross_width // 2)
            pygame.draw.rect(self.image, WHITE, (horiz_x, horiz_y, cross_width, arm_thickness))
            vert_x, vert_y = center[0] - (arm_thickness // 2), center[1] - (cross_height // 2)
            pygame.draw.rect(self.image, WHITE, (vert_x, vert_y, arm_thickness, cross_height))
        else:
            text_surf = font_powerup.render(text, True, text_color)
            text_rect = text_surf.get_rect(center=center)
            self.image.blit(text_surf, text_rect)
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = 2

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT: self.kill()


# --- Kelas Sprite: Shockwave ---
class Shockwave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, 25))
        self.image.fill(WHITE)
        self.image.set_alpha(180)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCREEN_HEIGHT
        self.speed_y = -15

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0: self.kill()


# --- Kelas Sprite: Laser Spesial Player ---
class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.height = player_rect.top
        self.image = pygame.Surface((20, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.midbottom = player_rect.midtop
        self.draw_laser()

    def draw_laser(self):
        self.image.fill((0, 0, 0, 0))
        aura_width = random.randint(18, 22)
        aura_rect = pygame.Rect((self.image.get_width() - aura_width) // 2, 0, aura_width, self.height)
        pygame.draw.rect(self.image, POWERUP_BLUE, aura_rect, 0, border_radius=4)
        core_width = 8
        core_rect = pygame.Rect((self.image.get_width() - core_width) // 2, 0, core_width, self.height)
        pygame.draw.rect(self.image, WHITE, core_rect, 0, border_radius=2)

    def update(self, player_rect=None):
        if player_rect is not None:
            self.height = player_rect.top
            self.image = pygame.Surface((20, self.height), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.midbottom = player_rect.midtop
            self.draw_laser()


# --- Kelas Sprite: Laser Musuh ---
class MusuhLaser(pygame.sprite.Sprite):
    def __init__(self, enemy_rect):
        super().__init__()
        self.height = SCREEN_HEIGHT - enemy_rect.bottom
        if self.height < 0: self.height = 0
        self.image = pygame.Surface((15, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.midtop = enemy_rect.midbottom
        self.draw_laser()

    def draw_laser(self):
        self.image.fill((0, 0, 0, 0))
        aura_width = random.randint(12, 17)
        aura_rect = pygame.Rect((self.image.get_width() - aura_width) // 2, 0, aura_width, self.height)
        pygame.draw.rect(self.image, ALIEN_GUN_RED, aura_rect, 0, border_radius=4)
        core_width = 6
        core_rect = pygame.Rect((self.image.get_width() - core_width) // 2, 0, core_width, self.height)
        pygame.draw.rect(self.image, (255, 200, 200), core_rect, 0, border_radius=2)

    def update(self, enemy_rect=None):
        if enemy_rect is not None:
            self.height = SCREEN_HEIGHT - enemy_rect.bottom
            if self.height < 0: self.height = 0
            self.image = pygame.Surface((15, self.height), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.midtop = enemy_rect.midbottom
            self.draw_laser()
        if enemy_rect is None or self.height <= 0:
            self.kill()


# --- Fungsi menggambar player default (tetap sama) ---
def draw_player_spaceship_default(surface, rect):
    cx, cy = rect.centerx, rect.centery
    w, h = rect.width, rect.height
    l, r, t, b = rect.left, rect.right, rect.top, rect.bottom
    body_points = [ (cx, t), (cx + (w*0.08), t + (h*0.1)), (cx + (w*0.15), t + (h*0.3)), (cx + (w*0.15), b - (h*0.2)), (cx + (w*0.07), b - (h*0.05)), (cx - (w*0.07), b - (h*0.05)), (cx - (w*0.15), b - (h*0.2)), (cx - (w*0.15), t + (h*0.3)), (cx - (w*0.08), t + (h*0.1)) ]
    pygame.draw.polygon(surface, COLOR_JET_BODY, body_points)
    pygame.draw.polygon(surface, COLOR_JET_OUTLINE, body_points, 2)
    wing_left_points = [ (cx - (w*0.12), t + (h*0.3)), (l - (w*0.1), t + (h*0.6)), (l - (w*0.05), b - (h*0.25)), (cx - (w*0.12), b - (h*0.25)) ]
    pygame.draw.polygon(surface, COLOR_JET_WING, wing_left_points)
    pygame.draw.polygon(surface, COLOR_JET_OUTLINE, wing_left_points, 2)
    wing_right_points = [ (cx + (w*0.12), t + (h*0.3)), (r + (w*0.1), t + (h*0.6)), (r + (w*0.05), b - (h*0.25)), (cx + (w*0.12), b - (h*0.25)) ]
    pygame.draw.polygon(surface, COLOR_JET_WING, wing_right_points)
    pygame.draw.polygon(surface, COLOR_JET_OUTLINE, wing_right_points, 2)
    y_attach_front = b - (h*0.35); y_attach_back = b - (h*0.23)
    x_attach = cx - (w*0.15); x_tip = cx - (w*0.30)
    tail_left_points = [ (x_attach, y_attach_front), (x_tip, y_attach_front), (x_tip, y_attach_back), (x_attach, y_attach_back) ]
    pygame.draw.polygon(surface, COLOR_JET_WING, tail_left_points)
    pygame.draw.polygon(surface, COLOR_JET_OUTLINE, tail_left_points, 2)
    x_attach_r = cx + (w*0.15); x_tip_r = cx + (w*0.30)
    tail_right_points = [ (x_attach_r, y_attach_front), (x_tip_r, y_attach_front), (x_tip_r, y_attach_back), (x_attach_r, y_attach_back) ]
    pygame.draw.polygon(surface, COLOR_JET_WING, tail_right_points)
    pygame.draw.polygon(surface, COLOR_JET_OUTLINE, tail_right_points, 2)
    pod_left_rect = pygame.Rect(cx - (w*0.38), t + (h*0.45), w*0.15, h*0.3)
    pygame.draw.rect(surface, COLOR_ENGINE_POD, pod_left_rect)
    pygame.draw.rect(surface, COLOR_JET_OUTLINE, pod_left_rect, 2)
    pod_right_rect = pygame.Rect(cx + (w*0.23), t + (h*0.45), w*0.15, h*0.3)
    pygame.draw.rect(surface, COLOR_ENGINE_POD, pod_right_rect)
    pygame.draw.rect(surface, COLOR_JET_OUTLINE, pod_right_rect, 2)
    fin_top = t + (h*0.05); fin_bottom = b - (h*0.10)
    fin_points = [ (cx - (w*0.05), fin_top), (cx + (w*0.05), fin_top), (cx + (w*0.08), fin_bottom), (cx - (w*0.08), fin_bottom) ]
    pygame.draw.polygon(surface, COLOR_JET_WING, fin_points)
    pygame.draw.polygon(surface, COLOR_JET_OUTLINE, fin_points, 2)
    cockpit_width = w * 0.25
    cockpit_height = h * 0.35
    cockpit_top_y = t + h*0.05
    cockpit_bottom_y = cockpit_top_y + cockpit_height
    cockpit_left_x = cx - cockpit_width/2
    cockpit_right_x = cx + cockpit_width/2
    cockpit_points = [ (cx - w*0.08, cockpit_top_y), (cx + w*0.08, cockpit_top_y), (cockpit_right_x, cockpit_top_y + h*0.15), (cockpit_right_x, cockpit_bottom_y), (cockpit_left_x, cockpit_bottom_y), (cockpit_left_x, cockpit_top_y + h*0.15) ]
    pygame.draw.polygon(surface, COLOR_COCKPIT_BLUE, cockpit_points)
    pygame.draw.polygon(surface, COLOR_JET_OUTLINE, cockpit_points, 2)
    shine_rect = pygame.Rect(cx - cockpit_width*0.25, cockpit_top_y + h*0.05, cockpit_width * 0.5, cockpit_height * 0.3)
    pygame.draw.ellipse(surface, COLOR_COCKPIT_HIGHLIGHT, shine_rect)


# --- Fungsi untuk menggambar Hati (tetap sama) ---
def draw_player_heart(surface, x, y, size):
    p1 = (x + size // 2, y + size)
    p2 = (x, y + size // 3)
    p3 = (x + size // 4, y)
    p4 = (x + size // 2, y + size // 4)
    p5 = (x + 3 * size // 4, y)
    p6 = (x + size, y + size // 3)
    heart_points = [p1, p2, p3, p4, p5, p6]
    pygame.draw.polygon(surface, RED, heart_points)
    pygame.draw.polygon(surface, WHITE, heart_points, 1)


# --- run_game ---
def run_game(screen, clock, high_score):
    PLAYER_WIDTH = PLAYER_IMAGE_SIZE[0]
    PLAYER_HEIGHT = PLAYER_IMAGE_SIZE[1]
    player_speed = 10
    PLAYER_TOP_BOUNDARY = SCREEN_HEIGHT * 0.4

    player = Player(PLAYER_WIDTH, PLAYER_HEIGHT)
    player.rect.centerx = SCREEN_WIDTH // 2
    player.rect.bottom = SCREEN_HEIGHT - 10

    semua_sprite = pygame.sprite.Group()
    grup_peluru_pemain = pygame.sprite.Group()
    grup_powerup = pygame.sprite.Group()
    grup_shockwave = pygame.sprite.Group()
    grup_musuh = pygame.sprite.Group()
    grup_peluru_musuh = pygame.sprite.Group()
    grup_laser_pemain = pygame.sprite.Group()
    grup_laser_musuh = pygame.sprite.Group()

    semua_sprite.add(player)

    # Menggunakan ukuran dari gambar yang dimuat, jika ada
    UFO_ENEMY_WIDTH = UFO_IMAGE_SIZE[0] if UFO_IMAGE else 60
    UFO_ENEMY_HEIGHT = UFO_IMAGE_SIZE[1] if UFO_IMAGE else 40
    SHOOTER_ENEMY_WIDTH = SHOOTER_IMAGE_SIZE[0] if SHOOTER_IMAGE else 140
    SHOOTER_ENEMY_HEIGHT = SHOOTER_IMAGE_SIZE[1] if SHOOTER_IMAGE else 85
    LASER_ENEMY_WIDTH = LASER_BOSS_IMAGE_SIZE[0] if LASER_BOSS_IMAGE else 120
    LASER_ENEMY_HEIGHT = LASER_BOSS_IMAGE_SIZE[1] if LASER_BOSS_IMAGE else 100

    base_enemy_speed = 4
    max_ufo_enemies = 4
    
    next_boss_spawn_score = 1000
    boss_spawn_interval = 300

    for _ in range(max_ufo_enemies):
        musuh = Musuh(UFO_ENEMY_WIDTH, UFO_ENEMY_HEIGHT, base_enemy_speed, enemy_type="UFO")
        for _ in range(10):
            musuh.rect.x = random.randrange(SCREEN_WIDTH - musuh.rect.width)
            collides = False
            for existing_enemy in grup_musuh:
                spawn_box = musuh.rect.inflate(UFO_ENEMY_WIDTH, 0)
                if spawn_box.colliderect(existing_enemy.rect):
                    collides = True; break
            if not collides: break
        grup_musuh.add(musuh); semua_sprite.add(musuh)

    score = 0
    frame_count = 0
    level = 1

    special_meter_count = 0
    SPECIAL_METER_MAX = 25

    powerup_spawn_timer = 0
    POWERUP_SPAWN_RATE = 10 * FPS

    game_running = True
    while game_running:

        clock.tick(FPS)
        frame_count += 1
        if frame_count % 12 == 0: score += 1
        level = 1 + (score // 500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit", score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.can_shoot(frame_count):
                        player.shoot(frame_count, grup_peluru_pemain, semua_sprite)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.rect.left > 0: player.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player.rect.right < SCREEN_WIDTH: player.rect.x += player_speed
        if keys[pygame.K_UP] and player.rect.top > PLAYER_TOP_BOUNDARY: player.rect.y -= player_speed
        if keys[pygame.K_DOWN] and player.rect.bottom < SCREEN_HEIGHT: player.rect.y += player_speed

        semua_sprite.update()
        player.update_timers()

        # === [PERBAIKAN KESULITAN DITERAPKAN DI SINI] ===
        
        # Opsi 1: Peningkatan kecepatan lebih lambat
        current_enemy_speed = base_enemy_speed + (level - 1) * 0.5
        
        # Opsi 2: Jumlah musuh bertambah setiap 2 level
        max_ufo_enemies = 4 + (level - 1) // 2
        max_shooter_enemies = 0
        if level >= 2:
            max_shooter_enemies = 1 + (level - 2) // 2
        # === [AKHIR PERBAIKAN] ===

        powerup_spawn_timer += 1
        if powerup_spawn_timer >= POWERUP_SPAWN_RATE:
            powerup_spawn_timer = 0
            tipe = random.choice(['T', 'P', 'S', 'K', 'L'])
            new_powerup = Powerup(tipe)
            grup_powerup.add(new_powerup)
            semua_sprite.add(new_powerup)

        # --- Cek Tabrakan ---
        tabrakan_peluru_musuh = pygame.sprite.groupcollide(grup_peluru_pemain, grup_musuh, True, True)
        for list_musuh_terkena in tabrakan_peluru_musuh.values():
            for musuh_yang_terkena in list_musuh_terkena:
                if musuh_yang_terkena.enemy_type == "LASER": score += 100
                elif musuh_yang_terkena.enemy_type == "SHOOTER": score += 30
                else: score += 10
                suara_ledakan.play()
                if not player.laser_active: special_meter_count += 1

        tabrakan_player_powerup = pygame.sprite.spritecollide(player, grup_powerup, True)
        for powerup in tabrakan_player_powerup:
            if powerup.type == 'T': player.activate_trishot()
            elif powerup.type == 'P': player.activate_shield()
            elif powerup.type == 'S':
                sw = Shockwave(); semua_sprite.add(sw); grup_shockwave.add(sw); suara_shockwave.play()
            elif powerup.type == 'K': player.activate_speedup()
            elif powerup.type == 'L': player.add_life()

        tabrakan_shockwave_musuh = pygame.sprite.groupcollide(grup_shockwave, grup_musuh, False, True)
        for list_musuh_terkena in tabrakan_shockwave_musuh.values():
            for musuh_yang_terkena in list_musuh_terkena:
                if musuh_yang_terkena.enemy_type == "LASER": score += 50
                elif musuh_yang_terkena.enemy_type == "SHOOTER": score += 15
                else: score += 5
                suara_ledakan.play()
                if not player.laser_active: special_meter_count += 1

        pygame.sprite.groupcollide(grup_shockwave, grup_peluru_musuh, False, True)
        pygame.sprite.groupcollide(grup_laser_pemain, grup_peluru_musuh, False, True)
        pygame.sprite.groupcollide(grup_laser_musuh, grup_peluru_pemain, False, True) 

        tabrakan_laser_musuh = pygame.sprite.groupcollide(grup_laser_pemain, grup_musuh, False, True)
        for list_musuh_terkena in tabrakan_laser_musuh.values():
            for musuh_yang_terkena in list_musuh_terkena:
                if musuh_yang_terkena.enemy_type == "LASER": score += 100
                elif musuh_yang_terkena.enemy_type == "SHOOTER": score += 30
                else: score += 10
                suara_ledakan.play()

        if special_meter_count >= SPECIAL_METER_MAX:
            player.activate_laser(semua_sprite, grup_laser_pemain)
            special_meter_count = 0

        # --- Logika Respawn Musuh ---
        ufo_count = sum(1 for m in grup_musuh if m.enemy_type == "UFO")
        while ufo_count < max_ufo_enemies:
            new_musuh = Musuh(UFO_ENEMY_WIDTH, UFO_ENEMY_HEIGHT, current_enemy_speed, enemy_type="UFO")
            for _ in range(10):
                new_musuh.rect.x = random.randrange(SCREEN_WIDTH - new_musuh.rect.width)
                collides = False
                for existing_enemy in grup_musuh:
                    # Memperluas area pengecekan tabrakan saat spawn agar tidak terlalu padat
                    spawn_box = new_musuh.rect.inflate(UFO_ENEMY_WIDTH, 0)
                    if spawn_box.colliderect(existing_enemy.rect): collides = True; break
                if not collides: break
            grup_musuh.add(new_musuh); semua_sprite.add(new_musuh); ufo_count += 1

        shooter_count = sum(1 for m in grup_musuh if m.enemy_type == "SHOOTER")
        while shooter_count < max_shooter_enemies:
            new_shooter = Musuh(SHOOTER_ENEMY_WIDTH, SHOOTER_ENEMY_HEIGHT, current_enemy_speed, 
                                enemy_type="SHOOTER",
                                all_sprites_group=semua_sprite, 
                                enemy_bullet_group=grup_peluru_musuh)
            for _ in range(10):
                new_shooter.rect.x = random.randrange(SCREEN_WIDTH - new_shooter.rect.width)
                collides = False
                for existing_enemy in grup_musuh:
                    spawn_box = new_shooter.rect.inflate(SHOOTER_ENEMY_WIDTH, 0)
                    if spawn_box.colliderect(existing_enemy.rect): collides = True; break
                if not collides: break
            grup_musuh.add(new_shooter); semua_sprite.add(new_shooter); shooter_count += 1
            
        laser_count = sum(1 for m in grup_musuh if m.enemy_type == "LASER")
        if score >= next_boss_spawn_score and laser_count == 0:
            next_boss_spawn_score = score + boss_spawn_interval
            w, h = LASER_ENEMY_WIDTH, LASER_ENEMY_HEIGHT
            new_laser_enemy = Musuh(w, h, 5,
                                    enemy_type="LASER",
                                    all_sprites_group=semua_sprite,
                                    enemy_laser_group=grup_laser_musuh) 
            grup_musuh.add(new_laser_enemy); semua_sprite.add(new_laser_enemy)

        # --- Cek Tabrakan Player (Logika Nyawa) ---
        if not player.shield_active and not player.invincible:
            tabrakan_player_musuh = pygame.sprite.spritecollide(player, grup_musuh, True)
            tabrakan_player_peluru_musuh = pygame.sprite.spritecollide(player, grup_peluru_musuh, True)
            tabrakan_player_laser_musuh = pygame.sprite.spritecollide(player, grup_laser_musuh, False) 
            if tabrakan_player_musuh or tabrakan_player_peluru_musuh or tabrakan_player_laser_musuh:
                suara_player_terkena.play()
                player.lives -= 1
                player.activate_invincibility()
                # Hapus semua musuh non-bos
                for musuh in grup_musuh:
                    if musuh.enemy_type != "LASER": musuh.kill() 
                if player.lives <= 0:
                    if player.laser_active: suara_laser.stop()
                    print(f"Game Over! Skor Akhir: {score}")
                    return "game_over", score

        # --- 4. Render Game ---
        screen.fill(BLACK)
        
        # Render semua sprite kecuali musuh yang menggunakan gambar yang dimuat
        for sprite in semua_sprite:
            if isinstance(sprite, Musuh) and (
                (sprite.enemy_type == "UFO" and UFO_IMAGE) or
                (sprite.enemy_type == "SHOOTER" and SHOOTER_IMAGE) or
                (sprite.enemy_type == "LASER" and LASER_BOSS_IMAGE)
            ):
                continue
            screen.blit(sprite.image, sprite.rect)

        # Render musuh yang menggunakan gambar yang dimuat
        for musuh in grup_musuh:
            if musuh.enemy_type == "UFO" and UFO_IMAGE:
                screen.blit(musuh.image, musuh.rect)
            elif musuh.enemy_type == "SHOOTER" and SHOOTER_IMAGE:
                screen.blit(musuh.image, musuh.rect)
            elif musuh.enemy_type == "LASER" and LASER_BOSS_IMAGE:
                 screen.blit(musuh.image, musuh.rect)


        if PLAYER_IMAGE:
            if player.invincible and frame_count % 10 < 5: pass
            else: screen.blit(player.image, player.rect)
        else: 
            if player.invincible and frame_count % 10 < 5: pass
            else: screen.blit(player.image, player.rect) 

        if player.shield_active:
            pygame.draw.circle(screen, POWERUP_BLUE, player.rect.center, player.rect.width // 2 + 10, 3)

        # --- UI (User Interface) ---
        ui_padding = 10
        bar_height = 15
        bar_length = 150
        
        score_text = font.render(f"Skor: {score}", True, WHITE)
        screen.blit(score_text, (ui_padding, ui_padding))
        
        ui_y_pos_kiri = score_text.get_height() + ui_padding + 5
        fill_percent = special_meter_count / SPECIAL_METER_MAX
        if player.laser_active: fill_percent = player.laser_timer / player.laser_duration
        fill_length = fill_percent * bar_length
        outline_rect = pygame.Rect(ui_padding, ui_y_pos_kiri, bar_length, bar_height)
        pygame.draw.rect(screen, (50, 50, 50), outline_rect)
        if player.laser_active:
             pygame.draw.rect(screen, POWERUP_PINK, (ui_padding, ui_y_pos_kiri, fill_length, bar_height))
        else:
             pygame.draw.rect(screen, POWERUP_BLUE, (ui_padding, ui_y_pos_kiri, fill_length, bar_height))
        pygame.draw.rect(screen, WHITE, outline_rect, 2)
        
        hiscore_text = font_ui.render(f"Hi-Score: {high_score}", True, WHITE)
        hiscore_rect = hiscore_text.get_rect(center=(SCREEN_WIDTH // 2, ui_padding + hiscore_text.get_height() // 2))
        screen.blit(hiscore_text, hiscore_rect)
        
        level_text = font_ui.render(f"Level: {level}", True, WHITE)
        level_rect = level_text.get_rect(topright=(SCREEN_WIDTH - ui_padding, ui_padding))
        screen.blit(level_text, level_rect)
        
        heart_size = 25
        heart_y_pos = level_rect.bottom + ui_padding // 2
        for i in range(player.lives):
            heart_x_pos = (SCREEN_WIDTH - ui_padding - heart_size) - (i * (heart_size + 5))
            draw_player_heart(screen, heart_x_pos, heart_y_pos, heart_size)
        
        ui_y_pos_kanan = heart_y_pos + heart_size + (ui_padding // 2)
        
        if player.speed_powerup_collected:
            speed_val_text = f"Power: {player.speed_multiplier:.1f}x"
            speed_text_surf = font_ui.render(speed_val_text, True, POWERUP_GREEN)
            speed_rect = speed_text_surf.get_rect(topright=(SCREEN_WIDTH - ui_padding, ui_y_pos_kanan))
            screen.blit(speed_text_surf, speed_rect)
            ui_y_pos_kanan += speed_rect.height + 5
            
        if player.trishot_active:
            timer_text = font_ui.render(f"Trishot: {player.trishot_timer // FPS + 1}s", True, POWERUP_ORANGE)
            timer_rect = timer_text.get_rect(topright=(SCREEN_WIDTH - ui_padding, ui_y_pos_kanan))
            screen.blit(timer_text, timer_rect)
            ui_y_pos_kanan += timer_rect.height + 5
            
        if player.shield_active:
            timer_text = font_ui.render(f"Shield: {player.shield_timer // FPS + 1}s", True, POWERUP_BLUE)
            timer_rect = timer_text.get_rect(topright=(SCREEN_WIDTH - ui_padding, ui_y_pos_kanan))
            screen.blit(timer_text, timer_rect)
            ui_y_pos_kanan += timer_rect.height + 5
            
        if player.laser_active:
            timer_text = font_ui.render(f"LASER: {player.laser_timer // FPS + 1}s", True, POWERUP_PINK)
            timer_rect = timer_text.get_rect(topright=(SCREEN_WIDTH - ui_padding, ui_y_pos_kanan))
            screen.blit(timer_text, timer_rect)
            ui_y_pos_kanan += timer_rect.height + 5

        if player.speed_indicator_timer > 0:
            speed_text_overlay = font_indicator.render("SPEED UP!", True, POWERUP_GREEN)
            speed_overlay_rect = speed_text_overlay.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(speed_text_overlay, speed_overlay_rect)

        pygame.display.flip()
    
    return "quit", score


# --- Fungsi Tampilan Start/Game Over (tetap sama) ---
def show_start_screen(screen, high_score):
    screen.fill(BLACK)
    title_font = pygame.font.SysFont(None, 80)
    text_font = pygame.font.SysFont(None, 40)
    title_surf = title_font.render("SPACE SHOOTER", True, WHITE)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    hiscore_surf = text_font.render(f"High Score: {high_score}", True, WHITE)
    hiscore_rect = hiscore_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    prompt_surf = text_font.render("Tekan [ENTER] untuk Mulai", True, WHITE)
    prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(title_surf, title_rect)
    screen.blit(hiscore_surf, hiscore_rect)
    screen.blit(prompt_surf, prompt_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    waiting = False

def show_game_over_screen(screen, score, high_score):
    screen.fill(BLACK)
    title_font = pygame.font.SysFont(None, 80)
    text_font = pygame.font.SysFont(None, 40)
    title_surf = title_font.render("GAME OVER", True, RED)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    score_surf = text_font.render(f"Skor Anda: {score}", True, WHITE)
    score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    if score > high_score:
        new_hi_surf = text_font.render("NEW HIGH SCORE!", True, POWERUP_GREEN)
        new_hi_rect = new_hi_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(new_hi_surf, new_hi_rect)
    else:
        hiscore_surf = text_font.render(f"High Score: {high_score}", True, WHITE)
        hiscore_rect = hiscore_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(hiscore_surf, hiscore_rect)
    prompt_surf = text_font.render("Tekan [ENTER] untuk Main Lagi", True, WHITE)
    prompt_rect = prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    screen.blit(title_surf, title_rect)
    screen.blit(score_surf, score_rect)
    screen.blit(prompt_surf, prompt_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "quit"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN: return "restart"


# --- Fungsi Main (Loop Utama Aplikasi) ---
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Shooter")
    clock = pygame.time.Clock()
    high_score = load_high_score()
    game_state = "start"
    running = True
    final_score = 0
    while running:
        if game_state == "start":
            show_start_screen(screen, high_score)
            game_state = "playing"
        elif game_state == "playing":
            game_result, final_score = run_game(screen, clock, high_score)
            if final_score > high_score:
                high_score = final_score
                save_high_score(high_score)
            if game_result == "quit": running = False
            elif game_result == "game_over": game_state = "game_over"
        elif game_state == "game_over":
            next_action = show_game_over_screen(screen, final_score, high_score)
            if next_action == "quit": running = False
            elif next_action == "restart": game_state = "playing"
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()