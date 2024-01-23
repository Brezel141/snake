
# Importing required libraries
import pygame as pg
import random

# Initial settings for the game display
dis_height = 500
dis_width = 500
display_surf = pg.display.set_mode([dis_height,dis_width])
window = 1000
tile_size = 50
range_vals = (tile_size // 2, window - tile_size // 2, tile_size)
get_random_position = lambda: [random.randrange(*range_vals), random.randrange(*range_vals)]

# Initialize the starting position and the snake
start_position = (window / 2 , window / 2)
snake = pg.rect.Rect([0, 0, tile_size - 2, tile_size - 2])
snake.center = get_random_position()
snake_dir = (0, 0)
length = 1
segments = [snake.copy()]

# Initialize food and score
food = snake.copy()
food.center = get_random_position()
score = 0
screen = pg.display.set_mode([window] * 2)
clock = pg.time.Clock()
time, time_step = 0, 330
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

# Initialize Pygame fonts
pg.font.init()
score_font = pg.font.SysFont("Arial", 11)

# Main game loop
while True:
    # Event handling
    for event in pg.event.get():
        # Check for quit event
        if event.type == pg.QUIT:
            exit()

        # Handling keyboard input for snake movement
        if event.type == pg.KEYDOWN:
            # Move up if 'W' is pressed and it's a valid direction
            if event.key == pg.K_w and dirs[pg.K_w]:
                snake_dir = (0, -tile_size)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            # Move down if 'S' is pressed and it's a valid direction
            if event.key == pg.K_s and dirs[pg.K_s]:
                snake_dir = (0, tile_size)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            # Move left if 'A' is pressed and it's a valid direction
            if event.key == pg.K_a and dirs[pg.K_a]:
                snake_dir = (-tile_size, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            # Move right if 'D' is pressed and it's a valid direction
            if event.key == pg.K_d and dirs[pg.K_d]:
                snake_dir = (tile_size, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    # Fill the screen with black color
    screen.fill('black')

    # Check for snake hitting the borders or eating itself
    if snake.left < 0 or snake.right > window or snake.top < 0 or snake.bottom > window or pg.Rect.collidelist(snake, segments[:-1]) != -1:
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]

    # Check if snake eats the food
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1
        score += 5      # Add to the score 
        time_step -= 5  # Decrease the time_step to increase speed

    # Draw food on the screen
    pg.draw.rect(screen, 'red', food)

    # Draw snake on the screen
    [pg.draw.rect(screen, 'green', segment) for segment in segments]

    # Move the snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]

    # Render and display the score
    score_text = score_font.render(f"Score: {score}", True, 'white')
    display_surf.blit(score_text, (10, 10))

    # Update the display and set the game clock
    pg.display.flip()
    clock.tick(60)
