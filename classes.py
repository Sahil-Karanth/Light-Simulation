import math

import numpy as np
import pyautogui as pg
import colorama

from values import Values

colorama.init()


def to_degrees(rad):
    return rad * 180 / math.pi

class Vector:
    def __init__(self, lst):
        self.values = list(lst)
        self.x = lst[0]
        self.y = lst[1]
        self.ndim = len(lst)

    def __add__(self, vec2):
        return Vector([a + b for a, b in zip(self.values, vec2.values)])

    def __sub__(self, vec2):
        return Vector([a - b for a, b in zip(self.values, vec2.values)])

    def __mul__(self, scalar):
        return Vector([a * scalar for a in self.values])

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return Vector([a / scalar for a in self.values])

    def __str__(self):
        return f"Vector({self.values})"

    def dotProd(self, vec2):
        return sum([a * b for a, b in zip(self.values, vec2.values)])

    def magnitude(self):
        return math.sqrt(sum([a**2 for a in self.values]))

    def normalise(self):
        mag = self.magnitude()
        if mag == 0:
            return ValueError("Cannot normalise the zero vector.")
        return self / mag

    def rotate(self, angle):
        return Vector(
            [
                self.x * math.cos(angle) - self.y * math.sin(angle),
                self.x * math.sin(angle) + self.y * math.cos(angle),
            ]
        )

    def get_angle(self):
        return math.atan2(self.y, self.x)


class Player:
    def __init__(self, pos, dir):
        self.pos = Vector(pos)
        self.dir = Vector(dir).normalise()
        self.fov = Values.get_value("Field_Of_View")

    def move(self, dir):
        self.pos += dir


class Ray:
    def __init__(self, pos, dir, intensity=255, TIR=False):
        self.pos = pos
        self.dir = dir.normalise()
        self.intensity = intensity
        self.TIR = TIR

    def __str__(self):
        return f"r = {self.pos.values} + t{self.dir.values}"

    @staticmethod
    def initialRayCast(player, map):

        def loop_code(ray):
    
            hit = ray.cast(map, refracting=False)

            if hit:
                return hit

        num_rays = Values.get_value("Number_Of_Rays")

        if num_rays == 1:
            ray = Ray(player.pos, player.dir)
            return [loop_code(ray)]

        hit_lst = []

        for angle in np.linspace(
            -player.fov / 2, player.fov / 2, num_rays
        ):
            ray = Ray(player.pos, player.dir.rotate(angle))

            hit_lst.append(loop_code(ray))

        return hit_lst
    

    def __specularReflectRay(hit, new_intensity):
        if hit.wall_orientation == "horizontal":
            new_dir = Vector([hit.ray.dir.x, hit.ray.dir.y * -1])
        elif hit.wall_orientation == "vertical":
            new_dir = Vector([hit.ray.dir.x * -1, hit.ray.dir.y])
        else:
            raise ValueError("Invalid wall orientation.")

        new_ray = Ray(hit.pos, new_dir, new_intensity)

        return new_ray

    def __diffuseReflectRay(hit, new_intensity):
        if hit.wall_orientation == "vertical":
            max_angle = math.pi / 2
            min_angle = 0

        elif hit.wall_orientation == "horizontal":
            max_angle = math.pi
            min_angle = math.pi / 2

        else:
            raise ValueError("Invalid wall orientation.")

        angle = np.random.uniform(min_angle, max_angle)

        new_dir = hit.ray.dir.rotate(angle)

        new_ray = Ray(hit.pos, new_dir, new_intensity)

        return new_ray

    @staticmethod
    def reflectRay(hit, new_intensity):

        if Values.get_value("Reflection_Type") == "Specular":
            return Ray.__specularReflectRay(hit, new_intensity)
        elif Values.get_value("Reflection_Type") == "Diffuse":
            return Ray.__diffuseReflectRay(hit, new_intensity)

    @staticmethod
    def __get_incidence_angle(angle, wall_orientation):

        if angle < 0 and angle >= -math.pi / 2:
            new_angle = -angle

        elif angle < -math.pi / 2 and angle >= -math.pi:
            new_angle = math.pi + angle 

        elif angle > 0 and angle <= math.pi / 2:
            new_angle = angle

        elif angle > math.pi / 2 and angle <= math.pi:
            new_angle = math.pi - angle

        else:
            raise ValueError("Invalid angle value.")
        
        if wall_orientation == "vertical":
            return new_angle
        
        elif wall_orientation == "horizontal":
            return math.pi / 2 - new_angle

    @staticmethod
    def refractRay(hit, new_intensity):

        ray_angle = hit.ray.dir.get_angle()

        if not hit.wall_orientation:
            return
        
        incident_angle = Ray.__get_incidence_angle(ray_angle, hit.wall_orientation)


        refracted_angle = np.arcsin(
            np.sin(incident_angle) / Values.get_value("Refractive_Index")
        )

        # Calculate the new direction based on the refracted angle
        if hit.wall_orientation == "vertical":
            new_dir = Vector([
                math.cos(refracted_angle) * (-1 if hit.ray.dir.x < 0 else 1),
                math.sin(refracted_angle) * (-1 if hit.ray.dir.y < 0 else 1)
            ])
        elif hit.wall_orientation == "horizontal":
            new_dir = Vector([
                math.sin(refracted_angle) * (-1 if hit.ray.dir.x < 0 else 1),
                math.cos(refracted_angle) * (-1 if hit.ray.dir.y < 0 else 1)
            ])
        

        critical_angle = np.arcsin(1 / Values.get_value("Refractive_Index"))

        if incident_angle > critical_angle and hit.prev_cell_value == 0 and hit.cell_value == 1:
            return Ray(hit.pos, new_dir, new_intensity, TIR=True)

        return Ray(hit.pos, new_dir, new_intensity)

    def cast(self, map, refracting, max_iter=100000):
        def handle_hit(current_pos, prev_pos, map):
            hit_wall_orientation = None

            if int(current_pos.x) != int(prev_pos.x):
                hit_wall_orientation = "vertical"
            elif int(current_pos.y) != int(prev_pos.y):
                hit_wall_orientation = "horizontal"

            prev_cell_value = map[int(prev_pos.y)][int(prev_pos.x)]
            return Hit(current_pos, self, hit_wall_orientation, map[int(current_pos.y)][int(current_pos.x)], prev_cell_value)

        current_pos = Vector([self.pos.x, self.pos.y])
        increment_vector = self.dir * 0.1
        stop_condition = 0 if refracting else 1

        while max_iter > 0:
            current_pos += increment_vector
            prev_pos = current_pos - increment_vector

            try:
                cell_value = map[int(current_pos.y)][int(current_pos.x)]
                if cell_value == stop_condition or cell_value == 2:

                    if int(current_pos.y) != int(prev_pos.y) and int(current_pos.x) != int(prev_pos.x):
                        
                        # Edge between two cells hit (corner)
                        
                        # backtrack and increase resolution
                        current_pos -= increment_vector
                        increment_vector *= 0.01

                        while max_iter > 0:
                            current_pos += increment_vector
                            prev_pos = current_pos - increment_vector
                            cell_value = map[int(current_pos.y)][int(current_pos.x)]

                            if cell_value == stop_condition or cell_value == 2:
                                return handle_hit(current_pos, prev_pos, map)

                            max_iter -= 1

                    return handle_hit(current_pos, prev_pos, map)

            except IndexError:
                pg.alert("System crashed - probably because the entered parameters are too intensive")
                exit()

            max_iter -= 1


class Hit:
    def __init__(self, pos, ray, hit_wall_orientation, cell_value, prev_cell_value):
        self.pos = pos
        self.wall_orientation = hit_wall_orientation
        self.ray = ray
        self.cell_value = cell_value
        self.prev_cell_value = prev_cell_value