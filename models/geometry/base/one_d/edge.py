from models.geometry.base.zero_d.point import Point

class Edge:
    def get_direction_line(self):
        raise NotImplementedError(
            "get_direction_line() is function was not implemented!")

    def contain(self, point: Point):
        raise NotImplementedError(
            "contain(Point) is function was not implemented!")

    def find_intersection(self, other):
        result = self.get_direction_line().find_intersection_with_line(other.get_direction_line())
        if (result == None):
            return None
        if ((not self.contain(result)) or (not other.contain(result))):
            return None
        return result