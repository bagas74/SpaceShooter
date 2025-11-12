# --- Variabel Lokal untuk Game --- (BARIS 9)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN_ENEMY = (0, 200, 50)
GREEN_TOSCA = (0, 204, 153)
GREEN = (0, 150, 0)
FPS = 60  # Dibutuhkan untuk timer
PLAYER_STARTING_LIVES = 3
PLAYER_INVINCIBILITY_DURATION = 7 * FPS
STAGE_CLEAR_DURATION = 6
# Pengaturan Banner Notifikasi Stage
BANNER_HEIGHT = 100  # Tinggi banner dalam piksel
BANNER_SPEED = 10    # Kecepatan banner bergerak (piksel per frame)
BANNER_STAY_TIME = 2 * FPS # Waktu banner diam di layar (2 detik)

# --- Warna-warna detail (Pesawat Dicerahkan) --- (BARIS 17)
COLOR_JET_BODY = (180, 190, 200)
COLOR_JET_OUTLINE = (40, 50, 60)
COLOR_JET_WING = (140, 150, 165)
COLOR_COCKPIT_BLUE = (0, 150, 255)
COLOR_COCKPIT_HIGHLIGHT = (200, 230, 255) # Diubah untuk kilauan oval
COLOR_ENGINE_POD = (100, 100, 100)
COLOR_RED_ACCENT = (200, 0, 0)
COLOR_STAR_RED = (200, 0, 0)

# Warna UFO Default (BARIS 27)
UFO_GREY_LIGHT = (180, 180, 180)
UFO_GREY_DARK = (100, 100, 100)
UFO_BLUE_DOME = (100, 200, 255)
UFO_BLUE_DOME_HIGHLIGHT = (200, 240, 255)
UFO_YELLOW_LIGHT = (255, 255, 0)
UFO_RED_FEET = (200, 0, 0)
UFO_OUTLINE = (50, 50, 50)

# Warna Musuh Alien Baru (New Enemy Default) (BARIS 36)
ALIEN_BODY_DARK = (80, 0, 120)  # Ungu gelap
ALIEN_BODY_LIGHT = (120, 0, 180) # Ungu terang
ALIEN_ACCENT_GREEN = (0, 255, 150) # Hijau neon
ALIEN_OUTLINE = (30, 0, 40) # Ungu hampir hitam
ALIEN_GUN_RED = (255, 50, 50) # Merah senjata
ALIEN_EYE_YELLOW = (255, 255, 0) # Mata kuning

# --- Warna Powerup --- (BARIS 44)
POWERUP_BLUE = (0, 191, 255)
POWERUP_ORANGE = (255, 165, 0)
POWERUP_RED = (200, 0, 0) 
POWERUP_GREEN = (0, 255, 0) # Hijau Biasa untuk speed
POWERUP_YELLOW_LIGHT = (255, 255, 200)
POWERUP_YELLOW_DARK = (204, 204, 0)

SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 600 

# --- Muat gambar musuh baru --- (BARIS 92)
ENEMY_IMAGE_PATH = "enemy_ship.png"
ENEMY_IMAGE_SIZE = (70, 70) 

# Muat Gambar Player (BARIS 107)
PLAYER_IMAGE_PATH = "player_ship.png" 
PLAYER_IMAGE_SIZE = (70, 75) # (Lebar, Tinggi)

# ... di dalam run_game, sekitar baris 578 ...
SPECIAL_METER_MAX = 25

# ... di dalam run_game, sekitar baris 581 ...
POWERUP_SPAWN_RATE = 10 * FPS