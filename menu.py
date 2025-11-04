import settings as s
import assets # [DITAMBAHKAN]
import pygame

# --- Variabel Lokal untuk Menu ---
# [DIHAPUS] Semua konstanta dihapus

# --- Inisialisasi font ---
# [DIHAPUS] Definisi title_font dan button_font dihapus
# Kita akan menggunakan assets.menu_title_font dan assets.menu_button_font

# Buat tombol
button_width = 200
button_height = 70
start_button_rect = pygame.Rect(
    (s.SCREEN_WIDTH - button_width) // 2, 
    (s.SCREEN_HEIGHT // 2) + 30,          
    button_width, 
    button_height
)

def run_menu(screen, clock):
    """
    Menjalankan loop menu.
    Menerima 'screen' dan 'clock' dari main.py.
    Mengembalikan status berikutnya ("playing" or "quit").
    """
    
    menu_running = True
    while menu_running:
        
        # --- 1. Event Handling Menu ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return "playing" 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "playing"

        # --- 2. Render Menu ---
        screen.fill(s.BLACK) 
        
        # Gambar Judul
        # [DIUBAH] Menggunakan assets.menu_title_font
        title_text = assets.menu_title_font.render("Space Man", True, s.WHITE) 
        title_rect = title_text.get_rect(center=(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)
        
        # Gambar Tombol Mulai
        pygame.draw.rect(screen, s.GREEN_TOSCA, start_button_rect, border_radius=10)
        # [DIUBAH] Menggunakan assets.menu_button_font
        start_text = assets.menu_button_font.render("Mulai", True, s.BLACK) 
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

        # --- 3. Update Layar ---
        pygame.display.flip()
        clock.tick(s.FPS)