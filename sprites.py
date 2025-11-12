import pygame
import random
import math
import settings as s
import assets

# --- Fungsi Helper (Dipindahkan dari game.py) ---
# (Semua fungsi draw_... Anda tetap sama, tidak ada perubahan di sini)
def draw_star(surface, color, center, outer_radius, inner_radius, num_points):
    points = []
    for i in range(num_points * 2):
        angle = i * math.pi / num_points
        radius = outer_radius if i % 2 == 0 else inner_radius
        angle_adjusted = angle - (math.pi / 2)
        x = center[0] + radius * math.cos(angle_adjusted)
        y = center[1] + radius * math.sin(angle_adjusted)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, s.COLOR_JET_OUTLINE, points, 2)

def draw_regular_polygon(surface, color, center, radius, num_points, rotation=0, width=0):
    """Menggambar poligon reguler (seperti segi delapan)"""
    points = []
    for i in range(num_points):
        angle = (i * 2 * math.pi / num_points) + rotation
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, width)

def draw_enemy_ufo(surface, rect):
    cx, cy = rect.centerx, rect.centery
    w, h = rect.width, rect.height
    l, r, t, b = rect.left, rect.right, rect.top, rect.bottom
    pygame.draw.ellipse(surface, s.UFO_GREY_DARK, [l, t + int(h * 0.4), w, int(h * 0.4)])
    pygame.draw.ellipse(surface, s.UFO_OUTLINE, [l, t + int(h * 0.4), w, int(h * 0.4)], 2)
    pygame.draw.ellipse(surface, s.UFO_GREY_LIGHT, [l, t + int(h * 0.3), w, int(h * 0.3)])
    pygame.draw.ellipse(surface, s.UFO_OUTLINE, [l, t + int(h * 0.3), w, int(h * 0.3)], 2)
    dome_rect = pygame.Rect(cx - int(w * 0.3), t, int(w * 0.6), int(h * 0.6))
    pygame.draw.ellipse(surface, s.UFO_BLUE_DOME, dome_rect)
    pygame.draw.ellipse(surface, s.UFO_OUTLINE, dome_rect, 2)
    highlight_rect = pygame.Rect(cx - int(w * 0.2), t + int(h * 0.1), int(w * 0.4), int(h * 0.3))
    pygame.draw.ellipse(surface, s.UFO_BLUE_DOME_HIGHLIGHT, highlight_rect)
    light_radius = int(w * 0.06)
    pygame.draw.circle(surface, s.UFO_YELLOW_LIGHT, (int(cx - w * 0.35), int(t + h * 0.45)), light_radius)
    pygame.draw.circle(surface, s.UFO_OUTLINE, (int(cx - w * 0.35), int(t + h * 0.45)), light_radius, 1)
    pygame.draw.circle(surface, s.UFO_YELLOW_LIGHT, (cx, int(t + h * 0.45)), light_radius)
    pygame.draw.circle(surface, s.UFO_OUTLINE, (cx, int(t + h * 0.45)), light_radius, 1)
    pygame.draw.circle(surface, s.UFO_YELLOW_LIGHT, (int(cx + w * 0.35), int(t + h * 0.45)), light_radius)
    pygame.draw.circle(surface, s.UFO_OUTLINE, (int(cx + w * 0.35), int(t + h * 0.45)), light_radius, 1)
    foot_y_start = t + int(h * 0.8)
    foot_y_end = b
    pygame.draw.polygon(surface, s.UFO_RED_FEET, [(cx - int(w*0.25), foot_y_start), (cx - int(w*0.3), foot_y_end), (cx - int(w*0.2), foot_y_end)])
    pygame.draw.polygon(surface, s.UFO_RED_FEET, [(cx, foot_y_start), (cx - int(w*0.05), foot_y_end), (cx + int(w*0.05), foot_y_end)])
    pygame.draw.polygon(surface, s.UFO_RED_FEET, [(cx + int(w*0.25), foot_y_start), (cx + int(w*0.2), foot_y_end), (cx + int(w*0.3), foot_y_end)])

def draw_alien_ship_enemy(surface, rect):
    cx, cy = rect.centerx, rect.centery
    w, h = rect.width, rect.height
    l, r, t, b = rect.left, rect.right, rect.top, rect.bottom
    body_points = [
        (cx, t + h*0.1), (l + w*0.1, cy - h*0.2), (l, cy + h*0.1), (l + w*0.1, b - h*0.1),
        (cx, b), (r - w*0.1, b - h*0.1), (r, cy + h*0.1), (r - w*0.1, cy - h*0.2)
    ]
    pygame.draw.polygon(surface, s.ALIEN_BODY_DARK, body_points)
    pygame.draw.polygon(surface, s.ALIEN_OUTLINE, body_points, 2)
    core_rect = pygame.Rect(cx - w*0.25, cy - h*0.2, w*0.5, h*0.4)
    pygame.draw.ellipse(surface, s.ALIEN_BODY_LIGHT, core_rect)
    pygame.draw.ellipse(surface, s.ALIEN_OUTLINE, core_rect, 2)
    pygame.draw.circle(surface, s.ALIEN_EYE_YELLOW, (cx, cy), int(w*0.1))
    pygame.draw.circle(surface, s.ALIEN_OUTLINE, (cx, cy), int(w*0.1), 1)
    wing_width = w * 0.2
    wing_height = h * 0.15
    wing_left_points = [ (l + w*0.05, cy - wing_height/2), (l - w*0.05, cy), (l + w*0.05, cy + wing_height/2) ]
    pygame.draw.polygon(surface, s.ALIEN_ACCENT_GREEN, wing_left_points)
    pygame.draw.polygon(surface, s.ALIEN_OUTLINE, wing_left_points, 2)
    wing_right_points = [ (r - w*0.05, cy - wing_height/2), (r + w*0.05, cy), (r - w*0.05, cy + wing_height/2) ]
    pygame.draw.polygon(surface, s.ALIEN_ACCENT_GREEN, wing_right_points)
    pygame.draw.polygon(surface, s.ALIEN_OUTLINE, wing_right_points, 2)
    gun_radius = int(w * 0.08)
    gun_offset_x = w * 0.2
    gun_offset_y = h * 0.1
    pygame.draw.circle(surface, s.ALIEN_GUN_RED, (cx - gun_offset_x, b - gun_offset_y), gun_radius)
    pygame.draw.circle(surface, s.ALIEN_OUTLINE, (cx - gun_offset_x, b - gun_offset_y), gun_radius, 1)
    pygame.draw.circle(surface, s.ALIEN_GUN_RED, (cx + gun_offset_x, b - gun_offset_y), gun_radius)
    pygame.draw.circle(surface, s.ALIEN_OUTLINE, (cx + gun_offset_x, b - gun_offset_y), gun_radius, 1)

def draw_player_spaceship_default(surface, rect):
    cx, cy = rect.centerx, rect.centery
    w, h = rect.width, rect.height
    l, r, t, b = rect.left, rect.right, rect.top, rect.bottom
    body_points = [
        (cx, t), (cx + (w*0.08), t + (h*0.1)), (cx + (w*0.15), t + (h*0.3)),
        (cx + (w*0.15), b - (h*0.2)), (cx + (w*0.07), b - (h*0.05)), (cx - (w*0.07), b - (h*0.05)),
        (cx - (w*0.15), b - (h*0.2)), (cx - (w*0.15), t + (h*0.3)), (cx - (w*0.08), t + (h*0.1))
    ]
    pygame.draw.polygon(surface, s.COLOR_JET_BODY, body_points)
    pygame.draw.polygon(surface, s.COLOR_JET_OUTLINE, body_points, 2)
    wing_left_points = [
        (cx - (w*0.12), t + (h*0.3)), (l - (w*0.1), t + (h*0.6)),
        (l - (w*0.05), b - (h*0.25)), (cx - (w*0.12), b - (h*0.25))
    ]
    pygame.draw.polygon(surface, s.COLOR_JET_WING, wing_left_points)
    pygame.draw.polygon(surface, s.COLOR_JET_OUTLINE, wing_left_points, 2)
    wing_right_points = [
        (cx + (w*0.12), t + (h*0.3)), (r + (w*0.1), t + (h*0.6)),
        (r + (w*0.05), b - (h*0.25)), (cx + (w*0.12), b - (h*0.25))
    ]
    pygame.draw.polygon(surface, s.COLOR_JET_WING, wing_right_points)
    pygame.draw.polygon(surface, s.COLOR_JET_OUTLINE, wing_right_points, 2)
    y_attach_front = b - (h*0.35); y_attach_back = b - (h*0.23)
    x_attach = cx - (w*0.15); x_tip = cx - (w*0.30)
    tail_left_points = [ (x_attach, y_attach_front), (x_tip, y_attach_front), (x_tip, y_attach_back), (x_attach, y_attach_back) ]
    pygame.draw.polygon(surface, s.COLOR_JET_WING, tail_left_points)
    pygame.draw.polygon(surface, s.COLOR_JET_OUTLINE, tail_left_points, 2)
    x_attach_r = cx + (w*0.15); x_tip_r = cx + (w*0.30)
    tail_right_points = [ (x_attach_r, y_attach_front), (x_tip_r, y_attach_front), (x_tip_r, y_attach_back), (x_attach_r, y_attach_back) ]
    pygame.draw.polygon(surface, s.COLOR_JET_WING, tail_right_points)
    pygame.draw.polygon(surface, s.COLOR_JET_OUTLINE, tail_right_points, 2)
    pod_left_rect = pygame.Rect(cx - (w*0.38), t + (h*0.45), w*0.15, h*0.3)
    pygame.draw.rect(surface, s.COLOR_ENGINE_POD, pod_left_rect)
    pygame.draw.rect(surface, s.COLOR_JET_OUTLINE, pod_left_rect, 2)
    pod_right_rect = pygame.Rect(cx + (w*0.23), t + (h*0.45), w*0.15, h*0.3)
    pygame.draw.rect(surface, s.COLOR_ENGINE_POD, pod_right_rect)
    pygame.draw.rect(surface, s.COLOR_JET_OUTLINE, pod_right_rect, 2)
    fin_top = t + (h*0.05); fin_bottom = b - (h*0.10)
    fin_points = [ (cx - (w*0.05), fin_top), (cx + (w*0.05), fin_top), (cx + (w*0.08), fin_bottom), (cx - (w*0.08), fin_bottom) ]
    pygame.draw.polygon(surface, s.COLOR_JET_WING, fin_points)
    pygame.draw.polygon(surface, s.COLOR_JET_OUTLINE, fin_points, 2)
    cockpit_width = w * 0.25
    cockpit_height = h * 0.35
    cockpit_top_y = t + h*0.05 
    cockpit_bottom_y = cockpit_top_y + cockpit_height
    cockpit_left_x = cx - cockpit_width/2
    cockpit_right_x = cx + cockpit_width/2
    cockpit_points = [
        (cx - w*0.08, cockpit_top_y), (cx + w*0.08, cockpit_top_y), (cockpit_right_x, cockpit_top_y + h*0.15),
        (cockpit_right_x, cockpit_bottom_y), (cockpit_left_x, cockpit_bottom_y), (cockpit_left_x, cockpit_top_y + h*0.15)
    ]
    pygame.draw.polygon(surface, s.COLOR_COCKPIT_BLUE, cockpit_points)
    pygame.draw.polygon(surface, s.COLOR_JET_OUTLINE, cockpit_points, 2)
    shine_rect = pygame.Rect(cx - cockpit_width*0.25, cockpit_top_y + h*0.05, cockpit_width * 0.5, cockpit_height * 0.3)
    pygame.draw.ellipse(surface, s.COLOR_COCKPIT_HIGHLIGHT, shine_rect)


# --- Kelas Sprite: Peluru Musuh ---
class PeluruMusuh(pygame.sprite.Sprite):
    def __init__(self, center_x, bottom_y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(s.RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.top = bottom_y
        self.speed_y = 8

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > s.SCREEN_HEIGHT:
            self.kill()

# --- Kelas Sprite: Musuh ---
class Musuh(pygame.sprite.Sprite):
    def __init__(self, width, height, speed, is_new_enemy=False):
        super().__init__()
        self.is_new_enemy = is_new_enemy 
        
        if self.is_new_enemy and assets.ENEMY_IMAGE:
            self.image = assets.ENEMY_IMAGE.copy() 
            self.rect = self.image.get_rect()
        else: 
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            if self.is_new_enemy:
                draw_alien_ship_enemy(self.image, self.image.get_rect())
            else:
                draw_enemy_ufo(self.image, self.image.get_rect())

        self.rect.y = random.randrange(-100, -40)
        self.rect.x = random.randrange(s.SCREEN_WIDTH - self.rect.width) 
        
        if self.is_new_enemy:
            self.speed_y = 2
        else:
            self.speed_y = speed

    def update(self):
        self.rect.y += self.speed_y
        
        if self.rect.top > s.SCREEN_HEIGHT:
            self.kill()

    def shoot(self):
        peluru1 = PeluruMusuh(self.rect.centerx - self.rect.width * 0.2, self.rect.bottom)
        peluru2 = PeluruMusuh(self.rect.centerx + self.rect.width * 0.2, self.rect.bottom)
        assets.suara_tembak_musuh.play()
        return (peluru1, peluru2)

# --- Kelas Sprite: Player ---
class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        if assets.PLAYER_IMAGE:
            self.image = assets.PLAYER_IMAGE.copy()
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            draw_player_spaceship_default(self.image, self.image.get_rect()) 
            
        self.speed_multiplier = 1.0
        self.trishot_active = False
        self.trishot_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        self.fire_delay = 15
        self.last_shot_time = 0
        
        self.laser_active = False
        self.laser_timer = 0
        self.laser_duration = 5 * s.FPS 
        self.laser_sprite = None 
        
        self.speed_indicator_timer = 0
        
        self.speed_powerup_collected = False

        # [BARU] Tambahkan variabel untuk Nyawa dan Imunitas
        self.lives = s.PLAYER_STARTING_LIVES
        self.is_invincible = False
        self.invincible_timer = 0
        
    # PENTING: Player tidak memiliki fungsi update()
    # Ini bagus, karena update() hanya dipanggil saat banner_state == "hidden"
    # dan kita mengontrol timer secara terpisah via update_timers()

    def update_timers(self):
        if self.trishot_active:
            self.trishot_timer -= 1
            if self.trishot_timer <= 0:
                self.trishot_active = False

        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
                
        if self.laser_active:
            self.laser_timer -= 1
            if self.laser_timer <= 0:
                self.laser_active = False
                assets.suara_laser.stop()
                if self.laser_sprite:
                    self.laser_sprite.kill() 
                    self.laser_sprite = None
            elif self.laser_sprite:
                self.laser_sprite.update(self.rect) # Update posisi laser
                
        if self.speed_indicator_timer > 0: 
            self.speed_indicator_timer -= 1

        # [BARU] Tambahkan logika hitungan mundur imunitas
        if self.is_invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.is_invincible = False

    # [BARU] Tambahkan metode ini di dalam kelas Player
    def get_hit(self):
        # Hanya kurangi nyawa jika TIDAK sedang imun
        # Pengecekan 'shield_active' sudah ditangani di game.py
        if not self.is_invincible:
            self.lives -= 1
            self.is_invincible = True
            self.invincible_timer = s.PLAYER_INVINCIBILITY_DURATION
            # [OPSIONAL] mainkan suara hit (pastikan Anda menambahkannya ke assets.py)
            # assets.suara_player_hit.play()

    def can_shoot(self, current_frame):
        if self.laser_active:
            return False
        return current_frame - self.last_shot_time > self.fire_delay

    def shoot(self, current_frame, grup_peluru, grup_semua):
        self.last_shot_time = current_frame
        assets.suara_tembak.play()

        bullet_speed = -6 * self.speed_multiplier 

        if self.trishot_active:
            peluru1 = Peluru(self.rect.centerx, self.rect.top, bullet_speed)
            peluru2 = Peluru(self.rect.left + self.rect.width * 0.15, self.rect.centery + self.rect.height * 0.1, bullet_speed)
            peluru3 = Peluru(self.rect.right - self.rect.width * 0.15, self.rect.centery + self.rect.height * 0.1, bullet_speed)
            grup_peluru.add(peluru1, peluru2, peluru3)
            grup_semua.add(peluru1, peluru2, peluru3)
        else:
            peluru = Peluru(self.rect.centerx, self.rect.top, bullet_speed)
            grup_peluru.add(peluru)
            grup_semua.add(peluru)

    def activate_trishot(self):
        self.trishot_active = True
        self.trishot_timer = 5 * s.FPS
        assets.suara_powerup.play()

    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = 5 * s.FPS
        assets.suara_shield.play()

    def activate_speedup(self):
        self.speed_multiplier += 0.5
        self.speed_indicator_timer = 2 * s.FPS
        assets.suara_powerup.play()
        self.speed_powerup_collected = True
        
    def activate_laser(self, all_sprites_group, laser_group):
        if self.laser_active: return 
            
        print("LASER AKTIF!")
        self.laser_active = True
        self.laser_timer = self.laser_duration
        self.laser_sprite = PlayerLaser(self.rect) 
        all_sprites_group.add(self.laser_sprite)
        laser_group.add(self.laser_sprite)
        assets.suara_laser.play(loops=-1) 

# --- Kelas Sprite: Peluru ---
class Peluru(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(s.WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = speed_y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# --- Kelas Sprite: Powerup ---
class Powerup(pygame.sprite.Sprite):
    def __init__(self, tipe):
        super().__init__()
        self.type = tipe
        self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        center = (self.rect.width // 2, self.rect.height // 2)
        
        radius_luar = 16 
        radius_dalam = 10 
        rotasi_segidelapan = math.pi / 8

        if self.type == 'P':
            color, text = s.POWERUP_BLUE, "P"
            text_color = s.WHITE
        elif self.type == 'T':
            color, text = s.POWERUP_ORANGE, "T"
            text_color = s.WHITE
        elif self.type == 'S':
            color, text = s.POWERUP_RED, "S" 
            text_color = s.WHITE
        elif self.type == '+0.5':
            color, text = s.POWERUP_GREEN, "+0.5" 
            text_color = s.POWERUP_GREEN
        
        draw_regular_polygon(self.image, color, center, radius_luar, 8, rotasi_segidelapan)
        draw_regular_polygon(self.image, s.WHITE, center, radius_luar, 8, rotasi_segidelapan, width=2)
        draw_regular_polygon(self.image, s.WHITE, center, radius_dalam, 8, rotasi_segidelapan, width=1)
        
        if self.type == '+0.5':
            font_powerup_kecil = pygame.font.SysFont('arial', 18, bold=True)
            text_surf = font_powerup_kecil.render(text, True, text_color)
        else:
            text_surf = assets.font_powerup.render(text, True, text_color) 

        text_rect = text_surf.get_rect()
        text_rect.center = center
        self.image.blit(text_surf, text_rect)
        
        self.rect.x = random.randrange(s.SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = 2

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > s.SCREEN_HEIGHT:
            self.kill()

# --- Kelas Sprite: Shockwave ---
class Shockwave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((s.SCREEN_WIDTH, 25))
        self.image.fill(s.WHITE)
        self.image.set_alpha(180)
        self.rect = self.image.get_rect()
        self.rect.bottom = s.SCREEN_HEIGHT
        self.speed_y = -15

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# --- Kelas Sprite: Laser Spesial Player ---
class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.height = player_rect.top 
        self.image = pygame.Surface((20, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.midbottom = player_rect.midtop
        self.draw_laser() 

    def draw_laser(self):
        self.image.fill((0, 0, 0, 0)) 
        
        aura_width = random.randint(18, 22)
        aura_rect = pygame.Rect((self.image.get_width() - aura_width) // 2, 0, aura_width, self.height)
        pygame.draw.rect(self.image, s.POWERUP_BLUE, aura_rect, 0, border_radius=4)
        
        core_width = 8
        core_rect = pygame.Rect((self.image.get_width() - core_width) // 2, 0, core_width, self.height)
        pygame.draw.rect(self.image, s.WHITE, core_rect, 0, border_radius=2)
        
    def update(self, player_rect=None): 
        if player_rect is not None:
            self.height = player_rect.top
            self.image = pygame.Surface((20, self.height), pygame.SRCALPHA) 
            self.rect = self.image.get_rect() 
            self.rect.midbottom = player_rect.midtop
            self.draw_laser()