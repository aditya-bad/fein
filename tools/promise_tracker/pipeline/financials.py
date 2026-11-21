#!/usr/bin/env python3
"""Reported numbers for auto-scoring: screener.in consolidated page (curl) or a CSV.

    python3 -I financials.py SYMBOL [--cache DIR] [--refresh] [--standalone] [--csv-out f.csv]

Screener (no login needed): https://www.screener.in/company/<SYMBOL>/consolidated/
Fetched with `curl -A 'Mozilla/5.0'` (stdlib urllib also works; curl is kept because
it handles the proxy/TLS setup on the Pi the same way as the shell). Cached as
<cache>/<SYMBOL>/screener.html; re-fetched when older than 3 days or with --refresh.

CSV alternative (for results PDFs / XBRL / manual entry), one row per number:
    period_end,period_type,field,value
    2026-03-31,FY,sales,5553
    2026-09-30,Q,sales,1384
period_type: Q (quarter), FY (fiscal year), BS (balance-sheet date). Fields used:
sales, op_profit, other_income, interest, depreciation, pbt, net_profit, eps, dividend_payout_pct,
borrowings, fixed_assets, cwip, cfo, fcf, debtor_days, inventory_days, wc_days, roce_pct.
"""
import argparse
import csv
import datetime as dt
import html
import os
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

ROWMAP = {
    "sales": "sales", "revenue": "sales", "expenses": "expenses", "operating profit": "op_profit",
    "financing profit": "op_profit", "other income": "other_income", "interest": "interest",
    "depreciation": "depreciation", "profit before tax": "pbt", "net profit": "net_profit", "eps in rs": "eps",
    "dividend payout %": "dividend_payout_pct", "borrowings": "borrowings", "fixed assets": "fixed_assets",
    "cwip": "cwip", "reserves": "reserves", "equity capital": "equity_capital",
    "cash from operating activity": "cfo", "free cash flow": "fcf", "debtor days": "debtor_days",
    "inventory days": "inventory_days", "working capital days": "wc_days", "roce %": "roce_pct",
    "cash conversion cycle": "ccc", "days payable": "payable_days",
}
SECTIONS = {"quarters": "Q", "profit-loss": "FY", "balance-sheet": "BS", "cash-flow": "FY", "ratios": "FY"}
MON = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def fetch_screener(symbol, root, refresh=False, standalone=False, max_age_days=3):
    path = os.path.join(C.sym_dir(root, symbol), "screener%s.html" % ("_sa" if standalone else ""))
    if not refresh and os.path.exists(path) and time.time() - os.path.getmtime(path) < max_age_days * 86400:
        return open(path, errors="replace").read(), path
    url = f"https://www.screener.in/company/{symbol}/" + ("" if standalone else "consolidated/")
    if shutil.which("curl"):
        r = subprocess.run(["curl", "-sS", "-L", "--compressed", "-A", "Mozilla/5.0", "--max-time", "60", url],
                           capture_output=True, timeout=90)
        body = r.stdout.decode("utf-8", "replace")
    else:
        import urllib.request
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as f:
            body = f.read().decode("utf-8", "replace")
    if 'id="quarters"' not in body:
        raise RuntimeError("screener page has no quarterly table (blocked, renamed symbol, or login wall)")
    with open(path, "w") as f:
        f.write(body)
    return body, path


def _num(s):
    s = s.replace(",", "").replace("%", "").strip()
    if s in ("", "-", "--"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _date(h):
    m = re.match(r"([A-Za-z]{3})\s+(\d{4})", h.strip())
    if not m:
        return None
    mo, y = MON[m.group(1).lower()], int(m.group(2))
    nxt = dt.date(y + (mo == 12), mo % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def parse_screener(page):
    """-> {"Q": {date: {field: v}}, "FY": {...}, "BS": {...}, "TTM": {field: v}, "as_of": latest Q date}"""
    out = {"Q": {}, "FY": {}, "BS": {}, "TTM": {}}
    for sec, kind in SECTIONS.items():
        i = page.find(f'id="{sec}"')
        if i < 0:
            continue
        j = page.find("</table>", i)
        t = page[i:j]
        heads = [html.unescape(re.sub(r"<[^>]+>|\s+", " ", x)).strip() for x in re.findall(r"<th[^>]*>(.*?)</th>", t, re.S)]
        cols = heads[1:]
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
            tds = [html.unescape(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
            tds = [re.sub(r"\s+", " ", x).strip() for x in tds]
            if not tds:
                continue
            label = re.sub(r"\s*\+$", "", tds[0]).strip().lower()
            field = ROWMAP.get(label)
            if not field:
                continue
            for h, v in zip(cols, tds[1:]):
                val = _num(v)
                if val is None:
                    continue
                if h.upper().startswith("TTM"):
                    out["TTM"][field] = val
                    continue
                d = _date(h)
                if d is None:
                    continue
                k = kind
                if sec == "balance-sheet":
                    k = "BS"
                out[k].setdefault(d, {})[field] = val
    out["as_of"] = max(out["Q"]) if out["Q"] else None
    return out


def load_csv(path):
    out = {"Q": {}, "FY": {}, "BS": {}, "TTM": {}}
    with open(path) as f:
        for r in csv.DictReader(f):
            d = dt.date.fromisoformat(r["period_end"])
            out[r["period_type"].upper()].setdefault(d, {})[r["field"]] = float(r["value"])
    out["as_of"] = max(out["Q"]) if out["Q"] else None
    return out


def merge(a, b):
    """b overrides a (CSV corrections on top of screener)."""
    for k in ("Q", "FY", "BS"):
        for d, row in b.get(k, {}).items():
            a.setdefault(k, {}).setdefault(d, {}).update(row)
    a["as_of"] = max(a["Q"]) if a.get("Q") else None
    return a


def to_csv(fin, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["period_end", "period_type", "field", "value"])
        for k in ("Q", "FY", "BS"):
            for d in sorted(fin[k]):
                for fld, v in sorted(fin[k][d].items()):
                    w.writerow([d.isoformat(), k, fld, v])


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol")
    p.add_argument("--cache")
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--standalone", action="store_true")
    p.add_argument("--csv-out")
    a = p.parse_args(argv)
    page, path = fetch_screener(a.symbol.upper(), C.cache_root(a.cache), a.refresh, a.standalone)
    fin = parse_screener(page)
    print(path, "quarters:", len(fin["Q"]), "years:", len(fin["FY"]), "latest quarter:", fin["as_of"])
    for d in sorted(fin["Q"])[-6:]:
        r = fin["Q"][d]
        print(" Q", d, {k: r.get(k) for k in ("sales", "op_profit", "net_profit")})
    for d in sorted(fin["FY"])[-4:]:
        r = fin["FY"][d]
        print(" FY", d, {k: r.get(k) for k in ("sales", "op_profit", "interest", "net_profit", "debtor_days", "roce_pct")})
    if a.csv_out:
        to_csv(fin, a.csv_out)
        print("wrote", a.csv_out)


if __name__ == "__main__":
    main()
