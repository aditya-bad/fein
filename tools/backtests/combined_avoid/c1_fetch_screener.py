#!/usr/bin/env python3
"""Step 2a (screener stream): standalone company page + 'Cash from Financing Activity' schedule for every event firm
not already cached. One stream, >= 1.55 s (solvency_screen.curl limiter). Output: $BT_COMB/status_sc.json and
$BT_COMB/sc/<slug>/{page.html, cash_from_financing_activity.json}. Downloaded HTML/JSON is untrusted data (parsed only)."""
import json, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common3 as C
import solvency_screen as SS
SS.GAP = 1.55
SCR_URL = "https://www.screener.in"
P = "Cash from Financing Activity"


def main():
    ids = C.id_maps()
    stp = os.path.join(C.OUT, "status_sc.json")
    st = C.jl(stp, {})
    n = 0
    for i, (sym, r) in enumerate(ids.items()):
        rec = st.get(sym) or {}
        try:
            if "cid" not in rec and "no_page" not in rec:
                if r.get("cid"):
                    rec.update(slug=r["slug"], cid=r["cid"], page=os.path.join(r["dir"], "page.html"), src="cache")
                else:
                    for cand in [sym] + ([r["bse_code"]] if r.get("bse_code") else []):
                        d = os.path.join(C.OUT, "sc", cand)
                        pg = SS.cached(os.path.join(d, "page.html"), 1e6,
                                       lambda: SS.curl(f"{SCR_URL}/company/{urllib.parse.quote(cand)}/")); n += 1
                        m = re.search(r'data-company-id="(\d+)"', pg or "")
                        if m and 'id="profit-loss"' in pg:
                            rec.update(slug=cand, cid=m.group(1), page=os.path.join(d, "page.html"), src="fetched"); break
                    else:
                        rec["no_page"] = 1
            if rec.get("cid") and "cf" not in rec:
                own = os.path.join(os.path.dirname(rec["page"]), "cash_from_financing_activity.json")
                if os.path.exists(own):
                    rec["cf"] = own
                else:
                    d = os.path.join(C.OUT, "sc", rec["slug"]); fp = os.path.join(d, "cash_from_financing_activity.json")
                    q = urllib.parse.urlencode({"parent": P, "section": "cash-flow"})
                    SS.cached(fp, 1e6, lambda: SS.curl(f"{SCR_URL}/api/company/{rec['cid']}/schedules/?{q}")); n += 1
                    rec["cf"] = fp
        except Exception as e:
            rec["error"] = str(e)[:200]
        st[sym] = rec
        if i % 20 == 0:
            C.js(stp, st); print(i, sym, rec.get("src"), "requests", n, flush=True)
    C.js(stp, st)
    print("screener done, requests", n, flush=True)


if __name__ == "__main__":
    main()
