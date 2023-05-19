import numpy as np
import pygame
import math
import sys
import random
import tkinter as tk
from tkinter import ttk

NUMBER_OF_ROWS = 6
NUMBER_OF_COLUMNS = 7

COMPUTER_TOKEN = 1
AI_TOKEN = 2

BLUE = (0, 153, 153)
BABYBLUE = (137, 207, 240)
PURPLE = (204, 0, 204)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

SQUARESIZE = 100
width = NUMBER_OF_COLUMNS * SQUARESIZE
height = (NUMBER_OF_ROWS + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)


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


def minimax_alpha_beta(grid, depth, alpha, beta, maximizingPlayer):
    valid_locations = getValidPositions(grid)
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
        for col in valid_locations:
            row = getNextRow(grid, col)
            tmp_grid = grid.copy()
            tmp_grid[row][col] = AI_TOKEN
            new_score = minimax_alpha_beta(tmp_grid, depth - 1, alpha, beta, False)[1]
            if new_score > max_eval:
                max_eval = new_score
                column = col
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break
        return column, max_eval

    else:  # Minimizing player
        min_eval = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextRow(grid, col)
            tmp_grid = grid.copy()
            tmp_grid[row][col] = COMPUTER_TOKEN
            new_score = minimax_alpha_beta(tmp_grid, depth - 1, alpha, beta, True)[1]
            if new_score < min_eval:
                min_eval = new_score
                column = col
            beta = min(beta, min_eval)
            if alpha >= beta:
                break
        return column, min_eval


def drawGrid(screen, grid):
    for i in range(NUMBER_OF_COLUMNS):
        for j in range(NUMBER_OF_ROWS):
            pygame.draw.rect(screen, BLUE, (i * SQUARESIZE, j * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BABYBLUE, (
                int(i * SQUARESIZE + SQUARESIZE / 2), int(j * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for i in range(NUMBER_OF_COLUMNS):
        for j in range(NUMBER_OF_ROWS):
            if grid[j][i] == COMPUTER_TOKEN:
                pygame.draw.circle(screen, PURPLE, (
                    int(i * SQUARESIZE + SQUARESIZE / 2), height - int(j * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif grid[j][i] == AI_TOKEN:
                pygame.draw.circle(screen, YELLOW, (
                    int(i * SQUARESIZE + SQUARESIZE / 2), height - int(j * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


# Define the levels and algorithms
levels = ["Easy", "Medium", "Hard"]
algorithms = ["Minimax", "Alpha-Beta"]
opponents = ["AI", "Human", "Random"]

# Create a Tkinter window
window = tk.Tk()
window.title("Algorithm Selection")
window.geometry("800x800")

# Variables to store the selected level and algorithm
selected_level = tk.StringVar()
selected_algorithm = tk.StringVar()
selected_opponents = tk.StringVar()


# Function to handle level selection
def select_level(event):
    selected_level.set(level_combobox.get())


# Function to handle algorithm selection
def select_algorithm(event):
    selected_algorithm.set(algorithm_combobox.get())


def select_opponent(event):
    selected_opponents.set(opponents_combobox.get())


# Create the level label and drop-down list
level_label = ttk.Label(window, text="Select Level:")
level_label.pack(pady=10)
level_combobox = ttk.Combobox(window, values=levels, textvariable=selected_level)
level_combobox.pack()
level_combobox.bind("<<ComboboxSelected>>", select_level)

# Create the algorithm label and drop-down list
algorithm_label = ttk.Label(window, text="Select Algorithm:")
algorithm_label.pack(pady=10)
algorithm_combobox = ttk.Combobox(window, values=algorithms, textvariable=selected_algorithm)
algorithm_combobox.pack()
algorithm_combobox.bind("<<ComboboxSelected>>", select_algorithm)

# Create the algorithm label and drop-down list
opponents_label = ttk.Label(window, text="Select opponent:")
opponents_label.pack(pady=10)
opponents_combobox = ttk.Combobox(window, values=opponents, textvariable=selected_opponents)
opponents_combobox.pack()
opponents_combobox.bind("<<ComboboxSelected>>", select_opponent)


# Function to print the selected level and algorithm
def print_selection():
    level = selected_level.get()
    algorithm = selected_algorithm.get()
    opp = selected_opponents.get()
    if level == 'Easy':
        depth = 1
    elif level == 'Medium':
        depth = 3
    else:
        depth = 4
    window.destroy()
    #execute(depth, algorithm, opp)


# Create the button to print the selected level and algorithm
print_button = ttk.Button(window, text="Start Game", command=print_selection)
print_button.pack(pady=20)

# Run the Tkinter event loop
window.mainloop()
