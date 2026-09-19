import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("箭途")
clock = pygame.time.Clock()

BG_COLOR = (30, 30, 30)
GRID_COLOR = (80, 80, 80)
ARROW_COLOR = (255, 200, 0)
TEXT_COLOR = (255, 255, 255)
SELECT_COLOR = (0, 200, 100)
ERROR_COLOR = (255, 80, 80)
BTN_COLOR = (60, 60, 60)
BTN_HOVER = (90, 90, 90)

FONT = pygame.font.SysFont("microsoftyahei", 48)
UI_FONT = pygame.font.SysFont("microsoftyahei", 28)
BIG_FONT = pygame.font.SysFont("microsoftyahei", 64)
TITLE_FONT = pygame.font.SysFont("microsoftyahei", 96)

ROWS, COLS = 5, 5
CELL_SIZE = 80
BOARD_WIDTH = COLS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE
BOARD_X = (WIDTH - BOARD_WIDTH) // 2
BOARD_Y = (HEIGHT - BOARD_HEIGHT) // 2 + 30

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
        [RIGHT, None, None, UP, None],
        [None, DOWN, None, None, LEFT],
        [None, None, RIGHT, None, None],
        [UP, None, None, DOWN, None],
        [None, LEFT, None, None, RIGHT],
    ],
    [
        [RIGHT, None, UP, None, None],
        [None, DOWN, None, None, LEFT],
        [None, None, RIGHT, None, None],
        [UP, None, None, DOWN, None],
        [None, LEFT, None, None, RIGHT],
    ],
    [
        [RIGHT, None, None, None, UP],
        [None, DOWN, None, LEFT, None],
        [None, None, RIGHT, None, None],
        [UP, None, None, DOWN, None],
        [None, LEFT, None, None, RIGHT],
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

START_BTN = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 60)
RESTART_BTN = pygame.Rect(WIDTH - 160, HEIGHT - 60, 130, 40)
NEXT_BTN = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 60)
MENU_BTN = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 60)


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


def draw_grid():
    for r in range(ROWS + 1):
        y = BOARD_Y + r * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR,
                         (BOARD_X, y), (BOARD_X + BOARD_WIDTH, y), 2)
    for c in range(COLS + 1):
        x = BOARD_X + c * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR,
                         (x, BOARD_Y), (x, BOARD_Y + BOARD_HEIGHT), 2)


def draw_arrow(row, col, direction):
    symbol = ARROW_SYMBOL.get(direction)
    if symbol is None:
        return

    cx = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
    cy = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

    if shake_cell == (row, col):
        cx += 6 if (shake_timer // 3) % 2 == 0 else -6

    color = ERROR_COLOR if shake_cell == (row, col) else ARROW_COLOR

    if selected == (row, col):
        rect = pygame.Rect(
            BOARD_X + col * CELL_SIZE + 4,
            BOARD_Y + row * CELL_SIZE + 4,
            CELL_SIZE - 8,
            CELL_SIZE - 8,
        )
        pygame.draw.rect(screen, SELECT_COLOR, rect, 3)

    text = FONT.render(symbol, True, color)
    rect = text.get_rect(center=(cx, cy))
    screen.blit(text, rect)


def draw_board():
    draw_grid()
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] is not None:
                draw_arrow(r, c, board[r][c])


def draw_button(rect, text):
    mouse_pos = pygame.mouse.get_pos()
    color = BTN_HOVER if rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=8)
    btn_text = UI_FONT.render(text, True, TEXT_COLOR)
    btn_rect = btn_text.get_rect(center=rect.center)
    screen.blit(btn_text, btn_rect)


def draw_menu():
    title = TITLE_FONT.render("箭途", True, ARROW_COLOR)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title, title_rect)

    sub = UI_FONT.render("点击箭头，让它飞出棋盘", True, TEXT_COLOR)
    sub_rect = sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
    screen.blit(sub, sub_rect)

    draw_button(START_BTN, "开始游戏")


def draw_ui():
    level_text = UI_FONT.render(f"关卡 {level_index + 1}", True, TEXT_COLOR)
    arrow_text = UI_FONT.render(f"剩余箭头：{count_arrows()}", True, TEXT_COLOR)
    mistake_text = UI_FONT.render(
        f"失误：{mistakes} / {MAX_MISTAKES}", True, TEXT_COLOR)

    screen.blit(level_text, (30, 20))
    screen.blit(arrow_text, (30, 55))
    screen.blit(mistake_text, (WIDTH - 220, 20))

    draw_button(RESTART_BTN, "重新开始")


def draw_overlay():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))


def draw_win_screen():
    draw_overlay()
    if level_index < len(LEVELS) - 1:
        title = BIG_FONT.render("通关！", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(title, title_rect)
        draw_button(NEXT_BTN, "下一关")
    else:
        title = BIG_FONT.render("全部通关！", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(title, title_rect)
        draw_button(NEXT_BTN, "重新开始")


def draw_lose_screen():
    draw_overlay()
    title = BIG_FONT.render("失败", True, ERROR_COLOR)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    screen.blit(title, title_rect)
    draw_button(MENU_BTN, "重新开始本关")


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
                    level_index = 0
                    load_level(level_index)
                continue

            if state == STATE_WIN:
                if NEXT_BTN.collidepoint(mx, my):
                    if level_index < len(LEVELS) - 1:
                        level_index += 1
                        load_level(level_index)
                    else:
                        level_index = 0
                        load_level(level_index)
                continue

            if state == STATE_LOSE:
                if MENU_BTN.collidepoint(mx, my):
                    load_level(level_index)
                continue

            if state == STATE_PLAYING:
                if RESTART_BTN.collidepoint(mx, my):
                    load_level(level_index)
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
