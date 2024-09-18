import random

import numpy as np
import pygame

from classes import Player, Ray, Vector

# Define the game map
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting")

# Define movement speed
MOVEMENT_SPEED = 0.1

# Create player instance
player = Player([4.5, 4.5], [1, 0])

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        next_move = Vector([0, -MOVEMENT_SPEED])
    elif keys[pygame.K_s]:
        next_move = Vector([0, MOVEMENT_SPEED])
    elif keys[pygame.K_a]:
        next_move = Vector([-MOVEMENT_SPEED, 0])
    elif keys[pygame.K_d]:
        next_move = Vector([MOVEMENT_SPEED, 0])
    else:
        next_move = Vector([0, 0])

    # use arrow keys to rotate
    # if keys[pygame.K_LEFT]:
    #     player.dir = player.dir.rotate(-0.1)
    # elif keys[pygame.K_RIGHT]:
    #     player.dir = player.dir.rotate(0.1)

    simulate_next_pos = player.pos + next_move

    # Check if the next position is a wall
    if game_map[int(simulate_next_pos.y)][int(simulate_next_pos.x)]:
        continue

    player.pos += next_move

    mouse_pos = Vector(list(pygame.mouse.get_pos()))

    player.dir = Vector(
        [
            mouse_pos.x - player.pos.x * CELL_SIZE,
            mouse_pos.y - player.pos.y * CELL_SIZE,
        ]
    ).normalise()

    # Clear the screen
    screen.fill((0, 0, 0))

    hit_lst = Ray.sendRays(player, game_map, "primitive")

    for hit in hit_lst:

        line_height = 1/(hit.x) * SCREEN_HEIGHT

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (hit.x * CELL_SIZE, SCREEN_HEIGHT / 2 - line_height / 2),
            (hit.x * CELL_SIZE, SCREEN_HEIGHT / 2 + line_height / 2),
        )

    pygame.display.flip()

    pygame.time.Clock().tick(60)  # Cap the frame rate


pygame.quit()
