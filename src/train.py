import gym

from src.agents import RandomAgent
from src.data import player_deal
from src.env import BridgeEnv
from gym.envs.registration import register

register(id='Bridge-v0', entry_point='src.env:BridgeEnv', nondeterministic=False)

env: BridgeEnv = gym.make('Bridge-v0')
env.setup(player_deal, RandomAgent())

for i_episode in range(20):
    done = False
    observation = env.reset()
    while not done:
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print(reward, observation)
        if done:
            break
env.close()