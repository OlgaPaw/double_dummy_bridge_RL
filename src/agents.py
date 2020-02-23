import json
import random
import sys
from abc import ABCMeta
from collections import defaultdict

import numpy

from src.models import GameState


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Agent(metaclass=ABCMeta):
    @classmethod
    def move(cls, state: GameState) -> int:
        raise NotImplementedError


class RandomAgent(Agent):
    @classmethod
    def move(cls, state: GameState) -> int:
        return random.sample(state.valid_moves, 1)[0]


class QLearnAgent(Agent):
    def __init__(self, learning_rate: float = 0.0, discount_factor: float = 0.0, rand_factor: float = 0.0):
        self.q_table = defaultdict(lambda: numpy.zeros(52))
        self.learning_rate = learning_rate
        self.rand_factor = rand_factor
        self.discount_factor = discount_factor
        self.data_file = f'src/q_models_data/q_learn.json'
        self.load()

    def move(self, state: GameState) -> int:
        key = str(state)
        #Update invalid actions:
        for action, _ in enumerate(self.q_table[key]):
            if action not in state.valid_moves:
                self.q_table[key][action] = -float('inf')
        if self.learning_rate > 0 and random.random() < self.rand_factor:
            valid_actions = numpy.where(self.q_table[key] > -float('inf'))[0]
            return int(numpy.random.choice(valid_actions))

        return int(numpy.argmax(self.q_table[key]))

    def update_q(self, state_key: str, action: int, reward: float, new_state_key: str):
        old_q_value = self.q_table[state_key][action]
        next_max = numpy.max(self.q_table[new_state_key])
        new_q_value = (1 - self.learning_rate) * old_q_value \
                    + self.learning_rate * (reward + self.discount_factor * next_max)
        self.q_table[state_key][action] = new_q_value

    def save(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.q_table, f, sort_keys=True, indent=2, cls=NumpyEncoder)

    def load(self):
        try:
            with open(self.data_file, 'r') as f:
                json_data = json.load(f)
            for key, value in json_data.items():
                self.q_table[key] = numpy.asarray(value)

        except:
            print(f'Data file {self.data_file} not found', sys.stderr)
