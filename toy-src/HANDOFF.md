# Session Handoff (작성: 2026-11-14 · combo multiplier is next)

## 목표와 완료 조건 · Goal and done-when
- Goal: coins collected close together are worth more (the "Combo" rule in `docs/design.md`).
- Done when: `Score.add_coin` applies the combo multiplier, `Score.reset_combo` resets it,
  `tests/test_score.py` covers the example in `docs/design.md` (ticks 1, 2, 4, 9 → 70 coin points),
  and `python3 -m unittest` passes.

## 확인된 사실과 결정 · Confirmed facts and decisions
- [V] The rule is written down: `docs/design.md` "Combo" (window = 3 ticks, ×1 ×2 ×3 then ×4 cap, reset on life lost). Read 2026-11-14.
- [V] `game.py` already calls `score.add_coin(self.tick)` and `score.reset_combo()` on a hit. Checked with `grep -n score tinyrunner/game.py`.
- [V] Only coin points are multiplied, never distance points (design.md, last bullet of "Combo").
- [?] The "within 3 ticks" check is inclusive (`<= 3`). design.md says so; no test pins it yet.

## 관련 파일·심볼 · Files and symbols
- `tinyrunner/score.py`: `Score.add_coin`, `Score.reset_combo` — the only file that should change for the rule.
- `tests/test_score.py`: add the combo tests here.
- `docs/design.md`: "Combo" — the source of truth.
- `tinyrunner/game.py`: `Game.step` — calls the two methods above. Should not need changes.

## 이미 한 변경 · Already changed
- `game.py` tick loop and `cli.py` landed (commit "game: tick loop ...").
- `reset_combo()` exists as a no-op so `game.py` can call it already.

## 실패한 접근법 (다시 시도 금지) · Failed approaches (do not retry)
- Tracking the combo inside `game.py`: rejected. Score rules live in `score.py` only (README "Rules of thumb").

## 검증 증거 · Evidence
- `python3 -m unittest` → 11 tests OK (before the combo work).

## 남은 리스크와 다음 행동 · Risks and next step
- Risk: `add_coin(tick)` signature must stay the same, `game.py` depends on it.
- Next step: combo is not implemented (`add_coin` adds a flat 10, see its docstring) → implement it in
  `score.py`, write the tests in `tests/test_score.py` first, then run `python3 -m unittest`.
- After that: update `docs/changelog.md` with a new entry.

## 승격 후보 (DECISIONS.md로 올릴 것) · Promotion candidates
- None.

### 기각됨 (다시 올리지 않는다) · Rejected
- None.
