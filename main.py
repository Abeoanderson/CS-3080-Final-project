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
    # constrructor

    # image 

    # Rotate

















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