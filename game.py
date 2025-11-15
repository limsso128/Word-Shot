import pygame
import random
import time
from settings import *
from player import Player
from enemy import Enemy
from bullet import Bullet


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # 1. 프레임 이미지 불러오기 (전체 배경)
        try:
            self.frame_image = pygame.image.load("img/frame.png").convert()
            self.frame_image = pygame.transform.scale(self.frame_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except FileNotFoundError:
            print("경고: 'img/frame.jpg' 파일을 찾을 수 없습니다. 검은색 배경으로 실행됩니다.")
            self.frame_image = None  # 프레임이 없어도 실행은 되도록

        # 2. 게임 영역 배경 이미지 불러오기 (프레임 안에 들어갈 배경)
        try:
            self.game_background_image = pygame.image.load("img/background.jpg").convert()
            # PLAY_AREA_RECT 크기에 맞게 스케일링
            self.game_background_image = pygame.transform.scale(self.game_background_image,
                                                                (PLAY_AREA_RECT.width, PLAY_AREA_RECT.height))
        except FileNotFoundError:
            print("경고: 'img/background.png' 파일을 찾을 수 없습니다. 게임 영역이 검은색으로 표시됩니다.")
            self.game_background_image = None  # 게임 배경이 없어도 실행

        # 키 반복 기능 활성화
        pygame.key.set_repeat(500, 30)

        pygame.display.set_caption("WordShot")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "START"

        self.saja_list = [
            {"word": "고진감래", "meaning": "고생 끝에 낙이 온다"},
            {"word": "동고동락", "meaning": "고통과 즐거움을 함께 한다"},
            {"word": "유비무환", "meaning": "미리 준비하면 근심이 없다"},
            {"word": "과유불급", "meaning": "지나친 것은 미치지 못한 것과 같다"},
            {"word": "다다익선", "meaning": "많으면 많을수록 좋다"},
            {"word": "일석이조", "meaning": "한 가지 일로 두 가지 이익을 얻음"},
            {"word": "자화자찬", "meaning": "자기가 한 일을 스스로 칭찬함"},
        ]

        # Player 객체 생성 시 PLAY_AREA_RECT 전달
        self.player = Player(PLAY_AREA_RECT)
        self.reset_game_variables()

    def reset_game_variables(self):
        # 리셋 시에도 PLAY_AREA_RECT 전달
        self.player.reset(PLAY_AREA_RECT)
        self.bullets = []
        self.enemies = []
        self.bullet_count = 0
        self.user_input = ""
        self.current_saja = random.choice(self.saja_list)
        self.score = 0
        self.correct_saja_list = []
        self.lives = 3  # 목숨 3개로 초기화
        self.last_enemy_spawn_time = time.time()
        self.enemy_spawn_interval = 4.0

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    self.handle_playing_keydown(event)
                elif event.type == pygame.TEXTINPUT:
                    char = event.text
                    if '\uac00' <= char <= '\ud7a3':
                        self.user_input += char

            elif self.game_state == "START":
                if event.type == pygame.MOUSEBUTTONDOWN and self.start_button_rect.collidepoint(event.pos):
                    self.reset_game_variables()
                    self.game_state = "PLAYING"
                    pygame.key.start_text_input()
            elif self.game_state == "GAME_OVER":
                if event.type == pygame.MOUSEBUTTONDOWN and self.restart_button_rect.collidepoint(event.pos):
                    self.game_state = "START"
                    pygame.key.stop_text_input()

    def handle_playing_keydown(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif event.key == pygame.K_RETURN:
            if self.user_input == self.current_saja["word"]:
                player_pos = self.player.get_pos()
                self.bullets.append(Bullet(player_pos[0], player_pos[1]))

                if self.current_saja["word"] not in self.correct_saja_list:
                    self.correct_saja_list.append(self.current_saja["word"])

                new_saja = random.choice(self.saja_list)
                while new_saja == self.current_saja:
                    new_saja = random.choice(self.saja_list)
                self.current_saja = new_saja
            self.user_input = ""

    def update(self):
        if self.game_state != "PLAYING":
            return

        # Player 업데이트 시에도 PLAY_AREA_RECT를 기준으로 하도록 (player.py에서 수정)
        self.player.update()

        for bullet in self.bullets:
            bullet.update()
            # 총알이 플레이 영역 상단을 벗어나면 제거
            if bullet.rect.bottom < PLAY_AREA_RECT.top:
                self.bullets.remove(bullet)

        current_time = time.time()
        if current_time - self.last_enemy_spawn_time > self.enemy_spawn_interval:
            # 적 생성 시 PLAY_AREA_RECT 전달
            self.enemies.append(Enemy(PLAY_AREA_RECT))
            self.last_enemy_spawn_time = current_time

            if self.score > 50 and self.enemy_spawn_interval > 2.0:
                self.enemy_spawn_interval -= 0.1
            elif self.score > 100 and self.enemy_spawn_interval > 1.5:
                self.enemy_spawn_interval -= 0.1
            elif self.score > 200 and self.enemy_spawn_interval > 1.0:
                self.enemy_spawn_interval -= 0.1
            self.enemy_spawn_interval = max(self.enemy_spawn_interval, 0.7)

        for enemy in self.enemies:
            enemy.update()

            # 적이 플레이 영역 하단을 벗어나면 제거 및 목숨 감소
            if enemy.rect.top > PLAY_AREA_RECT.bottom:
                self.enemies.remove(enemy)
                self.lives -= 1

        if self.lives <= 0:
            self.game_state = "GAME_OVER"
            pygame.key.stop_text_input()

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect.inflate(30, 30)):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break

    def draw(self):
        # 1. 기본 검은색 배경
        self.screen.fill(BLACK)

        # 2. 프레임 이미지 그리기 (game machine)
        if self.frame_image:
            self.screen.blit(self.frame_image, (0, 0))

        # 3. 게임 영역 배경 그리기 (background.png)
        if self.game_background_image:
            # PLAY_AREA_RECT의 위치에 게임 배경을 그림
            self.screen.blit(self.game_background_image, (PLAY_AREA_RECT.left, PLAY_AREA_RECT.top))
        else:
            # 게임 배경 이미지가 없으면, 해당 영역만 검은색으로 칠함
            pygame.draw.rect(self.screen, BLACK, PLAY_AREA_RECT)

        # 4. 현재 게임 상태에 맞는 화면 그리기 (게임 요소, UI 등)
        #    (이 함수들은 프레임과 게임배경 위에 덧그려짐)
        if self.game_state == "START":
            self.draw_start_screen()
        elif self.game_state == "PLAYING":
            self.draw_playing_screen()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over_screen()

        pygame.display.flip()

    def draw_start_screen(self):
        # 시작 화면 요소들을 PLAY_AREA_RECT 중앙에 배치
        title_text = FONT_LARGE.render("WordShot", True, WHITE)
        title_rect = title_text.get_rect(center=(PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.top + 150))
        self.screen.blit(title_text, title_rect)

        self.start_button_rect = pygame.Rect(PLAY_AREA_RECT.centerx - 100, PLAY_AREA_RECT.centery + 30, 200, 50)
        pygame.draw.rect(self.screen, MINT, self.start_button_rect)
        start_text = FONT_MEDIUM.render("게임 시작", True, WHITE)
        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(start_text, start_text_rect)

    def draw_playing_screen(self):
        # 게임 요소들은 PLAY_AREA 안에서만 그려짐 (코드는 동일)
        self.player.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # --- UI 그리기 (새로운 위치 기준) ---

        # 사자성어와 뜻 (화면 하단 중앙)
        saja_text = FONT_MEDIUM.render(self.current_saja['word'], True, WHITE)
        saja_rect = saja_text.get_rect(center=SAJA_WORD_POS)
        self.screen.blit(saja_text, saja_rect)

        meaning_text = FONT_SMALL.render(self.current_saja['meaning'], True, WHITE)
        meaning_rect = meaning_text.get_rect(center=SAJA_MEANING_POS)
        self.screen.blit(meaning_text, meaning_rect)

        # 입력창 (화면 하단 중앙)
        input_text = FONT_MEDIUM.render(self.user_input, True, PASTEL_YELLOW)
        underline_width = max(100, input_text.get_width() + 20)  # 최소 너비 보장
        underline_pos_start = (SCREEN_WIDTH // 2 - underline_width // 2, INPUT_BOX_Y + 5)
        underline_pos_end = (SCREEN_WIDTH // 2 + underline_width // 2, INPUT_BOX_Y + 5)
        pygame.draw.line(self.screen, PASTEL_YELLOW, underline_pos_start, underline_pos_end, 2)

        input_rect = input_text.get_rect(midbottom=(SCREEN_WIDTH // 2, INPUT_BOX_Y))
        self.screen.blit(input_text, input_rect)

        # 점수 (프레임 상단)
        score_text = FONT_GUI.render(f"{self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=SCORE_POS)
        self.screen.blit(score_text, score_rect)

        # 목숨 (프레임 상단)
        lives_text = FONT_GUI.render(f"LIVES: {self.lives}", True, WHITE)
        lives_rect = lives_text.get_rect(center=LIVES_POS)
        self.screen.blit(lives_text, lives_rect)

    def draw_game_over_screen(self):
        # 게임 오버 화면 요소들을 PLAY_AREA_RECT 중앙에 배치
        game_over_text = FONT_LARGE.render("게임 오버", True, PASTEL_PINK)
        game_over_rect = game_over_text.get_rect(center=(PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.top + 100))
        self.screen.blit(game_over_text, game_over_rect)

        final_score_text = FONT_MEDIUM.render(f"최종 점수: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.top + 200))
        self.screen.blit(final_score_text, final_score_rect)

        correct_list_text = FONT_SMALL.render("맞춘 사자성어:", True, PASTEL_YELLOW)
        correct_list_rect = correct_list_text.get_rect(center=(PLAY_AREA_RECT.centerx, PLAY_AREA_RECT.top + 260))
        self.screen.blit(correct_list_text, correct_list_rect)

        start_x = PLAY_AREA_RECT.left + 30
        current_x = start_x
        current_y = correct_list_rect.bottom + 20
        for i, word in enumerate(self.correct_saja_list):
            word_text = FONT_SMALL.render(word, True, WHITE)
            word_rect = word_text.get_rect(topleft=(current_x, current_y))

            if word_rect.right > PLAY_AREA_RECT.right - 30:
                current_y += word_rect.height + 5
                current_x = start_x
                word_rect.topleft = (current_x, current_y)

            self.screen.blit(word_text, word_rect)
            current_x = word_rect.right + 15

        self.restart_button_rect = pygame.Rect(PLAY_AREA_RECT.centerx - 100, PLAY_AREA_RECT.bottom - 70, 200, 50)
        pygame.draw.rect(self.screen, MINT, self.restart_button_rect)
        restart_text = FONT_MEDIUM.render("처음으로", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
        self.screen.blit(restart_text, restart_text_rect)