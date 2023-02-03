from itertools import chain
from pygame.sprite import Sprite
from game.sprites import PipePair, Bird
from game import window

from pygame.sprite import spritecollideany


class PipePairManager:
    def __init__(self) -> None:
        self._pipe_pairs: list[PipePair] = [PipePair()]
        self._counter = 0

    def reset(self):
        self._pipe_pairs = [PipePair()]
        self._counter = 0

    def update(self, dt):
        for pipe_pair in self._pipe_pairs:
            pipe_pair.update(dt)
        self._counter += 1
        if (self._counter % (window.SPEED - 10)) == 0:
            self._pipe_pairs.append(PipePair())

    def pop_first(self):
        self._pipe_pairs.pop(0)

    @property
    def pipe_pairs(self) -> list[PipePair]:
        return self._pipe_pairs

    @property
    def closest(self) -> PipePair:
        if len(self._pipe_pairs):
            return self._pipe_pairs[0]
        return PipePair()

    @property
    def sprites(self) -> list[Sprite]:
        return list(chain(*[pipe_pair.sprites() for pipe_pair in self._pipe_pairs]))


class Game:
    def __init__(self):
        self.birds: list[Bird] = []
        self.pipe_pair_manager: PipePairManager = PipePairManager()

    def reset(self, bird_n: int = 1):
        self.birds = [Bird(20, 20) for _ in range(bird_n)]
        self.pipe_pair_manager.reset()
        window.update()

    def update(self):
        self._update_positions()
        window.update(*[bird for bird in self.birds if bird], *self.pipe_pair_manager.sprites)
        if passed := self._is_passed():
            self.pipe_pair_manager.pop_first()
        self._handle_collisions()
        return (self._bird_positions, self._pipe_pair_positions), passed, self._is_game_over()

    def jump(self, do_jump: list[bool]):
        for bird, jump in zip(self.birds, do_jump):
            if jump:
                bird.jump()

    @property
    def _bird_positions(self):
        return tuple(bird.rect.center if bird else None for bird in self.birds)

    @property
    def _pipe_pair_positions(self):
        return tuple((pipe_pair.left, pipe_pair.gap_middle) 
            for pipe_pair in self.pipe_pair_manager.pipe_pairs)

    def _is_game_over(self):
        return not any(self.birds)

    def _is_passed(self):
        bird = next(bird for bird in self.birds if bird is not None)
        return bird.rect.left > self.pipe_pair_manager.closest.right

    def _update_positions(self):
        for bird in self.birds:
            if bird:
                bird.update(window.SPEED)
        self.pipe_pair_manager.update(window.SPEED)

    def _handle_collisions(self):
        for i, collided in enumerate(self._are_birds_collided()):
            if collided:
                self.birds[i].kill()
                self.birds[i] = None

    def _are_birds_collided(self):
        closest_pipe_pair = self.pipe_pair_manager.closest
        return tuple(
            spritecollideany(bird, closest_pipe_pair) if bird else False for bird in self.birds)
