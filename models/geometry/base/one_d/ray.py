from models.geometry.base.zero_d.point import Point
from .vector import Vector
from .line import Line
from .edge import Edge

EPSILON = 1e-3


class Ray(Edge):
    def __init__(self, start_point: Point, direction: Vector):
        self.start_point = start_point
        self.direction = direction.normalized()

    def get_direction_line(self):
        return Line.from_point_and_vector(self.start_point, self.direction)

    def contain(self, point: Point):
        if (point == self.start_point):
            return True
        v = Vector.from_two_points(self.start_point, point)
        return abs(Vector.from_two_points(self.start_point, point).angle(self.direction)) <= EPSILON

    def translate(self, direction: Vector):
        self.start_point += direction

    def rotate(self, angle):
        self.direction = self.direction.rotated(angle)
