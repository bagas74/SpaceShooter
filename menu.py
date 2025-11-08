import pygame
import os # <-- Impor 'os' untuk path file

# --- Variabel Lokal untuk Menu ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN_TOSCA = (0, 204, 153)

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- [PERBAIKAN] Path Absolut ke Aset ---
# Dapatkan path ke folder tempat script 'menu.py' ini berada
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
  import pygame
import os 
import math # [BARU] Impor modul 'math' untuk animasi sinus

# --- Variabel Lokal untuk Menu ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_CYAN = (0, 255, 255) # [UBAH] Warna baru yang futuristik

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- Path Aset ---
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd() 
    
# Path untuk background
background_img_path = os.path.join(script_dir, "background_menu.jpg")

# [BARU] Path untuk font kustom
# Pastikan Anda sudah mengunduh 'Orbitron-Bold.ttf' ke folder ini
FONT_FILENAME = "Orbitron-Bold.ttf" 
font_path = os.path.join(script_dir, FONT_FILENAME)

# --- Muat Gambar Background ---
try:
    background_img_original = pygame.image.load(background_img_path).convert()
    background_img = pygame.transform.scale(background_img_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error: Tidak dapat memuat gambar di path: {background_img_path}")
    background_img = None 

# --- [UBAH] Muat Font Kustom ---
# Kita akan menggunakan font 'Orbitron'
try:
    title_font = pygame.font.Font(font_path, 70)
    button_font = pygame.font.Font(font_path, 40)
    prompt_font = pygame.font.Font(font_path, 20) # [BARU] Font kecil untuk teks prompt
except FileNotFoundError:
    print(f"Error: File font '{FONT_FILENAME}' tidak ditemukan di path: {font_path}")
    print("Menggunakan font default sistem.")
    title_font = pygame.font.SysFont(None, 80)
    button_font = pygame.font.SysFont(None, 50)
    prompt_font = pygame.font.SysFont(None, 25)
except pygame.error as e:
    print(f"Error saat memuat font: {e}")
    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)
    prompt_font = pygame.font.Font(None, 25)

# --- Buat Tombol ---
button_width = 220 # [UBAH] Sedikit lebih lebar
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
    Mengembalikan status berikutnya ("playing" or "quit").
    """
    
    menu_running = True
    while menu_running:
        
        # [BARU] Dapatkan posisi mouse setiap frame
        mouse_pos = pygame.mouse.get_pos()
        # [BARU] Cek apakah mouse berada di atas tombol
        is_hovering = start_button_rect.collidepoint(mouse_pos)

        # --- 1. Event Handling Menu ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit" 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovering: # [UBAH] Cek variabel hover
                    return "playing" 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "playing" 

        # --- 2. Render Menu ---
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(BLACK) 
        
        # Gambar Judul
        title_text = title_font.render("SPACE MAN", True, WHITE) # [UBAH] Kapital
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)
        
        # --- [UBAH] Logika Render Tombol (Hover Effect) ---
        if is_hovering:
            # Tampilan saat mouse di atas: Solid
            pygame.draw.rect(screen, NEON_CYAN, start_button_rect, border_radius=10)
            start_text = button_font.render("MULAI", True, BLACK) # Teks hitam
        else:
            # Tampilan normal: Outline
            pygame.draw.rect(screen, NEON_CYAN, start_button_rect, border_radius=10, width=3)
            start_text = button_font.render("MULAI", True, NEON_CYAN) # Teks neon
        
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

        # --- [BARU] Animasi Teks Prompt Berkedip ---
        # Buat nilai yang berosilasi antara 150-255 menggunakan sin()
        pulse_val = 150 + (math.sin(pygame.time.get_ticks() * 0.003) + 1) * 52.5
        prompt_color = (pulse_val, pulse_val, pulse_val) # Warna abu-abu berkedip

        prompt_text = prompt_font.render("TEKAN ENTER UNTUK MEMULAI", True, prompt_color)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, start_button_rect.bottom + 40))
        screen.blit(prompt_text, prompt_rect)

        # --- 3. Update Layar ---
        pygame.display.flip()
        clock.tick(60)  # Fallback jika __file__ tidak terdefinisi (misal, di IDLE)
    script_dir = os.getcwd() 
    
# Gabungkan path folder tersebut dengan nama file gambar
background_img_path = os.path.join(script_dir, "background_menu.jpg")

# --- Muat Gambar Background ---
try:
    # 1. Muat gambar menggunakan path absolut
    background_img_original = pygame.image.load(background_img_path).convert()
    # 2. Sesuaikan ukuran gambar agar pas dengan layar
    background_img = pygame.transform.scale(background_img_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error: Tidak dapat memuat gambar di path: {background_img_path}")
    print(f"Pastikan file 'background_menu.jpg' ada di folder yang sama dengan 'menu.py'.")
    print(f"Detail error: {e}")
    background_img = None 

# Inisialisasi font (Pygame sudah di-init di main.py)
try:
    title_font = pygame.font.SysFont(None, 80)
    button_font = pygame.font.SysFont(None, 50)
except pygame.error as e:
    print(f"Error saat memuat font: {e}")
    # Jika font gagal, Pygame akan error, jadi kita inisialisasi default
    # (Meskipun error 'No video mode' adalah penyebab utamanya)
    pygame.font.init() # Pastikan modul font diinisialisasi jika terjadi error aneh
    title_font = pygame.font.Font(None, 80) # Gunakan font default
    button_font = pygame.font.Font(None, 50)


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
                if event.key == pygame.K_RETURN: # Tekan Enter
                    return "playing" 

        # --- 2. Render Menu ---
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(BLACK) 
        
        # Gambar Judul
        title_text = title_font.render("Space Man", True, WHITE) 
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)
        
        # Gambar Tombol Mulai
        pygame.draw.rect(screen, GREEN_TOSCA, start_button_rect, border_radius=10)
        start_text = button_font.render("Mulai", True, BLACK)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

        # --- 3. Update Layar ---
        pygame.display.flip()
        clock.tick(60)

# [PENTING] Pastikan tidak ada kode lain di bawah ini.
# File ini hanya mendefinisikan fungsi, tidak menjalankannya.