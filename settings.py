import pygame
import os

# !!! 중요 !!!
#
#    'frame.jpg'를 더 이상 사용하지 않으므로,
#    아래 값은 게임 윈도우의 전체 크기가 됩니다.
#    (기존 파일의 값을 그대로 유지합니다.)
#
# !!! 중요 !!!
SCREEN_WIDTH = 375
SCREEN_HEIGHT = 666

# -----------------------------------------------------------------

# 'PLAY_AREA_RECT'는 더 이상 사용하지 않으므로 삭제합니다.
# (x시작, y시작, 너비, 높이)
# PLAY_AREA_RECT = pygame.Rect(45, 230, 450, 470) # <--- 이 줄 삭제

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 파스텔톤 색상
PASTEL_PINK = (255, 204, 204) # 적
PASTEL_YELLOW = (255, 255, 204) # 총알
PASTEL_BLUE = (173, 216, 230) # 플레이어
MINT = (189, 252, 201) # 버튼

# BG_COLOR는 이제 사용하지 않습니다. (배경 이미지 사용)

# --- 새 GUI 위치 정의 (화면 전체 기준) ---
# 프레임이 없으므로 화면 기준으로 위치를 새로 잡습니다.
SCORE_POS = (SCREEN_WIDTH - 60, 30)     # 점수 (화면 우측 상단)
LIVES_POS = (60, 30)                    # 목숨 (화면 좌측 상단)

# 하단 입력창 및 사자성어 위치 (화면 하단 기준)
SAJA_MEANING_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)  # 사자성어 뜻 (중앙 정렬)
SAJA_WORD_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70)     # 사자성어 단어 (중앙 정렬)
INPUT_BOX_Y = SCREEN_HEIGHT - 30                            # 사용자 입력창 Y 위치 (하단)


# --- 폰트 설정 ---
pygame.init()

def find_font():
    """'font' 폴더에서 .ttf 또는 .otf 폰트 파일을 자동으로 찾습니다."""
    font_dir = 'font'
    if not os.path.exists(font_dir):
        return None
    for filename in os.listdir(font_dir):
        if filename.lower().endswith(('.ttf', '.otf')):
            return os.path.join(font_dir, filename)
    return None

FONT_PATH = find_font()

try:
    if FONT_PATH is None:
        raise FileNotFoundError # 폰트 파일이 없으면 에러 발생
    # 폰트 크기 (기존과 동일)
    FONT_LARGE = pygame.font.Font(FONT_PATH, 60)
    FONT_MEDIUM = pygame.font.Font(FONT_PATH, 30)
    FONT_SMALL = pygame.font.Font(FONT_PATH, 22)
    FONT_GUI = pygame.font.Font(FONT_PATH, 24) # 점수/목숨 표시용 폰트
    print(f"폰트 불러오기 성공: {FONT_PATH}")
except FileNotFoundError:
    print(f"경고: 'font' 폴더에 폰트 파일(.ttf, .otf)이 없습니다. 기본 폰트를 사용합니다 (한글 깨짐 발생).")
    FONT_LARGE = pygame.font.Font(None, 60)
    FONT_MEDIUM = pygame.font.Font(None, 30)
    FONT_SMALL = pygame.font.Font(None, 22)
    FONT_GUI = pygame.font.Font(None, 24)