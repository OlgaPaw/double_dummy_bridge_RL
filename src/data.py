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

validation_deal_same_trump = Deal(
    #[Deal "N:KQ4.843.J7.AKQ97 T2.Q7.AT98643.J5 J953.AJT92.Q2.T3 A876.K65.K5.8642"]
    hand_n=hand_factory(['SK', 'SQ', 'S4', 'H8', 'H4', 'H3', 'DJ', 'D7', 'CA', 'CK', 'CQ', 'C9', 'C7']),
    hand_e=hand_factory(['ST', 'S2', 'HQ', 'H7', 'DA', 'DT', 'D9', 'D8', 'D6', 'D4', 'D3', 'CJ', 'C5']),
    hand_s=hand_factory(['SJ', 'S9', 'S5', 'S3', 'HA', 'HJ', 'HT', 'H9', 'H2', 'DQ', 'D2', 'CT', 'C3']),
    hand_w=hand_factory(['SA', 'S8', 'S7', 'S6', 'HK', 'H6', 'H5', 'DK', 'D5', 'C8', 'C6', 'C4', 'C2']),
    declarer=Player.NORTH,
    leader=Player.EAST,
    contract=Contract(3, Trump.SPADES),
)


validation_deal_other_trump = Deal(
    #[Deal "N:KQ4.843.J7.AKQ97 T2.Q7.AT98643.J5 J953.AJT92.Q2.T3 A876.K65.K5.8642"]
    hand_n=hand_factory(['SK', 'SQ', 'S4', 'H8', 'H4', 'H3', 'DJ', 'D7', 'CA', 'CK', 'CQ', 'C9', 'C7']),
    hand_e=hand_factory(['ST', 'S2', 'HQ', 'H7', 'DA', 'DT', 'D9', 'D8', 'D6', 'D4', 'D3', 'CJ', 'C5']),
    hand_s=hand_factory(['SJ', 'S9', 'S5', 'S3', 'HA', 'HJ', 'HT', 'H9', 'H2', 'DQ', 'D2', 'CT', 'C3']),
    hand_w=hand_factory(['SA', 'S8', 'S7', 'S6', 'HK', 'H6', 'H5', 'DK', 'D5', 'C8', 'C6', 'C4', 'C2']),
    declarer=Player.EAST,
    leader=Player.SOUTH,
    contract=Contract(3, Trump.DIAMONDS),
)
