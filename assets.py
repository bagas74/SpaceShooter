import pygame
import os
import settings as s

# Inisialisasi modul pygame yang diperlukan untuk memuat aset
pygame.mixer.init()
pygame.font.init()

# --- Tentukan Path Folder Aset ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_FOLDER = os.path.join(BASE_DIR, 'assets', 'sound-effect')
IMAGE_FOLDER = os.path.join(BASE_DIR, 'assets', 'images')
MUSIC_FOLDER = os.path.join(BASE_DIR, 'assets', 'music')


# --- [PERBAIKAN] Definisikan jalur file musik ---
# Kita gunakan variabel MUSIC_FOLDER yang sudah Anda buat di atas
MUSIC_MENU = os.path.join(MUSIC_FOLDER, 'menu_music.mp3') 
MUSIC_GAME = os.path.join(MUSIC_FOLDER, 'game_music.mp3') 

# --- Font ---
font = pygame.font.SysFont(None, 55)
font_powerup = pygame.font.SysFont('arial', 22, bold=True) 
font_ui = pygame.font.SysFont('arial', 24)
font_indicator = pygame.font.SysFont('arial', 36, bold=True) 
title_font = pygame.font.SysFont(None, 100) 
button_font = pygame.font.SysFont(None, 45) 
score_font = pygame.font.SysFont(None, 60) 
menu_title_font = pygame.font.SysFont(None, 80) 
menu_button_font = pygame.font.SysFont(None, 50) 
stage_clear_font = pygame.font.SysFont('arial', 100, bold=True)

# --- Coba muat file suara ---
class NoSound:
    def play(self, *args, **kwargs): pass
    def stop(self): pass

# Fungsi helper untuk memuat suara
def load_sound(filename):
    # [PERBAIKAN] Menggunakan variabel SOUND_FOLDER yang sudah benar
    path = os.path.join(SOUND_FOLDER, filename) 
    if not os.path.exists(path):
        print(f"Peringatan: File suara '{filename}' tidak ditemukan di '{SOUND_FOLDER}'.")
        return NoSound()
    try:
        sound = pygame.mixer.Sound(path)
        print(f"Berhasil memuat suara: {filename}") # Pesan sukses
        return sound
    except pygame.error as e:
        print(f"Error memuat suara '{filename}': {e}")
        return NoSound()

# [DIUBAH] Kita sekarang memuat SEMUA suara, bukan hanya laser.wav
suara_tembak = load_sound("laser.wav")
suara_ledakan = load_sound("explosion.wav")
suara_powerup = load_sound("powerup.wav")
suara_shield = load_sound("powerup_shield.wav")
suara_shockwave = load_sound("shockwave.mp3")
suara_tembak_musuh = load_sound("enemy_laser.wav")
suara_laser = load_sound("laser_beam.wav") 
suara_player_hit = load_sound("player_hit.wav") 

# [DIUBAH] Atur volume untuk semua suara yang berhasil dimuat
if isinstance(suara_tembak, pygame.mixer.Sound):
    suara_tembak.set_volume(0.4)
if isinstance(suara_ledakan, pygame.mixer.Sound):
    suara_ledakan.set_volume(0.4)
if isinstance(suara_powerup, pygame.mixer.Sound):
    suara_powerup.set_volume(0.3)
if isinstance(suara_shield, pygame.mixer.Sound):
    suara_shield.set_volume(0.3)
if isinstance(suara_shockwave, pygame.mixer.Sound):
    suara_shockwave.set_volume(0.3)
if isinstance(suara_tembak_musuh, pygame.mixer.Sound):
    suara_tembak_musuh.set_volume(0.1)
if isinstance(suara_laser, pygame.mixer.Sound):
    suara_laser.set_volume(0.5)
if isinstance(suara_player_hit, pygame.mixer.Sound): # [BARU]
    suara_player_hit.set_volume(0.5)

# --- Muat gambar musuh baru ---
ENEMY_IMAGE = None
# [PERBAIKAN] Menggunakan variabel IMAGE_FOLDER yang sudah benar
enemy_image_path = os.path.join(IMAGE_FOLDER, s.ENEMY_IMAGE_PATH) 
if os.path.exists(enemy_image_path):
    try:
        ENEMY_IMAGE = pygame.image.load(enemy_image_path).convert_alpha()
        ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, s.ENEMY_IMAGE_SIZE)
        print(f"Gambar musuh '{enemy_image_path}' berhasil dimuat.")
    except pygame.error as e:
        print(f"Error memuat gambar musuh '{enemy_image_path}': {e}")
        ENEMY_IMAGE = None
else:
    print(f"Peringatan: Gambar musuh '{enemy_image_path}' tidak ditemukan. Menggunakan bentuk default.")

# Muat Gambar Player
PLAYER_IMAGE = None
# [PERBAIKAN] Menggunakan variabel IMAGE_FOLDER yang sudah benar
player_image_path = os.path.join(IMAGE_FOLDER, s.PLAYER_IMAGE_PATH)
if os.path.exists(player_image_path):
    try:
        PLAYER_IMAGE = pygame.image.load(player_image_path).convert_alpha()
        PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, s.PLAYER_IMAGE_SIZE)
        print(f"Gambar player '{player_image_path}' berhasil dimuat.")
    except pygame.error as e:
        print(f"Error memuat gambar player '{player_image_path}': {e}")
        PLAYER_IMAGE = None

# Di dalam assets.py

# ... (setelah kode 'Muat gambar musuh baru' untuk ENEMY_IMAGE) ...

# --- [TAMBAHKAN BLOK INI] ---
# Muat Gambar Musuh Shooter (Musuh Tipe 2)
ENEMY_SHOOTER_IMAGE = None
# Gunakan variabel dari settings.py
enemy_shooter_path = os.path.join(IMAGE_FOLDER, s.ENEMY_SHOOTER_PATH) 
if os.path.exists(enemy_shooter_path):
    try:
        ENEMY_SHOOTER_IMAGE = pygame.image.load(enemy_shooter_path).convert_alpha()
        # Gunakan ukuran dari settings.py
        ENEMY_SHOOTER_IMAGE = pygame.transform.scale(ENEMY_SHOOTER_IMAGE, s.ENEMY_SHOOTER_SIZE)
        print(f"Gambar musuh shooter '{enemy_shooter_path}' berhasil dimuat.")
    except pygame.error as e:
        print(f"Error memuat gambar musuh shooter '{enemy_shooter_path}': {e}")
        ENEMY_SHOOTER_IMAGE = None
else:
    print(f"Peringatan: Gambar player '{player_image_path}' tidak ditemukan. Menggunakan bentuk default.")