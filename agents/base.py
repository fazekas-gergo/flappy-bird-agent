import pygame
from game import window

class Agent:
    bird_n = 1

    def __call__(self, *args, **kwargs) -> list[bool]:
        if pygame.KEYDOWN in [evt.type for evt in window.events]:
            return [True]
        return [False]

    def on_game_over(self):
        pass


class LimitAgent(Agent):
    def __call__(self, state, *args, **kwargs) -> list[bool]:
        bird_positions, pipe_positions = state
        bird_pos, pipe_pos = bird_positions[0], pipe_positions[0]
        return [(bird_pos[1] - pipe_pos[1]) > 40]
