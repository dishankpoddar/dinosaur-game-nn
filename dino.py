import pygame
from pygame.locals import *
import os, sys

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
    
    DISPLAYSURF.fill(WHITE)

    # Draw Ground
    GROUND_X -= SPEED
    
    DISPLAYSURF.blit(ground, (GROUND_X, GROUND_Y))
    DISPLAYSURF.blit(ground, (GROUND_X + SCREEN_WIDTH, GROUND_Y))

    if GROUND_X <= -SCREEN_WIDTH:
        GROUND_X = 0

    pygame.display.update()
    GameClock.tick(FPS)
