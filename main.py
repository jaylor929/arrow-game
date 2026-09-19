import pygame
import sys

pygame.init()

# 窗口设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("箭途")
clock = pygame.time.Clock()

# 颜色
BG_COLOR = (30, 30, 30)
GRID_COLOR = (80, 80, 80)
ARROW_COLOR = (255, 200, 0)
TEXT_COLOR = (255, 255, 255)

# 字体：用系统字体，支持箭头符号
FONT = pygame.font.SysFont("microsoftyahei", 48)

# 棋盘参数
ROWS, COLS = 5, 5
CELL_SIZE = 80
BOARD_WIDTH = COLS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE
BOARD_X = (WIDTH - BOARD_WIDTH) // 2
BOARD_Y = (HEIGHT - BOARD_HEIGHT) // 2

# 方向
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

# 方向对应符号
ARROW_SYMBOL = {
    UP: "↑",
    DOWN: "↓",
    LEFT: "←",
    RIGHT: "→",
}

# 测试用棋盘
board = [
    [RIGHT, None, None, UP, None],
    [None, DOWN, None, None, LEFT],
    [None, None, RIGHT, None, None],
    [UP, None, None, DOWN, None],
    [None, LEFT, None, None, RIGHT],
]


def draw_grid():
    """画棋盘网格"""
    for r in range(ROWS + 1):
        y = BOARD_Y + r * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR,
                         (BOARD_X, y), (BOARD_X + BOARD_WIDTH, y), 2)
    for c in range(COLS + 1):
        x = BOARD_X + c * CELL_SIZE
        pygame.draw.line(screen, GRID_COLOR,
                         (x, BOARD_Y), (x, BOARD_Y + BOARD_HEIGHT), 2)


def draw_arrow(row, col, direction):
    """在指定格子画一个符号箭头"""
    symbol = ARROW_SYMBOL.get(direction)
    if symbol is None:
        return

    text = FONT.render(symbol, True, ARROW_COLOR)
    cx = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
    cy = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2
    rect = text.get_rect(center=(cx, cy))
    screen.blit(text, rect)


def draw_board():
    """画整个棋盘和箭头"""
    draw_grid()
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] is not None:
                draw_arrow(r, c, board[r][c])


# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)
    draw_board()
    pygame.display.flip()
    clock.tick(60)
