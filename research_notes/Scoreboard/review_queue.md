# Review queue (2026-11-22)

Calls a human must decide. For each, read the evidence, apply the WRITTEN rule strictly, then append one line to `research_notes/Scoreboard/review_decisions.jsonl`, e.g.

`{"id": "thesis:paper-call:X:y", "outcome": 1, "value": 24.3, "source": "https://...", "source_date": "2027-02-05", "note": "Q3 press release p2", "decided_by": "user"}`

Use `"outcome": "void"` only when the source no longer publishes the metric (scoring protocol). The next resolver run turns decisions into a memdb seed.

_Queue empty._
