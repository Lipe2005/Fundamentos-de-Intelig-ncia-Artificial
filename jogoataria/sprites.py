# pyrefly: ignore [missing-import]
import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.speed_x = PLAYER_SPEED
        
        self.rect.x += self.speed_x

        # Manter a nave dentro dos limites horizontais da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        # Cria um novo projétil a partir do centro da nave
        return Projectile(self.rect.centerx, self.rect.top)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = PROJECTILE_SPEED

    def update(self):
        self.rect.y += self.speed_y
        # Destrói o projétil se sair da tela, para economizar memória
        if self.rect.bottom < 0:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((ASTEROID_SIZE, ASTEROID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - ASTEROID_SIZE)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = speed

    def update(self):
        self.rect.y += self.speed_y
