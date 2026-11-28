#!/usr/bin/env python3
"""Fetch raw gold-study data (public files only; stdlib + curl). Saves to --out with sources.json (url, http, as_of).

    python3 tools/gold/fetch.py                       # -> research_notes/Gold/gold_study_<YYYY-MM>/data
    python3 tools/gold/fetch.py --out DIR [--only KEY]

No logins, no API keys, no CAPTCHA/anti-bot workarounds. A failed source is recorded (http code) and left missing.
"""
import argparse, datetime as dt, json, os, re, subprocess, sys, zipfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
YH = "https://query1.finance.yahoo.com/v8/finance/chart/{}?period1=0&period2=1900000000&interval={}"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
SRC = {
    # gold USD
    "wb_cmo_monthly.xlsx": ("https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021/related/"
                            "CMO-Historical-Data-Monthly.xlsx"),
    # FRED's LBMA series GOLDPMGBD228NLBM was discontinued (404 on 2026-11-28); datahub mirrors the WB/LBMA monthly
    # average and is updated past the WB file (WB workbook ended 2024-12 when fetched 2026-11-28)
    "datahub_gold_monthly.csv": "https://raw.githubusercontent.com/datasets/gold-prices/main/data/monthly.csv",
    "yahoo_gcf_1d.json": YH.format("GC%3DF", "1d"),
    "yahoo_gcf_1mo.json": YH.format("GC%3DF", "1mo"),
    "goldapi_xau.json": "https://api.gold-api.com/price/XAU",
    # FX
    "fred_EXINUS.csv": FRED.format("EXINUS"),
    "fred_DEXINUS.csv": FRED.format("DEXINUS"),
    "yahoo_inr_1d.json": YH.format("INR%3DX", "1d"),
    # rates / dollar
    "fred_DFII10.csv": FRED.format("DFII10"),
    "fred_FII10.csv": FRED.format("FII10"),
    "fred_GS10.csv": FRED.format("GS10"),
    "fred_DGS10.csv": FRED.format("DGS10"),
    "fred_CPIAUCSL.csv": FRED.format("CPIAUCSL"),
    "fred_FEDFUNDS.csv": FRED.format("FEDFUNDS"),
    "fred_DFEDTARU.csv": FRED.format("DFEDTARU"),
    "fred_DTWEXBGS.csv": FRED.format("DTWEXBGS"),
    "yahoo_dxy_1d.json": YH.format("DX-Y.NYB", "1d"),
    "yahoo_tnx_1d.json": YH.format("%5ETNX", "1d"),
    "treasury_real_yield_{Y}.csv": ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
                                    "daily-treasury-rates.csv/{Y}/all?type=daily_treasury_real_yield_curve"
                                    "&field_tdr_date_value={Y}&page&_format=csv"),
    # India domestic
    "ibja_home.html": "https://ibjarates.com/",
}


def curl(url, path):
    ua = ["-A", "Mozilla/5.0"] if ("yahoo" in url or "ibja" in url or "gold-api" in url) else []
    p = subprocess.run(["curl", "-sS", "-L", "-m", "120", *ua, "-o", path, "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    return p.stdout.strip() or p.stderr.strip()[:80]


def wb_gold(path):
    """World Bank CMO 'Monthly Prices' sheet -> {YYYY-MM: gold USD/oz}."""
    z = zipfile.ZipFile(path)
    st = [re.sub("<[^>]+>", "", x) for x in re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode(), re.S)]
    s = z.read("xl/worksheets/sheet2.xml").decode()
    col, out = None, {}
    for row in re.findall(r"<row [^>]*>(.*?)</row>", s, re.S):
        cells = re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(?:<v>([^<]*)</v>)?', row)
        if col is None:
            for c, attr, v in cells:
                if 't="s"' in attr and v and st[int(v)] == "Gold":
                    col = c
            continue
        d = {c: (st[int(v)] if 't="s"' in a and v else v) for c, a, v in cells}
        m = re.match(r"(\d{4})M(\d\d)", d.get("A", "") or "")
        if m and d.get(col):
            try:
                out[f"{m.group(1)}-{m.group(2)}"] = float(d[col])
            except ValueError:
                pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "research_notes", "Gold",
                                                  f"gold_study_{dt.date.today():%Y-%m}", "data"))
    ap.add_argument("--only", action="append")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    mp = os.path.join(a.out, "sources.json")
    meta = json.load(open(mp)) if os.path.exists(mp) else {}
    Y = str(dt.date.today().year)
    for fn, url in SRC.items():
        fn, url = fn.replace("{Y}", Y), url.replace("{Y}", Y)
        if a.only and fn not in a.only:
            continue
        path = os.path.join(a.out, fn)
        code = curl(url, path)
        meta[fn] = {"url": url, "http": code, "as_of": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")}
        print(fn, code, file=sys.stderr)
    xl = os.path.join(a.out, "wb_cmo_monthly.xlsx")
    if os.path.exists(xl):
        try:
            rows = wb_gold(xl)
            with open(os.path.join(a.out, "wb_gold_usd_monthly_avg.csv"), "w") as f:
                f.write("month,gold_usd_oz_monthly_avg\n" + "".join(f"{k},{v}\n" for k, v in sorted(rows.items())))
            meta["wb_gold_usd_monthly_avg.csv"] = dict(meta.get("wb_cmo_monthly.xlsx", {}), note="gold column extracted")
        except Exception as e:  # not an xlsx (e.g., an error page)
            meta["wb_cmo_monthly.xlsx"]["note"] = f"parse failed: {e}"
        os.remove(xl)
    json.dump(meta, open(mp, "w"), indent=1)


if __name__ == "__main__":
    main()
