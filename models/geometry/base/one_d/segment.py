from models.geometry.base.zero_d.point import Point
from .vector import Vector
from .line import Line
from .edge import Edge
from math import *

EPSILON = 1e-5


class Segment(Edge):
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def length(self):
        return self.point1.distance(self.point2)

    def get_direction_line(self):
        return Line.from_two_points(self.point1, self.point2)

    def contain(self, point: Point):
        return abs(self.point1.distance(point) + point.distance(self.point2) - self.length()) <= EPSILON

    def translate(self, direction: Vector):
        self.point1 += direction
        self.point2 += direction
