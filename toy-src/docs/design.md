# tinyrunner design

The rules below are the source of truth. When code and this file disagree,
fix the code (or change this file on purpose, in the same commit).

## Ticks

The game advances one tick at a time. Each tick the runner moves forward by
the current level's speed and may meet one event: a coin, an obstacle hit, or
nothing.

## Lives

- The runner starts with 3 lives.
- An obstacle hit costs one life.
- A heart pickup gives one life back, up to a maximum of 5.
- The game is over at 0 lives.

## Score

- Distance: 1 point per unit of distance (so speed × ticks).
- Coin: 10 points.

### Combo

Coins collected close together are worth more.

- A coin collected within 3 ticks of the previous coin continues the combo.
  "Within 3 ticks" means `tick - previous_coin_tick <= 3`.
- The multiplier is the position in the combo: the first coin is ×1, the second
  ×2, the third ×3, and every coin after that ×4 (the cap).
- A gap of more than 3 ticks starts a new combo at ×1.
- Losing a life resets the combo: the next coin is ×1.
- Only coin points are multiplied. Distance points are never multiplied.

Example: coins at ticks 1, 2, 4, 9 score 10 + 20 + 30 + 10 = 70 coin points.

## Levels

| Level | Speed | Obstacles |
|---|---|---|
| 1 | 1 | rock |
| 2 | 2 | rock, log |
| 3 | 3 | rock, log, bird |

## Obstacles

Each level has a spawn table. An obstacle can only spawn on a level whose
table lists it.
