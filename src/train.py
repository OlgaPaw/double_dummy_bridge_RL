import csv

import gym
from gym.envs.registration import register

from src.agents import Agent, QLearnAgent
from src.data import opponent_deal, player_deal
from src.env import BridgeEnv

register(id='Bridge-v0', entry_point='src.env:BridgeEnv', nondeterministic=False)


def get_next_deal():
    while True:
        yield player_deal
        yield opponent_deal


def learn(env: BridgeEnv, player: Agent, opponent: Agent, episodes=10000):
    for i in range(episodes):
        done = False
        env.setup(next(get_next_deal()), opponent)
        cumulative_reward = 0
        cards_played = []
        while not done:
            state_key = str(env.state)
            action = player.move(env.state)
            observation, reward, done, info = env.step(action)
            cumulative_reward += reward
            cards_played.append(info)
            new_state_key = str(env.state)
            player.update_q(state_key, action, reward, new_state_key)
            if done:
                yield i, cumulative_reward, cards_played
                break
        env.close()
        player.save()


if __name__ == '__main__':
    env: BridgeEnv = gym.make('Bridge-v0')

    player = QLearnAgent(learning_rate=0.2, discount_factor=0.9, rand_factor=0.2)
    opponent = QLearnAgent()
    env.setup(player_deal, opponent)
    with open(f'results/offence-{player.__class__.__name__}-{player.__class__.__name__}.csv', 'w') as offence:
        with open(f'results/defence-{player.__class__.__name__}-{player.__class__.__name__}.csv', 'w') as defence:
            for episode, reward, cards_played in learn(env, player, opponent, 200):
                game_file = offence if episode % 2 else defence
                csv.writer(game_file).writerow((episode // 2, reward, "".join(cards_played)))
