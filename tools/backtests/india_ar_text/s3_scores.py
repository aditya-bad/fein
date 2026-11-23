#!/usr/bin/env python3
"""Step 3: per text firm and pair (P1 = FY23 vs FY22, P2 = FY24 vs FY23): sections, quality gates, Jaccard (MD&A, AUD),
auditor-section new adverse items. Writes OUT/firmyears.json, OUT/auditor_flags.tsv (sentences for the hand check),
OUT/s3_funnel.json."""
import collections, csv, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402
import flags as FL  # noqa: E402
PAIRS = {"P1": ("2021", "2022"), "P2": ("2022", "2023")}
TXT = os.path.join(K.OUT, "text")


def ok_mda(s): return len(s["MDA"]) >= 5000
def ok_aud(s): return 10000 <= len(s["AUD"]) <= 150000


secs_cache = {}


def secs(sym, fy, st):
    k = (sym, fy)
    if k not in secs_cache:
        r = (st.get("reports") or {}).get(fy) or {}
        fn = os.path.join(TXT, f"{re.sub(r'[^\w&-]', '_', sym)}_{fy}.json.gz")
        if r.get("status") != "ok" or not os.path.exists(fn):
            secs_cache[k] = None
        else:
            secs_cache[k] = K.SEC.sections(K.load_text(fn))
    return secs_cache[k]


fun = collections.Counter()
out, flagrows = [], []
for fp in sorted(glob.glob(os.path.join(K.OUT, "firms", "*.json"))):
    st = K.jload(fp)
    if not st.get("text_firm"):
        continue
    sym = st["sym"]
    fun["text_firms"] += 1
    if not st.get("ar_rows"):
        fun["no_ar_list"] += 1
    for p, (f0, f1) in PAIRS.items():
        rep = st.get("reports") or {}
        if f0 not in rep or f1 not in rep:
            fun[f"{p}_missing_report"] += 1; continue
        fun[f"{p}_attempted"] += 1
        a, b = secs(sym, f0, st), secs(sym, f1, st)
        if not a or not b:
            fun[f"{p}_unusable_text"] += 1; continue
        row = {"sym": sym, "pair": p, "submitted": rep[f1]["submitted"], "sector": (st.get("labels") or {}).get("Sector", ""),
               "mda_ok": ok_mda(a) and ok_mda(b), "aud_ok": ok_aud(a) and ok_aud(b),
               "len_mda": len(b["MDA"]), "len_aud": len(b["AUD"]), "caro": b["caro"]}
        row["jac_mda"] = K.SEC.jaccard(a["MDA"], b["MDA"]) if row["mda_ok"] else None
        row["jac_aud"] = K.SEC.jaccard(a["AUD"], b["AUD"]) if row["aud_ok"] else None
        fun[f"{p}_mda_ok"] += row["mda_ok"]; fun[f"{p}_aud_ok"] += row["aud_ok"]
        if row["aud_ok"]:
            new = FL.new_items(b["AUD"], a["AUD"])
            row["flag_cats"] = sorted(new)
            for c, ss in new.items():
                for s in ss[:3]:
                    flagrows.append([sym, p, rep[f1]["submitted"][:10], c, s])
        else:
            row["flag_cats"] = None
        out.append(row)
K.jdump(out, os.path.join(K.OUT, "firmyears.json"))
K.jdump(dict(fun), os.path.join(K.OUT, "s3_funnel.json"))
with open(os.path.join(K.OUT, "auditor_flags.tsv"), "w", newline="") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["sym", "pair", "submitted", "cat", "sentence"]); w.writerows(flagrows)
print(json.dumps(dict(fun), indent=1)); print(len(out), "firm-years;", len(flagrows), "flag sentences")
