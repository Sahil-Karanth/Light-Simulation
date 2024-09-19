import random
from copy import deepcopy

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


def check_for_map_changes(game_map, mouse_pos, player):

    loc = [
        int(mouse_pos[0] / Values.CELL_SIZE),
        int(mouse_pos[1] / Values.CELL_SIZE),
    ]

    if pygame.mouse.get_pressed()[0]:

        if game_map[loc[1]][loc[0]] == 0 and loc != [int(player.pos.x), int(player.pos.y)]:
            game_map[loc[1]][loc[0]] = 1

    # if you right click on the screen, it will remove a wall
    if pygame.mouse.get_pressed()[2]:

        loc = [
            int(mouse_pos[0] / Values.CELL_SIZE),
            int(mouse_pos[1] / Values.CELL_SIZE),
        ]

        if game_map[loc[1]][loc[0]] == 1:
            game_map[loc[1]][loc[0]] = 0

def draw_player(screen, player):
    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (int(player.pos.x * Values.CELL_SIZE), int(player.pos.y * Values.CELL_SIZE)),
        10,
    )


def draw_ray(screen, start_vec, end_vec, colour=(255, 255, 0), alpha=255):

    ray_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    pygame.draw.line(
        ray_surface,
        (*colour, alpha),
        (start_vec.x * Values.CELL_SIZE, start_vec.y * Values.CELL_SIZE),
        (end_vec.x * Values.CELL_SIZE, end_vec.y * Values.CELL_SIZE),
        5,
    )

    screen.blit(ray_surface, (0, 0))


def draw_fading_ray(
    screen,
    start_vec,
    end_vec,
    colour=(255, 204, 0),
    alpha_start=255,
    alpha_end=0,
    segments=50,
):
    # Create a transparent surface
    ray_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    # Get start and end positions in pixel space
    start_pos = (start_vec.x * Values.CELL_SIZE, start_vec.y * Values.CELL_SIZE)
    end_pos = (end_vec.x * Values.CELL_SIZE, end_vec.y * Values.CELL_SIZE)

    # Calculate the difference between the start and end positions
    delta_x = (end_pos[0] - start_pos[0]) / segments
    delta_y = (end_pos[1] - start_pos[1]) / segments

    # Loop over the segments
    for i in range(segments):
        # Calculate the start and end points of the segment
        segment_start = (start_pos[0] + i * delta_x, start_pos[1] + i * delta_y)
        segment_end = (
            start_pos[0] + (i + 1) * delta_x,
            start_pos[1] + (i + 1) * delta_y,
        )

        # Calculate the current alpha value based on the segment index
        alpha = int(alpha_start + (alpha_end - alpha_start) * (i / segments))

        # Draw the segment with the current alpha value
        pygame.draw.line(
            ray_surface,
            (*colour, alpha),
            segment_start,
            segment_end,
            5,
        )

    # Blit the surface with the fading ray onto the main screen
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
        mouse_pos = pygame.mouse.get_pos()

        next_move = get_wasd_move(keys)

        check_for_map_changes(game_map, mouse_pos, player)

        # update_player_rotation(keys, player)
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

            # draw_ray(screen, player.pos, hit.pos)
            draw_fading_ray(
                screen,
                player.pos,
                hit.pos,
                alpha_start=hit.ray.intensity,
                alpha_end=hit.ray.intensity / Values.DECAY_FACTOR_REFLECTION,
                segments=50,
            )
            curr_hit = hit

            for _ in range(Values.MAX_REFLECTIONS):

                new_intensity = curr_hit.ray.intensity / Values.DECAY_FACTOR_REFLECTION

                if new_intensity < 1:
                    break

                new_ray = Ray.reflectRay(curr_hit, new_intensity)
                new_hit = new_ray.cast(game_map, "primitive")

                # draw_ray(screen, new_ray.pos, new_hit.pos, alpha=new_ray.intensity)

                draw_fading_ray(
                    screen,
                    new_ray.pos,
                    new_hit.pos,
                    alpha_start=new_ray.intensity,
                    alpha_end=new_ray.intensity / Values.DECAY_FACTOR_REFLECTION,
                    segments=50,
                )

                curr_hit = new_hit

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
