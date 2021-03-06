import pygame, sys
from pygame.locals import *
import array
# This is a sample Python script.

def print_array(board_user_input):
    for row in range(len(board_user_input)):
        for col in range(len(board_user_input[0])):
            print(board_user_input[row][col])
        print()

def print_hi():
    board_user_input = []
    board_user_input.append([1, 2])
    board_user_input.append([3, 4])
    board_user_input.append([5, 6])
    board_user_input.pop(len(board_user_input) - 1)

    #print(board_user_input)
    #board_user_input.append(1, 2, 3)
    #print_array(board_user_input)
    print("Original Array")
    print(board_user_input)

    array_copy = board_user_input[:]


    array_copy.append([10, 11])

    print("Duplicate Array")
    print(array_copy)

    print("Original Array")
    print(board_user_input)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
