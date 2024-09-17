import pygame
from classes import Player, Vector, Ray
import random
import numpy as np

# Define the game map
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CELL_SIZE = 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycasting")

# Define movement speed
MOVEMENT_SPEED = 0.15

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
    # USE WASD

    if game_map[int(player.pos.y)][int(player.pos.x)] == 1:
        player.pos = Vector([5,5])

    if keys[pygame.K_w]:
        player.move(Vector([0, -MOVEMENT_SPEED]))
    if keys[pygame.K_s]:
        player.move(Vector([0, MOVEMENT_SPEED]))
    if keys[pygame.K_a]:
        player.move(Vector([-MOVEMENT_SPEED, 0]))
    if keys[pygame.K_d]:
        player.move(Vector([MOVEMENT_SPEED, 0]))


    mouse_pos = pygame.mouse.get_pos()

    player.dir = Vector([mouse_pos[0] - player.pos.x * CELL_SIZE, mouse_pos[1] - player.pos.y * CELL_SIZE]).normalise()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw map
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, (255, 255, 255), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw player whose size is relative to the map
    pygame.draw.circle(screen, (255, 0, 0), (int(player.pos.x * CELL_SIZE), int(player.pos.y * CELL_SIZE)), 5)

    # draw player direction
    pygame.draw.line(screen, (0, 255, 0), (player.pos.x * CELL_SIZE, player.pos.y * CELL_SIZE), (player.pos.x * CELL_SIZE + player.dir.x * CELL_SIZE, player.pos.y * CELL_SIZE + player.dir.y * CELL_SIZE), 2)

    hit_lst = Ray.sendRays(player, game_map)

    for hit in hit_lst:
        pygame.draw.circle(screen, (0, 0, 255), (int(hit.x * CELL_SIZE), int(hit.y * CELL_SIZE)), 5)
        pygame.draw.line(screen, (0, 0, 255), (player.pos.x * CELL_SIZE, player.pos.y * CELL_SIZE), (hit.x * CELL_SIZE, hit.y * CELL_SIZE), 2)
    
    # Update the display
    pygame.display.flip()
    
    pygame.time.Clock().tick(60)  # Cap the frame rate

pygame.quit()
