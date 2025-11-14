import pygame
import random
from settings import *

class Enemy:
    def __init__(self):
        try:
            self.image = pygame.image.load("font/enemy.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
        except FileNotFoundError:
            self.image = None

        self.width = 40
        self.height = 40
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = 0
        self.speed = 1 # 속도를 2에서 1로 더 줄였습니다.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, PASTEL_PINK, self.rect)