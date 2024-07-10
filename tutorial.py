import pygame
from pygame.locals import *
import os, random, sys

pygame.init()

#Predefined colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(128, 128, 128)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

FPS = 60
FramePerSec = pygame.time.Clock()

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption('Tutorial Game')

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_sprite_url = os.path.join('PygameTutorial_3_0', 'Enemy.png')
        self.image = pygame.image.load(enemy_sprite_url)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, 370), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        if(self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_sprite_url = os.path.join('PygameTutorial_3_0', 'Player.png')
        self.image = pygame.image.load(player_sprite_url)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    
    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

P1 = Player()
E1 = Enemy()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    P1.update()
    E1.move()

    DISPLAYSURF.fill(WHITE)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)

    pygame.display.update()
    FramePerSec.tick(FPS)