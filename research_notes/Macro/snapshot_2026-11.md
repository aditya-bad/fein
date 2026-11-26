# Macro snapshot 2026-11 (generated 2026-11-26)

Stage 5 (valuation context). Every value has a date and a source; `second` = an independent cross-check.
`manual` = entered by hand from the cited page (no machine-readable public source). Research, not advice.

| Field | Value | Unit | As of | Source | Second source | Note |
|---|---|---|---|---|---|---|
| RBI policy repo rate | 5.5 | % | 2026-11-25 | [auto](https://www.rbi.org.in/) |  | RBI home page 'Current Rates' box; date is the page's rates date. Note: memdb insight:india-rates-rupee-regime-2025-26 had 5.25% (Jun-2026), so a hike to 5.50% happened in between (not dated here). |
| India 10-yr G-sec yield | 7.1641 | % | 2026-11-25 | [auto](https://www.rbi.org.in/) | 7.38 (2026-10-01, [src](https://fred.stlouisfed.org/series/INDIRLTLT01STM), OECD MEI via FRED, monthly average) | 6.94% GS 2036 (security nearest 10-yr maturity on RBI's list) |
| India CPI inflation (y/y) | 6.09 | % | 2026-10-31 | [manual](https://www.mospi.gov.in/uploads/latestreleasesfiles/1794480048335-Press%20Release%20of%20CPI%20for%20October%202026%20.pdf) | 6.09 (2026-11-12, [src](https://theprint.in/economy/indias-october-retail-inflation-breaches-rbis-6-ceiling-odds-of-december-repo-rate-hike-rise/3097181/)) | October 2026, provisional, CPI combined (2024 base); Sept 5.54%; food 8.94%; above RBI 6% upper band. Next release 14-Dec-2026. MoSPI API without login only serves the 2012 base (to Dec-2025). |
| USD/INR | 92.4895 | INR per USD | 2026-11-25 | [auto](https://www.rbi.org.in/) | 92.67 (2026-11-20, [src](https://fred.stlouisfed.org/series/DEXINUS), Fed H.10 noon NY); 92.24 (2026-11-25, [src](https://api.frankfurter.dev/v1/latest?base=USD&symbols=INR,EUR,JPY,GBP,CAD,SEK,CHF), ECB reference via Frankfurter) | FBIL reference rate |
| Brent crude | 91.8 | USD/bbl | 2026-11-24 | [auto](https://fred.stlouisfed.org/series/DCOILBRENTEU) |  | EIA Europe Brent spot via FRED |
| US dollar index (DXY) | 104.04 | index | 2026-11-25 | [auto](https://api.frankfurter.dev/v1/latest?base=USD&symbols=INR,EUR,JPY,GBP,CAD,SEK,CHF) | 123.5978 (2026-11-20, [src](https://fred.stlouisfed.org/series/DTWEXBGS), Fed broad trade-weighted dollar (Jan-2006=100): a different index, direction check only) | computed: ICE DXY formula on ECB reference rates (approximation, not ICE's print) |
| Gold (USD) | 3567.7 | USD/troy oz | 2026-11-26 | [auto](https://api.gold-api.com/price/XAU) |  | spot, gold-api.com |
| Gold (INR) | 106089 | INR per 10 g | 2026-11-26 | [auto](https://api.gold-api.com/price/XAU) | 122982.0 (2026-11-25, [src](https://ibjarates.com/), IBJA 999 AM rate: domestic, includes import duty, excludes GST) | computed: USD spot x USD/INR / 31.1035 x 10 (no duty) |
| Nifty 50 | 25819.25 | index | 2026-11-25 | [auto](https://archives.nseindia.com/content/indices/ind_close_all_25112026.csv) |  | NSE daily index file |
| Nifty 50 trailing P/E | 21.03 | x | 2026-11-25 | [auto](https://archives.nseindia.com/content/indices/ind_close_all_25112026.csv) |  | trailing P/E, consolidated earnings basis since 31-Mar-2021 |
| Nifty 50 P/B | 3.17 | x | 2026-11-25 | [auto](https://archives.nseindia.com/content/indices/ind_close_all_25112026.csv) |  |  |
| Nifty 50 dividend yield | 1.32 | % | 2026-11-25 | [auto](https://archives.nseindia.com/content/indices/ind_close_all_25112026.csv) |  |  |
| Nifty 50 earnings yield | 4.755 | % | 2026-11-25 | [auto](https://archives.nseindia.com/content/indices/ind_close_all_25112026.csv) |  | 100 / trailing P/E |
| Earnings yield minus 10-yr G-sec | -2.409 | pp | 2026-11-25 | [auto](https://archives.nseindia.com/content/indices/ind_close_all_25112026.csv) |  | earnings yield minus India 10-yr G-sec; see research_notes/Macro/ey_gsec_gap_test.md |
| US 10-yr Treasury | 4.85 | % | 2026-11-25 | [auto](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2026/all?type=daily_treasury_yield_curve&field_tdr_date_value=2026&page&_format=csv) | 4.91 (2026-11-24, [src](https://fred.stlouisfed.org/series/DGS10)) | US Treasury par yield curve |
| FPI net equity flows (month to date) | 84291 | INR crore (2-13 Nov, partial) | 2026-11-13 | [manual](https://www.multibagg.ai/market-pulse/articles/fpi-indian-equity-buying-november-cmwi79lp200op2rpblhzyy2c3) | 76189 (2026-11-13, [src](https://www.newsbytesapp.com/news/business/fpis-invest-over-76-000cr-in-indian-equities-in-november/story)) | UNVERIFIED and conflicting: another report says Rs 76,189 cr for 3-13 Nov. Direction (net buying after Sep -35,861 and Oct -34,843 cr outflows) agrees. NSDL not reachable by script. |

Gaps and caveats:
- DXY is computed from ECB reference rates with ICE's weights; it can differ from ICE's print by a few tenths.
- Gold INR (computed) excludes import duty; the IBJA domestic rate includes it. If the gap is far from the duty rate, treat both as unverified. **2026-11: the gap is ~16% (106,089 vs 122,982), well above a ~6% duty: unexplained, gold INR is single-source/unverified this month.**
- India 10-yr: RBI lists securities by maturity; the one nearest a 10-yr maturity is used. FRED is a monthly average.
- Nifty P/E is on consolidated earnings since 31-Mar-2021 (standalone before), so long histories have a break.
