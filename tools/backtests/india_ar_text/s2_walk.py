#!/usr/bin/env python3
"""Step 2: walk frame.txt in seeded order. Per symbol: screener page + weekly chart (labels, financial flag, mcap at
2023-03-31). Eligible = non-financial, Rs 500-20,000 cr. The first 200 eligible firms are text firms: NSE
annual_reports list, FY22/FY23/FY24 reports downloaded one at a time, pdftotext'd, PDFs deleted at once; only the
page texts are kept (gzip JSON). Stops at 350 eligible. One stream (NSE and screener alternate, >= 1.5 s each).
State per symbol: OUT/firms/<SYM>.json. Resumable. Usage: python3 s2_walk.py [--max-eligible 350] [--text 200]"""
import argparse, datetime as dt, json, os, re, sys, time, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402
SS = K.SS
T_SIZE = dt.date(2023, 3, 31)
FYS = ("2021", "2022", "2023")          # fromYr: FY22, FY23, FY24
FIRMS = os.path.join(K.OUT, "firms"); TXT = os.path.join(K.OUT, "text"); SC = os.path.join(K.OUT, "sc")
for d in (FIRMS, TXT, SC):
    os.makedirs(d, exist_ok=True)


def mcap_at(chart, T):
    ds = {d["metric"]: d["values"] for d in (chart or {}).get("datasets", [])}
    px = [(dt.date.fromisoformat(a), float(b)) for a, b, *_ in ds.get("Price", []) if b not in (None, "")]
    mcs = {a: c for a, c, *_ in ds.get("Market Cap to Sales", [])}
    sales = [(dt.date.fromisoformat(a), float(b)) for a, b, *_ in ds.get("Sales", []) if b not in (None, "")]
    before = [(d, p) for d, p in px if d <= T]
    if not before or (T - before[-1][0]).days > 31:
        return None
    dT = before[-1][0]
    m = mcs.get(dT.isoformat())
    s = [v for d, v in sales if d <= T]
    if m is None or not s or s[-1] <= 0:
        return None
    return float(m) * s[-1]


def screener(sym):
    d = os.path.join(SC, sym)
    page = SS.cached(os.path.join(d, "page.html"), 10 ** 6,
                     lambda: SS.curl(f"{K.SS.SCREENER}/company/{urllib.parse.quote(sym)}/"))
    if not page or 'id="profit-loss"' not in page:
        return None, None
    cid = (re.search(r'data-company-id="(\d+)"', page) or [None, None])[1]
    if not cid:
        return page, None
    q = "Price-Market+Cap+to+Sales-Sales"
    txt = SS.cached(os.path.join(d, "chart.json"), 10 ** 6,
                    lambda: SS.curl(f"{K.SS.SCREENER}/api/company/{cid}/chart/?q={q}&days=10000"))
    try:
        return page, json.loads(txt) if txt else None
    except ValueError:
        return page, None


def pick_reports(rows):
    out = {}
    for r in rows:
        if not r.get("submitted") and r.get("fileName"):
            r["submitted"] = K.N._stamp(r["fileName"])
    for fy in FYS:
        c = [r for r in rows if r.get("fromYr") == fy and r.get("fileName") and r.get("submitted")]
        if c:
            out[fy] = min(c, key=lambda r: r["submitted"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-eligible", type=int, default=350)
    ap.add_argument("--text", type=int, default=200)
    a = ap.parse_args()
    frame = open(os.path.join(K.OUT, "frame.txt")).read().split()
    n_el = n_txt = 0
    t0 = time.time()
    for i, sym in enumerate(frame):
        if n_el >= a.max_eligible:
            break
        fp = os.path.join(FIRMS, re.sub(r"[^\w&-]", "_", sym) + ".json")
        st = K.jload(fp, {}) or {"sym": sym, "order": i}
        try:
            if "elig" not in st:
                page, chart = screener(sym)
                if not page:
                    st.update(elig=False, why="no_screener_page")
                else:
                    lab = SS.labels(page)
                    fin = SS.is_financial(lab, page)
                    mc = mcap_at(chart, T_SIZE) if chart else None
                    st.update(labels=lab, fin=fin, name=SS.company_name(page), mcap_2303=mc)
                    if fin:
                        st.update(elig=False, why="financial")
                    elif mc is None:
                        st.update(elig=False, why="no_mcap_2303")
                    elif not (500 <= mc <= 20000):
                        st.update(elig=False, why="mcap_out_of_range")
                    else:
                        st.update(elig=True)
                K.jdump(st, fp)
            if not st["elig"]:
                continue
            n_el += 1
            st["el_rank"] = n_el
            if n_el <= a.text:
                n_txt += 1
                st["text_firm"] = True
                if "ar_rows" not in st:
                    try:
                        st["ar_rows"] = K.N.annual_reports(sym)
                    except Exception as e:
                        st["ar_rows"] = []; st["ar_err"] = str(e)[:200]
                    K.jdump(st, fp)
                rep = st.setdefault("reports", {})
                for fy, r in pick_reports(st["ar_rows"]).items():
                    if fy in rep and rep[fy].get("status") in ("ok", "empty"):
                        continue
                    tf = os.path.join(TXT, f"{re.sub(r'[^\w&-]', '_', sym)}_{fy}.json.gz")
                    try:
                        pages, size, npdf = K.fetch_text(r["fileName"], os.path.join(K.OUT, "work"))
                        if pages:
                            K.save_text(tf, pages)
                        rep[fy] = {"status": "ok" if sum(map(len, pages)) >= 50000 else "empty",
                                   "submitted": r["submitted"], "url": r["fileName"], "bytes": size,
                                   "npdf": npdf, "chars": sum(map(len, pages)), "pages": len(pages)}
                    except Exception as e:
                        rep[fy] = {"status": "fail", "err": str(e)[:200], "url": r["fileName"],
                                   "submitted": r["submitted"]}
                    K.jdump(st, fp)
            else:
                st["text_firm"] = False
            K.jdump(st, fp)
        except Exception as e:
            print("ERR", sym, e, flush=True)
            continue
        if i % 10 == 0:
            print(f"{i} walked, {n_el} eligible, {n_txt} text, {time.time() - t0:.0f}s", flush=True)
    print(f"done: walked to {i}, {n_el} eligible, {n_txt} text firms, {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
