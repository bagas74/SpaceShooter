import settings as s
import assets
import pygame
import random
import math
import sys
import os

from sprites import Player, Musuh, Peluru, PeluruMusuh, Powerup, Shockwave, PlayerLaser

try:
    player_mini_img = pygame.transform.scale(assets.PLAYER_IMAGE, (25, 27))
except: 
    player_mini_img = pygame.Surface((25, 27))
    player_mini_img.fill(s.POWERUP_BLUE)

def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)

# [KONSEP BARU] Fungsi Jeda Stage Terpisah
def show_stage_clear(screen, clock, stage_num):
    """
    Menjeda game dan menampilkan notifikasi Stage Clear.
    Memiliki loop-nya sendiri.
    """
    timer = 180 # Ambil 3 detik dari settings
    text = f"STAGE {stage_num}"
    
    while timer > 0:
        # Kita harus tetap menangani event QUIT di sini
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Jika user keluar saat jeda, kita harus return sinyal khusus
                return "quit" 

        # Gambar layar jeda
        screen.fill(s.BLACK)
        text_surf = assets.stage_clear_font.render(text, True, s.WHITE)
        text_rect = text_surf.get_rect(center=(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2))
        screen.blit(text_surf, text_rect)
        
        # Perbarui layar dan atur FPS
        pygame.display.flip()
        clock.tick(s.FPS)
        
        # Hitung mundur timer
        timer -= 1
        
    return "continue" # Sinyal untuk melanjutkan game


# --- run_game ---
def run_game(screen, clock):
    
    PLAYER_WIDTH = s.PLAYER_IMAGE_SIZE[0]
    PLAYER_HEIGHT = s.PLAYER_IMAGE_SIZE[1]
    player_speed = 10
    PLAYER_TOP_BOUNDARY = s.SCREEN_HEIGHT * 0.4 

    player = Player(PLAYER_WIDTH, PLAYER_HEIGHT)
    player.rect.centerx = s.SCREEN_WIDTH // 2 
    player.rect.bottom = s.SCREEN_HEIGHT - 10 

    semua_sprite = pygame.sprite.Group()
    grup_peluru_pemain = pygame.sprite.Group()
    grup_powerup = pygame.sprite.Group()
    grup_shockwave = pygame.sprite.Group()
    grup_musuh = pygame.sprite.Group()
    grup_peluru_musuh = pygame.sprite.Group()
    grup_laser_pemain = pygame.sprite.Group()

    semua_sprite.add(player)
    
    UFO_ENEMY_WIDTH = 60
    UFO_ENEMY_HEIGHT = 40
    SHOOTER_ENEMY_WIDTH = 60 
    SHOOTER_ENEMY_HEIGHT = 70 
    
    base_enemy_speed = 4
    
    for _ in range(3): 
        musuh = Musuh(UFO_ENEMY_WIDTH, UFO_ENEMY_HEIGHT, base_enemy_speed, is_new_enemy=False)
        for _ in range(10): 
            musuh.rect.x = random.randrange(s.SCREEN_WIDTH - musuh.rect.width) 
            collides = False
            for existing_enemy in grup_musuh:
                spawn_box = musuh.rect.inflate(UFO_ENEMY_WIDTH, 0) 
                if spawn_box.colliderect(existing_enemy.rect):
                    collides = True
                    break 
            if not collides:
                break 
        grup_musuh.add(musuh)
        semua_sprite.add(musuh)

    score = 0
    frame_count = 0
    special_meter_count = 0
    powerup_spawn_timer = 0
    
    # [DIHAPUS] Variabel jeda stage tidak diperlukan lagi
    # is_changing_stage = False
    # stage_clear_timer = 0
    # stage_clear_text = ""

    current_stage = 1
    max_ufo_enemies = 4 
    max_shooter_enemies = 0 
    current_enemy_speed = base_enemy_speed 

    game_running = True
    while game_running:

        # --- 1. Event Handling Game ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", 0 

            # [DIKEMBALIKAN] Event handling berjalan normal
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.can_shoot(frame_count):
                        player.shoot(frame_count, grup_peluru_pemain, semua_sprite)

        # --- [BLOK LOGIKA UTAMA] ---
        # [DIHAPUS] Blok 'if not is_changing_stage:' dihapus
            
        # --- UPDATE SKOR & FRAME ---
        frame_count += 1
        if frame_count % 12 == 0:
            score += 1
        
        # --- INPUT GERAK ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player.rect.right < s.SCREEN_WIDTH: 
            player.rect.x += player_speed
        if keys[pygame.K_UP] and player.rect.top > PLAYER_TOP_BOUNDARY:
            player.rect.y -= player_speed
        if keys[pygame.K_DOWN] and player.rect.bottom < s.SCREEN_HEIGHT: 
            player.rect.y += player_speed

        # --- 2. Logika Game (Update) ---
        new_enemy_bullets = []
        for sprite in semua_sprite:
            sprite.update() 
            
            if isinstance(sprite, Musuh) and sprite.is_new_enemy:
                if random.randrange(0, 100) < 2: 
                    peluru_baru = sprite.shoot() 
                    new_enemy_bullets.extend(peluru_baru)
        
        if new_enemy_bullets:
            semua_sprite.add(new_enemy_bullets)
            grup_peluru_musuh.add(new_enemy_bullets)
            
        player.update_timers()

        # [LOGIKA STAGE DIUBAH]
        new_stage = 1 + (score // 200) # (Ganti 200 ke 500 jika Anda mau)
        
        if new_stage > current_stage:
            # --- MULAI JEDA STAGE ---
            
            # Panggil fungsi jeda baru kita
            result = show_stage_clear(screen, clock, new_stage)
            if result == "quit": # Tangani jika user keluar saat jeda
                return "quit", 0
            
            # Setelah jeda selesai, atur ulang game
            current_stage = new_stage
            print(f"Memicu Stage {current_stage}!") 
            
            current_enemy_speed = base_enemy_speed + (current_stage * 0.5) 
            max_ufo_enemies = 3 + current_stage 
            max_shooter_enemies = current_stage - 1
            
            grup_musuh.empty()
            grup_peluru_musuh.empty()
            grup_peluru_pemain.empty()
            grup_powerup.empty()
        
        for musuh in grup_musuh.sprites():
            if musuh.rect.top > s.SCREEN_HEIGHT: 
                musuh.kill()
        
        powerup_spawn_timer += 1
        if powerup_spawn_timer >= s.POWERUP_SPAWN_RATE: 
            powerup_spawn_timer = 0 
            tipe = random.choice(['T', 'P', 'S', '+0.5'])
            new_powerup = Powerup(tipe)
            grup_powerup.add(new_powerup)
            semua_sprite.add(new_powerup)

        # --- 3. Cek Tabrakan ---
        tabrakan_peluru_musuh = pygame.sprite.groupcollide(grup_peluru_pemain, grup_musuh, True, True)
        for list_musuh_terkena in tabrakan_peluru_musuh.values():
            for musuh_yang_terkena in list_musuh_terkena:
                if musuh_yang_terkena.is_new_enemy: score += 50 
                else: score += 10 
                assets.suara_ledakan.play() 
                if not player.laser_active: special_meter_count += 1
        
        tabrakan_player_powerup = pygame.sprite.spritecollide(player, grup_powerup, True)
        for powerup in tabrakan_player_powerup:
            if powerup.type == 'T': player.activate_trishot()
            elif powerup.type == 'P': player.activate_shield()
            elif powerup.type == 'S':
                sw = Shockwave()
                semua_sprite.add(sw)
                grup_shockwave.add(sw)
                assets.suara_shockwave.play() 
            elif powerup.type == '+0.5': player.activate_speedup()

        tabrakan_shockwave_musuh = pygame.sprite.groupcollide(grup_shockwave, grup_musuh, False, True)
        for list_musuh_terkena in tabrakan_shockwave_musuh.values():
            for musuh_yang_terkena in list_musuh_terkena:
                if musuh_yang_terkena.is_new_enemy: score += 25
                else: score += 5
                assets.suara_ledakan.play()
                if not player.laser_active: special_meter_count += 1
        
        pygame.sprite.groupcollide(grup_shockwave, grup_peluru_musuh, False, True)
        pygame.sprite.groupcollide(grup_laser_pemain, grup_peluru_musuh, False, True)
        
        tabrakan_laser_musuh = pygame.sprite.groupcollide(grup_laser_pemain, grup_musuh, False, True)
        for list_musuh_terkena in tabrakan_laser_musuh.values():
            for musuh_yang_terkena in list_musuh_terkena:
                if musuh_yang_terkena.is_new_enemy: score += 50
                else: score += 10
                assets.suara_ledakan.play()
        
        if special_meter_count >= s.SPECIAL_METER_MAX: 
            player.activate_laser(semua_sprite, grup_laser_pemain)
            special_meter_count = 0 

        # --- Logika Respawn Musuh ---
        ufo_count = sum(1 for m in grup_musuh if not m.is_new_enemy)
        while ufo_count < max_ufo_enemies:
            new_musuh = Musuh(UFO_ENEMY_WIDTH, UFO_ENEMY_HEIGHT, current_enemy_speed, is_new_enemy=False)
            # ... (logika anti-tabrakan spawn Anda) ...
            grup_musuh.add(new_musuh)
            semua_sprite.add(new_musuh)
            ufo_count += 1
            
        shooter_count = sum(1 for m in grup_musuh if m.is_new_enemy)
        while shooter_count < max_shooter_enemies:
            w = s.ENEMY_IMAGE_SIZE[0] if assets.ENEMY_IMAGE else SHOOTER_ENEMY_WIDTH
            h = s.ENEMY_IMAGE_SIZE[1] if assets.ENEMY_IMAGE else SHOOTER_ENEMY_HEIGHT
            new_special_enemy = Musuh(w, h, current_enemy_speed, is_new_enemy=True)
            # ... (logika anti-tabrakan spawn Anda) ...
            grup_musuh.add(new_special_enemy)
            semua_sprite.add(new_special_enemy)
            shooter_count += 1

        # --- Cek Tabrakan Player ---
        tabrakan_player_musuh = pygame.sprite.spritecollide(player, grup_musuh, True)
        tabrakan_player_peluru_musuh = pygame.sprite.spritecollide(player, grup_peluru_musuh, True) 

        if tabrakan_player_musuh or tabrakan_player_peluru_musuh:
            if not player.shield_active:
                player.get_hit() 
                assets.suara_player_hit.play() 
        
        if player.lives <= 0:
            if player.laser_active:
                assets.suara_laser.stop() 
            print(f"Game Over! Skor Akhir: {score}")
            return "game_over", score 
        
        # --- 4. Render Game ---
        screen.fill(s.BLACK) 
        
        player_visible = True
        if player.is_invincible and player.invincible_timer % 10 < 5:
            player_visible = False
        
        if not player_visible:
            player.remove(semua_sprite)
        
        semua_sprite.draw(screen)
        
        if not player_visible:
            player.add(semua_sprite)

        if player.shield_active:
            pygame.draw.circle(screen, s.POWERUP_BLUE, player.rect.center, player.rect.width // 2 + 10, 3) 

        # --- UI (Skor dan Timer) ---
        score_text = assets.font.render(f"Skor: {score}", True, s.WHITE) 
        screen.blit(score_text, (10, 10))
        
        stage_text = assets.font_ui.render(f"Stage: {current_stage}", True, s.WHITE)
        screen.blit(stage_text, (10, 40))
        
        draw_lives(screen, 10, s.SCREEN_HEIGHT - 35, player.lives, player_mini_img)
        
        # UI Bar Spesial
        ui_y_pos = 70 
        BAR_LENGTH = 150
        BAR_HEIGHT = 15
        
        fill_percent = special_meter_count / s.SPECIAL_METER_MAX 
        if player.laser_active:
            fill_percent = player.laser_timer / player.laser_duration
            
        fill_length = fill_percent * BAR_LENGTH
        
        outline_rect = pygame.Rect(10, ui_y_pos, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(10, ui_y_pos, fill_length, BAR_HEIGHT)
        
        pygame.draw.rect(screen, (50, 50, 50), outline_rect) 
        pygame.draw.rect(screen, s.POWERUP_BLUE, fill_rect) 
        pygame.draw.rect(screen, s.WHITE, outline_rect, 2) 
        
        # UI (Timer Powerup di Kanan)
        ui_y_pos_kanan = 10
        
        if player.speed_powerup_collected:
            speed_val_text = f"Power: {player.speed_multiplier:.1f}x"
            speed_text_surf = assets.font_ui.render(speed_val_text, True, s.POWERUP_GREEN)
            screen.blit(speed_text_surf, (s.SCREEN_WIDTH - speed_text_surf.get_width() - 10, ui_y_pos_kanan))
            ui_y_pos_kanan += 30 
        if player.trishot_active:
            timer_text = assets.font_ui.render(f"Trishot: {player.trishot_timer // s.FPS + 1}s", True, s.POWERUP_ORANGE)
            screen.blit(timer_text, (s.SCREEN_WIDTH - timer_text.get_width() - 10, ui_y_pos_kanan))
            ui_y_pos_kanan += 30
        if player.shield_active:
            timer_text = assets.font_ui.render(f"Shield: {player.shield_timer // s.FPS + 1}s", True, s.POWERUP_BLUE)
            screen.blit(timer_text, (s.SCREEN_WIDTH - timer_text.get_width() - 10, ui_y_pos_kanan))
            ui_y_pos_kanan += 30
        if player.laser_active:
            timer_text = assets.font_ui.render(f"LASER: {player.laser_timer // s.FPS + 1}s", True, s.POWERUP_BLUE)
            screen.blit(timer_text, (s.SCREEN_WIDTH - timer_text.get_width() - 10, ui_y_pos_kanan))
            ui_y_pos_kanan += 30
        if player.speed_indicator_timer > 0:
            speed_text_overlay = assets.font_indicator.render("SPEED UP!", True, s.POWERUP_GREEN)
            screen.blit(speed_text_overlay, (s.SCREEN_WIDTH // 2 - speed_text_overlay.get_width() // 2, s.SCREEN_HEIGHT // 2))

        # [DIHAPUS] Blok 'else:' yang lama dihapus

        # --- 5. Update Layar (Selalu berjalan) ---
        pygame.display.flip()
        clock.tick(s.FPS)