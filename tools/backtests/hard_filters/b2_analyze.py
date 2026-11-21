#!/usr/bin/env python3
"""Part B: mechanical hard-filter snapshot of the 580-company PEAD sample at 30-Sep-2020, then forward
price outcomes of flagged vs unflagged firms.

  python3 b2_analyze.py PEAD_DIR HF_DIR OUT_JSON

PEAD_DIR: results/<SYM>.json (status ok = universe) and prices/<SYM>.json (Yahoo v8, cached by s2_prices.py)
HF_DIR:   screener/<SYM>.html [+ <SYM>_sa.html], shp/<SYM>.json, ann/<SYM>.json   (from b1_fetch.py)

Snapshot T0 = 2020-09-30. Fundamentals: fiscal years FY2016-FY2020 (FY2020 annual report public by T0).
Basis: consolidated page if it has >= 3 of those years, else standalone. Pledge: BSE SHP for Mar-2020
(filed Apr-May 2020; Dec-2019 if Mar-2020 missing). Auditor: NSE announcements 01-Jan-2015..30-Sep-2020.
Price at T0 = adjusted close on the first trading day on/after T0. Outcomes:
  5y  = adj close on first trading day on/after 2025-09-30 (or the last close if the series ends earlier)
  now = last adj close in the cache (2026-11-18)
Classes: loss50 = ratio < 0.5 ; x3 = ratio > 3.
Rules (pre-registered in research_notes/Backtests/hard_filters_test.md before outcomes were computed):
  R1 cash      : sum CFO / sum PAT (5y) < 0.3, PAT sum > 0, non-lender
  R1b cash-soft: same < 0.7
  R2 pledge    : promoter pledge > 25% of promoter holding (R2b: > 50%)
  R3 auditor   : any statutory-auditor resignation announced before T0 (branch/internal/secretarial/cost excluded)
  R4 debt+neg CFO: borrowings FY20 >= 1.5x FY17 and sum CFO FY18-20 < 0, non-lender
  R5 other income: other income / PBT (FY18-20 sums) > 30%, PBT > 0, non-lender
  ANY_HARD = R1 or R2 or R3 or R4 (mechanical stand-ins for the hard set); R5 reported separately."""
import datetime as dt, glob, json, math, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hfcommon as hc   # noqa: E402

PEAD, HF, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
T0, T5 = dt.date(2020, 9, 30), dt.date(2025, 9, 30)
AUD_EXCL = re.compile(r"internal audit|secretarial audit|cost audit|tax audit|branch audit", re.I)


def prices(sym):
    p = os.path.join(PEAD, "prices", sym + ".json")
    if not os.path.exists(p):
        return None
    j = json.load(open(p))
    try:
        r = j["chart"]["result"][0]
        ts = r["timestamp"]
        adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose") or r["indicators"]["quote"][0]["close"]
    except Exception:
        return None
    out = [(dt.datetime.fromtimestamp(t + 19800, dt.timezone.utc).date(), c) for t, c in zip(ts, adj) if c]
    return out or None


def splits_after(sym, d):
    """product of split/bonus ratios dated after d (Yahoo closes are split-adjusted)."""
    j = json.load(open(os.path.join(PEAD, "prices", sym + ".json")))
    f = 1.0
    for v in ((j["chart"]["result"][0].get("events") or {}).get("splits") or {}).values():
        if dt.datetime.fromtimestamp(v["date"], dt.timezone.utc).date() > d and v.get("denominator"):
            f *= v["numerator"] / v["denominator"]
    return f


def px_on_after(ser, d):
    for day, c in ser:
        if day >= d:
            return day, c
    return None


def lender_page(path):
    t = open(path, errors="replace").read()
    return "Financing Profit" in t or "Financing Margin" in t


univ = []
for fn in sorted(glob.glob(os.path.join(PEAD, "results", "*.json"))):
    j = json.load(open(fn))
    if j.get("status") == "ok":
        univ.append(j["symbol"])

rows, funnel = [], {"universe": len(univ)}
for s in univ:
    r = {"sym": s}
    ser = prices(s)
    a = px_on_after(ser, T0) if ser else None
    if not a or (a[0] - T0).days > 10:
        r["status"] = "no_price_at_T0"; rows.append(r); continue
    r["p0"], r["d0"] = a[1], a[0].isoformat()
    b = px_on_after(ser, T5)
    last = ser[-1]
    r["truncated"] = last[0] < dt.date(2026, 11, 1)
    r["r5"] = (b[1] if b else last[1]) / a[1]
    r["rnow"] = last[1] / a[1]
    r["d_last"] = last[0].isoformat()
    # fundamentals
    best = None
    for k in (s, s + "_sa"):
        p = os.path.join(HF, "screener", k + ".html")
        if not os.path.exists(p):
            continue
        sc = hc.parse_screener(p)
        m = hc.metrics_at(sc["FY"], 2020)
        # require the window to reach FY2019 at least (FY2020 preferred)
        if m.get("n_years", 0) >= 3 and m.get("last_fy", 0) >= 2019 and (best is None or m["n_years"] > best[0]["n_years"]):
            best = (m, sc["basis"], lender_page(p))
    if best:
        m, basis, lender = best
        r.update({"basis": basis, "lender": lender, "m": m})
        mr = hc.rules(m, lender=lender)
        r["R1"] = mr["F1b_cfo_pat_lt_0.3"]
        r["R1b"] = mr["F1_cfo_pat_lt_0.7"]
        r["R4"] = mr["G2_debt_up_neg_cfo"]
        r["R5"] = mr["F2_other_income"]
    else:
        r.update({"basis": None, "lender": None, "R1": None, "R1b": None, "R4": None, "R5": None})
    # pledge
    sp = os.path.join(HF, "shp", s + ".json")
    r["R2"] = r["R2b"] = None
    if os.path.exists(sp):
        j = json.load(open(sp))
        q = (j.get("q") or {}).get("March 2020") or {}
        vals = q.get("vals") or {}
        tot = vals.get("NumberOfShares|ShareholdingPattern")
        prom = vals.get("NumberOfShares|ShareholdingOfPromoterAndPromoterGroup")
        pct = vals.get("PledgedOrEncumberedSharesHeldAsPercentageOfTotalNumberOfShares|ShareholdingOfPromoterAndPromoterGroup")
        if q.get("status") == "ok" or tot:
            if pct is None:
                pct = 0.0 if (prom or tot) else None
            if tot:
                raw = None
                rq = json.load(open(os.path.join(PEAD, "prices", s + ".json")))["chart"]["result"][0]
                for t, c in zip(rq["timestamp"], rq["indicators"]["quote"][0]["close"]):
                    if c and dt.datetime.fromtimestamp(t + 19800, dt.timezone.utc).date() >= T0:
                        raw = c; break
                if raw:
                    r["mcap0_cr"] = round(raw * splits_after(s, T0) * tot / 1e7, 1)
            if pct is not None:
                r["pledge_pct"] = pct
                r["R2"], r["R2b"] = pct > 25, pct > 50
                r["promoter_pct"] = round(100 * prom / tot, 1) if prom and tot else 0.0
    # auditor
    ap = os.path.join(HF, "ann", s + ".json")
    r["R3"] = None
    if os.path.exists(ap):
        j = json.load(open(ap))
        if j.get("n_rows", 0) > 0:
            hits = []
            for d, desc, t in j["auditor_rows"]:
                x = (desc or "") + " " + (t or "")
                if re.search(r"resign", x, re.I) and re.search(r"auditor", x, re.I) and not AUD_EXCL.search(x):
                    when = dt.datetime.strptime(d.split()[0], "%d-%b-%Y").date()
                    if when <= T0:
                        hits.append([when.isoformat(), x[:160]])
            r["R3"] = bool(hits)
            r["R3_hits"] = hits[:3]
    flags = [r.get(k) for k in ("R1", "R2", "R3", "R4")]
    r["ANY"] = True if True in flags else (None if None in flags else False)
    r["ANY_known"] = True in flags          # fired on available data (unknown parts treated as not fired)
    r["status"] = "ok"
    rows.append(r)

ok = [r for r in rows if r.get("status") == "ok"]
funnel["price_at_T0"] = len(ok)
funnel["no_price_at_T0 (listed after T0 or gaps)"] = sum(r.get("status") == "no_price_at_T0" for r in rows)
funnel["truncated_series (stopped trading before Nov-2026)"] = sum(r.get("truncated") for r in ok)
funnel["with_fundamentals"] = sum(r.get("basis") is not None for r in ok)
funnel["lenders"] = sum(bool(r.get("lender")) for r in ok)
funnel["with_pledge"] = sum(r.get("R2") is not None for r in ok)
funnel["with_auditor_feed"] = sum(r.get("R3") is not None for r in ok)


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (round(c - h, 3), round(c + h, 3))


def fisher_two_sided(a, b, c, d):
    """2x2 [[a,b],[c,d]]: a = flagged&event, b = flagged&no-event, c = unflagged&event, d = unflagged&no."""
    n1, n2, m1, N = a + b, c + d, a + c, a + b + c + d
    def lp(x):
        return (math.lgamma(m1 + 1) - math.lgamma(x + 1) - math.lgamma(m1 - x + 1) +
                math.lgamma(N - m1 + 1) - math.lgamma(n1 - x + 1) - math.lgamma(N - m1 - n1 + x + 1) -
                (math.lgamma(N + 1) - math.lgamma(n1 + 1) - math.lgamma(N - n1 + 1)))
    lo, hi = max(0, m1 - n2), min(n1, m1)
    p0 = lp(a)
    return round(min(1.0, sum(math.exp(lp(x)) for x in range(lo, hi + 1) if lp(x) <= p0 + 1e-9)), 4)


def table(rule, horizon):
    known = [r for r in ok if r.get(rule) is not None]
    res = {"n_known": len(known), "n_unknown": len(ok) - len(known)}
    f = [r for r in known if r[rule]]
    u = [r for r in known if not r[rule]]
    res["n_flagged"], res["n_unflagged"] = len(f), len(u)
    for cls, test in (("loss50", lambda x: x < 0.5), ("x3", lambda x: x > 3)):
        kf = sum(test(r[horizon]) for r in f)
        ku = sum(test(r[horizon]) for r in u)
        kb = sum(test(r[horizon]) for r in known)
        res[cls] = {"flagged": [kf, len(f), round(kf / len(f), 3) if f else None, wilson(kf, len(f))],
                    "unflagged": [ku, len(u), round(ku / len(u), 3) if u else None, wilson(ku, len(u))],
                    "base_rate_known": [kb, len(known), round(kb / len(known), 3) if known else None],
                    "fisher_p": fisher_two_sided(kf, len(f) - kf, ku, len(u) - ku) if f and u else None,
                    "lift": round((kf / len(f)) / (kb / len(known)), 2) if f and kb else None}
    med = lambda xs: sorted(xs)[len(xs) // 2] if xs else None
    res["median_ratio"] = {"flagged": med([r[horizon] for r in f]), "unflagged": med([r[horizon] for r in u])}
    return res


out = {"T0": T0.isoformat(), "T5": T5.isoformat(), "funnel": funnel, "base_rates": {}, "rules": {}}
for h in ("r5", "rnow"):
    xs = [r[h] for r in ok]
    out["base_rates"][h] = {"n": len(xs), "loss50": round(sum(x < 0.5 for x in xs) / len(xs), 3),
                            "x3": round(sum(x > 3 for x in xs) / len(xs), 3),
                            "median": round(sorted(xs)[len(xs) // 2], 3)}
    for rule in ("R1", "R1b", "R2", "R2b", "R3", "R4", "R5", "ANY_known"):
        out["rules"].setdefault(rule, {})[h] = table(rule, h)
# overlap of flags + list of flagged names
# sensitivity: only firms already >= Rs 400 cr at T0 (removes the 'must later grow into the Rs 400 cr range'
# selection that the PEAD sample imposed), and the complement
big = [r for r in ok if (r.get("mcap0_cr") or 0) >= 400]
small = [r for r in ok if r.get("mcap0_cr") is not None and r["mcap0_cr"] < 400]
out["mcap_split"] = {"n_ge400": len(big), "n_lt400": len(small), "n_no_mcap": sum(r.get("mcap0_cr") is None for r in ok)}
for name, sub in (("mcap_ge400", big), ("mcap_lt400", small)):
    okk = ok
    ok = sub
    xs = [r["r5"] for r in sub]
    out["base_rates"][name] = {"n": len(xs), "loss50": round(sum(x < 0.5 for x in xs) / len(xs), 3) if xs else None,
                               "x3": round(sum(x > 3 for x in xs) / len(xs), 3) if xs else None}
    for rule in ("R1", "R1b", "R2", "R2b", "R3", "R4", "R5", "ANY_known"):
        out["rules"][rule][name] = table(rule, "r5")
    ok = okk
out["flagged_names"] = {rule: sorted([(r["sym"], round(r["r5"], 2)) for r in ok if r.get(rule)], key=lambda x: x[1])
                        for rule in ("R1", "R2", "R2b", "R3", "R4", "R5")}
out["rows"] = rows
json.dump(out, open(OUT, "w"), indent=1, default=str)
print(json.dumps(out["funnel"], indent=0))
print("base", out["base_rates"])
for rule, v in [(k + "|" + h, x[h]) for k, x in out["rules"].items() for h in ("r5", "rnow", "mcap_ge400")]:
    t = v
    print("%-9s n_known %3d flagged %3d | loss50 %s vs unflagged %s p=%s | x3 %s vs %s p=%s | med %s/%s" % (
        rule, t["n_known"], t["n_flagged"], t["loss50"]["flagged"][:3], t["loss50"]["unflagged"][2], t["loss50"]["fisher_p"],
        t["x3"]["flagged"][:3], t["x3"]["unflagged"][2], t["x3"]["fisher_p"],
        t["median_ratio"]["flagged"] and round(t["median_ratio"]["flagged"], 2), t["median_ratio"]["unflagged"] and round(t["median_ratio"]["unflagged"], 2)))
