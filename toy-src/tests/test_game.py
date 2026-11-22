import unittest

from tinyrunner.game import Game


class GameTest(unittest.TestCase):
    def test_distance_follows_level_speed(self):
        g = Game(level=2)
        g.step()
        g.step()
        self.assertEqual(g.score.total, 4)

    def test_hit_costs_a_life(self):
        g = Game()
        g.step("hit")
        self.assertEqual(g.lives.left, 2)

    def test_game_over_stops_ticks(self):
        g = Game()
        for _ in range(3):
            g.step("hit")
        self.assertTrue(g.over)
        g.step()
        self.assertEqual(g.tick, 3)


if __name__ == "__main__":
    unittest.main()
