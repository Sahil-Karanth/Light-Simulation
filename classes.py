import math

import numpy as np
import pyautogui as pg

from values import Values

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
    def __init__(self, pos, dir, intensity=255):
        self.pos = pos
        self.dir = dir.normalise()
        self.intensity = intensity

    def __str__(self):
        return f"r = {self.pos.values} + t{self.dir.values}"

    @staticmethod
    def initialRayCast(player, map, cast_type):
        hit_lst = []
        for angle in np.linspace(
            -player.fov / 2, player.fov / 2, Values.get_value("Number_Of_Rays")
        ):
            ray = Ray(player.pos, player.dir.rotate(angle))

            if cast_type == "primitive":
                hit = ray.cast_primitive(map, refracting=False)
            elif cast_type == "dda":
                hit = ray.cast_dda(map)
            else:
                raise ValueError("Invalid cast type.")

            if hit:
                hit_lst.append(hit)
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

        # CHECK IF I ACC NEED TO SWITHC HORIZONTAL AND VERITCAL
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
            new_angle =  math.pi + angle 

        elif angle > 0 and angle <= math.pi / 2:
            new_angle =  angle

        elif angle > math.pi / 2 and angle <= math.pi:
            new_angle =  math.pi - angle

        else:
            raise ValueError("Invalid angle value.")
        
        if wall_orientation == "vertical":
            return new_angle
        
        elif wall_orientation == "horizontal":
            return math.pi / 2 - new_angle
            
    

    @staticmethod
    def refractRay(hit, new_intensity):

        ray_angle = hit.ray.dir.get_angle()
        # print(f"Ray angle: {ray_angle}")
        incident_angle = Ray.__get_incidence_angle(ray_angle, hit.wall_orientation)
        # print(f"Incident angle: {incident_angle}")
        refracted_angle = np.arcsin(
            np.sin(incident_angle) / Values.get_value("Refractive_Index")
        )

        # print(f"Refracted angle: {refracted_angle}")
        print(f"Incident angle: {to_degrees(incident_angle)}")

        if hit.wall_orientation == "vertical":
            if ray_angle < 0:
                refracted_angle *= -1 if ray_angle >= -math.pi / 2 else -1 * (math.pi - refracted_angle)
            elif ray_angle > 0 and ray_angle <= math.pi / 2:
                pass  # No change needed
            elif ray_angle > math.pi / 2:
                refracted_angle = math.pi - refracted_angle

        elif hit.wall_orientation == "horizontal":
            if ray_angle < 0:
                refracted_angle = -1 * (math.pi / 2 - refracted_angle) if ray_angle >= -math.pi / 2 else -1 * (math.pi / 2 + refracted_angle)
            elif ray_angle > 0 and ray_angle <= math.pi / 2:
                refracted_angle = math.pi / 2 - refracted_angle
            elif ray_angle > math.pi / 2:
                refracted_angle = math.pi / 2 + refracted_angle



        new_dir = Vector([math.cos(refracted_angle), math.sin(refracted_angle)])

        new_ray = Ray(hit.pos, new_dir, new_intensity)

        return new_ray
        


    def cast_dda(self, map, max_dist=20):
        current_pos = Vector([self.pos.x, self.pos.y])

        # Calculate the step size and initial ray steps (DDA algorithm)
        delta_dist_x = abs(1 / self.dir.x) if self.dir.x != 0 else float("inf")
        delta_dist_y = abs(1 / self.dir.y) if self.dir.y != 0 else float("inf")

        step_x = 1 if self.dir.x > 0 else -1
        step_y = 1 if self.dir.y > 0 else -1

        side_dist_x = (
            (math.ceil(self.pos.x) - self.pos.x) * delta_dist_x
            if step_x > 0
            else (self.pos.x - math.floor(self.pos.x)) * delta_dist_x
        )
        side_dist_y = (
            (math.ceil(self.pos.y) - self.pos.y) * delta_dist_y
            if step_y > 0
            else (self.pos.y - math.floor(self.pos.y)) * delta_dist_y
        )

        # DDA loop to step through grid cells
        while max_dist > 0:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                current_pos.x += step_x
            else:
                side_dist_y += delta_dist_y
                current_pos.y += step_y

            max_dist -= 1

            # Check if we hit a wall

            try:

                if map[int(current_pos.y)][int(current_pos.x)]:
                    return current_pos  # Return the hit position

            except IndexError:
                pg.alert(
                    "System crashed - probably because the entered parameters are too intensive"
                )

        return None  # No collision within max_dist

    def cast_primitive(self, map, refracting, max_iter=100000,):

        current_pos = Vector([self.pos.x, self.pos.y])

        increment_vector = self.dir * 0.1

        stop_condition = 0 if refracting else 1

        while max_iter > 0:

            current_pos += increment_vector
            prev_pos = current_pos - increment_vector

            try:
                if map[int(current_pos.y)][int(current_pos.x)] == stop_condition or map[int(current_pos.y)][int(current_pos.x)] == 2:  # gone from inside block to outside

                    hit_wall_orientation = None
                    if int(current_pos.x) != int(
                        prev_pos.x
                    ):  # crossed vertical so wall is horizontal
                        hit_wall_orientation = "vertical"

                    elif int(current_pos.y) != int(prev_pos.y):
                        hit_wall_orientation = "horizontal"

                    return Hit(current_pos, self, hit_wall_orientation)

            except IndexError:
                pg.alert(
                    "System crashed - probably because the entered parameters are too intensive"
                )
                exit()

            max_iter -= 1

    def cast(self, game_map, cast_type, refracting):
        if cast_type == "Primitive":
            return self.cast_primitive(game_map, refracting)
        elif cast_type == "DDA":
            return self.cast_dda(game_map)
        else:
            raise ValueError("Invalid cast type.")


class Hit:
    def __init__(self, pos, ray, hit_wall_orientation):
        self.pos = pos
        self.wall_orientation = hit_wall_orientation
        self.ray = ray
