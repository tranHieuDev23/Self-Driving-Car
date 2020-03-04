from models.geometry.base.zero_d.point import Point
from models.geometry.base.one_d.segment import Segment
from models.objects.track import Track
from models.objects.car import Car
from .base.evaluator import Evaluator
from pyglet.graphics import Batch
from pyglet.gl import *
from typing import List
import math


class LineEvaluator(Evaluator):
    def __init__(self, car: Car, track: Track, lines: List[Segment], cooldown_period=math.inf):
        super().__init__(car, track)
        self.lines = lines
        self.cooldown_period = cooldown_period
        self.reset_score()
        self.__setup_graphic__()

    @staticmethod
    def load_lines_from_file(car: Car, track: Track, filepath):
        f = open(filepath)
        line_count = int(f.readline())
        lines = []
        for i in range(line_count):
            data = f.readline().split(',')
            point1 = Point(float(data[0]), float(data[1]))
            point2 = Point(float(data[2]), float(data[3]))
            lines.append(Segment(point1, point2))
        return LineEvaluator(car, track, lines)

    def draw_lines(self):
        glLineWidth(1)
        self.graphic_batch.draw()

    def reset_score(self):
        self.last_crossing = [- self.cooldown_period] * len(self.lines)
        self.square_score = 0.0
        self.linear_score = 0.0
        self.time_elapsed = 0.0

    def evaluate(self, dt: float):
        if (self.car.collision_bound.intersect_with(self.track.inside_bound)):
            self.linear_score -= 100
            return False
        if (self.car.collision_bound.intersect_with(self.track.outside_bound)):
            self.linear_score -= 100
            return False

        car_edges = self.car.collision_bound.get_edges()
        for i in range(len(self.lines)):
            line = self.lines[i]
            crossing = False
            for edge in car_edges:
                crossing |= (line.find_intersection(edge) != None)
            if (crossing and self.time_elapsed - self.last_crossing[i] >= self.cooldown_period):
                if (self.car.speed > 0):
                    self.linear_score += 10
                self.last_crossing[i] = self.time_elapsed

        return True

    def get_score(self):
        return self.square_score ** 2 + self.linear_score

    def __setup_graphic__(self):
        self.graphic_batch = Batch()
        for line in self.lines:
            data = [
                line.point1.x, line.point1.y,
                line.point2.x, line.point2.y
            ]
            color = [
                0, 255, 0,
                0, 255, 0
            ]
            self.graphic_batch.add(2, GL_LINES, None,
                                   ('v2f', data), ('c3B', color))
