# India dead-company data probe (Roadmap stage 1 -> unlocks the stage-2 solvency re-test)

Checked 22-Nov-2026 from the cloud session network (no login, no API key). Purpose: find free, machine-readable
lists of Indian listed companies that failed (insolvency, liquidation, compulsory delisting, suspension), so the
US solvency test (`research_notes/Backtests/solvency_flags_us.md`, decision:solvency-flags-graded, lesson L24) can be
re-run on India without survivorship bias. Fetcher: `tools/universe/dead_companies.py`. First snapshot:
`research_notes/Universe/india_dead_companies_2026-11-22.csv` (7,336 event rows).

## Verdict

Enough data exists for the outcome side of an Indian re-test. **IBBI's public-announcement export is the key
source**: every CIRP admission since January 2017 with the debtor's CIN, which marks listed companies. Exchange
lists give identifiers (ISIN, BSE code, NSE symbol) but few dates. Two gaps remain:
(1) an admission is not a death (see the caveats: Inox Wind and VA Tech Wabag both appear in 2017);
(2) point-in-time *financials* for the dead firms (screener keeps pages for many delisted companies; still to test).

## Sources

| # | Source | URL | Format | Loads here? | Rows (22-Nov-2026) | Fields | Mapping to symbol / ISIN |
|---|---|---|---|---|---|---|---|
| a1 | IBBI public announcements, CIRP (Form A) | `https://ibbi.gov.in/en/public-announcement?ann=Public+Announcement+of+Corporate+Insolvency+Resolution+Process&export_excel=export_excel` | ".xls" that is really tab-separated text (one request, ~2.9 MB) | yes (one connection reset; retry worked) | 9,263 announcements, 19-Jan-2017 to 05-Nov-2026; 673 with a listed CIN (starts with "L") | type, announcement date, last date for claims, debtor name, **CIN**, applicant (creditor), IRP name and address, remarks | CIN "L..." = listed when the CIN was issued. Name match to BSE/NSE lists: 553 of 751 kept rows got an ISIN, 172 an NSE symbol; 136 listed CINs unmatched (renamed companies such as Bhushan Steel -> Tata Steel BSL, Monnet Ispat -> JSW Ispat) |
| a2 | IBBI public announcements, liquidation | same, `ann=Public+Announcement+of+Liquidation+Process` | same | yes | 3,023 (221 with a listed CIN) | same | same: 185 of 236 kept rows got an ISIN |
| a3 | IBBI Form G (invitations for resolution plans) | `https://ibbi.gov.in/en/resolution-plans?export_excel=export_excel` | tab-separated | yes | ~199 pages | debtor, CIN, RP, EOI dates | CIN. Shows a CIRP is live, not its outcome; not used in the snapshot |
| b1 | NSE delisted list | `https://nsearchives.nseindia.com/content/equities/delisted.csv` | CSV | yes | 328 (Apr-2002 to Nov-2020 only) | symbol, name, delisting date, type (137 compulsory, 99 liquidation, 92 voluntary) | NSE symbol given; ISIN via name match to BSE (274 of 328) |
| b2 | NSE suspended list | `https://nsearchives.nseindia.com/content/equities/suspension.csv` | CSV | yes | 152 (Oct-1999 to Jul-2012 only) | symbol, name, suspension date | NSE symbol |
| b3 | NSE current equity list | `https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv` | CSV | yes | all active | symbol, name, listing date, ISIN | used for matching only |
| b4 | NSE delisting / suspension API | `www.nseindia.in/api/delisted-securities` and similar guesses | - | 404 | - | - | the NSE website's current delisting pages are not on a known open endpoint; not found |
| b5 | BSE list of scrips, status Delisted | `https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w?Group=&Scripcode=&industry=&segment=Equity&status=Delisted` | JSON (needs HTTP/2: `curl --http2`, as `collect.py` does) | yes | 4,624 | scrip code, scrip id, name, issuer name, **ISIN**, group, face value | ISIN + BSE code direct. **No delisting date or reason** |
| b6 | same, status Suspended | `...&status=Suspended` | JSON | yes | 1,238 | same, plus last market cap | ISIN + BSE code. No suspension date |
| b7 | same, status Active | `...&status=Active` | JSON | yes | 5,138 | same | used for matching only |
| c1 | IBBI mirror of NCLT orders | `https://ibbi.gov.in/en/orders/nclt?page=N` | HTML table, 20 per page, 1,614 pages (~32,000 orders) | yes | 100 fetched (5 pages) | order date, "In the matter of <company> [case no.]", PDF link, remark (Admission - Final order, Liquidation, Dissolution, Others...) | company name only (no CIN): name match; 7 of 100 orders were listed companies |
| c2 | NCLT's own site | `https://nclt.gov.in/order-judgement-date-wise` | HTML form | page loads, but **search needs a CAPTCHA** | - | - | not automatable (and we should not try to defeat a CAPTCHA) |

## How to use it for the re-test (proposal, not yet pre-registered)

- **Failure event (O_fail, India):** first of (i) IBBI CIRP admission of a listed-CIN company, (ii) IBBI liquidation
  order, (iii) NSE "Compulsory Delisting" or "Delisting - Liquidation", (iv) BSE delisted/suspended with no voluntary
  delisting or merger behind it. Date = IBBI announcement date (exact) or NSE delisting date; BSE-only events
  need a date from the last traded day (bhavcopy archives) - still to build.
- **Admission is not death.** Section 12A withdrawals, settlements with an operational creditor and orders set aside on
  appeal are common: Inox Wind (Jul-2017) and VA Tech Wabag (Sep-2017) appear as CIRP admissions on operational-creditor
  petitions and survived. Require, as in the US test, a price drawdown confirmation (for example >= 80% from the
  snapshot price within 5 years) or a liquidation / delisting event, and report admission-only cases separately.
- **Universe at each snapshot:** listed companies at T (BSE Active + Delisted + Suspended with ISIN, filtered by
  listing date) - this gets around the survivorship bias of today's NSE list. Financials at T must come from a
  filing made before T: screener keeps pages for many delisted firms (test next), else BSE XBRL results.
- **Name matching** is the weak link (renamed companies). Improve with BSE's former-name history or MCA CIN master
  data (MCA's site needs a CAPTCHA). CIN -> ISIN has no free bulk source that we found.

## Snapshot file

`india_dead_companies_2026-11-22.csv` columns: source, event, event_date, company, cin, nse_symbol, bse_code, isin,
match, remarks, url. Rows by source: bse_delisted 4,624; bse_suspended 1,238; ibbi_cirp 751; ibbi_liq 236;
nse_delisted 328; nse_suspended 152; ibbi_nclt 7. IBBI rows are kept only when the CIN is listed ("L") or the name
matches a listed company (`--all-ibbi` keeps all 12,386 fetched). `match` = name / name (ambiguous: field) /
listed_cin_unmatched / exchange. 52 IBBI rows map to symbols in today's 1,547-name live universe (mostly old,
resolved cases such as Alok Industries, Jyoti Structures, Orchid Pharma - companies that came back under new owners).

Caveats: name matches are exact after normalisation (fein_common.norm_name), unchecked by hand; "ambiguous" rows
need a look. Four IBBI liquidation rows carry a placeholder date (01-01-1970); the fetcher blanks dates before the IBC start (1-Dec-2016). NSE files are stale (2020, 2012) and are
history only. Research data, not SEBI-registered advice.
