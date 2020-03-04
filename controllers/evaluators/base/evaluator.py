from models.objects.car import Car
from models.objects.track import Track


class Evaluator:
    def __init__(self, car: Car, track: Track):
        self.car = car
        self.track = track

    def evaluate(self, dt: float):
        raise NotImplementedError(
            "evaluate(float) function was not implemented!")

    def get_score(self):
        raise NotImplementedError(
            "get_score() function was not implemented!")
