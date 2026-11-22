# FEIN universe tools

| File | Job |
|---|---|
| `dead_companies.py` | One snapshot of Indian listed companies that failed or left the market: IBBI CIRP and liquidation public announcements (with CIN), IBBI's mirror of NCLT orders, NSE delisted/suspended archive CSVs, BSE delisted/suspended scrip lists (ISIN). IBBI rows are mapped to BSE code / ISIN / NSE symbol by normalised name. Output: `research_notes/Universe/india_dead_companies_<date>.csv`. |

Standard library plus system `curl`; BSE calls go through `tools/detectors/fein_common.py` (`curl --http2`).
About 12 requests plus one per NCLT page, at least 1.5 s apart.

```bash
python3 dead_companies.py                    # all sources, 5 pages of NCLT orders (~1 min)
python3 dead_companies.py --nclt-pages 0     # skip NCLT orders
python3 dead_companies.py --all-ibbi         # keep unlisted IBBI debtors too (12k+ rows)
```

What each source holds, what is missing (dates on BSE lists, CIRP outcomes, renamed companies) and how it feeds
the survivorship-free Indian solvency re-test: `research_notes/Universe/india_dead_companies_probe.md`.
Research data, not SEBI-registered advice.
