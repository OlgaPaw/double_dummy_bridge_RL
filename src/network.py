from enum import Enum
from typing import Sequence

import keras
import numpy

Hand = Sequence[int]

STATE_SIZE = 54
DECK_SIZE = 52


class CardPosition(Enum):
    TRICK = 0
    PLAYER = 1
    LEFT_OPPONENT = 2
    PARTNER = 3
    RIGHT_OPPONENT = 4


class Suit(Enum):
    NONE = -1
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3


class Trump(Enum):
    NO_TRUMP = -1
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3


class InputPattern:
    def __init__(self, trump: int, hand1: Hand, hand2: Hand, hand3: Hand, hand4: Hand, trick: Hand, trick_suite: int):
        self.input = numpy.repeat(-1, STATE_SIZE)
        self._map_cards_to_input(hand1, CardPosition.PLAYER)
        self._map_cards_to_input(hand2, CardPosition.LEFT_OPPONENT)
        self._map_cards_to_input(hand3, CardPosition.PARTNER)
        self._map_cards_to_input(hand4, CardPosition.RIGHT_OPPONENT)
        self._map_cards_to_input(trick, CardPosition.TRICK)
        self.input[52] = Trump(trump).value
        self.input[53] = Suit(trick_suite).value

    def _map_cards_to_input(self, input_list: Hand, position: CardPosition):
        for item in input_list or []:
            self.input[item] = position.value

    def get_array(self) -> numpy.ndarray:
        return self.input.reshape(1, len(self.input))


def model() -> keras.Model:
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(STATE_SIZE, input_dim=STATE_SIZE, activation=keras.activations.relu))
    model.add(keras.layers.Dense(DECK_SIZE * STATE_SIZE, activation=keras.activations.relu))
    model.add(keras.layers.Dense(DECK_SIZE, activation=keras.activations.linear))
    model.compile(optimizer='adadelta', loss='mean_squared_error')
    return model


def load_model(filename: str) -> keras.Model:
    return keras.models.load_model(filename)
