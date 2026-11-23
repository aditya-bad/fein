# fein

Long-term investing research partnership with Claude.

- **Start here (human):** [MY_MEMORY.md](MY_MEMORY.md)
- **Claude instructions:** [CLAUDE.md](CLAUDE.md) → [memory/](memory/00_index.md)
- Reports: [reports/](reports/) · Sourced notes: [research_notes/](research_notes/)
- Indian annual reports (added 23-Nov-2026): `python3 tools/nse_fetch.py annual_reports SYMBOL [--download DIR]`
  lists one row per FY with the PDF/ZIP URL (4–85 MB) and `submitted` (broadcast time, else the stamp in the file
  name). Section parser (MD&A, auditor's report + CARO, BRSR excluded): `tools/backtests/india_ar_text/sections.py`;
  auditor-diff flags: `flags.py`. Pilot write-up: `research_notes/Backtests/india_annual_report_text.md`.
