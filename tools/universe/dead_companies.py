#!/usr/bin/env python3
"""Dead / distressed Indian listed companies: one snapshot from free public lists (stdlib + system curl).

Purpose: the outcome side of a survivorship-free Indian re-test of the solvency flags (Roadmap stage 2;
decision:solvency-flags-graded, lesson L24). Probe notes: research_notes/Universe/india_dead_companies_probe.md.

Sources (all checked 22-Nov-2026 from this network):
  ibbi_cirp   IBBI public announcements of CIRP (Form A), Excel export = tab-separated text, with CIN.
              https://ibbi.gov.in/en/public-announcement?ann=<type>&export_excel=export_excel
  ibbi_liq    same, "Public Announcement of Liquidation Process".
  ibbi_nclt   IBBI's mirror of NCLT orders (HTML, 20 per page; date, subject, order PDF, remark such as
              "Admission - Final order", "Liquidation", "Dissolution"). No CIN. --nclt-pages N (default 5).
  nse_delisted   https://nsearchives.nseindia.com/content/equities/delisted.csv (symbol, date, type) - STALE, ends Nov 2020
  nse_suspended  https://nsearchives.nseindia.com/content/equities/suspension.csv - STALE, ends Jul 2012
  bse_delisted / bse_suspended   BSE ListofScripData API, status=Delisted / Suspended (scrip code, ISIN,
              scrip id, name; no dates). Uses fein_common.bse_api (curl --http2), as collect.py does.
Mapping to exchange identifiers: IBBI rows whose CIN starts with "L" (company was listed when the CIN was
issued) are matched by normalised name (fein_common.norm_name) to BSE active+delisted+suspended lists
(-> BSE code, ISIN, scrip id) and to NSE EQUITY_L + delisted.csv (-> NSE symbol). Name matching is exact on
the normalised name; anything ambiguous is left blank (match = "ambiguous").

Output: research_notes/Universe/india_dead_companies_<date>.csv (one row per event):
  source, event, event_date, company, cin, nse_symbol, bse_code, isin, match, remarks, url
Default keeps IBBI rows only for listed CINs or name matches to a listed company (--all-ibbi keeps all).

Usage:
  python3 dead_companies.py                      # all sources, 5 pages of NCLT orders
  python3 dead_companies.py --nclt-pages 0 --skip bse
Research tool, not SEBI-registered advice.
"""
import argparse, csv, datetime as dt, html, io, json, os, re, subprocess, sys, time, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "detectors"))
import fein_common as C  # noqa: E402

IBBI = "https://ibbi.gov.in/en/"
NSE_ARCH = "https://nsearchives.nseindia.com/content/equities/"
OUTDIR = os.path.join(ROOT, "research_notes", "Universe")
GAP = 1.5
_last = [0.0]


def curl(url, tries=4, timeout=180):
    err = None
    for i in range(tries):
        wait = GAP - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = subprocess.run(["curl", "-sS", "-L", "--compressed", "-A", "Mozilla/5.0", "--max-time", str(timeout),
                                "-w", "\n%{http_code}", url], capture_output=True, timeout=timeout + 30)
            body, _, code = r.stdout.rpartition(b"\n")
            if code.strip() == b"200" and body:
                return body.decode("utf-8", "replace")
            err = f"HTTP {code.decode().strip()} {r.stderr.decode()[:120]}"
        except (subprocess.TimeoutExpired, OSError) as e:
            err = str(e)
        if i < tries - 1:
            time.sleep(5 * 2 ** i)
    raise RuntimeError(f"fetch failed: {url} ({err})")


def d_iso(s, fmts=("%d-%m-%Y", "%d-%b-%y", "%d %b, %Y", "%d-%b-%Y")):
    s = (s or "").strip()
    for f in fmts:
        try:
            return dt.datetime.strptime(s, f).date().isoformat()
        except ValueError:
            pass
    return ""


# ---------- sources ----------
def ibbi_pa(kind):
    ann = {"cirp": "Public Announcement of Corporate Insolvency Resolution Process",
           "liq": "Public Announcement of Liquidation Process"}[kind]
    url = IBBI + "public-announcement?" + urllib.parse.urlencode({"ann": ann, "export_excel": "export_excel"})
    txt = curl(url)
    rows = list(csv.reader(io.StringIO(txt), delimiter="\t"))
    head = [h.strip().lower() for h in rows[0]]
    col = lambda name: next(i for i, h in enumerate(head) if h.startswith(name))
    di, ni, ci, ai = col("date of announcement"), col("name of corporate debtor"), col("cin"), col("name of applicant")
    out = []
    for r in rows[1:]:
        if len(r) <= ci:
            continue
        d = d_iso(r[di])
        if d and d < "2016-12-01":     # IBC started 1-Dec-2016; earlier dates are placeholders (01-01-1970)
            d = ""
        out.append({"source": f"ibbi_{kind}", "event": "cirp_public_announcement" if kind == "cirp" else "liquidation_order",
                    "event_date": d, "company": html.unescape(r[ni].strip()), "cin": r[ci].strip().upper(),
                    "remarks": "applicant: " + html.unescape(r[ai].strip()), "url": IBBI + "public-announcement"})
    return out


def ibbi_nclt(pages):
    out = []
    for p in range(1, pages + 1):
        url = IBBI + f"orders/nclt?page={p}"
        page = curl(url, timeout=60)
        body = page[page.find("reporttable"):]
        for tr in re.findall(r"<tr>(.*?)</tr>", body, re.S):
            tds = re.findall(r"<td>(.*?)</td>", tr, re.S)
            if len(tds) < 4:
                continue
            link = re.search(r"href=\"?([^\s\">]+)", tds[2])
            subj = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", tds[2]))).strip()
            subj = re.sub(r"\(\s*[\d.]+\s*[KMG]B\)\s*$", "", subj).strip()
            m = re.match(r"In the matter of\s+(.+?)\s*(\[|$)", subj, re.I)
            remark = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", tds[3]))).strip()
            out.append({"source": "ibbi_nclt", "event": "nclt_order", "event_date": d_iso(re.sub(r"\s+", " ", tds[1])),
                        "company": (m.group(1) if m else subj).strip(" ,"), "cin": "", "remarks": f"{remark} | {subj}"[:300],
                        "url": urllib.parse.urljoin("https://ibbi.gov.in/", link.group(1)) if link else url})
    return out


def nse_lists():
    C.log.disabled = True
    out = []
    for r in C.read_csv_text(C.http_get(NSE_ARCH + "delisted.csv", as_text=True)):
        typ = (r.get("Type of Delisting") or "").strip()
        out.append({"source": "nse_delisted", "event": "delisted_" + re.sub(r"\W+", "_", typ.lower()).strip("_"),
                    "event_date": d_iso(r.get("Delisted Date")), "company": r.get("Company", ""), "nse_symbol": r.get("Symbol", ""),
                    "remarks": typ, "url": NSE_ARCH + "delisted.csv"})
    for r in C.read_csv_text(C.http_get(NSE_ARCH + "suspension.csv", as_text=True)):
        out.append({"source": "nse_suspended", "event": "suspended", "event_date": d_iso(r.get("Date of Suspension")),
                    "company": r.get("Company", ""), "nse_symbol": r.get("Symbol", ""), "remarks": "",
                    "url": NSE_ARCH + "suspension.csv"})
    active = C.read_csv_text(C.http_get(NSE_ARCH + "EQUITY_L.csv", as_text=True))
    return out, active


def bse_list(status):
    data, url = C.bse_api("ListofScripData/w", Group="", Scripcode="", industry="", segment="Equity", status=status)
    return data if isinstance(data, list) else [], url


# ---------- mapping ----------
def build_maps(bse_all, nse_active, nse_dead):
    by_name = {}

    def add(name, **ids):
        k = C.norm_name(name)
        if not k:
            return
        cur = by_name.setdefault(k, {})
        for f, v in ids.items():
            if v:
                if cur.get(f) and cur[f] != v:
                    cur[f] = "?"          # two different ids for one name -> ambiguous
                else:
                    cur[f] = v
    for r in bse_all:
        for nm in (r.get("Issuer_Name"), r.get("Scrip_Name")):
            add(nm, bse_code=r.get("SCRIP_CD"), isin=r.get("ISIN_NUMBER"))
    for r in nse_active:
        add(r.get("NAME OF COMPANY"), nse_symbol=r.get("SYMBOL"), isin=r.get("ISIN NUMBER"))
    for r in nse_dead:
        add(r["company"], nse_symbol=r.get("nse_symbol"))
    return by_name


def apply_map(row, by_name):
    hit = by_name.get(C.norm_name(row["company"]))
    if not hit:
        row.setdefault("match", "")
        return row
    amb = [f for f, v in hit.items() if v == "?"]
    for f, v in hit.items():
        if v != "?" and not row.get(f):
            row[f] = v
    row["match"] = "name" + (" (ambiguous: " + ",".join(amb) + ")" if amb else "")
    return row


COLS = ["source", "event", "event_date", "company", "cin", "nse_symbol", "bse_code", "isin", "match", "remarks", "url"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--nclt-pages", type=int, default=5)
    p.add_argument("--skip", default="", help="comma list of: ibbi,nclt,nse,bse")
    p.add_argument("--all-ibbi", action="store_true", help="keep every IBBI row, not just listed/matched ones")
    p.add_argument("--out", default=OUTDIR)
    a = p.parse_args()
    skip = set(filter(None, a.skip.split(",")))
    rows, bse_all, nse_active, status = [], [], [], {}

    def step(name, fn):
        try:
            got = fn()
            status[name] = f"ok {len(got) if isinstance(got, list) else ''}".strip()
            return got
        except Exception as e:
            status[name] = f"FAILED {str(e)[:150]}"
            print(f"{name}: {status[name]}", file=sys.stderr)
            return []
    nse_dead = []
    if "nse" not in skip:
        got = step("nse", nse_lists)
        if got:
            nse_dead, nse_active = got
            rows += nse_dead
    if "bse" not in skip:
        for st in ("Delisted", "Suspended", "Active"):
            data = step(f"bse_{st.lower()}", lambda st=st: bse_list(st)[0])
            bse_all += data
            if st != "Active":
                for r in data:
                    rows.append({"source": f"bse_{st.lower()}", "event": st.lower(), "event_date": "",
                                 "company": r.get("Issuer_Name") or r.get("Scrip_Name", ""), "bse_code": r.get("SCRIP_CD", ""),
                                 "isin": r.get("ISIN_NUMBER", ""), "remarks": f"scrip_id {r.get('scrip_id', '')}, group {r.get('GROUP', '')}",
                                 "url": r.get("NSURL", ""), "match": "exchange"})
    by_name = build_maps(bse_all, nse_active, nse_dead)
    ibbi = []
    if "ibbi" not in skip:
        ibbi += step("ibbi_cirp", lambda: ibbi_pa("cirp"))
        ibbi += step("ibbi_liq", lambda: ibbi_pa("liq"))
    if "nclt" not in skip and a.nclt_pages:
        ibbi += step("ibbi_nclt", lambda: ibbi_nclt(a.nclt_pages))
    n_ibbi = len(ibbi)
    for r in ibbi:
        apply_map(r, by_name)
        listed = r["cin"].startswith("L")
        if listed and not r.get("match"):
            r["match"] = "listed_cin_unmatched"
        if a.all_ibbi or listed or r.get("match"):
            rows.append(r)
    for r in rows:
        if r["source"].startswith(("nse_", "bse_")) and not r.get("isin"):
            apply_map(r, by_name)
    os.makedirs(a.out, exist_ok=True)
    day = dt.date.today().isoformat()
    path = os.path.join(a.out, f"india_dead_companies_{day}.csv")
    rows.sort(key=lambda r: (r["source"], r.get("event_date") or "", r["company"]))
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLS)
        for r in rows:
            w.writerow([r.get(c, "") for c in COLS])
    summ = {}
    for r in rows:
        summ[r["source"]] = summ.get(r["source"], 0) + 1
    print(json.dumps({"written": path, "rows": len(rows), "ibbi_rows_fetched": n_ibbi, "by_source": summ,
                      "steps": status}, indent=1))
    return 0 if all(not v.startswith("FAILED") for v in status.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
