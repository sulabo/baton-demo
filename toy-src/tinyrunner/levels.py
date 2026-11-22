"""Level rules. See docs/design.md "Levels"."""

LEVELS = {
    1: {"speed": 1},
    2: {"speed": 2},
    3: {"speed": 3},
}


def speed_for(level):
    if level not in LEVELS:
        raise ValueError(f"unknown level: {level}")
    return LEVELS[level]["speed"]


def last_level():
    return max(LEVELS)
