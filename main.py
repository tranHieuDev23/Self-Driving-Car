from models.objects.track import Track
from models.objects.car import Car
from controllers.evaluators.line_evaluator import LineEvaluator
from controllers.drivers.deep_q_driver import DeepQDriver
from controllers.drivers.player_driver import PlayerDriver
from views.drawer import Drawer
import os
import pyglet

track = Track.load_from_file('assets/tracks/track-1.trk')
car = Car(width=24, height=45)
car.init_position(track.start_point, track.start_direction)

evaluator = LineEvaluator.load_lines_from_file(
    car, track, "assets/evaluator_lines/track-1.lns")

driver = DeepQDriver(accepted_sensors=10, layer_count=8, output_per_hidden=32)
driver.load_model_weights('model.h5')

drawer = Drawer(1280, 720, car, track, evaluator)

window = pyglet.window.Window(1280, 720, resizable=True)

p_driver = PlayerDriver(window)

start_direction = track.start_direction.normalized()


def game_loop(dt: float):
    global track, car, p_driver, evaluator, start_direction

    turn_rate, acceleration_rate, action = driver.calculate_command(
        car, track, False)
    state = driver.get_input_data(car, track)
    car.move(turn_rate, acceleration_rate, dt)
    done = not evaluator.evaluate(dt)

    if (done):
        car.init_position(track.start_point, track.start_direction)
        evaluator.reset_score()


pyglet.clock.schedule_interval(game_loop, 1/60)


@window.event
def on_draw():
    window.clear()
    drawer.draw()
    evaluator.draw_lines()


@window.event
def on_resize(width, height):
    drawer.resize_canvas(width, height)
    drawer.draw()


pyglet.app.run()
