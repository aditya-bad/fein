#!/usr/bin/env python3
"""5-year base-rate classes for the decision card (roadmap stage 6, feeds stage 7 Brier baselines).

Standard library only. Re-uses the survivorship-free panels already on disk; fetches nothing.

  India: research_notes/Backtests/solvency_india_outputs/panel.csv (stratified frame incl. IBBI/NSE/BSE dead lists,
         stratum weights D 1.0 / X 4.264 / L 5.633; snapshots T = 2016-09-30 and 2018-09-30). The hard-filters v2
         panel (panel_v2.csv) holds the same 489 rows with the same r5/weights (checked below), so it adds no rows.
  US:    research_notes/Backtests/solvency_us_outputs/panel.csv (census of every 10-K filer in the SEC public-float
         frames; snapshots T = 2015-06-30, 2017-06-30, 2019-06-30; EDGAR fates for firms without prices).

Classes
  india_nonfin_1000_20000cr_5y : non-financial, mcap Rs 1,000-20,000 cr at T (panel already excludes financials)
  us_float_500m_10b_5y         : non-financial, non-utility, public float $500M-$10B on the T-10-K cover

Outcome definitions (fixed before looking at the numbers; same as the source tests):
  ge3x   : R5 >= 3 (India: price only; US: adjusted close incl. dividends)
  le_half: R5 <= 0.5, OR no R5 and a failure event (liquidation / delisting for cause / bankruptcy / price collapse)
  fail   : O_fail = liquidation or delisting-for-cause or bankruptcy (US) or a close <= 0.2x the close at T within
           5 years. This is the card's blow-up definition minus fraud findings (the panels have no fraud field).
Missing R5
  India (pre-registered rule of the source test): no R5 and O_fail -> counted (not >=3x, <=0.5x); no R5 and no
        O_fail -> excluded from the two tail rates and counted.
  US: no price history for ~44% of rows. Primary estimate: unpriced + EDGAR failure -> counted as failed/<=0.5x/
        not >=3x; unpriced + acquired / merger evidence -> counted as NEITHER tail (a deal price near market plus a
        premium); other unpriced (alive with ticker/identity problems, stopped filing, exchange transfers) ->
        excluded (missing at random assumption). Bounds: 'acquired excluded' (the priced-or-failed subset) and,
        for <=0.5x, 'stopped-filing counted as <=0.5x'.
CIs: 2,000 bootstrap draws (seed 20261123), resampling companies within stratum (India) or CIKs (US), so a company
that appears in several snapshots is one cluster. Percentile 95% intervals.

Usage: python3 tools/backtests/base_rates_5y/build.py [--draws 2000] [--out research_notes/Backtests/base_rates_5y_outputs/results.json]
"""
import argparse
import csv
import json
import os
import random
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
BT = os.path.join(ROOT, "research_notes", "Backtests")
SEED = 20261123


def _f(x):
    return float(x) if x not in ("", None) else None


# ----------------------------------------------------------------------------- per-row outcomes

def india_rows(lo=1000.0, hi=20000.0):
    p1 = list(csv.DictReader(open(os.path.join(BT, "solvency_india_outputs", "panel.csv"), encoding="utf-8")))
    p2 = list(csv.DictReader(open(os.path.join(BT, "hard_filters_india_v2_outputs", "panel_v2.csv"), encoding="utf-8")))
    same = len(p1) == len(p2) and all(a["key"] == b["key"] and a["snap"] == b["snap"] and a["r5"] == b["r5"]
                                      and a["weight"] == b["weight"] and a["o_fail"] == b["o_fail"]
                                      for a, b in zip(p1, p2))
    out, audit = [], defaultdict(int)
    for r in p1:
        m = _f(r["mcap"])
        if m is None or not (lo <= m <= hi):
            continue
        r5 = _f(r["r5"])
        fail = r["o_fail"] == "1"
        row = {"cluster": (r["stratum"], r["key"]), "stratum": r["stratum"], "w": float(r["weight"]),
               "snap": r["snap"], "fail": fail, "strict": r["o_strict"] == "1"}
        if r5 is not None:
            row["ge3"], row["le05"] = r5 >= 3.0, r5 <= 0.5
            audit["r5_known"] += 1
        elif fail:
            row["ge3"], row["le05"] = False, True
            audit["no_r5_failed_counted"] += 1
        else:
            row["ge3"] = row["le05"] = None
            audit["no_r5_not_failed_excluded"] += 1
        out.append(row)
    audit["rows"] = len(out)
    audit["panel_v2_identical_rows"] = same
    for s in ("D", "X", "L"):
        audit["rows_stratum_" + s] = sum(1 for x in out if x["stratum"] == s)
    return out, dict(audit)


def us_rows(lo=5e8, hi=1e10, variant="primary"):
    """variant: primary | acquired_excluded | stopped_as_loss"""
    rows = list(csv.DictReader(open(os.path.join(BT, "solvency_us_outputs", "panel.csv"), encoding="utf-8")))
    out, audit = [], defaultdict(int)
    for r in rows:
        fl = _f(r["float"])
        if fl is None or not (lo <= fl <= hi):
            continue
        r5 = _f(r["R5"])
        fail = r["O_fail"] == "1"
        fate = r["fate"]
        row = {"cluster": r["cik"], "stratum": "all", "w": 1.0, "snap": r["T"][:4], "fail": fail,
               "strict": r["O_strict"] == "1"}
        if r5 is not None:
            row["ge3"], row["le05"] = r5 >= 3.0, r5 <= 0.5
            audit["priced"] += 1
        elif fail:
            row["ge3"], row["le05"] = False, True
            audit["unpriced_edgar_failure"] += 1
        elif fate in ("acquired/merged", "merger-evidence-still-filing"):
            audit["unpriced_acquired"] += 1
            if variant == "acquired_excluded":
                row["ge3"] = row["le05"] = None
                row["drop_fail"] = True
            else:
                row["ge3"], row["le05"] = False, False
        elif fate == "stopped-filing" and variant == "stopped_as_loss":
            row["ge3"], row["le05"] = False, True
            audit["unpriced_stopped_as_loss"] += 1
        else:
            row["ge3"] = row["le05"] = None
            row["drop_fail"] = True     # identity/ticker problems: treat as missing at random for every rate
            audit["unpriced_excluded_" + fate.replace("/", "_").replace("-", "_")] += 1
        out.append(row)
    audit["rows"] = len(out)
    audit["distinct_ciks"] = len(set(x["cluster"] for x in out))
    return out, dict(audit)


# ----------------------------------------------------------------------------- estimators

def rates(rows):
    def wmean(key, skip_drop=False):
        num = den = 0.0
        n = 0
        for x in rows:
            v = x.get(key)
            if v is None or (skip_drop and x.get("drop_fail")):
                continue
            num += x["w"] * (1.0 if v else 0.0)
            den += x["w"]
            n += 1
        return (num / den if den else None), n
    out = {}
    out["p_ge_3x"], out["n_ge_3x"] = wmean("ge3")
    out["p_le_half"], out["n_le_half"] = wmean("le05")
    out["p_fail"], out["n_fail"] = wmean("fail", skip_drop=True)
    out["p_fail_strict"], _ = wmean("strict", skip_drop=True)
    return out


def bootstrap(rows, draws, seed=SEED):
    rng = random.Random(seed)
    by = defaultdict(lambda: defaultdict(list))   # stratum -> cluster -> rows
    for x in rows:
        by[x["stratum"]][x["cluster"]].append(x)
    strata = {s: list(c.values()) for s, c in by.items()}
    acc = defaultdict(list)
    for _ in range(draws):
        sample = []
        for s, clusters in strata.items():
            k = len(clusters)
            for _ in range(k):
                sample.extend(clusters[rng.randrange(k)])
        r = rates(sample)
        for key in ("p_ge_3x", "p_le_half", "p_fail", "p_fail_strict"):
            if r[key] is not None:
                acc[key].append(r[key])
    ci = {}
    for key, v in acc.items():
        v.sort()
        ci[key] = [round(v[int(0.025 * (len(v) - 1))], 4), round(v[int(0.975 * (len(v) - 1))], 4)]
    return ci


def by_snapshot(rows):
    snaps = sorted(set(x["snap"] for x in rows))
    return {s: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in rates([x for x in rows if x["snap"] == s]).items()}
            for s in snaps}


def _round(d):
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items()}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=2000)
    ap.add_argument("--out", default=os.path.join(BT, "base_rates_5y_outputs", "results.json"))
    a = ap.parse_args(argv)
    res = {"generated_by": "tools/backtests/base_rates_5y/build.py", "seed": SEED, "draws": a.draws}
    ind, ia = india_rows()
    res["india_nonfin_1000_20000cr_5y"] = {"point": _round(rates(ind)), "ci95": bootstrap(ind, a.draws),
                                          "by_snapshot": by_snapshot(ind), "audit": ia}
    # India robustness: live stratum only (what a survivors-only sample would have said)
    res["india_nonfin_1000_20000cr_5y"]["live_stratum_only"] = _round(rates([x for x in ind if x["stratum"] == "L"]))
    us = {}
    for v in ("primary", "acquired_excluded", "stopped_as_loss"):
        rows, au = us_rows(variant=v)
        us[v] = {"point": _round(rates(rows)), "audit": au}
        if v == "primary":
            us[v]["ci95"] = bootstrap(rows, a.draws)
            us[v]["by_snapshot"] = by_snapshot(rows)
    res["us_float_500m_10b_5y"] = us
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
