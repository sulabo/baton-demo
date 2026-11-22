#!/usr/bin/env python3
"""baton on/off demo: the same "pick up where we left off" prompt in fresh copies of the tinyrunner repo.

  python3 run_demo.py run --baton <baton checkout at v1.0.0-beta.3> --work <scratch dir> --out results/<label> \
      [--n 5] [--prompt "Where were we? Pick up where we left off."] [--model sonnet] [--max-turns 30] \
      [--run-usd 2] [--total-usd 20]
  python3 run_demo.py report --out results/<label>

Each run:
  - builds a new repo with make_toy_repo.sh (same commits, same HANDOFF.md every time);
  - runs `claude -p ... --output-format stream-json` with no user settings, no MCP servers, no user plugins
    (`--setting-sources project --strict-mcp-config`, minimal environment). Arm "on" adds `--plugin-dir <baton>`;
    arm "off" has no baton at all. HANDOFF.md is in the repo in both arms;
  - Bash runs in Claude Code's sandbox with reads under $HOME denied, so a run can't see anything but the repo;
  - afterwards runs the repo's tests and grade_combo.py, and saves the stream with local paths replaced.
Arms alternate (off,on / on,off) to spread time-of-day drift. BATON_OBSERVE=off keeps the runs out of baton's usage log.
"""
import argparse, json, os, re, shutil, statistics, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PROMPT = "Where were we? Pick up where we left off."
HANDOFF_FIRST_LINE = "# Session Handoff (작성: 2026-11-14"  # make_toy_repo.sh가 만드는 인계서 첫 줄 — 도구 결과에 이게 나오면 에이전트가 인계서를 연 것
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
# ponytail: 셸로 파일을 쓰는 흔한 꼴만 잡는다(리다이렉트·sed -i·tee·파이썬 open(...,'w')). 변수로 만든 경로 등은 놓친다
BASH_WRITE = re.compile(r"(?<![0-9&])>>?\s*(?!/dev/null|&)[\w./~-]+|\bsed\s+-i\b|\btee\b|open\([^)]*['\"][wa]['\"]|\.write_text\(")
EXPLORE_BASH = re.compile(r"^\s*(ls|find|tree|cat|head|tail|sed\s+-n|grep|rg|wc|git\s+(?:log|status|show|diff|ls-files|blame))\b")


def claude_bin():
    for c in (os.path.expanduser("~/.local/bin/claude"), shutil.which("claude")):
        if c and os.path.exists(c): return os.path.realpath(c)
    sys.exit("claude binary not found")


def sandbox_settings(run_dir):
    return json.dumps({
        "sandbox": {"enabled": True, "filesystem": {"denyRead": ["~/"], "allowRead": [run_dir]},
                    "allowUnsandboxedCommands": False, "failIfUnavailable": True},
        "permissions": {"blockReadsOutsideWorkingDirectories": True},
    })


LEFTOVER = [(re.compile(r"/private/tmp/claude-\d+/[^\"\s\\]*"), "/tmp/x"),   # 하네스 임시 폴더·세션 기록 경로
            (re.compile(r"-Users-[A-Za-z0-9._-]*"), "-work"),
            (re.compile(r"-private-tmp-claude-\d+-*"), "-tmp-")]                     # 세션 기록 폴더 이름(경로 슬러그)


def scrub(text, pairs):
    for a, b in pairs:
        text = text.replace(a, b)
    for rx, b in LEFTOVER:
        text = rx.sub(b, text)
    return text


def run_one(a, arm, i):
    label_dir = os.path.join(os.path.abspath(a.work), os.path.basename(os.path.abspath(a.out)))
    run_dir = os.path.join(label_dir, f"{arm}-{i}", "tinyrunner")
    if os.path.exists(os.path.dirname(run_dir)): shutil.rmtree(os.path.dirname(run_dir))
    subprocess.run(["bash", os.path.join(HERE, "make_toy_repo.sh"), run_dir], check=True, capture_output=True)
    base = subprocess.run(["git", "-C", run_dir, "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    cache = os.path.join(os.path.dirname(run_dir), "xdg-cache"); cfg = os.path.join(os.path.dirname(run_dir), "xdg-config")
    os.makedirs(cache); os.makedirs(cfg)
    bin_ = claude_bin()
    cmd = [bin_, "-p", a.prompt, "--output-format", "stream-json", "--verbose", "--include-hook-events",
           "--model", a.model, "--max-turns", str(a.max_turns), "--max-budget-usd", str(a.run_usd),
           "--setting-sources", "project", "--strict-mcp-config", "--permission-mode", "bypassPermissions",
           "--settings", sandbox_settings(run_dir)]
    if arm == "on": cmd += ["--plugin-dir", os.path.abspath(a.baton)]
    tmp = os.path.join(os.path.dirname(run_dir), "tmp"); os.makedirs(tmp)
    env = {k: os.environ[k] for k in ("HOME", "USER", "LOGNAME", "SHELL") if k in os.environ}
    env["TMPDIR"] = tmp  # 부모 세션의 임시 폴더를 물려받지 않게
    env.update(PATH=":".join([os.path.dirname(bin_), os.path.dirname(os.path.realpath(sys.executable)),
                              "/opt/homebrew/bin", "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin"]),
               LANG="en_US.UTF-8", TERM="xterm-256color", XDG_CACHE_HOME=cache, XDG_CONFIG_HOME=cfg,
               BATON_OBSERVE="off", GIT_CONFIG_GLOBAL="/dev/null")
    raw = os.path.join(os.path.dirname(run_dir), "stream.jsonl")
    t0 = time.time()
    with open(raw, "w") as fo, open(raw + ".err", "w") as fe:
        try:
            rc = subprocess.run(cmd, cwd=run_dir, stdin=subprocess.DEVNULL, stdout=fo, stderr=fe, env=env, timeout=1200).returncode
        except subprocess.TimeoutExpired:
            rc = "timeout"
    secs = round(time.time() - t0)
    tests = subprocess.run([sys.executable, "-m", "unittest"], cwd=run_dir, capture_output=True, text=True, timeout=120)
    m = re.search(r"Ran (\d+) test", tests.stderr)
    grade = json.loads(subprocess.run([sys.executable, "-I", os.path.join(HERE, "grade_combo.py"), run_dir],
                                      capture_output=True, text=True, timeout=60).stdout)
    g = ["git", "-C", run_dir, "-c", "core.fsmonitor=", "-c", "core.hooksPath=/dev/null"]
    subprocess.run(g + ["add", "-A"], check=False, capture_output=True)
    stat = subprocess.run(g + ["diff", "--cached", "--stat", base], capture_output=True, text=True).stdout.strip().splitlines()
    changed = [ln.split("|")[0].strip() for ln in stat[:-1]] if stat else []
    os.makedirs(a.out, exist_ok=True)
    pairs = [(run_dir, "/work/tinyrunner"), (label_dir, "/work"), (os.path.abspath(a.baton), "/plugins/baton"),
             (os.path.expanduser("~"), "~"),
             (os.environ.get("USER", "\0"), "user")]
    with open(raw) as f: body = scrub(f.read(), pairs)
    with open(os.path.join(a.out, f"{arm}-{i}.jsonl"), "w") as f: f.write(body)
    with open(os.path.join(a.out, f"{arm}-{i}.diff"), "w") as f:
        f.write(scrub(subprocess.run(g + ["diff", "--cached", base], capture_output=True, text=True).stdout, pairs))
    return {"arm": arm, "i": i, "rc": rc, "seconds": secs, "tests_ok": tests.returncode == 0,
            "tests_ran": int(m.group(1)) if m else None, "grade_pass": grade["pass"], "grade": grade["checks"],
            "changed": changed, **analyze(os.path.join(a.out, f"{arm}-{i}.jsonl"))}


def bash_explore(cmd):
    return any(EXPLORE_BASH.match(seg) for seg in re.split(r"\|\||&&|[;|\n]", cmd))


def analyze(path):
    calls, first, sub_calls, sub_tokens = {}, None, set(), 0
    tools, explore, before_edit, edited, handoff_read, injected, result = 0, 0, 0, False, 0, False, {}
    handoff_seen = 0
    names = {}
    for ln in open(path):
        try: d = json.loads(ln)
        except json.JSONDecodeError: continue
        t = d.get("type")
        if t == "system" and "[baton] 아래는" in json.dumps(d, ensure_ascii=False): injected = True
        if t == "result": result = d
        if t == "user" and not d.get("parent_tool_use_id"):
            for b in (d.get("message") or {}).get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_result" and HANDOFF_FIRST_LINE in json.dumps(b.get("content"), ensure_ascii=False):
                    handoff_seen += 1
        if t != "assistant": continue
        m = d.get("message") or {}
        u = m.get("usage") or {}
        tok = sum(u.get(k, 0) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
        if d.get("parent_tool_use_id"):
            if m.get("id") not in sub_calls: sub_calls.add(m.get("id")); sub_tokens += tok
            continue
        if m.get("id") not in calls:
            calls[m.get("id")] = tok
            if first is None: first = tok
        for b in m.get("content") or []:
            if not isinstance(b, dict) or b.get("type") != "tool_use": continue
            n = b.get("name"); inp = b.get("input") or {}
            tools += 1; names[n] = names.get(n, 0) + 1
            ex = n in ("Read", "Grep", "Glob", "LS") or (n in ("Agent", "Task")) or (n == "Bash" and bash_explore(str(inp.get("command", ""))))
            explore += ex
            if n in EDIT_TOOLS or (n == "Bash" and BASH_WRITE.search(str(inp.get("command", "")))): edited = True
            if not edited: before_edit += 1
            blob = json.dumps(inp)
            if "HANDOFF.md" in blob and (n == "Read" or (n == "Bash" and re.search(r"\b(cat|head|tail|sed|less|grep)\b[^|;&]*HANDOFF\.md", blob))):
                handoff_read += 1
    return {"model_calls": len(calls), "input_tokens": sum(calls.values()), "first_call": first,
            "num_turns": result.get("num_turns"), "cost_usd": result.get("total_cost_usd"), "subtype": result.get("subtype"),
            "tool_calls": tools, "explore_calls": explore, "tools_before_first_edit": before_edit,
            "handoff_reads": handoff_read, "handoff_seen": handoff_seen, "baton_injected": injected, "sub_calls": len(sub_calls), "sub_tokens": sub_tokens,
            "tool_names": names}


def cmd_run(a):
    os.makedirs(a.out, exist_ok=True)
    idx_path = os.path.join(a.out, "runs.json")
    idx = json.load(open(idx_path)) if os.path.exists(idx_path) else []
    done = {(r["arm"], r["i"]) for r in idx}
    spent = sum(r.get("cost_usd") or 0 for r in idx)
    for i in range(1, a.n + 1):
        for arm in (("off", "on") if i % 2 else ("on", "off")):
            if (arm, i) in done: continue
            if spent >= a.total_usd:
                print(f"STOP: total budget {a.total_usd} USD reached ({spent:.2f})"); return
            r = run_one(a, arm, i)
            spent += r.get("cost_usd") or 0
            idx.append(r); json.dump(idx, open(idx_path, "w"), indent=1, ensure_ascii=False)
            print(f"{arm}-{i}: rc={r['rc']} {r['seconds']}s turns={r['num_turns']} calls={r['model_calls']} "
                  f"in={r['input_tokens']:,} tools={r['tool_calls']} cost={r['cost_usd']} grade={r['grade_pass']} "
                  f"tests={r['tests_ok']}/{r['tests_ran']} injected={r['baton_injected']} spent={spent:.2f}", flush=True)
    cmd_report(a)


def cmd_report(a):
    idx = json.load(open(os.path.join(a.out, "runs.json")))
    for r in idx:  # 분석 규칙을 고치면 저장된 스트림으로 다시 센다(실행 결과·채점은 그대로)
        r.update(analyze(os.path.join(a.out, f"{r['arm']}-{r['i']}.jsonl")))
    keys = [("input_tokens", "input tokens (sum over model calls)"), ("model_calls", "model calls"), ("num_turns", "turns"),
            ("tool_calls", "tool calls"), ("explore_calls", "exploration calls"),
            ("tools_before_first_edit", "tool calls before the first file write (heuristic)"), ("cost_usd", "cost (USD)"), ("seconds", "wall time (s)")]
    arms = [x for x in ("off", "on") if any(r["arm"] == x for r in idx)]
    rows = {x: [r for r in idx if r["arm"] == x] for x in arms}
    lines = ["| metric | " + " | ".join(f"baton {x} (n={len(rows[x])}) median [min–max]" for x in arms) + " | on vs off (median) |",
             "|---|" + "---|" * (len(arms) + 1)]
    for k, label in keys:
        cells, meds = [], {}
        for x in arms:
            v = [r[k] for r in rows[x] if r.get(k) is not None]
            meds[x] = statistics.median(v) if v else None
            # 중앙값이 .5로 끝나면 그대로 보인다(반올림하면 3.5가 4로 보여 글에 잘못 옮겨졌다 — 11-23)
            f = (lambda z: f"{z:,.2f}") if k == "cost_usd" else (lambda z: f"{z:,.0f}" if float(z).is_integer() else f"{z:,.1f}")
            cells.append(f"{f(meds[x])} [{f(min(v))}–{f(max(v))}]" if v else "-")
        delta = f"{(meds['on'] - meds['off']) / meds['off'] * 100:+.0f}%" if len(arms) == 2 and meds.get("off") else "-"
        lines.append(f"| {label} | " + " | ".join(cells) + f" | {delta} |")
    for k, label in (("handoff_seen", "runs where the agent opened the handoff itself (its text came back in a tool result)"), ("grade_pass", "runs whose combo passed the grader"),
                     ("tests_ok", "runs whose test suite passed"), ("baton_injected", "runs where baton injected the handoff")):
        lines.append(f"| {label} | " + " | ".join(f"{sum(bool(r[k]) for r in rows[x])}/{len(rows[x])}" for x in arms) + " | |")
    out = "\n".join(lines)
    print(out)
    print("\nper run:")
    for r in sorted(idx, key=lambda r: (r["arm"], r["i"])):
        print(f"  {r['arm']}-{r['i']}: in={r['input_tokens']:,} calls={r['model_calls']} turns={r['num_turns']} tools={r['tool_calls']} "
              f"explore={r['explore_calls']} before_edit={r['tools_before_first_edit']} handoff_seen={r['handoff_seen']} "
              f"cost={r['cost_usd']:.2f} grade={r['grade_pass']} tests={r['tests_ok']}/{r['tests_ran']} sub={r['sub_calls']} "
              f"changed={','.join(r['changed'])}")
    with open(os.path.join(a.out, "summary.md"), "w") as f: f.write(out + "\n")


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sp = p.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run")
    r.add_argument("--baton", required=True); r.add_argument("--work", required=True); r.add_argument("--out", required=True)
    r.add_argument("--n", type=int, default=5); r.add_argument("--prompt", default=DEFAULT_PROMPT)
    r.add_argument("--model", default="sonnet"); r.add_argument("--max-turns", type=int, default=30)
    r.add_argument("--run-usd", type=float, default=2.0); r.add_argument("--total-usd", type=float, default=20.0)
    q = sp.add_parser("report"); q.add_argument("--out", required=True)
    a = p.parse_args(argv)
    {"run": cmd_run, "report": cmd_report}[a.cmd](a)


if __name__ == "__main__":
    main(sys.argv[1:])
