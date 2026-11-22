import unittest

from tinyrunner.lives import Lives, MAX_LIVES, START_LIVES


class LivesTest(unittest.TestCase):
    def test_start(self):
        self.assertEqual(Lives().left, START_LIVES)

    def test_lose_until_dead(self):
        lives = Lives()
        for _ in range(START_LIVES):
            lives.lose_life()
        self.assertTrue(lives.dead)
        lives.lose_life()
        self.assertEqual(lives.left, 0)

    def test_gain_is_capped(self):
        lives = Lives()
        for _ in range(10):
            lives.gain_life()
        self.assertEqual(lives.left, MAX_LIVES)


if __name__ == "__main__":
    unittest.main()
