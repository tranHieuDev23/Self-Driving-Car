from models.geometry.base.zero_d.point import Point
import math

EPSILON = 1e-5


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_two_points(start_point: Point, end_point: Point):
        return Vector(end_point.x - start_point.x, end_point.y - start_point.y)

    def __eq__(self, other):
        if (other == None):
            return False
        return abs(self.x - other.x) <= EPSILON and abs(self.y - other.y) <= EPSILON

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        l = self.length()
        return Vector(self.x / l, self.y / l)

    def rotated(self, angle: float):
        x_prime = self.x * math.cos(angle) + self.y * math.sin(angle)
        y_prime = self.y * math.cos(angle) - self.x * math.sin(angle) 
        return Vector(x_prime, y_prime)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def det(self, other):
        return self.x * other.y - self.y * other.x

    def angle(self, other):
        angle_cos = self.dot(other) / (self.length() * other.length())
        angle_cos = min(angle_cos, 1) 
        angle_cos = max(angle_cos, -1) 
        return math.acos(angle_cos)

    def clockwise_angle(self, other):
        do = self.dot(other)
        de = self.det(other)
        return math.atan2(de, do)
