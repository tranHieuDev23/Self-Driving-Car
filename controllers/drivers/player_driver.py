from pyglet.window import Window, key
from .base.driver import Driver
from models.objects.car import Car
from models.objects.track import Track

ACCELERATION_CHANGE = 1
TURN_CHANGE = 1


class PlayerDriver(Driver):
    def __init__(self, window):
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.acceleration_rate = 0.0
        self.turn_rate = 0.0
        window.push_handlers(self)

    def on_key_press(self, symbol, modifiers):
        if (symbol == key.UP):
            self.forward = True
        if (symbol == key.DOWN):
            self.backward = True
        if (symbol == key.RIGHT):
            self.left = True
        if (symbol == key.LEFT):
            self.right = True

    def on_key_release(self, symbol, modifiers):
        if (symbol == key.UP):
            self.forward = False
        if (symbol == key.DOWN):
            self.backward = False
        if (symbol == key.RIGHT):
            self.left = False
        if (symbol == key.LEFT):
            self.right = False

    def calculate_command(self, car: Car, track: Track):
        if (self.left != self.right):
            if (self.left):
                self.turn_rate = min(self.turn_rate + TURN_CHANGE, 1)
            else:
                self.turn_rate = max(self.turn_rate - TURN_CHANGE, -1)
        else:
            self.turn_rate = 0.0

        if (self.forward != self.backward):
            if (self.forward):
                self.acceleration_rate = min(
                    self.acceleration_rate + ACCELERATION_CHANGE, 1)
            else:
                self.acceleration_rate = max(
                    self.acceleration_rate - ACCELERATION_CHANGE, -1)
        else:
            self.acceleration_rate = 0.0

        return (self.turn_rate, self.acceleration_rate)
