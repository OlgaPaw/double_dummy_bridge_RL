import random
import sys
from enum import Enum
from io import StringIO
from typing import Dict, Tuple

import gym

from src.agents import Agent
from src.models import Card, Deal, GameState, Player

# Types declaration
Observation = Dict
Reward = float
Done = bool
Info = str

DECK_SIZE = 52
CARDS_FOR_PLAYER = 13
TRICK_SIZE = 4
SUIT_COUNT = 4
HAND = [DECK_SIZE] * CARDS_FOR_PLAYER
TRICK = [DECK_SIZE] * TRICK_SIZE


class Rewards(Enum):
    INVALID_MOVE = -float('inf')
    VALID_MOVE = 0.1
    TRICK_WON = 1.0
    TRICK_LOST = -1.0
    OTHER = 0


class BridgeEnv(gym.Env):
    def __init__(self):
        self.action_space = gym.spaces.Discrete(DECK_SIZE)
        self.observation_space = gym.spaces.Dict({
            'my_hand': gym.spaces.MultiDiscrete(HAND),
            'partner_hand': gym.spaces.MultiDiscrete(HAND),
            'opponent1_hand': gym.spaces.MultiDiscrete(HAND),
            'opponent2_hand': gym.spaces.MultiDiscrete(HAND),
            'trick': gym.spaces.MultiDiscrete(TRICK),
            'trump': gym.spaces.Discrete(SUIT_COUNT),
            "gamer_type": gym.spaces.Discrete(2),  # offence, defence
        })
        self.deal: Deal = None
        self.state: GameState = None
        self.opponent: Agent = None

    def setup(self, deal: Deal, opponent: Agent) -> None:
        self.deal = deal
        self.opponent = opponent
        self.state = GameState.from_deal(deal)

    def reset(self) -> None:
        self.state = GameState.from_deal(self.deal)
        if self.state.current_player == Player.WEST or self.state.current_player == Player.EAST:
            opponent_card = Card(self.opponent.move(self.state))
            self._move_and_get_reward(opponent_card)

    def step(self, action: Card) -> Tuple[Observation, Reward, Done, Info]:
        assert self.deal, "please run setup before learning"
        assert self.action_space.contains(action)
        card = Card(action)

        if not self._action_is_valid(card):
            return self._state_to_observation(), Rewards.INVALID_MOVE.value, False, '.'
        info = opponent_move_info = ''
        reward, done, info = self._move_and_get_reward(card)
        if not done and (self.state.current_player == Player.WEST or self.state.current_player == Player.EAST):
            opponent_card = Card(self.opponent.move(self.state))
            # fallback to random card if opponent move is invalid
            if Card(opponent_card) not in self.state.valid_moves:
                opponent_card = random.sample(self.state.valid_moves, 1)[0]
            reward, done, opponent_move_info = self._move_and_get_reward(opponent_card)
            reward = -reward
        return self._state_to_observation(), reward, done, "".join([info, opponent_move_info])

    def _move_and_get_reward(self, card: Card) -> Tuple[Reward, Done, Info]:
        self.state.trick.add_card(card, self.state.current_player)
        self.state.player_hand.remove(card)
        info = f'{self.state.current_player.value}:{str(card)}'
        done = not self.state.any_hand_not_empty

        if self.state.trick.full:
            winner = self.state.trick.winner
            current_pair_won = winner == self.state.current_player or winner == self.state.current_player.partner
            reward = Rewards.TRICK_WON.value if current_pair_won else Rewards.TRICK_LOST.value
            self.state.trick.clear()
            self.state.current_player = winner
            return reward, done, info
        else:
            self.state.current_player = self.state.current_player.next
            return Rewards.VALID_MOVE.value, done, info

    def render(self, mode: str = "human") -> StringIO:
        outfile = StringIO() if mode == 'ansi' else sys.stdout
        outfile.write(f'\n{self.state.to_dict()}\n')
        return outfile

    def _action_is_valid(self, action: Card) -> bool:
        if action not in self.state.player_hand:
            return False
        if action not in self.state.valid_moves:
            return False
        return True

    def _state_to_observation(self) -> Observation:
        return {
            "my_hand": self.state.player_hand,
            "opponent1_hand": self.state.left_opponent_hand,
            "partner_hand": self.state.partner_hand,
            "opponent2_hand": self.state.right_opponent_hand,
            "trick": self.state.trick,
            "gamer_type": self.state.play_type.value,
            "trump": self.state.trump.id,
        }