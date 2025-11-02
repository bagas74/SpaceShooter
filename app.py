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
    