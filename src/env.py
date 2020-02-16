import sys
from enum import Enum
from io import StringIO
from typing import Dict, Tuple

import gym

from src.models import Card, Deal, GameState

# Types declaration
Observation = Dict
Reward = float
Done = bool
Info = Dict

DECK_SIZE = 52
CARDS_FOR_PLAYER = 13
TRICK_SIZE = 4
SUIT_COUNT = 4
HAND = [DECK_SIZE] * CARDS_FOR_PLAYER
TRICK = [DECK_SIZE] * TRICK_SIZE


class Rewards(Enum):
    INVALID_MOVE = -float('inf')
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

    def setup(self, deal: Deal) -> None:
        self.deal = deal
        self.state = GameState.from_deal(deal)

    def reset(self) -> None:
        self.state = GameState.from_deal(self.deal)

    def step(self, action: Card) -> Tuple[Observation, Reward, Done, Info]:
        assert self.deal, "please run setup before learning"
        assert self.action_space.contains(action)
        card = Card(action)

        if not self._action_is_valid(card):
            return self._state_to_observation(), Rewards.INVALID_MOVE.value, False, 'Invalid move'

        reward, done = self._update_state(card)
        return self._state_to_observation(), reward, done, None

    def _update_state(self, card: Card) -> Tuple[Reward, Done]:
        self.state.trick.add_card(card, self.state.current_player)
        self.state.player_hand.remove(card)

        done = not self.state.any_hand_not_empty
        if self.state.trick.full:
            winner = self.state.trick.winner
            current_pair_won = winner == self.state.current_player or winner == self.state.current_player.partner
            reward = Rewards.TRICK_WON.value if current_pair_won else Rewards.TRICK_LOST.value
            self.state.trick.clear()
            self.state.current_player = winner
            return reward, done
        else:
            self.state.current_player = self.state.current_player.next
            return Rewards.OTHER.value, done

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