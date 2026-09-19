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
SELECT_COLOR = (0, 200, 100)

# 字体
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

# 当前选中的格子
selected = None  # (row, col) 或 None


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

    # 如果被选中，画一个高亮框
    if selected == (row, col):
        rect = pygame.Rect(
            BOARD_X + col * CELL_SIZE + 4,
            BOARD_Y + row * CELL_SIZE + 4,
            CELL_SIZE - 8,
            CELL_SIZE - 8,
        )
        pygame.draw.rect(screen, SELECT_COLOR, rect, 3)

    text = FONT.render(symbol, True, ARROW_COLOR)
    rect = text.get_rect(center=(cx, cy))
    screen.blit(text, rect)


def draw_board():
    draw_grid()
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] is not None:
                draw_arrow(r, c, board[r][c])

def can_fly_out(board, row, col, direction):
    """判断 (row, col) 处的箭头能否飞出棋盘"""
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


def pos_to_cell(mx, my):
    """把鼠标坐标转成 (row, col)，不在棋盘内返回 None"""
    if not (BOARD_X <= mx < BOARD_X + BOARD_WIDTH):
        return None
    if not (BOARD_Y <= my < BOARD_Y + BOARD_HEIGHT):
        return None
    col = (mx - BOARD_X) // CELL_SIZE
    row = (my - BOARD_Y) // CELL_SIZE
    return row, col


# 主循环
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
                        print(f"({r},{c}) 方向 {direction} 可以飞出")
                    else:
                        print(f"({r},{c}) 方向 {direction} 被阻挡")
                else:
                    selected = None

    screen.fill(BG_COLOR)
    draw_board()
    pygame.display.flip()
    clock.tick(60)
