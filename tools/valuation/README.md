# tools/valuation: the standard valuation worksheet (roadmap stage 5)

`worksheet.py` turns one small input file of company figures into one Markdown section with the same five
blocks for every company, so deep dives produce comparable valuation outputs. It uses only the standard
library and runs on a Raspberry Pi (Python 3.7+).

Guide, worked examples, design choices and known limits: `research_notes/Templates/valuation_and_decision.md`.

## Run
```bash
python3 tools/valuation/worksheet.py --template > my_company.json     # blank input
python3 tools/valuation/worksheet.py my_company.json                  # Markdown to stdout
python3 tools/valuation/worksheet.py my_company.json -o section.md --json results.json
```
The input is JSON. Lines that start with `#` or `//` are comments. `--json` dumps every computed number, and
`tools/decision/decision_card.py` uses it as stage-5 input.

## What it outputs
| Block | What it answers |
|---|---|
| Snapshot | Market cap, EV, P/E, EV/EBITDA, P/FCF, FCF yield, NOPAT margin |
| (a) Reverse DCF | The revenue CAGR the price implies (margin flat, or moving to the base-case margin); the year-1 growth that fades to terminal; the margin needed on the base-case growth path; the IRR the price offers if the base case happens; a Gordon check on trailing FCF; the implied path year by year; and a **feasibility flag** when the path needs reinvestment above 100% of NOPAT |
| (b) Scenario DCF | Bear/base/bull (+ blow-up) DCF values, a probability-weighted value, the bear downside, P(value < price); 5-year multiples from each scenario's exit P/E next to the **DCF-consistent P/E at year 5**, and an exit-multiple gap warning; P(≥2x/3x/5x), P(≤0.5x), P(blow-up), the EV of the 5-year multiple, the median and the hurdle |
| (c) Twin engine | EPS CAGR needed for 2x/3x/5x in N years at each exit P/E, and the share of the return that has to come from re-rating |
| (d) Temperature | P/E against the stock's own history (needs n ≥ 5), the sector median and the market (Nifty bands from `insight:india-valuation-forward-returns`) |
| (e) Sensitivity | Cost of equity × growth shift, and terminal growth × end margin |

## Model (one line each)
- `g_t` fades linearly from `growth` (year 1) to `growth_end` (year N). The NOPAT margin moves linearly from today's to `margin_end`.
- `FCF = NOPAT × (1 − g / ROIIC)`: growth has to be paid for (value-driver formula; `insight:flag-high-pe-context`).
- `TV = NOPAT_N × (1+tg) × (1 − tg/ROIC_T) / (r − tg)`. Equity = PV + recurring non-operating income perpetuity + non-operating assets − net debt.
- `EPS_t` scales with operating NOPAT + recurring other income. Treasury income on net cash is held flat.
- 5-year multiple = (EPS₅ × exit P/E + distributed FCF per share) ÷ price. Set `"exit_pe": "dcf"` to use the DCF-consistent multiple instead.
- 5-year probabilities: each scenario gets a lognormal spread (σ = `dispersion`, default 0.30) and the blow-up is a point mass.

## Defaults
| | India | US |
|---|---|---|
| Cost of equity | 12.5% (range 12–13%) | 9.5% (range 9–10%) |
| Terminal growth | 5.0% | 3.0% |
| Hurdle (index CAGR) | 12% | 8% |

## Input rules that matter
- `shares` must use the same scale as the money units: ₹ cr goes with shares in crore, $M with shares in millions.
- `net_debt` is negative for net cash. Leave out lease liabilities when rent sits inside the margin you use (Indian pre-Ind AS 116 EBITDA; US retailers with occupancy in COGS).
- Use the **economic** margin: pre-Ind AS 116 for Indian retailers, core (ex other income) for cash-rich companies, and after SBC.
- Every input needs a source tag or an `[EST]` with its method in `notes` (stock-research-analyst rule).
- **Holdco-like stocks (v1.2, 2026-11-23):** put a listed stake (post-tax, after any discount you assume) in `non_operating_value` and set `non_operating_growth` (or per-scenario `nonop_growth`). The 5-year multiple then adds the stake at year 5 to EPS₅ × exit P/E, and the DCF-consistent P/E leaves the stake out. Without the key, behaviour is unchanged. Example: `live/SUNFLAG.json` (plus the steel-only stub `live/SUNFLAG_stub.json`).

## Bank / NBFC mode (v1.1, 2026-11-22)
Lenders are valued on book and ROE, not revenue/EBIT/FCF. Put `"mode": "bank"` in the input
(`worksheet.py --template --mode bank` prints the template); `bank.py` does the work and returns the same result
keys, so `decision_card.py` reads it unchanged.
- Book is **fully diluted** first (`dilution`: warrant/QIP shares and the cash still to come; `book_adjustments`:
  money already in reserves, e.g. warrant subscriptions).
- (a) ROE needed forever `g + P/B × (CoE − g)`; ROE needed for N years then only CoE; **implied CoE at today's ROE**
  `g + (ROE − g) ÷ P/B`; justified P/B on the base case; base-case IRR.
- (b) Residual-income scenarios: ROE fades linearly `roe_start → roe_end`; `B_t = B_(t-1)(1 + ROE_t(1 − payout))`;
  `TV = (ROE_T − CoE)·B_N ÷ (CoE − g)`; 5-yr multiple = (BVPS₅ × exit P/B + dividends) ÷ price, next to the
  RIM-consistent P/B at year 5 (`"exit_pb": "rim"` uses it).
- (c) twin engine on book; (d) P/B vs own history (`pb_history`, n ≥ 5) and peers (`sector_pbs`); (e) book stress
  (+1/2/3/5% loan loss as % of book, leverage); (f) CoE × long-run ROE grid and justified P/B.
- Example: `examples/FEDERALBNK.json` (dry run, TEST MATERIAL).

## Examples (TEST MATERIAL, no verdict)
`examples/VMM.json`, `examples/CUMMINSIND.json` and `examples/FIVE.json` take their figures from the three practice deep dives. Their outputs are `examples/*_worksheet.md` and `*_worksheet.json`. `examples/SYNTHETIC.json` is a **fictional** company that only exists to test the code path where every gate clears.
