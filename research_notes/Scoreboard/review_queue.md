# Review queue (2026-11-28)

Calls a human must decide. For each, read the evidence, apply the WRITTEN rule strictly, then append one line to `research_notes/Scoreboard/review_decisions.jsonl`, e.g.

`{"id": "thesis:paper-call:X:y", "outcome": 1, "value": 24.3, "source": "https://...", "source_date": "2027-02-05", "note": "Q3 press release p2", "decided_by": "user"}`

Use `"outcome": "void"` only when the source no longer publishes the metric (scoring protocol). The next resolver run turns decisions into a memdb seed.

## `thesis:paper-call:VIYASH:card-2026-11-26-5y-blowup`
- **Type** ? / no spec · P(ours) 0.07 · P(base) 0.1537 · resolve by 2031-11-25
- **Rule:** YES if between 2026-11-25 and 2031-11-25: Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).
- **Why here:** NO SPEC: add one to tools/scoreboard/specs.json (type c)

## `thesis:paper-call:VIYASH:card-2026-11-26-5y-ge3x`
- **Type** ? / no spec · P(ours) 0.0204 · P(base) 0.2129 · resolve by 2031-11-25
- **Rule:** YES if the total-return multiple (adjusted close incl. dividends reinvested, splits/bonuses adjusted) from 2026-11-25 (entry INR 228.88) to the last close on or before 2031-11-25 is ≥ 3.0.
- **Why here:** NO SPEC: add one to tools/scoreboard/specs.json (type a)

## `thesis:paper-call:VIYASH:card-2026-11-26-5y-le0p5x`
- **Type** ? / no spec · P(ours) 0.2678 · P(base) 0.1127 · resolve by 2031-11-25
- **Rule:** YES if the total-return multiple from 2026-11-25 (entry INR 228.88) to the last close on or before 2031-11-25 is ≤ 0.5, or the stock is delisted/suspended below that level.
- **Why here:** NO SPEC: add one to tools/scoreboard/specs.json (type a)

