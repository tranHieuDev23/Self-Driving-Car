from models.objects.track import Track
from models.objects.car import Car
from .base.evaluator import Evaluator


class StateEvaluator(Evaluator):
    def __init__(self, car: Car, track: Track, track_penalty=0,
                 not_moving_penalty=10000, not_moving_speed_limit=30, not_moving_time_limit=3):
        super().__init__(car, track)

        self.track_penalty = track_penalty
        self.not_moving_penalty = not_moving_penalty
        self.not_moving_speed_limit = not_moving_speed_limit
        self.not_moving_time_limit = not_moving_time_limit

        self.score = 0
        self.not_moving_duration = 0
        self.alive_duration = 1

    def evaluate(self, dt):
        if (self.car.collision_bound.intersect_with(self.track.inside_bound)):
            self.score -= self.track_penalty
            return False
        if (self.car.collision_bound.intersect_with(self.track.outside_bound)):
            self.score -= self.track_penalty
            return False

        if (self.car.speed <= self.not_moving_speed_limit):
            self.not_moving_duration += dt
            if (self.not_moving_duration >= self.not_moving_time_limit):
                self.score -= self.not_moving_penalty
                return False
            return True

        self.not_moving_duration = 0.0
        self.alive_duration += dt

        self.score += self.car.speed * dt
        return True

    def get_score(self):
        return self.score + self.alive_duration ** 2
