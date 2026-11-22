#!/usr/bin/env python3
"""Check a run's tinyrunner/score.py against the Combo rule in docs/design.md.
   python3 -I grade_combo.py <run dir>   → prints JSON {"checks": {...}, "pass": bool}
Runs the session's code in a child process, so a broken file only fails the checks."""
import json, subprocess, sys

PROBE = r'''
import json, sys
sys.path.insert(0, ".")
out = {}
def check(name, fn):
    try: out[name] = bool(fn())
    except Exception as e: out[name] = False
from tinyrunner.score import Score
from tinyrunner.game import Game
def coins(ticks, reset_after=None):
    s = Score()
    for i, t in enumerate(ticks):
        s.add_coin(tick=t)
        if reset_after is not None and i == reset_after: s.reset_combo()
    return s.total
check("design_example_70", lambda: coins([1, 2, 4, 9]) == 70)
check("cap_at_x4", lambda: coins([1, 2, 3, 4, 5]) == 140)
check("window_inclusive_3", lambda: coins([1, 4]) == 30)
check("gap_4_restarts", lambda: coins([1, 5]) == 20)
check("reset_combo", lambda: coins([1, 2, 3], reset_after=1) == 40)
def dist():
    s = Score(); s.add_coin(tick=1); s.add_coin(tick=2); s.add_distance(5); return s.total == 35
check("distance_not_multiplied", dist)
def game():
    g = Game(level=1)
    for e in ("coin", "coin", "hit", "coin"): g.step(e)
    return g.score.total == 44
check("game_hit_resets_combo", game)
print(json.dumps(out))
'''

def main(run_dir):
    p = subprocess.run([sys.executable, "-I", "-c", PROBE], cwd=run_dir, capture_output=True, text=True, timeout=30)
    try: checks = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception: checks = {}
    print(json.dumps({"checks": checks, "pass": bool(checks) and all(checks.values()), "error": p.stderr[-300:] if not checks else ""}))

if __name__ == "__main__":
    main(sys.argv[1])
