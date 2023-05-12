
def checkFour(player):
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT):

            if verticalCheck(i, j, player):
                return True

            if horizontalCheck(i, j, player):
                return True

            if diagonalCheck(i, j, player):
                return True


def verticalCheck(row, col, player):
    # Boolean variable to check four in a row
    flag = False
    consecutive_count = 0
    for i in range(row, ROW_COUNT):
        if grid[i][col] == player:
            consecutive_count += 1
        else:
            break

    if consecutive_count >= 4:
        flag = True

    return flag


def horizontalCheck(row, col, player):
    # Boolean variable to check four in a row
    flag = False
    consecutive_count = 0

    for j in range(col, COLUMN_COUNT):
        if grid[row][j] == player:
            consecutive_count += 1
        else:
            break

    if consecutive_count >= 4:
        flag = True

    return flag