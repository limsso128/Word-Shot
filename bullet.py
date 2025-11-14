import pygame
from settings import *

class Bullet:
    def __init__(self, x, y):
        self.width = 20 # 총알의 폭을 10에서 20으로 늘려 맞추기 쉽게 합니다.
        self.height = 20
        self.speed = 15 # 총알 속도를 10에서 15로 높여 타격감을 높입니다.
        self.rect = pygame.Rect(x - self.width // 2, y, self.width, self.height)

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, PASTEL_YELLOW, self.rect)