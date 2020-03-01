import json
import random
import sys
from abc import ABCMeta
from collections import defaultdict

import numpy

from src.models import GameState
from src.network import InputPattern, load_model, model


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
        key = self._state_to_input(state)
        #Update invalid actions:
        for action, _ in enumerate(self.q_table[key]):
            if action not in state.valid_moves:
                self.q_table[key][action] = -float('inf')
        if self.learning_rate > 0 and random.random() < self.rand_factor:
            valid_actions = numpy.where(self.q_table[key] > -float('inf'))[0]
            return int(numpy.random.choice(valid_actions))

        return int(numpy.argmax(self.q_table[key]))

    def _state_to_input(self, state: GameState):
        return str(state)

    def update_q(self, state: GameState, action: int, reward: float, new_state: GameState):
        state_key = self._state_to_input(state)
        new_state_key = self._state_to_input(new_state)
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


class DeepQLearnAgent(Agent):
    # Implementing EpsGreedyPolicy
    def __init__(self, learning_rate: float = 0.0, discount_factor: float = 0.0, rand_factor: float = 0.0):
        self.learning_rate = learning_rate
        self.rand_factor = rand_factor
        self.discount_factor = discount_factor
        self.model = None
        self.data_file = f'src/q_models_data/deep_q_learn.h5'
        self.load()

    def move(self, state: GameState) -> int:
        state_input = self._state_to_input(state)
        q_values = self.model.predict(state_input)[0]
        if self.learning_rate > 0 and random.random() < self.rand_factor:
            card_in_hand = len(state.player_hand)
            n_best = q_values.argsort()[card_in_hand:][::-1]
            action = random.choice(n_best)
        else:
            action = int(numpy.argmax(q_values))
        return action

    def _state_to_input(self, state: GameState):
        model_input = InputPattern(
            trump=state.trump.id,
            hand1=state.player_hand,
            hand2=state.left_opponent_hand,
            hand3=state.partner_hand,
            hand4=state.right_opponent_hand,
            trick=state.trick.cards,
            trick_suite=state.trick.color.id if state.trick.color else -1
        )
        return model_input.get_array()

    def update_q(self, state: GameState, action: int, reward: float, new_state: GameState):
        state_input = self._state_to_input(state)
        new_state_input = self._state_to_input(new_state)
        old_q_values = self.model.predict(state_input)[0]
        next_q_values = self.model.predict(new_state_input)[0]
        next_max = numpy.max(next_q_values)
        old_q_value = old_q_values[action]
        new_q_value = (1 - self.learning_rate) * old_q_value \
                    + self.learning_rate * (reward + self.discount_factor * next_max)
        rewards = self._get_state_rewards_rules(state, old_q_values, action, new_q_value)
        self.model.fit(state_input, rewards, steps_per_epoch=1, verbose=False)

    def _get_state_rewards_q(self, state: GameState, old_q_values: numpy.ndarray, action: int, new_q_value: float):
        rewards = old_q_values
        rewards[action] = new_q_value
        return rewards.reshape(1, len(rewards))

    def _get_state_rewards_rules(self, state: GameState, old_q_values: numpy.ndarray, action: int, new_q_value: float):
        reward_invalid = -13
        raward_valid = 0.1
        rewards = old_q_values
        for index, _ in enumerate(rewards):
            if index not in state.valid_moves:
                rewards[index] = reward_invalid
            else:
                rewards[index] = raward_valid
        # rewards[action] = new_q_value
        return rewards.reshape(1, len(rewards))

    def save(self):
        self.model.save(self.data_file)

    def load(self):
        try:
            self.model = load_model(self.data_file)
        except OSError:
            print(f'Data file {self.data_file} not found', sys.stderr)
            self.model = model()
