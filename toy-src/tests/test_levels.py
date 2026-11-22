import unittest

from tinyrunner.levels import last_level, speed_for


class LevelsTest(unittest.TestCase):
    def test_speeds(self):
        self.assertEqual([speed_for(n) for n in (1, 2, 3)], [1, 2, 3])

    def test_unknown_level(self):
        with self.assertRaises(ValueError):
            speed_for(99)

    def test_last_level(self):
        self.assertEqual(last_level(), 3)


if __name__ == "__main__":
    unittest.main()
