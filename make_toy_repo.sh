#!/usr/bin/env bash
# Build the tinyrunner demo repo with a fixed git history.
#   bash make_toy_repo.sh <empty target dir>
# The handoff (HANDOFF.md) is committed at step 6, and one more commit lands after it,
# so baton's freshness line reports "1 commit since the handoff".
set -euo pipefail
SRC="$(cd "$(dirname "$0")/toy-src" && pwd)"
DEST="${1:?usage: make_toy_repo.sh <target dir>}"
[ -e "$DEST" ] && [ -n "$(ls -A "$DEST" 2>/dev/null)" ] && { echo "target not empty: $DEST" >&2; exit 1; }
mkdir -p "$DEST"
cd "$DEST"
git init -q -b main
git config user.name "tinyrunner dev"
git config user.email "dev@example.invalid"
printf '__pycache__/\n*.pyc\n' > .gitignore

step() {  # step <date> <message> <paths...>
  local when="$1" msg="$2"; shift 2
  for p in "$@"; do mkdir -p "$(dirname "$p")"; cp "$SRC/$p" "$p"; done
  git add -A
  GIT_AUTHOR_DATE="$when" GIT_COMMITTER_DATE="$when" git commit -q -m "$msg"
}

step "2026-11-10T10:00:00+09:00" "init: package skeleton, README, design doc" \
  README.md tinyrunner/__init__.py docs/design.md tests/__init__.py
step "2026-11-11T10:00:00+09:00" "lives: start at 3, cap at 5" \
  tinyrunner/lives.py tests/test_lives.py
step "2026-11-11T15:00:00+09:00" "score: coin and distance points" \
  tinyrunner/score.py tests/test_score.py
step "2026-11-13T10:00:00+09:00" "levels: speeds for levels 1-3" \
  tinyrunner/levels.py tests/test_levels.py
step "2026-11-14T10:00:00+09:00" "game: tick loop wiring lives, score and levels" \
  tinyrunner/game.py tinyrunner/cli.py tinyrunner/__main__.py tests/test_game.py
step "2026-11-14T18:00:00+09:00" "handoff: combo multiplier is next" \
  HANDOFF.md
step "2026-11-16T10:00:00+09:00" "obstacles: spawn table per level" \
  tinyrunner/obstacles.py tests/test_obstacles.py docs/changelog.md
git log --oneline | cat
