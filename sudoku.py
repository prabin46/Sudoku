import time
import pygame, sys
import numpy as np
import copy


def find_next_empty(puzzle):
    for r in range(9):      # range(9) is 0, 1, 2, 3, ... 8
        for c in range(9):
            if puzzle[r][c] == 0:
                return r, c
    return None, None  # if no space in the puzzle are empyt (0)

def is_valid(puzzle, guess, row, col):
    # figures out whether the guess at the row, col of the puzzle is a valid guess
    # return True or False

    # for a guess to be valid, we need to follow the sudoku rules
    # guess number must not be repeated in the row, column, or 3x3 square that it appears in

    # checking row
    row_vals = puzzle[row]
    if guess in row_vals:
        return False # if we've repeated, then our guess is not valid!

    # checking columns
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    # checking square
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False
    return True

def solve_sudoku(puzzle):

    # solve sudoku using backtracking!
    # our puzzle is a list of lists, where each inner list is a row in our sudoku puzzle
    # return whether a solution exists
    # mutates puzzle to be the solution ( if solution exits)

    # choose somewhere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    # if there's nowhere left, then we're done because we only allowed valid inputs
    if row is None:     # this is true if our find_next_empty function returns None, None
        return True

    # if there is a place to put a number, then make a guess  between 1 and 9
    for guess in range(1, 10):  # range(1, 10) is 1, 2, 3,...9
        # check if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            # if this is a valid guess, then place it at that spot on the puzzle
            puzzle[row][col] = guess
            computer_game_solution.append([row, col, guess])


            # then we recursively call our solver!
            if solve_sudoku(puzzle):
                return True

        # if not valid or if nothing gets returned true, then we need to backtrack and try a new number
        puzzle[row][col] = 0
        for i in range(len(computer_game_solution)):
            if computer_game_solution[i][0] == row and computer_game_solution[i][1] == col:
                computer_game_solution.pop(i)

    # if none of the numbers that we try work, then this puzzle is UNSOLVABLE!!!
    return False


def display_suggestion():
    board_for_computer = copy.deepcopy(board)
    computer_game_solution.clear()
    if solve_sudoku(board_for_computer):
        # print(computer_game_solution[0])
        number_press_event(board, computer_game_solution[0][2], computer_game_solution[0][0], computer_game_solution[0][1])
    else:
        print("Problem not solved")


if __name__ == '__main__':
    example_board =[
        [3, 9, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 0, 5],
        [0, 0, 0, 7, 1, 9, 0, 8, 0],

        [0, 5, 0, 0, 6, 8, 0, 0, 0],
        [2, 0, 6, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 4],

        [5, 0, 0, 0, 0, 0, 0, 0, 0],
        [6, 7, 0, 1, 0, 5, 0, 4, 0],
        [1, 0, 9, 0, 0, 0, 2, 0, 0]
    ]




    # Initialing pygame
    pygame.init()
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    BOARD_ROWS = 9
    BOARD_COLS = 9
    BLOCK_WIDTH = SCREEN_WIDTH//9
    BLOCK_HEIGHT = SCREEN_HEIGHT//9
    LINE_WIDTH_THICK = 5
    LINE_WIDTH_THIN = 2
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    SELECED = (67, 224, 172)
    BG_COLOR = (28, 170, 156)
    LINE_COLOR = (23, 145, 135)

    font = pygame.font.SysFont(None, 80)
    font_alert = pygame.font.SysFont(None, 22)
    font_alert_erase = pygame.font.SysFont(None, 22)

    global clicked_row
    global clicked_col
    global player_game_solution
    global computer_game_solution

    player_game_solution = []
    computer_game_solution = []
    clicked_row = clicked_col = -1



    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Sudoku') # set the title of the screen
    screen.fill(BG_COLOR) # set the background color as BG_COLOR

    # Creating Game board
    board = copy.deepcopy(example_board)


    # Drawing lines for the board
    def draw_lines():
        for i in range(9):
            if i % 3 == 0:
                pygame.draw.line(screen, LINE_COLOR, (0, i * BLOCK_HEIGHT), (SCREEN_WIDTH, i * BLOCK_HEIGHT),
                                 LINE_WIDTH_THICK)
                pygame.draw.line(screen, LINE_COLOR, (i * BLOCK_WIDTH, 0), (i * BLOCK_WIDTH, SCREEN_HEIGHT),
                                 LINE_WIDTH_THICK)
            else:
                pygame.draw.line(screen, LINE_COLOR, (0, i * BLOCK_HEIGHT), (SCREEN_WIDTH, i * BLOCK_HEIGHT),
                                 LINE_WIDTH_THIN)
                pygame.draw.line(screen, LINE_COLOR, (i * BLOCK_WIDTH, 0), (i * BLOCK_WIDTH, SCREEN_HEIGHT),
                                 LINE_WIDTH_THIN)

    def draw_numbers():
        offset_x = BLOCK_WIDTH / 3.5
        offset_y = BLOCK_HEIGHT / 6
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                output = int(board[row][col])
                if output == 0:
                    n_text = font.render(str(" "), True, pygame.Color(SELECED))
                else:
                    n_text = font.render(str(output), True, pygame.Color('white'))

                screen.blit(n_text, [col * BLOCK_WIDTH + offset_x, row * BLOCK_HEIGHT + offset_y])
    # writing numbers to the board
    def mark_square(row, col, num):
        board[row][col] = num

    # checking if the square is empty
    def available_square(row, col):
        return board[row][col] == 0

    # Check if the board is full
    def is_board_full():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    return False
        print("You Won!")
        return True

    def number_press_event(board, number, row, col):
        if is_valid(board, number, row, col):
            mark_square(row, col, number)
            # print(board)
            draw_numbers()
            #tracking user Input
            player_game_solution.append([row, col, number])
            alert_message = font_alert_erase.render("Invalid   Number", True, pygame.Color(BG_COLOR))
            screen.blit(alert_message, [9, 3])
            is_board_full()

        else:
            alert_message = font_alert.render("Invalid   Number", True, pygame.Color('white'))
            screen.blit(alert_message, [9, 3])



    draw_lines()
    num = 0
    # Mainloop
    while True:
        draw_numbers()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]   # x
                mouseY = event.pos[1]   # y

                offset_rec = 5
                if clicked_row != -1:
                    pygame.draw.rect(screen, BG_COLOR, (clicked_col * BLOCK_WIDTH + offset_rec, clicked_row * BLOCK_HEIGHT + offset_rec, BLOCK_WIDTH - (2 * offset_rec), BLOCK_HEIGHT - (2 * offset_rec)))
                    draw_numbers()

                clicked_row = int(mouseY // BLOCK_HEIGHT)
                clicked_col = int(mouseX // BLOCK_WIDTH)
                if available_square(clicked_row, clicked_col):
                    pygame.draw.rect(screen, SELECED, (clicked_col * BLOCK_WIDTH + offset_rec, clicked_row * BLOCK_HEIGHT + offset_rec, BLOCK_WIDTH - (2 * offset_rec), BLOCK_HEIGHT - (2 * offset_rec)))
                    draw_numbers()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if available_square(clicked_row, clicked_col):
                        number_press_event(board, 1, clicked_row, clicked_col)

                if event.key == pygame.K_2:
                    if available_square(clicked_row, clicked_col):
                        number_press_event(board, 2, clicked_row, clicked_col)

                if event.key == pygame.K_3:
                    if available_square(clicked_row, clicked_col):
                        number_press_event(board, 3, clicked_row, clicked_col)

                if event.key == pygame.K_4:
                    if available_square(clicked_row, clicked_col):
                        number_press_event(board, 4, clicked_row, clicked_col)

                if event.key == pygame.K_5:
                    if available_square(clicked_row, clicked_col):
                        number_press_event(board, 5, clicked_row, clicked_col)

                if event.key == pygame.K_6:
                    if available_square(clicked_row, clicked_col):
                        number_press_event(board, 6, clicked_row, clicked_col)

                if event.key == pygame.K_7:
                    if available_square(clicked_row, clicked_col):
                        number_press_event(board, 7, clicked_row, clicked_col)

                if event.key == pygame.K_8:
                    if available_square(clicked_row, clicked_col):
                        number_press_event(board, 8, clicked_row, clicked_col)

                if event.key == pygame.K_9:
                    if available_square(clicked_row, clicked_col):
                        number_press_event(board, 9, clicked_row, clicked_col)

                if event.key == pygame.K_s:
                    display_suggestion()




        pygame.display.update()


