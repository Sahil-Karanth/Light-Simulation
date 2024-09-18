import random

import numpy as np
import pygame

from classes import Player, Ray, Vector
from values import Values

def load_map(file):
    with open(file, "r") as file:
        return [[int(cell) for cell in line if cell != "\n"] for line in file]

game_map = load_map("map.txt")

pygame.init()

screen = pygame.display.set_mode((Values.SCREEN_WIDTH, Values.SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting")

# Define movement speed
MOVEMENT_SPEED = 1

# Create player instance
player = Player([4.5, 4.5], [0, -1])

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

    if keys[pygame.K_LEFT]:
        player.dir = player.dir.rotate(-0.1)
    elif keys[pygame.K_RIGHT]:
        player.dir = player.dir.rotate(0.1)

    simulate_next_pos = player.pos + next_move

    # Check if the next position is a wall
    if game_map[int(simulate_next_pos.y)][int(simulate_next_pos.x)]:
        continue

    player.pos += next_move


    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw map
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell:
                # outline the cell with a line
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (x * Values.CELL_SIZE, y * Values.CELL_SIZE, Values.CELL_SIZE, Values.CELL_SIZE),
                    1,
                )

    # Draw player whose size is relative to the map
    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (int(player.pos.x * Values.CELL_SIZE), int(player.pos.y * Values.CELL_SIZE)),
        10,
    )


    hit_lst = Ray.sendRays(player, game_map, "primitive")

    for hit in hit_lst:
        pygame.draw.circle(
            screen, (0, 0, 255), (int(hit.x * Values.CELL_SIZE), int(hit.y * Values.CELL_SIZE)), 1
        )
        pygame.draw.line(
            screen,
            (0, 0, 255),
            (player.pos.x * Values.CELL_SIZE, player.pos.y * Values.CELL_SIZE),
            (hit.x * Values.CELL_SIZE, hit.y * Values.CELL_SIZE),
            2,
        )

        # calculate distance
        distance = (
            Vector([hit.x - player.pos.x, hit.y - player.pos.y]).magnitude() * Values.CELL_SIZE
        )

    # exit()
    # Update the display
    pygame.display.flip()

    pygame.time.Clock().tick(60)  # Cap the frame rate


pygame.quit()
