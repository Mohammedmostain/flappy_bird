import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
BACKGROUND_COLOR = (0, 200, 255)  # Sky blue
BIRD_COLOR = (255, 255, 0)  # Yellow
PIPE_COLOR = (0, 255, 0)  # Green
TEXT_COLOR = (255, 255, 255)  # White

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.SysFont("Arial", 30)

def get_high_score():
    try:
        with open("high_score.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def save_high_score(new_high_score):
    with open("high_score.txt", "w") as f:
        f.write(str(new_high_score))

def draw_bird(bird_pos):
    pygame.draw.circle(screen, BIRD_COLOR, bird_pos, 15)

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, PIPE_COLOR, (pipe[0], 0, 70, pipe[1]))
        pygame.draw.rect(screen, PIPE_COLOR, (pipe[0], pipe[1] + 200, 70, SCREEN_HEIGHT - pipe[1] - 200))

def update_pipes(pipes):
    for pipe in pipes:
        pipe[0] -= 5
    if pipes[0][0] < -70:  # Pipe width is 70
        new_pipe_y = random.randint(150, 450)  # Random height for the new pipe
        pipes.append([SCREEN_WIDTH, new_pipe_y, False])  # Add new pipe
        pipes.pop(0)  # Remove the oldest pipe

def check_collision(bird_pos, pipes):
    bird_rect = pygame.Rect(bird_pos[0] - 15, bird_pos[1] - 15, 30, 30)  # Bird's hitbox
    for pipe in pipes:
        upper_pipe_rect = pygame.Rect(pipe[0], 0, 70, pipe[1])
        lower_pipe_rect = pygame.Rect(pipe[0], pipe[1] + 200, 70, SCREEN_HEIGHT - pipe[1] - 200)
        if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
            return True
    return False

def display_score(score, high_score):
    score_surface = font.render(f"Score: {score}", True, TEXT_COLOR)
    high_score_surface = font.render(f"High Score: {high_score}", True, TEXT_COLOR)
    screen.blit(score_surface, (10, 10))
    screen.blit(high_score_surface, (10, 40))

def display_message(message):
    message_surface = font.render(message, True, TEXT_COLOR)
    screen.blit(message_surface, (SCREEN_WIDTH / 2 - message_surface.get_width() / 2, SCREEN_HEIGHT / 2))

def game_loop():
    bird_pos = [100, SCREEN_HEIGHT / 2]
    bird_vel = 0
    gravity = 0.25
    jump_height = -7  # Adjusted for lesser vertical jumps
    pipes = [[SCREEN_WIDTH, 300, False]]  # Initial pipe
    score = 0
    high_score = get_high_score()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_vel = jump_height

        bird_vel += gravity
        bird_pos[1] += bird_vel

        screen.fill(BACKGROUND_COLOR)
        draw_pipes(pipes)
        update_pipes(pipes)
        draw_bird(bird_pos)

        # Scoring
        pipe_passed = pipes[0][0] + 70 < bird_pos[0] and not pipes[0][2]
        if pipe_passed:
            score += 1
            pipes[0][2] = True  # Mark pipe as passed

        display_score(score, high_score)

        if bird_pos[1] >= SCREEN_HEIGHT or bird_pos[1] <= 0 or check_collision(bird_pos, pipes):
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            display_message("Game Over! Press R to Restart")
            pygame.display.flip()
            waitForRestart = True
            while waitForRestart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game_loop()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

        pygame.display.update()
        clock.tick(30)

game_loop()
