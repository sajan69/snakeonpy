import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Tetrominos (Tetris pieces)
tetrominos = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1],
     [0, 1, 0]],     # T
    [[1, 1, 1],
     [1, 0, 0]],     # L
    [[1, 1, 1],
     [0, 0, 1]],     # J
    [[1, 1],
     [1, 1]],        # O
    [[0, 1, 1],
     [1, 1, 0]],     # S
    [[1, 1, 0],
     [0, 1, 1]]      # Z
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Function to create a new tetromino
def new_tetromino():
    tetromino = random.choice(tetrominos)
    return tetromino, 0, GRID_WIDTH // 2 - len(tetromino[0]) // 2

# Function to draw a block
def draw_block(x, y):
    pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, BLACK, (x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2))

# Function to draw the tetromino
def draw_tetromino(tetromino, x, y):
    for row in range(len(tetromino)):
        for col in range(len(tetromino[0])):
            if tetromino[row][col] == 1:
                draw_block(x + col, y + row)

# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    current_tetromino, tetromino_x, tetromino_y = new_tetromino()
    move_delay = FPS // 2  # Delay between automatic downward movements
    move_counter = 0

    while True:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetromino_x -= 1
                elif event.key == pygame.K_RIGHT:
                    tetromino_x += 1
                elif event.key == pygame.K_DOWN:
                    tetromino_y += 1
                elif event.key == pygame.K_UP:
                    # Rotate the tetromino
                    current_tetromino = [list(row) for row in zip(*current_tetromino[::-1])]

        # Move tetromino downward automatically
        move_counter += 1
        if move_counter >= move_delay:
            tetromino_y += 1
            move_counter = 0

        # Draw tetromino
        draw_tetromino(current_tetromino, tetromino_x, tetromino_y)

        
        pygame.display.update()
        clock.tick(FPS)


game_loop()
