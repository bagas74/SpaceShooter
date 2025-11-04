import pygame 
 
# --- Variabel Lokal untuk Game Over --- 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 
RED = (200, 0, 0)  
GREEN = (0, 150, 0)  
 
SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 600 
 
# Inisialisasi font  
title_font = pygame.font.SysFont(None, 100) 
button_font = pygame.font.SysFont(None, 45) 

# Buat Tombol "Main Lagi" 
button_width = 180 
button_height = 60 
restart_button_rect = pygame.Rect( 
    (SCREEN_WIDTH // 2) - button_width - 20,  
    (SCREEN_HEIGHT // 2) + 50,  
    button_width,  
    button_height 
) 