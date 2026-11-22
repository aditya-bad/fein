#!/usr/bin/env python3
"""Step 2: polite screener fetch in three phases (>= 1.5 s between requests, one stream, all cached).

  phase pages     : standalone company page /company/<slug>/ (BSE code, else NSE symbol; 404 -> try the other id).
                    No outcome information. Decides which snapshots have annual data (FY0 in (T-18m, T-6m]).
  phase charts    : one chart call per firm with snapshot data: Price-Market Cap to Sales-Sales (weekly, full history).
                    Gives size at T and (later, in s3) the outcome path.
  phase schedules : Borrowings / Other Assets / Cash from Financing (standalone) for firms in the size band at a T.
Cache layout: $CACHE/sc/<slug>/{page.html,chart.json,*.json}. Progress: $CACHE/fetch_status.json.
"""
import argparse, datetime as dt, json, os, re, sys, time, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K

SS, F = K.SS, K.F
FOREVER = 1e6   # cache never expires within this test


def page_for(r):
    tried = []
    for slug in [r["slug"]] + ([r["nse_symbol"]] if r["nse_symbol"] and r["nse_symbol"] != r["slug"] else []):
        d = os.path.join(K.CACHE, "sc", slug)
        p = os.path.join(d, "page.html")
        miss = os.path.join(d, "404")
        tried.append(slug)
        if os.path.exists(miss):
            continue
        body = K.SS.cached(p, FOREVER, lambda: SS.curl(f"{K.SCREENER}/company/{urllib.parse.quote(slug)}/"))
        if body and 'id="profit-loss"' in body:
            return slug, d, body
        os.makedirs(d, exist_ok=True)
        open(miss, "w").close()
    return None, None, None


def fy0_for(fin, T):
    lo = dt.date(T.year - 2, T.month, 1) + dt.timedelta(days=0)
    lo = dt.date(T.year - 1, 3, 31) if T.month == 9 else lo      # (T-18m, T-6m] for T = 30-Sep
    hi = dt.date(T.year, 3, 31)
    c = [d for d in fin["FY"] if lo < d <= hi and d in fin["BS"]]
    return max(c) if c else None


def snapshot_eligibility(page):
    fin = F.parse_screener(page)
    return {s: (fy0_for(fin, T).isoformat() if fy0_for(fin, T) else None) for s, T in K.SNAPS.items()}


def mcap_at(chart, T):
    ds = {d["metric"]: d["values"] for d in (chart or {}).get("datasets", [])}
    px = [(dt.date.fromisoformat(a), float(b)) for a, b, *_ in ds.get("Price", []) if b not in (None, "")]
    mcs = {a: c for a, c, *_ in ds.get("Market Cap to Sales", [])}
    sales = [(dt.date.fromisoformat(a), float(b)) for a, b, *_ in ds.get("Sales", []) if b not in (None, "")]
    if not px:
        return {"status": "no_price_history"}
    before = [(d, p) for d, p in px if d <= T]
    if not before or (T - before[-1][0]).days > 31:
        return {"status": "not_trading_at_T"}
    dT, pT = before[-1]
    m = mcs.get(dT.isoformat())
    s = [v for d, v in sales if d <= T]
    if m is None or not s or s[-1] <= 0:
        return {"status": "size_unknown", "px_date": dT.isoformat(), "px": pT}
    m, sv = float(m), s[-1]
    return {"status": "ok", "px_date": dT.isoformat(), "px": pT, "mcs": m, "sales_ttm": sv, "mcap": m * sv,
            "mcap_lo": max(m - 0.05, 0) * sv, "mcap_hi": (m + 0.05) * sv}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["pages", "charts", "schedules", "all"], default="all")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    SS.GAP = 1.55
    frame = K.read_csv(os.path.join(K.CACHE, "frame.csv"))[: a.limit]
    stp = os.path.join(K.CACHE, "fetch_status.json")
    st = K.jload(stp, {})
    t0, n = time.time(), 0
    phases = ["pages", "charts", "schedules"] if a.phase == "all" else [a.phase]
    for ph in phases:
        for i, r in enumerate(frame, 1):
            k = r["key"]
            s = st.setdefault(k, {})
            try:
                if ph == "pages" and "page" not in s:
                    slug, d, page = page_for(r)
                    if not page:
                        s["page"] = "no_page"
                    else:
                        lab = SS.labels(page)
                        s.update(page="ok", slug=slug, fin=SS.is_financial(lab, page),
                                 industry=" / ".join(v for kk, v in lab.items() if kk in ("Broad Industry", "Industry")),
                                 name=SS.company_name(page), elig=snapshot_eligibility(page),
                                 cid=(re.search(r'data-company-id="(\d+)"', page) or [None, None])[1])
                    n += 1
                elif ph == "charts" and s.get("page") == "ok" and not s["fin"] and any(s["elig"].values()) \
                        and "size" not in s:
                    d = os.path.join(K.CACHE, "sc", s["slug"])
                    q = "Price-Market+Cap+to+Sales-Sales"
                    txt = SS.cached(os.path.join(d, "chart.json"), FOREVER,
                                    lambda: SS.curl(f"{K.SCREENER}/api/company/{s['cid']}/chart/?q={q}&days=10000"))
                    ch = json.loads(txt) if txt else {}
                    s["size"] = {sn: (mcap_at(ch, T) if s["elig"].get(sn) else {"status": "no_annual_at_T"})
                                 for sn, T in K.SNAPS.items()}
                    n += 1
                elif ph == "schedules" and "size" in s and "sched" not in s and any(
                        z.get("status") == "ok" and z["mcap_hi"] >= K.MCAP_LO and z["mcap_lo"] <= K.MCAP_HI
                        for z in s["size"].values()):
                    d = os.path.join(K.CACHE, "sc", s["slug"])
                    SS.fetch_schedules(s["cid"], d, FOREVER, standalone=True)
                    s["sched"] = "ok"
                    n += 1
            except Exception as e:          # keep going; record
                s[ph + "_error"] = str(e)[:200]
                print("ERR", k, ph, e, flush=True)
            if n and n % 50 == 0:
                K.jsave(stp, st)
            if i % 200 == 0:
                print(f"{ph} {i}/{len(frame)} requests~{n} {time.time()-t0:.0f}s", flush=True)
        K.jsave(stp, st)
        print(f"phase {ph} done, {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
