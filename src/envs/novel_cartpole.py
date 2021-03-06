import math

import numpy as np
from gym import register, logger
from gym.envs.classic_control import CartPoleEnv


def register_novel_cartpole(max_episode_steps: int = 100,
                            random_acceleration: float = 10,
                            novelty_chance: float = 0.5,
                            reward_threshold: int = 200):
    register(
        id='NovelCartPole-v0',
        entry_point='envs.novel_cartpole:NovelCartPoleEnv',
        max_episode_steps=max_episode_steps,
        kwargs={
            'random_acceleration': random_acceleration,
            'novelty_chance': novelty_chance,
        },
        reward_threshold=reward_threshold
    )


class NovelCartPoleEnv(CartPoleEnv):
    """A game of CartPole that does novel things."""

    def __init__(self, random_acceleration, novelty_chance):
        super().__init__()
        self.random_acceleration = random_acceleration
        self.novelty_chance = novelty_chance

    def step(self, action):
        # Forgive me father, for I have sinned
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        state = self.state
        x, x_dot, theta, theta_dot = state
        force = self.force_mag if action == 1 else -self.force_mag
        # The spicy bits
        if np.random.random_sample() >= self.novelty_chance:
            force *= self.random_acceleration
        # End spicy bits
        costheta = math.cos(theta)
        sintheta = math.sin(theta)
        temp = (force + self.polemass_length * theta_dot * theta_dot * sintheta) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
                self.length * (4.0 / 3.0 - self.masspole * costheta * costheta / self.total_mass))
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass
        if self.kinematics_integrator == 'euler':
            x = x + self.tau * x_dot
            x_dot = x_dot + self.tau * xacc
            theta = theta + self.tau * theta_dot
            theta_dot = theta_dot + self.tau * thetaacc
        else:  # semi-implicit euler
            x_dot = x_dot + self.tau * xacc
            x = x + self.tau * x_dot
            theta_dot = theta_dot + self.tau * thetaacc
            theta = theta + self.tau * theta_dot
        self.state = (x, x_dot, theta, theta_dot)
        done = x < -self.x_threshold \
               or x > self.x_threshold \
               or theta < -self.theta_threshold_radians \
               or theta > self.theta_threshold_radians
        done = bool(done)

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this environment has already returned done = True. "
                            "You should always call 'reset()' once you receive 'done = True' -- any further steps are "
                            "undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state), reward, done, {}

    def _randomly_accelerate_cart(self, acceleration: float, chance: float):
        """Randomly accelerates the cart.

        Args:
            acceleration (float): The multipler of the cart's speed should it accelerate
            chance (float): The percent of the time the cart should
        """
