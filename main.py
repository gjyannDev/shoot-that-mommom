import pygame
import os
import time
import random
import button
import sys
import math

pygame.font.init()

WIDTH, HEIGHT = 900, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")

# Load images
ENEMY_ONE = pygame.image.load(os.path.join("assets/characters", "enemy_1_goblin.png")).convert_alpha()
ENEMY_TWO = pygame.image.load(os.path.join("assets/characters", "enemy_2_armored.png")).convert_alpha()
ENEMY_THREE = pygame.image.load(os.path.join("assets/characters", "enemy_3_skeleton.png")).convert_alpha()

# Player player
CHARACTER_ONE = pygame.image.load(os.path.join("assets/characters", "hero_1_archer.png")).convert_alpha()
CHARACTER_TWO = pygame.image.load(os.path.join("assets/characters", "hero_2_necro.png")).convert_alpha()
CHARACTER_THREE = pygame.image.load(os.path.join("assets/characters", "hero_3_wizard.png")).convert_alpha()

# Lasers
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png")).convert_alpha()

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT)).convert_alpha()
MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "menu_bg.png")), (WIDTH, HEIGHT)).convert_alpha()

# Buttons
START_BTN = pygame.image.load(os.path.join("assets/buttons", "start_btn.png")).convert_alpha()
OPTIONS_BTN = pygame.image.load(os.path.join("assets/buttons", "options_btn.png")).convert_alpha()
QUIT_BTN = pygame.image.load(os.path.join("assets/buttons", "quit_btn.png")).convert_alpha()

start_btn = button.Button(350, 200, START_BTN, 0.8)
options_btn = button.Button(350, 275, OPTIONS_BTN, 0.8)
quit_btn = button.Button(350, 350, QUIT_BTN, 0.8)

bg_width = BG.get_width()
bg_rect = BG.get_rect()

scroll = 0
tiles = math.ceil(WIDTH  / bg_width) + 1

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  SCREEN.blit(img, (x, y))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.x -= vel  # Move left horizontally
    
    def off_screen(self, height):
        return not(0 <= self.x <= WIDTH)

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj, horizontal=False):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel, horizontal)  # Add horizontal movement
            if laser.off_screen(WIDTH if horizontal else HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = CHARACTER_ONE
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
        "enemyOne": (ENEMY_ONE),
        "enemyTwo": (ENEMY_TWO),
        "enemyThree": (ENEMY_THREE)
    }
    
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.x -= vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 7

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        global scroll
        #draw scrolling background
        for i in range(-1, tiles):
            SCREEN.blit(BG, (i * bg_width + scroll, 0))
            bg_rect.x = i * bg_width + scroll

        #scroll background
        scroll += 5

        #reset scroll
        if scroll >= bg_width:
            scroll = 0
            
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        SCREEN.blit(lives_label, (10, 10))
        SCREEN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(SCREEN)

        player.draw(SCREEN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            SCREEN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(
                    x=random.randint(WIDTH, WIDTH + 1000),  # Spawn off-screen to the right
                    y=random.randint(75, HEIGHT - 100),    # Random y position within screen height
                    color=random.choice(["enemyOne", "enemyTwo", "enemyThree"])
                )
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.x + enemy.get_width() < 0:  # Check if off-screen (left)
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        
        SCREEN.blit(MENU_BG, (0,0))
        
        if start_btn.draw(SCREEN):
            main()
        if options_btn.draw(SCREEN):
            print('options')
        if quit_btn.draw(SCREEN):
            pygame.quit()
            sys.exit()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
    pygame.quit()
    
    
main_menu()