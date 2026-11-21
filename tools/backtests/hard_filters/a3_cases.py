#!/usr/bin/env python3
"""Part A: merge hand-coded pre-T flags (a2_episodes.py) with mechanical pre-T metrics and BSE pledge data,
then compute per-rule confusion matrices.

  python3 a3_cases.py CASES_DIR CASES_JSON OUT_JSON
CASES_DIR: screener/ pages (<KEY>.html), pledge.json (a1_pledge.py), ../sec/<KEY>.csv (sec_fetch.py facts --csv)
CASES_JSON: `python3 -m memdb search "" --type case_study --limit 200 --json` (coverage check only)

Point-in-time rule for annual data: India FY (March year-end) counts as public from 30-Sep of that year;
US fiscal year counts from period_end + 90 days. Need >= 3 fiscal years before T, else mechanical = U."""
import csv, datetime as dt, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hfcommon as hc          # noqa: E402
from a2_episodes import EPISODES, EXCLUDED, H, G   # noqa: E402

CD, CJ, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
MECH = ["F1_cfo_pat_lt_0.7", "F1b_cfo_pat_lt_0.3", "G2_debt_up_neg_cfo", "G5_neg_fcf", "G6_debtor_days", "F2_other_income", "H1b_proxy"]
pledge = json.load(open(os.path.join(CD, "pledge.json"))) if os.path.exists(os.path.join(CD, "pledge.json")) else {}


def d(s):
    return dt.date.fromisoformat(s)


def india_metrics(key, T):
    T = d(T)
    last_fy = T.year if T >= dt.date(T.year, 9, 30) else T.year - 1
    best = None
    for k in (key, key + "_sa") if not key.endswith("_sa") else (key,):
        p = os.path.join(CD, "screener", k + ".html")
        if not os.path.exists(p):
            continue
        sc = hc.parse_screener(p)
        m = hc.metrics_at(sc["FY"], last_fy)
        if m.get("n_years", 0) >= 3 and (best is None or m["n_years"] > best[0]["n_years"]):
            best = (m, sc["basis"], sc.get("BSE"))
        elif best is None:
            best = (m, sc["basis"], sc.get("BSE"))
    return best


def us_metrics(key, T):
    p = os.path.join(CD, "..", "sec", key + ".csv")
    if not os.path.exists(p):
        return None
    T = d(T)
    fy = {}
    for r in csv.DictReader(open(p)):
        pe = d(r["period_end"])
        if pe + dt.timedelta(days=90) > T:
            continue
        f = lambda x: float(r[x]) / 1e6 if r.get(x) not in (None, "") else None
        rec = {"sales": f("revenue"), "pat": f("net_income"), "cfo": f("cfo"), "fcf": f("fcf"), "op": f("op_income"),
               "debt": f("lt_debt"), "pbt": None}
        if rec["sales"] and f("receivables") is not None:
            rec["debtor_days"] = round(365 * f("receivables") / rec["sales"], 1)
        fy[pe.year if pe.month > 6 else pe.year - 1 if pe.month < 3 else pe.year] = rec
    if not fy:
        return ({"n_years": 0}, "sec", None)
    return (hc.metrics_at(fy, max(fy)), "sec", None)


BSE_OVERRIDE = {"MANPASAND": "539207", "COXKINGS": "533144"}
NA_G1 = {"paytm-ipo-2021", "false-alarm-eternal-zomato-losses-dilution", "mazagon-dock"}   # no promoter / IPO = govt
rows = []
for e in EPISODES:
    r = dict(e)
    r["mech"], r["mech_src"], r["metrics"] = {k: None for k in MECH}, None, {}
    if e["key"]:
        res = india_metrics(e["key"], e["T"]) if e["mkt"] == "IN" else us_metrics(e["key"], e["T"])
        if res:
            m, basis, bse = res
            r["metrics"], r["mech_src"] = m, basis
            if m.get("n_years", 0) >= 3:
                r["mech"] = hc.rules(m, lender=e["lender"])
            if e["mkt"] == "US" and m.get("n_years", 0) >= 3:
                r["mech"]["F2_other_income"] = None          # not parsed from SEC facts
            # pledge from BSE SHP (overrides the hand code unless the hand code is Y with evidence)
            bse = BSE_OVERRIDE.get(e["key"], bse)
            if bse:
                pk = bse + ":" + e["T"]
                pv = pledge.get(pk)
                if pv and pv.get("status") in ("ok", "parse_fail") and pv.get("total_shares"):
                    pct = pv.get("pledge_pct_of_promoter")
                    if pct is None and (pv.get("promoter_shares") or pv.get("status") == "parse_fail"):
                        pct = 0.0     # tag absent = nothing pledged (or no promoter group)
                    r["flags"]["G1"] = "Y" if pct > 25 else "N"
                    r["ev"]["G1"] = "BSE SHP %s (filed %s): %.1f%% of promoter holding pledged" % (pv["qtr"], pv["filed"], pct)
    if e["mkt"] == "IN" and r["flags"]["G1"] == "N" and "G1" not in r["ev"]:
        r["flags"]["G1"] = "U"          # Indian promoter company with no pledge data at T
    if (e["mkt"] != "IN" and r["flags"]["G1"] == "N") or e["id"] in NA_G1:
        r["flags"]["G1"] = "NA"         # widely held / no promoter group
    if e["lender"]:
        for k in MECH:
            r["mech"][k] = "NA"
    rows.append(r)

# coverage check against memdb
cases = json.load(open(CJ))
ids = {c["id"] for c in cases}
covered = {x for r in rows for x in r["records"]} | set(EXCLUDED)
missing = sorted(ids - covered)
extra = sorted(covered - ids)


def outcome_class(r):
    return "T" if r["label"] == "T" else "W"       # FA counts as a winner


def v(r, rule):
    if rule in r["flags"]:
        return r["flags"][rule]
    x = r["mech"].get(rule)
    if x == "NA":
        return "NA"
    return "U" if x is None else ("Y" if x else "N")


RULES = H + G + MECH


def matrix(rows_, rule_fn):
    out = {"T": {"Y": 0, "N": 0, "U": 0, "NA": 0}, "W": {"Y": 0, "N": 0, "U": 0, "NA": 0}}
    for r in rows_:
        out[outcome_class(r)][rule_fn(r)] += 1
    return out


def combo(rules_):
    def f(r):
        vals = [v(r, k) for k in rules_]
        if "Y" in vals:
            return "Y"
        if "U" in vals:
            return "U"
        return "N" if "N" in vals else "NA"
    return f


res = {"n_episodes": len(rows), "missing_records": missing, "unknown_ids": extra,
       "by_label": {}, "rules": {}, "combos": {}, "rules_by_trap_sub": {}}
for r in rows:
    res["by_label"][r["label"] + ("-" + r["sub"] if r["sub"] else "")] = res["by_label"].get(r["label"] + ("-" + r["sub"] if r["sub"] else ""), 0) + 1
for k in RULES:
    res["rules"][k] = matrix(rows, lambda r, k=k: v(r, k))
    res["rules_by_trap_sub"][k] = {s: matrix([r for r in rows if r["label"] == "T" and r["sub"] == s], lambda r, k=k: v(r, k))["T"]
                                   for s in ("fraud", "lev", "bust")}
COMBOS = {
    "HARD_current (H1a,H1b,H1c,H2,H3,H4,H5)": ["H1a", "H1b", "H1c", "H2", "H3", "H4", "H5"],
    "HARD + H2b broad": ["H1a", "H1b", "H1c", "H2", "H2b", "H3", "H4", "H5"],
    "GRADED any (G1,G3,G4 + mechanical)": G + [k for k in MECH if k != "H1b_proxy"],
    "mech cash only (F1b CFO/PAT<0.3 or G2)": ["F1b_cfo_pat_lt_0.3", "G2_debt_up_neg_cfo"],
    "pledge only (G1)": ["G1"],
}
for name, rs in COMBOS.items():
    res["combos"][name] = matrix(rows, combo(rs))
    res["combos"][name + " | traps by sub"] = {s: matrix([r for r in rows if r["label"] == "T" and r["sub"] == s], combo(rs))["T"]
                                               for s in ("fraud", "lev", "bust")}
# count of graded flags fired per episode (the '3+ open flags' rule)
for r in rows:
    r["n_graded_Y"] = sum(v(r, k) == "Y" for k in G + MECH if k != "H1b_proxy")
    r["n_hard_Y"] = sum(v(r, k) == "Y" for k in H if k != "H2b")
    r["final"] = {k: v(r, k) for k in RULES}
res["graded_count_dist"] = {}
for c in ("T", "W"):
    dist = {}
    for r in rows:
        if outcome_class(r) == c:
            dist[r["n_graded_Y"]] = dist.get(r["n_graded_Y"], 0) + 1
    res["graded_count_dist"][c] = dict(sorted(dist.items()))
res["episodes"] = [{k: r[k] for k in ("id", "label", "sub", "mkt", "key", "T", "lender", "outcome", "final", "ev", "later",
                                      "metrics", "mech_src", "n_graded_Y", "n_hard_Y", "note", "records")} for r in rows]
json.dump(res, open(OUT, "w"), indent=1, default=str)
print("episodes", len(rows), res["by_label"], "missing", missing, "extra", extra)
for k in RULES:
    m = res["rules"][k]
    print("%-22s traps Y/N/U %2d/%2d/%2d | winners Y/N/U %2d/%2d/%2d" % (k, m["T"]["Y"], m["T"]["N"], m["T"]["U"], m["W"]["Y"], m["W"]["N"], m["W"]["U"]))
for k, m in res["combos"].items():
    if "|" in k:
        print("   ", k, m)
    else:
        print("%-45s traps Y/N/U %2d/%2d/%2d | winners Y/N/U %2d/%2d/%2d" % (k, m["T"]["Y"], m["T"]["N"], m["T"]["U"], m["W"]["Y"], m["W"]["N"], m["W"]["U"]))
print("graded flags fired per episode:", res["graded_count_dist"])
