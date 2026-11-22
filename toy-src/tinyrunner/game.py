"""The tick loop. It only calls the rule modules; rules live in their own files."""

from .levels import speed_for
from .lives import Lives
from .score import Score


class Game:
    def __init__(self, level=1):
        self.tick = 0
        self.level = level
        self.lives = Lives()
        self.score = Score()

    def step(self, event=None):
        """Advance one tick. event is None, "coin", "hit" or "heart"."""
        if self.over:
            return
        self.tick += 1
        self.score.add_distance(speed_for(self.level))
        if event == "coin":
            self.score.add_coin(self.tick)
        elif event == "hit":
            self.lives.lose_life()
            self.score.reset_combo()
        elif event == "heart":
            self.lives.gain_life()

    @property
    def over(self):
        return self.lives.dead
