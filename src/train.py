import csv
import statistics
from copy import deepcopy

import gym
from gym.envs.registration import register

from src.agents import Agent, DeepQLearnAgent
from src.data import opponent_deal, player_deal
from src.env import BridgeEnv

register(id='Bridge-v0', entry_point='src.env:BridgeEnv', nondeterministic=False)


def get_next_deal():
    while True:
        yield player_deal
        yield opponent_deal


def learn(env: BridgeEnv, player: Agent, opponent: Agent, episodes=10000):
    max_invalid = 50
    deal_iterator = get_next_deal()
    for i in range(episodes):
        done = False
        first_move = env.setup(next(deal_iterator), opponent)
        cumulative_reward = 0
        invalid_actions = 0
        cards_played = [first_move] if first_move else []
        while not done:
            state = deepcopy(env.state)
            action = player.move(state)
            observation, reward, done, info = env.step(action)
            if reward >= -1:
                cumulative_reward += reward
            else:
                invalid_actions += 1
            cards_played.append(info)
            player.update_q(state, action, reward, env.state)
            if done or invalid_actions > max_invalid:
                yield i, invalid_actions, cumulative_reward, cards_played
                break


if __name__ == '__main__':
    for i in range(30):
        env: BridgeEnv = gym.make('Bridge-v0')

        player = DeepQLearnAgent(learning_rate=0.2, discount_factor=0.4, rand_factor=0.1)
        opponent = DeepQLearnAgent()

        env.setup(player_deal, opponent)
        values = {0: {'invalid_actions': [], 'rewards': []}, 1: {'invalid_actions': [], 'rewards': []}}
        with open(f'results/{i}offence-{player.__class__.__name__}-{player.__class__.__name__}.csv', 'w') as offence:
            with open(
                f'results/{i}defence-{player.__class__.__name__}-{player.__class__.__name__}.csv', 'w'
            ) as defence:
                for episode, invalid_actions, reward, cards_played in learn(env, player, opponent, 200):
                    game_file = offence if episode % 2 else defence

                    print(episode // 2, invalid_actions, reward, "".join(cards_played))
                    values[episode % 2]['invalid_actions'].append(invalid_actions)
                    values[episode % 2]['rewards'].append(reward)
                    csv.writer(game_file).writerow((episode // 2, invalid_actions, reward, "".join(cards_played)))

        print("################SUMMARY############")
        print("OFFENCE")
        print(
            f"invalid min:{min(values[0]['invalid_actions'])} "
            f"max:{max(values[0]['invalid_actions'])} "
            f"mean:{statistics.mean(values[0]['invalid_actions'])} "
        )
        print(
            f"rewards min:{min(values[0]['rewards'])} "
            f"max:{max(values[0]['rewards'])} "
            f"mean:{statistics.mean(values[0]['rewards'])} "
        )
        print("DEFENCE")
        print(
            f"invalid min:{min(values[1]['invalid_actions'])} "
            f"max:{max(values[1]['invalid_actions'])} "
            f"mean:{statistics.mean(values[1]['invalid_actions'])} "
        )
        print(
            f"rewards min:{min(values[1]['rewards'])} "
            f"max:{max(values[1]['rewards'])} "
            f"mean:{statistics.mean(values[1]['rewards'])} "
        )

        env.close()
        player.save()
        print("Saved")