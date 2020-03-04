from .base.two_d.shape import Shape
from .base.one_d.ray import Ray
from .base.one_d.segment import Segment
from .base.one_d.vector import Vector
from .base.zero_d.point import Point
from typing import List


class Polygon(Shape):
    def __init__(self, vertices: List[Point]):
        self.vertices = vertices
        vertices_cnt = len(vertices)
        self.edges = []
        for i in range(vertices_cnt):
            j = (i + 1) % vertices_cnt
            self.edges.append(Segment(vertices[i], vertices[j]))

    def get_edges(self):
        return self.edges

    def point_is_on(self, point: Point):
        for e in self.edges:
            if (e.contain(point)):
                return True
        return False

    def point_is_inside(self, point: Point):
        if (self.point_is_on(point)):
            return False
            
        right_ray = Ray(point, Vector(1, 0))
        intersect_count = 0
        for e in self.edges:
            p = right_ray.find_intersection(e)
            if (p == None):
                continue
            intersect_count += 1
        return intersect_count & 1 == 1
