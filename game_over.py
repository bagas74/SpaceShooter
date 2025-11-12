import settings as s
import assets # [DITAMBAHKAN]
import pygame
import os # <-- [BARU] Diperlukan untuk memeriksa keberadaan file

# --- [BARU] Nama file untuk menyimpan skor ---
HIGH_SCORE_FILE = "highscore.txt"

# --- [BARU] Fungsi untuk memuat high score ---
def load_high_score():
    """Membaca high score dari file."""
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            score = int(file.read())
            return score
    except (IOError, ValueError):
        return 0

# --- [BARU] Fungsi untuk menyimpan high score ---
def save_high_score(new_score):
    """Menyimpan high score baru ke file."""
    try:
        with open(HIGH_SCORE_FILE, 'w') as file:
            file.write(str(new_score))
    except IOError:
        print(f"Error: Tidak dapat menyimpan high score ke {HIGH_SCORE_FILE}")


# --- Tata Letak Tombol ---
button_width = 200 
button_height = 60
button_spacing = 20 
center_x = s.SCREEN_WIDTH // 2
start_y = (s.SCREEN_HEIGHT // 2) + 50 # Posisi Y tombol pertama

# Tombol "Menu"
menu_button_rect = pygame.Rect(
    center_x - (button_width // 2), 
    start_y,
    button_width, 
    button_height
)

# Tombol "Credits"
credits_button_rect = pygame.Rect(
    center_x - (button_width // 2), 
    menu_button_rect.bottom + button_spacing, 
    button_width, 
    button_height
)

# Tombol "Keluar"
quit_button_rect = pygame.Rect(
    center_x - (button_width // 2), 
    credits_button_rect.bottom + button_spacing, 
    button_width, 
    button_height
)

if s.MUSIC_ENABLED:
    pygame.mixer.music.load(assets.MUSIC_MENU)
    pygame.mixer.music.play(-1)

def run_game_over(screen, clock, final_score):
    """
    Menjalankan loop layar game over.
    Mengembalikan "menu", "credits", atau "quit".
    """
    
    # --- Logika High Score (Dijalankan satu kali) ---
    high_score = load_high_score()
    is_new_high_score = False
    
    if final_score > high_score:
        high_score = final_score
        save_high_score(high_score) # Simpan skor baru
        is_new_high_score = True
        
    # --- Variabel untuk Animasi ---
    animation_timer = 0
    flash_colors = [s.POWERUP_ORANGE, s.WHITE] 
    
    game_over_running = True
    while game_over_running:
        
        # --- 1. Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit" 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button_rect.collidepoint(event.pos):
                    return "menu" 
                elif credits_button_rect.collidepoint(event.pos):
                    return "credits"
                elif quit_button_rect.collidepoint(event.pos):
                    return "quit" 

        # --- Update Timer Animasi ---
        animation_timer += 1

        # --- 2. Render ---
        screen.fill(s.BLACK)
        
        # [MODIFIKASI] Tampilkan "NEW HIGH SCORE!" di TENGAH ATAS
        if is_new_high_score:
            color_index = (animation_timer // 20) % len(flash_colors)
            current_color = flash_colors[color_index]
            
            new_hs_text = assets.score_font.render("NEW HIGH SCORE!", True, current_color) 
            
            # Posisikan di tengah atas dengan padding 20px
            # 'midtop' = (center_x, top_y)
            new_hs_rect = new_hs_text.get_rect(midtop=(s.SCREEN_WIDTH // 2, 20)) 
            screen.blit(new_hs_text, new_hs_rect)
        
        # Gambar Judul (Posisinya tetap)
        title_text = assets.title_font.render("GAME OVER", True, s.RED)
        title_rect = title_text.get_rect(center=(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2 - 130)) 
        screen.blit(title_text, title_rect)

        # Tampilkan High Score (Posisinya tetap)
        hs_text_str = f"Skor Tertinggi: {high_score}"
        hs_text = assets.score_font.render(hs_text_str, True, s.WHITE) 
        hs_rect = hs_text.get_rect(center=(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2 - 70)) 
        screen.blit(hs_text, hs_rect)

        # Tampilkan Skor Akhir (Posisinya tetap)
        score_text_str = f"Skor Anda: {final_score}"
        score_text = assets.score_font.render(score_text_str, True, s.WHITE) 
        score_rect = score_text.get_rect(center=(s.SCREEN_WIDTH // 2, hs_rect.bottom + 25)) 
        screen.blit(score_text, score_rect)
        
        # --- (Render Tombol tidak berubah) ---
        
        # Gambar Tombol "Menu"
        pygame.draw.rect(screen, s.GREEN, menu_button_rect, border_radius=10)
        menu_text = assets.button_font.render("Menu", True, s.WHITE) 
        menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
        screen.blit(menu_text, menu_text_rect)

        # Gambar Tombol "Credits"
        pygame.draw.rect(screen, s.POWERUP_BLUE, credits_button_rect, border_radius=10)
        credits_text = assets.button_font.render("Credits", True, s.BLACK) 
        credits_text_rect = credits_text.get_rect(center=credits_button_rect.center)
        screen.blit(credits_text, credits_text_rect)

        # Gambar Tombol "Keluar"
        pygame.draw.rect(screen, s.RED, quit_button_rect, border_radius=10)
        quit_text = assets.button_font.render("Keluar", True, s.WHITE)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        screen.blit(quit_text, quit_text_rect)

        # --- 3. Update Layar ---
        pygame.display.flip()
        clock.tick(s.FPS)