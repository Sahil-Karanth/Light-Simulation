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
        self.pos = pos
        self.dir = dir.normalise()

    def __str__(self):
        return f"r = {self.pos.values} + t{self.dir.values}"

    def cast(self, map, max_dist=20):

        if max_dist == 0:
            return None
            
        if self.dir.dotProd(Vector([0, 1])) > 0: # looking up
            # move up to the next horizontal line
            to_next_y = (int(self.pos.y) + 1 - self.pos.y) / self.dir.y
            x_step = 1 / self.dir.y * self.dir.x

        else: # looking down
            # move down to the next horizontal line
            to_next_y = (int(self.pos.y) - self.pos.y) / self.dir.y
            x_step = 1 / self.dir.y * self.dir.x
        
        if self.dir.dotProd(Vector([1, 0])) > 0: # looking right
            # move right to the next vertical line
            to_next_x = (int(self.pos.x) + 1 - self.pos.x) / self.dir.x
            y_step = 1 / self.dir.x * self.dir.y
        
        else: # looking left
            # move left to the next vertical line
            to_next_x = (int(self.pos.x) - self.pos.x) / self.dir.x
            y_step = 1 / self.dir.x * self.dir.y

        
        while max_dist > 0:
            if to_next_y < to_next_x:
                self.pos += Vector([0, to_next_y])
                to_next_x -= to_next_y
                to_next_y = 1
            else:
                self.pos += Vector([to_next_x, 0])
                to_next_y -= to_next_x
                to_next_x = 1

            max_dist -= 1

            if map[int(self.pos.y)][int(self.pos.x)]:
                return self.pos
            
        
        
  
        
        

