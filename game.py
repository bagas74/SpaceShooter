import settings as s
import assets
import pygame
import random
import math
import sys
import os

from sprites import Player, Musuh, Peluru, PeluruMusuh, Powerup, Shockwave, PlayerLaser

try:
    player_mini_img = pygame.transform.scale(assets.PLAYER_IMAGE, (50, 45))
except: 
    player_mini_img = pygame.Surface((50, 45))
    player_mini_img.fill(s.POWERUP_BLUE)

def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 50 * i
        img_rect.y = y
        surface.blit(img, img_rect)

# --- run_game ---
def run_game(screen, clock):
    
    # --- Setup Variabel Game ---
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
    stage_xp = 0 # Variabel terpisah untuk stage
    special_meter_count = 0
    powerup_spawn_timer = 0
    
    banner_state = "hidden"
    banner_y_pos = -s.BANNER_HEIGHT
    banner_stay_timer = 0
    banner_text_surf = None 

    current_stage = 1
    max_ufo_enemies = 4 
    max_shooter_enemies = 0 
    current_enemy_speed = base_enemy_speed 

    # --- Variabel untuk Indikator Volume ---
    volume_indicator_timer = 0 
    volume_indicator_text = ""   

    # --- Logika musik untuk layar game ---
    if s.MUSIC_ENABLED:
        pygame.mixer.music.load(assets.MUSIC_GAME)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(s.MUSIC_VOLUME) 
    
    game_running = True
    while game_running:

        # --- 1. Event Handling Game ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", 0 
            
            if event.type == pygame.KEYDOWN:
                
                # --- Logika Tombol Mute 'M'] ---
                if event.key == pygame.K_m:
                    s.MUSIC_ENABLED = not s.MUSIC_ENABLED
                    if s.MUSIC_ENABLED:
                        pygame.mixer.music.load(assets.MUSIC_GAME)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(s.MUSIC_VOLUME)
                        volume_indicator_timer = 60 
                        volume_indicator_text = f"Volume: {int(s.MUSIC_VOLUME * 100)}%"
                    else:
                        pygame.mixer.music.stop()
                        volume_indicator_timer = 60 
                        volume_indicator_text = "Music: Off"
                
                # --- Logika Volume Up/Down ---
                elif event.key == pygame.K_EQUALS: # Tombol =/+
                    s.MUSIC_VOLUME = min(1.0, round(s.MUSIC_VOLUME + 0.1, 1))
                    pygame.mixer.music.set_volume(s.MUSIC_VOLUME)
                    s.MUSIC_ENABLED = True 
                    volume_indicator_timer = 60 
                    volume_indicator_text = f"Volume: {int(s.MUSIC_VOLUME * 100)}%"
                    
                elif event.key == pygame.K_MINUS: # Tombol -/_
                    s.MUSIC_VOLUME = max(0.0, round(s.MUSIC_VOLUME - 0.1, 1))
                    pygame.mixer.music.set_volume(s.MUSIC_VOLUME)
                    volume_indicator_timer = 60 
                    volume_indicator_text = f"Volume: {int(s.MUSIC_VOLUME * 100)}%"
                    
                    if s.MUSIC_VOLUME <= 0.0:
                        s.MUSIC_ENABLED = False
                        volume_indicator_text = "Music: Off" 
                        
                # --- Logika Tembak ---
                if banner_state == "hidden":
                    if event.key == pygame.K_SPACE:
                        if player.can_shoot(frame_count):
                            player.shoot(frame_count, grup_peluru_pemain, semua_sprite)

        # --- UPDATE SKOR & FRAME ---
        frame_count += 1
        if frame_count % 12 == 0:
            score += 1
            stage_xp += 1 
        
        # --- Update Timer Indikator ---
        if volume_indicator_timer > 0:
            volume_indicator_timer -= 1
            
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
        
        if banner_state == "hidden":
            for sprite in semua_sprite:
                sprite.update() 
                
                if isinstance(sprite, Musuh) and sprite.is_new_enemy:
                    if random.randrange(0, 100) < 2: 
                        peluru_baru = sprite.shoot() 
                        new_enemy_bullets.extend(peluru_baru)
        else:
             player.update()
        
        if new_enemy_bullets:
            semua_sprite.add(new_enemy_bullets)
            grup_peluru_musuh.add(new_enemy_bullets)
            
        player.update_timers()

        # --- Logika Stage ---
        new_stage = 1 + (stage_xp // 500) 
        
        if new_stage > current_stage and banner_state == "hidden":
            banner_state = "moving_down"
            banner_text_surf = assets.stage_clear_font.render(f"STAGE {new_stage}", True, s.WHITE)
            current_stage = new_stage
            print(f"Memicu Stage {current_stage}!") 
            
            current_enemy_speed = base_enemy_speed + (current_stage * 0.15) 
            max_ufo_enemies = min(2 + current_stage, 6) 
            max_shooter_enemies = current_stage // 3
            
            for musuh in grup_musuh:
                musuh.kill()
            for peluru in grup_peluru_musuh:
                peluru.kill()
            for peluru in grup_peluru_pemain:
                peluru.kill()
            for powerup in grup_powerup:
                powerup.kill()
        
        # --- Logika Animasi Banner ---
        if banner_state == "moving_down":
            banner_y_pos += s.BANNER_SPEED
            if banner_y_pos >= 0: 
                banner_y_pos = 0
                banner_state = "visible"
                banner_stay_timer = s.BANNER_STAY_TIME
        
        elif banner_state == "visible":
            banner_stay_timer -= 1
            if banner_stay_timer <= 0:
                banner_state = "moving_up"
        
        elif banner_state == "moving_up":
            banner_y_pos -= s.BANNER_SPEED
            if banner_y_pos <= -s.BANNER_HEIGHT: 
                banner_y_pos = -s.BANNER_HEIGHT
                banner_state = "hidden"
        
        for musuh in grup_musuh.sprites():
            if musuh.rect.top > s.SCREEN_HEIGHT: 
                musuh.kill()
        
        # --- Spawn Powerup ---
        if banner_state == "hidden":
            powerup_spawn_timer += 1
            if powerup_spawn_timer >= s.POWERUP_SPAWN_RATE: 
                powerup_spawn_timer = 0 
                tipe = random.choice(['T', 'P', 'S', '+0.5'])
                new_powerup = Powerup(tipe)
                grup_powerup.add(new_powerup)
                semua_sprite.add(new_powerup)

        # --- 3. Cek Tabrakan ---
        if banner_state == "hidden":
            tabrakan_peluru_musuh = pygame.sprite.groupcollide(grup_peluru_pemain, grup_musuh, True, True)
            for list_musuh_terkena in tabrakan_peluru_musuh.values():
                for musuh_yang_terkena in list_musuh_terkena:
                    if musuh_yang_terkena.is_new_enemy:
                        score += 50
                        stage_xp += 50
                    else:
                        score += 10
                        stage_xp += 10
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
                    if musuh_yang_terkena.is_new_enemy:
                        score += 25
                        stage_xp += 25
                    else:
                        score += 5
                        stage_xp += 5
                    assets.suara_ledakan.play()
                    if not player.laser_active: special_meter_count += 1
            
            pygame.sprite.groupcollide(grup_shockwave, grup_peluru_musuh, False, True)
            pygame.sprite.groupcollide(grup_laser_pemain, grup_peluru_musuh, False, True)
            
            tabrakan_laser_musuh = pygame.sprite.groupcollide(grup_laser_pemain, grup_musuh, False, True)
            for list_musuh_terkena in tabrakan_laser_musuh.values():
                for musuh_yang_terkena in list_musuh_terkena:
                    if musuh_yang_terkena.is_new_enemy:
                        score += 50
                        stage_xp += 50
                    else:
                        score += 10
                        stage_xp += 10
                    assets.suara_ledakan.play()
            
            if special_meter_count >= s.SPECIAL_METER_MAX: 
                player.activate_laser(semua_sprite, grup_laser_pemain)
                special_meter_count = 0 

            # --- Logika Respawn Musuh ---
            ufo_count = sum(1 for m in grup_musuh if not m.is_new_enemy)
            while ufo_count < max_ufo_enemies:
                new_musuh = Musuh(UFO_ENEMY_WIDTH, UFO_ENEMY_HEIGHT, current_enemy_speed, is_new_enemy=False)
                grup_musuh.add(new_musuh)
                semua_sprite.add(new_musuh)
                ufo_count += 1
                
            shooter_count = sum(1 for m in grup_musuh if m.is_new_enemy)
            while shooter_count < max_shooter_enemies:
                w = s.ENEMY_IMAGE_SIZE[0] if assets.ENEMY_IMAGE else SHOOTER_ENEMY_WIDTH
                h = s.ENEMY_IMAGE_SIZE[1] if assets.ENEMY_IMAGE else SHOOTER_ENEMY_HEIGHT
                new_special_enemy = Musuh(w, h, current_enemy_speed, is_new_enemy=True)
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
        
        # --- Cek Game Over (Di luar 'if hidden') ---
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
        
        draw_lives(screen, 30, s.SCREEN_HEIGHT - 55, player.lives, player_mini_img)
        
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
        
        # --- UI (Timer Powerup di Kanan) ---
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
        
        # Tampilkan "SPEED UP!"
        if player.speed_indicator_timer > 0:
            speed_text_overlay = assets.font_indicator.render("SPEED UP!", True, s.POWERUP_GREEN)
            screen.blit(speed_text_overlay, (s.SCREEN_WIDTH // 2 - speed_text_overlay.get_width() // 2, s.SCREEN_HEIGHT // 2))

        # Render Indikator Volume
        if volume_indicator_timer > 0:
            volume_text_overlay = assets.font_indicator.render(volume_indicator_text, True, s.WHITE)
            volume_rect = volume_text_overlay.get_rect(center=(s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2 + 40)) 
            screen.blit(volume_text_overlay, volume_rect)

        # Tampilkan Instruksi Volume
        instruction_text_str = "M: Mute | -/+ : Volume"
        instruction_surf = assets.font_ui.render(instruction_text_str, True, s.WHITE)
        instruction_surf.set_alpha(150) 
        instruction_rect = instruction_surf.get_rect(bottomright=(s.SCREEN_WIDTH - 10, s.SCREEN_HEIGHT - 10))
        screen.blit(instruction_surf, instruction_rect)

        # Render Banner (digambar paling akhir agar di atas UI)
        if banner_state != "hidden":
            banner_surf = pygame.Surface((s.SCREEN_WIDTH, s.BANNER_HEIGHT), pygame.SRCALPHA)
            banner_surf.fill((0, 0, 0, 180)) 
            screen.blit(banner_surf, (0, banner_y_pos))
            
            text_rect = banner_text_surf.get_rect(center=(s.SCREEN_WIDTH // 2, banner_y_pos + s.BANNER_HEIGHT // 2))
            screen.blit(banner_text_surf, text_rect)

        # --- 5. Update Layar (Selalu berjalan) ---
        pygame.display.flip()
        clock.tick(s.FPS)