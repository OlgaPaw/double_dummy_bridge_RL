import csv
import random
import statistics
from copy import deepcopy

import gym
from gym.envs.registration import register

from src.agents import Agent, DeepQLearnAgent
from src.data import opponent_deal, player_deal, validation_deal_other_trump, validation_deal_same_trump
from src.env import BridgeEnv

register(id='Bridge-v0', entry_point='src.env:BridgeEnv', nondeterministic=False)


def get_next_deal():
    while True:
        yield player_deal
        yield opponent_deal
        yield validation_deal_same_trump
        yield validation_deal_other_trump


def play(env: BridgeEnv, player: Agent, opponent: Agent, episodes=10000):
    deal_iterator = get_next_deal()
    for i in range(episodes):
        done = False
        first_move = env.setup(next(deal_iterator), opponent)
        trick_won = 0
        invalid_actions = 0
        cards_played = [first_move] if first_move else []
        while not done:
            state = deepcopy(env.state)
            action = player.move(state)
            if action not in state.valid_moves:
                invalid_actions += 1
                action = random.sample(state.valid_moves, 1)[0]
            _, reward, done, info = env.step(action)
            cards_played.append(info)
            if reward == 1:
                trick_won += 1
            if done:
                yield i, invalid_actions, trick_won, cards_played
                break


DEALS = ['offence', 'defence', 'same_trump', 'other_trump']

if __name__ == '__main__':
    env: BridgeEnv = gym.make('Bridge-v0')

    player = DeepQLearnAgent()
    opponent = DeepQLearnAgent()
    env.setup(player_deal, opponent)
    deals_count = len(DEALS)
    values = {i: {'invalid_actions': [], 'tricks_won': []} for i in range(deals_count)}
    files = dict(zip(DEALS, [None] * deals_count))
    files = {i: open(f'results/validate/{deal}.csv', 'w') for i, deal in enumerate(DEALS)}

    for episode, invalid_actions, trick_won, cards_played in play(env, player, opponent, deals_count * 100):
        game_file = files[episode % deals_count]

        values[episode % deals_count]['invalid_actions'].append(invalid_actions)
        values[episode % deals_count]['tricks_won'].append(trick_won)
        csv.writer(game_file).writerow((episode // deals_count, invalid_actions, trick_won, "".join(cards_played)))

    for fd in files.values():
        fd.close()

    print("################SUMMARY############")
    for i, value in values.items():
        print(DEALS[i].upper())
        print(
            f"invalid min:{min(value['invalid_actions'])} "
            f"max:{max(value['invalid_actions'])} "
            f"mean:{statistics.mean(value['invalid_actions'])} "
        )
        print(
            f"tricks_won min:{min(value['tricks_won'])} "
            f"max:{max(value['tricks_won'])} "
            f"mean:{statistics.mean(value['tricks_won'])} "
        )
    env.close()
