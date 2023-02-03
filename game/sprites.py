import random
import numpy as np
import pygame
from pygame.sprite import Sprite, Group
from game import window


class Pipe(Sprite):
    _INITIAL_IMAGE = pygame.image.load('images/pipe.png').convert()
    _VELOCITY = -0.05

    def __init__(self, x, y, upside=False):
        Sprite.__init__(self)
        self.image = self._INITIAL_IMAGE
        if upside:
            self.image = pygame.transform.flip(self.image, flip_x=False, flip_y=True)
            self.rect = self.image.get_rect(left=x, bottom=y)
        else:
            self.rect = self.image.get_rect(left=x, top=y)

    def update(self, dt) -> bool:
        self.rect.move_ip(self._VELOCITY * dt, 0)
        if self.rect.right < 0:
            self.kill()


class PipePair(Group):
    _GAP_SIZE = 130
    _GAP_MIDDLE_RANGE = (200, window.HEIGHT - 200)

    def __init__(self):
        super().__init__(self)
        self.gap_middle = self._generate_gap_middle()
        self.upper_pipe = Pipe(window.WIDTH, self.gap_middle - (self._GAP_SIZE // 2), upside=True)
        self.lower_pipe = Pipe(window.WIDTH, self.gap_middle + (self._GAP_SIZE // 2), upside=False)
        self.add(self.upper_pipe, self.lower_pipe)

    @property
    def right(self) -> int:
        return self.lower_pipe.rect.right

    @property
    def left(self) -> int:
        return self.lower_pipe.rect.left

    @property
    def pipes(self) -> tuple[Pipe]:
        return self.upper_pipe, self.lower_pipe

    @staticmethod
    def _generate_gap_middle():
        randoms = [random.randint(*PipePair._GAP_MIDDLE_RANGE) for _ in range(5)]
        best_i = np.argmin([min((r - l)**2 for l in PipePair._GAP_MIDDLE_RANGE) for r in randoms])
        return randoms[best_i]

class Bird(Sprite):
    _INITIAL_IMAGE = pygame.image.load('images/bird.png').convert()
    _ACC = 0.00006
    _ANGLE_VELOCITY = -0.015
    _JUMP_VELOCITY = -0.08
    _JUMP_ANGLE = 35

    def __init__(self, x, y, angle=0):
        Sprite.__init__(self)
        self._position = pygame.Vector2(x, y)
        self._angle = angle
        self._velocity = 0

        self.image = self._INITIAL_IMAGE
        self.rect = self.image.get_rect(center=self._position)

    def update(self, dt):
        self._update_position(dt)
        self._update_angle(dt)
        self.image = pygame.transform.rotate(self._INITIAL_IMAGE, self._angle)
        self.rect = self.image.get_rect(center=self._position)

    def jump(self):
        self._velocity = self._JUMP_VELOCITY
        self._angle = self._JUMP_ANGLE

    def _update_position(self, dt):
        self._velocity += self._ACC * dt
        if (self.rect.bottom < 0) and (self._velocity < 0):
            self._position.y = -self.image.get_height()
        elif (self.rect.top > window.HEIGHT) and (self._velocity > 0):
            self._position.y = window.HEIGHT + self.image.get_height()
        else:
            self._position.y += self._velocity * dt

    def _update_angle(self, dt):
        if self._angle > -90:
            self._angle += self._ANGLE_VELOCITY * dt
