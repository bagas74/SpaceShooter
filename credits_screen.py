import pygame
import settings as s
import assets

if s.MUSIC_ENABLED:
    pygame.mixer.music.load(assets.MUSIC_MENU)
    pygame.mixer.music.play(-1)

def run(screen, clock):
    """
    Menjalankan layar Credit yang menggulir.
    Akan kembali ke 'menu' saat tombol ditekan.
    """
    
    # --- Teks Kredit ---
    # [DIUBAH] Nama placeholder telah diganti
    credit_lines = [
        ("CREDITS", assets.stage_clear_font), # Font besar/judul
        ("", assets.font_ui), # Spasi
        ("Game Design & Programming", assets.font),
        ("StarWars Studio", assets.font_ui), # <-- DIUBAH
        ("", assets.font_ui),
        ("Art & Graphics", assets.font),
        ("StarWars Studio", assets.font_ui), # <-- DIUBAH
        # (Anda bisa tambahkan sumber aset lain di sini jika perlu)
        ("", assets.font_ui),
        ("Music & Sound Effects", assets.font),
        ("Strange Battle oleh TossDaCook dari itch.io", assets.font_ui),
        ("Space Jam 1 oleh LilyRabbit dari itch.io", assets.font_ui),
        ("SFX dari freesound.org", assets.font_ui),
        ("", assets.font_ui),
        ("Special Thanks", assets.font),
        ("StarWars Team", assets.font_ui),
        ("", assets.font_ui),
        ("", assets.font_ui),
        ("© 2025 StarWars Studio", assets.font_ui), # <-- DIUBAH
        ("", assets.font_ui),
        ("", assets.font_ui),
        ("Tekan ESC atau ENTER untuk kembali", assets.font)
    ]

    # --- Render Teks (Satu kali saja) ---
    rendered_surfaces = []
    for text, font in credit_lines:
        rendered_surfaces.append(font.render(text, True, s.WHITE))
    
    line_spacing = 10  # Spasi ekstra antar baris
    
    # [BARU] Variabel untuk scrolling
    scroll_speed = 1.0  # Kecepatan gulir (1 piksel per frame)
    
    # Mulai scroll_y dari bawah layar agar teks muncul dari bawah
    scroll_y = s.SCREEN_HEIGHT 
    
    # [BARU] Hitung total tinggi semua teks untuk looping
    total_height = 0
    for surface in rendered_surfaces:
        total_height += surface.get_height() + line_spacing
        

    # --- Game Loop (Hanya untuk layar ini) ---
    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # Kirim sinyal 'quit' ke main.py
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return "menu"  # Kembali ke menu

        # 2. [BARU] Update Logika Scroll
        scroll_y -= scroll_speed
        
        # Jika semua teks sudah tergulir ke atas (hilang),
        # reset posisinya ke bawah layar lagi agar berulang (looping)
        if scroll_y + total_height < 0:
            scroll_y = s.SCREEN_HEIGHT

        
        # 3. Draw
        screen.fill(s.BLACK)
        
        # [MODIFIKASI] Gunakan 'scroll_y' sebagai Y awal
        current_y = scroll_y 
        
        for surface in rendered_surfaces:
            # Dapatkan rect dan pusatkan di layar
            rect = surface.get_rect(center=(s.SCREEN_WIDTH // 2, current_y))
            
            # Gambar teks ke layar
            screen.blit(surface, rect)
            
            # Pindah ke baris berikutnya
            current_y += surface.get_height() + line_spacing

        # 4. Flip Display
        pygame.display.flip()
        clock.tick(s.FPS)

    return "menu" # Jaga-jaga jika loop berhenti