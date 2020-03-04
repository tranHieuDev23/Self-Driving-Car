from models.geometry.base.one_d.vector import Vector


class Shape:
    def get_edges(self):
        raise NotImplementedError(
            "get_edges() function was not implemented!")

    def translate(self, direction: Vector):
        raise NotImplementedError(
            "translate(direction) function was not implemented!")

    def rotate(self, angle: float):
        raise NotImplementedError(
            "rotate(angle) function was not implemented!")

    def find_intersection_points(self, other):
        edges = self.get_edges()
        other_edges = other.get_edges()
        result = []

        for e in edges:
            for oe in other_edges:
                p = e.find_intersection(oe)
                if (p != None):
                    result.append(p)

        return result
    
    def intersect_with(self, other):
        return len(self.find_intersection_points(other)) > 0
