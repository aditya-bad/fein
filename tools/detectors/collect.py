#!/usr/bin/env python3
"""FEIN collector: pull Indian disclosure data and store it (standard library only).

Pulls, for each day in a range (default: yesterday -> today, IST):
  NSE corporate announcements (main board + SME), PIT insider disclosures (Reg 7),
  SAST Reg 29 disclosures, bulk deals and block deals, and BSE announcements (backup).
Once per run it also takes an all-company NSE promoter-pledge snapshot (snapshot date = today).

Raw JSON/CSV is saved gzipped under $FEIN_DATA/raw/YYYY-MM-DD/, normalised rows go into
$FEIN_DATA/fein.sqlite, logs go to $FEIN_DATA/logs/collect.log. FEIN_DATA defaults to ~/fein-data.

Usage:
  python3 collect.py                              # yesterday -> today
  python3 collect.py --from 2026-11-18 --to 2026-11-20
  python3 collect.py --only pledges,deals         # subset: announcements,bse,insider,sast,deals,pledges
  python3 collect.py --no-bse                     # skip the BSE backup feed
  python3 collect.py --selftest                   # tiny live fetch, prints counts, writes nothing
Exit code 0 if at least one dataset succeeded, 1 if everything failed.
"""
import argparse, datetime as dt, gzip, json, os, re, sys, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fein_common as C
from fein_common import log, num, parse_date

DATASETS = ["announcements", "bse", "insider", "sast", "deals", "pledges"]


def save_raw(day, name, data):
    d = os.path.join(C.DATA, "raw", day)
    os.makedirs(d, exist_ok=True)
    with gzip.open(os.path.join(d, name + ".json.gz"), "wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def ddmmyyyy(day):
    y, m, d = day.split("-")
    return f"{d}-{m}-{y}"


def safe_rows(rows, fn, what):
    out, bad = [], 0
    for r in rows or []:
        try:
            x = fn(r)
            if x:
                out.append(x)
        except Exception as e:  # one bad row must not kill the run
            bad += 1
            if bad <= 3:
                log.warning("%s: skipped bad row (%s): %s", what, e, str(r)[:160])
    if bad:
        log.warning("%s: %d bad rows skipped", what, bad)
    return out


# ---------- normalisers ----------
def n_nse_ann(r):
    d = parse_date(r.get("an_dt") or r.get("sort_date"))
    text = (r.get("attchmntText") or "").strip()
    if r.get("voiceSummary"):
        text += "\n[summary] " + r["voiceSummary"].strip()
    return {"source": "NSE", "id": str(r["seq_id"]), "dt": d, "date": d[:10] if d else None,
            "symbol": r.get("symbol"), "bse_code": None, "company": r.get("sm_name"),
            "category": r.get("desc"), "subject": r.get("desc"), "text": text,
            "url": r.get("attchmntFile")}


def n_bse_ann(r):
    d = parse_date(r.get("NEWS_DT") or r.get("DT_TM"))
    m = re.search(r"/stock-share-price/[^/]+/([^/]+)/\d+", r.get("NSURL") or "")
    att = r.get("ATTACHMENTNAME")
    return {"source": "BSE", "id": r["NEWSID"], "dt": d, "date": d[:10] if d else None,
            "symbol": m.group(1).upper() if m else None, "bse_code": str(r.get("SCRIP_CD")),
            "company": r.get("SLONGNAME"),
            "category": " / ".join(x for x in (r.get("CATEGORYNAME"), r.get("SUBCATNAME")) if x),
            "subject": r.get("NEWSSUB"), "text": (r.get("HEADLINE") or "").strip(),
            "url": f"https://www.bseindia.com/xml-data/corpfiling/AttachLive/{att}" if att else r.get("NSURL")}


def n_pit(r):
    d = parse_date(r.get("date"))
    return {"id": str(r.get("pid") or r.get("did")), "dt": d, "date": d[:10] if d else None,
            "symbol": r.get("symbol"), "company": r.get("company"), "person": r.get("acqName"),
            "category": r.get("personCategory"), "mode": r.get("acqMode"),
            "tx_type": r.get("tdpTransactionType"), "sec_type": r.get("secType"),
            "qty": num(r.get("secAcq")), "value": num(r.get("secVal")),
            "before_pct": num(r.get("befAcqSharesPer")), "after_pct": num(r.get("afterAcqSharesPer")),
            "trade_from": parse_date(r.get("acqfromDt")), "trade_to": parse_date(r.get("acqtoDt")),
            "url": r.get("xbrl")}


def n_sast(r):
    d = parse_date(r.get("timestamp") or r.get("sysTime"))
    return {"id": f"{r.get('application_no')}|{(r.get('acquirerName') or '')[:80]}", "dt": d,
            "date": d[:10] if d else None, "symbol": r.get("symbol"), "company": r.get("company"),
            "acquirer": r.get("acquirerName"), "promoter": r.get("promoterType"),
            "reg_type": r.get("regType"), "mode": r.get("acquisitionMode"), "side": r.get("acqSaleType"),
            "shares_acq": num(r.get("noOfShareAcq")), "shares_sale": num(r.get("noOfShareSale")),
            "shares_after": num(r.get("noOfShareAft")), "pct_acq": num(r.get("totAcqShare")),
            "pct_sale": num(r.get("totSaleShare")), "pct_after": num(r.get("totAftShare")),
            "period": r.get("acquirerDate"), "url": r.get("attachement")}


def n_deal(kind):
    def f(r):
        g = lambda *ks: next((r[k] for k in ks if k in r), None)
        qty, price = num(g("Quantity Traded")), num(g("Trade Price / Wght. Avg. Price"))
        return {"date": parse_date(g("Date")), "kind": kind, "symbol": g("Symbol"),
                "company": g("Security Name"), "client": g("Client Name"),
                "side": (g("Buy / Sell", "Buy/Sell") or "").upper(), "qty": qty, "price": price,
                "value_cr": round(qty * price / 1e7, 3) if qty and price else None,
                "remarks": g("Remarks")}
    return f


# ---------- fetchers ----------
def fetch_announcements(con, day):
    rows = []
    for index in ("equities", "sme"):
        data, url = C.nse_api("corporate-announcements", index=index,
                              from_date=ddmmyyyy(day), to_date=ddmmyyyy(day))
        save_raw(day, f"nse_announcements_{index}", data)
        rows += safe_rows(data if isinstance(data, list) else data.get("data"), n_nse_ann, "announcements")
    C.upsert(con, "announcements", rows)
    C.upsert(con, "symbols", [{"symbol": r["symbol"], "name": r["company"], "isin": None,
                               "norm": C.norm_name(r["company"])} for r in rows
                              if r["symbol"] and r["company"] and not known_symbol(con, r["symbol"])])
    return len(rows)


def known_symbol(con, sym):
    return con.execute("SELECT 1 FROM symbols WHERE symbol=?", (sym,)).fetchone() is not None


def fetch_bse(con, day, max_pages=40):
    ymd = day.replace("-", "")
    raw, page = [], 1
    while page <= max_pages:
        data, _ = C.bse_api("AnnSubCategoryGetData/w", pageno=page, strCat=-1, strPrevDate=ymd,
                            strScrip="", strSearch="P", strToDate=ymd, strType="C", subcategory=-1)
        t = data.get("Table") or []
        raw += t
        total = (data.get("Table1") or [{}])[0].get("ROWCNT", 0)
        if not t or len(raw) >= total:
            break
        page += 1
    save_raw(day, "bse_announcements", raw)
    rows = safe_rows(raw, n_bse_ann, "bse")
    C.upsert(con, "announcements", rows)
    return len(rows)


def fetch_insider(con, day):
    data, _ = C.nse_api("corporates-pit", index="equities", from_date=ddmmyyyy(day), to_date=ddmmyyyy(day))
    save_raw(day, "nse_pit", data)
    rows = safe_rows(data.get("data"), n_pit, "insider")
    if not rows and dt.date.fromisoformat(day).weekday() < 5:
        # Seen Nov-2026: the all-market PIT feed returns nothing after ~May-2026. Fall back to
        # per-symbol calls for companies that filed insider/SAST-type news that day.
        syms = [r[0] for r in con.execute(
            "SELECT DISTINCT symbol FROM sast WHERE date=? AND promoter='Y' AND symbol IS NOT NULL "
            "UNION SELECT DISTINCT symbol FROM announcements WHERE date=? AND source='NSE' AND "
            "(category LIKE '%Insider%' OR category LIKE '%Trading Plan%')", (day, day))][:25]
        log.warning("insider %s: all-market PIT feed empty; per-symbol fallback for %d symbols", day, len(syms))
        for s in syms:
            try:
                d2, _ = C.nse_api("corporates-pit", index="equities", symbol=s)
                rows += safe_rows(d2.get("data"), n_pit, "insider")
            except Exception as e:
                log.warning("insider %s: %s", s, e)
    C.upsert(con, "insider_trades", rows)
    return len(rows)


def fetch_sast(con, day):
    data, _ = C.nse_api("corporate-sast-reg29", index="equities", from_date=ddmmyyyy(day), to_date=ddmmyyyy(day))
    save_raw(day, "nse_sast", data)
    rows = safe_rows(data.get("data"), n_sast, "sast")
    C.upsert(con, "sast", rows)
    return len(rows)


def fetch_deals(con, day):
    n = 0
    for kind in ("bulk", "block"):
        # The JSON form of this endpoint is capped at 70 rows; csv=true returns everything.
        url = (C.NSE + "historicalOR/bulk-block-short-deals?" +
               urllib.parse.urlencode({"optionType": f"{kind}_deals", "from": ddmmyyyy(day),
                                       "to": ddmmyyyy(day), "csv": "true"}))
        txt = C.http_get(url, as_text=True)
        raw = C.read_csv_text(txt) if not txt.lstrip().startswith(("{", "[", "<")) else []
        save_raw(day, f"nse_{kind}", raw)
        rows = safe_rows(raw, n_deal(kind), kind)
        C.upsert(con, "deals", rows)
        n += len(rows)
    fetch_share_counts(con, day)
    return n


SHP_TOTAL = re.compile(r'NumberOfFullyPaidUpEquityShares[^>]*contextRef="ShareholdingPattern_ContextI"[^>]*>\s*(\d+)')


def fetch_share_counts(con, day, max_new=60):
    """Share counts for deal symbols that the pledge snapshot does not cover (SME, no-promoter cos).
    Source: total fully paid-up shares in the latest NSE shareholding-pattern XBRL. Cached ~100 days."""
    stale = (C.today_ist() - dt.timedelta(days=100)).isoformat()
    syms = [r[0] for r in con.execute(
        "SELECT DISTINCT symbol FROM deals WHERE date=? AND symbol NOT IN "
        "(SELECT symbol FROM pledges WHERE total_shares>0) AND symbol NOT IN "
        "(SELECT symbol FROM shares WHERE fetched>=?)", (day, stale))][:max_new]
    got = 0
    for s in syms:
        try:
            for index in ("equities", "sme"):
                data, _ = C.nse_api("corporate-share-holdings-master", index=index, symbol=s)
                if isinstance(data, list) and data:
                    break
            if not (isinstance(data, list) and data and data[0].get("xbrl")):
                continue
            m = SHP_TOTAL.search(C.http_get(data[0]["xbrl"], as_text=True))
            if m:
                C.upsert(con, "shares", [{"symbol": s, "as_of": parse_date(data[0].get("date")), "shares": float(m.group(1)),
                                          "source": data[0]["xbrl"], "fetched": C.today_ist().isoformat()}])
                got += 1
        except Exception as e:
            log.warning("share count %s: %s", s, e)
    if syms:
        log.info("share counts: %d/%d deal symbols resolved from SHP XBRL", got, len(syms))


def refresh_symbols(con):
    rows = []
    for path, sym_k, name_k, isin_k in [
            ("content/equities/EQUITY_L.csv", "SYMBOL", "NAME OF COMPANY", "ISIN NUMBER"),
            ("emerge/corporates/content/SME_EQUITY_L.csv", "SYMBOL", "NAME_OF_COMPANY", "ISIN_NUMBER")]:
        try:
            for r in C.read_csv_text(C.http_get(C.NSE_ARCH + path, as_text=True)):
                if r.get(sym_k):
                    rows.append({"symbol": r[sym_k], "name": r.get(name_k), "isin": r.get(isin_k),
                                 "norm": C.norm_name(r.get(name_k))})
        except Exception as e:
            log.warning("symbol list %s: %s", path, e)
    C.upsert(con, "symbols", rows)
    return len(rows)


def name_to_symbol(con):
    m = {}
    for r in con.execute("SELECT symbol, norm FROM symbols WHERE norm IS NOT NULL AND norm<>''"):
        m.setdefault(r["norm"], r["symbol"])
    for r in con.execute("SELECT DISTINCT symbol, company FROM sast WHERE symbol IS NOT NULL"):
        m.setdefault(C.norm_name(r["company"]), r["symbol"])
    return m


def fetch_pledges(con, snap_day):
    refresh_symbols(con)
    data, _ = C.nse_api("corporate-pledgedata", index="equities")
    save_raw(snap_day, "nse_pledge_snapshot", data)
    best = {}
    for r in data.get("data") or []:  # several rows per company possible: keep latest SHP quarter
        k = r.get("comName")
        if k and (k not in best or (parse_date(r.get("shp")) or "") > (parse_date(best[k].get("shp")) or "")):
            best[k] = r
    nmap = name_to_symbol(con)
    unmapped = []

    def f(r):
        sym = nmap.get(C.norm_name(r["comName"]))
        if not sym:
            unmapped.append(r["comName"])
            return None
        return {"snapshot_date": snap_day, "symbol": sym, "company": r["comName"],
                "shp_date": parse_date(r.get("shp")), "promoter_holding_pct": num(r.get("percPromoterHolding")),
                "pledged_pct_of_promoter": num(r.get("percPromoterShares")),
                "pledged_pct_of_equity": num(r.get("percTotShares")),
                "promoter_pledged_shares": num(r.get("totPromoterShares")),
                "promoter_shares": num(r.get("totPromoterHolding")),
                "total_shares": num(r.get("totIssuedShares")), "all_pledged_pct": num(r.get("percSharesPledged")),
                "broadcast_dt": parse_date(r.get("broadcastDt"))}
    rows = safe_rows(list(best.values()), f, "pledges")
    if unmapped:
        log.warning("pledges: %d companies without NSE symbol match, e.g. %s", len(unmapped), unmapped[:5])
    C.upsert(con, "pledges", rows)
    return len(rows)


def days(frm, to):
    d = dt.date.fromisoformat(frm)
    while d <= dt.date.fromisoformat(to):
        yield d.isoformat()
        d += dt.timedelta(days=1)


def run_one(con, name, day, fn):
    try:
        n = fn()
        con.commit()   # one commit per dataset-day
        log.info("%-13s %s rows=%d", name, day, n)
        con.execute("INSERT INTO runs VALUES(datetime('now'),?,?,?,?,?)", (name, day, n, "ok", ""))
        con.commit()
        return True
    except Exception as e:
        log.error("%-13s %s FAILED: %s", name, day, e)
        con.rollback()
        con.execute("INSERT INTO runs VALUES(datetime('now'),?,?,?,?,?)", (name, day, 0, "error", str(e)[:300]))
        con.commit()
        return False


def selftest():
    y = (C.today_ist() - dt.timedelta(days=1)).isoformat()
    print(f"selftest: live tiny fetch for {y} (nothing is written to the data dir)")
    checks = [
        ("NSE announcements", lambda: C.nse_api("corporate-announcements", index="equities",
                                                from_date=ddmmyyyy(y), to_date=ddmmyyyy(y))[0]),
        ("NSE SAST reg29", lambda: C.nse_api("corporate-sast-reg29", index="equities",
                                             from_date=ddmmyyyy(y), to_date=ddmmyyyy(y))[0].get("data")),
        ("NSE PIT (all-market)", lambda: C.nse_api("corporates-pit", index="equities",
                                                   from_date=ddmmyyyy(y), to_date=ddmmyyyy(y))[0].get("data")),
        ("NSE PIT INDOTECH", lambda: C.nse_api("corporates-pit", index="equities", symbol="INDOTECH")[0].get("data")),
        ("NSE pledge INDOTECH", lambda: C.nse_api("corporate-pledgedata", index="equities", symbol="INDOTECH")[0].get("data")),
        ("NSE bulk deals csv", lambda: C.read_csv_text(C.http_get(
            C.NSE + f"historicalOR/bulk-block-short-deals?optionType=bulk_deals&from={ddmmyyyy(y)}&to={ddmmyyyy(y)}&csv=true",
            as_text=True))),
        ("BSE announcements p1", lambda: C.bse_api("AnnSubCategoryGetData/w", pageno=1, strCat=-1,
                                                   strPrevDate=y.replace("-", ""), strScrip="", strSearch="P",
                                                   strToDate=y.replace("-", ""), strType="C", subcategory=-1)[0].get("Table")),
    ]
    ok = 0
    for name, fn in checks:
        try:
            rows = fn() or []
            print(f"  OK   {name:24s} {len(rows)} rows")
            ok += 1
        except Exception as e:
            print(f"  FAIL {name:24s} {e}")
    print(f"selftest: {ok}/{len(checks)} sources answered (0 rows can be normal on holidays; "
          "PIT all-market has been empty since ~May-2026)")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    t = C.today_ist()
    p.add_argument("--from", dest="frm", default=(t - dt.timedelta(days=1)).isoformat(), help="YYYY-MM-DD")
    p.add_argument("--to", default=t.isoformat(), help="YYYY-MM-DD")
    p.add_argument("--only", help="comma list of: " + ",".join(DATASETS))
    p.add_argument("--no-bse", action="store_true")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    C.setup_logging("collect")
    lock = C.single_instance("collect")
    if not lock:
        log.error("another collect.py is still running; exiting")
        return 1
    want = set((a.only or ",".join(DATASETS)).split(","))
    if a.no_bse:
        want.discard("bse")
    con = C.db()
    log.info("collect %s -> %s datasets=%s data=%s", a.frm, a.to, sorted(want), C.DATA)
    results = []
    for day in days(a.frm, a.to):
        # SAST before insider: the PIT fallback uses that day's SAST promoter rows.
        for name, fn in [("announcements", fetch_announcements), ("sast", fetch_sast),
                         ("insider", fetch_insider), ("deals", fetch_deals), ("bse", fetch_bse)]:
            if name in want:
                results.append(run_one(con, name, day, lambda: fn(con, day)))
    if "pledges" in want:
        results.append(run_one(con, "pledges", t.isoformat(), lambda: fetch_pledges(con, t.isoformat())))
    con.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    con.close()
    log.info("collect done: %d/%d steps ok", sum(results), len(results))
    return 0 if any(results) else 1


if __name__ == "__main__":
    sys.exit(main())
