#!/usr/bin/env python3
"""Step 5: survivorship audit - how many companies on each dead/live list had a screener page, annual data at a
snapshot, and made the panel. Output: solvency_india_outputs/survivorship_audit.json"""
import collections, csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K

st = K.jload(os.path.join(K.CACHE, "fetch_status.json"), {})
fr = K.read_csv(os.path.join(K.CACHE, "frame.csv"))
pk = collections.Counter(r["key"] for r in K.read_csv(os.path.join(K.OUTDIR, "panel.csv")))
out = {}
for src in ["ibbi_liq", "ibbi_cirp", "ibbi_nclt", "nse_delisted_forced", "bse_suspended", "nse_suspended",
            "bse_delisted", "nse_delisted_voluntary", "bse_active", "nse_active"]:
    g = [r for r in fr if src in r["sources"].split("|")]
    if not g:
        continue
    ok = [r for r in g if st.get(r["key"], {}).get("page") == "ok"]
    out[src] = {"companies": len(g), "page": len(ok),
                "annual_at_a_T": sum(any(st[r["key"]]["elig"].values()) for r in ok),
                "in_panel": sum(1 for r in g if pk[r["key"]])}
out["identifier_less_rows_dropped"] = K.jload(os.path.join(K.CACHE, "frame_meta.json"), {}).get("identifier_less_rows_dropped")
K.jsave(os.path.join(K.OUTDIR, "survivorship_audit.json"), out)
print(json.dumps(out, indent=1))
