# Tetris PyGame
# Imports
import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 430, 500
FPS = 35

BLOCK = 20
ROWS = (HEIGHT - 120) // BLOCK
COLS = 10

# board origin
BOARD_X = 110
BOARD_Y = 20

# next box
HOLD_X, HOLD_Y, HOLD_SIZE = 20, 50, 70

# hold box
NEXT_X = BOARD_X + COLS * BLOCK + 20
NEXT_Y, NEXT_SIZE = 50, 70

# game states
START = 0
PLAYING = 1
GAME_OVER = 2

# Game settinngs: screen, clock, title, etc.
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Abes Tetris Game")

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BG_COLOR = (31,25,76)
GRID = (100,100,100)
LOSE = (255,0,0)
GHOST = (180, 180, 180)

# load / store images
PREVIEW_BLOCK = 10  # smaller than the in-game BLOCK (20)

ASSETS = {
    1: pygame.image.load("Assets/1.png"),
    2: pygame.image.load("Assets/2.png"),
    3: pygame.image.load("Assets/3.png"),
    4: pygame.image.load("Assets/4.png")
}

PREVIEW_ASSETS = {
    k: pygame.transform.scale(img, (PREVIEW_BLOCK, PREVIEW_BLOCK))
    for k, img in ASSETS.items()
}

# fonts
font1 = pygame.font.Font(
    "Assets/PressStart2P-Regular.ttf",
    30
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
        self.lines = 0
        self.held = None
        self.can_hold = True
        self.message = ""
        self.message_timer = 0
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)] # list compreheni
        self.next = None
        self.end = False
        self.new_shape()

    # Make grid
    def make_board(self):
    # Horizontal lines
        for i in range(self.rows + 1):
            pygame.draw.line(
                SCREEN,
                GRID,
                (BOARD_X, BOARD_Y + BLOCK * i),
                (BOARD_X + COLS * BLOCK, BOARD_Y + BLOCK * i)
            )
        # Vertical lines
        for j in range(self.cols + 1):
            pygame.draw.line(
                SCREEN,
                GRID,
                (BOARD_X + BLOCK * j, BOARD_Y),
                (BOARD_X + BLOCK * j, BOARD_Y + ROWS * BLOCK)
            )
        # draw border 
        pygame.draw.rect(
            SCREEN,
            WHITE,
            (
                BOARD_X,
                BOARD_Y,
                COLS * BLOCK,
                ROWS * BLOCK
            ),
            3
        )
        # draw hold box
        HOLD_BOX = pygame.Rect(
            20,
            50,
            70,
            70
        )

        pygame.draw.rect(
            SCREEN,
            WHITE,
            HOLD_BOX,
            2
        )
        text = font2.render("HOLD", True, WHITE)
        SCREEN.blit(text, (HOLD_X+ 20, HOLD_Y - 20))
        # draw next box
        NEXT_BOX = pygame.Rect(
            BOARD_X + COLS*BLOCK + 20,
            50,
            70,
            70
        )

        pygame.draw.rect(
            SCREEN,
            WHITE,
            NEXT_BOX,
            2
        )
    # Make new shape
    def new_shape(self):
        if not self.next:
            self.next = Shape(5,0)

        self.figure = self.next
        self.next = Shape(5,0)

        # check if new piece immediately collides if so end game
        if self.collision():
            self.end = True

    # draw preview of peice
    def draw_preview(self, piece, box_x, box_y, box_size=70):
        if piece is None:
            return

        cells = piece.image()
        rows = [i for i in range(4) for j in range(4) if i * 4 + j in cells]
        cols = [j for i in range(4) for j in range(4) if i * 4 + j in cells]
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        piece_w = (max_col - min_col + 1) * PREVIEW_BLOCK
        piece_h = (max_row - min_row + 1) * PREVIEW_BLOCK

        offset_x = box_x + (box_size - piece_w) // 2
        offset_y = box_y + (box_size - piece_h) // 2

        for i in range(4):
            for j in range(4):
                if i * 4 + j in cells:
                    x = offset_x + (j - min_col) * PREVIEW_BLOCK
                    y = offset_y + (i - min_row) * PREVIEW_BLOCK
                    SCREEN.blit(PREVIEW_ASSETS[piece.color], (x, y))
                    pygame.draw.rect(SCREEN, WHITE, (x, y, PREVIEW_BLOCK, PREVIEW_BLOCK), 1)

    # calculate the row the piece would land on if dropped now
    def ghost_position(self):
        original_y = self.figure.y

        while not self.collision():
            self.figure.y += 1

        self.figure.y -= 1
        ghost_y = self.figure.y

        self.figure.y = original_y
        return ghost_y
    # Restart
    def restart(self):
        self.score = 0
        self.level = 1
        self.lines = 0
        self.message = ""
        self.message_timer = 0
        self.held = None
        self.can_hold = True
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.end = False
        self.next = None
        self.new_shape()

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

    # hold peices
    def hold(self):

        if not self.can_hold:
            return

        if self.held is None:
            self.held = self.figure
            self.new_shape()
        else:
            self.figure, self.held = self.held, self.figure

            self.figure.x = 5
            self.figure.y = 0
            self.figure.orientation = 0

        self.can_hold = False


    # freez peices at the bottom
    def freeze_piece(self):
        for i in range(4):
            for j in range(4):

                if i * 4 + j in self.figure.image():

                    row = self.figure.y + i
                    col = self.figure.x + j

                    if row >= 0:
                        self.grid[row][col] = self.figure.color

        self.can_hold = True
        self.clear_rows()
        self.new_shape()

    # clear row if whole row is clear
    def clear_rows(self):

        cleared = 0
        row = self.rows - 1

        while row >= 0:

            if 0 not in self.grid[row]:

                del self.grid[row]

                self.grid.insert(
                    0,
                    [0 for _ in range(self.cols)]
                )

                cleared += 1
                # don't decrement `row` here — the row that shifted down
                # into this same index (from further up the board) still
                # needs to be checked before we move on
            else:
                row -= 1

        if cleared > 0:
            self.update_score(cleared)
    # update scores for lines
    def update_score(self, cleared):

        scores = {
            1: 100,
            2: 300,
            3: 500,
            4: 800
        }

        self.score += scores[cleared]
        self.lines += cleared

        if cleared == 4:
            self.message = "TETRIS!"
            self.message_timer = pygame.time.get_ticks()

        self.level = (self.lines // 10) + 1



# Main game loop
def main():
    tetris = Game(ROWS, COLS)

    game_state = START
    countdown = 3
    countdown_timer = pygame.time.get_ticks()

    counter = 0
    move = True
    move_counter = 0
    move_delay = 5

    # poll key state once up front so it always exists before it's read
    keys = pygame.key.get_pressed()

    run = True
    while run:
        if game_state == START:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()

            SCREEN.fill(BG_COLOR)

            current_time = pygame.time.get_ticks()

            if current_time - countdown_timer >= 1000:
                countdown -= 1
                countdown_timer = current_time

            if countdown <= 0:
                game_state = PLAYING


            text = font1.render(
                str(countdown) if countdown > 0 else "START!",
                True,
                WHITE
            )

            SCREEN.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2
                )
            )

            pygame.display.update()
            CLOCK.tick(FPS)

            continue



        SCREEN.fill(BG_COLOR)
        current_time = pygame.time.get_ticks()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if tetris.end:
                    # only restart is valid once the game is over
                    if event.key == pygame.K_r:
                        tetris.restart()

                        game_state = START
                        countdown = 3
                        countdown_timer = pygame.time.get_ticks()
                else:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        tetris.move_left()

                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        tetris.move_right()

                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        tetris.rotate()

                    elif event.key == pygame.K_SPACE:
                        tetris.slam()
                        tetris.freeze_piece()
                    elif event.key == pygame.K_c:
                        tetris.hold()

        # continuous key state (held-down movement / soft drop), read once per frame
        keys = pygame.key.get_pressed()

        if game_state == PLAYING:
            if not tetris.end:
                move_counter += 1

                if move_counter >= move_delay:

                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        tetris.move_left()

                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        tetris.move_right()

                    move_counter = 0

                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    if not tetris.move_down():
                        tetris.freeze_piece()

                counter += 1
                if counter >= 10000:
                    counter = 0

                if move:
                    if counter % max(1, FPS // tetris.level) == 0:
                        if not tetris.move_down(): # if peice cannot move down freez it
                            tetris.freeze_piece()

        tetris.make_board()
        # draw frozen blocks
        for row in range(ROWS):
            for col in range(COLS):

                if tetris.grid[row][col] > 0:

                    shape = ASSETS[tetris.grid[row][col]]

                    x = BOARD_X + col * BLOCK
                    y = BOARD_Y + row * BLOCK

                    SCREEN.blit(shape, (x, y))

                    pygame.draw.rect(
                        SCREEN,
                        WHITE,
                        (x, y, BLOCK, BLOCK),
                        1
                    )
        # draw ghost piece (outline only, shows where it will land)
        if not tetris.end:
            ghost_y = tetris.ghost_position()

            for i in range(4):
                for j in range(4):
                    if i * 4 + j in tetris.figure.image():

                        x = BOARD_X + BLOCK * (tetris.figure.x + j)
                        y = BOARD_Y + BLOCK * (ghost_y + i)

                        if x >= 0 and y >= 0:
                            pygame.draw.rect(
                                SCREEN,
                                GHOST,
                                (x, y, BLOCK, BLOCK),
                                2
                            )
        # show shape on game screen
        for i in range(4):
            for j in range(4):
                if i * 4 + j in tetris.figure.image():
                    shape = ASSETS[tetris.figure.color]

                    x = BOARD_X + BLOCK * (tetris.figure.x + j)
                    y = BOARD_Y + BLOCK * (tetris.figure.y + i)

                    if x >= 0 and y >= 0:
                        SCREEN.blit(shape, (x, y))
                    pygame.draw.rect(
                        SCREEN,
                        WHITE,
                        (x, y, BLOCK, BLOCK),
                        1
                    )
        # draw next and held peice preveiws in centered box
        tetris.draw_preview(tetris.next, NEXT_X, NEXT_Y, NEXT_SIZE)
        tetris.draw_preview(tetris.held, HOLD_X, HOLD_Y, HOLD_SIZE)
        score_text = font2.render(
            f"Score: {tetris.score}",
            True,
            WHITE
        )

        level_text = font2.render(
            f"Level: {tetris.level}",
            True,
            WHITE
        )

        lines_text = font2.render(
            f"Lines: {tetris.lines}",
            True,
            WHITE
        )


        SCREEN.blit(score_text, (10, HEIGHT - 90))
        SCREEN.blit(level_text, (10, HEIGHT - 65))
        SCREEN.blit(lines_text, (10, HEIGHT - 40))

        #tetris timer check so it fades
        if tetris.message and current_time - tetris.message_timer > 2000:
            tetris.message = ""

        #if timer still going render tetris
        if tetris.message:
            text = font2.render(
                tetris.message,
                True,
                WHITE
            )

            SCREEN.blit(text, (100, HEIGHT - 100))

        if tetris.end:
            game_state = GAME_OVER
        if game_state == GAME_OVER:

            text = font1.render(
                "GAME OVER",
                True,
                LOSE
            )

            restart = font2.render(
                "Press R to restart",
                True,
                WHITE
            )

            SCREEN.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - 40
                )
            )

            SCREEN.blit(
                restart,
                (
                    WIDTH // 2 - restart.get_width() // 2,
                    HEIGHT // 2 + 30
                )
            )

        CLOCK.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    main()