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

# Buat Tombol "Keluar" 
quit_button_rect = pygame.Rect( 
    (SCREEN_WIDTH // 2) + 20,  
    (SCREEN_HEIGHT // 2) + 50,  
    button_width,  
    button_height 
) 

def run_game_over(screen, clock): 
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
                # Cek tombol "Main Lagi" 
                if restart_button_rect.collidepoint(event.pos): 
                    # [PERUBAHAN] Ganti dari "main_menu" menjadi "playing" 
                    return "playing"  
                 
                # Cek tombol "Keluar" 
                if quit_button_rect.collidepoint(event.pos): 
                    return "quit"  
 
        # --- 2. Render --- 
        screen.fill(BLACK) 
         
        title_text = title_font.render("GAME OVER", True, RED) 
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)) 
        screen.blit(title_text, title_rect)
        
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