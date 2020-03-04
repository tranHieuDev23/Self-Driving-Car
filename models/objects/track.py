from models.geometry.base.zero_d.point import Point
from models.geometry.base.one_d.vector import Vector
from models.geometry.polygon import Polygon


class Track:
    def __init__(self, inside_bound: Polygon, outside_bound: Polygon,
                 start_point: Point, start_direction: Vector):
        if (len(inside_bound.find_intersection_points(outside_bound)) > 0):
            raise RuntimeError("inside_bound intersects with outside_bound")
        if (inside_bound.point_is_inside(start_point) or inside_bound.point_is_on(start_point)):
            raise RuntimeError("start_point is inside inside_bound!")
        if ((not outside_bound.point_is_inside(start_point)) or outside_bound.point_is_on(start_point)):
            raise RuntimeError("start_point is outside outside_bound!")

        self.inside_bound = inside_bound
        self.outside_bound = outside_bound
        self.start_point = start_point
        self.start_direction = start_direction.normalized()

    @staticmethod
    def load_from_file(filepath):
        f = open(filepath)

        in_vertex_count = int(f.readline())
        in_vertex = []
        for i in range(in_vertex_count):
            data = f.readline().split(',')
            in_vertex.append(Point(float(data[0]), float(data[1])))
        inside_bound = Polygon(in_vertex)

        out_vertex_count = int(f.readline())
        out_vertex = []
        for i in range(out_vertex_count):
            data = f.readline().split(',')
            out_vertex.append(Point(float(data[0]), float(data[1])))
        outside_bound = Polygon(out_vertex)

        data = f.readline().split(',')
        start_point = Point(float(data[0]), float(data[1]))

        data = f.readline().split(',')
        start_direction = Vector(float(data[0]), float(data[1]))

        return Track(inside_bound, outside_bound, start_point, start_direction)
