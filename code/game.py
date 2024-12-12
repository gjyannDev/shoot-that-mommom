import pygame
import os
import time
import random
import button
import sys
import math

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Tutorial")

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
ENEMY_THREE = pygame.image.load(os.path.join("assets/characters", "enemy_3_skeleton.png")).convert_alpha()
ENEMY_ONE = pygame.transform.scale(pygame.image.load(os.path.join("assets/characters", "enemy_1_goblin.png")), (32, 40)).convert_alpha()
ENEMY_TWO = pygame.transform.scale(pygame.image.load(os.path.join("assets/characters", "enemy_2_armored.png")), (56, 44)).convert_alpha()
ENEMY_THREE = pygame.transform.scale(pygame.image.load(os.path.join("assets/characters", "enemy_3_skeleton.png")), (28, 56)).convert_alpha()

#Player player
CHARACTER_ONE = pygame.transform.scale(pygame.image.load(os.path.join("assets/characters", "hero_1_archer.png")), (64, 64)).convert_alpha()
CHARACTER_TWO = pygame.transform.scale(pygame.image.load(os.path.join("assets/characters", "hero_2_necro.png")), (64, 64)).convert_alpha()
CHARACTER_THREE = pygame.transform.scale(pygame.image.load(os.path.join("assets/characters", "hero_3_wizard.png")), (64, 64)).convert_alpha()

#hero attack 
WIZARD_ATTACK = pygame.transform.scale(pygame.image.load(os.path.join("assets/shoots_img", "fireball.png")), (56, 56)).convert_alpha()
ARCHER_ATTACK = pygame.transform.scale(pygame.image.load(os.path.join("assets/shoots_img", "arrow.png")), (56, 56)).convert_alpha()
NECRO_ATTACK = pygame.transform.scale(pygame.image.load(os.path.join("assets/shoots_img", "necromancer_ball.png")), (56, 56)).convert_alpha()

#Background
BG_ONE = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "bg_one.png")), (WIDTH, HEIGHT)).convert_alpha()
BG_TWO = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "bg_two.png")), (WIDTH, HEIGHT)).convert_alpha()
MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "menu_bg.png")), (WIDTH, HEIGHT)).convert_alpha()
OPTION_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "options_bg.png")), (WIDTH, HEIGHT)).convert_alpha()
SELECT_CHARACTER_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "select_character_bg.png")), (WIDTH, HEIGHT)).convert_alpha()
SELECT_BACKGROUND_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "select_background_bg.png")), (WIDTH, HEIGHT)).convert_alpha()

# Buttons
START_BTN = pygame.image.load(os.path.join("assets/buttons", "start_btn.png")).convert_alpha()
OPTIONS_BTN = pygame.image.load(os.path.join("assets/buttons", "options_btn.png")).convert_alpha()
QUIT_BTN = pygame.image.load(os.path.join("assets/buttons", "quit_btn.png")).convert_alpha()

CHAR_BTN = pygame.image.load(os.path.join("assets/buttons", "character_btn.png")).convert_alpha()
BG_BTN = pygame.image.load(os.path.join("assets/buttons", "background_btn.png")).convert_alpha()
BACK_BTN = pygame.image.load(os.path.join("assets/buttons", "back_btn.png")).convert_alpha()

start_btn = button.Button(350, 200, START_BTN, 0.8)
options_btn = button.Button(350, 275, OPTIONS_BTN, 0.8)
quit_btn = button.Button(350, 350, QUIT_BTN, 0.8)

character_btn = button.Button(25, 140, CHAR_BTN, 0.7)
background_btn = button.Button(25, 200, BG_BTN, 0.7)
back_btn = button.Button(25, 260, BACK_BTN, 0.7)

ACRCHER_CARD = pygame.image.load(os.path.join("assets/cards", "archer_card.png")).convert_alpha()
WIZARD_CARD = pygame.image.load(os.path.join("assets/cards", "wizard_card.png")).convert_alpha()
NECRO_CARD = pygame.image.load(os.path.join("assets/cards", "necromancer_card.png")).convert_alpha()

BG_ONE_CARD = pygame.image.load(os.path.join("assets/cards", "bg_1_card.png")).convert_alpha()
BG_TWO_CARD = pygame.image.load(os.path.join("assets/cards", "bg_2_card.png")).convert_alpha()

archer_card = button.Button(180, 200, ACRCHER_CARD, 0.8)
wizard_card = button.Button(380, 200, WIZARD_CARD, 0.8)
necro_card = button.Button(580, 200, NECRO_CARD, 0.8)

bg_one = button.Button(180, 200, BG_ONE_CARD, 0.8)
bg_two = button.Button(480, 200, BG_TWO_CARD, 0.8)

#Background Musics
menu_bg_music = pygame.mixer.Sound(os.path.join("assets/sounds", 'menu_bg_music.ogg'))
play_bg_music = pygame.mixer.Sound(os.path.join("assets/sounds", 'play_bg_music.ogg'))

arrow_sound = pygame.mixer.Sound(os.path.join("assets/sounds", 'arrow_sound_1.ogg'))
fireball_sound = pygame.mixer.Sound(os.path.join("assets/sounds", 'fireball_sound.ogg'))
necro_sound = pygame.mixer.Sound(os.path.join("assets/sounds", 'necro_power.ogg'))
monster_hurt = pygame.mixer.Sound(os.path.join("assets/sounds", 'retro_hurt.ogg'))

game_background = BG_ONE

bg_width = game_background.get_width()
bg_rect = game_background.get_rect()

scroll = 0
tiles = math.ceil(WIDTH  / bg_width) + 1
font_name = pygame.font.match_font('helvetica')
hero_attack = ARCHER_ATTACK
hero_character = CHARACTER_ONE
hero_attack_sound = arrow_sound
enemy_hurt = []
points = 0

def draw_text(screen, text, fontSize, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, fontSize)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

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

    #*ADD TWO TYPE OF DOUBLE ARROW SHOT OR SOMETHING 
    def shoot(self):
        if self.cool_down_counter == 0:
            # Create two lasers: one to the left and one to the right
            #?First type of shoot
            # laser_left = Laser(self.x + self.get_width() - 30, self.y + 50, self.laser_img)  
            # laser_right = Laser(self.x + self.get_width() - 30, self.y, self.laser_img)  
            
            #?Second type of shoot
            # laser_left = Laser(self.x + 10, self.y, self.laser_img) 
            # laser_right = Laser(self.x + self.get_width() - 30, self.y, self.laser_img)
            
            #?default type of shoot 
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            
            # self.lasers.append(laser_left)
            # self.lasers.append(laser_right)
           
            self.cool_down_counter = 1
        hero_attack_sound.play()
        hero_attack_sound.set_volume(1)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = hero_character
        self.laser_img = hero_attack
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.lives = 5
        self.life_image = pygame.transform.scale(pygame.image.load(os.path.join("assets/shoots_img", "heart_lives.png")), (96, 96)).convert_alpha()

    def move_lasers(self, vel, objs):
        global points
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        pygame.mixer.Sound(os.path.join("assets/sounds", 'retro_hurt.ogg')).play()
                        objs.remove(obj)
                        points += 24
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
        
    def healthbar(self, window):
        # Fixed position for the health bar at the top left of the screen
        bar_x = 10  # X-coordinate of the health bar
        bar_y = 10  # Y-coordinate of the health bar
        bar_width = 300  # Width of the health bar
        bar_height = 12 # Height of the health bar
        
        # Draw the red (background) bar
        pygame.draw.rect(window, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
        
        # Draw the green (health) bar proportional to the player's health
        current_health_width = bar_width * (self.health / self.max_health)
        pygame.draw.rect(window, (0, 255, 0), (bar_x, bar_y, current_health_width, bar_height), border_radius=4)

    def draw_lives(self, window):
        for i in range(self.lives):
            # Draw each life icon with spacing
            x = 10 + i * 50  # Adjust spacing between icons (40 pixels apart)
            y = 10  # Fixed y-position
            window.blit(self.life_image, (x, y))
            
    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
    
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
        # self.health = self.set_health()

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
    main_font = pygame.font.SysFont("comicsans", 28)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 7

    player = Player(0, 250)

    clock = pygame.time.Clock()
    
    menu_bg_music.stop()
    
    play_bg_music.play()
    play_bg_music.set_volume(0.3)
        
    lost = False
    lost_count = 0

    def redraw_window():
        global scroll, points
        
        #draw scrolling background
        for i in range(-1, tiles):
            SCREEN.blit(game_background, (i * bg_width + scroll, 0))
            bg_rect.x = i * bg_width + scroll

        #scroll background
        scroll += 1

        #reset scroll
        if scroll >= bg_width:
            scroll = 0
        # draw text
        player.draw_lives(SCREEN)
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        points_label = main_font.render(f"Points: {points}", 1, (255,255,255))

        SCREEN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        SCREEN.blit(points_label, (WIDTH - points_label.get_width() - 10, 40))

        for enemy in enemies:
            enemy.draw(SCREEN)

        player.draw(SCREEN)

        if lost:
            points = 0
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
            wave_length += 8
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
                player.lose_life()
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)
        
def characterMenu():
    global hero_character, hero_attack, hero_attack_sound
    run = True
    
    while run:
    
        SCREEN.blit(SELECT_CHARACTER_BG, (0,0))
        
        if archer_card.draw(SCREEN):
            hero_character = CHARACTER_ONE
            hero_attack = ARCHER_ATTACK
            hero_attack_sound = arrow_sound
            main_menu()
            
        if necro_card.draw(SCREEN):
            print('necro card')
            hero_character = CHARACTER_TWO
            hero_attack = NECRO_ATTACK
            hero_attack_sound = necro_sound
            main_menu()
            
        if wizard_card.draw(SCREEN):
            print('wizard card')
            hero_character = CHARACTER_THREE
            hero_attack = WIZARD_ATTACK
            hero_attack_sound = fireball_sound
            main_menu()
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
        
    pygame.quit()

def backgroundMenu():
    global game_background
    run = True
    
    while run:
    
        SCREEN.blit(SELECT_BACKGROUND_BG, (0,0))
        
        if bg_one.draw(SCREEN):
            game_background = BG_ONE
            main_menu()
            
        if bg_two.draw(SCREEN):
            game_background = BG_TWO
            main_menu()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
        
    pygame.quit()
        
def menu():
    run = True
    while run:
        
        SCREEN.blit(OPTION_BG, (0,0))
        
        if character_btn.draw(SCREEN):
            characterMenu()
        if background_btn.draw(SCREEN):
            backgroundMenu()
        if back_btn.draw(SCREEN):
            main_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
        
    pygame.quit()


def main_menu():
    run = True
    while run:
        
        SCREEN.blit(MENU_BG, (0,0))
        
        menu_bg_music.play()
        menu_bg_music.set_volume(0.2)
        
        if start_btn.draw(SCREEN):
            main()
        if options_btn.draw(SCREEN):
            menu()
        if quit_btn.draw(SCREEN):
            pygame.quit()
            sys.exit()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
        
    pygame.quit()

main_menu()