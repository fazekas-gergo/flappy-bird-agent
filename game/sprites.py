from random import randint
import pygame
from pygame import Vector2, Surface
from pygame.sprite import Sprite, Group


class Pipe(Sprite):
    _INITIAL_IMAGE: Surface = None
    _VELOCITY = -0.1

    @classmethod
    def config(cls, image_path):
        cls._INITIAL_IMAGE = pygame.image.load(image_path).convert()

    def __init__(self, x, y, upside=False):
        Sprite.__init__(self)
        self.image = self._INITIAL_IMAGE
        if upside:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(left=x, bottom=y)
        else:
            self.rect = self.image.get_rect(left=x, top=y)

    def update(self, dt) -> bool:
        self.rect.move_ip(self._VELOCITY * dt, 0)
        if self.rect.right < 0:
            self.kill()


class PipePair(Group):
    _GAP_TOP_RANGE = None
    _GAP_SIZE = None
    _WINDOW_WIDTH = None

    @classmethod
    def config(cls, gap_top_range: tuple, gap_size, window_width):
        cls._GAP_TOP_RANGE = gap_top_range
        cls._GAP_SIZE = gap_size
        cls._WINDOW_WIDTH = window_width

    def __init__(self):
        super().__init__(self)
        gap_start = randint(*self._GAP_TOP_RANGE)
        upper_pipe = Pipe(self._WINDOW_WIDTH, gap_start, upside=True)
        lower_pipe = Pipe(self._WINDOW_WIDTH, gap_start + self._GAP_SIZE, upside=False)
        self.add(lower_pipe, upper_pipe)

        self.gap_middle = gap_start + (self._GAP_SIZE // 2)
        self._lower_pipe = lower_pipe

    @property
    def right(self) -> int:
        return self._lower_pipe.rect.right

    @property
    def left(self) -> int:
        return self._lower_pipe.rect.left


class Bird(Sprite):
    _INITIAL_IMAGE: Surface = None
    MAX_POS_Y: int = None
    _ACC = 0.0005
    _ANGLE_VELOCITY = -0.05
    _JUMP_VELOCITY = -0.25
    _JUMP_ANGLE = 35

    @classmethod
    def config(cls, image_path: str, max_pos_y: int):
        Bird._INITIAL_IMAGE = pygame.image.load(image_path).convert()
        cls._MAX_POS_Y = max_pos_y

    def __init__(self, x, y, angle=0):
        Sprite.__init__(self)
        self._position = Vector2(x, y)
        self._angle = angle
        self._velocity = 0

        self.image = self._INITIAL_IMAGE
        self.rect = self.image.get_rect(center=self._position)

    def update(self, dt):
        self._update_position_and_angle(dt)
        self.image = pygame.transform.rotate(self._INITIAL_IMAGE, self._angle)
        self.rect = self.image.get_rect(center=self._position)

    def jump(self):
        self._velocity = self._JUMP_VELOCITY
        self._angle = self._JUMP_ANGLE

    def is_out(self):
        return ((self.rect.bottom < 0) and (self._velocity < 0)) or (
            (self.rect.top > self._MAX_POS_Y) and self._velocity > 0
        )

    def _update_position_and_angle(self, dt):
        self._velocity += self._ACC * dt
        if not self.is_out():
            self._position.y += self._velocity * dt
        if self._angle > -90:
            self._angle += self._ANGLE_VELOCITY * dt
