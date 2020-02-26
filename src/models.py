from copy import deepcopy
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, Iterable, List, Optional, Set

COLORS = 'CDHS'
VALUES_MAP = {8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A'}
NAMES_MAP = dict(zip(VALUES_MAP.values(), VALUES_MAP.keys()))


class TrickFullException(Exception):
    pass


class Player(Enum):
    WEST = 'W'
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'

    @property
    def order(self):
        return 'WNES'

    @property
    def next(self):
        index = self.order.index(self.value)
        return Player(self.order[(index + 1) % 4])

    @property
    def partner(self):
        return self.next.next


class Color(Enum):
    CLUBS = 'C'
    DIAMONDS = 'D'
    HEARTS = 'H'
    SPADES = 'S'

    @property
    def id(self):
        return COLORS.index(self.value)


class Trump(Enum):
    NO_TRUMP = 'NT'
    CLUBS = 'C'
    DIAMONDS = 'D'
    HEARTS = 'H'
    SPADES = 'S'

    @property
    def id(self):
        try:
            return COLORS.index(self.value)
        except ValueError:
            return -1


class Card(int):
    @property
    def value(self):
        return self % 13

    @property
    def color(self):
        return Color(COLORS[self // 13])

    @property
    def value_str(self):
        return VALUES_MAP.get(self.value, str(self.value + 2))

    def __str__(self):
        return f'{self.color.value}{self.value_str}'

    @staticmethod
    def from_str(data: str):
        color_str, value_str = data
        value = NAMES_MAP[value_str] if value_str in NAMES_MAP else int(value_str) - 2
        color_id = Color(color_str).id
        return Card(color_id * 13 + value)


Hand = Set[Card]  # max len 13


class PlayType(Enum):
    OFFENCE = 0
    DEFENCE = 1


@dataclass
class Contract:
    tricks: int
    trump: Trump

    def __str__(self):
        return f'{self.tricks}{self.trump.value}'


@dataclass
class Trick:
    trump: Trump
    cards: List[Card] = None
    leader: Player = None

    @property
    def empty(self):
        return not self.cards or len(self.cards) == 0

    @property
    def full(self):
        return self.cards and len(self.cards) == 4

    @property
    def color(self):
        return self.cards[0].color if self.cards else None

    def add_card(self, card: Card, player: Player) -> None:
        if not self.cards:
            self.cards = [card]
            self.leader = player
        elif len(self.cards) >= 4:
            raise TrickFullException
        else:
            self.cards.append(card)

    def clear(self):
        self.cards, self.leader = None, None

    @property
    def winning_card(self) -> Optional[Card]:
        if not self.full:
            return None
        trump_cards = [card for card in self.cards if card.color.value == self.trump.value]
        cards_in_color = [card for card in self.cards if card.color == self.cards[0].color]
        return max(trump_cards, default=None) or max(cards_in_color)

    @property
    def winner(self) -> Player:
        winning_card_id = self.cards.index(self.winning_card) if self.winning_card is not None else -1
        if winning_card_id < 0:
            return None
        winner = self.leader
        for _ in range(winning_card_id):
            winner = winner.next
        return winner


@dataclass
class Deal:
    hand_w: Hand
    hand_n: Hand
    hand_e: Hand
    hand_s: Hand
    declarer: Player
    leader: Player
    contract: Contract

    @property
    def hands(self):
        return {
            Player.WEST: self.hand_w,
            Player.NORTH: self.hand_n,
            Player.EAST: self.hand_e,
            Player.SOUTH: self.hand_s,
        }

    @property
    def trump(self):
        return self.contract.trump

    @property
    def defence_pair(self):
        return 'NS' if self.declarer.value in 'NS' else 'WE'

    @property
    def offence_pair(self):
        return 'NS' if self.declarer.value not in 'NS' else 'WE'


@dataclass
class GameState:
    hands: Dict[Player, Hand]
    current_player: Player
    trump: Trump
    play_type: PlayType
    trick: Trick

    @staticmethod
    def from_deal(deal: Deal):
        return GameState(
            current_player=deal.leader,
            hands=deepcopy(deal.hands),
            trump=deal.trump,
            play_type=PlayType.DEFENCE,  # defence always start
            trick=Trick(deal.trump)
        )

    def to_dict(self):
        return asdict(self)

    @property
    def player_hand(self) -> Hand:
        return self.hands[self.current_player]

    @property
    def left_opponent_hand(self) -> Hand:
        return self.hands[self.current_player.next]

    @property
    def partner_hand(self) -> Hand:
        return self.hands[self.current_player.next.next]

    @property
    def right_opponent_hand(self) -> Hand:
        return self.hands[self.current_player.next.next.next]

    @property
    def valid_moves(self):
        vist_color = self.trick.color
        if not vist_color:
            return self.player_hand

        cards_in_color = {card for card in self.player_hand if card.color == vist_color}
        return cards_in_color or self.player_hand

    @property
    def any_hand_not_empty(self):
        return any((
            len(self.player_hand), len(self.left_opponent_hand), len(self.partner_hand), len(self.right_opponent_hand)
        ))

    def __str__(self):
        return (
            f'{self.trump.value}'
            f',{"".join(str(card) for card in self.trick.cards or [])}'
            f',{"".join(str(card) for card in self.player_hand or [])}'
            f',{"".join(str(card) for card in self.left_opponent_hand or [])}'
            f',{"".join(str(card) for card in self.partner_hand or [])}'
            f',{"".join(str(card) for card in self.right_opponent_hand or [])}'
        )


def hand_factory(cards: Iterable[str]) -> Set[Card]:
    return {Card.from_str(item) for item in cards}