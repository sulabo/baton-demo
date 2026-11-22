# baton on/off demo — tinyrunner

The same "pick up where we left off" prompt, run in fresh copies of a small public-safe repo, with and without baton.
Everything here was written for this demo: the repo, the handoff and the grader. Nothing comes from a private project.

## What runs

- **Repo**: `tinyrunner`, a 7-commit Python package (standard library only, 13 tests). `make_toy_repo.sh` builds it from
  `toy-src/` with fixed commit dates. `HANDOFF.md` (2,357 characters, baton's section template) is committed at commit 6 and
  says the next step is a combo multiplier in `tinyrunner/score.py`. One more commit (obstacles) lands after it, so the handoff
  is slightly out of date on purpose.
- **Arms**
  - `off`: no baton. `HANDOFF.md` is still in the repo; the agent can open it.
  - `on`: baton `v1.0.0-beta.3` loaded with `--plugin-dir`. Nothing else differs.
- **Isolation**: `claude -p --output-format stream-json --verbose --include-hook-events`, with
  `--setting-sources project --strict-mcp-config` (no user settings, no user plugins, no MCP servers),
  a minimal environment, `--permission-mode bypassPermissions` with Claude Code's sandbox settings turned on
  (`sandbox.enabled`, `failIfUnavailable`, reads under `$HOME` denied), and `BATON_OBSERVE=off` plus per-run `XDG_CACHE_HOME`/`XDG_CONFIG_HOME`, so runs share nothing and stay out of
  baton's usage log. Each run gets a new copy of the repo. Arms alternate (off,on / on,off).
- **After each run**: the repo's test suite, and `grade_combo.py`, which checks seven cases of the combo rule in
  `docs/design.md` against the session's code.

## Reproduce

```sh
# 1. baton at the release tag
git clone https://github.com/sulabo/baton && git -C baton checkout v1.0.0-beta.3

# 2. runs (Claude Code 2.1.330 was used; any logged-in Claude Code works)
python3 run_demo.py run --baton ./baton --work /tmp/baton-demo --out results/status-en \
    --n 6 --model sonnet --prompt "Where were we?"
python3 run_demo.py run --baton ./baton --work /tmp/baton-demo --out results/continue-en \
    --n 6 --model sonnet --prompt "Pick up where we left off and continue with the next step."
python3 run_demo.py run --baton ./baton --work /tmp/baton-demo --out results/continue-ko \
    --n 6 --model sonnet --prompt "이어서 해줘"
python3 run_demo.py run --baton ./baton --work /tmp/baton-demo --out results/status-en-opus \
    --n 3 --model opus --prompt "Where were we?"
python3 run_demo.py run --baton ./baton --work /tmp/baton-demo --out results/continue-en-opus \
    --n 3 --model opus --prompt "Pick up where we left off and continue with the next step."

# 3. tables (re-counts from the saved streams)
python3 run_demo.py report --out results/status-en
```

`--run-usd` (default 2) caps one run, `--total-usd` (default 20) caps a batch. The 48 runs below cost USD 5.13
(`total_cost_usd` summed); with a 2-run pilot and 2 discarded runs, about USD 6.

Run one batch at a time per `--out` folder. Two runners on the same folder share run directories and spoil each other's
runs (that happened once here; those two runs were deleted and run again).

## Results (2026-11-23, Claude Code 2.1.330)

Medians, with [min–max]; token medians are rounded to whole tokens. "Input tokens" is the sum over the main thread's model calls of
`input + cache_creation + cache_read` tokens, i.e. everything sent to the model, cached or not.

### "Where were we?" — status question

| | Sonnet 5.5, off (n=6) | Sonnet 5.5, on (n=6) | change | Opus 5.5, off (n=3) | Opus 5.5, on (n=3) | change |
|---|---|---|---|---|---|---|
| agent opened the handoff itself | 6/6 | 0/6 | | 3/3 | 0/3 | |
| model calls | 3.5 [3–4] | 2 [2–2] | −1.5 | 4 [3–4] | 2 [2–2] | −2 |
| tool calls | 2.5 [2–3] | 1 [1–1] | | 3 [2–4] | 1 [1–1] | |
| input tokens | 82,210 [68,580–93,797] | 49,678 [49,450–49,769] | **−40%** | 97,589 [72,339–99,040] | 50,187 [49,942–50,579] | **−49%** |
| cost (USD) | 0.07 | 0.06 | −5% | 0.15 | 0.13 | −13% |
| wall time (s) | 14 | 10 | −26% | 25 | 15 | −40% |

### "Pick up where we left off and continue with the next step." — continue and do the work

| | Sonnet 5.5, off (n=6) | Sonnet 5.5, on (n=6) | change |
|---|---|---|---|
| agent opened the handoff itself | 6/6 | 0/6 | |
| combo passed the grader (7 cases) | 6/6 | 6/6 | same |
| model calls | 5 [5–6] | 4 [4–4] | −1 |
| tool calls before the first file write | 3 [3–4] | 1 [1–1] | −2 |
| input tokens | 122,764 [120,261–150,364] | 104,389 [104,284–104,982] | **−15%** |
| cost (USD) | 0.09 | 0.09 | −2% |
| wall time (s) | 21 | 18 | −14% |

Same prompt in Korean ("이어서 해줘"), Sonnet 5.5, n=6 each: opened the handoff 6/6 vs 0/6, grader 6/6 vs 6/6,
model calls 5 → 4, input tokens 122,897 → 104,351 (**−15%**, on ranged 77,743–158,691), cost 0.09 → 0.09 (−4%).

**Opus 5.5 on the same continue prompt went the other way** (n=3 each):

| | Opus 5.5, off (n=3) | Opus 5.5, on (n=3) | change |
|---|---|---|---|
| agent opened the handoff itself | 3/3 | 0/3 | |
| combo passed the grader | 3/3 | 3/3 | same |
| model calls | 6 [5–7] | 7 [6–7] | +1 |
| tool calls | 5 [4–6] | 11 [10–11] | |
| input tokens | 154,439 [126,568–186,250] | 193,764 [165,446–194,994] | **+25%** |
| cost (USD) | 0.21 | 0.25 | +18% |
| wall time (s) | 46 | 48 | +4% |

The extra calls were not a search for the handoff. In all three `on` runs the agent edited with Claude Code's Edit tool,
which needs a Read of the file first, so it read files again that it had already printed with `cat`. In all three `off`
runs it edited through shell commands and never used Read. Three runs each can't tell whether baton's injected header
("check one or two claims against git and the files before you continue") caused that switch or it was chance.

### Why the cost barely moves

Almost all of the saved tokens are **cache reads**: the same conversation prefix re-sent on each extra model call, billed
at a fraction of the normal input price. New content written to the cache is about the same in both arms
(status, Sonnet: 12,369 vs 13,011 tokens; the injected page is new content in the `on` arm, the file the agent opens is new
content in the `off` arm). In a repo this small, one or two fewer calls is a small bill.

## What this demo does not show

- A big repo. Here the `off` agent finds the handoff in one command because the repo is tiny and the file sits at the top.
- A long session. Each run is one prompt and ends after 2–6 model calls.
- That the handoff was right. It was written for the demo and is only one commit stale.
- Other people's setups. The first call here carries about 22.3K tokens without baton and 24.6K with it (the injected
  page is the 2.3K difference), because no user plugins or instructions are loaded. A real setup carries more, which makes
  every extra call cost more.

## Files

- `make_toy_repo.sh`, `toy-src/` — the repo.
- `run_demo.py` — runner and report. `grade_combo.py` — the grader.
- `results/<set>/` — `runs.json` (one row per run), `summary.md` (the table), `<arm>-<i>.jsonl` (the stream-json output,
  with local paths replaced by `/work`, `/plugins`, `/tmp/x`, `~`), `<arm>-<i>.diff` (what the session changed).
- Pilot, not counted: one run per arm with "Where were we? Pick up where we left off." The `off` run only reported the
  status; the `on` run went on and implemented the feature. One run each can't separate that from chance, so the prompts
  above ask either for status or for work.

## License

MIT. See `LICENSE`. baton itself: https://github.com/sulabo/baton
