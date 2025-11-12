import settings as s
import pygame
import sys

# --- Inisialisasi Utama ---
pygame.init() 
pygame.mixer.init() 

# --- [PERBAIKAN] Pengaturan Layar DIPINDAHKAN KE ATAS ---
# Kita HARUS membuat layar/screen SEBELUM mengimpor file (seperti assets)
# yang mencoba memuat gambar.

# [MODIFIKASI] Tambahkan flag RESIZABLE (bisa diubah ukuran) dan SCALED (otomatis stretch)
screen = pygame.display.set_mode(
    (s.SCREEN_WIDTH, s.SCREEN_HEIGHT),
    pygame.RESIZABLE | pygame.SCALED
)
# [SELESAI MODIFIKASI]

pygame.display.set_caption("Space Man: StarWars")
clock = pygame.time.Clock()

# Atur Volume Musik
pygame.mixer.music.set_volume(s.MUSIC_VOLUME) 
# --- [SELESAI PERBAIKAN] ---


# --- Impor Modul Game Anda ---
# Sekarang aman untuk mengimpor file-file ini
import menu   
import game   
import game_over 
import assets 
import credits_screen


# --- Game State Manager ---
game_state = "menu"
current_score = 0
running = True
# [HAPUS] current_music dihapus (sudah dihapus oleh Anda, ini benar)

while running:
    
    # --- [HAPUS] SEMUA BLOK LOGIKA MUSIK DIHAPUS DARI SINI ---

    # --- Logika Status Game (Pondasi Anda - Tidak Berubah) ---
    if game_state == "menu":
        pygame.event.clear()
        result = menu.run_menu(screen, clock)
        
        if result == "playing":
            game_state = "playing" 
        elif result == "credits": 
            game_state = "credits"
        elif result == "quit":
            running = False 

    elif game_state == "playing":
        result, score_from_game = game.run_game(screen, clock) 

        if result == "game_over":
            game_state = "game_over"
            current_score = score_from_game 
        elif result == "quit":
            running = False 

    elif game_state == "game_over":
        pygame.event.clear()
        result = game_over.run_game_over(screen, clock, current_score)
        
        if result == "menu": 
            game_state = "menu"
        elif result == "credits":
            game_state = "credits"
        elif result == "quit":
            running = False 
            
    elif game_state == "credits":
        pygame.event.clear()
        result = credits_screen.run(screen, clock)
        
        if result == "menu":
            game_state = "menu"
        elif result == "quit":
            running = False

# --- Keluar ---
pygame.quit()
sys.exit()