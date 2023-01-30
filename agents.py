import random

import numpy as np
from game import Bird
from game.game import PipePairs


def no_agent(*args, **kwargs):
    pass


def random_agent(bird: Bird, _):
    if random.random() > 0.95:
        bird.jump()


def limit_agent(bird: Bird, pipe_pairs: PipePairs):
    closest_pipe_pair = pipe_pairs.get()
    if closest_pipe_pair:
        if bird.rect.bottom > closest_pipe_pair.gap_middle + 55:
            bird.jump()


class MlAgent:
    def __init__(self):
        self.memory = list()
        self.w = np.zeros(3)
        self.alpha = 1.5
        self.e = 5e-3

    def __call__(self, bird: Bird, pipe_pairs: PipePairs):
        state = self._get_state(bird, pipe_pairs)
        x = np.concatenate(([1], state))  # Add bias
        y_est = _sigmoid(np.dot(x, self.w))
        if np.random.random() > (1 - self.e):
            y_est = 1 - y_est
        if y_est > 0.5:
            bird.jump()
        self.memory.append((x, y_est))

    def train(self, better: bool, points):
        self._set_hiperparams(points)
        for i, (state, y_est) in enumerate(self.memory[::-1], start=1):
            gamma = (0.95**i) * (1 / len(self.memory))
            y = int((y_est > 0.5) == better)
            self.w += self._gradient(state, y, y_est) * self.alpha * gamma
        self.memory.clear()
        print(self.w)

    def _set_hiperparams(self, points):
        if (points == 0) and (self.alpha > 1):
            self.alpha = 0.1
            self.e = 5e-3
        elif points > 0:
            self.alpha = 0.01
            self.e = 0

    def _get_state(self, bird: Bird, pipe_pairs: PipePairs) -> np.ndarray:
        closest_pipes = pipe_pairs.get()
        vertical_distance = closest_pipes.gap_middle - bird.rect.bottom if closest_pipes else 0
        horizontal_distance = closest_pipes.right - bird.rect.left if closest_pipes else 600
        return np.array([horizontal_distance / 200, vertical_distance / 400])

    def _gradient(self, x, y, y_est):
        e = y - y_est
        sigm_der = y_est * (1 - y_est)
        return x * e * sigm_der


def _sigmoid(x: np.ndarray):
    return 1 / (1 + np.exp(-x))
