# tools/macro — monthly macro snapshot (stage 5: valuation context)

**What it builds:** a dated, sourced macro context sheet for India + US, used as the market-level backdrop for
valuation (stage 5) and the decision card (stage 6). **Unlocks:** a running monthly history of the same fields,
and the pre-registered test of whether the Nifty earnings-yield minus G-sec gap means anything
(`research_notes/Macro/ey_gsec_gap_test.md`).

Standard library + `curl`. Public pages/files only — no logins, no API keys, no CAPTCHA or anti-bot workarounds.

```
python3 tools/macro/snapshot.py                         # current month -> research_notes/Macro/snapshot_YYYY-MM.md/.json
python3 tools/macro/snapshot.py --month 2026-11 --memdb # + memdb metrics (ticker MACRO, period YYYY-MM)
python3 tools/macro/snapshot.py --out-dir "$FEIN_DATA/macro"   # what the Pi job does
python3 tools/macro/snapshot.py --selftest              # offline parser checks
python3 tools/macro/ey_gap_test.py [--cache DIR]        # the pre-registered EY-gap test (~180 NSE files, cached)
python3 tools/macro/ey_gap_test.py --selftest           # offline OLS / Newey-West checks
```

## Sources (tested 2026-11-26)
| Field | Primary | Second source |
|---|---|---|
| RBI repo rate | rbi.org.in home "Current Rates" box | — (FRED IRSTCB01INM156N stops 2023) |
| India 10-yr G-sec | rbi.org.in home, GS security nearest a 10-yr maturity | FRED INDIRLTLT01STM (OECD, monthly avg) |
| CPI y/y | **manual** (`manual.json`, MoSPI press release) — MoSPI's no-login API serves only the 2012 base (to Dec-2025) | news report |
| USD/INR | FBIL reference via RBI home | FRED DEXINUS; ECB via api.frankfurter.dev |
| Brent | FRED DCOILBRENTEU | — |
| DXY | computed with ICE weights from ECB reference rates (approximation) | FRED DTWEXBGS (broad dollar; direction only) |
| Gold USD | api.gold-api.com spot | — |
| Gold INR | computed (USD spot × USD/INR, per 10 g, no duty) | IBJA 999 AM (ibjarates.com, includes duty) |
| Nifty 50 close, P/E, P/B, DY | archives.nseindia.com `ind_close_all_DDMMYYYY.csv` (exists from 29-Feb-2012) | — |
| EY − G-sec | derived: 100/PE − 10-yr | — |
| US 10-yr | home.treasury.gov daily par curve CSV | FRED DGS10 |
| FPI flows | **manual** — fpi.nsdl.co.in gives an empty reply to scripted requests | second news report |

A failed source is written as `missing` with a note, never guessed. `manual.json` is keyed by month; a manual
entry is used only when the automatic fetch gives nothing, and is marked `manual` in the output.

## Known limits
- Nifty P/E switched from standalone to consolidated earnings on 31-Mar-2021: long P/E histories have a break.
- NSE archive P/E history starts Feb-2012; niftyindices.com's older P/E history is a browser-only endpoint we do
  not script. For 1999–2011 a manual CSV export would be needed.
- Gold INR computed vs IBJA differ by duty and any local premium; on 2026-11-26 the gap was ~16%, unexplained.

## Pi
Monthly job `macro` in `deploy/pi/jobs.sh` (2nd of each month, 08:15 IST) writes to `$FEIN_DATA/macro/`. It does
not touch memdb or the repo; copy a snapshot into `research_notes/Macro/` and run `--memdb` from a session.
