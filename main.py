import settings as s
import pygame

# --- Inisialisasi Utama ---
pygame.init() 
pygame.mixer.init() 

# --- Impor Modul Game Anda ---
import menu   
import game   
import game_over 
import assets 

# --- Pengaturan Layar ---
screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
pygame.display.set_caption("Space Man: Asteroid Dodge (Modular)")
clock = pygame.time.Clock()

# --- Game State Manager ---
game_state = "menu"
current_score = 0
running = True

while running:
    if game_state == "menu":
        pygame.event.clear() # <-- [HARUS ADA]
        result = menu.run_menu(screen, clock)
        
        if result == "playing":
            game_state = "playing" 
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
        pygame.event.clear() # <-- [HARUS ADA]
        result = game_over.run_game_over(screen, clock, current_score)
        
        # [WAJIB DIPERBAIKI] Pastikan logikanya seperti ini
        if result == "menu": 
            game_state = "menu" # Kembali ke menu
        elif result == "quit":
            running = False 

# --- Keluar ---
pygame.quit()