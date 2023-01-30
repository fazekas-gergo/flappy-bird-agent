import pygame
from pygame.sprite import Group

pygame.init()


class Window:
    def __init__(self, background_img_path: str, frame_rate: int = 30):
        # Timing
        self.frame_rate = frame_rate
        self._clock = pygame.time.Clock()
        # Sprites
        self.sprites = Group()
        # Background
        self.background = pygame.image.load(background_img_path)
        self.width = self.background.get_width()
        self.height = self.background.get_height()
        self._screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = self.background.convert()

    def update(self):
        dt = self._clock.tick(self.frame_rate)
        dirty_rects = [s.rect.copy() for s in self.sprites]
        self.sprites.clear(self._screen, self.background)
        self.sprites.update(dt)
        self.sprites.draw(self._screen)
        dirty_rects.extend([s.rect for s in self.sprites])
        pygame.display.update(dirty_rects)

    def reset(self):
        self.sprites.empty()
        self._screen.blit(self.background, (0, 0))
        pygame.display.flip()
