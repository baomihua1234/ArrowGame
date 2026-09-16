import copy


# 箭头移动方向
DIRECTIONS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}


# 判断一个箭头能否飞出棋盘
def can_exit(board, row, col):

    rows = len(board)
    cols = len(board[0])

    # 防止坐标越界
    if not (
        0 <= row < rows
        and
        0 <= col < cols
    ):
        return False

    direction = board[row][col]

    # 空格或非法字符不是箭头
    if direction not in DIRECTIONS:
        return False

    dr, dc = DIRECTIONS[direction]

    # 从箭头前面的第一个格子开始检查
    r = row + dr
    c = col + dc

    while (
        0 <= r < rows
        and
        0 <= c < cols
    ):

        # 如果前方发现另一个箭头，则被阻挡
        if board[r][c] != ".":
            return False

        r += dr
        c += dc

    # 一直检查到棋盘外都没有障碍
    return True


# 判断关卡是否已经清空
def is_level_clear(board):

    for row in board:

        for cell in row:

            if cell != ".":
                return False

    return True


# 计算棋盘上剩余箭头数量
def count_arrows(board):

    count = 0

    for row in board:

        for cell in row:

            if cell != ".":
                count += 1

    return count


# 检查一个关卡理论上是否能够通关
def is_solvable(original_board):

    test_board = copy.deepcopy(
        original_board
    )

    while not is_level_clear(test_board):

        removed = False

        for row in range(len(test_board)):

            for col in range(
                len(test_board[0])
            ):

                if (
                    test_board[row][col] != "."
                    and
                    can_exit(
                        test_board,
                        row,
                        col
                    )
                ):

                    test_board[row][col] = "."

                    removed = True

                    break

            if removed:
                break

        # 一个箭头都无法移除，说明发生死锁
        if not removed:
            return False

    return True