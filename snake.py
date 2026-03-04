import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

def reset_game():
    snake = [[WIDTH // 2, HEIGHT // 2], [WIDTH // 2 - CELL_SIZE, HEIGHT // 2], [WIDTH // 2 - 2 * CELL_SIZE, HEIGHT // 2]]
    direction = "RIGHT"
    food = get_random_food_pos(snake)
    score = 0
    return snake, direction, food, score

def get_random_food_pos(snake):
    while True:
        pos = [random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE)]
        if pos not in snake:
            return pos

def game_over_screen(score):
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))

    font_small = pygame.font.SysFont(None, 32)
    restart_text = font_small.render("Press SPACE to restart or ESC to quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

    screen.fill(BLACK)
    screen.blit(text, text_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    snake, direction, food, score = reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # Calculate new head position
        head = list(snake[0])
        if direction == "UP":
            head[1] -= CELL_SIZE
        if direction == "DOWN":
            head[1] += CELL_SIZE
        if direction == "LEFT":
            head[0] -= CELL_SIZE
        if direction == "RIGHT":
            head[0] += CELL_SIZE

        # Check for collisions
        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake):
            game_over_screen(score)
            snake, direction, food, score = reset_game()
            continue

        snake.insert(0, head)

        # Check for eating food
        if head == food:
            score += 1
            food = get_random_food_pos(snake)
        else:
            snake.pop()

        # Drawing
        screen.fill(BLACK)

        # Draw food
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

        # Draw snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
