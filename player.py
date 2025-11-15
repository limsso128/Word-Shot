import pygame
from settings import *


class Player:
    def __init__(self, screen_rect):  # 1. screen_rect를 인자로 받음
        self.screen_rect = screen_rect  # 2. screen_rect 저장
        try:
            # 이미지 파일 로드 시도
            self.image = pygame.image.load("font/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))  # 이미지 크기를 정사각형으로 변경
        except FileNotFoundError:
            # 파일을 찾지 못하면 image를 None으로 설정
            self.image = None

        self.width = 50
        self.height = 20

        # 3. screen_rect 기준으로 초기 위치 설정
        self.x = self.screen_rect.centerx - self.width // 2
        self.y = self.screen_rect.bottom - self.height - 10  # 화면 하단에 배치 (10px 여백)

        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # 4. (개선) 이미지가 있으면 rect를 이미지에 맞게 재설정
        if self.image:
            self.rect = self.image.get_rect(centerx=self.screen_rect.centerx,
                                            bottom=self.screen_rect.bottom - 10)
        else:
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            self.rect.centerx = self.screen_rect.centerx
            self.rect.bottom = self.screen_rect.bottom - 10

    def update(self):
        keys = pygame.key.get_pressed()

        # 5. screen_rect의 왼쪽 경계 확인
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        # 6. screen_rect의 오른쪽 경계 확인
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # 7. (안전장치) 경계를 벗어나지 않도록 고정
        if self.rect.left < self.screen_rect.left: # self.screen_rect.left는 0
            self.rect.left = self.screen_rect.left
        if self.rect.right > self.screen_rect.right: # self.screen_rect.right는 SCREEN_WIDTH
            self.rect.right = self.screen_rect.right

    def draw(self, screen):
        if self.image:
            # 이미지가 있으면 이미지를 그림
            screen.blit(self.image, self.rect)
        else:
            # 이미지가 없으면 파스텔톤 파란색 사각형을 그림
            pygame.draw.rect(screen, PASTEL_BLUE, self.rect)

    def reset(self, screen_rect):  # 8. screen_rect를 인자로 받음
        # 9. screen_rect 기준으로 위치 리셋
        self.rect.centerx = screen_rect.centerx
        self.rect.bottom = screen_rect.bottom - 10  # __init__과 동일하게

    def get_pos(self):
        return self.rect.midtop