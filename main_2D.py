import random

import numpy as np
import pygame

from classes import Player, Ray, Vector
from values import Values


def load_map(file):
    with open(file, "r") as file:
        return [[int(cell) for cell in line if cell != "\n"] for line in file]


def draw_grid_cell(screen, x, y):
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (
            x * Values.CELL_SIZE,
            y * Values.CELL_SIZE,
            Values.CELL_SIZE,
            Values.CELL_SIZE,
        ),
        1,
    )


def draw_player(screen, player):
    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (int(player.pos.x * Values.CELL_SIZE), int(player.pos.y * Values.CELL_SIZE)),
        10,
    )


def draw_ray(screen, start_vec, end_vec, colour=(0, 0, 255), alpha=255):

    ray_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    
    pygame.draw.line(
        ray_surface,
        (*colour, alpha),
        (start_vec.x * Values.CELL_SIZE, start_vec.y * Values.CELL_SIZE),
        (end_vec.x * Values.CELL_SIZE, end_vec.y * Values.CELL_SIZE),
        5,
    )
    
    screen.blit(ray_surface, (0, 0))



def get_wasd_move(keys):

    if keys[pygame.K_w]:
        next_move = Vector([0, -Values.MOVEMENT_SPEED])
    elif keys[pygame.K_s]:
        next_move = Vector([0, Values.MOVEMENT_SPEED])
    elif keys[pygame.K_a]:
        next_move = Vector([-Values.MOVEMENT_SPEED, 0])
    elif keys[pygame.K_d]:
        next_move = Vector([Values.MOVEMENT_SPEED, 0])
    else:
        next_move = Vector([0, 0])

    return next_move


def update_player_rotation(keys, player):

    if keys[pygame.K_LEFT]:
        player.dir = player.dir.rotate(-0.05)
    elif keys[pygame.K_RIGHT]:
        player.dir = player.dir.rotate(0.05)


def draw_map(screen, game_map):
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell:
                draw_grid_cell(screen, x, y)


def main():

    game_map = load_map("map.txt")

    pygame.init()

    screen = pygame.display.set_mode((Values.SCREEN_WIDTH, Values.SCREEN_HEIGHT))
    pygame.display.set_caption("Raycasting")

    player = Player([4.5, 4.5], [0, -1])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player movement
        keys = pygame.key.get_pressed()

        next_move = get_wasd_move(keys)

        # update_player_rotation(keys, player)
        mouse_pos = pygame.mouse.get_pos()
        player.dir = Vector(
            [
                mouse_pos[0] - player.pos.x * Values.CELL_SIZE,
                mouse_pos[1] - player.pos.y * Values.CELL_SIZE,
            ]
        ).normalise()

        simulate_next_pos = player.pos + next_move

        # Check if the next position is a wall
        if game_map[int(simulate_next_pos.y)][int(simulate_next_pos.x)]:
            continue

        player.pos += next_move

        screen.fill((0, 0, 0))

        draw_map(screen, game_map)

        draw_player(screen, player)

        hit_lst = Ray.initialRayCast(player, game_map, "primitive")
        for hit in hit_lst:

            draw_ray(screen, player.pos, hit.pos)
            curr_hit = hit

            for _ in range(Values.NUM_REFLECTIONS):
                new_ray = Ray.reflectRay(curr_hit, curr_hit.ray.intensity / 2)
                new_hit = new_ray.cast(game_map, "primitive")
                draw_ray(screen, new_ray.pos, new_hit.pos, alpha=new_ray.intensity)

                curr_hit = new_hit

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
