import unittest

from tinyrunner.score import COIN_POINTS, Score


class ScoreTest(unittest.TestCase):
    def test_distance(self):
        s = Score()
        s.add_distance(3)
        self.assertEqual(s.total, 3)

    def test_single_coin(self):
        s = Score()
        s.add_coin(tick=1)
        self.assertEqual(s.total, COIN_POINTS)
        self.assertEqual(s.coins, 1)


if __name__ == "__main__":
    unittest.main()
