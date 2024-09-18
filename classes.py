import math

import numpy as np


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


class Player:
    def __init__(self, pos, dir):
        self.pos = Vector(pos)
        self.dir = Vector(dir).normalise()
        self.fov = np.pi / 3

    def move(self, dir):
        self.pos += dir


class Ray:
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir.normalise()

    def __str__(self):
        return f"r = {self.pos.values} + t{self.dir.values}"

    @staticmethod
    def sendRays(player, map, cast_type):
        hit_lst = []
        for angle in np.linspace(-player.fov / 2, player.fov / 2, 70):
            ray = Ray(player.pos, player.dir.rotate(angle))

            if cast_type == "primitive":
                hit = ray.cast_primitive(map)
            elif cast_type == "dda":
                hit = ray.cast_dda(map)
            else:
                raise ValueError("Invalid cast type.")

            if hit:
                hit_lst.append(hit)
        return hit_lst

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
            if map[int(current_pos.y)][int(current_pos.x)]:
                return current_pos  # Return the hit position

        return None  # No collision within max_dist

    def cast_primitive(self, map, max_dist=20):

        current_pos = Vector([self.pos.x, self.pos.y])

        increment_vector = self.dir * 0.1

        while True:

            current_pos += increment_vector

            if map[int(current_pos.y)][int(current_pos.x)]:
                return current_pos
