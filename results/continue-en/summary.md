| metric | baton off (n=6) median [min–max] | baton on (n=6) median [min–max] | on vs off (median) |
|---|---|---|---|
| input tokens (sum over model calls) | 122,764 [120,261–150,364] | 104,389 [104,284–104,982] | -15% |
| model calls | 5 [5–6] | 4 [4–4] | -20% |
| turns | 5 [5–11] | 4 [4–4] | -20% |
| tool calls | 4 [4–10] | 3 [3–3] | -25% |
| exploration calls | 4 [4–4] | 3 [3–3] | -25% |
| tool calls before the first file write (heuristic) | 3 [3–4] | 1 [1–1] | -67% |
| cost (USD) | 0.09 [0.09–0.11] | 0.09 [0.09–0.09] | -2% |
| wall time (s) | 21 [19–26] | 18 [18–19] | -14% |
| runs where the agent opened the handoff itself (its text came back in a tool result) | 6/6 | 0/6 | |
| runs whose combo passed the grader | 6/6 | 6/6 | |
| runs whose test suite passed | 6/6 | 6/6 | |
| runs where baton injected the handoff | 0/6 | 6/6 | |
