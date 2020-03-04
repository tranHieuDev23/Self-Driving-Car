from models.objects.track import Track
from models.objects.car import Car
from .base.driver import Driver
from keras.models import Sequential
from keras.layers import Dense, LeakyReLU
from keras.optimizers import Adam
from keras.regularizers import l2
from collections import deque
import numpy as np
import random as rd

TURN_RATES = [-1.0, 0.0, 1.0]
ACCELERATION_RATES = [0.0]


class DeepQDriver(Driver):
    def __init__(self,
                 gamma=0.99, epsilon=0.5, epsilon_min=0.1, epsilon_decay=0.995,
                 accepted_sensors=10, layer_count=3, output_per_hidden=8, learning_rate=0.001, regulation_rate=0.0,
                 turn_rates=TURN_RATES, acceleration_rates=ACCELERATION_RATES):
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.last_explore = None
        self.memory = []

        self.actions = []
        for acceleration_action in acceleration_rates:
            for turn_action in turn_rates:
                self.actions.append((turn_action, acceleration_action))
        self.action_count = len(self.actions)

        self.accepted_sensors = accepted_sensors
        self.model = Sequential()
        self.model.add(Dense(output_per_hidden,
                             input_shape=(accepted_sensors + 1,),
                             activity_regularizer=l2(regulation_rate)))
        self.model.add(LeakyReLU())
        for i in range(2, layer_count):
            self.model.add(
                Dense(output_per_hidden, activity_regularizer=l2(regulation_rate)))
            self.model.add(LeakyReLU())
        self.model.add(
            Dense(self.action_count, activity_regularizer=l2(regulation_rate)))

        self.model.compile(
            loss='mse',
            optimizer=Adam(lr=learning_rate))

    def get_input_data(self, car: Car, track: Track):
        input_data = list(map(lambda x: x / car.max_vision,
                              car.get_sensor_reading(track)))
        input_data.append(car.speed / car.max_speed)
        return np.array([input_data])

    def act(self, car: Car, track: Track, allow_explore: bool):
        if allow_explore:
            if (rd.random() < self.epsilon):
                return rd.randrange(self.action_count)
        input_data = self.get_input_data(car, track)
        qs = self.model.predict(input_data)[0]
        return np.argmax(qs)

    def calculate_command(self, car: Car, track: Track, allow_explore=False):
        action = self.act(car, track, allow_explore)
        turn_rate, acceleration_rate = self.actions[action]
        return turn_rate, acceleration_rate, action

    def remember(self, state: np.array, action: int, reward: float, new_state: np.array, done: bool):
        experience = (state, action, reward, new_state, done)
        self.memory.append(experience)

    def dump_memory_to_cache(self):
        with open('memory-cache.txt', 'a') as file:
            for experience in self.memory:
                (state, action, reward, new_state, done) = experience
                for value in state.tolist()[0]:
                    file.write(str(value) + ' ')
                file.write(str(action))
                file.write(' ')
                file.write(str(reward))
                file.write(' ')
                for value in new_state.tolist()[0]:
                    file.write(str(value) + ' ')
                file.write(str(done))
                file.write('\n')
        self.memory = []

    def load_memory_from_cache(self, batch_size: int):
        with open('memory-cache.txt') as file:
            batch = []
            cnt = 0
            for line in file:
                data = line.split(' ')
                if (len(data) < self.accepted_sensors * 2 + 5):
                    continue
                state = []
                for i in range(self.accepted_sensors + 1):
                    state.append(float(data[i]))
                state = np.array(state).reshape((1, self.accepted_sensors + 1))
                action = int(data[self.accepted_sensors + 1])
                reward = float(data[self.accepted_sensors + 2])
                new_state = []
                for i in reversed(range(self.accepted_sensors + 1)):
                    new_state.append(float(data[- 2 - i]))
                new_state = np.array(new_state).reshape(
                    (1, self.accepted_sensors + 1))
                done = (data[-1] == 'True\n')
                batch.append((state, action, reward, new_state, done))
                cnt += 1
                if (cnt == batch_size):
                    yield batch
                    batch = []
                    cnt = 0
        if (cnt > 0):
            yield batch

    def replay_memory(self, batch_size=1024, epochs=1):
        history = None
        for minibatch in self.load_memory_from_cache(batch_size):
            X_train = []
            y_train = []

            for state, action, reward, new_state, done in minibatch:
                target = reward
                if (not done):
                    target += self.gamma * \
                        np.amax(self.model.predict(new_state))
                target_func = self.model.predict(state)[0]
                target_func[action] = target
                X_train.append(state.flatten())
                y_train.append(target_func)

            X_train = np.array(X_train)
            y_train = np.array(y_train)
            history = self.model.fit(X_train, y_train, epochs=epochs)
        if (history == None):
            return None
        return history.history['loss'][0]

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    def save_model_weights(self, filepath, overwrite=True):
        self.model.save_weights(filepath, overwrite)

    def load_model_weights(self, filepath):
        self.model.load_weights(filepath)
