# tools/gold — gold study + monthly monitor (defence layer, stage 5 context, stage 7 calls)

Stdlib + `curl`; public files only (no logins, keys, CAPTCHA or anti-bot workarounds).

```
python3 tools/gold/fetch.py --out research_notes/Gold/gold_study_YYYY-MM/data    # raw files + sources.json (as_of)
python3 tools/gold/study.py --data research_notes/Gold/gold_study_YYYY-MM/data --out research_notes/Gold/gold_study_YYYY-MM
```
`study.py` writes `results.json`: source cross-checks, ≥20%/≥15% drawdown episodes (USD and INR) with run-up, Fed regime and
real-yield context, Q3/Q4 broad stats, LBMA consensus vs random walk, today's state (GC=F, spot, INR, IBJA), pre-registered
analog scenarios (12m/24m), probabilities for the GOLD paper calls, and the L52 allocation tie. Method: 
`research_notes/Gold/gold_study_2026-11/prereg.md` — don't change it silently; new rules need a new prereg.

Monthly update: re-run both into a new dated folder; compare `today`, `scenarios` and `calls` with the prior month; resolve
due calls from Yahoo GC=F daily closes. Update the `LBMA` dict each January (new consensus) and the `old` call dict when
calls are added. Known: World Bank workbook stopped at 2024-12 (datahub mirror used after); FRED LBMA series discontinued.
