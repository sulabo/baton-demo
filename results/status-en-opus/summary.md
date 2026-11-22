| metric | baton off (n=3) median [min–max] | baton on (n=3) median [min–max] | on vs off (median) |
|---|---|---|---|
| input tokens (sum over model calls) | 97,589 [72,339–99,040] | 50,187 [49,942–50,579] | -49% |
| model calls | 4 [3–4] | 2 [2–2] | -50% |
| turns | 4 [3–5] | 2 [2–2] | -50% |
| tool calls | 3 [2–4] | 1 [1–1] | -67% |
| exploration calls | 3 [2–4] | 1 [1–1] | -67% |
| tool calls before the first file write (heuristic) | 3 [2–4] | 1 [1–1] | -67% |
| cost (USD) | 0.15 [0.14–0.15] | 0.13 [0.13–0.13] | -13% |
| wall time (s) | 25 [23–27] | 15 [15–18] | -40% |
| runs where the agent opened the handoff itself (its text came back in a tool result) | 3/3 | 0/3 | |
| runs whose combo passed the grader | 0/3 | 0/3 | |
| runs whose test suite passed | 3/3 | 3/3 | |
| runs where baton injected the handoff | 0/3 | 3/3 | |
