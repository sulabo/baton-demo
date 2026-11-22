| metric | baton off (n=6) median [min–max] | baton on (n=6) median [min–max] | on vs off (median) |
|---|---|---|---|
| input tokens (sum over model calls) | 122,896.5 [120,268–150,579] | 104,351 [77,743–158,691] | -15% |
| model calls | 5 [5–6] | 4 [3–6] | -20% |
| turns | 5 [5–6] | 4 [3–6] | -20% |
| tool calls | 4 [4–5] | 3 [2–5] | -25% |
| exploration calls | 4 [4–5] | 3 [2–4] | -25% |
| tool calls before the first file write (heuristic) | 3 [3–3] | 1 [1–1] | -67% |
| cost (USD) | 0.09 [0.09–0.10] | 0.09 [0.08–0.10] | -4% |
| wall time (s) | 23 [21–26] | 20 [17–22] | -13% |
| runs where the agent opened the handoff itself (its text came back in a tool result) | 6/6 | 0/6 | |
| runs whose combo passed the grader | 6/6 | 6/6 | |
| runs whose test suite passed | 6/6 | 6/6 | |
| runs where baton injected the handoff | 0/6 | 6/6 | |
