"""Score rules. See docs/design.md "Score"."""

COIN_POINTS = 10
DISTANCE_POINTS = 1  # per unit of distance


class Score:
    def __init__(self):
        self.total = 0
        self.coins = 0

    def add_distance(self, distance):
        self.total += distance * DISTANCE_POINTS

    def add_coin(self, tick):
        """Called by game.py with the tick the coin was collected on.

        Combo is not implemented yet: every coin is worth COIN_POINTS.
        """
        self.coins += 1
        self.total += COIN_POINTS

    def reset_combo(self):
        """Called by game.py when a life is lost. Does nothing until combo lands."""
