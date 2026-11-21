#!/usr/bin/env python3
"""Part B step 1: fetch the data for the mechanical hard-filter snapshot of the 580-company PEAD sample.

  python3 b1_fetch.py PEAD_DIR OUT_DIR screener   # screener.in consolidated page (fallback standalone)
  python3 b1_fetch.py PEAD_DIR OUT_DIR shp        # BSE SHP XBRL nearest to 31-Mar-2020 (promoter pledge)
  python3 b1_fetch.py PEAD_DIR OUT_DIR ann        # NSE announcements 01-01-2015..30-09-2020 (auditor exits)

PEAD_DIR holds results/<SYM>.json from tools/backtests/india_pead/s3_results.py (status 'ok' = the 580).
Everything is cached under OUT_DIR; re-runs skip what exists. Polite gaps: screener 3 s, BSE/NSE 1.5 s.
Downloaded pages are untrusted data: only parsed with regex, never executed."""
import glob, json, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
PEAD, OUT, WHAT = sys.argv[1], sys.argv[2], sys.argv[3]
syms = []
for fn in sorted(glob.glob(os.path.join(PEAD, "results", "*.json"))):
    j = json.load(open(fn))
    if j.get("status") == "ok":
        syms.append(j["symbol"])
if os.environ.get("SHARD"):            # e.g. SHARD=1/3 -> every 3rd symbol starting at index 1
    i, n = map(int, os.environ["SHARD"].split("/"))
    syms = syms[i::n]
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def curl(url, http2=False):
    cmd = ["curl", "-sS", "-L", "--compressed", "-A", UA, "--max-time", "60", "-w", "\n%{http_code}"]
    if http2:
        cmd += ["--http2", "-H", "Referer: https://www.bseindia.com/"]
    r = subprocess.run(cmd + [url], capture_output=True, timeout=90)
    body = r.stdout.decode("utf-8", "replace")
    body, _, code = body.rpartition("\n")
    return code.strip(), body


def has_pl(page):
    i = page.find('id="profit-loss"')
    return i >= 0 and "Net Profit" in page[i:i + 60000] and re.search(r"<td[^>]*>\s*-?[\d,]+\.?\d*\s*</td>", page[i:i + 60000])


def first_fy(page):
    i = page.find('id="profit-loss"')
    if i < 0:
        return 9999
    ys = re.findall(r"Mar (\d{4})", page[i:i + 6000])
    return min(int(y) for y in ys) if ys else 9999


def get_page(s, kind):
    for attempt in range(4):
        t0 = time.time()
        code, body = curl("https://www.screener.in/company/%s/%s" % (s, kind))
        time.sleep(max(0, 3.0 - (time.time() - t0)))
        if code == "429":
            time.sleep(30 * (attempt + 1)); continue
        return code, body
    return code, body


if WHAT in ("screener", "screener_list"):
    # consolidated page first; if it is missing/empty or starts after FY2016, also keep the standalone page
    # (standalone usually spans 12 fiscal years, FY2015-FY2026), saved as <SYM>_sa.html.
    D = os.path.join(OUT, "screener"); os.makedirs(D, exist_ok=True)
    if WHAT == "screener_list":
        syms = sys.argv[4].split(",")
    for s in syms:
        fn = os.path.join(D, s + ".html")
        fsa = os.path.join(D, s + "_sa.html")
        if not os.path.exists(fn) and not os.path.exists(fn + ".fail"):
            code, body = get_page(s, "consolidated/")
            if code == "200" and has_pl(body):
                open(fn, "w").write("<!-- basis:consolidated -->\n" + body)
            else:
                open(fn + ".fail", "w").write(code)
        need_sa = (not os.path.exists(fn)) or first_fy(open(fn, errors="replace").read()) > 2016
        if need_sa and not os.path.exists(fsa) and not os.path.exists(fsa + ".fail"):
            code, body = get_page(s, "")
            if code == "200" and has_pl(body):
                open(fsa, "w").write("<!-- basis:standalone -->\n" + body)
            else:
                open(fsa + ".fail", "w").write(code)
        print(s, "C" if os.path.exists(fn) else "-", "S" if os.path.exists(fsa) else "-", flush=True)

elif WHAT == "shp":
    import bse_fetch as b
    D = os.path.join(OUT, "shp"); os.makedirs(D, exist_ok=True)
    for s in syms:
        fn = os.path.join(D, s + ".json")
        if os.path.exists(fn):
            continue
        sp = os.path.join(OUT, "screener", s + ".html")
        if not os.path.exists(sp):
            continue
        m = re.search(r"bseindia\.com/[^\"']*?/(\d{6})/", open(sp, errors="replace").read())
        if not m:
            json.dump({"symbol": s, "status": "no_bse_code"}, open(fn, "w")); print(s, "no bse"); continue
        code = m.group(1)
        try:
            lst = b.api("SHPQNewFormat/w", scripcode=code, qtrid="", Type="EQ").get("Table", [])
        except Exception as e:
            print(s, "list err", e); continue
        pick = {}
        for want in ("March 2020", "December 2019", "June 2020", "March 2019", "March 2018"):
            for x in lst:
                if x.get("qtr") == want:
                    pick[want] = x
        res = {"symbol": s, "bse": code, "status": "ok", "q": {}}
        for want in ("March 2020",):   # trend quarters dropped for speed
            x = pick.get(want) or (pick.get("December 2019") if want == "March 2020" else None)
            if not x:
                continue
            url = "https://www.bseindia.com" + x["xbrlurl"] if x.get("xbrlurl", "").endswith(".xml") else None
            if not url:
                res["q"][want] = {"status": "no_xml", "xbrlurl": x.get("xbrlurl")}; continue
            time.sleep(1.5)
            hc, body = curl(url, http2=True)
            vals = {}
            for tag in ("PledgedOrEncumberedNumberOfShares", "PledgedOrEncumberedSharesHeldAsPercentageOfTotalNumberOfShares",
                        "NumberOfShares"):
                for ctx in ("ShareholdingOfPromoterAndPromoterGroup", "ShareholdingPattern"):
                    mm = re.search(r"<in-bse-shp:%s contextRef=\"%s(?:_ContextI|I)\"[^>]*>\s*([0-9.]+)" % (tag, ctx), body)
                    if mm:
                        vals[tag + "|" + ctx] = float(mm.group(1))
            res["q"][want] = {"status": "ok" if vals else "parse_fail_%s" % hc, "qtr_used": x["qtr"],
                              "filed": x.get("filing_date_time"), "vals": vals}
        json.dump(res, open(fn, "w"))
        print(s, code, {k: v.get("vals", {}).get("PledgedOrEncumberedSharesHeldAsPercentageOfTotalNumberOfShares|ShareholdingOfPromoterAndPromoterGroup") for k, v in res["q"].items()}, flush=True)

elif WHAT in ("ann", "ann_list"):
    import nse_fetch as n
    if WHAT == "ann_list":   # Part A: python3 b1_fetch.py X OUT ann_list SYM1,SYM2 FROM TO
        syms = sys.argv[4].split(",")
    n.MIN_GAP = 1.5
    D = os.path.join(OUT, "ann"); os.makedirs(D, exist_ok=True)
    PAT = re.compile(r"auditor|statutory audit", re.I)
    for s in syms:
        fn = os.path.join(D, s + ".json")
        if os.path.exists(fn):
            continue
        try:
            rows = n.announcements(s, *(sys.argv[5:7] if WHAT == "ann_list" else ("01-01-2015", "30-09-2020"))) or []
        except Exception as e:
            print(s, "err", e); continue
        keep = [[x.get("an_dt"), x.get("desc"), (x.get("attchmntText") or "")[:600]] for x in rows
                if PAT.search((x.get("desc") or "") + " " + (x.get("attchmntText") or ""))]
        json.dump({"symbol": s, "n_rows": len(rows), "auditor_rows": keep}, open(fn, "w"))
        print(s, len(rows), len(keep), flush=True)
