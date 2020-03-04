from models.geometry.base.zero_d.point import Point
from models.geometry.base.one_d.vector import Vector
from models.geometry.base.one_d.segment import Segment
from models.geometry.base.one_d.ray import Ray
from models.geometry.rectangle import Rectangle
from models.objects.track import Track
import math

SENSOR_ANGLES = [
    0, math.pi / 6, math.pi / 3, math.pi / 2, math.pi * 5 / 6, math.pi,
    math.pi * 7 / 6, math.pi * 3 / 2, math.pi * 5 / 3, math.pi * 11 / 6
]


class Car:
    def __init__(self, width: float, height: float, sensor_angles=SENSOR_ANGLES,
                 max_speed=300.0, max_acceleration=30.0, max_turn=math.pi / 3, max_vision=300.0):
        # Setting up the base characteristics
        self.width = width
        self.height = height
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration
        self.max_turn = max_turn
        self.max_vision = max_vision
        # Setting up the sensor rays
        self.sensor_angles = sensor_angles
        self.sensors = []

    def init_position(self, position: Point, direction: Vector):
        self.position = Point(position.x, position.y)
        self.direction = Vector(direction.x, direction.y).normalized()
        # Calculating the rectangular collision bound
        self.collision_bound = Rectangle(
            self.position, direction * self.height / 2, self.width / self.height)
        # Initialize the sensor rays
        self.sensors = []
        for angle in self.sensor_angles:
            self.sensors.append(Ray(position, direction.rotated(angle)))
        # Initial state
        self.speed = 50

    def move(self, turn_rate: float, acceleration_rate: float, dt: float):
        turn_angle = turn_rate * self.max_turn
        acceleration = acceleration_rate * self.max_acceleration

        self.speed += acceleration * dt
        if (self.speed > self.max_speed):
            self.speed = self.max_speed
        if (self.speed < -self.max_speed):
            self.speed = -self.max_speed

        self.__rotate__(turn_angle * dt)
        self.__translate__(self.direction * self.speed * dt)

    def get_sensor_reading(self, track: Track):
        result = []
        for ray in self.sensors:
            reading = self.max_vision
            for edge in track.inside_bound.get_edges():
                intersection = ray.find_intersection(edge)
                if (intersection == None):
                    continue
                reading = min(reading, self.position.distance(intersection))
            for edge in track.outside_bound.get_edges():
                intersection = ray.find_intersection(edge)
                if (intersection == None):
                    continue
                reading = min(reading, self.position.distance(intersection))
            result.append(reading)
        return result

    def __translate__(self, direction: Vector):
        self.position += direction
        self.collision_bound.translate(direction)
        for ray in self.sensors:
            ray.translate(direction)

    def __rotate__(self, angle: float):
        self.direction = self.direction.rotated(angle)
        self.collision_bound.rotate(angle)
        for ray in self.sensors:
            ray.rotate(angle)
