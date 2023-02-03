import pygame
from pygame.sprite import Sprite

SPEED = 60
FLAGS = pygame.DOUBLEBUF

pygame.init()
_background = pygame.image.load('images/background.png')
_window = pygame.display.set_mode((_background.get_width(), _background.get_height()), FLAGS)
_background.convert()
_clock = pygame.time.Clock()

WIDTH = _window.get_width()
HEIGHT = _window.get_height()


events: list[pygame.event.Event] = []


def update(*sprites: Sprite):
    global events
    events = pygame.event.get()
    _window.blits(((_background, (0, 0)), *[(s.image, s.rect) for s in sprites]))
    pygame.display.flip()
    _clock.tick(SPEED)
