#!/usr/bin/env python3
"""FEIN valuation worksheet (roadmap stage 5).

Standard library only (runs on a Raspberry Pi, Python >= 3.7). One input file of company
figures -> one Markdown section with the same five blocks for every company:

  (a) reverse DCF: the growth and margin path implied by today's price
  (b) scenario DCF: bear/base/bull (+ optional blow-up) with probabilities ->
      probability-weighted value, downside, and a 5-year outcome distribution
  (c) twin-engine table: EPS CAGR needed x exit P/E for 2x/3x/5x in N years
  (d) valuation temperature: P/E vs the stock's own history, sector median and market
  (e) sensitivity tables (cost of equity x growth; terminal growth x margin)

Model (deliberately simple and transparent, so every number can be re-derived by hand):
  revenue_t = revenue_{t-1} * (1 + g_t)       g_t fades linearly from g_start (yr 1) to g_end (yr N)
  margin_t  = m0 + (m_end - m0) * t / N       NOPAT margin (after tax, after SBC)
  NOPAT_t   = revenue_t * margin_t
  FCF_t     = NOPAT_t * (1 - g_t / ROIIC)     value-driver formula: growth must be paid for
  TV_N      = NOPAT_N * (1 + tg) * (1 - tg / ROIC_terminal) / (r - tg)
  equity    = PV(FCF) + PV(TV) + PV(recurring non-operating income) + non-operating assets - net debt
  EPS_t     = EPS_0 * (NOPAT_t + OI_t) / (NOPAT_0 + OI_0)
  5-yr multiple = (EPS_5 * exit P/E + cumulative distributed FCF per share) / price
  v1.3 optional: cash tax (FCF_t += NOPAT_t * (t_book - t_cash,t) / (1 - t_book); EPS stays on book tax),
  a reinvestment-realism check (ROIIC used / implied by price vs the last-5y incremental ROIC), and an
  exit-multiple bet table (exit P/E used vs DCF-consistent P/E vs own median; 5-yr EV under each).

Usage:
  python3 worksheet.py input.json                 # Markdown to stdout
  python3 worksheet.py input.json -o section.md   # write the Markdown section
  python3 worksheet.py input.json --json out.json # also dump machine-readable results
  python3 worksheet.py --template > new.json      # blank input template

Input is JSON; lines starting with '#' or '//' are treated as comments and ignored.
Research tooling, not SEBI-registered advice. Outputs are only as good as the inputs.
"""
import argparse
import datetime as _dt
import json
import math
import os
import sys

VERSION = "1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode)"

MARKET_DEFAULTS = {
    # cost of equity, terminal growth, hurdle CAGR (what an index fund is assumed to earn)
    "india": {"coe": 0.125, "tg": 0.05, "hurdle": 0.12, "coe_range": "12-13%"},
    "us": {"coe": 0.095, "tg": 0.03, "hurdle": 0.08, "coe_range": "9-10%"},
}

# Temperature bands on P/E / own-median P/E. The >=2x band carries lesson L12 / insight:flag-high-pe-context:
# buying at ~2x a stock's own median P/E was followed by 4-6 flat years even with EPS growth.
TEMP_BANDS = [
    (0.70, "COLD"), (0.90, "COOL"), (1.10, "NORMAL"), (1.50, "WARM"), (2.00, "HOT"), (float("inf"), "VERY HOT"),
]
MIN_HISTORY_POINTS = 5

# insight:india-valuation-forward-returns (Nifty trailing P/E -> subsequent 5-yr returns)
NIFTY_BANDS = [
    (12.0, "cheap market: from P/E < 12 the Nifty's 5-yr return averaged ~29%/yr (Stable Investor, data to 2015)"),
    (18.0, "below-average market P/E"),
    (22.0, "around the long-run average"),
    (24.5, "expensive: from 22-25x, 3-5 yr returns were poor (MoneyWorks4Me)"),
    (float("inf"), "very expensive: every negative 5-yr Nifty return started at P/E >= 24.5 (Freefincal); "
                   "from P/E > 24 the 5-yr return averaged ~2.7%/yr (Stable Investor)"),
]

TEMPLATE = {
    "company": "Company name", "ticker": "TICKER", "market": "india",
    "practice": True, "currency": "INR", "units": "INR cr",
    "as_of": "2026-11-21", "price": 100.0,
    "shares": 10.0,
    "# shares": "in the same scale as the money units (INR cr money -> shares in crore; USD M -> shares in millions)",
    "net_debt": 0.0,
    "# net_debt": "negative = net cash. Exclude lease liabilities if rent is inside the margin you use",
    "non_operating_value": 0.0,
    "other_income_recurring_post_tax": 0.0,
    "treasury_income_post_tax": 0.0,
    "# treasury_income_post_tax": "interest on the net cash already in net_debt; held flat in the EPS path",
    "base": {"fy": "FY26", "revenue": 1000.0, "ebitda": 150.0, "ebit": 120.0, "pat": 90.0, "fcf": 60.0,
             "eps": None, "eps_normalised": None, "eps_forward": None, "pe_trailing": None, "sbc": 0.0},
    "tax_rate": 0.25,
    "# cash_tax_rate": "v1.3 optional: cash tax rate when it differs from book tax (accelerated/bonus depreciation). "
                       "Or give deferred_tax_share (deferred tax / total tax expense). cash_tax_rate_end = rate in "
                       "year N and the terminal value (default: same as cash_tax_rate)",
    "nopat_margin": None,
    "# nopat_margin": "if null: (ebit - sbc_if_not_expensed) * (1 - tax) / revenue",
    "roiic": 0.25, "terminal_roic": None,
    "# incremental_roic_5y": "v1.3 optional: company's last-5y incremental ROIC (dNOPAT / dInvested capital), or give "
                             "roic_history [{fy, nopat, invested_capital}] and the worksheet derives it; >5 pts gap "
                             "to the ROIIC used or implied is flagged",
    "years": 10, "coe": None, "terminal_growth": None, "hurdle_cagr": None,
    "payout_of_fcf": 0.0,
    "dispersion": 0.30,
    "base_case": {"growth": 0.15, "growth_end": 0.08, "margin_end": 0.12, "roiic": None, "exit_pe": 30},
    "scenarios": [
        {"name": "bear", "prob": 0.30, "growth": 0.08, "growth_end": 0.05, "margin_end": 0.10, "exit_pe": 20},
        {"name": "base", "prob": 0.50, "growth": 0.15, "growth_end": 0.08, "margin_end": 0.12, "exit_pe": 30},
        {"name": "bull", "prob": 0.18, "growth": 0.22, "growth_end": 0.10, "margin_end": 0.14, "exit_pe": 40},
    ],
    "blowup": {"prob": 0.02, "multiple": 0.10, "note": "what would have to happen"},
    "twin_engine": {"targets": [2, 3, 5], "horizon": 5, "exit_pes": None, "hist_eps_cagr": None,
                    "hist_eps_note": ""},
    "pe_history": [{"date": "FY22", "pe": 30.0}],
    "sector_pes": {"Peer A": 25.0},
    "market_pe": {"index": "Nifty 50", "pe": 20.6, "as_of": "2026-11"},
    "notes": ["source tags and [EST] methods for every input go here"],
    "sources": [],
}


# ----------------------------------------------------------------------------- input

def _bank():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import bank  # noqa: E402  (v1.1: bank/NBFC mode, P/B-ROE + residual income)
    return bank


def load_input(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.lstrip().startswith(("#", "//"))]
    d = json.loads("".join(lines))
    if str(d.get("mode", "")).lower() in ("bank", "nbfc", "lender"):
        return _bank().normalise(d, MARKET_DEFAULTS)
    return normalise(d)


def _num(x, name):
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        raise ValueError("field %s must be a number, got %r" % (name, x))


def normalise(d):
    """Fill defaults, derive missing fields, validate. Returns a new dict and a list of warnings."""
    d = json.loads(json.dumps(d))  # deep copy
    warn = d.setdefault("_warnings", [])
    mkt = str(d.get("market", "india")).lower()
    if mkt not in MARKET_DEFAULTS:
        raise ValueError("market must be 'india' or 'us'")
    d["market"] = mkt
    md = MARKET_DEFAULTS[mkt]
    for k in ("price", "shares"):
        if d.get(k) in (None, 0):
            raise ValueError("%s is required and must be non-zero" % k)
        d[k] = _num(d[k], k)
    d["net_debt"] = _num(d.get("net_debt", 0.0), "net_debt") or 0.0
    d["non_operating_value"] = _num(d.get("non_operating_value", 0.0), "non_operating_value") or 0.0
    # v1.2 (2026-11-23, live deep dive #1, a holdco-like stock): optional growth of the non-operating value to year 5.
    # When set (a number, e.g. 0.12 = the stake compounds at 12%/yr), the 5-year multiple adds non_operating_value x
    # (1+g)^5 per share on top of EPS5 x exit P/E (which values the operating business only). None = old behaviour
    # (non-operating value ignored in the 5-year multiple; still counted in the DCF value). Scenario key: nonop_growth.
    d["non_operating_growth"] = _num(d.get("non_operating_growth"), "non_operating_growth")
    d["other_income_recurring_post_tax"] = _num(d.get("other_income_recurring_post_tax", 0.0), "oi") or 0.0
    # interest on the net cash already counted in net_debt: held flat in the EPS path (not grown, not valued twice)
    d["treasury_income_post_tax"] = _num(d.get("treasury_income_post_tax", 0.0), "treasury") or 0.0
    b = d.get("base") or {}
    for k in ("revenue", "ebitda", "ebit", "pat", "fcf", "eps", "eps_normalised", "eps_forward", "pe_trailing", "sbc"):
        b[k] = _num(b.get(k), "base." + k)
    if not b.get("revenue"):
        raise ValueError("base.revenue is required")
    d["base"] = b
    d["tax_rate"] = _num(d.get("tax_rate", 0.25), "tax_rate")
    d["coe"] = _num(d.get("coe"), "coe") or md["coe"]
    d["terminal_growth"] = _num(d.get("terminal_growth"), "terminal_growth")
    if d["terminal_growth"] is None:
        d["terminal_growth"] = md["tg"]
    d["hurdle_cagr"] = _num(d.get("hurdle_cagr"), "hurdle_cagr") or md["hurdle"]
    if d["terminal_growth"] >= d["coe"] - 0.01:
        raise ValueError("terminal_growth must be at least 1 pp below the cost of equity")
    d["years"] = int(d.get("years", 10))
    if d["years"] < 5:
        raise ValueError("years must be >= 5 (the 5-year outcome is read from the projection)")
    _cash_tax(d)
    _roic_history(d)
    d["roiic"] = _num(d.get("roiic", 0.25), "roiic")
    d["terminal_roic"] = _num(d.get("terminal_roic"), "terminal_roic") or d["roiic"]
    d["payout_of_fcf"] = _num(d.get("payout_of_fcf", 0.0), "payout_of_fcf") or 0.0
    d["dispersion"] = _num(d.get("dispersion", 0.30), "dispersion")
    # NOPAT margin
    if d.get("nopat_margin") is None:
        if b.get("ebit") is None:
            if b.get("ebitda") is None:
                raise ValueError("give nopat_margin, base.ebit or base.ebitda")
            raise ValueError("base.ebit missing: give ebit (EBITDA - D&A) or nopat_margin")
        d["nopat_margin"] = b["ebit"] * (1 - d["tax_rate"]) / b["revenue"]
        d["_nopat_margin_method"] = "base.ebit x (1 - tax) / revenue"
    else:
        d["nopat_margin"] = _num(d["nopat_margin"], "nopat_margin")
        d["_nopat_margin_method"] = "given"
    # EPS
    if b.get("eps") is None:
        if b.get("pat") is None:
            raise ValueError("give base.eps or base.pat")
        b["eps"] = b["pat"] / d["shares"]
        d["_eps_method"] = "base.pat / shares"
    else:
        d["_eps_method"] = "given"
    if b["eps"] <= 0:
        warn.append("EPS <= 0: P/E and twin-engine blocks are not meaningful; use eps_normalised")
    # base case & scenarios
    bc = d.get("base_case")
    scen = d.get("scenarios") or []
    if not bc:
        named = [s for s in scen if str(s.get("name", "")).lower() == "base"]
        if not named:
            raise ValueError("give base_case or a scenario named 'base'")
        bc = dict(named[0])
    d["base_case"] = _fill_case(bc, d)
    d["scenarios"] = [_fill_case(s, d) for s in scen]
    bl = d.get("blowup") or {"prob": 0.0, "multiple": 0.1}
    bl["prob"] = _num(bl.get("prob", 0.0), "blowup.prob") or 0.0
    bl["multiple"] = _num(bl.get("multiple", 0.1), "blowup.multiple")
    d["blowup"] = bl
    if d["scenarios"]:
        tot = sum(s["prob"] for s in d["scenarios"]) + bl["prob"]
        if abs(tot - 1.0) > 0.005:
            warn.append("scenario + blow-up probabilities summed to %.3f; rescaled to 1.0" % tot)
            for s in d["scenarios"]:
                s["prob"] /= tot
            bl["prob"] /= tot
    te = d.get("twin_engine") or {}
    te.setdefault("targets", [2, 3, 5])
    te.setdefault("horizon", 5)
    d["twin_engine"] = te
    return d


def _cash_tax(d):
    """v1.3 (Kirby lesson, L34): cash tax below book tax (bonus depreciation, deferred tax). None = old behaviour."""
    ct = _num(d.get("cash_tax_rate"), "cash_tax_rate")
    share = _num(d.get("deferred_tax_share"), "deferred_tax_share")
    if ct is None and share is not None:
        ct = d["tax_rate"] * (1 - share)
        d["_cash_tax_method"] = "tax_rate x (1 - deferred_tax_share %.2f)" % share
    elif ct is not None:
        d["_cash_tax_method"] = "given"
    d["cash_tax_rate"] = ct
    if ct is None:
        d["cash_tax_rate_end"] = None
        return
    if not (-0.5 < ct < 0.9) or d["tax_rate"] >= 0.99:
        raise ValueError("cash_tax_rate must be a fraction and tax_rate < 1")
    ce = _num(d.get("cash_tax_rate_end"), "cash_tax_rate_end")
    d["cash_tax_rate_end"] = ct if ce is None else ce


def _roic_history(d):
    """v1.3: last-5y incremental ROIC, given or derived from roic_history (first vs last of the last 6 points)."""
    h = _num(d.get("incremental_roic_5y"), "incremental_roic_5y")
    d["_inc_roic_method"] = "given" if h is not None else None
    hist = d.get("roic_history") or []
    if h is None and len(hist) >= 2:
        pts = [p for p in hist if p.get("nopat") is not None and p.get("invested_capital") is not None][-6:]
        if len(pts) >= 2:
            dn = float(pts[-1]["nopat"]) - float(pts[0]["nopat"])
            dic = float(pts[-1]["invested_capital"]) - float(pts[0]["invested_capital"])
            if dic > 0:
                h = dn / dic
                d["_inc_roic_method"] = "dNOPAT / dIC, %s -> %s (roic_history)" % (pts[0].get("fy"), pts[-1].get("fy"))
            else:
                d["_warnings"].append("roic_history: invested capital did not grow over the window, so incremental "
                                      "ROIC is undefined (no realism check)")
    d["incremental_roic_5y"] = h


def _fill_case(c, d):
    c = dict(c)
    c["name"] = str(c.get("name", "base"))
    c["growth"] = _num(c.get("growth"), "growth")
    if c["growth"] is None:
        raise ValueError("case %s needs 'growth'" % c["name"])
    ge = _num(c.get("growth_end"), "growth_end")
    c["growth_end"] = c["growth"] if ge is None else ge
    me = _num(c.get("margin_end"), "margin_end")
    c["margin_end"] = d["nopat_margin"] if me is None else me
    c["roiic"] = _num(c.get("roiic"), "roiic") or d["roiic"]
    if c.get("nonop_growth") is not None:
        c["nonop_growth"] = _num(c.get("nonop_growth"), "nonop_growth")
    else:
        c.pop("nonop_growth", None)
    if isinstance(c.get("exit_pe"), str) and c["exit_pe"].lower() == "dcf":
        c["exit_pe"] = "dcf"
    else:
        c["exit_pe"] = _num(c.get("exit_pe"), "exit_pe")
    c["prob"] = _num(c.get("prob", 0.0), "prob") or 0.0
    return c


# ----------------------------------------------------------------------------- model

def project(d, g_start, g_end, m_end, roiic=None, coe=None, tg=None, years=None):
    """Run the DCF. Returns dict(rows, value_ps, ev, pv_fcf, pv_tv, ...)."""
    roiic = roiic or d["roiic"]
    r = coe if coe is not None else d["coe"]
    tg = d["terminal_growth"] if tg is None else tg
    n = years or d["years"]
    troic = d["terminal_roic"]
    rev0 = d["base"]["revenue"]
    m0 = d["nopat_margin"]
    oi0 = d["other_income_recurring_post_tax"]
    nopat0 = rev0 * m0
    tb = d["tax_rate"]
    ct0 = d.get("cash_tax_rate")
    ct_end = d.get("cash_tax_rate_end")
    rows = []
    rev = rev0
    pv = 0.0
    cum_dist = 0.0
    for t in range(1, n + 1):
        g = g_start + (g_end - g_start) * (t - 1) / (n - 1) if n > 1 else g_start
        rev = rev * (1 + g)
        m = m0 + (m_end - m0) * t / n
        nopat = rev * m
        reinv_rate = g / roiic if roiic else 0.0
        fcf = nopat * (1 - reinv_rate)
        tax_shield = 0.0
        if ct0 is not None:   # v1.3: deferred (cash < book) tax adds to FCF; NOPAT/EPS stay on book tax
            ct = ct0 + (ct_end - ct0) * (t - 1) / (n - 1) if n > 1 else ct0
            tax_shield = nopat * (tb - ct) / (1 - tb)
            fcf += tax_shield
        oi = oi0 * (1 + tg) ** t
        disc = (1 + r) ** t
        pv += fcf / disc
        eps = None
        denom = nopat0 + oi0
        tre_ps = d["treasury_income_post_tax"] / d["shares"]
        if denom > 0:
            eps = (d["base"]["eps"] - tre_ps) * (nopat + oi) / denom + tre_ps
        if t <= 5:
            cum_dist += max(fcf, 0.0) * d["payout_of_fcf"]
        row = {"t": t, "g": g, "revenue": rev, "margin": m, "nopat": nopat, "reinv_rate": reinv_rate,
               "fcf": fcf, "eps": eps}
        if ct0 is not None:
            row["tax_shield"] = tax_shield
        rows.append(row)
    nopat_n1 = rows[-1]["nopat"] * (1 + tg)
    if ct0 is None:
        tv = nopat_n1 * (1 - tg / troic) / (r - tg)
    else:
        tv = nopat_n1 * ((1 - tg / troic) + (tb - ct_end) / (1 - tb)) / (r - tg)
    pv_tv = tv / (1 + r) ** n
    pv_oi = oi0 * (1 + tg) / (r - tg) if oi0 else 0.0
    ev = pv + pv_tv
    equity = ev + pv_oi + d["non_operating_value"] - d["net_debt"]
    # DCF-consistent value at the end of year 5 (what a buyer then would pay on the same assumptions):
    # PV@5 of FCF 6..N + PV@5 of TV + recurring OI perpetuity + non-op assets - net debt + FCF retained in yrs 1-5
    pv5 = sum(rows[t - 1]["fcf"] / (1 + r) ** (t - 5) for t in range(6, n + 1))
    pv5 += tv / (1 + r) ** (n - 5)
    oi5 = oi0 * (1 + tg) ** 5
    pv5 += oi5 * (1 + tg) / (r - tg) if oi0 else 0.0
    retained = sum(max(rows[t - 1]["fcf"], 0.0) * (1 - d["payout_of_fcf"]) + min(rows[t - 1]["fcf"], 0.0)
                   for t in range(1, 6))
    eq5 = pv5 + d["non_operating_value"] - d["net_debt"] + retained
    eps5 = rows[4]["eps"]
    # v1.2: when non_operating_growth is set, EPS covers the operating business only, so the DCF-consistent P/E
    # must leave the non-operating value out (it is added separately to the 5-year multiple).
    eq5_op = eq5 - d["non_operating_value"] if d.get("non_operating_growth") is not None else eq5
    dcf_pe5 = (eq5_op / d["shares"]) / eps5 if eps5 and eps5 > 0 else None
    return {"rows": rows, "pv_fcf": pv, "pv_tv": pv_tv, "tv_share": pv_tv / ev if ev else None, "pv_oi": pv_oi,
            "ev": ev, "equity": equity, "value_ps": equity / d["shares"], "cum_dist_ps_5y": cum_dist / d["shares"],
            "value5_ps": eq5 / d["shares"], "dcf_pe5": dcf_pe5,
            "max_reinv_rate": max(x["reinv_rate"] for x in rows)}


RANGES = {"g": (-0.30, 0.80), "g_fade": (-0.30, 1.20), "m": (-0.05, 0.60), "r": (None, 0.40)}


def _na(x, rng, fmt=None):
    """Format a solved value, or say the price is outside what the tested range can produce."""
    if x is not None:
        return "**%s**" % (fmt or pct)(x)
    return "none in tested range %s to %s (the price is outside what this path can produce)" % (
        pct(rng[0], 0) if rng[0] is not None else "TG+1pp", pct(rng[1], 0))


def _solve(f, lo, hi, target, steps=200, tol=1e-7):
    """Find x in [lo, hi] with f(x) = target. Scans a grid for a sign change, then bisects.
    Returns None if no crossing exists in the range."""
    xs = [lo + (hi - lo) * i / steps for i in range(steps + 1)]
    prev_x, prev_v = xs[0], f(xs[0]) - target
    for x in xs[1:]:
        v = f(x) - target
        if prev_v == 0:
            return prev_x
        if (prev_v < 0) != (v < 0):
            a, b, fa = prev_x, x, prev_v
            for _ in range(100):
                mid = (a + b) / 2
                fm = f(mid) - target
                if abs(fm) < tol or (b - a) < tol:
                    return mid
                if (fa < 0) != (fm < 0):
                    b = mid
                else:
                    a, fa = mid, fm
            return (a + b) / 2
        prev_x, prev_v = x, v
    return None


def reverse_dcf(d):
    price = d["price"]
    bc = d["base_case"]
    m0 = d["nopat_margin"]
    out = {}
    # 1. constant growth for N years, margin flat at today's
    out["g_flat_margin"] = _solve(lambda g: project(d, g, g, m0)["value_ps"], RANGES["g"][0], RANGES["g"][1], price)
    # 2. constant growth, margin moves to the base-case end margin
    out["g_base_margin"] = _solve(lambda g: project(d, g, g, bc["margin_end"])["value_ps"],
                                  RANGES["g"][0], RANGES["g"][1], price)
    # 3. growth fading linearly to terminal growth by year N, margin to base-case end margin
    tg = d["terminal_growth"]
    out["g_fade_start"] = _solve(lambda g: project(d, g, tg, bc["margin_end"])["value_ps"],
                                 RANGES["g_fade"][0], RANGES["g_fade"][1], price)
    # 4. base-case growth path, solve the end margin
    out["m_needed_base_growth"] = _solve(lambda m: project(d, bc["growth"], bc["growth_end"], m)["value_ps"],
                                         RANGES["m"][0], RANGES["m"][1], price)
    # 5. expected return implied by the price on the base case (the IRR of buying at today's price)
    out["implied_coe_base"] = _solve(
        lambda r: -project(d, bc["growth"], bc["growth_end"], bc["margin_end"], roiic=bc["roiic"], coe=r)["value_ps"],
        d["terminal_growth"] + 0.011, 0.40, -price)
    # v1.3: ROIIC the price implies on the base-case growth and margin path (only with a realism history)
    if d.get("incremental_roic_5y") is not None:
        if min(bc["growth"], bc["growth_end"]) > 0:
            out["roiic_implied_base"] = _solve(
                lambda x: project(d, bc["growth"], bc["growth_end"], bc["margin_end"], roiic=x)["value_ps"],
                0.01, 3.0, price, steps=300)
        else:
            out["roiic_implied_base"] = None
    # Gordon sanity check on trailing FCF: price = FCF*(1+g)/(r-g) -> g = (P*r - F)/(P + F)
    fcf = d["base"].get("fcf")
    mcap = price * d["shares"]
    ev_mkt = mcap + d["net_debt"]
    if fcf and fcf > 0:
        r = d["coe"]
        out["gordon_g_on_fcf"] = (ev_mkt * r - fcf) / (ev_mkt + fcf)
    else:
        out["gordon_g_on_fcf"] = None
    # implied path for the most readable case (fade to terminal)
    g_path = out["g_fade_start"]
    out["path_case"] = "fade"
    if g_path is None:
        g_path = out["g_base_margin"]
        out["path_case"] = "flat-growth"
    if g_path is not None:
        ge = tg if out["path_case"] == "fade" else g_path
        out["path"] = project(d, g_path, ge, bc["margin_end"])
    else:
        out["path"] = None
    return out


def norm_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def scenario_analysis(d):
    price = d["price"]
    res = []
    for s in d["scenarios"]:
        p = project(d, s["growth"], s["growth_end"], s["margin_end"], roiic=s["roiic"])
        eps5 = p["rows"][4]["eps"]
        mult5 = None
        exit_pe = p["dcf_pe5"] if s["exit_pe"] == "dcf" else s["exit_pe"]
        nog = s.get("nonop_growth", d.get("non_operating_growth"))
        nonop5_ps = (d["non_operating_value"] * (1 + nog) ** 5 / d["shares"]) if nog is not None else 0.0
        if exit_pe and eps5:
            mult5 = (eps5 * exit_pe + p["cum_dist_ps_5y"] + nonop5_ps) / price
        res.append({"name": s["name"], "prob": s["prob"], "growth": s["growth"], "growth_end": s["growth_end"],
                    "margin_end": s["margin_end"], "roiic": s["roiic"], "exit_pe": exit_pe,
                    "exit_pe_is_dcf": s["exit_pe"] == "dcf", "dcf_pe5": p["dcf_pe5"],
                    "value_ps": p["value_ps"], "value_vs_price": p["value_ps"] / price - 1, "eps5": eps5,
                    "eps_cagr5": (eps5 / d["base"]["eps"]) ** 0.2 - 1 if eps5 and d["base"]["eps"] > 0 else None,
                    "dist_ps_5y": p["cum_dist_ps_5y"], "mult5": mult5, "tv_share": p["tv_share"],
                    "nonop5_ps": nonop5_ps})
    bl = d["blowup"]
    out = {"scenarios": res, "blowup": bl}
    if not res:
        return out
    pw = sum(r["prob"] * r["value_ps"] for r in res) + bl["prob"] * bl["multiple"] * price
    out["pw_value"] = pw
    out["pw_vs_price"] = pw / price - 1
    worst = min(res, key=lambda r: r["value_ps"])
    out["bear_value"] = worst["value_ps"]
    out["downside_bear"] = worst["value_ps"] / price - 1
    out["p_value_below_price"] = sum(r["prob"] for r in res if r["value_ps"] < price) + bl["prob"]
    # 5-year outcome distribution: lognormal around each scenario's 5-yr multiple, plus a blow-up point mass
    sig = d["dispersion"]
    if all(r["mult5"] for r in res):
        def p_ge(k):
            return sum(r["prob"] * (1 - norm_cdf((math.log(k) - math.log(r["mult5"])) / sig)) for r in res) + \
                (bl["prob"] if bl["multiple"] >= k else 0.0)

        def p_le(k):
            return sum(r["prob"] * norm_cdf((math.log(k) - math.log(r["mult5"])) / sig) for r in res) + \
                (bl["prob"] if bl["multiple"] <= k else 0.0)
        out["p_ge_3x"] = p_ge(3.0)
        out["p_ge_2x"] = p_ge(2.0)
        out["p_ge_5x"] = p_ge(5.0)
        out["p_le_half"] = p_le(0.5)
        out["p_blowup"] = bl["prob"]
        out["ev_mult5"] = sum(r["prob"] * r["mult5"] for r in res) + bl["prob"] * bl["multiple"]
        out["ev_cagr5"] = out["ev_mult5"] ** 0.2 - 1 if out["ev_mult5"] > 0 else -1.0
        # median of the mixture, by bisection on the CDF
        lo, hi = 0.01, 50.0
        for _ in range(80):
            mid = math.sqrt(lo * hi)
            if p_le(mid) < 0.5:
                lo = mid
            else:
                hi = mid
        out["median_mult5"] = math.sqrt(lo * hi)
        out["hurdle_mult5"] = (1 + d["hurdle_cagr"]) ** 5
        out["exit_bet"] = exit_bet(d, res, bl)
    return out


def exit_bet(d, res, bl):
    """v1.3 (L21): make the exit multiple visible as a bet. For each scenario: the exit P/E used, the P/E the DCF
    itself justifies at year 5, and the stock's own median P/E (n >= MIN_HISTORY_POINTS); then the EV of the 5-year
    multiple if every scenario exited at each of the three. Display only: the card's gate still uses the stated exit."""
    price = d["price"]
    hist = [p["pe"] for p in (d.get("pe_history") or []) if p.get("pe")]
    own = _median(hist) if len(hist) >= MIN_HISTORY_POINTS else None
    rows = []
    for r in res:
        def m(pe):
            if not pe or not r["eps5"]:
                return None
            return (r["eps5"] * pe + r["dist_ps_5y"] + r["nonop5_ps"]) / price
        rows.append({"name": r["name"], "prob": r["prob"], "exit_pe": r["exit_pe"], "dcf_pe5": r["dcf_pe5"],
                     "own_median": own, "mult_stated": r["mult5"], "mult_dcf": m(r["dcf_pe5"]), "mult_own": m(own),
                     "stated_vs_dcf": (r["exit_pe"] / r["dcf_pe5"]) if r["exit_pe"] and r["dcf_pe5"] and r["dcf_pe5"] > 0 else None,
                     "stated_vs_own": (r["exit_pe"] / own) if r["exit_pe"] and own else None})

    def ev(key):
        if any(x[key] is None for x in rows):
            return None
        return sum(x["prob"] * x[key] for x in rows) + bl["prob"] * bl["multiple"]
    return {"own_median": own, "n_hist": len(hist), "rows": rows, "ev_stated": ev("mult_stated"),
            "ev_dcf": ev("mult_dcf"), "ev_own": ev("mult_own"), "hurdle": (1 + d["hurdle_cagr"]) ** 5}


def twin_engine(d):
    te = d["twin_engine"]
    h = float(te.get("horizon", 5))
    b = d["base"]
    eps0 = b.get("eps_normalised") or (d["price"] / b["pe_trailing"] if b.get("pe_trailing") else b["eps"])
    pe0 = d["price"] / eps0 if eps0 > 0 else None
    if not pe0:
        return None
    exit_pes = te.get("exit_pes")
    if not exit_pes:
        cands = [pe0 * 0.5, pe0 * 0.75, pe0]
        med = _median([p["pe"] for p in d.get("pe_history") or [] if p.get("pe")])
        if med and len(d.get("pe_history") or []) >= MIN_HISTORY_POINTS:
            cands.append(med)
        sec = _median(list((d.get("sector_pes") or {}).values()))
        if sec:
            cands.append(sec)
        exit_pes = sorted(set(round(x, 1) for x in cands))
    table = []
    for m in te["targets"]:
        row = {"target": m, "cells": []}
        for pe5 in exit_pes:
            need = (m * pe0 / pe5) ** (1 / h) - 1
            rerating_share = math.log(pe5 / pe0) / math.log(m) if m > 1 else None
            row["cells"].append({"exit_pe": pe5, "eps_cagr": need, "rerating_share": rerating_share})
        table.append(row)
    return {"pe0": pe0, "eps0": eps0, "horizon": h, "exit_pes": exit_pes, "table": table,
            "hist_eps_cagr": te.get("hist_eps_cagr"), "hist_eps_note": te.get("hist_eps_note", "")}


def _median(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def _band(ratio):
    for lim, name in TEMP_BANDS:
        if ratio < lim:
            return name
    return TEMP_BANDS[-1][1]


def temperature(d):
    b = d["base"]
    price = d["price"]
    pes = {}
    pes["trailing (given)" if b.get("pe_trailing") else "trailing (price / base EPS)"] = \
        b.get("pe_trailing") or (price / b["eps"] if b["eps"] > 0 else None)
    if b.get("eps_normalised"):
        pes["normalised EPS"] = price / b["eps_normalised"]
    if b.get("eps_forward"):
        pes["forward EPS"] = price / b["eps_forward"]
    hist = [p for p in (d.get("pe_history") or []) if p.get("pe")]
    own_med = _median([p["pe"] for p in hist])
    sector = d.get("sector_pes") or {}
    sec_med = _median(list(sector.values()))
    out = {"pes": pes, "n_hist": len(hist), "own_median": own_med, "sector_median": sec_med,
           "sector": sector, "rows": []}
    for label, pe in pes.items():
        if not pe:
            continue
        row = {"basis": label, "pe": pe}
        if own_med and len(hist) >= MIN_HISTORY_POINTS:
            row["vs_own"] = pe / own_med
            row["own_band"] = _band(pe / own_med)
            row["pctile"] = sum(1 for p in hist if p["pe"] <= pe) / len(hist)
        else:
            row["vs_own"] = None
            row["own_band"] = "INSUFFICIENT HISTORY (n=%d < %d)" % (len(hist), MIN_HISTORY_POINTS)
        if sec_med:
            row["vs_sector"] = pe / sec_med
            row["sector_band"] = _band(pe / sec_med)
        out["rows"].append(row)
    mp = d.get("market_pe")
    if mp and mp.get("pe"):
        note = ""
        if d["market"] == "india" and "nifty" in str(mp.get("index", "")).lower():
            for lim, txt in NIFTY_BANDS:
                if mp["pe"] < lim:
                    note = txt
                    break
        else:
            note = "no market-level base rate on file for this index (add one before using it)"
        out["market"] = {"index": mp.get("index"), "pe": mp["pe"], "as_of": mp.get("as_of"), "note": note}
    return out


def sensitivity(d):
    bc = d["base_case"]
    r0 = d["coe"]
    rs = [r0 - 0.02, r0 - 0.01, r0, r0 + 0.01, r0 + 0.02]
    gs = [-0.06, -0.03, 0.0, 0.03, 0.06]
    t1 = []
    for r in rs:
        row = []
        for dg in gs:
            if d["terminal_growth"] >= r - 0.005:
                row.append(None)
                continue
            p = project(d, bc["growth"] + dg, max(bc["growth_end"] + dg / 2, d["terminal_growth"]),
                        bc["margin_end"], roiic=bc["roiic"], coe=r)
            row.append(p["value_ps"])
        t1.append((r, row))
    tg0 = d["terminal_growth"]
    tgs = [tg0 - 0.01, tg0, tg0 + 0.01]
    ms = [bc["margin_end"] + x for x in (-0.02, -0.01, 0.0, 0.01, 0.02)]
    t2 = []
    for tg in tgs:
        row = []
        for m in ms:
            p = project(d, bc["growth"], bc["growth_end"], m, roiic=bc["roiic"], tg=tg)
            row.append(p["value_ps"])
        t2.append((tg, row))
    return {"coe_x_growth": {"rows": t1, "cols": gs}, "tg_x_margin": {"rows": t2, "cols": ms}}


def run(d):
    if d.get("mode") in ("bank", "nbfc", "lender"):
        return _bank().run(d, _band, MIN_HISTORY_POINTS, NIFTY_BANDS)
    price = d["price"]
    b = d["base"]
    mcap = price * d["shares"]
    ev_mkt = mcap + d["net_debt"]
    snap = {"mcap": mcap, "ev": ev_mkt,
            "pe": b.get("pe_trailing") or (price / b["eps"] if b["eps"] > 0 else None),
            "ev_ebitda": ev_mkt / b["ebitda"] if b.get("ebitda") else None,
            "p_fcf": mcap / b["fcf"] if b.get("fcf") else None,
            "fcf_yield": b["fcf"] / mcap if b.get("fcf") else None,
            "ev_sales": ev_mkt / b["revenue"]}
    bc = d["base_case"]
    base = project(d, bc["growth"], bc["growth_end"], bc["margin_end"], roiic=bc["roiic"])
    rv = reverse_dcf(d)
    out = {"input": d, "snapshot": snap, "base": base, "reverse": rv,
           "scenarios": scenario_analysis(d), "twin": twin_engine(d), "temperature": temperature(d),
           "sensitivity": sensitivity(d), "version": VERSION,
           "generated": _dt.date.today().isoformat()}
    if d.get("incremental_roic_5y") is not None:
        out["realism"] = realism(d, rv)
    return out


REALISM_GAP = 0.05   # v1.3: ROIIC used/implied this far (either way) from the last-5y incremental ROIC is flagged


def realism(d, rv):
    """v1.3: compare each ROIIC the worksheet uses (and the one the price implies) with what the company earned on
    its incremental capital over the last ~5 years."""
    h = d["incremental_roic_5y"]
    items = [("default ROIIC (input)", d["roiic"])]
    items += [("scenario %s" % s["name"], s["roiic"]) for s in d["scenarios"]]
    items.append(("implied by price on the base-case path", rv.get("roiic_implied_base")))
    rows = []
    for label, x in items:
        gap = (x - h) if x is not None else None
        rows.append({"label": label, "roiic": x, "gap": gap, "flag": gap is not None and abs(gap) > REALISM_GAP})
    return {"history": h, "method": d.get("_inc_roic_method"), "rows": rows,
            "flagged": [r["label"] for r in rows if r["flag"]]}


# ----------------------------------------------------------------------------- markdown

def pct(x, nd=1):
    return "n/a" if x is None else ("%." + str(nd) + "f%%") % (100 * x)


def num(x, nd=1):
    if x is None:
        return "n/a"
    if abs(x) >= 1000:
        return "{:,.0f}".format(x)
    return ("{:,.%df}" % nd).format(x)


def mult(x):
    return "n/a" if x is None else "%.2fx" % x


def render(res, heading_level=2):
    if res.get("mode") == "bank":
        return _bank().render(res, heading_level, pct, num, mult,
                              MARKET_DEFAULTS[res["input"]["market"]]["coe_range"])
    d = res["input"]
    H = "#" * heading_level
    h = "#" * (heading_level + 1)
    cur = d.get("currency", "")
    u = d.get("units", "")
    price = d["price"]
    L = []
    L.append("%s Valuation worksheet: %s (%s) · as of %s" % (H, d.get("company"), d.get("ticker"), d.get("as_of")))
    L.append("")
    if d.get("practice"):
        L.append("> **TEST MATERIAL. No verdict.** These inputs exist to exercise the template (lesson L9). "
                 "The scenario assumptions are illustrative [EST], not research conclusions. "
                 "Research, not SEBI-registered advice.")
        L.append("")
    L.append("*Worksheet v%s. Money in %s; per-share figures in %s. Cost of equity %s (market default %s), "
             "terminal growth %s, %d-year explicit period, ROIIC %s, terminal ROIC %s.*"
             % (res["version"], u, cur, pct(d["coe"]), MARKET_DEFAULTS[d["market"]]["coe_range"],
                pct(d["terminal_growth"]), d["years"], pct(d["roiic"], 0), pct(d["terminal_roic"], 0)))
    if d.get("cash_tax_rate") is not None:
        L.append("*Cash tax (v1.3): %s in year 1 → %s in year %d and the terminal value, vs book tax %s (%s). FCF adds "
                 "NOPAT × (book − cash) ÷ (1 − book); EPS stays on book tax.*"
                 % (pct(d["cash_tax_rate"]), pct(d["cash_tax_rate_end"]), d["years"], pct(d["tax_rate"]),
                    d.get("_cash_tax_method")))
    L.append("")
    for w in d.get("_warnings", []):
        L.append("> Warning: %s" % w)
    if d.get("_warnings"):
        L.append("")
    s = res["snapshot"]
    b = d["base"]
    L.append("%s Snapshot (%s)" % (h, b.get("fy", "base year")))
    L.append("| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s (%s) |" % (
        num(price, 2), num(s["mcap"]), num(d["net_debt"]), num(s["ev"]), num(s["pe"]), num(s["ev_ebitda"]),
        num(s["p_fcf"]), pct(s["fcf_yield"]), pct(d["nopat_margin"]), d.get("_nopat_margin_method")))
    L.append("")

    # (a) reverse DCF
    rv = res["reverse"]
    L.append("%s (a) Reverse DCF: what today's price implies" % h)
    L.append("| Question | Implied by price %s |" % num(price, 2))
    L.append("|---|---|")
    L.append("| Revenue CAGR for %d yrs, NOPAT margin flat at %s | %s |"
             % (d["years"], pct(d["nopat_margin"]), _na(rv["g_flat_margin"], RANGES["g"])))
    L.append("| Revenue CAGR for %d yrs, margin moving to base-case %s | %s |"
             % (d["years"], pct(d["base_case"]["margin_end"]), _na(rv["g_base_margin"], RANGES["g"])))
    L.append("| Year-1 growth, fading linearly to %s by year %d (margin to %s) | %s |"
             % (pct(d["terminal_growth"]), d["years"], pct(d["base_case"]["margin_end"]),
                _na(rv["g_fade_start"], RANGES["g_fade"])))
    L.append("| NOPAT margin needed by year %d on the base-case growth path (%s → %s) | %s |"
             % (d["years"], pct(d["base_case"]["growth"]), pct(d["base_case"]["growth_end"]),
                _na(rv["m_needed_base_growth"], RANGES["m"])))
    L.append("| Gordon check: perpetual FCF growth implied by trailing FCF yield | %s |" % pct(rv["gordon_g_on_fcf"]))
    if rv.get("roiic_implied_base") is not None or "roiic_implied_base" in rv:
        L.append("| ROIIC the price implies on the base-case growth and margin path | %s |"
                 % _na(rv.get("roiic_implied_base"), (0.01, 3.0)))
    L.append("| Expected return (IRR) the price offers if the base case happens | %s (vs cost of equity %s) |"
             % (_na(rv["implied_coe_base"], (d["terminal_growth"] + 0.011, 0.40)), pct(d["coe"])))
    L.append("")
    if rv.get("path"):
        p = rv["path"]
        L.append("Implied path (%s case). Reinvestment = growth ÷ ROIIC; P/E column = today's price ÷ that year's EPS:"
                 % ("fade-to-terminal" if rv["path_case"] == "fade" else "flat-growth"))
        L.append("")
        L.append("| Year | Growth | Revenue | NOPAT margin | NOPAT | Reinvestment % NOPAT | FCF | EPS | Price ÷ EPS |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for r in p["rows"]:
            if r["t"] in (1, 2, 3, 5, 7, d["years"]) or r["t"] == d["years"]:
                L.append("| %d | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                    r["t"], pct(r["g"]), num(r["revenue"]), pct(r["margin"]), num(r["nopat"]),
                    pct(r["reinv_rate"], 0), num(r["fcf"]), num(r["eps"], 2),
                    num(price / r["eps"]) if r["eps"] and r["eps"] > 0 else "n/a"))
        L.append("")
        last = p["rows"][-1]
        if p["max_reinv_rate"] > 1.0:
            L.append("> **Feasibility flag:** on this path reinvestment exceeds 100%% of NOPAT (peak %s), so FCF is "
                     "negative and growth would need outside capital at ROIIC %s. Either ROIIC is higher than "
                     "assumed or the implied path is not self-fundable." % (pct(p["max_reinv_rate"], 0), pct(d["roiic"], 0)))
            L.append("")
        L.append("Reading: the price needs revenue of ~%s %s by year %d (%.1fx today's) and terminal value is %s of EV. "
                 "Compare with what the business has shown (unit runway, reinvestment capacity, ROIIC), not with a "
                 "consensus number." % (num(last["revenue"]), u, d["years"], last["revenue"] / b["revenue"],
                                        pct(p["tv_share"], 0)))
        L.append("")

    if res.get("realism"):
        rz = res["realism"]
        L.append("Reinvestment realism (v1.3): last-5y incremental ROIC **%s** (%s). Flag when a ROIIC used or implied "
                 "differs by more than %s:" % (pct(rz["history"]), rz["method"], pct(REALISM_GAP, 0)))
        L.append("")
        L.append("| ROIIC | Value | Gap vs history | Flag |")
        L.append("|---|---|---|---|")
        for r in rz["rows"]:
            L.append("| %s | %s | %s | %s |" % (r["label"], pct(r["roiic"]) if r["roiic"] is not None else
                                                 "none in tested range 1-300%",
                                                 ("%+.1f pts" % (100 * r["gap"])) if r["gap"] is not None else "n/a",
                                                 "**FLAG**" if r["flag"] else "ok"))
        L.append("")
        if rz["flagged"]:
            L.append("> **Reinvestment-realism flag:** %s. Either the business will earn on new capital what it has "
                     "not earned recently, or the path is mis-specified (e.g. pricing-led growth that needs little "
                     "capital). Say which in the deep dive." % "; ".join(rz["flagged"]))
            L.append("")

    # (b) scenarios
    sc = res["scenarios"]
    if sc["scenarios"]:
        L.append("%s (b) Scenario DCF and 5-year outcome distribution" % h)
        L.append("| Scenario | Prob | Growth yr1 → yr%d | NOPAT margin yr%d | ROIIC | DCF value/sh | vs price | "
                 "EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |"
                 % (d["years"], d["years"]))
        L.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in sc["scenarios"]:
            L.append("| %s | %s | %s → %s | %s | %s | %s | %s | %s | %s%s | %s | %s |" % (
                r["name"], pct(r["prob"], 0), pct(r["growth"]), pct(r["growth_end"]), pct(r["margin_end"]),
                pct(r["roiic"], 0), num(r["value_ps"], 1), pct(r["value_vs_price"], 0), pct(r["eps_cagr5"]),
                num(r["exit_pe"]), " (dcf)" if r["exit_pe_is_dcf"] else "", num(r["dcf_pe5"]), mult(r["mult5"])))
        bl = sc["blowup"]
        if bl["prob"]:
            L.append("| blow-up | %s | — | — | — | %s | %s | — | — | — | %s |" % (
                pct(bl["prob"], 0), num(bl["multiple"] * price, 1), pct(bl["multiple"] - 1, 0), mult(bl["multiple"])))
        L.append("")
        L.append("| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |")
        L.append("|---|---|---|---|")
        L.append("| %s | %s | %s | %s |" % (num(sc["pw_value"], 1), pct(sc["pw_vs_price"], 0),
                                          pct(sc["downside_bear"], 0), pct(sc["p_value_below_price"], 0)))
        L.append("")
        if "p_ge_3x" in sc:
            L.append("5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=%.2f, blow-up as a point mass):"
                     % d["dispersion"])
            L.append("")
            L.append("| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (%s/yr) |"
                     % pct(d["hurdle_cagr"], 0))
            L.append("|---|---|---|---|---|---|---|---|---|")
            L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                pct(sc["p_ge_2x"], 0), pct(sc["p_ge_3x"], 0), pct(sc["p_ge_5x"], 0), pct(sc["p_le_half"], 0),
                pct(sc["p_blowup"], 0), mult(sc["ev_mult5"]), pct(sc["ev_cagr5"]), mult(sc["median_mult5"]),
                mult(sc["hurdle_mult5"])))
            L.append("")
            gap = [r for r in sc["scenarios"] if r["dcf_pe5"] and r["exit_pe"] and not r["exit_pe_is_dcf"]
                   and r["exit_pe"] > 1.25 * r["dcf_pe5"]]
            if gap:
                L.append("> **Exit-multiple gap:** in %s the exit P/E used is >1.25x the DCF-consistent P/E at year 5. "
                         "Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of "
                         "equity justifies. Show the card both ways (set `exit_pe` to \"dcf\" to test)."
                         % ", ".join(r["name"] for r in gap))
                L.append("")
            eb = sc.get("exit_bet")
            if eb:
                L.append("**Exit-multiple bet (v1.3, L21).** The 5-year multiple is a bet on the P/E the market pays in "
                         "year 5. Own median P/E: %s." % ("%s (n=%d)" % (num(eb["own_median"]), eb["n_hist"])
                                                         if eb["own_median"] else
                                                         "n/a (n=%d < %d)" % (eb["n_hist"], MIN_HISTORY_POINTS)))
                L.append("")
                L.append("| Scenario | Exit P/E used | DCF-consistent P/E yr5 | Own median P/E | Used ÷ DCF | Used ÷ own | "
                         "5-yr multiple at used | at DCF P/E | at own median |")
                L.append("|---|---|---|---|---|---|---|---|---|")
                for x in eb["rows"]:
                    L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                        x["name"], num(x["exit_pe"]), num(x["dcf_pe5"]), num(x["own_median"]), mult(x["stated_vs_dcf"]),
                        mult(x["stated_vs_own"]), mult(x["mult_stated"]), mult(x["mult_dcf"]), mult(x["mult_own"])))
                L.append("| **EV (incl. blow-up)** | | | | | | **%s** | **%s** | **%s** |"
                         % (mult(eb["ev_stated"]), mult(eb["ev_dcf"]), mult(eb["ev_own"])))
                L.append("")
                L.append("Hurdle %s. The card's gate uses the stated exit; the other two columns show how much of the "
                         "answer is the multiple bet." % mult(eb["hurdle"]))
                L.append("")
            L.append("Base rates for these probabilities live in the decision card (stage 6), not here.")
            L.append("")

    # (c) twin engine
    tw = res["twin"]
    if tw:
        L.append("%s (c) Twin engine: EPS growth needed × exit multiple" % h)
        L.append("Starting P/E %s on EPS %s. Cell = EPS CAGR needed over %d years; (r) = share of the return that "
                 "must come from re-rating (negative = de-rating eats part of EPS growth)."
                 % (num(tw["pe0"]), num(tw["eps0"], 2), tw["horizon"]))
        L.append("")
        L.append("| Target | " + " | ".join("exit P/E %s" % num(x) for x in tw["exit_pes"]) + " |")
        L.append("|---|" + "---|" * len(tw["exit_pes"]))
        for row in tw["table"]:
            cells = []
            for c in row["cells"]:
                cells.append("%s (r %s)" % (pct(c["eps_cagr"], 0), pct(c["rerating_share"], 0)))
            L.append("| %sx | %s |" % (num(row["target"], 0), " | ".join(cells)))
        L.append("")
        if tw.get("hist_eps_cagr") is not None:
            L.append("Track record for comparison: EPS CAGR %s %s." % (pct(tw["hist_eps_cagr"]), tw.get("hist_eps_note", "")))
            L.append("")
        L.append("Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from "
                 "re-rating over long runs; when more than half of a gain is multiple, it is fragile "
                 "(`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs "
                 "~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).")
        L.append("")

    # (d) temperature
    tp = res["temperature"]
    L.append("%s (d) Valuation temperature" % h)
    L.append("| Basis | P/E | vs own median (n=%d) | Own band | Percentile in own history | vs sector median | Sector band |"
             % tp["n_hist"])
    L.append("|---|---|---|---|---|---|---|")
    for r in tp["rows"]:
        L.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            r["basis"], num(r["pe"]), mult(r.get("vs_own")), r.get("own_band"),
            pct(r.get("pctile"), 0) if r.get("pctile") is not None else "n/a",
            mult(r.get("vs_sector")), r.get("sector_band", "no sector P/Es given")))
    L.append("")
    if tp["own_median"]:
        L.append("Own P/E history: " + ", ".join("%s %s" % (p.get("date"), num(p["pe"])) for p in d.get("pe_history") or [])
                 + " (median %s)." % num(tp["own_median"]))
    if tp["sector"]:
        L.append("Sector P/Es: " + ", ".join("%s %s" % (k, num(v)) for k, v in tp["sector"].items())
                 + " (median %s)." % num(tp["sector_median"]))
    if tp.get("market"):
        m = tp["market"]
        L.append("Market: %s P/E %s (%s): %s." % (m["index"], num(m["pe"]), m.get("as_of"), m["note"]))
    L.append("Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. "
             "≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).")
    L.append("")

    # (e) sensitivity
    se = res["sensitivity"]
    L.append("%s (e) Sensitivity (base case; value per share, and vs price)" % h)
    t = se["coe_x_growth"]
    L.append("Cost of equity (rows) × shift in base-case growth path (columns; year-%d growth shifts by half):" % d["years"])
    L.append("")
    L.append("| CoE \\ Δgrowth | " + " | ".join(("%+.0f pp" % (100 * c)) for c in t["cols"]) + " |")
    L.append("|---|" + "---|" * len(t["cols"]))
    for r, row in t["rows"]:
        L.append("| %s | %s |" % (pct(r), " | ".join(
            "n/a" if v is None else "%s (%s)" % (num(v, 0), pct(v / price - 1, 0)) for v in row)))
    L.append("")
    t = se["tg_x_margin"]
    L.append("Terminal growth (rows) × year-%d NOPAT margin (columns):" % d["years"])
    L.append("")
    L.append("| TG \\ margin | " + " | ".join(pct(c) for c in t["cols"]) + " |")
    L.append("|---|" + "---|" * len(t["cols"]))
    for tg, row in t["rows"]:
        L.append("| %s | %s |" % (pct(tg), " | ".join("%s (%s)" % (num(v, 0), pct(v / price - 1, 0)) for v in row)))
    L.append("")
    if d.get("notes"):
        L.append("%s Input notes" % h)
        for n_ in d["notes"]:
            L.append("- %s" % n_)
        L.append("")
    if d.get("sources"):
        L.append("Sources: " + "; ".join(d["sources"]))
        L.append("")
    return "\n".join(L)


def _jsonable(res):
    def conv(o):
        if isinstance(o, dict):
            return {k: conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [conv(v) for v in o]
        if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
            return None
        return o
    return conv(res)


def main(argv=None):
    ap = argparse.ArgumentParser(description="FEIN valuation worksheet (stage 5)")
    ap.add_argument("input", nargs="?", help="input JSON file")
    ap.add_argument("-o", "--out", help="write the Markdown section to this file")
    ap.add_argument("--json", help="also write machine-readable results to this file")
    ap.add_argument("--template", action="store_true", help="print a blank input template")
    ap.add_argument("--mode", choices=["default", "bank"], default="default",
                    help="with --template: 'bank' prints the bank/NBFC (P/B-ROE, residual income) template")
    ap.add_argument("--level", type=int, default=2, help="Markdown heading level (default 2)")
    a = ap.parse_args(argv)
    if a.template:
        print(json.dumps(_bank().TEMPLATE if a.mode == "bank" else TEMPLATE, indent=2))
        return 0
    if not a.input:
        ap.error("input file required (or --template)")
    d = load_input(a.input)
    res = run(d)
    md = render(res, a.level)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(md + "\n")
    else:
        print(md)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(_jsonable(res), f, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
