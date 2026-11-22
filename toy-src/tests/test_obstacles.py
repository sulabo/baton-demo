import unittest

from tinyrunner.obstacles import can_spawn


class ObstaclesTest(unittest.TestCase):
    def test_level_tables(self):
        self.assertTrue(can_spawn(1, "rock"))
        self.assertFalse(can_spawn(1, "bird"))
        self.assertTrue(can_spawn(3, "bird"))

    def test_unknown_level(self):
        self.assertFalse(can_spawn(9, "rock"))


if __name__ == "__main__":
    unittest.main()
