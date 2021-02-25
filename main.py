import pygame, sys
from pygame.locals import *
# This is a sample Python script.



def print_hi(name):
    pygame.init()
    DISPLAY = pygame.display.set_mode((500,400), 0, 32)

    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    DISPLAY.fill(WHITE)

    `pygame.draw.rect(DISPLAY, BLUE, (200, 150, 100, 50))`

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
