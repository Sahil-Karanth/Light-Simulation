import random
from copy import deepcopy

import numpy as np
import pyautogui as pg
import pygame

from classes import Player, Ray, Vector, to_degrees
from SettingsWindow import SettingsWindow
from values import Values

# TODO:
# - fix diffuse reflection
# - add a refractive index to the ray class and slider to adjust
# - TIR

def make_map():
    width = Values.get_value("SCREEN_WIDTH") // Values.get_value("CELL_SIZE")
    height = Values.get_value("SCREEN_HEIGHT") // Values.get_value("CELL_SIZE")

    with open("map.txt", "w") as file:

        file.write("2" * width + "\n")
        for i in range(height - 2):
            file.write(f"2{'0'*(width-2)}2\n")
        file.write("2" * width + "\n")


def load_map(file):
    with open(file, "r") as file:
        return [[int(cell) for cell in line if cell != "\n"] for line in file]


def draw_grid_cell(screen, x, y, fill_color):
    # pygame.draw.rect(
    #     screen,
    #     fill_color,
    #     (
    #         x * Values.get_value("CELL_SIZE"),
    #         y * Values.get_value("CELL_SIZE"),
    #         Values.get_value("CELL_SIZE"),
    #         Values.get_value("CELL_SIZE"),
    #     ),
    # )

    pygame.draw.rect(
        screen,
        (255,255,255),
        (
            x * Values.get_value("CELL_SIZE"),
            y * Values.get_value("CELL_SIZE"),
            Values.get_value("CELL_SIZE"),
            Values.get_value("CELL_SIZE"),
        ),
        1
    )


def check_for_map_changes(game_map, mouse_pos, player):

    loc = [
        int(mouse_pos[0] / Values.get_value("CELL_SIZE")),
        int(mouse_pos[1] / Values.get_value("CELL_SIZE")),
    ]

    if pygame.mouse.get_pressed()[0]:

        if game_map[loc[1]][loc[0]] == 0 and loc != [
            int(player.pos.x),
            int(player.pos.y),
        ]:
            game_map[loc[1]][loc[0]] = 1

    # if you right click on the screen, it will remove a wall
    if pygame.mouse.get_pressed()[2]:

        loc = [
            int(mouse_pos[0] / Values.get_value("CELL_SIZE")),
            int(mouse_pos[1] / Values.get_value("CELL_SIZE")),
        ]

        if game_map[loc[1]][loc[0]] == 1:
            game_map[loc[1]][loc[0]] = 0


def draw_player(screen, player):
    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (
            int(player.pos.x * Values.get_value("CELL_SIZE")),
            int(player.pos.y * Values.get_value("CELL_SIZE")),
        ),
        10,
    )


def draw_ray(screen, start_vec, end_vec, colour=(255, 255, 0), alpha=255):

    ray_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    pygame.draw.line(
        ray_surface,
        (*colour, alpha),
        (
            start_vec.x * Values.get_value("CELL_SIZE"),
            start_vec.y * Values.get_value("CELL_SIZE"),
        ),
        (
            end_vec.x * Values.get_value("CELL_SIZE"),
            end_vec.y * Values.get_value("CELL_SIZE"),
        ),
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
    start_pos = (
        start_vec.x * Values.get_value("CELL_SIZE"),
        start_vec.y * Values.get_value("CELL_SIZE"),
    )
    end_pos = (
        end_vec.x * Values.get_value("CELL_SIZE"),
        end_vec.y * Values.get_value("CELL_SIZE"),
    )

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
        next_move = Vector([0, -Values.get_value("MOVEMENT_SPEED")])
    elif keys[pygame.K_s]:
        next_move = Vector([0, Values.get_value("MOVEMENT_SPEED")])
    elif keys[pygame.K_a]:
        next_move = Vector([-Values.get_value("MOVEMENT_SPEED"), 0])
    elif keys[pygame.K_d]:
        next_move = Vector([Values.get_value("MOVEMENT_SPEED"), 0])
    else:
        next_move = Vector([0, 0])

    return next_move


def get_instruction_text():

    with open("instructions.txt", "r") as file:
        return file.read()


def update_player_rotation(keys, player):

    if keys[pygame.K_LEFT]:
        player.dir = player.dir.rotate(-0.05)
    elif keys[pygame.K_RIGHT]:
        player.dir = player.dir.rotate(0.05)


def draw_map(screen, game_map):
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 1:
            
                if Values.get_value("Reflection_Mode") == "Reflection":
                    draw_grid_cell(screen, x, y, fill_color=(200, 200, 200))

                elif Values.get_value("Reflection_Mode") == "Refraction":
                    draw_grid_cell(screen, x, y, fill_color=(0, 0, 139))

            elif cell == 2:
                draw_grid_cell(screen, x, y, fill_color=(200, 200, 200))                


def check_for_settings_open():
    if pygame.key.get_pressed()[pygame.K_p]:
        print("Opening settings window")
        settings_window = SettingsWindow()
        settings_window.run()

def perform_trace(player, game_map, screen, hit_lst):
    for hit in hit_lst:
        draw_fading_ray(
            screen,
            player.pos,
            hit.pos,
            alpha_start=hit.ray.intensity,
            alpha_end=hit.ray.intensity / Values.get_value("Decay_Factor"),
            segments=50,
        )
        curr_hit = hit

        if Values.get_value("Reflection_Mode") == "Reflection":

            for _ in range(Values.get_value("Max_Reflections")):
                new_intensity = curr_hit.ray.intensity / Values.get_value(
                    "Decay_Factor"
                )

                if new_intensity < 1:
                    break


                if not curr_hit.wall_orientation:
                    break

                new_ray = Ray.reflectRay(curr_hit, new_intensity)
                new_hit = new_ray.cast(game_map, refracting=False)

                draw_fading_ray(
                    screen,
                    new_ray.pos,
                    new_hit.pos,
                    alpha_start=new_ray.intensity,
                    alpha_end=new_ray.intensity / Values.get_value("Decay_Factor"),
                    segments=50,
                )

                curr_hit = new_hit

        elif Values.get_value("Reflection_Mode") == "Refraction" and hit.cell_value != 2:

            for _ in range(Values.get_value("Max_Reflections")):

                refraction_angles = Ray.get_refraction_angles(curr_hit, going_to_air=False)

                # print("ANGLE OF INCIDENCE: ", to_degrees(refraction_angles.incident_angle))

                if not refraction_angles:
                    break

                new_ray = Ray.refractRay(curr_hit, refraction_angles, 255)

                if not new_ray:
                    break

                new_hit = new_ray.cast(game_map, refracting=True)

                if new_hit.cell_value == 2:
                    break
                
                draw_fading_ray(
                    screen,
                    new_ray.pos,
                    new_hit.pos,
                    alpha_start=new_ray.intensity,
                    alpha_end=new_ray.intensity / Values.get_value("Decay_Factor"),
                    segments=50,
                )

                # now we've done the first refraction into the block until it hits the boundary from wall to air
                max_iter = 10
            
                refraction_angles = Ray.get_refraction_angles(new_hit, going_to_air=True)
                if not refraction_angles:
                    break
                if refraction_angles.incident_angle > refraction_angles.critical_angle:
                    TIR_again = True

                else:
                    TIR_again = False

                while max_iter > 0 and TIR_again:

                    TIR_ray = Ray.reflectRay(new_hit, new_ray.intensity)

                    if not TIR_ray:
                        break

                    TIR_hit = TIR_ray.cast(game_map, refracting=True)

                    draw_fading_ray(
                        screen,
                        TIR_ray.pos,
                        TIR_hit.pos,
                        alpha_start=TIR_ray.intensity,
                        alpha_end=TIR_ray.intensity / Values.get_value("Decay_Factor"),
                        segments=50,
                    )

                    # determine if TIR should happen again

                    refraction_angles = Ray.get_refraction_angles(TIR_hit)

                    if not refraction_angles:
                        break

                    if refraction_angles.incident_angle > refraction_angles.critical_angle:
                        TIR_again = True

                    else:
                        TIR_again = False
                        print(f"NO TIR AGAIN LEAVING ON INCIDENT ANGLE: {to_degrees(refraction_angles.incident_angle)}")

                    new_hit = TIR_hit



                # now TIR is done (or never happened), we need to refract back into the air

                refraction_angles = Ray.get_refraction_angles(new_hit, going_to_air=True)

                if refraction_angles.incident_angle > refraction_angles.critical_angle:
                    break

                new_ray = Ray.refractRay(new_hit, refraction_angles, 255, going_to_air=True)

                new_hit = new_ray.cast(game_map, refracting=False)

                draw_fading_ray(
                    screen,
                    new_ray.pos,
                    new_hit.pos,
                    alpha_start=new_ray.intensity,
                    alpha_end=new_ray.intensity / Values.get_value("Decay_Factor"),
                    segments=50,
                )

                curr_hit = new_hit





def main():

    make_map()
    game_map = load_map("map.txt")

    pygame.init()

    screen = pygame.display.set_mode(
        (Values.get_value("SCREEN_WIDTH"), Values.get_value("SCREEN_WIDTH"))
    )
    pygame.display.set_caption(
        "Raycasting | press 'p' to open settings | press 'f' to freeze (good for diffuse)"
    )

    screen.fill((0, 0, 0))

    player = Player([4.5, 4.5], [0, -1])

    settings_window = SettingsWindow()
    settings_window.run()

    frozen = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    frozen = not frozen

        check_for_settings_open()

        if not frozen:

            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            next_move = get_wasd_move(keys)

            check_for_map_changes(game_map, mouse_pos, player)

            # Update player direction
            player.dir = Vector(
                [
                    mouse_pos[0] - player.pos.x * Values.get_value("CELL_SIZE"),
                    mouse_pos[1] - player.pos.y * Values.get_value("CELL_SIZE"),
                ]
            ).normalise()


            simulate_next_pos = player.pos + next_move

            # Check if the next position is a wall
            if not game_map[int(simulate_next_pos.y)][int(simulate_next_pos.x)]:
                player.pos += next_move

            screen.fill((0, 0, 0))

            draw_map(screen, game_map)
            draw_player(screen, player)

            hit_lst = Ray.initialRayCast(player, game_map)

            perform_trace(player, game_map, screen, hit_lst)


        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
