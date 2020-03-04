from models.objects.car import Car
from models.objects.track import Track


class Driver:
    def calculate_command(self, car: Car, track: Track):
        raise NotImplementedError(
            "command(Car) function was not implemented!")
