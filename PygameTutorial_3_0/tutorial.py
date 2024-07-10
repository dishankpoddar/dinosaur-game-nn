import pygame
from pygame.locals import *
import os, random, sys, time

pygame.init()

# Predefined colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(128, 128, 128)
GREY_TRANSLUCENT = pygame.Color(128, 128, 128, a=0.5)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)

# FPS Defined
FPS = 60
FramePerSec = pygame.time.Clock()

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption('Tutorial Game')

# Game Variables
SPEED = 5
ENEMY_BOUNDARY = 40
SCORE = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load('AnimatedStreet.png')

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_sprite_url = 'Enemy.png'
        self.image = pygame.image.load(enemy_sprite_url)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(ENEMY_BOUNDARY, SCREEN_WIDTH - ENEMY_BOUNDARY), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if(self.rect.top > SCREEN_WIDTH):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(ENEMY_BOUNDARY, SCREEN_WIDTH - ENEMY_BOUNDARY), 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_sprite_url = 'Player.png'
        self.image = pygame.image.load(player_sprite_url)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Sprites Definition
P1 = Player()
E1 = Enemy()

# Enemy Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 3000)


pygame.mixer.init()
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1,0.0)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 1

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    DISPLAYSURF.blit(background, (0,0))
    # DISPLAYSURF.fill(WHITE)
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    # Moves and redraws all Sprites
    for entity in all_sprites:
        entity.draw(DISPLAYSURF)
        # DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,200))
        game_over_score = font.render(f'Score: {SCORE}', True, BLACK)
        DISPLAYSURF.blit(game_over_score, (30,260))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)