class Vector:

    def __init__(self, lst):
        self.values = list(lst)
        self.x = self.values[0]
        self.y = self.values[1]
        self.z = self.values[2]
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
        return Vector([a / scalar for a in self.values])

    def __str__(self):
        return f"Vector({self.values})"

    def dotProd(self, vec2):
        return sum([a * b for a, b in zip(self.values, vec2.values)])

    def magnitude(self):
        return sum([a**2 for a in self.values]) ** 0.5

    def normalise(self):
        return self / self.magnitude()


class Player:

    def __init__(self, pos, dir):
        self.pos = Vector(pos)
        self.dir = Vector(dir).normalise()


class Ray:

    def __init__(self, pos, dir):
        self.pos = Vector(pos)
        self.dir = Vector(dir).normalise()

    def cast(self, map):
        pass
