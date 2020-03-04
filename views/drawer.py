from pyglet.graphics import *
from pyglet.gl import *
from pyglet.image import *
from pyglet.text import *
from pyglet.sprite import Sprite
from models.geometry.base.one_d.vector import Vector
from models.objects.car import Car
from models.objects.track import Track
from controllers.evaluators.base.evaluator import Evaluator
import math
import itertools

BACKGROUND_COLOR = {'red': 128, 'green': 126, 'blue': 120}
TRACK_BORDER_COLOR = {'red': 250, 'green': 210, 'blue': 1}
TRACK_BORDER_WIDTH = 4
CAR_SPRITE_PATH = 'assets/sprites/car.png'


class Drawer:
    def __init__(self, width: float, height: float, car: Car, track: Track, evaluator: Evaluator):
        self.car = car
        self.track = track
        self.evaluator = evaluator
        self.__setup_gameplay_graphic__(width, height)

        self.can_draw_ray = True
        self.can_draw_score = True

    def resize_canvas(self, width, height):
        self.background_image = SolidColorImagePattern(
            (BACKGROUND_COLOR['red'], BACKGROUND_COLOR['green'], BACKGROUND_COLOR['blue'], 255)).create_image(width, height)

    def draw(self):
        self.__draw_gameplay__()
        if (self.can_draw_ray):
            self.__draw_sensor_rays__()
        if (self.can_draw_score):
            self.__draw_score__()

    def __setup_gameplay_graphic__(self, width, height):
        self.background_image = SolidColorImagePattern(
            (BACKGROUND_COLOR['red'], BACKGROUND_COLOR['green'], BACKGROUND_COLOR['blue'], 255)).create_image(width, height)
        self.gameplay_batch = Batch()
        self.__add_border_to_batch__(self.gameplay_batch, self.track)
        self.__add_car_sprite_to_batch__(self.gameplay_batch, self.car)
        self.score_label = Label(x=20, y=20)

    def __add_border_to_batch__(self, batch: Batch, track: Track):
        in_map = []
        in_color = []
        in_cnt = 0
        for point in track.inside_bound.vertices:
            in_map.append(point.x)
            in_map.append(point.y)
            in_color.append(TRACK_BORDER_COLOR['red'])
            in_color.append(TRACK_BORDER_COLOR['green'])
            in_color.append(TRACK_BORDER_COLOR['blue'])
            in_cnt += 1

        out_map = []
        out_color = []
        out_cnt = 0
        for point in track.outside_bound.vertices:
            out_map.append(point.x)
            out_map.append(point.y)
            out_color.append(TRACK_BORDER_COLOR['red'])
            out_color.append(TRACK_BORDER_COLOR['green'])
            out_color.append(TRACK_BORDER_COLOR['blue'])
            out_cnt += 1

        inside_group = OrderedGroup(0)
        outside_group = OrderedGroup(1)
        batch.add(in_cnt, GL_LINE_LOOP, inside_group,
                  ('v2f', in_map), ('c3B', in_color))
        batch.add(out_cnt, GL_LINE_LOOP, outside_group,
                  ('v2f', out_map), ('c3B', out_color))

    def __add_car_sprite_to_batch__(self, batch: Batch, car: Car):
        car_image = pyglet.image.load(CAR_SPRITE_PATH)
        car_image.anchor_x = car_image.width // 2
        car_image.anchor_y = car_image.height // 2

        self.car_sprite = Sprite(
            car_image, x=car.position.x, y=car.position.y, batch=batch)
        self.car_sprite.scale_x = car.width / car_image.width
        self.car_sprite.scale_y = car.height / car_image.height

    def __draw_gameplay__(self):
        self.background_image.blit(0, 0)
        old_line_width = GL_LINE_WIDTH
        glLineWidth(TRACK_BORDER_WIDTH)
        sprite_rotation = math.degrees(
            self.car.direction.clockwise_angle(Vector(0, 1)))
        self.car_sprite.update(
            x=self.car.position.x, y=self.car.position.y, rotation=sprite_rotation)
        self.gameplay_batch.draw()

    def __draw_sensor_rays__(self):
        readings = self.car.get_sensor_reading(self.track)
        sensor_batch = Batch()
        for (ray, distance) in itertools.zip_longest(self.car.sensors, readings):
            end_point = ray.start_point + ray.direction * distance
            ray_data = [
                ray.start_point.x, ray.start_point.y,
                end_point.x, end_point.y
            ]
            ray_color = [
                255, 0, 0,
                255, 0, 0
            ]
            sensor_batch.add(2, GL_LINES, None,
                             ('v2f', ray_data), ('c3B', ray_color))
        glLineWidth(1)
        sensor_batch.draw()

    def __draw_score__(self):
        self.score_label.text = str(self.evaluator.get_score())
        self.score_label.draw()
