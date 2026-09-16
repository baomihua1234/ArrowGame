import pygame
import copy

from game_logic import (
    can_exit,
    is_level_clear,
    count_arrows,
    is_solvable
)

pygame.init()

# ---------- 基本设置 ----------
WIDTH, HEIGHT = 900, 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("一箭又一箭")

clock = pygame.time.Clock()


# ---------- 颜色 ----------
BG = (245, 245, 235)

CELL = (220, 235, 220)
CELL_HOVER = (205, 225, 205)

GRID = (75, 95, 75)

TEXT = (50, 65, 50)
ARROW = (40, 70, 45)

BUTTON = (90, 125, 90)
BUTTON_HOVER = (70, 105, 70)

WHITE = (255, 255, 255)

RED = (180, 65, 65)
GREEN = (55, 130, 75)


# ---------- 字体 ----------
title_font = pygame.font.SysFont(
    "Microsoft YaHei",
    48
)

large_font = pygame.font.SysFont(
    "Microsoft YaHei",
    38
)

ui_font = pygame.font.SysFont(
    "Microsoft YaHei",
    24
)

small_font = pygame.font.SysFont(
    "Microsoft YaHei",
    18
)

arrow_font = pygame.font.SysFont(
    "Segoe UI Symbol",
    44
)


# ---------- 箭头 ----------
ARROW_SYMBOLS = {
    "U": "↑",
    "D": "↓",
    "L": "←",
    "R": "→"
}


# ---------- 三个关卡 ----------
LEVELS = [

    {
        "name": "第 1 关",
        "mistakes": 3,

        "board": [
            ["L", "D", ".", "."],
            ["U", ".", "U", "."],
            ["R", "D", "U", "."],
            ["D", ".", ".", "."]
        ]
    },

    {
        "name": "第 2 关",
        "mistakes": 3,

        "board": [
            [".", "D", "R", "U", "R"],
            [".", ".", ".", ".", "R"],
            ["L", ".", "U", ".", "L"],
            [".", "D", ".", "U", "L"],
            ["R", ".", ".", ".", "."]
        ]
    },

    {
        "name": "第 3 关",
        "mistakes": 3,

        "board": [
            ["U", ".", ".", ".", ".", "."],
            [".", "R", "U", "R", ".", "D"],
            ["R", "D", "R", ".", ".", "."],
            ["R", "D", "U", "R", ".", "."],
            [".", "R", ".", ".", "D", "R"],
            [".", "L", "D", ".", ".", "D"]
        ]
    }
]



# ---------- 启动时检查关卡 ----------
for i, level in enumerate(LEVELS):

    if not is_solvable(
        level["board"]
    ):

        raise ValueError(
            f"第 {i + 1} 关无法通关"
        )


# ---------- 游戏状态 ----------
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_CLEAR = "clear"
STATE_GAME_OVER = "game_over"
STATE_ALL_CLEAR = "all_clear"

game_state = STATE_MENU

current_level = 0

board = []

mistakes_left = 3

status_message = ""

status_color = TEXT


# ---------- 加载关卡 ----------
def load_level(index):

    global board
    global mistakes_left
    global status_message
    global status_color

    board = copy.deepcopy(
        LEVELS[index]["board"]
    )

    mistakes_left = LEVELS[index][
        "mistakes"
    ]

    status_message = (
        "请选择一个可以飞出棋盘的箭头"
    )

    status_color = TEXT


# ---------- 棋盘布局 ----------
def get_board_layout():

    rows = len(board)
    cols = len(board[0])

    if rows <= 4:
        cell_size = 82

    elif rows == 5:
        cell_size = 72

    else:
        cell_size = 64

    board_width = (
        cols * cell_size
    )

    board_x = (
        WIDTH - board_width
    ) // 2

    board_y = 190

    return (
        board_x,
        board_y,
        cell_size
    )


# ---------- 按钮 ----------
def draw_button(rect, text):

    if rect.collidepoint(
        pygame.mouse.get_pos()
    ):
        color = BUTTON_HOVER

    else:
        color = BUTTON

    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=10
    )

    surface = ui_font.render(
        text,
        True,
        WHITE
    )

    text_rect = surface.get_rect(
        center=rect.center
    )

    screen.blit(
        surface,
        text_rect
    )


# ---------- 标题 ----------
def draw_title():

    surface = title_font.render(
        "一箭又一箭",
        True,
        TEXT
    )

    rect = surface.get_rect(
        center=(
            WIDTH // 2,
            65
        )
    )

    screen.blit(
        surface,
        rect
    )


# ---------- 画棋盘 ----------
def draw_board():

    board_x, board_y, cell_size = (
        get_board_layout()
    )

    mouse_pos = pygame.mouse.get_pos()

    for row in range(len(board)):

        for col in range(
            len(board[0])
        ):

            rect = pygame.Rect(

                board_x
                + col * cell_size,

                board_y
                + row * cell_size,

                cell_size,

                cell_size
            )

            if rect.collidepoint(
                mouse_pos
            ):
                color = CELL_HOVER

            else:
                color = CELL

            pygame.draw.rect(
                screen,
                color,
                rect
            )

            pygame.draw.rect(
                screen,
                GRID,
                rect,
                2
            )

            cell = board[row][col]

            if cell != ".":

                surface = (
                    arrow_font.render(
                        ARROW_SYMBOLS[cell],
                        True,
                        ARROW
                    )
                )

                arrow_rect = (
                    surface.get_rect(
                        center=rect.center
                    )
                )

                screen.blit(
                    surface,
                    arrow_rect
                )


# ---------- 显示游戏信息 ----------
def draw_game_info():

    level_surface = ui_font.render(
        LEVELS[current_level]["name"],
        True,
        TEXT
    )

    screen.blit(
        level_surface,
        (80, 125)
    )

    mistake_surface = ui_font.render(
        f"剩余失误机会：{mistakes_left}",
        True,
        TEXT
    )

    mistake_rect = (
        mistake_surface.get_rect(
            center=(
                WIDTH // 2,
                138
            )
        )
    )

    screen.blit(
        mistake_surface,
        mistake_rect
    )

    count_surface = ui_font.render(
        f"剩余箭头：{count_arrows(board)}",
        True,
        TEXT
    )

    count_rect = (
        count_surface.get_rect(
            topright=(
                820,
                125
            )
        )
    )

    screen.blit(
        count_surface,
        count_rect
    )

    message_surface = small_font.render(
        status_message,
        True,
        status_color
    )

    message_rect = (
        message_surface.get_rect(
            center=(
                WIDTH // 2,
                610
            )
        )
    )

    screen.blit(
        message_surface,
        message_rect
    )


# ---------- 结果遮罩 ----------
def draw_overlay(
    title,
    subtitle
):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            255,
            255,
            255,
            225
        )
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    title_surface = large_font.render(
        title,
        True,
        TEXT
    )

    title_rect = (
        title_surface.get_rect(
            center=(
                WIDTH // 2,
                270
            )
        )
    )

    screen.blit(
        title_surface,
        title_rect
    )

    subtitle_surface = ui_font.render(
        subtitle,
        True,
        TEXT
    )

    subtitle_rect = (
        subtitle_surface.get_rect(
            center=(
                WIDTH // 2,
                330
            )
        )
    )

    screen.blit(
        subtitle_surface,
        subtitle_rect
    )


# ---------- 按钮位置 ----------
start_button = pygame.Rect(
    330,
    450,
    240,
    60
)

menu_button = pygame.Rect(
    80,
    635,
    170,
    45
)

restart_button = pygame.Rect(
    650,
    635,
    170,
    45
)

center_button = pygame.Rect(
    330,
    390,
    240,
    60
)


# ---------- 加载第一关 ----------
load_level(0)


# ---------- 游戏循环 ----------
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        if (
            event.type
            == pygame.MOUSEBUTTONDOWN
            and
            event.button == 1
        ):

            mouse_x, mouse_y = (
                event.pos
            )


            # ----- 主菜单 -----
            if game_state == STATE_MENU:

                if start_button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    current_level = 0

                    load_level(
                        current_level
                    )

                    game_state = (
                        STATE_PLAYING
                    )


            # ----- 游戏中 -----
            elif (
                game_state
                ==
                STATE_PLAYING
            ):

                if menu_button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    game_state = (
                        STATE_MENU
                    )


                elif restart_button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    load_level(
                        current_level
                    )


                else:

                    (
                        board_x,
                        board_y,
                        cell_size
                    ) = get_board_layout()

                    col = (
                        mouse_x
                        - board_x
                    ) // cell_size

                    row = (
                        mouse_y
                        - board_y
                    ) // cell_size

                    rows = len(board)

                    cols = len(
                        board[0]
                    )

                    if (
                        0 <= row < rows
                        and
                        0 <= col < cols
                    ):

                        cell = (
                            board[row][col]
                        )


                        # 点击空格
                        if cell == ".":

                            status_message = (
                                "这里没有箭头"
                            )

                            status_color = TEXT


                        # 可以飞出
                        elif can_exit(
                            board,
                            row,
                            col
                        ):

                            board[row][col] = "."

                            status_message = (
                                "成功！箭头已飞出"
                            )

                            status_color = GREEN


                            if is_level_clear(
                                board
                            ):

                                if (
                                    current_level
                                    ==
                                    len(LEVELS) - 1
                                ):

                                    game_state = (
                                        STATE_ALL_CLEAR
                                    )

                                else:

                                    game_state = (
                                        STATE_CLEAR
                                    )


                        # 被阻挡
                        else:

                            mistakes_left -= 1

                            status_message = (
                                "前方有障碍！"
                                f"剩余 {mistakes_left} 次机会"
                            )

                            status_color = RED

                            if (
                                mistakes_left
                                <= 0
                            ):

                                game_state = (
                                    STATE_GAME_OVER
                                )


            # ----- 当前关通过 -----
            elif (
                game_state
                ==
                STATE_CLEAR
            ):

                if center_button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    current_level += 1

                    load_level(
                        current_level
                    )

                    game_state = (
                        STATE_PLAYING
                    )


            # ----- 游戏失败 -----
            elif (
                game_state
                ==
                STATE_GAME_OVER
            ):

                if center_button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    load_level(
                        current_level
                    )

                    game_state = (
                        STATE_PLAYING
                    )


            # ----- 全部通关 -----
            elif (
                game_state
                ==
                STATE_ALL_CLEAR
            ):

                if center_button.collidepoint(
                    mouse_x,
                    mouse_y
                ):

                    current_level = 0

                    load_level(
                        current_level
                    )

                    game_state = (
                        STATE_PLAYING
                    )


    # ---------- 绘制 ----------
    screen.fill(BG)


    # 主菜单
    if game_state == STATE_MENU:

        draw_title()

        heading = ui_font.render(
            "游戏规则",
            True,
            TEXT
        )

        heading_rect = heading.get_rect(
            center=(
                WIDTH // 2,
                190
            )
        )

        screen.blit(
            heading,
            heading_rect
        )

        rules = [

            "点击一个箭头。",

            "如果箭头前方直到棋盘边缘都没有其他箭头，它就可以飞出。",

            "如果前方存在其他箭头，则失误机会减少一次。",

            "清空全部箭头即可进入下一关。",

            "失误机会耗尽则挑战失败。"
        ]

        y = 245

        for rule in rules:

            surface = small_font.render(
                rule,
                True,
                TEXT
            )

            rule_rect = surface.get_rect(
                center=(
                    WIDTH // 2,
                    y
                )
            )

            screen.blit(
                surface,
                rule_rect
            )

            y += 38

        draw_button(
            start_button,
            "开始游戏"
        )


    # 游戏及结果页面
    else:

        draw_title()

        draw_game_info()

        draw_board()


        if (
            game_state
            ==
            STATE_PLAYING
        ):

            draw_button(
                menu_button,
                "返回菜单"
            )

            draw_button(
                restart_button,
                "重新开始"
            )


        elif (
            game_state
            ==
            STATE_CLEAR
        ):

            draw_overlay(
                "本关通过！",
                "继续挑战下一关"
            )

            draw_button(
                center_button,
                "下一关"
            )


        elif (
            game_state
            ==
            STATE_GAME_OVER
        ):

            draw_overlay(
                "挑战失败",
                "失误机会已经用完"
            )

            draw_button(
                center_button,
                "重新挑战"
            )


        elif (
            game_state
            ==
            STATE_ALL_CLEAR
        ):

            draw_overlay(
                "全部通关！",
                "恭喜完成全部三个关卡"
            )

            draw_button(
                center_button,
                "重新挑战"
            )


    pygame.display.flip()

    clock.tick(60)


pygame.quit()