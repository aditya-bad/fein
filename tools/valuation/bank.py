#!/usr/bin/env python3
"""Bank / NBFC mode for the FEIN valuation worksheet (stage 5). Added 2026-11-22 (FEDERALBNK dry run).

Why a separate mode: a lender's "revenue", "EBIT", "FCF" and "ROIIC" are not meaningful (debt is raw
material, not financing), so the value-driver DCF in worksheet.py does not apply. Banks are valued on
book value and the return earned on it:

  justified P/B  = (ROE - g) / (CoE - g)                       (Gordon on residual income)
  implied ROE    = g + P/B x (CoE - g)                          (what the price needs, forever)
  RIM value      = B0 + sum_t (ROE_t - CoE) x B_(t-1) / (1+CoE)^t + TV_N
  TV_N           = (ROE_T - CoE) x B_N / (CoE - g) / (1+CoE)^N  (terminal ROE_T persists, BV grows at g)
  B_t            = B_(t-1) x (1 + ROE_t x (1 - payout_t))       (book grows by retained earnings)
  5-yr multiple  = (BVPS_5 x exit P/B + dividends per share over 5 yrs) / price

Dilution: warrants / QIPs are applied up front (fully diluted shares and book, cash received at the
exercise price), because a P/B on undiluted book flatters a bank that is about to issue ~10% more stock.
Same result keys as worksheet.run() (snapshot, reverse, scenarios, twin, temperature, sensitivity), so
tools/decision/decision_card.py works unchanged except for its stage-5 text block. Standard library only.
"""
import math

VERSION = "1.1-bank (2026-11-22)"

TEMPLATE = {
    "mode": "bank",
    "company": "Bank name", "ticker": "TICKER", "market": "india", "practice": True,
    "currency": "INR", "units": "INR cr", "as_of": "2026-11-21", "price": 100.0,
    "shares": 100.0, "# shares": "crore, same scale as money units",
    "book_value": 10000.0, "# book_value": "net worth (equity + reserves), INR cr, at the latest balance sheet",
    "book_adjustments": [{"name": "share warrant money already in reserves", "amount": 0.0}],
    "dilution": [{"name": "warrants", "shares": 0.0, "cash_in": 0.0, "# cash_in": "cash still to be received"}],
    "base": {"fy": "TTM", "pat": 1200.0, "pat_normalised": None, "roe_reported": 0.12, "dps": 1.0,
             "pe_trailing": None, "loans": 80000.0, "assets": 120000.0, "net_npa": 300.0, "cet1": 0.15},
    "coe": None, "terminal_growth": None, "hurdle_cagr": None, "years": 10, "dispersion": 0.30,
    "payout": 0.10,
    "base_case": {"roe_start": 0.13, "roe_end": 0.14, "exit_pb": 2.0},
    "scenarios": [
        {"name": "bear", "prob": 0.30, "roe_start": 0.11, "roe_end": 0.11, "exit_pb": 1.2},
        {"name": "base", "prob": 0.50, "roe_start": 0.13, "roe_end": 0.14, "exit_pb": 1.8},
        {"name": "bull", "prob": 0.18, "roe_start": 0.15, "roe_end": 0.16, "exit_pb": 2.5},
    ],
    "blowup": {"prob": 0.02, "multiple": 0.2, "note": "asset-quality / governance event that wipes most of book"},
    "stress_loss_rates": [0.01, 0.02, 0.03, 0.05],
    "pb_history": [{"date": "FY22", "pb": 1.1}],
    "sector_pbs": {"Peer A": 1.5},
    "market_pe": {"index": "Nifty 50", "pe": 20.6, "as_of": "2026-11"},
    "notes": ["source tags and [EST] methods for every input go here"], "sources": [],
}


def _f(x, name, default=None):
    if x is None:
        return default
    try:
        return float(x)
    except (TypeError, ValueError):
        raise ValueError("field %s must be a number, got %r" % (name, x))


def normalise(d, market_defaults):
    warn = d.setdefault("_warnings", [])
    mkt = str(d.get("market", "india")).lower()
    md = market_defaults[mkt]
    d["market"] = mkt
    for k in ("price", "shares", "book_value"):
        d[k] = _f(d.get(k), k)
        if not d[k]:
            raise ValueError("bank mode: %s is required" % k)
    adj = sum(_f(a.get("amount"), "book_adjustments.amount", 0.0) for a in d.get("book_adjustments") or [])
    dil_sh = sum(_f(x.get("shares"), "dilution.shares", 0.0) for x in d.get("dilution") or [])
    dil_cash = sum(_f(x.get("cash_in"), "dilution.cash_in", 0.0) for x in d.get("dilution") or [])
    d["_book_undiluted"] = d["book_value"] - adj
    d["_shares_diluted"] = d["shares"] + dil_sh
    d["_book_diluted"] = d["book_value"] + dil_cash          # warrant money already received stays in book
    d["_bvps_undiluted"] = d["_book_undiluted"] / d["shares"]
    d["_bvps"] = d["_book_diluted"] / d["_shares_diluted"]
    if dil_sh:
        warn.append("fully diluted: +%.2f cr shares, +%.0f cash to be received; BVPS %.2f -> %.2f"
                    % (dil_sh, dil_cash, d["_bvps_undiluted"], d["_bvps"]))
    d["coe"] = _f(d.get("coe"), "coe") or md["coe"]
    tg = _f(d.get("terminal_growth"), "terminal_growth")
    d["terminal_growth"] = md["tg"] if tg is None else tg
    d["hurdle_cagr"] = _f(d.get("hurdle_cagr"), "hurdle_cagr") or md["hurdle"]
    if d["terminal_growth"] >= d["coe"] - 0.01:
        raise ValueError("terminal_growth must be at least 1 pp below the cost of equity")
    d["years"] = int(d.get("years", 10))
    if d["years"] < 5:
        raise ValueError("years must be >= 5")
    d["dispersion"] = _f(d.get("dispersion"), "dispersion", 0.30)
    d["payout"] = _f(d.get("payout"), "payout", 0.10)
    b = d.get("base") or {}
    for k in ("pat", "pat_normalised", "roe_reported", "dps", "pe_trailing", "loans", "assets", "net_npa", "cet1"):
        b[k] = _f(b.get(k), "base." + k)
    d["base"] = b
    b["eps"] = (b.get("pat_normalised") or b.get("pat") or 0) / d["_shares_diluted"]

    def fill(c):
        c = dict(c)
        c["name"] = str(c.get("name", "base"))
        c["roe_start"] = _f(c.get("roe_start"), "roe_start")
        if c["roe_start"] is None:
            raise ValueError("case %s needs roe_start" % c["name"])
        c["roe_end"] = _f(c.get("roe_end"), "roe_end", c["roe_start"])
        c["payout"] = _f(c.get("payout"), "payout", d["payout"])
        ep = c.get("exit_pb")
        c["exit_pb"] = "rim" if isinstance(ep, str) and ep.lower() in ("rim", "dcf") else _f(ep, "exit_pb")
        c["prob"] = _f(c.get("prob"), "prob", 0.0)
        return c
    bc = d.get("base_case") or next((s for s in d.get("scenarios") or [] if s.get("name") == "base"), None)
    if not bc:
        raise ValueError("give base_case or a scenario named 'base'")
    d["base_case"] = fill(bc)
    d["scenarios"] = [fill(s) for s in d.get("scenarios") or []]
    bl = d.get("blowup") or {"prob": 0.0, "multiple": 0.2}
    bl["prob"] = _f(bl.get("prob"), "blowup.prob", 0.0)
    bl["multiple"] = _f(bl.get("multiple"), "blowup.multiple", 0.2)
    d["blowup"] = bl
    if d["scenarios"]:
        tot = sum(s["prob"] for s in d["scenarios"]) + bl["prob"]
        if abs(tot - 1) > 0.005:
            warn.append("scenario + blow-up probabilities summed to %.3f; rescaled" % tot)
            for s in d["scenarios"]:
                s["prob"] /= tot
            bl["prob"] /= tot
    return d


# ----------------------------------------------------------------------------- model

def project(d, roe_start, roe_end, payout=None, coe=None, tg=None, years=None):
    r = d["coe"] if coe is None else coe
    g = d["terminal_growth"] if tg is None else tg
    n = d["years"] if years is None else years
    po = d["payout"] if payout is None else payout
    b = d["_bvps"]
    rows, pv_ri, cum_div5 = [], 0.0, 0.0
    for t in range(1, n + 1):
        roe = roe_start + (roe_end - roe_start) * (t - 1) / max(n - 1, 1)
        eps = roe * b
        div = eps * po
        ri = (roe - r) * b
        pv_ri += ri / (1 + r) ** t
        b_next = b + eps - div
        if t <= 5:
            cum_div5 += div
        rows.append({"t": t, "roe": roe, "bvps_open": b, "eps": eps, "dps": div, "ri": ri, "bvps": b_next})
        b = b_next
    tv = (roe_end - r) * b / (r - g) / (1 + r) ** n
    value = d["_bvps"] + pv_ri + tv
    # RIM-consistent P/B at year 5: value of the remaining path at t=5 / BVPS_5
    b5 = rows[4]["bvps"]
    rem = sum(rw["ri"] / (1 + r) ** (rw["t"] - 5) for rw in rows[5:]) + (roe_end - r) * b / (r - g) / (1 + r) ** (n - 5)
    return {"rows": rows, "value_ps": value, "pv_ri": pv_ri, "tv": tv, "tv_share": tv / value if value else None,
            "bvps5": b5, "eps5": rows[4]["eps"], "cum_div5": cum_div5, "rim_pb5": (b5 + rem) / b5,
            "justified_pb_terminal": (roe_end - g) / (r - g)}


def _solve(f, lo, hi, target, steps=200):
    flo = f(lo) - target
    for _ in range(steps):
        mid = (lo + hi) / 2
        fm = f(mid) - target
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def reverse(d):
    r, g, pb = d["coe"], d["terminal_growth"], d["price"] / d["_bvps"]
    out = {"pb": pb, "pb_undiluted": d["price"] / d["_bvps_undiluted"],
           "roe_implied_gordon": g + pb * (r - g)}
    roe_now = d["base"].get("roe_reported")
    if d["base"].get("pat_normalised"):
        roe_now = d["base"]["pat_normalised"] / d["_book_diluted"]
    out["roe_now"] = roe_now
    # the cost of equity the market is using if today's ROE is permanent (g + (ROE - g) / P/B)
    out["coe_implied_at_current_roe"] = g + (roe_now - g) / pb if roe_now else None
    # ROE held for N years, after which the bank earns only its cost of equity (no franchise value left)
    def val_fade(roe):
        p = project(d, roe, roe)
        pv = d["_bvps"] + p["pv_ri"]   # TV = 0 when ROE_T = CoE
        return pv
    out["roe_implied_10y_then_coe"] = _solve(val_fade, 0.0, 0.8, d["price"])
    bc = d["base_case"]
    try:
        out["irr_base"] = _solve(lambda rr: project(d, bc["roe_start"], bc["roe_end"], bc["payout"], coe=rr)["value_ps"]
                                 if rr > d["terminal_growth"] + 0.002 else 1e9,
                                 d["terminal_growth"] + 0.003, 0.6, d["price"])
    except ZeroDivisionError:
        out["irr_base"] = None
    out["justified_pb_base"] = (bc["roe_end"] - g) / (r - g)
    out["base"] = project(d, bc["roe_start"], bc["roe_end"], bc["payout"])
    return out


def norm_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def scenarios(d):
    price, res = d["price"], []
    for s in d["scenarios"]:
        p = project(d, s["roe_start"], s["roe_end"], s["payout"])
        exit_pb = p["rim_pb5"] if s["exit_pb"] == "rim" else s["exit_pb"]
        mult5 = (p["bvps5"] * exit_pb + p["cum_div5"]) / price if exit_pb else None
        res.append({"name": s["name"], "prob": s["prob"], "roe_start": s["roe_start"], "roe_end": s["roe_end"],
                    "exit_pb": exit_pb, "exit_pb_is_rim": s["exit_pb"] == "rim", "rim_pb5": p["rim_pb5"],
                    "value_ps": p["value_ps"], "value_vs_price": p["value_ps"] / price - 1, "bvps5": p["bvps5"],
                    "eps5": p["eps5"], "dist_ps_5y": p["cum_div5"], "mult5": mult5, "tv_share": p["tv_share"],
                    "exit_pe": None, "dcf_pe5": None})
    bl = d["blowup"]
    out = {"scenarios": res, "blowup": bl}
    if not res:
        return out
    out["pw_value"] = sum(x["prob"] * x["value_ps"] for x in res) + bl["prob"] * bl["multiple"] * price
    out["pw_vs_price"] = out["pw_value"] / price - 1
    worst = min(res, key=lambda x: x["value_ps"])
    out["bear_value"], out["downside_bear"] = worst["value_ps"], worst["value_ps"] / price - 1
    out["p_value_below_price"] = sum(x["prob"] for x in res if x["value_ps"] < price) + bl["prob"]
    sig = d["dispersion"]
    if all(x["mult5"] for x in res):
        def p_ge(k):
            return sum(x["prob"] * (1 - norm_cdf((math.log(k) - math.log(x["mult5"])) / sig)) for x in res) + \
                (bl["prob"] if bl["multiple"] >= k else 0.0)

        def p_le(k):
            return sum(x["prob"] * norm_cdf((math.log(k) - math.log(x["mult5"])) / sig) for x in res) + \
                (bl["prob"] if bl["multiple"] <= k else 0.0)
        out.update(p_ge_3x=p_ge(3.0), p_ge_2x=p_ge(2.0), p_ge_5x=p_ge(5.0), p_le_half=p_le(0.5), p_blowup=bl["prob"])
        out["ev_mult5"] = sum(x["prob"] * x["mult5"] for x in res) + bl["prob"] * bl["multiple"]
        out["ev_cagr5"] = out["ev_mult5"] ** 0.2 - 1 if out["ev_mult5"] > 0 else -1.0
        lo, hi = 0.01, 50.0
        for _ in range(80):
            mid = math.sqrt(lo * hi)
            lo, hi = (mid, hi) if p_le(mid) < 0.5 else (lo, mid)
        out["median_mult5"] = math.sqrt(lo * hi)
        out["hurdle_mult5"] = (1 + d["hurdle_cagr"]) ** 5
    return out


def twin(d):
    pb0 = d["price"] / d["_bvps"]
    exits = sorted(set(round(x, 2) for x in (pb0 * 0.6, pb0 * 0.8, pb0, _median(
        [p["pb"] for p in d.get("pb_history") or [] if p.get("pb")]) or pb0) if x))
    table = []
    for m in (2, 3, 5):
        table.append({"target": m, "cells": [{"exit_pb": e, "bv_cagr": (m * pb0 / e) ** 0.2 - 1,
                                               "rerating_share": math.log(e / pb0) / math.log(m)} for e in exits]})
    return {"pb0": pb0, "exit_pbs": exits, "table": table, "pe0": None}


def _median(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def temperature(d, band_fn, min_hist, nifty_bands):
    pb = d["price"] / d["_bvps"]
    hist = [p for p in d.get("pb_history") or [] if p.get("pb")]
    own = _median([p["pb"] for p in hist])
    sec = d.get("sector_pbs") or {}
    sec_med = _median(list(sec.values()))
    row = {"basis": "P/B (fully diluted)", "pe": pb, "pb": pb}
    if own and len(hist) >= min_hist:
        row.update(vs_own=pb / own, own_band=band_fn(pb / own), pctile=sum(1 for p in hist if p["pb"] <= pb) / len(hist))
    else:
        row.update(vs_own=None, own_band="INSUFFICIENT HISTORY (n=%d < %d)" % (len(hist), min_hist))
    if sec_med:
        row.update(vs_sector=pb / sec_med, sector_band=band_fn(pb / sec_med))
    out = {"rows": [row], "own_median": own, "n_hist": len(hist), "sector_median": sec_med, "sector": sec}
    pe = d["base"].get("pe_trailing") or (d["price"] / d["base"]["eps"] if d["base"]["eps"] else None)
    out["pe"] = pe
    mp = d.get("market_pe")
    if mp and mp.get("pe"):
        note = next((t for lim, t in nifty_bands if mp["pe"] < lim), "") if "nifty" in str(mp.get("index", "")).lower() \
            else "no market-level base rate on file"
        out["market"] = {"index": mp.get("index"), "pe": mp["pe"], "as_of": mp.get("as_of"), "note": note}
    return out


def stress(d):
    b = d["base"]
    if not (b.get("loans") and d["book_value"]):
        return None
    eq = d["_book_diluted"]
    rows = []
    for lr in d.get("stress_loss_rates") or [0.01, 0.02, 0.03, 0.05]:
        loss = lr * b["loans"] * (1 - 0.25)          # post-tax at 25%
        rows.append({"loss_rate": lr, "post_tax_loss": loss, "pct_of_book": loss / eq,
                     "bvps_after": (eq - loss) / d["_shares_diluted"]})
    return {"leverage": (b.get("assets") or 0) / eq if b.get("assets") else None, "rows": rows,
            "net_npa_pct_book": (b.get("net_npa") or 0) / eq}


def sensitivity(d):
    bc = d["base_case"]
    rs = [d["coe"] + x for x in (-0.02, -0.01, 0.0, 0.01, 0.02)]
    roes = [bc["roe_end"] + x for x in (-0.03, -0.015, 0.0, 0.015, 0.03)]
    t = []
    for r in rs:
        t.append((r, [None if d["terminal_growth"] >= r - 0.005 else
                      project(d, bc["roe_start"], e, bc["payout"], coe=r)["value_ps"] for e in roes]))
    jp = [(r, [(e - d["terminal_growth"]) / (r - d["terminal_growth"]) for e in roes]) for r in rs]
    return {"coe_x_roe": {"rows": t, "cols": roes}, "justified_pb": {"rows": jp, "cols": roes}}


def run(d, band_fn, min_hist, nifty_bands):
    price = d["price"]
    snap = {"mcap": price * d["shares"], "mcap_diluted": price * d["_shares_diluted"], "pb": price / d["_bvps"],
            "pb_undiluted": price / d["_bvps_undiluted"], "bvps": d["_bvps"], "bvps_undiluted": d["_bvps_undiluted"],
            "pe": d["base"].get("pe_trailing") or (price / d["base"]["eps"] if d["base"]["eps"] else None),
            "roe_reported": d["base"].get("roe_reported"), "ev": None}
    return {"mode": "bank", "input": d, "snapshot": snap, "reverse": reverse(d), "scenarios": scenarios(d),
            "twin": twin(d), "temperature": temperature(d, band_fn, min_hist, nifty_bands), "stress": stress(d),
            "sensitivity": sensitivity(d), "version": VERSION}


# ----------------------------------------------------------------------------- markdown

def render(res, heading_level, pct, num, mult, coe_range):
    d, H, h = res["input"], "#" * heading_level, "#" * (heading_level + 1)
    s, rv, sc, tp = res["snapshot"], res["reverse"], res["scenarios"], res["temperature"]
    L = ["%s Valuation worksheet (bank mode): %s (%s) · as of %s" % (H, d.get("company"), d.get("ticker"), d.get("as_of")), ""]
    if d.get("practice"):
        L += ["> **TEST MATERIAL. No verdict.** Inputs exist to exercise the template (lesson L9). Scenario ROEs and "
              "exit P/Bs are illustrative [EST]. Research, not SEBI-registered advice.", ""]
    L += ["*Worksheet v%s. Money in %s. Cost of equity %s (market default %s), terminal growth %s, %d-year explicit "
          "period, payout %s. Book is fully diluted for pending issues.*" % (res["version"], d.get("units"), pct(d["coe"]),
                                                                            coe_range, pct(d["terminal_growth"]), d["years"],
                                                                            pct(d["payout"], 0)), ""]
    for w in d.get("_warnings", []):
        L.append("> Note: %s" % w)
    L += ["", "%s Snapshot" % h,
          "| Price | Mcap (diluted) | BVPS undiluted → diluted | P/B undiluted → diluted | P/E | ROE (reported) |",
          "|---|---|---|---|---|---|",
          "| %s | %s | %s → %s | %s → %s | %s | %s |" % (num(d["price"], 2), num(s["mcap_diluted"], 0), num(s["bvps_undiluted"], 2),
                                                     num(s["bvps"], 2), mult(s["pb_undiluted"]), mult(s["pb"]), num(s["pe"]),
                                                     pct(s["roe_reported"])), ""]
    L += ["%s (a) Reverse P/B: what today's price needs" % h, "| Question | Answer |", "|---|---|",
          "| ROE needed forever (Gordon: g + P/B × (CoE − g)) | **%s** |" % pct(rv["roe_implied_gordon"]),
          "| ROE needed for %d years, then only CoE (no franchise value left) | %s |" % (d["years"], pct(rv["roe_implied_10y_then_coe"])),
          "| Cost of equity the market is using if today's ROE (%s on diluted book) is permanent | **%s** (ours %s) |"
          % (pct(rv["roe_now"]), pct(rv["coe_implied_at_current_roe"]), pct(d["coe"])),
          "| Justified P/B on the base case's long-run ROE %s | %s |" % (pct(d["base_case"]["roe_end"]), mult(rv["justified_pb_base"])),
          "| IRR the price offers if the base case happens | **%s** (hurdle %s) |" % (pct(rv["irr_base"]), pct(d["hurdle_cagr"])),
          ""]
    L += ["%s (b) Residual-income scenarios" % h,
          "| Scenario | Prob | ROE start → end | RIM value | vs price | BVPS yr 5 | Exit P/B used | RIM-consistent P/B yr 5 | 5-yr multiple |",
          "|---|---|---|---|---|---|---|---|---|"]
    gap = []
    for x in sc["scenarios"]:
        L.append("| %s | %s | %s → %s | %s | %s | %s | %s | %s | %s |" % (
            x["name"], pct(x["prob"], 0), pct(x["roe_start"]), pct(x["roe_end"]), num(x["value_ps"], 1),
            pct(x["value_vs_price"], 0), num(x["bvps5"], 1), mult(x["exit_pb"]), mult(x["rim_pb5"]), mult(x["mult5"])))
        if x["exit_pb"] and x["rim_pb5"] and x["exit_pb"] > 1.3 * x["rim_pb5"]:
            gap.append(x["name"])
    bl = sc["blowup"]
    L.append("| blow-up | %s | — | — | — | — | — | — | %s |" % (pct(bl["prob"], 0), mult(bl["multiple"])))
    L.append("")
    if gap:
        L += ["> **Exit-multiple gap:** in %s the exit P/B is >1.3× what the residual-income path justifies at our CoE. "
              "That part of the return is a bet on the market paying up (L21)." % ", ".join(gap), ""]
    if sc.get("ev_mult5") is not None:
        L += ["| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV multiple (CAGR) | Median | Hurdle | Prob-weighted RIM value |",
              "|---|---|---|---|---|---|---|---|---|",
              "| %s | %s | %s | %s | %s | %s (%s) | %s | %s | %s (%s) |" % (
                  pct(sc["p_ge_2x"], 0), pct(sc["p_ge_3x"], 0), pct(sc["p_ge_5x"], 0), pct(sc["p_le_half"], 0),
                  pct(sc["p_blowup"], 0), mult(sc["ev_mult5"]), pct(sc["ev_cagr5"]), mult(sc["median_mult5"]),
                  mult(sc["hurdle_mult5"]), num(sc["pw_value"], 1), pct(sc["pw_vs_price"], 0)), ""]
    tw = res["twin"]
    L += ["%s (c) Twin engine on book: BVPS CAGR needed (5 yrs, ignoring dividends) from P/B %s" % (h, mult(tw["pb0"])),
          "| Target | " + " | ".join("exit P/B %s" % mult(e) for e in tw["exit_pbs"]) + " |",
          "|---|" + "---|" * len(tw["exit_pbs"])]
    for r in tw["table"]:
        L.append("| %dx | %s |" % (r["target"], " | ".join("%s (re-rating %s)" % (pct(c["bv_cagr"], 0), pct(c["rerating_share"], 0))
                                                         for c in r["cells"])))
    L.append("")
    r0 = tp["rows"][0]
    L += ["%s (d) Temperature" % h, "| Basis | Value | Own median (n) | vs own | Own band | Sector median | vs sector | Sector band |",
          "|---|---|---|---|---|---|---|---|",
          "| %s | %s | %s (%d) | %s | %s | %s | %s | %s |" % (r0["basis"], mult(r0["pb"]), mult(tp["own_median"]), tp["n_hist"],
                                                        mult(r0.get("vs_own")), r0["own_band"], mult(tp["sector_median"]),
                                                        mult(r0.get("vs_sector")), r0.get("sector_band", "n/a"))]
    if tp.get("market"):
        L.append("")
        L.append("Market: %s P/E %s (%s): %s" % (tp["market"]["index"], num(tp["market"]["pe"]), tp["market"]["as_of"], tp["market"]["note"]))
    L.append("")
    st = res.get("stress")
    if st:
        L += ["%s (e) Book-value stress (lender-specific)" % h,
              "Leverage (assets ÷ diluted book): %s. Net NPA as %% of book: %s." % (mult(st["leverage"]), pct(st["net_npa_pct_book"])), "",
              "| Extra loss on loans | Post-tax hit | % of book | BVPS after |", "|---|---|---|---|"]
        for r in st["rows"]:
            L.append("| %s | %s | %s | %s |" % (pct(r["loss_rate"], 0), num(r["post_tax_loss"], 0), pct(r["pct_of_book"], 0), num(r["bvps_after"], 1)))
        L.append("")
    se = res["sensitivity"]
    L += ["%s (f) Sensitivity: RIM value per share, CoE (rows) × long-run ROE (columns)" % h, "",
          "| CoE \\ ROE | " + " | ".join(pct(c) for c in se["coe_x_roe"]["cols"]) + " |", "|---|" + "---|" * 5]
    for r, row in se["coe_x_roe"]["rows"]:
        L.append("| %s | %s |" % (pct(r), " | ".join("n/a" if v is None else "%s (%s)" % (num(v, 0), pct(v / d["price"] - 1, 0)) for v in row)))
    L += ["", "Justified P/B (same grid): " + "; ".join("CoE %s: %s" % (pct(r), ", ".join(mult(v) for v in row))
                                                         for r, row in se["justified_pb"]["rows"]), ""]
    if d.get("notes"):
        L.append("%s Input notes" % h)
        L += ["- %s" % n for n in d["notes"]]
        L.append("")
    if d.get("sources"):
        L += ["Sources: " + "; ".join(d["sources"]), ""]
    return "\n".join(L)
