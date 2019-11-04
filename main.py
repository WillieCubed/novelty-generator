"""The entry point for novelty experimentation."""
import gym
import numpy as np
# noinspection PyUnresolvedReferences
from envs.novel_cartpole import register_novel_cartpole


def main():
    """Run experiments."""
    register_novel_cartpole(novelty_chance=1, random_acceleration=1000)
    print('Now playing NovelCartPole...')
    play_cartpole()


def play_cartpole(num_episodes: int = 20, seed: int = 17):
    """Play a game of CartPole with a novel environment.

    Training is affected how we expect: The greater the random acceleration,
    the more timesteps it takes for the agent to reach its goal.

    Args:
        num_episodes (int): The maximum number of episodes to train in the environment
        seed (int): 17 by default
    """
    # TODO: Generalize learning implementation to multiple types of envs
    env = gym.make('NovelCartPole-v0')
    np.random.seed(seed)
    env.seed(seed)
    # TODO: Use simple DQN
    for _ in range(num_episodes):
        observation = env.reset()
        for t in range(100):
            env.render()
            print(observation)
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if done:
                print(f'Done after {t + 1} timesteps')
                break
    env.close()


class GymRunner:
    """A manager class for running Gym experiments."""
    # TODO: Abstract away basic Gym loop
    pass


if __name__ == '__main__':
    main()
