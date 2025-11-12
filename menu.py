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