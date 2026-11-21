#!/usr/bin/env python3
"""Part B: markdown tables + per-company CSV from b2_analyze.py output.
  python3 b3_tables.py partB.json tables.md flags.csv"""
import csv, json, sys
o = json.load(open(sys.argv[1]))
NAMES = {"R1": "R1 CFO/PAT 5y < 0.3", "R1b": "R1b CFO/PAT 5y < 0.7", "R2": "R2 pledge > 25%", "R2b": "R2b pledge > 50%",
         "R3": "R3 auditor resignation before T0", "R4": "R4 debt ≥1.5x + Σ3y CFO < 0", "R5": "R5 other income > 30% PBT",
         "ANY_known": "**ANY of R1–R4**"}
L = []
for h, title in (("r5", "5-year (30-Sep-2020 → 30-Sep-2025)"), ("rnow", "to date (→ 18-Nov-2026)"),
                 ("mcap_ge400", "5-year, only firms with mcap ≥ Rs 400 cr at T0")):
    b = o["base_rates"][h if h != "mcap_ge400" else "mcap_ge400"]
    L.append("\n**%s** — base rates: loss50 %.1f%%, x3 %.1f%% (n = %d)\n" % (title, 100 * b["loss50"], 100 * b["x3"], b["n"]))
    L.append("| Rule | known / flagged | flagged → >50% loss | unflagged → >50% loss | Fisher p | flagged → >3x | unflagged → >3x | Fisher p | median ratio flagged / unflagged |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for k, v in o["rules"].items():
        t = v[h]
        f, u = t["loss50"]["flagged"], t["loss50"]["unflagged"]
        xf, xu = t["x3"]["flagged"], t["x3"]["unflagged"]
        mf, mu = t["median_ratio"]["flagged"], t["median_ratio"]["unflagged"]
        L.append("| %s | %d / %d | %d (%.1f%%, CI %s–%s) | %.1f%% | %s | %d (%.0f%%) | %.0f%% | %s | %s / %s |" % (
            NAMES[k], t["n_known"], t["n_flagged"], f[0], 100 * (f[2] or 0), f[3][0], f[3][1], 100 * (u[2] or 0),
            t["loss50"]["fisher_p"], xf[0], 100 * (xf[2] or 0), 100 * (xu[2] or 0), t["x3"]["fisher_p"],
            round(mf, 2) if mf else "–", round(mu, 2) if mu else "–"))
open(sys.argv[2], "w").write("\n".join(L) + "\n")
with open(sys.argv[3], "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["sym", "basis", "lender", "mcap0_cr", "p0_date", "ratio_5y", "ratio_now", "cfo_pat_5y", "pledge_pct",
                "R1", "R1b", "R2", "R3", "R4", "R5", "R3_first_hit"])
    for r in o["rows"]:
        if r.get("status") != "ok":
            w.writerow([r["sym"], "", "", "", "", "", "", "", "", "", "", "", "", "", "", r.get("status")]); continue
        w.writerow([r["sym"], r.get("basis"), r.get("lender"), r.get("mcap0_cr"), r.get("d0"), round(r["r5"], 3), round(r["rnow"], 3),
                    (r.get("m") or {}).get("cfo_pat"), r.get("pledge_pct"), r.get("R1"), r.get("R1b"), r.get("R2"), r.get("R3"),
                    r.get("R4"), r.get("R5"), (r.get("R3_hits") or [[""]])[0][0]])
