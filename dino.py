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
jump_sfx = pygame.mixer.Sound(os.path.join('assets', 'sfx', 'jump.mp3'))
points_sfx = pygame.mixer.Sound(os.path.join('assets', 'sfx', '100points.mp3'))

# Game Variables
SPEED = round(SCREEN_WIDTH/250)
GRAVITY = round(SCREEN_HEIGHT/250)
SCORE = 0

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
CLOUD_Y_MAX = round(SCREEN_HEIGHT//2, -1)
CLOUD_Y_MIN = round(SCREEN_HEIGHT//5, -1)

# Dinosaur Dimensions
RUNNING_DINO_WIDTH = round(min(80, SCREEN_WIDTH//16), -1)
RUNNING_DINO_HEIGHT = round(min(90, SCREEN_HEIGHT//8), -1)
DUCKING_DINO_WIDTH = round(min(110, SCREEN_WIDTH//12), -1)
DUCKING_DINO_HEIGHT = round(min(60, SCREEN_HEIGHT//12), -1)
RUNNING_DINO_Y = GROUND_Y - (RUNNING_DINO_HEIGHT - DUCKING_DINO_HEIGHT)//2
JUMPING_DINO_Y = RUNNING_DINO_Y - RUNNING_DINO_HEIGHT*1.5
DUCKING_DINO_Y = GROUND_Y + (RUNNING_DINO_HEIGHT - DUCKING_DINO_HEIGHT)//2

# Object Classes
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        cloud_sprite_url = os.path.join('assets', 'cloud.png')
        self.image = pygame.transform.scale(pygame.image.load(cloud_sprite_url), (CLOUD_WIDTH, CLOUD_HEIGHT))
        self.x_pos = SCREEN_WIDTH + round(SCREEN_WIDTH//12, -1)
        self.y_pos = random.randint(CLOUD_Y_MIN, CLOUD_Y_MAX)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

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

        self.x_pos = round(min(200, SCREEN_WIDTH//6), -1)
        self.y_pos = RUNNING_DINO_Y
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.ducking = False

    def jump(self):
        jump_sfx.play()
        if self.rect.centery >= RUNNING_DINO_Y:
            self.rect.centery = JUMPING_DINO_Y

    def duck(self):
        self.ducking = True
        self.rect.centery = DUCKING_DINO_Y

    def unduck(self):
        self.ducking = False
        self.rect.centery = RUNNING_DINO_Y

    def apply_gravity(self):
        if self.rect.centery < RUNNING_DINO_Y:
            self.rect.centery += GRAVITY

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 2:
            self.current_image = 0

        if self.ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.image = self.running_sprites[int(self.current_image)]

# Groups
cloud_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()

# Events
CLOUD_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CLOUD_EVENT, 3000)

# Objects
dinosaur = Dino()
dino_group.add(dinosaur)

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
            cloud_group.add(current_cloud)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()
    
    DISPLAYSURF.fill(WHITE)

    SPEED += 0.0025
    if int(SCORE) % 100 == 0 and int(SCORE) > 0:
        points_sfx.play()

    SCORE += 0.1
    player_score_surface = font.render(
        str(int(SCORE)), True, (BLACK))
    DISPLAYSURF.blit(player_score_surface, (SCREEN_WIDTH*0.9, 10))

    # Draw Cloud
    cloud_group.update()
    cloud_group.draw(DISPLAYSURF)
    
    # Draw Dinosaur
    dino_group.update()
    dino_group.draw(DISPLAYSURF)

    # Draw Ground
    GROUND_X -= SPEED
    
    DISPLAYSURF.blit(ground, (GROUND_X, GROUND_Y))
    DISPLAYSURF.blit(ground, (GROUND_X + SCREEN_WIDTH, GROUND_Y))

    if GROUND_X <= -SCREEN_WIDTH:
        GROUND_X = 0

    pygame.display.update()
    GameClock.tick(FPS)
