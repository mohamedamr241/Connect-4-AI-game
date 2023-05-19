ROW_COUNT = 6
COLUMN_COUNT = 7

COMPUTER_PIECE = 1
AI_PIECE = 2


def isValidPos(grid, col):
    return grid[ROW_COUNT - 1][col] == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if isValidPos(board, col):
            valid_locations.append(col)
    return valid_locations


def getNextRow(grid, col):
    for i in range(ROW_COUNT):
        if grid[i][col] == 0:
            return i

def checkWinner(grid, player):
    if count_streak(grid, player, 4) >= 1:
        return True

def estimate(state):
    center_count = 0
    center_column = len(state[0]) // 2  # Calculate the index of the center column

    for row in state:
        if row[center_column] == AI_PIECE:
            center_count += 1

    my_fours = count_streak(state, AI_PIECE, 4)
    my_threes = count_streak(state, AI_PIECE, 3)
    my_twos = count_streak(state, AI_PIECE, 2)
    opp_fours = count_streak(state, COMPUTER_PIECE, 4)
    opp_threes = count_streak(state, COMPUTER_PIECE, 3)

    if opp_fours > 0:
        return -100000
    else:
        return center_count * 5 + my_fours * 200 + my_threes * 10 + my_twos * 3 + opp_threes * -6

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

