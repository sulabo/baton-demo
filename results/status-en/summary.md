| metric | baton off (n=6) median [min–max] | baton on (n=6) median [min–max] | on vs off (median) |
|---|---|---|---|
| input tokens (sum over model calls) | 82,209.5 [68,580–93,797] | 49,677.5 [49,450–49,769] | -40% |
| model calls | 3.5 [3–4] | 2 [2–2] | -43% |
| turns | 3.5 [3–4] | 2 [2–2] | -43% |
| tool calls | 2.5 [2–3] | 1 [1–1] | -60% |
| exploration calls | 2.5 [2–3] | 1 [1–1] | -60% |
| tool calls before the first file write (heuristic) | 2.5 [2–3] | 1 [1–1] | -60% |
| cost (USD) | 0.07 [0.06–0.07] | 0.06 [0.06–0.06] | -5% |
| wall time (s) | 13.5 [11–26] | 10 [10–11] | -26% |
| runs where the agent opened the handoff itself (its text came back in a tool result) | 6/6 | 0/6 | |
| runs whose combo passed the grader | 0/6 | 0/6 | |
| runs whose test suite passed | 6/6 | 6/6 | |
| runs where baton injected the handoff | 0/6 | 6/6 | |
