from abc import ABCMeta
import random

from src.models import GameState


class Agent(metaclass=ABCMeta):
    @classmethod
    def move(cls, state: GameState) -> int:
        raise NotImplementedError


class RandomAgent(Agent):
    @classmethod
    def move(cls, state: GameState) -> int:
        return random.sample(state.valid_moves, 1)[0]