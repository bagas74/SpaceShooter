import settings as s
import assets 
import pygame

# --- [PERBAIKAN] Definisi Rect Tombol yang lengkap ---
button_width = 200
button_height = 70

start_button_rect = pygame.Rect(
    (s.SCREEN_WIDTH - button_width) // 2, 
    (s.SCREEN_HEIGHT // 2) + 30,          
    button_width, 
    button_height
)

credits_button_rect = pygame.Rect(
    (s.SCREEN_WIDTH - button_width) // 2, 
    start_button_rect.bottom + 20, 
    button_width, 
    button_height
)

quit_button_rect = pygame.Rect(
    (s.SCREEN_WIDTH - button_width) // 2, 
    credits_button_rect.bottom + 20, 
    button_width, 
    button_height
)

music_toggle_width = 150
music_toggle_height = 50 
music_toggle_rect = pygame.Rect(
    s.SCREEN_WIDTH - music_toggle_width - 20, # 20px dari kanan
    start_button_rect.top, # Sejajar dengan tombol 'Mulai'
    music_toggle_width, 
    music_toggle_height
)
# --- [SELESAI PERBAIKAN] ---


def run_menu(screen, clock):
    """
    Menjalankan loop menu.
    """
    
    # --- [BARU] Logika Musik untuk Layar Ini ---
    # Cek jika musik HARUSNYA menyala saat masuk layar
    if s.MUSIC_ENABLED:
        pygame.mixer.music.load(assets.MUSIC_MENU)
        pygame.mixer.music.play(-1) # -1 = loop
    # --- [SELESAI BLOK BARU] ---
    
    menu_running = True
    while menu_running:
        
        # --- 1. Event Handling Menu ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return "playing" 
                elif credits_button_rect.collidepoint(event.pos):
                    return "credits"
                elif quit_button_rect.collidepoint(event.pos):
                    return "quit"
                
                # --- [MODIFIKASI] Logika Toggle Musik ---
                elif music_toggle_rect.collidepoint(event.pos):
                    s.MUSIC_ENABLED = not s.MUSIC_ENABLED # Balik nilainya
                    
                    if s.MUSIC_ENABLED:
                        # Jika baru dinyalakan, putar musik
                        pygame.mixer.music.load(assets.MUSIC_MENU)
                        pygame.mixer.music.play(-1)
                    else:
                        # Jika baru dimatikan, hentikan
                        pygame.mixer.music.stop() 
                # --- [SELESAI MODIFIKASI] ---
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "playing"

        # --- 2. Render Menu ---
        screen.fill(s.BLACK) 
        
        # Gambar Judul
        title_text = assets.menu_title_font.render("Space Man", True, s.WHITE) 
        title_rect = title_text.get_rect(center=(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_text, title_rect)
        
        # Gambar Tombol Mulai
        pygame.draw.rect(screen, s.GREEN_TOSCA, start_button_rect, border_radius=10)
        start_text = assets.menu_button_font.render("Mulai", True, s.BLACK) 
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_text_rect)

        # Gambar Tombol Credits
        pygame.draw.rect(screen, s.POWERUP_BLUE, credits_button_rect, border_radius=10)
        credits_text = assets.menu_button_font.render("Credits", True, s.BLACK) 
        credits_text_rect = credits_text.get_rect(center=credits_button_rect.center)
        screen.blit(credits_text, credits_text_rect)

        # Gambar Tombol Keluar
        pygame.draw.rect(screen, s.POWERUP_RED, quit_button_rect, border_radius=10)
        quit_text = assets.menu_button_font.render("Keluar", True, s.BLACK) 
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        screen.blit(quit_text, quit_text_rect)
        
        # Render Tombol Musik (Logika ini sudah benar)
        if s.MUSIC_ENABLED:
            music_text_str = "Music: On"
            music_btn_color = s.GREEN_TOSCA
        else:
            music_text_str = "Music: Off"
            music_btn_color = s.POWERUP_RED
            
        pygame.draw.rect(screen, music_btn_color, music_toggle_rect, border_radius=10)
        music_text_surf = assets.button_font.render(music_text_str, True, s.BLACK) 
        music_text_rect = music_text_surf.get_rect(center=music_toggle_rect.center)
        screen.blit(music_text_surf, music_text_rect)

        # --- 3. Update Layar ---
        pygame.display.flip()
        clock.tick(s.FPS)