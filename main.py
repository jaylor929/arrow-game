import pygame
import sys
import math
import array

pygame.init()
pygame.mixer.init()

def make_sound(freq, duration, volume=0.3):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    buf = array.array('h')
    for i in range(n_samples):
        t = i / sample_rate
        value = int(volume * 32767 * math.sin(2 * math.pi * freq * t))
        buf.append(value)
    return pygame.mixer.Sound(buffer=buf.tobytes())

SOUND_FLY = make_sound(880, 0.15)
SOUND_BLOCK = make_sound(220, 0.2)
SOUND_CLICK = make_sound(660, 0.08)


# 窗口
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("箭途")
clock = pygame.time.Clock()

MENU_BG = pygame.image.load("assets/menu_bg.jpg").convert()
MENU_BG = pygame.transform.scale(MENU_BG, (WIDTH, HEIGHT))

# 配色：布达佩斯大饭店复古梦幻
BG_COLOR = (247, 217, 217)        # 奶油粉
CARD_COLOR = (255, 248, 240)      # 奶油白
CARD_BORDER = (212, 175, 55)      # 金色
GRID_COLOR = (232, 160, 160)      # 酒店粉
TEXT_COLOR = (59, 42, 42)         # 深棕
SUBTEXT_COLOR = (120, 90, 90)     # 淡棕
BTN_COLOR = (232, 160, 160)       # 酒店粉
BTN_HOVER = (155, 44, 44)         # 酒红
BTN_TEXT = (255, 248, 240)        # 奶油白
SELECT_COLOR = (155, 44, 44)      # 酒红
ERROR_COLOR = (155, 44, 44)       # 酒红
OVERLAY_COLOR = (59, 42, 42, 160) # 深棕半透明

# 箭头方向颜色
ARROW_COLORS = {
    "up": (191, 227, 208),        # 薄荷绿
    "down": (155, 44, 44),        # 酒红
    "left": (212, 175, 55),       # 金色
    "right": (232, 160, 160),     # 酒店粉
}

# 字体
FONT_PATH = "C:/WINDOWS/FONTS/SIMSUN.TTC"

TITLE_FONT = pygame.font.Font(FONT_PATH, 108)
BIG_FONT = pygame.font.Font(FONT_PATH, 64)
UI_FONT = pygame.font.Font(FONT_PATH, 26)
SMALL_FONT = pygame.font.Font(FONT_PATH, 20)
FONT = pygame.font.Font(FONT_PATH, 48)
ARROW_FONT = pygame.font.SysFont("microsoftyahei", 48)
# 棋盘
ROWS, COLS = 7, 7
CELL_SIZE = 56
BOARD_WIDTH = COLS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE
BOARD_X = (WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 120
# 方向
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

ARROW_SYMBOL = {
    UP: "↑",
    DOWN: "↓",
    LEFT: "←",
    RIGHT: "→",
}

LEVELS = [
    [
        [RIGHT, None, None, None, None, UP, None],
        [None, None, None, DOWN, None, None, None],
        [None, LEFT, None, None, None, None, None],
        [None, None, None, None, RIGHT, None, None],
        [None, None, UP, None, None, None, None],
        [None, None, None, None, None, DOWN, None],
        [None, LEFT, None, None, None, None, None],
    ],
    [
        [RIGHT, None, None, UP, None, None, None],
        [None, DOWN, None, None, None, LEFT, None],
        [None, None, None, RIGHT, None, None, None],
        [None, None, UP, None, None, None, DOWN],
        [None, LEFT, None, None, DOWN, None, None],
        [None, None, None, RIGHT, None, None, None],
        [None, None, None, None, None, UP, None],
    ],
    [
        [RIGHT, None, None, None, UP, None, None],
        [None, DOWN, None, None, None, LEFT, None],
        [None, None, None, RIGHT, None, None, None],
        [None, None, UP, None, None, None, DOWN],
        [None, LEFT, None, None, DOWN, None, None],
        [None, None, None, RIGHT, None, None, None],
        [None, None, None, None, None, UP, None],
    ],
]

MAX_MISTAKES = 3

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_WIN = "win"
STATE_LOSE = "lose"

state = STATE_MENU
level_index = 0
board = [row[:] for row in LEVELS[level_index]]
selected = None
mistakes = 0
shake_cell = None
shake_timer = 0
flying_arrows = []

# 按钮
START_BTN = pygame.Rect(WIDTH // 2 - 120, 480, 240, 56)
RESTART_BTN = pygame.Rect(WIDTH - 190, HEIGHT - 70, 150, 46)
NEXT_BTN = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 20, 240, 56)
MENU_BTN = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 60, 240, 56)
EXIT_BTN = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 100, 240, 56)
BACK_BTN = pygame.Rect(40, HEIGHT - 70, 170, 46)

def load_level(index):
    global board, selected, mistakes, state, shake_cell, shake_timer
    board = [row[:] for row in LEVELS[index]]
    selected = None
    mistakes = 0
    state = STATE_PLAYING
    shake_cell = None
    shake_timer = 0


def count_arrows():
    return sum(1 for r in range(ROWS) for c in range(COLS) if board[r][c] is not None)


def draw_rounded_card(rect, radius=18, border=3):
    """画圆角卡片：阴影 + 填充 + 金边"""
    shadow = rect.move(6, 6)
    pygame.draw.rect(screen, (220, 190, 190), shadow, border_radius=radius)
    pygame.draw.rect(screen, CARD_COLOR, rect, border_radius=radius)
    pygame.draw.rect(screen, CARD_BORDER, rect, border, border_radius=radius)


def draw_button(rect, text, font=None):
    """复古圆角按钮"""
    if font is None:
        font = UI_FONT
    mouse_pos = pygame.mouse.get_pos()
    hover = rect.collidepoint(mouse_pos)
    color = BTN_HOVER if hover else BTN_COLOR

    shadow = rect.move(4, 4)
    pygame.draw.rect(screen, (220, 190, 190), shadow, border_radius=12)
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, CARD_BORDER, rect, 2, border_radius=12)

    btn_text = font.render(text, True, BTN_TEXT)
    btn_rect = btn_text.get_rect(center=rect.center)
    screen.blit(btn_text, btn_rect)

def draw_info_card(rect, label, value, value_color=TEXT_COLOR):
    """画一个信息卡片：小圆角 + 金边 + 标签 + 数值"""
    pygame.draw.rect(screen, CARD_COLOR, rect, border_radius=10)
    pygame.draw.rect(screen, CARD_BORDER, rect, 2, border_radius=10)

    label_surf = SMALL_FONT.render(label, True, SUBTEXT_COLOR)
    label_rect = label_surf.get_rect(topleft=(rect.x + 12, rect.y + 8))
    screen.blit(label_surf, label_rect)

    value_surf = UI_FONT.render(str(value), True, value_color)
    value_rect = value_surf.get_rect(topleft=(rect.x + 12, rect.y + 30))
    screen.blit(value_surf, value_rect)


def draw_grid():
    board_rect = pygame.Rect(BOARD_X - 10, BOARD_Y - 10,
                             BOARD_WIDTH + 20, BOARD_HEIGHT + 20)
    draw_rounded_card(board_rect, radius=14, border=3)

    for r in range(ROWS + 1):
        y = BOARD_Y + r * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR,
                         (BOARD_X, y), (BOARD_X + BOARD_WIDTH, y), 1)
    for c in range(COLS + 1):
        x = BOARD_X + c * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR,
                         (x, BOARD_Y), (x, BOARD_Y + BOARD_HEIGHT), 1)


def draw_arrow(row, col, direction):
    symbol = ARROW_SYMBOL.get(direction)
    if symbol is None:
        return

    cx = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
    cy = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

    if shake_cell == (row, col):
        cx += 5 if (shake_timer // 3) % 2 == 0 else -5

    color = ERROR_COLOR if shake_cell == (row, col) else ARROW_COLORS[direction]

    if selected == (row, col):
        rect = pygame.Rect(
            BOARD_X + col * CELL_SIZE + 3,
            BOARD_Y + row * CELL_SIZE + 3,
            CELL_SIZE - 6,
            CELL_SIZE - 6,
        )
        pygame.draw.rect(screen, SELECT_COLOR, rect, 3, border_radius=8)

    text = ARROW_FONT.render(symbol, True, color)
    rect = text.get_rect(center=(cx, cy))
    screen.blit(text, rect)


def draw_board():
    draw_grid()
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] is not None:
                draw_arrow(r, c, board[r][c])

    for arrow in flying_arrows:
        symbol = ARROW_SYMBOL.get(arrow["direction"])
        text = ARROW_FONT.render(symbol, True, ARROW_COLORS[arrow["direction"]])
        rect = text.get_rect(center=(arrow["x"], arrow["y"]))
        screen.blit(text, rect)


def draw_menu():
    screen.blit(MENU_BG, (0, 0))
    title = TITLE_FONT.render("箭途", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(WIDTH // 2, 150))
    screen.blit(title, title_rect)

    sub = UI_FONT.render("点击箭头，让它飞出棋盘", True, SUBTEXT_COLOR)
    sub_rect = sub.get_rect(center=(WIDTH // 2, 280))
    screen.blit(sub, sub_rect)

    poem_font = pygame.font.Font(FONT_PATH, 22)
    poem_font.set_italic(True)

    poem_text = poem_font.render(
        "“当你启程出发　但愿你的旅途漫长　充满奇迹　充满发现”",
        True,
        SUBTEXT_COLOR
    )
    poem_rect = poem_text.get_rect(center=(WIDTH // 2, 340))
    screen.blit(poem_text, poem_rect)
    draw_button(START_BTN, "开始游戏")


def draw_ui():
    # 左边两个信息卡片
    level_card = pygame.Rect(40, 25, 150, 70)
    arrow_card = pygame.Rect(210, 25, 190, 70)

    draw_info_card(level_card, "关卡", level_index + 1)
    draw_info_card(arrow_card, "剩余箭头", count_arrows())

    # 右上角失误卡片
    mistake_card = pygame.Rect(WIDTH - 200, 25, 160, 70)
    draw_info_card(mistake_card, "失误", f"{mistakes} / {MAX_MISTAKES}",
                   value_color=ERROR_COLOR)

    draw_button(RESTART_BTN, "重新开始")
    draw_button(BACK_BTN, "返回主界面")

def draw_overlay():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    screen.blit(overlay, (0, 0))


def draw_center_card(title, btn_text, btn_rect, title_color=TEXT_COLOR):
    card = pygame.Rect(WIDTH // 2 - 260, HEIGHT // 2 - 180, 520, 360)
    draw_rounded_card(card, radius=20, border=4)

    title_surf = BIG_FONT.render(title, True, title_color)
    title_rect = title_surf.get_rect(center=(WIDTH // 2 + 20, HEIGHT // 2 - 80))
    screen.blit(title_surf, title_rect)

    draw_button(btn_rect, btn_text)


def draw_win_screen():
    draw_overlay()
    if level_index < len(LEVELS) - 1:
        draw_center_card("通关！", "下一关", NEXT_BTN)
    else:
        draw_center_card("恭喜，全部通关！", "重新开始", NEXT_BTN)
        draw_button(EXIT_BTN, "退出")


def draw_lose_screen():
    draw_overlay()
    draw_center_card("失败！", "重新开始本关", MENU_BTN, title_color=ERROR_COLOR)


def pos_to_cell(mx, my):
    if not (BOARD_X <= mx < BOARD_X + BOARD_WIDTH):
        return None
    if not (BOARD_Y <= my < BOARD_Y + BOARD_HEIGHT):
        return None
    col = (mx - BOARD_X) // CELL_SIZE
    row = (my - BOARD_Y) // CELL_SIZE
    return row, col


def can_fly_out(board, row, col, direction):
    if direction == UP:
        for r in range(row - 1, -1, -1):
            if board[r][col] is not None:
                return False
        return True
    if direction == DOWN:
        for r in range(row + 1, ROWS):
            if board[r][col] is not None:
                return False
        return True
    if direction == LEFT:
        for c in range(col - 1, -1, -1):
            if board[row][c] is not None:
                return False
        return True
    if direction == RIGHT:
        for c in range(col + 1, COLS):
            if board[row][c] is not None:
                return False
        return True
    return False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if state == STATE_MENU:
                if START_BTN.collidepoint(mx, my):
                    SOUND_CLICK.play()
                    level_index = 0
                    load_level(level_index)
                continue

            if state == STATE_WIN:
                if NEXT_BTN.collidepoint(mx, my):
                    SOUND_CLICK.play()
                    if level_index < len(LEVELS) - 1:
                        level_index += 1
                        load_level(level_index)
                    else:
                        level_index = 0
                        load_level(level_index)
                if level_index == len(LEVELS) - 1 and EXIT_BTN.collidepoint(mx, my):
                    SOUND_CLICK.play()
                    pygame.quit()
                    sys.exit()
                continue

            if state == STATE_LOSE:
                if MENU_BTN.collidepoint(mx, my):
                    SOUND_CLICK.play()
                    load_level(level_index)
                continue

            if state == STATE_PLAYING:
                if RESTART_BTN.collidepoint(mx, my):
                    SOUND_CLICK.play()
                    load_level(level_index)
                    continue
                if BACK_BTN.collidepoint(mx, my):
                    SOUND_CLICK.play()
                    state = STATE_MENU
                    continue

                cell = pos_to_cell(mx, my)
                if cell is not None:
                    r, c = cell
                    if board[r][c] is not None:
                        selected = (r, c)
                        direction = board[r][c]
                        if can_fly_out(board, r, c, direction):
                            board[r][c] = None
                            selected = None
                            SOUND_FLY.play()

                            cx = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
                            cy = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2

                            speed = 12
                            dx, dy = 0, 0
                            if direction == UP:
                                dy = -speed
                            elif direction == DOWN:
                                dy = speed
                            elif direction == LEFT:
                                dx = -speed
                            elif direction == RIGHT:
                                dx = speed

                            flying_arrows.append({
                                "direction": direction,
                                "x": cx,
                                "y": cy,
                                "dx": dx,
                                "dy": dy,
                            })

                            if count_arrows() == 0:
                                state = STATE_WIN
                        else:
                            mistakes += 1
                            shake_cell = (r, c)
                            shake_timer = 20
                            if mistakes >= MAX_MISTAKES:
                                state = STATE_LOSE
                    else:
                        selected = None

    if shake_timer > 0:
        shake_timer -= 1
        if shake_timer == 0:
            shake_cell = None

    # 更新飞出箭头
    for arrow in flying_arrows[:]:
        arrow["x"] += arrow["dx"]
        arrow["y"] += arrow["dy"]
        if (arrow["x"] < -100 or arrow["x"] > WIDTH + 100 or
                arrow["y"] < -100 or arrow["y"] > HEIGHT + 100):
            flying_arrows.remove(arrow)

    screen.fill(BG_COLOR)

    if state == STATE_MENU:
        draw_menu()
    else:
        draw_board()
        draw_ui()
        if state == STATE_WIN:
            draw_win_screen()
        elif state == STATE_LOSE:
            draw_lose_screen()

    pygame.display.flip()
    clock.tick(60)

