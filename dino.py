import pygame
from pygame.locals import *
import os, random, sys

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

# Game Variables
SPEED = 5

# Object Classes
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        cloud_sprite_url = os.path.join('assets', 'cloud.png')
        CLOUD_WIDTH = min(200, SCREEN_WIDTH//6)
        CLOUD_HEIGHT = min(80, SCREEN_HEIGHT//9)
        self.image = pygame.transform.scale(pygame.image.load(cloud_sprite_url), (CLOUD_WIDTH, CLOUD_HEIGHT))
        CLOUD_Y_MAX = SCREEN_HEIGHT//2
        CLOUD_Y_MIN = SCREEN_HEIGHT//5
        self.x_pos = SCREEN_WIDTH + SCREEN_WIDTH//12
        self.y_pos = random.randint(CLOUD_Y_MIN, CLOUD_Y_MAX)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1

# Groups
cloud_group = pygame.sprite.Group()

# Events
CLOUD_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CLOUD_EVENT, 3000)

# Ground
ground = pygame.image.load(os.path.join('assets', 'ground.png'))
ground = pygame.transform.scale(ground, (SCREEN_WIDTH, 20))
GROUND_X = 0
GROUND_Y = 3*SCREEN_HEIGHT//4

pygame.init()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == CLOUD_EVENT:
            current_cloud = Cloud()
            cloud_group.add(current_cloud)
    
    DISPLAYSURF.fill(WHITE)

    # Draw Cloud
    cloud_group.update()
    cloud_group.draw(DISPLAYSURF)

    # Draw Ground
    GROUND_X -= SPEED
    
    DISPLAYSURF.blit(ground, (GROUND_X, GROUND_Y))
    DISPLAYSURF.blit(ground, (GROUND_X + SCREEN_WIDTH, GROUND_Y))

    if GROUND_X <= -SCREEN_WIDTH:
        GROUND_X = 0

    pygame.display.update()
    GameClock.tick(FPS)
