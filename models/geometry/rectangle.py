from .base.two_d.shape import Shape
from .base.one_d.segment import Segment
from .base.one_d.vector import Vector
from .base.zero_d.point import Point
from typing import List
import math


class Rectangle(Shape):
    def __init__(self, center: Point, halfLength: Vector, widthOverLength: float):
        self.center = center
        self.halfLength = halfLength
        self.halfWidth = halfLength.rotated(math.pi / 2) * widthOverLength

    def get_vertices(self):
        return [
            self.center + self.halfLength + self.halfWidth,
            self.center + self.halfLength - self.halfWidth,
            self.center - self.halfLength - self.halfWidth,
            self.center - self.halfLength + self.halfWidth
        ]

    def get_edges(self):
        vertices = self.get_vertices()
        result = []
        for i in range(4):
            j = (i + 1) % 4
            result.append(Segment(vertices[i], vertices[j]))
        return result

    def translate(self, direction: Vector):
        self.center.x += direction.x
        self.center.y += direction.y

    def rotate(self, angle: float):
        self.halfLength = self.halfLength.rotated(angle)
        self.halfWidth = self.halfWidth.rotated(angle)
