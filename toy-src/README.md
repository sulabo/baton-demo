# tinyrunner

Rules engine for a tiny endless-runner game. No graphics: the game loop is a
plain Python class you can drive from tests or from the command line.

## Run

```sh
python3 -m tinyrunner          # prints a simulated 30-tick run
python3 -m unittest            # runs the test suite (standard library only)
```

## Layout

| Path | What it holds |
|---|---|
| `tinyrunner/lives.py` | Starting lives, losing and gaining a life |
| `tinyrunner/score.py` | Coin points, distance points, combo (planned) |
| `tinyrunner/levels.py` | Level list and the speed of each level |
| `tinyrunner/obstacles.py` | Which obstacles can spawn on each level |
| `tinyrunner/game.py` | The tick loop that wires the rules together |
| `tinyrunner/cli.py` | `python3 -m tinyrunner` |
| `docs/design.md` | The game rules. Code follows this file |
| `docs/changelog.md` | What changed, newest first |
| `tests/` | One test file per module |

## Rules of thumb

- Game rules live in `docs/design.md` first, then in code.
- Each rule has one home: score rules in `score.py`, life rules in `lives.py`.
  `game.py` only calls them.
- Standard library only. No dependencies.

## License

MIT
