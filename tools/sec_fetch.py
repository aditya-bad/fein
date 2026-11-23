#!/usr/bin/env python3
"""Polite SEC EDGAR fetcher (standard library only).

Tested live 2026-11-20 (all HTTP 200 with a descriptive User-Agent):
  data.sec.gov/submissions/CIK##########.json      filing history + company metadata
  data.sec.gov/api/xbrl/companyfacts/CIK##########.json   every XBRL fact a company filed
  data.sec.gov/api/xbrl/companyconcept/CIK##########/us-gaap/TAG.json
  data.sec.gov/api/xbrl/frames/us-gaap/TAG/USD/CY2024.json   one fact, all companies
  efts.sec.gov/LATEST/search-index?q=...&forms=...&startdt=...&enddt=...   full-text search (2001+)
  www.sec.gov/Archives/edgar/data/CIK/ACCESSIONNODASH/index.json   files inside a filing
  www.sec.gov/files/company_tickers.json            ticker -> CIK map

SEC fair-access rules: declare who you are in the User-Agent, stay <= 10 requests/s.
This tool sends "fein-research admin@example.com" and spaces requests >= 0.15 s
(about 6-7 req/s), backs off on 429/503. Override UA with env SEC_UA if needed.

Usage (TICKER may also be a CIK number, e.g. 1067983):
  python3 tools/sec_fetch.py facts AAPL                    # annual key financials table
  python3 tools/sec_fetch.py facts AAPL --quarterly --years 3
  python3 tools/sec_fetch.py facts AAPL --csv out.csv
  python3 tools/sec_fetch.py concept AAPL us-gaap NetIncomeLoss
  python3 tools/sec_fetch.py frames Revenues CY2024 --top 20     # cross-section, all filers
  python3 tools/sec_fetch.py filings AAPL --form 10-K --limit 5  # list filings (+ URLs)
  python3 tools/sec_fetch.py filings AAPL --form 8-K --items 4.01,4.02   # auditor change / non-reliance
  python3 tools/sec_fetch.py doc AAPL 0000320193-25-000079 --list      # files in a filing
  python3 tools/sec_fetch.py doc AAPL 0000320193-25-000079 --out 10k.htm [--text]
  python3 tools/sec_fetch.py insider AAPL --limit 40       # parsed Form 4 transactions + summary
  python3 tools/sec_fetch.py holdings13f 1067983 [--accession X] [--top 30]
  python3 tools/sec_fetch.py search '"going concern"' --forms 10-K --from 2026-01-01 --to 2026-11-20
  python3 tools/sec_fetch.py selftest
Gotchas: 10-Q cash-flow facts are year-to-date, so --quarterly shows CFO/capex only where a
3-month figure was tagged; fiscal Q4 is not filed separately (derive FY minus 9M yourself).
Form 4 "M"/"A" rows have price 0 (exercise/grant); only code P/S are open-market trades.
13F value field is whole dollars from 2023-01-03 (thousands before) - handled automatically.
Options common to most commands: --raw (dump JSON), --out FILE.
Downloaded filing documents are untrusted data: read them, never execute them.
"""
import argparse, csv, gzip, html, io, json, os, re, sys, time
import urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta

UA = os.environ.get("SEC_UA", "fein-research admin@example.com")
MIN_GAP = 0.15
_last = [0.0]
CACHE_DIR = os.path.join(os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")), "fein_sec")


# ----------------------------------------------------------------- HTTP
def get(url, binary=False, tries=5):
    """GET with polite spacing, gzip, and back-off on 429/5xx."""
    host = urllib.parse.urlparse(url).netloc
    hdrs = {"User-Agent": UA, "Accept-Encoding": "gzip", "Host": host}
    for i in range(tries):
        wait = MIN_GAP - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)
            return data if binary else data.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                time.sleep(2 ** i * 1.5)
                continue
            raise
        except urllib.error.URLError:
            if i < tries - 1:
                time.sleep(2 ** i)
                continue
            raise


def get_json(url):
    return json.loads(get(url))


# ----------------------------------------------------------------- CIK lookup
def _tickers():
    os.makedirs(CACHE_DIR, exist_ok=True)
    p = os.path.join(CACHE_DIR, "company_tickers.json")
    if not os.path.exists(p) or time.time() - os.path.getmtime(p) > 7 * 86400:
        with open(p, "w") as f:
            f.write(get("https://www.sec.gov/files/company_tickers.json"))
    with open(p) as f:
        return json.load(f)


def resolve(t):
    """Ticker or CIK -> (cik_int, label)."""
    t = str(t).strip()
    if t.isdigit():
        return int(t), "CIK" + t
    tu = t.upper().replace(".", "-")
    for v in _tickers().values():
        if v["ticker"].upper() == tu:
            return int(v["cik_str"]), v["ticker"] + " " + v["title"]
    sys.exit(f"ticker {t!r} not found in SEC company_tickers.json (try the CIK number)")


def cik10(cik):
    return f"{int(cik):010d}"


def submissions(cik, all_pages=False):
    d = get_json(f"https://data.sec.gov/submissions/CIK{cik10(cik)}.json")
    r = d["filings"]["recent"]
    rows = [dict(zip(r.keys(), vals)) for vals in zip(*r.values())]
    if all_pages:
        for f in d["filings"].get("files", []):
            o = get_json("https://data.sec.gov/submissions/" + f["name"])
            rows += [dict(zip(o.keys(), vals)) for vals in zip(*o.values())]
    return d, rows


def archive_url(cik, accession, name=""):
    return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession.replace('-', '')}/{name}"


def filing_index(cik, accession):
    return get_json(archive_url(cik, accession, "index.json"))["directory"]["item"]


# ----------------------------------------------------------------- facts
# Each metric: list of (taxonomy, tag, unit) tried in order; first with data wins per period,
# so companies that switched tags (e.g. Revenues -> RevenueFromContract...) get merged.
METRICS = [
    ("revenue", [("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax", "USD"),
                 ("us-gaap", "Revenues", "USD"), ("us-gaap", "SalesRevenueNet", "USD"),
                 ("us-gaap", "RevenueFromContractWithCustomerIncludingAssessedTax", "USD")]),
    ("gross_profit", [("us-gaap", "GrossProfit", "USD")]),
    ("op_income", [("us-gaap", "OperatingIncomeLoss", "USD")]),
    ("net_income", [("us-gaap", "NetIncomeLoss", "USD"), ("us-gaap", "ProfitLoss", "USD")]),
    ("eps_diluted", [("us-gaap", "EarningsPerShareDiluted", "USD/shares")]),
    ("cfo", [("us-gaap", "NetCashProvidedByUsedInOperatingActivities", "USD"),
             ("us-gaap", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations", "USD")]),
    ("capex", [("us-gaap", "PaymentsToAcquirePropertyPlantAndEquipment", "USD"),
               ("us-gaap", "PaymentsToAcquireProductiveAssets", "USD")]),
    ("sbc", [("us-gaap", "ShareBasedCompensation", "USD"),
             ("us-gaap", "AllocatedShareBasedCompensationExpense", "USD")]),
    ("buybacks", [("us-gaap", "PaymentsForRepurchaseOfCommonStock", "USD")]),
    ("dividends", [("us-gaap", "PaymentsOfDividends", "USD"),
                   ("us-gaap", "PaymentsOfDividendsCommonStock", "USD")]),
    ("diluted_shares", [("us-gaap", "WeightedAverageNumberOfDilutedSharesOutstanding", "shares")]),
    # instants (balance sheet)
    ("shares_out", [("dei", "EntityCommonStockSharesOutstanding", "shares"),
                    ("us-gaap", "CommonStockSharesOutstanding", "shares")]),
    ("cash", [("us-gaap", "CashAndCashEquivalentsAtCarryingValue", "USD"),
              ("us-gaap", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", "USD")]),
    ("lt_debt", [("us-gaap", "LongTermDebtNoncurrent", "USD"), ("us-gaap", "LongTermDebt", "USD")]),
    ("equity", [("us-gaap", "StockholdersEquity", "USD"),
                ("us-gaap", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest", "USD")]),
    ("goodwill", [("us-gaap", "Goodwill", "USD")]),
    ("receivables", [("us-gaap", "AccountsReceivableNetCurrent", "USD")]),
    ("inventory", [("us-gaap", "InventoryNet", "USD")]),
]
INSTANT = {"shares_out", "cash", "lt_debt", "equity", "goodwill", "receivables", "inventory"}


def _days(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def _series(facts, tax, tag, unit, quarterly, instant):
    """Return {period_end: (val, filed, form, accn)} de-duplicated, latest filing wins."""
    try:
        pts = facts["facts"][tax][tag]["units"][unit]
    except KeyError:
        return {}
    out = {}
    for p in pts:
        form = p.get("form", "")
        if not (form.startswith("10-K") or form.startswith("10-Q") or form.startswith("20-F")
                or form.startswith("40-F")):
            continue
        if instant:
            if "start" in p:
                continue
            if not quarterly and not (form.startswith("10-K") or form.startswith("20-F")
                                      or form.startswith("40-F")):
                continue
        else:
            if "start" not in p:
                continue
            d = _days(p["start"], p["end"])
            if quarterly and not (80 <= d <= 100):
                continue
            if not quarterly and not (350 <= d <= 380):
                continue
        k = p["end"]
        if k not in out or p.get("filed", "") > out[k][1]:
            out[k] = (p["val"], p.get("filed", ""), form, p.get("accn", ""))
    return out


def company_facts(cik):
    return get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10(cik)}.json")


def build_table(facts, quarterly=False, years=10):
    table = {}
    used = {}
    for name, cands in METRICS:
        inst = name in INSTANT
        merged = {}
        for tax, tag, unit in cands:
            s = _series(facts, tax, tag, unit, quarterly, inst)
            for k, v in s.items():
                if k not in merged:
                    merged[k] = v
                    used.setdefault(name, set()).add(tag)
        for k, v in merged.items():
            table.setdefault(k, {})[name] = v[0]
    # instants: dei share counts are dated at cover date, not period end -> snap to nearest period
    ends = sorted(k for k, row in table.items() if any(m not in INSTANT for m in row))
    if ends:
        snapped = {}
        for k, row in table.items():
            if k in ends:
                snapped.setdefault(k, {}).update(row)
                continue
            near = min(ends, key=lambda e: abs(_days(e, k)))
            if abs(_days(near, k)) <= 120:
                tgt = snapped.setdefault(near, {})
                for m, v in row.items():
                    tgt.setdefault(m, v)
        table = snapped
    for row in table.values():
        if "cfo" in row and "capex" in row:
            row["fcf"] = row["cfo"] - row["capex"]
    keys = sorted(table)
    cutoff = (date.today() - timedelta(days=366 * years)).isoformat()
    keys = [k for k in keys if k >= cutoff]
    return keys, table, used


COLS = ["revenue", "gross_profit", "op_income", "net_income", "eps_diluted", "cfo", "capex", "fcf",
        "sbc", "buybacks", "dividends", "diluted_shares", "shares_out", "cash", "lt_debt", "equity",
        "goodwill", "receivables", "inventory"]


def _fmt(v, col):
    if v is None:
        return "-"
    if col == "eps_diluted":
        return f"{v:.2f}"
    if abs(v) >= 1e9:
        return f"{v/1e9:.2f}B"
    if abs(v) >= 1e6:
        return f"{v/1e6:.1f}M"
    return f"{v:,.0f}"


def cmd_facts(a):
    cik, label = resolve(a.ticker)
    f = company_facts(cik)
    keys, table, used = build_table(f, a.quarterly, a.years)
    if a.raw:
        print(json.dumps({k: table[k] for k in keys}, indent=1))
        return
    if a.csv:
        with open(a.csv, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["period_end"] + COLS)
            for k in keys:
                w.writerow([k] + [table[k].get(c, "") for c in COLS])
        print(f"wrote {a.csv} ({len(keys)} periods)")
    print(f"{f.get('entityName')} ({label}) CIK {cik} - {'quarterly' if a.quarterly else 'annual'} "
          f"XBRL facts as filed (latest amendment wins); USD unless noted")
    cols = [c for c in COLS if any(c in table[k] for k in keys)]
    width = 11
    print("metric".ljust(15) + "".join(k.rjust(width) for k in keys))
    for c in cols:
        print(c.ljust(15) + "".join(_fmt(table[k].get(c), c).rjust(width) for k in keys))
    # derived checks useful for red flags
    if len(keys) >= 2:
        k0, k1 = keys[-2], keys[-1]
        r0, r1 = table[k0], table[k1]
        notes = []
        if r1.get("sbc") and r1.get("fcf"):
            notes.append(f"SBC / FCF {k1}: {r1['sbc']/r1['fcf']:.0%}" if r1["fcf"] > 0 else
                         f"SBC {k1} {_fmt(r1['sbc'],'sbc')} with negative FCF")
        if r1.get("net_income") and r1.get("cfo") and r1["net_income"] > 0:
            notes.append(f"CFO / net income {k1}: {r1['cfo']/r1['net_income']:.2f}")
        if r0.get("diluted_shares") and r1.get("diluted_shares"):
            notes.append(f"diluted share change {k0}->{k1}: {r1['diluted_shares']/r0['diluted_shares']-1:+.1%}")
        if r0.get("receivables") and r1.get("receivables") and r0.get("revenue") and r1.get("revenue"):
            notes.append(f"receivables growth {r1['receivables']/r0['receivables']-1:+.0%} vs revenue "
                         f"growth {r1['revenue']/r0['revenue']-1:+.0%}")
        if notes:
            print("\nchecks: " + " | ".join(notes))
    print("\ntags used: " + "; ".join(f"{k}={','.join(sorted(v))}" for k, v in used.items()))


def cmd_concept(a):
    cik, label = resolve(a.ticker)
    d = get_json(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik10(cik)}/{a.taxonomy}/{a.tag}.json")
    if a.raw:
        print(json.dumps(d, indent=1))
        return
    print(f"{d.get('entityName')} {a.taxonomy}:{a.tag} - {d.get('label')}")
    for unit, pts in d["units"].items():
        print(f"[{unit}]")
        for p in pts[-a.limit:]:
            print(f"  {p.get('start','          ')} {p['end']} {p['val']:>18,} {p.get('form',''):6} "
                  f"fy{p.get('fy')} {p.get('fp')} filed {p.get('filed')} {p.get('accn')}")


def cmd_frames(a):
    unit = a.unit or ("USD-per-shares" if "PerShare" in a.tag else "USD")  # frames API spells per-share units with "-per-"
    d = get_json(f"https://data.sec.gov/api/xbrl/frames/{a.taxonomy}/{a.tag}/{unit}/{a.period}.json")
    rows = sorted(d["data"], key=lambda x: -x["val"])
    if a.raw:
        print(json.dumps(rows[:a.top], indent=1))
        return
    print(f"{a.taxonomy}:{a.tag} {unit} {a.period}: {d.get('pts')} companies. Top {a.top}:")
    print("  (frames are raw filer data: scaling errors exist, e.g. a value 1000x too big - sanity-check outliers)")
    for x in rows[:a.top]:
        print(f"  {x['val']:>20,.0f}  CIK {x['cik']:>8}  {x['entityName'][:50]}  ({x['end']})")


# ----------------------------------------------------------------- filings / docs
def cmd_filings(a):
    cik, label = resolve(a.ticker)
    d, rows = submissions(cik, a.all)
    forms = [x.strip().upper() for x in a.form.split(",")] if a.form else None
    items = set(x.strip() for x in a.items.split(",")) if a.items else None
    out = []
    for r in rows:
        if forms and r["form"].upper() not in forms:
            continue
        if items and not (items & set(r.get("items", "").split(","))):
            continue
        out.append(r)
        if len(out) >= a.limit:
            break
    if a.raw:
        print(json.dumps(out, indent=1))
        return
    print(f"{d['name']} CIK {cik} SIC {d.get('sic')} {d.get('sicDescription')} FYE {d.get('fiscalYearEnd')} "
          f"tickers {d.get('tickers')}")
    for r in out:
        print(f"{r['filingDate']} {r['form']:8} {r['accessionNumber']} items={r.get('items') or '-':10} "
              f"{archive_url(cik, r['accessionNumber'], r['primaryDocument'])}")


def html_to_text(s):
    s = re.sub(r"(?is)<(script|style|ix:header).*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</(p|div|tr|li|h\d)>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n\n", s).strip()


def cmd_doc(a):
    cik, _ = resolve(a.ticker)
    items = filing_index(cik, a.accession)
    if a.list or not (a.file or a.out):
        for it in items:
            print(f"{it.get('size') or '':>10} {it['name']}  {archive_url(cik, a.accession, it['name'])}")
        return
    name = a.file
    if not name:  # pick primary: largest .htm that is not an index / exhibit
        cands = [it for it in items if re.search(r"\.(htm|html|txt|xml)$", it["name"], re.I)
                 and "index" not in it["name"] and not it["name"].startswith("R")]
        cands.sort(key=lambda it: -int(it.get("size") or 0))
        name = cands[0]["name"]
    data = get(archive_url(cik, a.accession, name), binary=True)
    if a.text:
        data = html_to_text(data.decode("utf-8", "replace")).encode()
    with open(a.out, "wb") as fh:
        fh.write(data)
    print(f"saved {name} -> {a.out} ({len(data):,} bytes)")


# ----------------------------------------------------------------- Form 4
CODES = {"P": "open-mkt BUY", "S": "open-mkt SELL", "A": "grant/award", "M": "option exercise",
         "F": "tax withholding", "G": "gift", "C": "conversion", "D": "disposed to issuer",
         "X": "option exercise (in-the-money)", "J": "other", "W": "will/inheritance"}


def _t(el, path):
    x = el.find(path)
    return x.text.strip() if x is not None and x.text else ""


def parse_form4(xml_text):
    root = ET.fromstring(xml_text)
    owners = []
    for ro in root.findall("reportingOwner"):
        rel = ro.find("reportingOwnerRelationship")
        role = []
        if rel is not None:
            if _t(rel, "isDirector") in ("1", "true"): role.append("Dir")
            if _t(rel, "isOfficer") in ("1", "true"): role.append(_t(rel, "officerTitle") or "Officer")
            if _t(rel, "isTenPercentOwner") in ("1", "true"): role.append("10%")
        owners.append((_t(ro, "reportingOwnerId/rptOwnerName"), "/".join(role)))
    plan = _t(root, "aff10b5One") in ("1", "true")
    foot = " ".join((f.text or "") for f in root.iter("footnote"))
    if not plan and re.search(r"10b5-1", foot):
        plan = True
    tx = []
    for t in root.findall("nonDerivativeTable/nonDerivativeTransaction"):
        sh = _t(t, "transactionAmounts/transactionShares/value")
        px = _t(t, "transactionAmounts/transactionPricePerShare/value")
        tx.append({
            "date": _t(t, "transactionDate/value"),
            "code": _t(t, "transactionCoding/transactionCode"),
            "ad": _t(t, "transactionAmounts/transactionAcquiredDisposedCode/value"),
            "shares": float(sh) if sh else 0.0,
            "price": float(px) if px else 0.0,
            "after": _t(t, "postTransactionAmounts/sharesOwnedFollowingTransaction/value"),
            "direct": _t(t, "ownershipNature/directOrIndirectOwnership/value"),
        })
    return {"issuer": _t(root, "issuer/issuerTradingSymbol"), "owners": owners, "plan_10b5_1": plan,
            "tx": tx}


def form4_xml_name(cik, accession):
    for it in filing_index(cik, accession):
        n = it["name"]
        if n.lower().endswith(".xml") and "index" not in n.lower():
            return n
    return None


def cmd_insider(a):
    cik, label = resolve(a.ticker)
    d, rows = submissions(cik, a.all)
    f4 = [r for r in rows if r["form"] in ("4", "4/A")]
    if a.since:
        f4 = [r for r in f4 if r["filingDate"] >= a.since]
    f4 = f4[:a.limit]
    print(f"{d['name']}: parsing {len(f4)} Form 4 filings (issuer CIK {cik})", file=sys.stderr)
    out = []
    for r in f4:
        try:
            name = form4_xml_name(cik, r["accessionNumber"])
            if not name:
                continue
            p = parse_form4(get(archive_url(cik, r["accessionNumber"], name)))
        except Exception as e:  # keep going on one bad filing
            print(f"  skip {r['accessionNumber']}: {e}", file=sys.stderr)
            continue
        for t in p["tx"]:
            out.append({"filed": r["filingDate"], "accession": r["accessionNumber"],
                        "owner": p["owners"][0][0] if p["owners"] else "", "role":
                        p["owners"][0][1] if p["owners"] else "", "plan_10b5_1": p["plan_10b5_1"], **t,
                        "value": round(t["shares"] * t["price"], 2)})
    if a.raw:
        print(json.dumps(out, indent=1))
        return
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(out, fh, indent=1)
    for t in out:
        print(f"{t['date']} {t['code']:1} {CODES.get(t['code'], t['code'])[:16]:16} {t['shares']:>12,.0f} "
              f"@ {t['price']:>9.2f} = {t['value']:>14,.0f}  {'10b5-1' if t['plan_10b5_1'] else '      '} "
              f"{t['owner'][:24]:24} {t['role'][:30]}")
    buys = [t for t in out if t["code"] == "P"]
    sells = [t for t in out if t["code"] == "S"]
    disc_sells = [t for t in sells if not t["plan_10b5_1"]]
    print("\nSUMMARY (open-market only; grants/exercises/tax excluded)")
    print(f"  buys:  {len(buys)} tx, {len({t['owner'] for t in buys})} insiders, "
          f"${sum(t['value'] for t in buys):,.0f}")
    print(f"  sells: {len(sells)} tx, {len({t['owner'] for t in sells})} insiders, "
          f"${sum(t['value'] for t in sells):,.0f}  (non-10b5-1: {len(disc_sells)} tx, "
          f"${sum(t['value'] for t in disc_sells):,.0f})")
    # cluster detection: >=3 distinct insiders on the same side inside any 30-day window
    for side, lst in (("BUY", buys), ("SELL (non-plan)", disc_sells)):
        lst = sorted(lst, key=lambda t: t["date"])
        best = (0, None)
        for i, t in enumerate(lst):
            end = (date.fromisoformat(t["date"]) + timedelta(days=30)).isoformat()
            names = {x["owner"] for x in lst[i:] if x["date"] <= end}
            if len(names) > best[0]:
                best = (len(names), t["date"])
        if best[0] >= 3:
            print(f"  CLUSTER {side}: {best[0]} distinct insiders within 30 days from {best[1]}")
    print("  Evidence: open-market BUYS (code P), esp. by several insiders, small caps, and non-routine "
          "traders, carry the signal; sales are mostly noise unless clustered and off-plan.")


# ----------------------------------------------------------------- 13F
def cmd_13f(a):
    cik, label = resolve(a.ticker)
    d, rows = submissions(cik)
    f13 = [r for r in rows if r["form"] in ("13F-HR", "13F-HR/A")]
    if not f13:
        sys.exit(f"{d['name']}: no 13F-HR filings in recent submissions")
    r = next((x for x in f13 if x["accessionNumber"] == a.accession), None) if a.accession else f13[0]
    if r is None:
        sys.exit("accession not found among 13F filings")
    items = filing_index(cik, r["accessionNumber"])
    xmls = [it["name"] for it in items if it["name"].lower().endswith(".xml")
            and it["name"].lower() != "primary_doc.xml"]
    if not xmls:
        sys.exit("no information-table XML found (pre-2013 13Fs are text-only)")
    root = ET.fromstring(get(archive_url(cik, r["accessionNumber"], xmls[0])))
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"
    agg = {}
    for it in root.iter(ns + "infoTable"):
        g = lambda p: (it.find(ns + p).text or "").strip() if it.find(ns + p) is not None else ""
        name, cusip = g("nameOfIssuer"), g("cusip")
        val = float(g("value") or 0)
        sh = float((it.find(f"{ns}shrsOrPrnAmt/{ns}sshPrnamt").text or 0)) if it.find(
            f"{ns}shrsOrPrnAmt/{ns}sshPrnamt") is not None else 0
        pc = g("putCall")
        key = (name, cusip, pc)
        e = agg.setdefault(key, [0.0, 0.0, g("titleOfClass")])
        e[0] += val
        e[1] += sh
    rowsv = sorted(agg.items(), key=lambda kv: -kv[1][0])
    total = sum(v[0] for v in agg.values())
    # Since 2023-01-03 the value field is in whole dollars (before: thousands).
    mult = 1 if r["filingDate"] >= "2023-01-03" else 1000
    if a.raw:
        print(json.dumps([{"issuer": k[0], "cusip": k[1], "putCall": k[2], "value_usd": v[0] * mult,
                           "shares": v[1]} for k, v in rowsv], indent=1))
        return
    print(f"{d['name']} 13F {r['form']} filed {r['filingDate']} period {r.get('reportDate')} "
          f"{r['accessionNumber']}: {len(agg)} positions, total ${total*mult/1e9:,.2f}B")
    for (name, cusip, pc), (v, sh, cls) in rowsv[:a.top]:
        print(f"  {v*mult/1e6:>12,.1f}M {v/total:6.1%}  {sh:>15,.0f}  {cusip}  {name[:36]} {cls[:10]} {pc}")
    print("Note: 13F = long US-listed positions only, reported up to 45 days after quarter end; "
          "no shorts, no cash, no non-US lines. Confidential-treatment positions may be missing.")


# ----------------------------------------------------------------- full-text search
def cmd_search(a):
    q = {"q": a.query}
    if a.forms:
        q["forms"] = a.forms
    if a.frm or a.to:
        q.update({"dateRange": "custom", "startdt": a.frm or "2001-01-01",
                  "enddt": a.to or date.today().isoformat()})
    if a.page > 1:
        q["from"] = str((a.page - 1) * 100)
    if a.ciks:
        q["ciks"] = ",".join(cik10(resolve(c)[0]) for c in a.ciks.split(","))
    url = "https://efts.sec.gov/LATEST/search-index?" + urllib.parse.urlencode(q)
    d = get_json(url)
    hits = d["hits"]["hits"]
    if a.raw:
        print(json.dumps(hits, indent=1))
        return
    print(f"{d['hits']['total']['value']} hits ({d['hits']['total']['relation']}); showing {len(hits)} "
          f"(EDGAR FTS returns 100 per page; use --raw for all fields)")
    for h in hits[:a.limit]:
        s = h["_source"]
        adsh, fname = h["_id"].split(":", 1)
        cik = s["ciks"][0] if s.get("ciks") else ""
        print(f"{s.get('file_date')} {s.get('file_type','')[:8]:8} {s['display_names'][0][:55]:55} "
              f"items={','.join(s.get('items') or []) or '-'} {archive_url(cik, adsh, fname) if cik else adsh}")


# ----------------------------------------------------------------- self-test
def cmd_selftest(a):
    ok = True

    def check(name, fn):
        nonlocal ok
        try:
            msg = fn()
            print(f"PASS {name}: {msg}")
        except Exception as e:
            ok = False
            print(f"FAIL {name}: {e!r}")

    check("ticker map", lambda: f"AAPL -> CIK {resolve('AAPL')[0]}" if resolve("AAPL")[0] == 320193
          else (_ for _ in ()).throw(AssertionError("AAPL CIK mismatch")))
    check("submissions", lambda: f"{len(submissions(320193)[1])} recent Apple filings")

    def facts():
        keys, t, _ = build_table(company_facts(320193), False, 5)
        last = t[keys[-1]]
        assert last.get("revenue", 0) > 1e11 and last.get("net_income", 0) > 1e10, last
        return f"FY ending {keys[-1]} revenue {_fmt(last['revenue'],'')} NI {_fmt(last['net_income'],'')}"
    check("companyfacts", facts)
    check("companyconcept", lambda: f"{len(get_json('https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/NetIncomeLoss.json')['units']['USD'])} NetIncomeLoss points")
    check("frames", lambda: f"{get_json('https://data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2024.json')['pts']} filers with CY2024 Revenues")
    check("full-text search", lambda: f"{get_json('https://efts.sec.gov/LATEST/search-index?q=%22going%20concern%22&forms=10-K')['hits']['total']['value']} '\"going concern\"' 10-K hits")

    def f4():
        _, rows = submissions(320193)
        r = next(x for x in rows if x["form"] == "4")
        p = parse_form4(get(archive_url(320193, r["accessionNumber"], form4_xml_name(320193, r["accessionNumber"]))))
        return f"{r['filingDate']} {p['owners'][0][0]}: {len(p['tx'])} non-derivative tx, 10b5-1={p['plan_10b5_1']}"
    check("form 4 parse", f4)

    def f13():
        _, rows = submissions(1067983)
        r = next(x for x in rows if x["form"] == "13F-HR")
        names = [it["name"] for it in filing_index(1067983, r["accessionNumber"])]
        assert any(n.endswith(".xml") and n != "primary_doc.xml" for n in names), names
        return f"Berkshire 13F {r['filingDate']} files {names[-2:]}"
    check("13F index", f13)
    print("ALL PASS" if ok else "SOME CHECKS FAILED")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("facts", help="key financials time series from XBRL companyfacts")
    p.add_argument("ticker"); p.add_argument("--quarterly", action="store_true")
    p.add_argument("--years", type=int, default=10); p.add_argument("--csv")
    p.add_argument("--raw", action="store_true"); p.set_defaults(fn=cmd_facts)

    p = sp.add_parser("concept", help="one XBRL concept for one company (all periods)")
    p.add_argument("ticker"); p.add_argument("taxonomy"); p.add_argument("tag")
    p.add_argument("--limit", type=int, default=40); p.add_argument("--raw", action="store_true")
    p.set_defaults(fn=cmd_concept)

    p = sp.add_parser("frames", help="one concept across all companies for a period (CY2024, CY2024Q3I)")
    p.add_argument("tag"); p.add_argument("period"); p.add_argument("--taxonomy", default="us-gaap")
    p.add_argument("--unit"); p.add_argument("--top", type=int, default=25)
    p.add_argument("--raw", action="store_true"); p.set_defaults(fn=cmd_frames)

    p = sp.add_parser("filings", help="list filings, filter by form / 8-K item")
    p.add_argument("ticker"); p.add_argument("--form", help="comma list, e.g. 10-K,10-Q,8-K,DEF 14A,S-1,4")
    p.add_argument("--items", help="8-K items, e.g. 4.01,4.02,5.02"); p.add_argument("--limit", type=int, default=20)
    p.add_argument("--all", action="store_true", help="include older paged history")
    p.add_argument("--raw", action="store_true"); p.set_defaults(fn=cmd_filings)

    p = sp.add_parser("doc", help="list or download files inside a filing")
    p.add_argument("ticker"); p.add_argument("accession"); p.add_argument("--file")
    p.add_argument("--out"); p.add_argument("--list", action="store_true")
    p.add_argument("--text", action="store_true", help="strip HTML to plain text"); p.set_defaults(fn=cmd_doc)

    p = sp.add_parser("insider", help="parse Form 4 insider transactions for an issuer")
    p.add_argument("ticker"); p.add_argument("--limit", type=int, default=40, help="max Form 4 filings")
    p.add_argument("--since", help="YYYY-MM-DD filing date floor"); p.add_argument("--all", action="store_true")
    p.add_argument("--out"); p.add_argument("--raw", action="store_true"); p.set_defaults(fn=cmd_insider)

    p = sp.add_parser("holdings13f", help="13F-HR holdings for an institutional filer (ticker or CIK)")
    p.add_argument("ticker"); p.add_argument("--accession"); p.add_argument("--top", type=int, default=30)
    p.add_argument("--raw", action="store_true"); p.set_defaults(fn=cmd_13f)

    p = sp.add_parser("search", help="EDGAR full-text search (2001+)")
    p.add_argument("query"); p.add_argument("--forms"); p.add_argument("--from", dest="frm")
    p.add_argument("--to"); p.add_argument("--ciks", help="comma list of tickers/CIKs")
    p.add_argument("--limit", type=int, default=25); p.add_argument("--page", type=int, default=1,
                   help="100 hits per page"); p.add_argument("--raw", action="store_true")
    p.set_defaults(fn=cmd_search)

    p = sp.add_parser("selftest", help="live checks of every endpoint"); p.set_defaults(fn=cmd_selftest)
    a = ap.parse_args()
    try:
        a.fn(a)
    except BrokenPipeError:
        sys.stderr.close()
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} for {e.url}")


if __name__ == "__main__":
    main()
