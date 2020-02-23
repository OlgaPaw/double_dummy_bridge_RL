from src.models import Contract, Deal, Player, Trump, hand_factory

player_deal = Deal(
    #[Deal "N:KJ93.J4.A98.Q764 T6.QT3.KJT654.T2 AQ875.962.7.AJ85 42.AK875.Q32.K93"]
    hand_n=hand_factory(['SK', 'SJ', 'S9', 'S3', 'HJ', 'H4', 'DA', 'D9', 'D8', 'CQ', 'C7', 'C6', 'C4']),
    hand_e=hand_factory(['ST', 'S6', 'HQ', 'HT', 'H3', 'DK', 'DJ', 'DT', 'D6', 'D5', 'D4', 'CT', 'C2']),
    hand_s=hand_factory(['SA', 'SQ', 'S8', 'S7', 'S5', 'H9', 'H6', 'H2', 'D7', 'CA', 'CJ', 'C8', 'C5']),
    hand_w=hand_factory(['S4', 'S2', 'HA', 'HK', 'H8', 'H7', 'H5', 'DQ', 'D3', 'D2', 'CK', 'C9', 'C3']),
    declarer=Player.SOUTH,
    leader=Player.WEST,
    contract=Contract(4, Trump.SPADES),
)

opponent_deal = Deal(
    #[Deal "N:KJ93.J4.A98.Q764 T6.QT3.KJT654.T2 AQ875.962.7.AJ85 42.AK875.Q32.K93"]
    hand_e=hand_factory(['SK', 'SJ', 'S9', 'S3', 'HJ', 'H4', 'DA', 'D9', 'D8', 'CQ', 'C7', 'C6', 'C4']),
    hand_s=hand_factory(['ST', 'S6', 'HQ', 'HT', 'H3', 'DK', 'DJ', 'DT', 'D6', 'D5', 'D4', 'CT', 'C2']),
    hand_w=hand_factory(['SA', 'SQ', 'S8', 'S7', 'S5', 'H9', 'H6', 'H2', 'D7', 'CA', 'CJ', 'C8', 'C5']),
    hand_n=hand_factory(['S4', 'S2', 'HA', 'HK', 'H8', 'H7', 'H5', 'DQ', 'D3', 'D2', 'CK', 'C9', 'C3']),
    declarer=Player.SOUTH,
    leader=Player.EAST,
    contract=Contract(4, Trump.SPADES),
)

other_deal = Deal(
    #[Deal "S:QT95.Q963.K.K975 AK87.K4.QJT62.AQ 62.AJT7.54.J8643 J43.852.A9873.T2"]
    hand_n=hand_factory(['SQ', 'ST', 'S9', 'S5', 'HQ', 'H9', 'H6', 'H3', 'DK', 'CK', 'C9', 'C7', 'C5']),
    hand_e=hand_factory(['SA', 'SK', 'S8', 'S7', 'HK', 'H4', 'DQ', 'DJ', 'DT', 'D6', 'D2', 'CA', 'CQ']),
    hand_s=hand_factory(['S6', 'S2', 'HA', 'HJ', 'HT', 'H7', 'D6', 'D4', 'CJ', 'C8', 'C6', 'C4', 'C3']),
    hand_w=hand_factory(['SJ', 'S4', 'S3', 'H8', 'H5', 'H2', 'DA', 'D9', 'D8', 'D7', 'D3', 'CT', 'C2']),
    declarer=Player.WEST,
    leader=Player.NORTH,
    contract=Contract(3, Trump.NO_TRUMP),
)
