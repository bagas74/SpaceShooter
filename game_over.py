import pygame
import os # Impor modul os untuk memeriksa file

# --- Variabel Lokal untuk Game Over ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0) 
GREEN = (0, 150, 0) 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Inisialisasi font 
# Kita perlu inisialisasi pygame.font di sini juga
pygame.font.init() 
title_font = pygame.font.SysFont(None, 100)
# [PERUBAHAN] Mengubah ukuran font skor dari 60 menjadi 45
score_font = pygame.font.SysFont(None, 45) 
button_font = pygame.font.SysFont(None, 45)

# [BARU] Muat gambar latar belakang
BACKGROUND_IMAGE_PATH = "background_menu.jpg"
BACKGROUND_IMAGE = None

if os.path.exists(BACKGROUND_IMAGE_PATH):
    try:
        BACKGROUND_IMAGE = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
        BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
        print(f"Gambar latar belakang '{BACKGROUND_IMAGE_PATH}' berhasil dimuat.")
    except pygame.error as e:
        print(f"Error memuat gambar latar belakang '{BACKGROUND_IMAGE_PATH}': {e}")
        BACKGROUND_IMAGE = None
else:
    print(f"Peringatan: Gambar latar belakang '{BACKGROUND_IMAGE_PATH}' tidak ditemukan. Menggunakan latar belakang hitam.")

# [PERBAIKAN] Pindahkan posisi Y tombol agar ada ruang untuk skor
button_y_pos = (SCREEN_HEIGHT // 2) + 100 

# Buat Tombol "Main Lagi"
button_width = 180
button_height = 60
restart_button_rect = pygame.Rect(
    (SCREEN_WIDTH // 2) - button_width - 20, 
    button_y_pos, # [UBAH]
    button_width, 
    button_height
)

# Buat Tombol "Keluar"
quit_button_rect = pygame.Rect(
    (SCREEN_WIDTH // 2) + 20, 
    button_y_pos, # [UBAH]
    button_width, 
    button_height
)

# [PERBAIKAN KUNCI 1]
# Terima 4 argumen: screen, clock, final_score, dan high_score
def run_game_over(screen, clock, final_score, high_score):
    """
    Menjalankan loop layar game over.
    Mengembalikan "playing" atau "quit".
    """
    
    game_over_running = True
    while game_over_running:
        
        # --- 1. Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit" 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return "playing" 
                
                if quit_button_rect.collidepoint(event.pos):
                    return "quit" 

        # --- 2. Render ---
        if BACKGROUND_IMAGE:
            screen.blit(BACKGROUND_IMAGE, (0, 0)) # [BARU] Gambar latar belakang
        else:
            screen.fill(BLACK) # Jika gambar tidak ada, isi dengan hitam
        
        # [PERBAIKAN KUNCI 2] Geser "GAME OVER" ke atas
        title_text = title_font.render("GAME OVER", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(title_text, title_rect)
        
        # [PERBAIKAN KUNCI 3] Tampilkan Skor Akhir dan High Score
        # Ukuran font sekarang lebih kecil (45)
        score_text = score_font.render(f"Skor Anda: {final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(score_text, score_rect)
        
        # Ukuran font sekarang lebih kecil (45)
        hiscore_text = score_font.render(f"High Score: {high_score}", True, WHITE)
        hiscore_rect = hiscore_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(hiscore_text, hiscore_rect)
        
        
        # Gambar Tombol "Main Lagi"
        pygame.draw.rect(screen, GREEN, restart_button_rect, border_radius=10)
        restart_text = button_font.render("Main Lagi", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        screen.blit(restart_text, restart_text_rect)

        # Gambar Tombol "Keluar"
        pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10)
        quit_text = button_font.render("Keluar", True, WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        screen.blit(quit_text, quit_text_rect)

        # --- 3. Update Layar ---
        pygame.display.flip()
        clock.tick(60)

# Bagian ini hanya untuk pengujian mandiri file game_over.py
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Over Test")
    clock = pygame.time.Clock()

    # Contoh penggunaan
    contoh_final_score = 1230
    contoh_high_score = 2500

    result = run_game_over(screen, clock, contoh_final_score, contoh_high_score)
    print(f"Hasil dari layar game over: {result}")
    pygame.quit()