import math

class Custom_Vector:


    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


    def __repr__(self):
        return f"Custom_Vector({self.x}, {self.y}, {self.z})"

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def add(self, other):
        return Custom_Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other):
        return Custom_Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z