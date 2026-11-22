"""Life rules. See docs/design.md "Lives"."""

START_LIVES = 3
MAX_LIVES = 5


class Lives:
    def __init__(self, start=START_LIVES):
        self.left = start

    def lose_life(self):
        if self.left > 0:
            self.left -= 1

    def gain_life(self):
        self.left = min(self.left + 1, MAX_LIVES)

    @property
    def dead(self):
        return self.left == 0
