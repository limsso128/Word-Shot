import pygame
import random
from settings import *


class Enemy:
    def __init__(self, play_area_rect):  # 1. play_area_rect를 인자로 받음
        self.play_area_rect = play_area_rect  # 2. play_area_rect 저장
        try:
            self.image = pygame.image.load("font/enemy.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
        except FileNotFoundError:
            self.image = None

        self.width = 40
        self.height = 40

        # 3. play_area_rect의 너비 안에서 랜덤 X위치 지정
        self.x = random.randint(self.play_area_rect.left, self.play_area_rect.right - self.width)

        # 4. play_area_rect의 상단 바로 위에서 시작하도록 Y위치 지정
        self.y = self.play_area_rect.top - self.height

        self.speed = 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, PASTEL_PINK, self.rect)