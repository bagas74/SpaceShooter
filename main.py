import pygame 
 
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
pygame.display.set_caption("Space Man: Asteroid Dodge (Modular)") 
clock = pygame.time.Clock() 
 
# --- Game State Manager --- 
game_state = "menu" 
running = True 
 
while running: 
    if game_state == "menu": 
        result = menu.run_menu(screen, clock)
          if result == "playing": 
            game_state = "playing"  
        elif result == "quit": 
            running = False  
 
    elif game_state == "playing": 
        result = game.run_game(screen, clock)  
         
        if result == "game_over": 
            game_state = "game_over"  
        elif result == "quit": 
            running = False  
 
    # --- [PERUBAHAN DI BLOK INI] ---  
    elif game_state == "game_over": 
        result = game_over.run_game_over(screen, clock) 
         
        # [DIUBAH] Jika "Main Lagi" diklik, 'result' akan jadi "playing" 
        if result == "playing":  
            game_state = "playing" # Langsung kembali ke state game 
        elif result == "quit": 
            running = False  
 
# --- Keluar --- 
pygame.quit()
