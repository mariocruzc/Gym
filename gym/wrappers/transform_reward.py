"""Wrapper for transforming the reward."""
from typing import Callable

import gym
from gym import RewardWrapper


class TransformReward(RewardWrapper):
    """Transform the reward via an arbitrary function.

    Example:
        >>> import gym
        >>> env = gym.make('CartPole-v1')
        >>> env = TransformReward(env, lambda r: 0.01*r)
        >>> env.reset()
        >>> observation, reward, done, info = env.step(env.action_space.sample())
        >>> reward
        0.01
    """

    def __init__(self, env: gym.Env, f: Callable[[float], float]):
        """Initialize the :class:`TransformReward` wrapper with an environment and reward transform function :param:`f`.

        Args:
            env: The environment to apply the wrapper
            f: A function that transforms the reward
        """
        super().__init__(env)
        assert callable(f)
        self.f = f

    def reward(self, reward):
        """Transforms the reward using callable :attr:`f`.

        Args:
            reward: The reward to transform

        Returns:
            The transformed reward
        """
        return self.f(reward)
