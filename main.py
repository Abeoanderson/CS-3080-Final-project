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
BG_COLOR = (31,25,76)
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
class Game:
    # constructor
    def __init__(self,rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.level = 1
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)] # list compreheni
        self.next = None
        self.end = False
        self.new_shape()

    # Make grid
    def make_grid(self):
        for i in range(self.rows + 1):
            pygame.draw.line(SCREEN, GRID, (0, BLOCK * i), (WIDTH, BLOCK * i))
        for j in range(self.cols + 1):
            pygame.draw.line(SCREEN, GRID, (BLOCK * j, 0), (BLOCK * j, HEIGHT - 120))
    # Make new shape
    def new_shape(self):
        if not self.next:
            self.next = Shape(5,0)
        self.figure = self.next
        self.next = Shape(5,0)

    # check collisions returns a bool for collison yes or no
    def collision(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():

                    block_row = self.figure.y + i
                    block_col = self.figure.x + j

                    if block_col < 0 or block_col >= self.cols:
                        return True

                    if block_row >= self.rows:
                        return True

                    if block_row >= 0 and self.grid[block_row][block_col] > 0:
                        return True

        return False
    # remove row

    # peices fall
    def move_down(self):
        self.figure.y += 1

        if self.collision():
            self.figure.y -= 1
            return False

        return True

    # move left 
    def move_left(self):
        self.figure.x -= 1

        if self.collision():
            self.figure.x += 1
            return False

        return True

    # move right 
    def move_right(self):
        self.figure.x += 1

        if self.collision():
            self.figure.x -= 1
            return False

        return True


    # Rotate piece
    def rotate(self):
        old_rotation = self.figure.orientation
        old_x = self.figure.x

        self.figure.rotate()

        # Try normal rotation
        if not self.collision():
            return

        # Try moving right
        self.figure.x += 1
        if not self.collision():
            return

        # Try moving left
        self.figure.x -= 2
        if not self.collision():
            return

        # Rotation failed
        self.figure.x = old_x
        self.figure.orientation = old_rotation
    # Hard drop (slam)
    def slam(self):
        while self.move_down():
            pass

    # freez peices at the bottom
    def freeze_piece(self):
        for i in range(4):
            for j in range(4):

                if i * 4 + j in self.figure.image():

                    row = self.figure.y + i
                    col = self.figure.x + j

                    if row >= 0:
                        self.grid[row][col] = self.figure.color

        self.new_shape()




# Main game loop
def main():
    tetris = Game(ROWS, COLS)
    counter = 0
    move = True
    move_counter = 0
    move_delay = 5

    run = True
    while run:
        SCREEN.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    tetris.move_left()

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    tetris.move_right()

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    tetris.rotate()

                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    if not tetris.move_down():
                        tetris.freeze_piece()

                elif event.key == pygame.K_SPACE:
                    tetris.slam()
                    tetris.freeze_piece()
        keys = pygame.key.get_pressed()
        # hold down keys keeps them moving
        move_counter += 1

        if move_counter >= move_delay:

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                tetris.move_left()

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                tetris.move_right()

            move_counter = 0

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            tetris.move_down()
        counter += 1
        if counter >= 10000:
            counter = 0

        if move:
            if counter %(FPS //(tetris.level)) == 0:
                if not tetris.end: # while game still goes
                    if not tetris.move_down(): # if peice cannot move down freez it
                        tetris.freeze_piece()

        tetris.make_grid()
        # draw frozen blocks
        for row in range(ROWS):
            for col in range(COLS):

                if tetris.grid[row][col] > 0:

                    shape = ASSETS[tetris.grid[row][col]]

                    x = col * BLOCK
                    y = row * BLOCK

                    SCREEN.blit(shape, (x, y))

                    pygame.draw.rect(
                        SCREEN,
                        WHITE,
                        (x, y, BLOCK, BLOCK),
                        1
                    )

        # show shape on game screen
        for i in range(4):
            for j in range(4):
                if i * 4 + j in tetris.figure.image():
                    shape = ASSETS[tetris.figure.color]

                    x = BLOCK * (tetris.figure.x + j)
                    y = BLOCK * (tetris.figure.y + i)

                    if x >= 0 and y >= 0:
                        SCREEN.blit(shape, (x, y))
                    pygame.draw.rect(
                        SCREEN,
                        WHITE,
                        (x, y, BLOCK, BLOCK),
                        1
                    )
        CLOCK.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    main()