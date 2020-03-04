from models.geometry.base.zero_d.point import Point
from .edge import Edge
from .vector import Vector

EPSILON = 1e-5


class Line(Edge):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def from_two_points(point1: Point, point2: Point):
        return Line.from_point_and_vector(point1, Vector.from_two_points(point1, point2))

    @staticmethod
    def from_point_and_vector(point: Point, direction: Vector):
        if (direction == Vector(0, 0)):
            raise ValueError('direction cannot be equal to (0, 0)!')
        if (direction.y == 0):
            return Line(0, 1, - point.y)
        a = 1
        b = - direction.x / direction.y
        c = - (a * point.x + b * point.y)
        return Line(a, b, c)

    def get_direction_line(self):
        return self

    def evaluate(self, point: Point):
        return self.a * point.x + self.b * point.y + self.c

    def contain(self, point: Point):
        return abs(self.evaluate(point) - 0) <= EPSILON

    def parallel(self, other):
        return self.a == other.a and self.b == other.b and self.c != other.c

    def coincide(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c

    def find_intersection_with_line(self, other):
        if (self.parallel(other) or self.coincide(other)):
            return None
        d = self.a * other.b - other.a * self.b
        dx = self.c * other.b - other.c * self.b
        dy = self.a * other.c - other.a * self.c
        return Point(- dx / d, - dy / d)

    def translate(self, direction: Vector):
        if (self.a == 0):
            self.c -= direction.y
            return
        point1 = Point(- self.c / self.a, 0) + direction
        point2 = Point(- (self.b + self.c) / self.a, 1) + direction
        newLine = Line.from_two_points(point1, point2)
        self.a = newLine.a
        self.b = newLine.b
        self.c = newLine.c
