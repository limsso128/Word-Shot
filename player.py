import pygame
from settings import *

class Player:
    def __init__(self):
        try:
            # 이미지 파일 로드 시도
            self.image = pygame.image.load("font/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50)) # 이미지 크기를 정사각형으로 변경
        except FileNotFoundError:
            # 파일을 찾지 못하면 image를 None으로 설정
            self.image = None

        self.width = 50
        self.height = 20
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 5 # 플레이어 이동 속도를 7에서 5로 줄여 정밀 조준이 가능하도록 합니다.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        if self.image:
            # 이미지가 있으면 이미지를 그림
            screen.blit(self.image, self.rect)
        else:
            # 이미지가 없으면 파스텔톤 파란색 사각형을 그림
            pygame.draw.rect(screen, PASTEL_BLUE, self.rect)

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - self.width // 2
        self.rect.y = SCREEN_HEIGHT - 70

    def get_pos(self):
        return self.rect.midtop