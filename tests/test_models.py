import pytest

from src.models import Card, Color, Contract, Deal, GameState, Player, PlayType, Trick, Trump, hand_factory


def test_next_player():
    south = Player.SOUTH
    north = Player.NORTH
    west = Player.WEST
    east = Player.EAST

    assert south.next == west
    assert west.next == north
    assert north.next == east
    assert east.next == south


def test_player_partner():
    south = Player.SOUTH
    north = Player.NORTH
    west = Player.WEST
    east = Player.EAST

    assert south.partner == north
    assert north.partner == south
    assert west.partner == east
    assert east.partner == west


def test_state_from_deal():
    deal = Deal(
        hand_w={Card(0)},
        hand_n={Card(1)},
        hand_e={Card(2)},
        hand_s={Card(3)},
        declarer=Player.SOUTH,
        leader=Player.EAST,
        contract=Contract(1, Trump('NT'))
    )

    state = GameState.from_deal(deal)
    assert state.player_hand == {Card(2)}
    assert state.left_opponent_hand == {Card(3)}
    assert state.partner_hand == {Card(0)}
    assert state.right_opponent_hand == {Card(1)}
    assert state.current_player == Player.EAST
    assert state.trump == Trump('NT')
    assert state.play_type == PlayType.DEFENCE


@pytest.mark.parametrize(
    'trick,expected_cards', (
        (Trick(Trump('NT')), {Card(0), Card(13), Card(26), Card(39)}),
        (Trick(Trump('NT'), [Card(1)]), {Card(0)}),
        (Trick(Trump('NT'), [Card(14)]), {Card(13)}),
        (Trick(Trump('NT'), [Card(27)]), {Card(26)}),
        (Trick(Trump('NT'), [Card(51)]), {Card(39)}),
    )
)
def test_valid_moves(trick, expected_cards):
    state = GameState(
        hands={
            Player.EAST: {Card(0), Card(13), Card(26), Card(39)},
            Player.WEST: None,
            Player.SOUTH: None,
            Player.NORTH: None,
        },
        current_player=Player.EAST,
        trump=Trump('NT'),
        play_type=PlayType.DEFENCE,
        trick=trick,
    )
    assert state.valid_moves == expected_cards


@pytest.mark.parametrize(
    'trick,winning_card,winner', (
        (Trick(Trump('NT')), None, None),
        (Trick(Trump('NT'), [Card(1)], Player.EAST), None, None),
        (
            Trick(Trump('NT'), [Card(0), Card(1), Card(2), Card(3)], Player.EAST),
            Card(3),
            Player.NORTH,
        ),
        (
            Trick(Trump('C'), [Card(0), Card(1), Card(2), Card(3)], Player.EAST),
            Card(3),
            Player.NORTH,
        ),
        (
            Trick(Trump('C'), [Card(0), Card(13), Card(14), Card(15)], Player.EAST),
            Card(0),
            Player.EAST,
        ),
        (
            Trick(Trump('D'), [Card(0), Card(13), Card(15), Card(14)], Player.EAST),
            Card(15),
            Player.WEST,
        ),
        (
            Trick(Trump('D'), [Card(0), Card(3), Card(2), Card(1)], Player.EAST),
            Card(3),
            Player.SOUTH,
        ),
    )
)
def test_winning_card(trick, winning_card, winner):
    assert trick.winning_card == winning_card
    assert trick.winner == winner


@pytest.mark.parametrize(
    'trick,expected', (
        (
            Trick(Trump('NT')),
            Trick(Trump('NT'), [Card(0)], Player.NORTH),
        ),
        (
            Trick(Trump('NT'), [Card(1)], Player.EAST),
            Trick(Trump('NT'), [Card(1), Card(0)], Player.EAST),
        ),
    )
)
def test_add_card(trick, expected):
    trick.add_card(Card(0), Player.NORTH)
    assert trick == expected


@pytest.mark.parametrize(
    'card_number,expected_color', (
        (0, Color.CLUBS),
        (12, Color.CLUBS),
        (13, Color.DIAMONDS),
        (26, Color.HEARTS),
        (39, Color.SPADES),
        (51, Color.SPADES),
    )
)
def test_card_color(card_number, expected_color):
    assert Card(card_number).color == expected_color


def test_hand_factory():
    hand = hand_factory(['SK', 'SJ', 'S9', 'S3', 'HJ', 'H4', 'DA', 'D9', 'D8', 'CQ', 'C7', 'C6', 'C4'])
    spades = (Card(50), Card(48), Card(46), Card(40))
    hearts = (Card(35), Card(28))
    diamonds = (Card(19), Card(20), Card(25))
    clubs = (Card(2), Card(4), Card(5), Card(10))
    assert hand == {*spades, *hearts, *diamonds, *clubs}
