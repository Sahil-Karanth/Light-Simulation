class Vector:

    def __init__(self, lst):
        self.values = list(lst)
        self.x = self.values[0]
        self.y = self.values[1]
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
        self.fov = 60

    def move(self, dir):
        # dir is a vector
        self.pos += dir


class Ray:

    def __init__(self, pos, dir):
        self.pos = Vector(pos)
        self.dir = Vector(dir).normalise()

    def __str__(self):
        return f"r = {self.pos.values} + t{self.dir.values}"

    def cast(self, map):

        if self.dir.dotProd(Vector([0, 1])) > 0: # looking up
            stepY = -1
            nextY = int(self.pos.y)
            yDist = (self.pos.y - nextY) * self.dir.y
            yStep = -1

        else: # looking down
            stepY = 1
            nextY = int(self.pos.y) + 1
            yDist = (nextY - self.pos.y) * self.dir.y
            yStep = 1

            