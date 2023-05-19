import math
import random

NUMBER_OF_ROWS = 6
NUMBER_OF_COLUMNS = 7

COMPUTER_TOKEN = 1
AI_TOKEN = 2


def isValidPos(grid, col):
    return grid[NUMBER_OF_ROWS - 1][col] == 0


def getValidPositions(grid):
    valid_positions = []
    for col in range(NUMBER_OF_COLUMNS):
        if isValidPos(grid, col):
            valid_positions.append(col)
    return valid_positions


def getNextRow(grid, col):
    for row in range(NUMBER_OF_ROWS):
        if grid[row][col] == 0:
            return row

def checkWinner(grid, player):
    if count_streak(grid, player, 4) >= 1:
        return True

def estimate(grid):
    center_count = 0
    center_column = len(grid[0]) // 2

    for row in grid:
        if row[center_column] == AI_TOKEN:
            center_count += 1

    AI_fours = count_streak(grid, AI_TOKEN, 4)
    AI_threes = count_streak(grid, AI_TOKEN, 3)
    AI_twos = count_streak(grid, AI_TOKEN, 2)
    opp_fours = count_streak(grid, COMPUTER_TOKEN, 4)
    opp_threes = count_streak(grid, COMPUTER_TOKEN, 3)

    if opp_fours > 0:
        return -100000
    else:
        return center_count * 5 + AI_fours * 200 + AI_threes * 10 + AI_twos * 3 + opp_threes * -6


# check if there are n numbers of streaks beside each other in vertically, horizontally and diagonally.
def count_streak(grid, player, streak):
    count = 0
    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLUMNS):
            if grid[i][j] == player:
                count += vertical_streak(i, j, grid, streak)
                count += horizontal_streak(i, j, grid, streak)
                count += diagonal_streak(i, j, grid, streak)
    return count


def vertical_streak(row, col, grid, streak):
    # check n streaks beside each other vertically and return 1 if the count is found and 0 if not.
    consecutive_count = 0
    player = grid[row][col]

    for i in range(row, NUMBER_OF_ROWS):
        if grid[i][col] == player:
            consecutive_count += 1
        else:
            break

    return 1 if consecutive_count >= streak else 0


def horizontal_streak(row, col, state, streak):
    # check n streaks beside each other horizontally and return 1 if the count is found and 0 if not.
    consecutive_count = 0
    player = state[row][col]

    for j in range(col, NUMBER_OF_COLUMNS):
        if state[row][j] == player:
            consecutive_count += 1
        else:
            break

    return 1 if consecutive_count >= streak else 0


def diagonal_streak(row, col, grid, streak):
    # check n streaks beside each other diagonally and return 1 if the count is found and 0 if not.
    player = grid[row][col]
    total = 0
    # check for diagonals with positive slope
    consecutive_count = 0
    j = col
    for i in range(row, NUMBER_OF_ROWS):
        if j > (NUMBER_OF_COLUMNS - 1) or grid[i][j] != player:
            break
        else:
            consecutive_count += 1
        j += 1

    if consecutive_count >= streak:
        total += 1

    # check for diagonals with negative slope
    consecutive_count = 0
    j = col
    for i in range(row, -1, -1):
        if j > (NUMBER_OF_COLUMNS - 1) or grid[i][j] != player:
            break
        else:
            consecutive_count += 1
        j += 1

    if consecutive_count >= streak:
        total += 1

    return total

def is_terminal_node(grid):
    return checkWinner(grid, COMPUTER_TOKEN) or checkWinner(grid, AI_TOKEN) or len(getValidPositions(grid)) == 0


def minimax(grid, depth, maximizingPlayer):
    valid_positions = getValidPositions(grid)
    if is_terminal_node(grid):
        if checkWinner(grid, AI_TOKEN):
            return (None, 100000000000000)
        elif checkWinner(grid, COMPUTER_TOKEN):
            return (None, -10000000000000)
        else:  # Game is over, no more valid moves
            return (None, 0)
    if depth == 0:
        return (None, estimate(grid))
    if maximizingPlayer:
        max_eval = -math.inf
        column = 0
        for col in valid_positions:
            row = getNextRow(grid, col)
            tmp_grid = grid.copy()
            tmp_grid[row][col] = AI_TOKEN
            new_score = minimax(tmp_grid, depth - 1, False)[1]
            if new_score > max_eval:
                max_eval = new_score
                column = col
        return column, max_eval

    else:  # Minimizing player
        min_eval = math.inf
        column = random.choice(valid_positions)
        for col in valid_positions:
            row = getNextRow(grid, col)
            tmp_grid = grid.copy()
            tmp_grid[row][col] = COMPUTER_TOKEN
            new_score = minimax(tmp_grid, depth - 1, True)[1]
            if new_score < min_eval:
                min_eval = new_score
                column = col
        return column, min_eval
