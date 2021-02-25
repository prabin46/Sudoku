import time
import pygame, sys
import numpy as np


def find_next_empty(pussle):
    for r in range(9): # range(9) is 0, 1, 2, 3, ... 8
        for c in range(9):
            if pussle[r][c] == 0:
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

    # step 1: choose somewhere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    # Step 1.1 if there's nowhere left, then we're done because we only allowed valid inputs
    if row is None: # this is true if our find_next_empty function returns None, None
        return True

    # step 2: if there is a place to put a number, then make a guess  between 1 and 9
    for guess in range(1, 10): # range(1, 10) is 1, 2, 3,...9
        # step 3: check if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            # step 3.1: if this is a valid guess, then place it at that spot on the puzzle
            puzzle[row][col] = guess
            # time.sleep(1)
            # print_board(example_board)
            # step 4: then we recursively call our solver!
            if solve_sudoku(puzzle):
                return True

        # step 5: if not valid or if nothing gets returned true, then we need to backtrack and try a new number
        puzzle[row][col] = 0

    # step 6: if none of the numbers that we try work, then this puzzle is UNSOLVABLE!!!
    return False

def print_board(puzzle):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")

        for j in range(len(puzzle[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(puzzle[i][j])
            else:
                print(str(puzzle[i][j]) + " ", end="")


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

    #print_board(example_board)
    #solve_sudoku(example_board)
    #print_board(example_board)

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
    BG_COLOR = (28, 170, 156)
    LINE_COLOR = (23, 145, 135)

    font = pygame.font.SysFont(None, 80)

    global clicked_row
    global clicked_col
    clicked_row = clicked_col = -1

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Sudoku') # set the title of the screen
    screen.fill(BG_COLOR) # set the background color as BG_COLOR

    # Creating Game board
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    board = example_board

    print(board)

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
                    n_text = font.render(str(""), True, pygame.Color('white'))
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
        return True

    def number_press_event(board, number, row, col):
        if is_valid(board, number, row, col):
            mark_square(row, col, number)
            # print(board)
            draw_numbers()
        else:
            print("Invalid Number...!")


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
                    pygame.draw.rect(screen, BLUE, (clicked_col * BLOCK_WIDTH + offset_rec, clicked_row * BLOCK_HEIGHT + offset_rec, BLOCK_WIDTH - (2 * offset_rec), BLOCK_HEIGHT - (2 * offset_rec)))
                    draw_numbers()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if available_square(clicked_row, clicked_col):
                        number_press_event(board,1 , clicked_row, clicked_col)

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




        pygame.display.update()


