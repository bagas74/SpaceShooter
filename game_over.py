import settings as s
import assets # [DITAMBAHKAN]
import pygame

# --- Variabel Lokal untuk Game Over ---
# [DIHAPUS] Semua konstanta dihapus

# --- Inisialisasi font ---
# [DIHAPUS] Definisi title_font, button_font, dan score_font dihapus
# Kita akan menggunakan font dari assets

# Buat Tombol "Menu"
button_width = 180
button_height = 60
menu_button_rect = pygame.Rect(
    (s.SCREEN_WIDTH // 2) - button_width - 20, 
    (s.SCREEN_HEIGHT // 2) + 50,
    button_width, 
    button_height
)

# Buat Tombol "Keluar"
quit_button_rect = pygame.Rect(
    (s.SCREEN_WIDTH // 2) + 20, 
    (s.SCREEN_HEIGHT // 2) + 50, 
    button_width, 
    button_height
)

def run_game_over(screen, clock, final_score):
    """
    Menjalankan loop layar game over.
    Mengembalikan "menu" atau "quit".
    """
    
    game_over_running = True
    while game_over_running:
        
        # --- 1. Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit" 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button_rect.collidepoint(event.pos):
                    return "menu" 
                
                if quit_button_rect.collidepoint(event.pos):
                    return "quit" 

        # --- 2. Render ---
        screen.fill(s.BLACK)
        
        # Gambar Judul
        # [DIUBAH] Menggunakan assets.title_font
        title_text = assets.title_font.render("GAME OVER", True, s.RED)
        title_rect = title_text.get_rect(center=(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2 - 80))
        screen.blit(title_text, title_rect)

        # Tampilkan Skor Akhir
        score_text_str = f"Skor Anda: {final_score}"
        # [DIUBAH] Menggunakan assets.score_font
        score_text = assets.score_font.render(score_text_str, True, s.WHITE) 
        score_rect = score_text.get_rect(center=(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2 - 20))
        screen.blit(score_text, score_rect)
        
        # Gambar Tombol "Menu"
        pygame.draw.rect(screen, s.GREEN, menu_button_rect, border_radius=10)
        # [DIUBAH] Menggunakan assets.button_font
        menu_text = assets.button_font.render("Menu", True, s.WHITE) 
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        screen.blit(menu_text, menu_text_rect)

        # Gambar Tombol "Keluar"
        pygame.draw.rect(screen, s.RED, quit_button_rect, border_radius=10)
        # [DIUBAH] Menggunakan assets.button_font
        quit_text = assets.button_font.render("Keluar", True, s.WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        screen.blit(quit_text, quit_text_rect)

        # --- 3. Update Layar ---
        pygame.display.flip()
        clock.tick(s.FPS)