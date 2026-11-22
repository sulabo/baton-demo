"""Obstacle spawn tables. See docs/design.md "Levels" and "Obstacles"."""

SPAWN = {
    1: ("rock",),
    2: ("rock", "log"),
    3: ("rock", "log", "bird"),
}


def can_spawn(level, obstacle):
    return obstacle in SPAWN.get(level, ())
