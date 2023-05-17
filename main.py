
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



def diagonalCheck(row, col, player):
    rightSlope = False
    leftSlope = False

    # check for diagonals with right slope(POSITIVE SLOPE)

    consecutive_count = 0
    j = col
    for i in range(row, 6):
        if j > 6:
            break
        elif grid[i][j] == player:
            consecutive_count += 1
        else:
            break
        j += 1  # increment column when row is incremented

    if consecutive_count >= 4:
        rightSlope = True

    # check for diagonals with left slope(NEGATIVE SLOPE)
    consecutive_count = 0
    j = col
    for i in range(row, -1, -1):
        if j > 6:
            break
        elif grid[i][j] == player:
            consecutive_count += 1
        else:
            break
        j += 1  # increment column when row is decremented

    if consecutive_count >= 4:
        leftSlope = True

    slope = rightSlope or leftSlope
    return slope



def count_streak(state, player, streak):
    count = 0
    # for each piece in the board...
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT):
            if state[i][j] == player:
                # check if a vertical streak starts at (i, j)
                count += vertical_streak(i, j, state, streak)

                # check if a horizontal four-in-a-row starts at (i, j)
                count += horizontal_streak(i, j, state, streak)

                # check if a diagonal (either way) four-in-a-row starts at (i, j)
                count += diagonal_streak(i, j, state, streak)
    # return the sum of streaks of length 'streak'
    return count


def vertical_streak(row, col, state, streak):
    # check n streaks beside each other vertically and return 1 if the count is found and 0 if not.
    consecutive_count = 0
    player = state[row][col]

    for i in range(row, ROW_COUNT):
        if state[i][col] == player:
            consecutive_count += 1
        else:
            break

    return 1 if consecutive_count >= streak else 0


def horizontal_streak(row, col, state, streak):
    # check n streaks beside each other horizontally and return 1 if the count is found and 0 if not.
    consecutive_count = 0
    player = state[row][col]

    for j in range(col, COLUMN_COUNT):
        if state[row][j] == player:
            consecutive_count += 1
        else:
            break

    return 1 if consecutive_count >= streak else 0


def diagonal_streak(row, col, state, streak):
    # check n streaks beside each other diagonally and return 1 if the count is found and 0 if not.
    player = state[row][col]
    total = 0
    # check for diagonals with positive slope
    consecutive_count = 0
    j = col
    for i in range(row, ROW_COUNT):
        if j > COLUMN_COUNT - 1:
            break
        elif state[i][j] == player:
            consecutive_count += 1
        else:
            break
        j += 1  # increment column when row is incremented

    if consecutive_count >= streak:
        total += 1

    # check for diagonals with negative slope
    consecutive_count = 0
    j = col
    for i in range(row, -1, -1):
        if j > COLUMN_COUNT - 1:
            break
        elif state[i][j] == player:
            consecutive_count += 1
        else:
            break
        j += 1  # increment column when row is incremented

    if consecutive_count >= streak:
        total += 1

    return total
