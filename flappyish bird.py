import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 50, HEIGHT // 2
BIRD_RADIUS = 15
gravity = 0.5
jump_strength = -8
pipe_width = 60
gap_height = 150
pipe_speed = 3
score = 0


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

lives = 3

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load assets
bird_images = [
    pygame.image.load("./images/redbird-downflap.png").convert_alpha(),
    pygame.image.load("./images/redbird-midflap.png").convert_alpha(),
    pygame.image.load("./images/redbird-upflap.png").convert_alpha(),
]
background = pygame.image.load("./images/background-day.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

ground_image = pygame.image.load("./images/base.png").convert_alpha()
ground_image = pygame.transform.scale(ground_image, (WIDTH, ground_image.get_height()))

pipe_image = pygame.image.load("./images/pipe-green.png").convert_alpha()  
pipe_image_flipped = pygame.transform.flip(pipe_image, False, True)

# Clock for frame rate
clock = pygame.time.Clock() 

# Game State
game_started = False
playing = True

# Bird attributes
bird_y = BIRD_Y
bird_velocity = 0
bird_frame = 0

# Pipe attributes
pipes = []

def create_pipe():
    """Creates a pipe with random height and movement direction."""
    min_height = 50
    max_height = HEIGHT - gap_height - 50
    height = random.randint(min_height, max_height)  
    pipes.append([WIDTH , height , random.choice([-1, 1])])  # 

def move_pipes():
    """Moves pipes left and adds vertical movement."""
    global score
    for pipe in pipes:
        pipe[0] -= pipe_speed
        pipe[1] += pipe[2] * 2
        
        # Reverse movement if hitting bounds
        if pipe[1] <= 50 or pipe[1] >= HEIGHT - gap_height - 50:   
            pipe[2] *= -1  

    # Remove pipes that go off-screen and increase score
    if pipes and pipes[0][0] + pipe_width < 0:
        pipes.pop(0)
        score += 1  

def draw_pipes():
    """Draws all pipes on the screen."""
    for pipe in pipes:
        top_pipe_height = pipe[1] 
        bottom_pipe_y = pipe[1] + gap_height
        screen.blit(pygame.transform.scale(pipe_image_flipped, (pipe_width, top_pipe_height)), (pipe[0], 0))
        screen.blit(pygame.transform.scale(pipe_image, (pipe_width, HEIGHT - bottom_pipe_y)), (pipe[0], bottom_pipe_y))   


def reset_bird():
    """Resets the bird position after losing a life."""
    global bird_y, bird_velocity, pipes
    bird_y = BIRD_Y  # Reset to initial position
    bird_velocity = 0
    pipes.clear()  # Remove all pipes so player has a fresh start

def check_collision():
    """Checks if the bird has collided with the ground, ceiling, or pipes."""
    global lives, bird_y, bird_velocity, pipes

    if bird_y - BIRD_RADIUS <= 0 or bird_y + BIRD_RADIUS >= HEIGHT:
        lives -= 1
        reset_bird()
        return lives <= 0  # If no lives left, return True to end game

    for pipe in pipes:
        if BIRD_X + BIRD_RADIUS > pipe[0] and BIRD_X - BIRD_RADIUS < pipe[0] + pipe_width:
            if bird_y - BIRD_RADIUS < pipe[1] or bird_y + BIRD_RADIUS > pipe[1] + gap_height:
                lives -= 1
                reset_bird()
                return lives <= 0  

    return False

def draw_bird():
    """Animates and draws the bird."""
    global bird_frame
    bird_frame = (bird_frame + 1) % len(bird_images)  
    screen.blit(bird_images[bird_frame], (BIRD_X - BIRD_RADIUS, int(bird_y - BIRD_RADIUS)))

def show_score():
    """Displays the current score."""
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

def show_menu():
    """Displays the main menu with an image before the game starts."""
    menu_image = pygame.image.load("./images/message.png").convert_alpha()
    menu_rect = menu_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill(WHITE)  # Optional, in case the image has transparency
    screen.blit(menu_image, menu_rect)
    pygame.display.update()

def show_paused():
    """Displays the pause message."""
    font = pygame.font.Font(None, 48)
    text = font.render("Paused", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 2 - 25))

def show_lives():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(text, (WIDTH - 100, 10))

# Game loop
running = True
frame_count = 0

while running:
    if not game_started:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_started = True
                # Reset game state on restart
                bird_y = BIRD_Y
                bird_velocity = 0
                pipes.clear()
                score = 0
                frame_count = 0
    else:
        screen.blit(background, (0, 0))
        screen.blit(ground_image, (0, HEIGHT - ground_image.get_height()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength
                if event.key == pygame.K_p:
                    playing = not playing  

        if playing:
            # Bird physics
            bird_velocity += gravity
            bird_y += bird_velocity

            # Pipe handling
            if frame_count % 90 == 0:
                create_pipe()
            move_pipes()

            # Drawing
            draw_pipes()
            draw_bird()
            show_score()
            show_lives()

            # Check for collisions
            if check_collision():
                if lives <= 0:
                    running = False
                else:
                    show_lives()
                

            frame_count += 1
        else:
            show_paused()

    pygame.display.update()
    clock.tick(30)

pygame.quit()


