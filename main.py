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

FONT = pygame.font.SysFont("microsoftyahei", 48)
UI_FONT = pygame.font.SysFont("microsoftyahei", 28)

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

board = [
    [RIGHT, None, None, UP, None],
    [None, DOWN, None, None, LEFT],
    [None, None, RIGHT, None, None],
    [UP, None, None, DOWN, None],
    [None, LEFT, None, None, RIGHT],
]

selected = None
mistakes = 0
MAX_MISTAKES = 3

# 碰撞动画状态
shake_cell = None       # (row, col)
shake_timer = 0         # 剩余帧数


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

    # 碰撞时左右晃动
    if shake_cell == (row, col):
        cx += 6 if (shake_timer // 3) % 2 == 0 else -6

    color = ARROW_COLOR
    if shake_cell == (row, col):
        color = ERROR_COLOR

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


def draw_ui():
    level_text = UI_FONT.render("关卡 1", True, TEXT_COLOR)
    arrow_text = UI_FONT.render(f"剩余箭头：{count_arrows()}", True, TEXT_COLOR)
    mistake_text = UI_FONT.render(
        f"失误：{mistakes} / {MAX_MISTAKES}", True, TEXT_COLOR)

    screen.blit(level_text, (30, 20))
    screen.blit(arrow_text, (30, 55))
    screen.blit(mistake_text, (WIDTH - 220, 20))


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
            cell = pos_to_cell(*event.pos)
            if cell is not None:
                r, c = cell
                if board[r][c] is not None:
                    selected = (r, c)
                    direction = board[r][c]
                    if can_fly_out(board, r, c, direction):
                        board[r][c] = None
                        selected = None
                    else:
                        mistakes += 1
                        shake_cell = (r, c)
                        shake_timer = 20
                else:
                    selected = None

    # 更新碰撞动画
    if shake_timer > 0:
        shake_timer -= 1
        if shake_timer == 0:
            shake_cell = None

    screen.fill(BG_COLOR)
    draw_board()
    draw_ui()
    pygame.display.flip()
    clock.tick(60)
