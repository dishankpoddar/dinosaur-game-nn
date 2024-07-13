import pygame
from pygame.locals import *
import os, random, sys

pygame.init()

# Colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(128, 128, 128)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

# Game Clock Settings
FPS = 120
GameClock = pygame.time.Clock()

# Screen information
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption('Dinosaur Game')

# Sounds
death_sfx = pygame.mixer.Sound(os.path.join('assets', 'sfx', 'lose.mp3'))
points_sfx = pygame.mixer.Sound(os.path.join('assets', 'sfx', '100points.mp3'))
jump_sfx = pygame.mixer.Sound(os.path.join('assets', 'sfx', 'jump.mp3'))

# Game Variables
SPEED = round(SCREEN_WIDTH/250)
SPEED_DELTA = SPEED*0.0005
GRAVITY = round(SCREEN_HEIGHT/250)
SCORE = 0
OBSTACLE_TIMER = 0
OBSTACLE_COOLDOWN = 1000
OBSTACLE_COOLDOWN_DELTA = 0
GAME_OVER = False
OUTLINES = False

# Fonts
font = pygame.font.Font(os.path.join('assets', 'PressStart2P-Regular.ttf'), 24)

# Ground
ground = pygame.image.load(os.path.join('assets', 'ground.png'))
ground = pygame.transform.scale(ground, (SCREEN_WIDTH, 20))
GROUND_X = 0
GROUND_Y = 3*SCREEN_HEIGHT//4

# Cloud Dimensions
CLOUD_WIDTH = round(min(200, SCREEN_WIDTH//6), -1)
CLOUD_HEIGHT = round(min(80, SCREEN_HEIGHT//9), -1)
CLOUD_X = SCREEN_WIDTH + round(SCREEN_WIDTH//12, -1)
CLOUD_Y_MAX = round(SCREEN_HEIGHT//2, -1)
CLOUD_Y_MIN = round(SCREEN_HEIGHT//5, -1)

# Dinosaur Dimensions
RUNNING_DINO_WIDTH = round(min(80, SCREEN_WIDTH//16), -1)
RUNNING_DINO_HEIGHT = round(min(90, SCREEN_HEIGHT//8), -1)
DUCKING_DINO_WIDTH = round(min(110, SCREEN_WIDTH//12), -1)
DUCKING_DINO_HEIGHT = round(min(60, SCREEN_HEIGHT//12), -1)
DINO_X = round(min(200, SCREEN_WIDTH//6), -1)
RUNNING_DINO_Y = GROUND_Y - (RUNNING_DINO_HEIGHT - DUCKING_DINO_HEIGHT)//2
JUMPING_DINO_Y = RUNNING_DINO_Y - RUNNING_DINO_HEIGHT*2.75
DUCKING_DINO_Y = GROUND_Y + (RUNNING_DINO_HEIGHT - DUCKING_DINO_HEIGHT)//2

# Cactus Dimensions
CACTUS_WIDTH = round(min(80, SCREEN_WIDTH//16), -1)
CACTUS_HEIGHT = round(min(90, SCREEN_HEIGHT//8), -1)
CACTUS_X = SCREEN_WIDTH
CACTUS_Y = GROUND_Y - (SCREEN_HEIGHT)//48
CACTUS_SPAWN_CHANCE = 60

# Pterodactyl Dimensions
PTERO_WIDTH = round(min(80, SCREEN_WIDTH//16), -1)
PTERO_HEIGHT = round(min(90, SCREEN_HEIGHT//12), -1)
PTERO_X = SCREEN_WIDTH
PTERO_Y_HIGH = GROUND_Y - RUNNING_DINO_HEIGHT
PTERO_Y_MED = GROUND_Y - DUCKING_DINO_HEIGHT
PTERO_Y_LOW = GROUND_Y - (SCREEN_HEIGHT)//48
PTERO_SPAWN_CHANCE = 40

# Groups
cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()

# Object Classes
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__((cloud_group))
        cloud_sprite_url = os.path.join('assets', 'cloud.png')
        self.image = pygame.transform.scale(pygame.image.load(cloud_sprite_url), (CLOUD_WIDTH, CLOUD_HEIGHT))
        self.x_pos = CLOUD_X
        self.y_pos = random.randint(CLOUD_Y_MIN, CLOUD_Y_MAX)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__((obstacle_group))
        self.current_image = random.randint(0, len(self.sprites)-1)
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= SPEED
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        if OUTLINES:
            pygame.draw.rect(self.image, RED, [0, 0, self.image.get_width(), self.image.get_height()], 1)

class Cactus(Obstacle):
    def __init__(self):
        self.x_pos = CACTUS_X
        self.y_pos = CACTUS_Y
        self.sprites = [
            pygame.transform.scale(
                pygame.image.load(os.path.join('assets', 'cactus', f'cactus{i}.png')), (CACTUS_WIDTH, CACTUS_HEIGHT))
            for i in range(1, 7)
        ]
        super().__init__()

class Ptero(Obstacle):
    def __init__(self):
        self.x_pos = PTERO_X
        self.y_pos = random.choice([PTERO_Y_LOW, PTERO_Y_MED, PTERO_Y_HIGH])
        self.sprites = [
            pygame.transform.scale(
                pygame.image.load(os.path.join('assets', 'ptero', f'ptero{i}.png')), (PTERO_WIDTH, PTERO_HEIGHT))
            for i in range(1, 3)
        ]
        super().__init__()

    def update(self):
        self.animate()
        super().update()

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__((dino_group))

        self.running_sprites = [
            pygame.transform.scale(
                pygame.image.load(os.path.join('assets', 'dino', f'dino{i}.png')), (RUNNING_DINO_WIDTH, RUNNING_DINO_HEIGHT))
            for i in range(1, 3)
        ]
        self.ducking_sprites = [
            pygame.transform.scale(
                pygame.image.load(os.path.join('assets', 'dino', f'dinoDucking{i}.png')), (DUCKING_DINO_WIDTH, DUCKING_DINO_HEIGHT))
            for i in range(1, 3)
        ]

        self.sprites = self.running_sprites
        self.x_pos = DINO_X
        self.y_pos = RUNNING_DINO_Y
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.ducking = False

    def jump(self):
        jump_sfx.play()
        if self.rect.centery >= RUNNING_DINO_Y:
            self.rect.centery = JUMPING_DINO_Y

    def duck(self):
        self.ducking = True
        self.rect.centery = DUCKING_DINO_Y
        self.sprites = self.ducking_sprites

    def unduck(self):
        self.ducking = False
        self.rect.centery = RUNNING_DINO_Y
        self.sprites = self.running_sprites

    def apply_gravity(self):
        if self.rect.centery < RUNNING_DINO_Y:
            self.rect.centery += GRAVITY

    def update(self):
        self.animate()
        self.apply_gravity()
        if OUTLINES:
            pygame.draw.rect(self.image, RED, [0, 0, self.image.get_width(), self.image.get_height()], 1)

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 2:
            self.current_image = 0

        self.image = self.sprites[int(self.current_image)]

# Events
CLOUD_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CLOUD_EVENT, 3000)

# Objects
dinosaur = Dino()

# Game Loop
while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == CLOUD_EVENT:
            current_cloud = Cloud()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()
    
    if GAME_OVER:
        continue

    DISPLAYSURF.fill(WHITE)

    SCORE += 0.1
    player_score_surface = font.render(str(int(SCORE)), True, (BLACK))
    DISPLAYSURF.blit(player_score_surface, (SCREEN_WIDTH*0.9, 10))

    SPEED += SPEED_DELTA
    if int(SCORE) % 100 == 0 and int(SCORE) > 0:
        points_sfx.play()

    if pygame.time.get_ticks() - OBSTACLE_TIMER >= OBSTACLE_COOLDOWN + OBSTACLE_COOLDOWN_DELTA and SCORE > 20:
        if SCORE > 200:
            obstacle_class = random.choices([Cactus, Ptero], weights=[6, 4])[0]
        else:
            obstacle_class = Cactus
        new_obstacle = obstacle_class()
        OBSTACLE_TIMER = pygame.time.get_ticks()
        OBSTACLE_COOLDOWN_DELTA = random.randint(1, 40)

    # Draw Cloud
    cloud_group.update()
    cloud_group.draw(DISPLAYSURF)

    # Draw Obstacle
    obstacle_group.update()
    obstacle_group.draw(DISPLAYSURF)
    
    # Draw Dinosaur
    dino_group.update()
    dino_group.draw(DISPLAYSURF)

    # Draw Ground
    GROUND_X -= SPEED
    
    DISPLAYSURF.blit(ground, (GROUND_X, GROUND_Y))
    DISPLAYSURF.blit(ground, (GROUND_X + SCREEN_WIDTH, GROUND_Y))

    if GROUND_X <= -SCREEN_WIDTH:
        GROUND_X = 0

    # Collisions
    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        GAME_OVER = True
        death_sfx.play()
        
        game_over_text = font.render("G A M E   O V E R", True, BLACK)
        game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        game_over_screen_fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        game_over_screen_fade.fill(BLACK)
        game_over_screen_fade.set_alpha(160)
        DISPLAYSURF.blit(game_over_screen_fade, (0,0))
        DISPLAYSURF.blit(game_over_text, game_over_text_rect)

    pygame.display.update()
    GameClock.tick(FPS)
