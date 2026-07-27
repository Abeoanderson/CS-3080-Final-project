# Tetris PyGame
# Imports
import sys

import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 300, 500
FPS = 35

BLOCK = 20
ROWS = (HEIGHT - 120) // BLOCK
COLS = WIDTH // BLOCK

# Game settinngs: screen, clock, title, etc.
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Abes Tetris Game")

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BG_COLOR = (20,20,20)
GRID = (100,100,100)
WIN = (0,255,0)
LOSE = (255,0,0)

# load / store images
ASSETS ={
    1: pygame.image.load("Assets/1.png"),
    2: pygame.image.load("Assets/2.png"),
    3: pygame.image.load("Assets/3.png"),
    4: pygame.image.load("Assets/4.png")
}

# fonts
font1 = pygame.font.Font(
    "Assets/PressStart2P-Regular.ttf",
    50
)

font2 = pygame.font.Font(
    "Assets/VT323-Regular.ttf",
    20
)

# shape class
class Shape:
    #global variables for types I, Z, S, L, J, T, O and coordinates
    VERSIONS = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]
    }
    SHAPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']

    # constrructor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.SHAPES)
        self.shape = self.VERSIONS[self.type]
        self.color = random.randint(1,4)
        self.orientation = 0

    # image - version of the shape based on current orientation
    def image(self):
        return self.shape[self.orientation]

    # Rotate the shape if possible
    def rotate(self):
        self.orientation = (self.orientation + 1) % len(self.shape)

















# Game Class
    # constructore

    # Make grid

    # Make new shape


# Main game loop
def main():
    run = True
    while run:
        SCREEN.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()


        pygame.display.update()

if __name__ == "__main__":
    main()