import copy
import torch
from torch.nn import functional as F
import numpy as np


class _Model(torch.nn.Module):
    def __init__(self, n_state: int, n_hidden: int) -> bool:
        super().__init__()
        self.hidden = torch.nn.Linear(n_state, n_hidden)
        self.output = torch.nn.Linear(n_hidden, 1)
        
    def forward(self, state):
        x = self.hidden(state)
        x = F.relu(x)
        x = self.output(x)
        return F.sigmoid(x)


class GeneticAgent:
    def __init__(self, bird_n: int) -> None:
        self.bird_n = bird_n
        self.models = [_Model(n_state=2, n_hidden=3) for _ in range(bird_n)]
        self.points = [0] * bird_n
        self.i = 0

    def __call__(self, state: tuple, passed: bool) -> bool:
        if (self.i % 4 == 0) or passed:
            bird_positions, pipe_positions = state
            pipe_pos = pipe_positions[0]
            return [self._do_jump(i, bird_pos, pipe_pos, passed) for i, bird_pos in enumerate(bird_positions)]

    def on_game_over(self):
        print(f"Points: {self.points}")
        best_i = np.argmax(self.points)
        if self.points[best_i] > 0:
            best_model = self.models[best_i]
            for i in range(len(self.models)):
                if i != best_i:
                    self.models[i] = self.modify_model(copy.deepcopy(best_model))
        else:
            self.models = [_Model(n_state=2, n_hidden=3) for _ in range(self.bird_n)]
        self.points = [0] * self.bird_n

    def _do_jump(self, i, bird_pos, pipe_pos, passed):
        if bird_pos:
            if passed:
                self.points[i] += 1
            x = (bird_pos[0] - pipe_pos[0], bird_pos[1] - pipe_pos[1])
            with torch.no_grad():
                y = self.models[i](torch.tensor(x, dtype=torch.float32))
            if y > 0.5:
                return True
        return False

    def modify_model(self, model: _Model):
        with torch.no_grad():
            for param in model.parameters():
                param.add_(torch.randn(param.size()) * 0.01)
        return model
