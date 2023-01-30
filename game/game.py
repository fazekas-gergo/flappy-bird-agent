from game.window import Window
from game.sprites import *
from pygame.sprite import spritecollideany
from queue import Queue

TIMER_EVENT = pygame.USEREVENT + 1
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, TIMER_EVENT])


class Game:
    def __init__(self, background_img, bird_img, pipe_img, gap_size=130, gap_margin=100, **kwargs):
        self._window = Window(background_img, **kwargs)
        self.bird = None
        self.pipe_pairs = PipePairs()
        pygame.time.set_timer(TIMER_EVENT, 1_700)

        Bird.config(bird_img, max_pos_y=self._window.height)
        Pipe.config(pipe_img)
        PipePair.config(
            gap_top_range=(gap_margin, self._window.height - (gap_margin + gap_size)),
            gap_size=gap_size,
            window_width=self._window.width,
        )

    def attempt(self, agent=None) -> bool:
        points = 0
        self._reset()
        while not spritecollideany(self.bird, self.pipe_pairs.get()):
            self._handle_events()
            if self._is_bird_passed_pipe():
                self.pipe_pairs.pop()
                points += 1
            if self.bird.is_out():
                points -= 0.1
            agent(self.bird, self.pipe_pairs)
            self._window.update()
        return points

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == TIMER_EVENT:
                self._start_pipes()
            elif event.type == pygame.KEYDOWN:
                self.bird.jump()

    def _reset(self):
        self._window.reset()
        self.pipe_pairs.clear()
        self.bird = Bird(40, 30)
        self._window.sprites.add(self.bird)

    def _start_pipes(self):
        pipe_pair = PipePair()
        self.pipe_pairs.add(pipe_pair)
        self._window.sprites.add(pipe_pair)

    def _is_bird_passed_pipe(self):
        if len(self.pipe_pairs):
            return self.bird.rect.left > self.pipe_pairs.get().right


class PipePairs:
    def __init__(self):
        self._queue = Queue()
        self.default = Group()

    def get(self, i=0) -> Group | PipePair:
        if self._queue.qsize() <= i:
            return self.default
        return self._queue.queue[i]

    def pop(self):
        self._queue.get()

    def add(self, pipe_pair: PipePair):
        self._queue.put(pipe_pair)

    def clear(self):
        self._queue = Queue()

    def __len__(self):
        return self._queue.qsize()
