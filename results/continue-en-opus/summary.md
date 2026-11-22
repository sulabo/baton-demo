| metric | baton off (n=3) median [min–max] | baton on (n=3) median [min–max] | on vs off (median) |
|---|---|---|---|
| input tokens (sum over model calls) | 154,439 [126,568–186,250] | 193,764 [165,446–194,994] | +25% |
| model calls | 6 [5–7] | 7 [6–7] | +17% |
| turns | 6 [5–7] | 12 [11–12] | +100% |
| tool calls | 5 [4–6] | 11 [10–11] | +120% |
| exploration calls | 5 [4–6] | 8 [8–8] | +60% |
| tool calls before the first file write (heuristic) | 2 [2–3] | 5 [5–5] | +150% |
| cost (USD) | 0.21 [0.20–0.21] | 0.25 [0.22–0.26] | +18% |
| wall time (s) | 46 [41–48] | 48 [47–60] | +4% |
| runs where the agent opened the handoff itself (its text came back in a tool result) | 3/3 | 0/3 | |
| runs whose combo passed the grader | 3/3 | 3/3 | |
| runs whose test suite passed | 3/3 | 3/3 | |
| runs where baton injected the handoff | 0/3 | 3/3 | |
