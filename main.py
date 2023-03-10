import pygame
from agents.base import Agent, LimitAgent
from agents.genetic import GeneticAgent
from game import Game, window


def main(agent: Agent):
    game = Game()
    game.reset()
    while pygame.QUIT not in [evt.type for evt in window.events]:
        state, passed, game_over = game.update()
        if game_over:
            agent.on_game_over()
            game.reset(agent.bird_n)
        else:
            do_jump = agent(state, passed)
            game.jump(do_jump)


if __name__ == '__main__':
    main(GeneticAgent(10))
