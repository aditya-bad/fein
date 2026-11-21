#!/usr/bin/env python3
"""Part A: markdown tables from a3_cases.py output.   python3 a4_tables.py partA.json > tables.md"""
import json, sys
r = json.load(open(sys.argv[1]))
NAMES = {"H1a": "H1a fake-cash signal", "H1b": "H1b implausible economics", "H1c": "H1c profits unverifiable",
         "H2": "H2 auditor exit over disagreement / qualified", "H2b": "H2b broad: any auditor exit / restatement / regulator misstatement / delayed results (5y)",
         "H3": "H3 rating 'not cooperating'", "H4": "H4 SME/Telegram pump", "H5": "H5 RPT cash leakage",
         "G1": "G1 pledge >25% of promoter holding", "G3": "G3 dilution / repeated raises", "G4": "G4 P/E >50",
         "F1_cfo_pat_lt_0.7": "F1 Σ5y CFO/PAT <0.7", "F1b_cfo_pat_lt_0.3": "F1b Σ5y CFO/PAT <0.3",
         "G2_debt_up_neg_cfo": "G2 debt ≥1.5x + Σ3y CFO<0", "G5_neg_fcf": "G5 Σ5y FCF <0",
         "G6_debtor_days": "G6 debtor days >120 or +30d", "F2_other_income": "F2 other income >30% PBT", "H1b_proxy": "H1b-proxy (blind): ROCE >40% 3y or OPM +10pp in 3y"}


def pct(a, b):
    return "%d%%" % round(100 * a / b) if b else "–"


print("| Rule | Traps fired / known (unknown) | Winners fired / known (unknown) | Trap catch rate (known) | Winner reject rate (known) | Precision (traps among fired) |")
print("|---|---|---|---|---|---|")
for k, m in list(r["rules"].items()) + [(k, v) for k, v in r["combos"].items() if "|" not in k]:
    T, W = m["T"], m["W"]
    kt, kw = T["Y"] + T["N"], W["Y"] + W["N"]
    fired = T["Y"] + W["Y"]
    print("| %s | %d / %d (%d) | %d / %d (%d) | %s | %s | %s |" % (NAMES.get(k, "**" + k + "**"), T["Y"], kt, T["U"], W["Y"], kw, W["U"],
                                                              pct(T["Y"], kt), pct(W["Y"], kw), pct(T["Y"], fired)))
print()
print("Hard set by trap type (Y / N / U): ")
for k, v in r["combos"].items():
    if "|" in k:
        print("- %s: %s" % (k, "; ".join("%s %d/%d/%d" % (s, x["Y"], x["N"], x["U"]) for s, x in v.items())))
print()
print("| Episode | Label | T | Outcome | Fired pre-T | Later warnings |")
print("|---|---|---|---|---|---|")
for e in r["episodes"]:
    fired = [("H1b-proxy" if k == "H1b_proxy" else k.split("_")[0]) for k, v in e["final"].items() if v == "Y"]
    later = "; ".join("%s: %s" % (k, v) for k, v in (e.get("later") or {}).items())
    lab = e["label"] + ("-" + e["sub"] if e["sub"] else "")
    print("| %s | %s | %s | %s | %s | %s |" % (e["id"], lab, e["T"], e["outcome"], ", ".join(fired) or "–", later or ""))
