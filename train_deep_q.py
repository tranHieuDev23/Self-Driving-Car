from models.objects.track import Track
from models.objects.car import Car
from controllers.evaluators.line_evaluator import LineEvaluator
from controllers.drivers.deep_q_driver import DeepQDriver
from views.drawer import Drawer
import os
import pyglet

track = Track.load_from_file('assets/tracks/track-1.trk')
car = Car(width=24, height=45)
car.init_position(track.start_point, track.start_direction)

evaluator = LineEvaluator.load_lines_from_file(
    car, track, "assets/evaluator_lines/track-1.lns")

driver = DeepQDriver(
    gamma=0.99, epsilon=0.8, epsilon_decay=0.99, epsilon_min=0.1,
    learning_rate=0.01, accepted_sensors=10, layer_count=8, output_per_hidden=32, regulation_rate=0.0)

drawer = Drawer(1280, 720, car, track, evaluator)

window = pyglet.window.Window(1280, 720, resizable=True)

last_score = 0.0
time_elapsed = 0.0
game_count = 0
skip_frame = False
losses = []
scores = []


def game_loop(dt: float):
    global track, car, driver, evaluator, last_score, time_elapsed, game_count, skip_frame, losses, scores

    if (skip_frame):
        skip_frame = False
        return

    time_elapsed += dt

    state = driver.get_input_data(car, track)

    turn_rate, acceleration_rate, action = driver.calculate_command(
        car, track, True)
    car.move(turn_rate, acceleration_rate, dt)
    done = not evaluator.evaluate(dt)

    reward = evaluator.get_score() - last_score
    last_score = evaluator.get_score()
    new_state = driver.get_input_data(car, track)

    driver.remember(state, action, reward, new_state, done)

    if (done or time_elapsed >= 300):
        driver.dump_memory_to_cache()
        print("Game", game_count, "ended!")
        losses.append(driver.replay_memory(1 << 10, 10))
        scores.append(evaluator.get_score() + 100)
        driver.decay_epsilon()
        driver.last_explore = None
        game_count += 1
        print("Game", game_count, "starting! Epsilon:", driver.epsilon)
        last_score = 0.0
        time_elapsed = 0.0
        car.init_position(track.start_point, track.start_direction)
        evaluator.reset_score()
        skip_frame = True


pyglet.clock.schedule_interval(game_loop, 1/30)


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

# Save model to file to use later

driver.save_model_weights("model.h5")
