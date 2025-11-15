import pygame
import os

# !!! 중요 !!!
#
#    가지고 계신 'frame.jpg' 파일의
#    [실제 너비]와 [실제 높이]로 아래 두 값을 꼭 수정해주세요.
#    (현재는 540x960 이미지라고 가정하고 작성되었습니다.)
#
# !!! 중요 !!!
SCREEN_WIDTH = 375
SCREEN_HEIGHT = 666

# -----------------------------------------------------------------

# 'frame.jpg' 이미지 안에서 'background.png'가 그려질 영역이자,
# 실제 게임이 실행될 영역 (적, 플레이어, 총알이 움직이는 곳)
# 이 값은 (540, 960) 화면 크기를 기준으로 추정한 값입니다.
# 'frame.jpg'와 'background.png'에 맞게 이 값을 조절해야 합니다.
# (x시작, y시작, 너비, 높이)
PLAY_AREA_RECT = pygame.Rect(45, 230, 450, 470)

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
# gameframe.jpg의 기존 UI 위에 덮어씌울 위치 (540x960 기준)
SCORE_POS = (450, 140)     # 점수 (프레임의 '380' 숫자 위치)
LIVES_POS = (330, 140)     # 목숨 (프레임의 'Lv. 99+' 위치)

# 하단 입력창 및 사자성어 위치 (540x960 기준)
SAJA_MEANING_POS = (SCREEN_WIDTH // 2, 745)  # 사자성어 뜻 (중앙 정렬)
SAJA_WORD_POS = (SCREEN_WIDTH // 2, 785)     # 사자성어 단어 (중앙 정렬)
INPUT_BOX_Y = 830                            # 사용자 입력창 Y 위치 (하단)


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
    # 프레임에 맞게 폰트 크기 미세 조정
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