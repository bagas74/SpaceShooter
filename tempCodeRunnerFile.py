import sys
import pygame # <<< [PERBAIKAN] Modul pygame belum di-import

# --- Inisialisasi Utama ---
pygame.init()

# --- Impor Modul Game Anda ---
import menu
import game
import game_over

# --- Pengaturan Layar ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# [UBAH] Judul game Anda dari permintaan sebelumnya
pygame.display.set_caption("Space Shooter") 
clock = pygame.time.Clock()

# --- [BARU] Muat High Score di Awal ---
# Kita asumsikan fungsi load_high_score() ada di dalam file game.py
try:
    high_score = game.load_high_score()
except AttributeError:
    print("Error: Pastikan 'game.py' memiliki fungsi 'load_high_score()'")
    high_score = 0

# --- [BARU] Variabel untuk skor ---
# Variabel ini akan menyimpan skor di akhir ronde
final_score = 0

# --- Game State Manager ---
game_state = "menu"
running = True

while running:
    if game_state == "menu":
        # Modul menu tidak perlu tahu high score, ia hanya memulai
        result = menu.run_menu(screen, clock)
        
        if result == "playing":
            game_state = "playing"
        elif result == "quit":
            running = False

    elif game_state == "playing":
        # [PERBAIKAN KUNCI 1]
        # 1. Kirim 'high_score' ke dalam game.
        # 2. Terima DUA nilai kembali: 'result' (game_over/quit) dan 'final_score'.
        result, final_score = game.run_game(screen, clock, high_score)
        
        if result == "game_over":
            game_state = "game_over" # <-- Ini sudah benar
            
            # [PERBAIKAN KUNCI 2]
            # Cek dan simpan high score baru DI SINI (di file main)
            if final_score > high_score:
                high_score = final_score
                # Kita asumsikan fungsi save_high_score() ada di game.py
                try:
                    game.save_high_score(high_score)
                except AttributeError:
                    print("Error: 'game.py' tidak punya 'save_high_score()'")

        elif result == "quit":
            running = False

    # [INFORMASI] Logika Anda untuk masuk ke 'game_over.py' sudah benar.
    # Saat 'game_state' diubah (di blok "playing"), 
    # loop berikutnya akan menjalankan blok di bawah ini.
    elif game_state == "game_over":
        # [PERBAIKAN KUNCI 3]
        # Kirim 'final_score' dan 'high_score' ke layar game over
        # agar bisa ditampilkan.
        result = game_over.run_game_over(screen, clock, final_score, high_score)
        
        if result == "playing":
            game_state = "playing" # Kembali main
        elif result == "quit":
            running = False

# --- Keluar ---
pygame.quit()
sys.exit() # [REKOMENDASI] Tambahkan sys.exit() untuk keluar bersih