"""python3 -m tinyrunner: print a simulated run."""

from .game import Game

PATTERN = [None, "coin", "coin", None, "coin", None, None, None, "hit", "coin"]


def main(ticks=30):
    g = Game(level=1)
    for i in range(ticks):
        g.step(PATTERN[i % len(PATTERN)])
    print(f"ticks={g.tick} score={g.score.total} coins={g.score.coins} lives={g.lives.left}")


if __name__ == "__main__":
    main()
