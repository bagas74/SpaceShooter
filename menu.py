import pygame
# --- Variabel Lokal untuk Menu ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN_TOSCA = (0, 204, 153)
# Kita perlu tahu ukuran layar untuk menempatkan tombol
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Inisialisasi font (Pygame sudah di-init di main.py)
title_font = pygame.font.SysFont(None, 80)
button_font = pygame.font.SysFont(None, 50)

# Buat tombol
button_width = 200
button_height = 70
start_button_rect = pygame.Rect(
 (SCREEN_WIDTH - button_width) // 2, 
 (SCREEN_HEIGHT // 2) + 30, 
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
 return "quit" # Memberi sinyal "quit" ke main.py
 
 if event.type == pygame.MOUSEBUTTONDOWN:
 if start_button_rect.collidepoint(event.pos):
 return "playing" # Memberi sinyal "playing" ke main.py
 
 if event.type == pygame.KEYDOWN:
 if event.key == pygame.K_RETURN:
 return "playing" # Memberi sinyal "playing" ke main.py
 # --- 2. Render Menu ---
 screen.fill(BLACK)
 
 # Gambar Judul
 title_text = title_font.render("Space Man", True, WHITE)
 title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 
- 50))
 screen.blit(title_text, title_rect)
 
 # Gambar Tombol Mulai
 pygame.draw.rect(screen, GREEN_TOSCA, start_button_rect, border_radius=10)
 start_text = button_font.render("Mulai", True, BLACK)
 start_text_rect = start_text.get_rect(center=start_button_rect.center)
 screen.blit(start_text, start_text_rect)
 # --- 3. Update Layar ---
 pygame.display.flip()
 clock.tick(60)