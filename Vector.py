import math
import random

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




# Pick a random angle from the Z-axis 0 deg to our max threshold
# Randomly rotate that vector around the Z-axis
# This will generate all possible directions within that cone
def random_vector_in_cone(max_angle_deg, defaultAngle, progress, maxOffset):
    max_angle_rad = math.radians(max_angle_deg)
    cos_theta = math.cos(max_angle_rad)

    u = random.uniform(cos_theta, 1)

    # Full rotation if we're at max angle; otherwise limit to upper half (y >= 0)
    if max_angle_deg == defaultAngle:
        alpha = random.uniform(0, 2 * math.pi)  # Full cone

    else:
        alpha = random.uniform(0, math.pi)  # Only upper half

    phi = math.acos(u)
    x = math.sin(phi) * math.cos(alpha)
    y = math.sin(phi) * math.sin(alpha) + (progress * maxOffset)
    z = u

    return Custom_Vector(x, y, z)
