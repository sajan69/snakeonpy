
import random
import json
import pygame


pygame.init()


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


font = pygame.font.SysFont(None, 40)


try:
    with open("high_scores.json", "r") as file:
        high_scores = json.load(file)
except FileNotFoundError:
    high_scores = [0, 0, 0]


def save_high_scores():
    with open("high_scores.json", "w") as file:
        json.dump(high_scores, file)


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def draw_button(text, font, color, rect, action=None):
    pygame.draw.rect(screen, color, rect)
    draw_text(text, font, BLACK, rect.centerx, rect.centery)
    return pygame.Rect(rect)


def main_menu():
    screen.fill(BLACK)
    title_font = pygame.font.SysFont(None, 60)
    draw_text(" Simple Snake Game by Sajan Adhikari", title_font, WHITE, WIDTH // 2, HEIGHT // 4)

    play_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
    high_scores_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 50)

    play_button = draw_button("Play", font, GREEN, play_button_rect)
    high_scores_button = draw_button("High Scores", font, GREEN, high_scores_button_rect, display_high_scores)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    game_loop()
                elif high_scores_button.collidepoint(mouse_pos):
                    display_high_scores()


def display_high_scores():
    screen.fill(BLACK)
    draw_text("High Scores", font, WHITE, WIDTH // 2, HEIGHT // 4)
    for i, score in enumerate(high_scores):
        draw_text(str(i + 1) + ". " + str(score), font, WHITE, WIDTH // 2, HEIGHT // 2 + i * 40)

    go_back_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 200, WIDTH // 2, 50)
    go_back_button = draw_button("Go Back", font, GREEN, go_back_button_rect, main_menu)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if go_back_button.collidepoint(mouse_pos):
                    main_menu()

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))


def draw_fruit(fruit):
    pygame.draw.rect(screen, RED, (fruit[0], fruit[1], BLOCK_SIZE, BLOCK_SIZE))


def display_score(score):
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))



def game_loop():
    global snake, fruit, direction
    # Set up game variables
    snake = [(WIDTH // 2, HEIGHT // 2)]
    fruit = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
             random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
    direction = "RIGHT"
    score = 0

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != "DOWN":
            direction = "UP"
        elif keys[pygame.K_DOWN] and direction != "UP":
            direction = "DOWN"
        elif keys[pygame.K_LEFT] and direction != "RIGHT":
            direction = "LEFT"
        elif keys[pygame.K_RIGHT] and direction != "LEFT":
            direction = "RIGHT"

        # Update snake position
        if direction == "UP":
            new_head = (snake[0][0], snake[0][1] - BLOCK_SIZE)
        elif direction == "DOWN":
            new_head = (snake[0][0], snake[0][1] + BLOCK_SIZE)
        elif direction == "LEFT":
            new_head = (snake[0][0] - BLOCK_SIZE, snake[0][1])
        elif direction == "RIGHT":
            new_head = (snake[0][0] + BLOCK_SIZE, snake[0][1])

        
        snake.insert(0, new_head)

        
        if snake[0] == fruit:
            score += 1
            fruit = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                     random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
        else:
            # snake klo last vaag lai hataidinu to make it seem like moving
            snake.pop()

        # wall sanga ko collision check hannu
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
                snake[0][1] < 0 or snake[0][1] >= HEIGHT):
            if game_over(score):
                return

        # aafu sanga collision check hannu
        if snake[0] in snake[1:]:
            if game_over(score):
                return

        
        screen.fill(BLACK)

        
        draw_snake(snake)
        draw_fruit(fruit)
        display_score(score)

        
        pygame.display.update()

        # change this to increase difficulty level
        clock.tick(5)


def game_over(score):
    global snake, fruit, direction, high_scores
    if score > min(high_scores):
        high_scores.append(score)
        high_scores.sort(reverse=True)
        high_scores = high_scores[:3]
        save_high_scores()
    screen.fill(BLACK)
    draw_text("You died!", font, RED, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text("Your score: " + str(score), font, WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text("High Scores:", font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    for i, score in enumerate(high_scores):
        draw_text(str(i + 1) + ". " + str(score), font, WHITE, WIDTH // 2, HEIGHT // 2 + 90 + i * 40)

    go_back_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 200, WIDTH // 2, 50)
    go_back_button = draw_button("Go Back", font, GREEN, go_back_button_rect, main_menu)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if go_back_button.collidepoint(mouse_pos):
                    main_menu()
                    return


if __name__ == "__main__":
    main_menu()

