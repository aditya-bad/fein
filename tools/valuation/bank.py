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

v1.2 (2026-11-25, UTKARSHBNK live dive #5, lesson L41) - all optional, old inputs give identical results:
  * `cet1_book` (per share, current undiluted shares; = CET1 capital from Pillar 3 DF-11, i.e. net worth less DTA,
    intangibles and other regulatory deductions) shown SIDE BY SIDE with reported book: P/CET1, the ROE required on
    CET1 book, and every scenario's 5-year multiple when the exit P/B is applied to CET1 book (per-scenario
    `exit_p_cet1`, else the same exit P/B - harsh, flagged). The deduction gap per share is held constant (optional
    `cet1_gap_runoff_years`: falls linearly to 0, e.g. DTA used up). The RIM value itself does not depend on the book
    measure when earnings are unchanged (clean surplus); a bound 'value if the deductions are worth nothing' is shown.
    `book_basis: "cet1"` makes the CET1 multiples the primary outputs (what the decision card reads).
  * Scenario-only dilution: a `dilution` entry with `"scenarios": ["bear"]` (and `"year": k`, default 1; `shares`, or
    `cash_in` + `issue_price`) is applied only in those scenarios, at the end of year k, per existing share
    (BVPS -> (BVPS + cash per share) / (1 + new-share fraction)); the book change is a dirty-surplus item that the
    per-share RIM value includes. Entries without `scenarios` keep the old up-front treatment.
  * Non-linear ROE path per case: `roe_path` = {"shape": "j", "trough": -0.04, "trough_year": 2, "recover_by": 6,
    "power": 0.6} (linear from roe_start to the trough, then trough + (roe_end - trough) x x^power, x = share of the
    recovery period elapsed; power < 1 = fast early recovery, > 1 = slow start), or an explicit list of yearly ROEs
    (later years interpolate linearly to roe_end). The terminal ROE is always roe_end.
Same result keys as worksheet.run() (snapshot, reverse, scenarios, twin, temperature, sensitivity), so
tools/decision/decision_card.py works unchanged except for its stage-5 text block. Standard library only.
"""
import math

VERSION = "1.2-bank (2026-11-25; CET1 book side by side, scenario-only dilution, J-curve ROE path)"

TEMPLATE = {
    "mode": "bank",
    "company": "Bank name", "ticker": "TICKER", "market": "india", "practice": True,
    "currency": "INR", "units": "INR cr", "as_of": "2026-11-21", "price": 100.0,
    "shares": 100.0, "# shares": "crore, same scale as money units",
    "book_value": 10000.0, "# book_value": "net worth (equity + reserves), INR cr, at the latest balance sheet",
    "book_adjustments": [{"name": "share warrant money already in reserves", "amount": 0.0}],
    "dilution": [{"name": "warrants", "shares": 0.0, "cash_in": 0.0, "# cash_in": "cash still to be received"},
                 {"name": "bear-case raise (optional)", "scenarios": ["bear"], "year": 2, "cash_in": 0.0,
                  "issue_price": 80.0, "# scenarios": "only these cases; omit the key for an up-front issue"}],
    "cet1_book": None, "# cet1_book": "optional, per share: CET1 capital (Pillar 3 DF-11) / shares",
    "cet1_gap_runoff_years": None, "book_basis": "reported",
    "base": {"fy": "TTM", "pat": 1200.0, "pat_normalised": None, "roe_reported": 0.12, "dps": 1.0,
             "pe_trailing": None, "loans": 80000.0, "assets": 120000.0, "net_npa": 300.0, "cet1": 0.15},
    "coe": None, "terminal_growth": None, "hurdle_cagr": None, "years": 10, "dispersion": 0.30,
    "payout": 0.10,
    "base_case": {"roe_start": 0.13, "roe_end": 0.14, "exit_pb": 2.0},
    "scenarios": [
        {"name": "bear", "prob": 0.30, "roe_start": 0.11, "roe_end": 0.11, "exit_pb": 1.2,
         "roe_path": {"shape": "j", "trough": 0.02, "trough_year": 2, "recover_by": 6, "power": 1.0},
         "exit_p_cet1": None},
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
    upfront, later = [], []
    for x in d.get("dilution") or []:
        x = dict(x)
        x["cash_in"] = _f(x.get("cash_in"), "dilution.cash_in", 0.0)
        sh = _f(x.get("shares"), "dilution.shares")
        ip = _f(x.get("issue_price"), "dilution.issue_price")
        if sh is None:
            sh = x["cash_in"] / ip if ip else 0.0
        x["shares"] = sh
        (later if x.get("scenarios") else upfront).append(x)
    dil_sh = sum(x["shares"] for x in upfront)
    dil_cash = sum(x["cash_in"] for x in upfront)
    d["_book_undiluted"] = d["book_value"] - adj
    d["_shares_diluted"] = d["shares"] + dil_sh
    d["_book_diluted"] = d["book_value"] + dil_cash          # warrant money already received stays in book
    d["_bvps_undiluted"] = d["_book_undiluted"] / d["shares"]
    d["_bvps"] = d["_book_diluted"] / d["_shares_diluted"]
    if dil_sh:
        warn.append("fully diluted: +%.2f cr shares, +%.0f cash to be received; BVPS %.2f -> %.2f"
                    % (dil_sh, dil_cash, d["_bvps_undiluted"], d["_bvps"]))
    # v1.2 CET1 book (per share, undiluted) -> diluted CET1 BVPS; the gap to reported book is the deduction per share
    c1 = _f(d.get("cet1_book"), "cet1_book")
    if c1 is not None:
        if c1 <= 0:
            raise ValueError("cet1_book must be positive (per share)")
        d["_cet1_bvps_undiluted"] = c1
        d["_cet1_bvps"] = (c1 * d["shares"] + dil_cash) / d["_shares_diluted"]
        d["_cet1_gap"] = d["_bvps"] - d["_cet1_bvps"]
        if d["_cet1_gap"] < 0:
            warn.append("cet1_book is above reported book (gap %.2f/share): check the input" % d["_cet1_gap"])
    else:
        d["_cet1_bvps"] = d["_cet1_gap"] = None
    ro = _f(d.get("cet1_gap_runoff_years"), "cet1_gap_runoff_years")
    d["cet1_gap_runoff_years"] = int(ro) if ro else None
    d["book_basis"] = str(d.get("book_basis") or "reported").lower()
    if d["book_basis"] not in ("reported", "cet1"):
        raise ValueError("book_basis must be 'reported' or 'cet1'")
    if d["book_basis"] == "cet1" and c1 is None:
        raise ValueError("book_basis 'cet1' needs cet1_book")
    d["_later_dilution"] = later
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
        c["roe_path"] = _norm_path(c.get("roe_path"), c["name"])
        epc = c.get("exit_p_cet1")
        c["exit_p_cet1"] = "rim" if isinstance(epc, str) and epc.lower() in ("rim", "dcf") else _f(epc, "exit_p_cet1")
        c["raises"] = [{"name": x.get("name", "raise"), "year": int(_f(x.get("year"), "dilution.year", 1)),
                        "shares": x["shares"], "cash_in": x["cash_in"]}
                       for x in later if c["name"] in x["scenarios"]]
        return c
    bc = d.get("base_case") or next((s for s in d.get("scenarios") or [] if s.get("name") == "base"), None)
    if not bc:
        raise ValueError("give base_case or a scenario named 'base'")
    d["base_case"] = fill(bc)
    d["scenarios"] = [fill(s) for s in d.get("scenarios") or []]
    names = {s["name"] for s in d["scenarios"]} | {d["base_case"]["name"]}
    for x in later:
        if not set(x["scenarios"]) & names:
            warn.append("dilution %r names no existing scenario (%s): ignored" % (x.get("name"), x["scenarios"]))
        for r in d["scenarios"] + [d["base_case"]]:
            for z in r["raises"]:
                if not 1 <= z["year"] <= d["years"]:
                    raise ValueError("dilution year must be 1..years")
    if later:
        warn.append("scenario-only dilution: " + "; ".join("%s in %s (yr %d, +%.2f cr shares, +%.0f cash)" % (
            x.get("name"), "/".join(x["scenarios"]), int(_f(x.get("year"), "year", 1)), x["shares"], x["cash_in"])
            for x in later))
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


def _norm_path(p, name):
    """None (linear) | {"shape": "j", ...} | [yearly ROEs]. Validated here, evaluated in roe_series()."""
    if p in (None, "", "linear") or (isinstance(p, dict) and str(p.get("shape", "linear")).lower() == "linear"):
        return None
    if isinstance(p, list):
        if not p:
            return None
        return [_f(x, "roe_path[]") for x in p]
    if isinstance(p, dict) and str(p.get("shape")).lower() in ("j", "j-curve", "jcurve"):
        q = {"shape": "j", "trough": _f(p.get("trough"), "roe_path.trough"),
             "trough_year": int(_f(p.get("trough_year"), "roe_path.trough_year", 1)),
             "recover_by": int(_f(p.get("recover_by"), "roe_path.recover_by", 5)),
             "power": _f(p.get("power"), "roe_path.power", 1.0)}
        if q["trough"] is None:
            raise ValueError("case %s: J-curve roe_path needs 'trough'" % name)
        if not (1 <= q["trough_year"] < q["recover_by"]) or q["power"] <= 0:
            raise ValueError("case %s: J-curve needs 1 <= trough_year < recover_by and power > 0" % name)
        return q
    raise ValueError("case %s: roe_path must be a list, 'linear' or {'shape': 'j', ...}" % name)


def roe_series(roe_start, roe_end, n, path=None):
    """Yearly ROE for t = 1..n. Default: linear roe_start -> roe_end (v1.1 behaviour)."""
    if path is None:
        return [roe_start + (roe_end - roe_start) * (t - 1) / max(n - 1, 1) for t in range(1, n + 1)]
    if isinstance(path, list):
        k = len(path)
        out = list(path[:n])
        for t in range(k + 1, n + 1):          # interpolate from the last listed value to roe_end at year n
            out.append(path[-1] + (roe_end - path[-1]) * (t - k) / (n - k))
        return out
    ty, rb, tr, pw = path["trough_year"], min(path["recover_by"], n), path["trough"], path["power"]
    out = []
    for t in range(1, n + 1):
        if t <= ty:
            out.append(roe_start + (tr - roe_start) * ((t - 1) / (ty - 1) if ty > 1 else 1.0))
        elif t < rb:
            out.append(tr + (roe_end - tr) * ((t - ty) / (rb - ty)) ** pw)
        else:
            out.append(roe_end)
    return out


# ----------------------------------------------------------------------------- model

def project(d, roe_start, roe_end, payout=None, coe=None, tg=None, years=None, path=None, raises=None):
    """Per-share residual-income projection. `raises` (v1.2): scenario-only equity issues at the end of year k;
    per existing share the book becomes (BVPS + cash per share) / (1 + new-share fraction). The change is a
    dirty-surplus item that enters the per-share value (V0 = B0 + sum PV(EPS - r B_(t-1) + dirty_t) + TV)."""
    r = d["coe"] if coe is None else coe
    g = d["terminal_growth"] if tg is None else tg
    n = d["years"] if years is None else years
    po = d["payout"] if payout is None else payout
    b = d["_bvps"]
    s0 = d["_shares_diluted"]
    m = 1.0                                  # shares outstanding / shares at t=0 (after up-front dilution)
    gap = d.get("_cet1_gap")
    ro = d.get("cet1_gap_runoff_years")
    roes = roe_series(roe_start, roe_end, n, path)
    by_year = {}
    for z in raises or []:
        by_year.setdefault(z["year"], []).append(z)
    rows, pv_ri, cum_div5, pv_dirty = [], 0.0, 0.0, 0.0
    for t in range(1, n + 1):
        roe = roes[t - 1]
        eps = roe * b
        div = eps * po
        ri = (roe - r) * b
        pv_ri += ri / (1 + r) ** t
        b_next = b + eps - div
        dirty, frac = 0.0, 0.0
        for z in by_year.get(t, []):
            cur = s0 * m
            frac = z["shares"] / cur
            b_new = (b_next + z["cash_in"] / cur) / (1 + frac)
            dirty += b_new - b_next
            b_next = b_new
            m *= 1 + frac
            if gap is not None:
                gap /= (1 + frac)
        pv_dirty += dirty / (1 + r) ** t
        if gap is not None and ro:
            gap = max(gap - d["_cet1_gap"] / ro / m, 0.0)
        if t <= 5:
            cum_div5 += div
        rows.append({"t": t, "roe": roe, "bvps_open": b, "eps": eps, "dps": div, "ri": ri, "bvps": b_next,
                     "dirty": dirty, "share_mult": m, "cet1_bvps": (b_next - gap) if gap is not None else None})
        b = b_next
    tv = (roe_end - r) * b / (r - g) / (1 + r) ** n
    value = d["_bvps"] + pv_ri + pv_dirty + tv
    # RIM-consistent P/B at year 5: value of the remaining path at t=5 / BVPS_5
    b5 = rows[4]["bvps"]
    rem = sum((rw["ri"] + rw["dirty"]) / (1 + r) ** (rw["t"] - 5) for rw in rows[5:]) + \
        (roe_end - r) * b / (r - g) / (1 + r) ** (n - 5)
    out = {"rows": rows, "value_ps": value, "pv_ri": pv_ri, "pv_dirty": pv_dirty, "tv": tv,
           "tv_share": tv / value if value else None,
           "bvps5": b5, "eps5": rows[4]["eps"], "cum_div5": cum_div5, "rim_pb5": (b5 + rem) / b5,
           "justified_pb_terminal": (roe_end - g) / (r - g), "share_mult5": rows[4]["share_mult"]}
    if gap is not None:
        c5 = rows[4]["cet1_bvps"]
        out.update(cet1_bvps5=c5, rim_p_cet1_5=(b5 + rem) / c5 if c5 and c5 > 0 else None)
    return out


def _case_project(d, c, **kw):
    return project(d, c["roe_start"], c["roe_end"], c["payout"], path=c.get("roe_path"), raises=c.get("raises"), **kw)


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
        out["irr_base"] = _solve(lambda rr: _case_project(d, bc, coe=rr)["value_ps"]
                                 if rr > d["terminal_growth"] + 0.002 else 1e9,
                                 d["terminal_growth"] + 0.003, 0.6, d["price"])
    except ZeroDivisionError:
        out["irr_base"] = None
    out["justified_pb_base"] = (bc["roe_end"] - g) / (r - g)
    out["base"] = _case_project(d, bc)
    if d.get("_cet1_bvps"):                 # v1.2: the same questions on CET1 book (side by side)
        pc = d["price"] / d["_cet1_bvps"]
        out["p_cet1"] = pc
        out["roe_implied_gordon_cet1"] = g + pc * (r - g)
        out["roe_now_cet1"] = (roe_now * d["_bvps"] / d["_cet1_bvps"]) if roe_now is not None else None
        out["coe_implied_at_current_roe_cet1"] = g + (out["roe_now_cet1"] - g) / pc if roe_now is not None else None
        out["justified_p_cet1_base"] = (bc["roe_end"] * d["_bvps"] / d["_cet1_bvps"] - g) / (r - g)
    return out


def norm_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def _dist(res, key, bl, sig, hurdle):
    """Lognormal mixture over scenario multiples `key` plus the blow-up point mass."""
    if not res or not all(x.get(key) and x[key] > 0 for x in res):
        return {}

    def p_ge(k):
        return sum(x["prob"] * (1 - norm_cdf((math.log(k) - math.log(x[key])) / sig)) for x in res) + \
            (bl["prob"] if bl["multiple"] >= k else 0.0)

    def p_le(k):
        return sum(x["prob"] * norm_cdf((math.log(k) - math.log(x[key])) / sig) for x in res) + \
            (bl["prob"] if bl["multiple"] <= k else 0.0)
    out = dict(p_ge_3x=p_ge(3.0), p_ge_2x=p_ge(2.0), p_ge_5x=p_ge(5.0), p_le_half=p_le(0.5), p_blowup=bl["prob"])
    out["ev_mult5"] = sum(x["prob"] * x[key] for x in res) + bl["prob"] * bl["multiple"]
    out["ev_cagr5"] = out["ev_mult5"] ** 0.2 - 1 if out["ev_mult5"] > 0 else -1.0
    lo, hi = 0.01, 50.0
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        lo, hi = (mid, hi) if p_le(mid) < 0.5 else (lo, mid)
    out["median_mult5"] = math.sqrt(lo * hi)
    out["hurdle_mult5"] = (1 + hurdle) ** 5
    return out


def scenarios(d):
    price, res = d["price"], []
    has_c1 = bool(d.get("_cet1_bvps"))
    for s in d["scenarios"]:
        p = _case_project(d, s)
        exit_pb = p["rim_pb5"] if s["exit_pb"] == "rim" else s["exit_pb"]
        mult5 = (p["bvps5"] * exit_pb + p["cum_div5"]) / price if exit_pb else None
        row = {"name": s["name"], "prob": s["prob"], "roe_start": s["roe_start"], "roe_end": s["roe_end"],
               "exit_pb": exit_pb, "exit_pb_is_rim": s["exit_pb"] == "rim", "rim_pb5": p["rim_pb5"],
               "value_ps": p["value_ps"], "value_vs_price": p["value_ps"] / price - 1, "bvps5": p["bvps5"],
               "eps5": p["eps5"], "dist_ps_5y": p["cum_div5"], "mult5": mult5, "tv_share": p["tv_share"],
               "exit_pe": None, "dcf_pe5": None, "roe_path": s.get("roe_path"),
               "roe_by_year": [rw["roe"] for rw in p["rows"]], "raises": s.get("raises") or [],
               "share_mult5": p["share_mult5"], "pv_dirty": p["pv_dirty"]}
        if has_c1:
            if s.get("exit_p_cet1") == "rim":
                ec, how = p.get("rim_p_cet1_5"), "rim"
            elif s.get("exit_p_cet1") is not None:
                ec, how = s["exit_p_cet1"], "given"
            else:
                ec, how = exit_pb, "same as exit P/B (harsh)"
            c5 = p.get("cet1_bvps5")
            row.update(cet1_bvps5=c5, exit_p_cet1=ec, exit_p_cet1_how=how, rim_p_cet1_5=p.get("rim_p_cet1_5"),
                       mult5_cet1=(c5 * ec + p["cum_div5"]) / price if (ec and c5 and c5 > 0) else None,
                       value_ps_deductions_worthless=p["value_ps"] - d["_cet1_gap"])
        res.append(row)
    bl = d["blowup"]
    out = {"scenarios": res, "blowup": bl, "book_basis": d.get("book_basis", "reported")}
    if not res:
        return out
    out["pw_value"] = sum(x["prob"] * x["value_ps"] for x in res) + bl["prob"] * bl["multiple"] * price
    out["pw_vs_price"] = out["pw_value"] / price - 1
    worst = min(res, key=lambda x: x["value_ps"])
    out["bear_value"], out["downside_bear"] = worst["value_ps"], worst["value_ps"] / price - 1
    out["p_value_below_price"] = sum(x["prob"] for x in res if x["value_ps"] < price) + bl["prob"]
    sig = d["dispersion"]
    rep_ = _dist(res, "mult5", bl, sig, d["hurdle_cagr"])
    if has_c1:
        c1d = _dist(res, "mult5_cet1", bl, sig, d["hurdle_cagr"])
        out["cet1"] = c1d
        out["pw_value_deductions_worthless"] = out["pw_value"] - sum(x["prob"] for x in res) * d["_cet1_gap"]
        if d.get("book_basis") == "cet1":
            out["reported"] = rep_
            rep_ = c1d
    out.update(rep_)
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
                      project(d, bc["roe_start"], e, bc["payout"], coe=r, path=bc.get("roe_path"),
                              raises=bc.get("raises"))["value_ps"] for e in roes]))
    jp = [(r, [(e - d["terminal_growth"]) / (r - d["terminal_growth"]) for e in roes]) for r in rs]
    return {"coe_x_roe": {"rows": t, "cols": roes}, "justified_pb": {"rows": jp, "cols": roes}}


def run(d, band_fn, min_hist, nifty_bands):
    price = d["price"]
    snap = {"mcap": price * d["shares"], "mcap_diluted": price * d["_shares_diluted"], "pb": price / d["_bvps"],
            "pb_undiluted": price / d["_bvps_undiluted"], "bvps": d["_bvps"], "bvps_undiluted": d["_bvps_undiluted"],
            "pe": d["base"].get("pe_trailing") or (price / d["base"]["eps"] if d["base"]["eps"] else None),
            "roe_reported": d["base"].get("roe_reported"), "ev": None,
            "cet1_bvps": d.get("_cet1_bvps"), "p_cet1": (price / d["_cet1_bvps"]) if d.get("_cet1_bvps") else None,
            "cet1_gap_ps": d.get("_cet1_gap")}
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
    if s.get("cet1_bvps"):
        L += ["**CET1 book (v1.2, L41):** %s per share (diluted; gap to reported book %s/share = DTA, intangibles and other "
              "Pillar 3 deductions) → **P/CET1 %s** vs P/B %s.%s" % (
                  num(s["cet1_bvps"], 2), num(s["cet1_gap_ps"], 2), mult(s["p_cet1"]), mult(s["pb"]),
                  " Primary outputs below use the CET1 basis (book_basis = cet1)." if d.get("book_basis") == "cet1" else
                  " Primary outputs use reported book; CET1 columns are side by side."), ""]
    L += ["%s (a) Reverse P/B: what today's price needs" % h, "| Question | Answer |", "|---|---|",
          "| ROE needed forever (Gordon: g + P/B × (CoE − g)) | **%s** |" % pct(rv["roe_implied_gordon"]),
          "| ROE needed for %d years, then only CoE (no franchise value left) | %s |" % (d["years"], pct(rv["roe_implied_10y_then_coe"])),
          "| Cost of equity the market is using if today's ROE (%s on diluted book) is permanent | **%s** (ours %s) |"
          % (pct(rv["roe_now"]), pct(rv["coe_implied_at_current_roe"]), pct(d["coe"])),
          "| Justified P/B on the base case's long-run ROE %s | %s |" % (pct(d["base_case"]["roe_end"]), mult(rv["justified_pb_base"])),
          "| IRR the price offers if the base case happens | **%s** (hurdle %s) |" % (pct(rv["irr_base"]), pct(d["hurdle_cagr"]))]
    if rv.get("p_cet1"):
        L += ["| ROE needed forever on **CET1 book** (P/CET1 %s) | **%s** |" % (mult(rv["p_cet1"]), pct(rv["roe_implied_gordon_cet1"])),
              "| Today's ROE on CET1 book; CoE the market is using on that basis | %s; %s |"
              % (pct(rv.get("roe_now_cet1")), pct(rv.get("coe_implied_at_current_roe_cet1"))),
              "| Justified P/CET1 on the base case's long-run ROE (scaled to CET1 book) | %s |" % mult(rv.get("justified_p_cet1_base"))]
    L.append("")
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
    extra = []
    for x in sc["scenarios"]:
        if x.get("roe_path") is not None:
            extra.append("- %s ROE path (%s): %s" % (x["name"], "J-curve" if isinstance(x["roe_path"], dict) else "explicit list",
                                                  ", ".join(pct(v) for v in x["roe_by_year"])))
        for z in x.get("raises") or []:
            extra.append("- %s: equity raise %s at end of year %d (+%s cr shares, +%s cash); shares ×%.3f by year 5; "
                         "book change per share (PV) %s" % (x["name"], z["name"], z["year"], num(z["shares"], 2),
                                                            num(z["cash_in"], 0), x["share_mult5"], num(x["pv_dirty"], 2)))
    if extra:
        L += ["Scenario paths and scenario-only dilution (v1.2):"] + extra + [""]
    if sc.get("cet1"):
        L += ["**CET1 basis, side by side** (same earnings; exit multiple applied to CET1 book at year 5):", "",
              "| Scenario | CET1 BVPS yr 5 | Exit P/CET1 (how) | RIM-consistent P/CET1 yr 5 | 5-yr multiple (CET1) | vs reported-basis multiple | RIM value if deductions worth nothing |",
              "|---|---|---|---|---|---|---|"]
        for x in sc["scenarios"]:
            L.append("| %s | %s | %s (%s) | %s | %s | %s | %s |" % (x["name"], num(x.get("cet1_bvps5"), 1), mult(x.get("exit_p_cet1")),
                                                           x.get("exit_p_cet1_how"), mult(x.get("rim_p_cet1_5")),
                                                           mult(x.get("mult5_cet1")), mult(x["mult5"]),
                                                           num(x.get("value_ps_deductions_worthless"), 1)))
        c1 = sc["cet1"]
        if c1:
            alt = sc.get("reported") if sc.get("book_basis") == "cet1" else sc
            L += ["", "| Basis | P(≥3x) | P(≤0.5x) | EV multiple | Median |", "|---|---|---|---|---|",
                  "| reported book | %s | %s | %s | %s |" % (pct(alt.get("p_ge_3x"), 0), pct(alt.get("p_le_half"), 0),
                                                       mult(alt.get("ev_mult5")), mult(alt.get("median_mult5"))),
                  "| CET1 book | %s | %s | %s | %s |" % (pct(c1["p_ge_3x"], 0), pct(c1["p_le_half"], 0),
                                                   mult(c1["ev_mult5"]), mult(c1["median_mult5"]))]
        L += ["", "The RIM value does not change with the book measure when earnings are the same (clean surplus); the "
              "CET1 basis changes the multiple paid, the ROE required and what an exit P/B on honest book returns.", ""]
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
