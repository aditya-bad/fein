#!/usr/bin/env python3
"""FEIN detector: run change rules over fein.sqlite and write alerts (standard library only).

Rules (each alert row = date, symbol, rule, details, source URL):
  pledge_up / pledge_cross_10|25|50 / pledge_down   promoter pledge between the two latest snapshots
        (both bases: % of promoter holding = NSE percPromoterShares, % of equity = percTotShares;
         never percSharesPledged, which includes non-promoter pledges - lesson L6)
  pledge_invocation / pledge_release                PIT pledge invoke/revoke rows + announcement text
  insider_buy (>= Rs 1 cr) / insider_sell (>= Rs 5 cr)   promoter, promoter group, director or KMP,
        open-market only (PIT Reg 7)
  sast_promoter_open_market                         promoter open-market buy/sale filed under SAST Reg 29
        (stand-in while the NSE PIT feed is empty; no rupee value is published)
  insider_cluster                                   >= 2 different insiders, same stock, same direction,
        open market, within 30 days
  auditor_resignation / auditor_change / kmp_resignation (CFO, CEO, CS)
  rating_downgrade / rating_not_cooperating / default_delay   announcement keyword rules (NSE; BSE as backup)
  large_deal                                        bulk/block deal >= 1% of equity (or >= Rs 50 cr when the
        share count is unknown)

Alerts already emitted on an earlier run are not repeated (table `alerts`), unless --all.
Output: $FEIN_DATA/alerts/<today IST>.md and .csv = every alert first seen today (re-runs are safe).

Usage:
  python3 detect.py                          # events of the last 3 days up to today (IST)
  python3 detect.py --from 2026-11-18 --to 2026-11-20 [--all]
  python3 detect.py --selftest               # live Indo Tech pledge check + offline rule checks
"""
import argparse, csv, datetime as dt, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fein_common as C
from fein_common import log

INSIDER_CATS = ("promoter", "promoter group", "director", "key managerial personnel")
BUY_MIN, SELL_MIN = 1e7, 5e7          # Rs 1 cr, Rs 5 cr
PLEDGE_STEP, PLEDGE_LEVELS = 2.0, (10, 25, 50)
DEAL_PCT, DEAL_CR_FALLBACK = 1.0, 50.0
CLUSTER_DAYS, CLUSTER_MIN = 30, 2

ROLE = r"(chief financial officer|\bc\.?f\.?o\b|chief executive officer|\bc\.?e\.?o\b|company secretary|compliance officer)"
LEAVE = r"(resign\w*|cessation|step(?:ped|s)? down)"
ANN_RULES = [
    ("auditor_resignation", re.compile(r"resign\w*[^.]{0,80}\bauditors?\b|\bauditors?\b[^.]{0,80}resign", re.I)),
    ("auditor_change", re.compile(r"change in auditors|\b(appoint\w*|change|cessation|casual vacancy)\b[^.]{0,60}statutory auditor"
                                  r"|statutory auditors?\b[^.]{0,60}\b(appoint\w*|change|cessation)\b", re.I)),
    ("kmp_resignation", re.compile(ROLE + r"[^.]{0,100}" + LEAVE + "|" + LEAVE + r"[^.]{0,100}" + ROLE, re.I)),
    ("rating_downgrade", re.compile(r"downgrad\w*|watch with negative|negative implications|outlook[^.]{0,30}\bto negative", re.I)),
    ("rating_not_cooperating", re.compile(r"issuer not co-?operating|non[- ]?co-?operat\w*|not co-?operating", re.I)),
    ("default_delay", re.compile(r"\bdefault(?:ed|s)?\b|delay(?:ed)? in (?:the )?(?:re)?payment|delay in servicing"
                                 r"|non[- ]payment of (?:interest|principal|dues|instal)|delayed (?:re)?payment", re.I)),
    ("insolvency_new", re.compile(r"\b(admit\w*|admission|initiat\w*|commence\w*)\b[^.]{0,80}(insolvency|\bcirp\b)"
                                  r"|interim resolution professional", re.I)),
]
# Rules matched on the exchange's own text only; the NSE AI 'voiceSummary' adds too much noise for these
NO_SUMMARY = {"default_delay", "insolvency_new", "auditor_change"}
NOISE_CATS = ("analysts/institutional investor meet", "copy of newspaper publication", "investor presentation")
MINOR_AUDITOR = re.compile(r"(internal|secretarial|cost|tax)\s+auditor", re.I)
NIL_DEFAULT = re.compile(r"\b(no|nil|not|any|without|timely)\b[^.]{0,50}\b(default|delay)|default[^.]{0,30}\b(nil|not applicable)\b", re.I)
PLEDGE_INVOKE = re.compile(r"invo(?:c|k)\w*[^.]{0,60}(pledge|encumb)|(pledge|encumb)\w*[^.]{0,60}invo(?:c|k)", re.I)
PLEDGE_RELEASE = re.compile(r"(release|revoc\w*|revok\w*)[^.]{0,40}(pledge|encumb)|(pledge|encumb)\w*[^.]{0,40}(release|revok|revoc)", re.I)


def crore(x):
    return f"Rs {x / 1e7:,.2f} cr" if x is not None else "n/a"


def pct(x):
    return f"{x:.2f}%" if x is not None else "n/a"


# ---------- rules ----------
def rule_pledges(con, frm, to):
    out = []
    snaps = [r[0] for r in con.execute(
        "SELECT DISTINCT snapshot_date FROM pledges WHERE snapshot_date<=? ORDER BY 1 DESC", (to,))]
    if len(snaps) < 2:
        log.info("pledge rules: %d snapshot(s) so far - need 2 to compare (first run builds the baseline)", len(snaps))
        return out
    cur_d = snaps[0]
    prev_syms = {r[0] for r in con.execute("SELECT symbol FROM pledges WHERE snapshot_date=?", (snaps[1],))}
    if len(prev_syms) < 200:   # previous snapshot was a single-symbol/partial one: do not infer "new"
        prev_syms = None
    for cur in con.execute("SELECT * FROM pledges WHERE snapshot_date=?", (cur_d,)):
        prev = con.execute("SELECT * FROM pledges WHERE symbol=? AND snapshot_date<? "
                           "ORDER BY snapshot_date DESC LIMIT 1", (cur["symbol"], cur_d)).fetchone()
        if not prev:
            # Company absent from the previous full snapshot but present now = a new promoter
            # pledge disclosure (or a new listing). Compare from zero, but only if it is pledged.
            if prev_syms is None or (cur["pledged_pct_of_promoter"] or 0) <= 0:
                continue
            prev = {"snapshot_date": snaps[1] + " (absent)", "pledged_pct_of_promoter": 0.0,
                    "pledged_pct_of_equity": 0.0}
        out += pledge_compare(prev, cur)
    return out


def pledge_compare(prev, cur):
    out, crossed, up, down = [], [], False, False
    for basis, col in (("of promoter holding", "pledged_pct_of_promoter"), ("of equity", "pledged_pct_of_equity")):
        a, b = prev[col] or 0.0, cur[col]
        if b is None:
            continue
        up |= b - a >= PLEDGE_STEP
        down |= a - b >= PLEDGE_STEP
        crossed += [(lv, basis) for lv in PLEDGE_LEVELS if a < lv <= b]
    det = (f"promoter pledge {pct(prev['pledged_pct_of_promoter'])} -> {pct(cur['pledged_pct_of_promoter'])} of promoter holding; "
           f"{pct(prev['pledged_pct_of_equity'])} -> {pct(cur['pledged_pct_of_equity'])} of equity "
           f"(snapshots {prev['snapshot_date']} vs {cur['snapshot_date']}, SHP {cur['shp_date']})")
    url = f"https://www.nseindia.in/api/corporate-pledgedata?index=equities&symbol={cur['symbol']}"
    base = {"date": cur["snapshot_date"], "symbol": cur["symbol"], "url": url}
    if crossed:
        top = max(lv for lv, _ in crossed)
        bases = sorted({b for lv, b in crossed if lv == top})
        out.append(dict(base, rule=f"pledge_cross_{top}", details=f"crossed {top}% ({', '.join(bases)}); " + det,
                        key=f"pledge_cross_{top}|{cur['symbol']}|{cur['snapshot_date']}"))
    if up:
        out.append(dict(base, rule="pledge_up", details=det, key=f"pledge_up|{cur['symbol']}|{cur['snapshot_date']}"))
    if down:
        out.append(dict(base, rule="pledge_down", details=det, key=f"pledge_down|{cur['symbol']}|{cur['snapshot_date']}"))
    return out


def is_insider_cat(cat):
    c = (cat or "").strip().lower()
    return c in INSIDER_CATS or c.startswith("promoter")


def rule_insider(con, frm, to):
    out = []
    for r in con.execute("SELECT * FROM insider_trades WHERE date BETWEEN ? AND ?", (frm, to)):
        mode = (r["mode"] or "").lower()
        if "invocation" in mode or "invoke" in (r["tx_type"] or "").lower():
            out.append(dict(date=r["date"], symbol=r["symbol"], rule="pledge_invocation", url=r["url"],
                            key=f"pledge_invocation|pit|{r['id']}",
                            details=f"PIT: {r['person']} ({r['category']}) {r['mode']} of {r['qty'] or 0:,.0f} shares"))
        elif "revok" in mode or "release" in mode or "revoke" in (r["tx_type"] or "").lower():
            out.append(dict(date=r["date"], symbol=r["symbol"], rule="pledge_release", url=r["url"],
                            key=f"pledge_release|pit|{r['id']}",
                            details=f"PIT: {r['person']} ({r['category']}) {r['mode']} of {r['qty'] or 0:,.0f} shares"))
        if not is_insider_cat(r["category"]) or (r["sec_type"] or "").lower() not in ("equity shares", ""):
            continue
        v = r["value"] or 0
        if mode == "market purchase" and v >= BUY_MIN or mode == "market sale" and v >= SELL_MIN:
            rule = "insider_buy" if mode == "market purchase" else "insider_sell"
            out.append(dict(date=r["date"], symbol=r["symbol"], rule=rule, url=r["url"], key=f"{rule}|{r['id']}",
                            details=f"{r['person']} ({r['category']}) {r['mode']} {r['qty'] or 0:,.0f} sh, {crore(v)}; "
                                    f"holding {pct(r['before_pct'])} -> {pct(r['after_pct'])}; traded {r['trade_from']}..{r['trade_to']}"))
    for r in con.execute("SELECT * FROM sast WHERE date BETWEEN ? AND ? AND promoter='Y' AND mode='Open Market'", (frm, to)):
        sh = r["shares_acq"] if (r["side"] or "").startswith("Acq") else r["shares_sale"]
        p = r["pct_acq"] if (r["side"] or "").startswith("Acq") else r["pct_sale"]
        out.append(dict(date=r["date"], symbol=r["symbol"], rule="sast_promoter_open_market", url=r["url"],
                        key=f"sast_promoter_open_market|{r['id']}",
                        details=f"{r['acquirer']} (promoter) {r['side']} {sh or 0:,.0f} sh ({pct(p)}) on {r['period']}; "
                                f"after {pct(r['pct_after'])} [{r['reg_type']}]"))
    return out


def rule_cluster(con, frm, to):
    """>=2 distinct insiders in the same stock and direction within CLUSTER_DAYS, open market."""
    lo = (dt.date.fromisoformat(frm) - dt.timedelta(days=CLUSTER_DAYS)).isoformat()
    ev = []
    for r in con.execute("SELECT symbol, date, person, category, mode, value, url FROM insider_trades "
                         "WHERE date BETWEEN ? AND ? AND mode IN ('Market Purchase','Market Sale')", (lo, to)):
        if is_insider_cat(r["category"]) or (r["category"] or "").lower() in ("immediate relative", "employees/designated employees"):
            ev.append((r["symbol"], r["date"], C.norm_name(r["person"]).replace("limted", "")[:16] or "?",
                       "buy" if r["mode"] == "Market Purchase" else "sell", r["value"], r["url"], r["person"]))
    for r in con.execute("SELECT symbol, date, acquirer, side, url FROM sast WHERE date BETWEEN ? AND ? "
                         "AND promoter='Y' AND mode='Open Market'", (lo, to)):
        ev.append((r["symbol"], r["date"], C.norm_name(r["acquirer"]).replace("limted", "")[:16] or "?",
                   "buy" if (r["side"] or "").startswith("Acq") else "sell", None, r["url"], r["acquirer"]))
    groups = {}
    for e in ev:
        groups.setdefault((e[0], e[3]), []).append(e)
    out = []
    for (sym, side), es in groups.items():
        es.sort(key=lambda e: e[1])
        last = es[-1]
        if last[1] < frm:
            continue
        start = (dt.date.fromisoformat(last[1]) - dt.timedelta(days=CLUSTER_DAYS)).isoformat()
        win = [e for e in es if e[1] >= start]
        names = {}
        for e in win:
            names.setdefault(e[2], (e[6] or "").strip())
        people = sorted(names.values())
        if len(names) >= CLUSTER_MIN:
            tot = sum(e[4] or 0 for e in win)
            out.append(dict(date=last[1], symbol=sym, rule="insider_cluster", url=last[5],
                            key=f"insider_cluster|{sym}|{side}|{last[1]}",
                            details=f"{len(people)} insiders {side} in {CLUSTER_DAYS}d ({win[0][1]}..{last[1]}): "
                                    f"{'; '.join(people[:5])}" + (f"; PIT value {crore(tot)}" if tot else "")))
    return out


def rule_announcements(con, frm, to):
    out, seen = [], set()
    rows = con.execute("SELECT * FROM announcements WHERE date BETWEEN ? AND ? "
                       "ORDER BY CASE source WHEN 'NSE' THEN 0 ELSE 1 END, dt", (frm, to)).fetchall()
    for r in rows:
        cat = (r["category"] or "").lower()
        if any(cat.startswith(n) for n in NOISE_CATS):
            continue
        blob_full = " | ".join(x for x in (r["category"], r["subject"], r["text"]) if x)
        blob_main = blob_full.split("\n[summary]")[0]
        hits = []
        for rule, rx in ANN_RULES:
            blob = blob_main if rule in NO_SUMMARY else blob_full
            m = rx.search(blob)
            if not m:
                continue
            if rule.startswith("auditor") and MINOR_AUDITOR.search(m.group(0)) and "statutory" not in m.group(0).lower():
                continue
            if rule == "default_delay" and NIL_DEFAULT.search(blob):
                continue
            if rule in ("rating_downgrade", "rating_not_cooperating") and "rating" not in blob.lower():
                continue
            hits.append((rule, m.group(0)))
        if PLEDGE_INVOKE.search(blob_full):
            hits.append(("pledge_invocation", PLEDGE_INVOKE.search(blob_full).group(0)))
        elif PLEDGE_RELEASE.search(blob_full):
            hits.append(("pledge_release", PLEDGE_RELEASE.search(blob_full).group(0)))
        if any(h[0] == "auditor_resignation" for h in hits):
            hits = [h for h in hits if h[0] != "auditor_change"]
        for rule, match in hits:
            dk = (rule, r["symbol"] or r["bse_code"], r["date"])
            if dk in seen:   # same event filed on NSE and BSE, or several filings that day
                continue
            seen.add(dk)
            first = (r["text"] or r["subject"] or "").split("\n")[0]
            out.append(dict(date=r["date"], symbol=r["symbol"] or f"BSE:{r['bse_code']}", rule=rule, url=r["url"],
                            key=f"{rule}|{r['source']}|{r['id']}",
                            details=f"[{r['source']}: {r['category']}] match '{match[:60]}' - {first[:220]}"))
    return out


def rule_deals(con, frm, to):
    """Net each client's buys and sells per stock per day (block trades also appear in the bulk list,
    so identical rows are counted once). Same-day round trips by HFT/arbitrage desks net to ~0 and drop out."""
    agg = {}
    for r in con.execute("SELECT DISTINCT date, symbol, client, side, qty, price, value_cr, kind FROM deals "
                         "WHERE date BETWEEN ? AND ? ORDER BY kind DESC", (frm, to)):
        k = (r["date"], r["symbol"], r["client"])
        a = agg.setdefault(k, {"buy": 0.0, "sell": 0.0, "val": 0.0, "kinds": set(), "seen": set()})
        sig = (r["side"], r["qty"], r["price"])
        if sig in a["seen"]:
            continue
        a["seen"].add(sig)
        a["buy" if r["side"].startswith("B") else "sell"] += r["qty"] or 0
        a["val"] += (r["value_cr"] or 0) * (1 if r["side"].startswith("B") else -1)
        a["kinds"].add(r["kind"])
    out, unknown = [], 0
    for (day, sym, client), a in agg.items():
        net = a["buy"] - a["sell"]
        sh = con.execute("SELECT total_shares FROM pledges WHERE symbol=? AND total_shares>0 "
                         "ORDER BY snapshot_date DESC LIMIT 1", (sym,)).fetchone() or \
            con.execute("SELECT shares FROM shares WHERE symbol=? AND shares>0", (sym,)).fetchone()
        p = abs(net) / sh[0] * 100 if sh else None
        if p is None:
            unknown += 1
        if (p is not None and p >= DEAL_PCT) or (p is None and abs(a["val"]) >= DEAL_CR_FALLBACK):
            side = "net BUY" if net > 0 else "net SELL"
            out.append(dict(date=day, symbol=sym, rule="large_deal",
                            url="https://www.nseindia.com/report-detail/display-bulk-and-block-deals",
                            key=f"large_deal|{day}|{sym}|{client}",
                            details=f"{'/'.join(sorted(a['kinds']))} {side} {client}: {abs(net):,.0f} sh, Rs {abs(a['val']):,.2f} cr"
                                    + (f" = {p:.2f}% of equity" if p is not None else " (share count unknown)")
                                    + (f" (bought {a['buy']:,.0f}, sold {a['sell']:,.0f})" if a["buy"] and a["sell"] else "")))
    if unknown:
        log.info("deals: %d client-days without a share count (value fallback used)", unknown)
    return out


RULES = [rule_pledges, rule_insider, rule_cluster, rule_announcements, rule_deals]


def run_rules(con, frm, to):
    alerts = []
    for fn in RULES:
        try:
            a = fn(con, frm, to)
            log.info("%-20s %d alerts", fn.__name__, len(a))
            alerts += a
        except Exception as e:
            log.error("%s failed: %s", fn.__name__, e)
    return alerts


ORDER = ["pledge_cross_50", "pledge_cross_25", "pledge_cross_10", "pledge_up", "pledge_invocation",
         "auditor_resignation", "rating_not_cooperating", "default_delay", "rating_downgrade", "insolvency_new", "kmp_resignation",
         "insider_sell", "insider_buy", "insider_cluster", "sast_promoter_open_market", "large_deal",
         "auditor_change", "pledge_release", "pledge_down"]


def write_outputs(alerts, day, frm, to, new_only):
    d = os.path.join(C.DATA, "alerts")
    os.makedirs(d, exist_ok=True)
    alerts = sorted(alerts, key=lambda a: (ORDER.index(a["rule"]) if a["rule"] in ORDER else 99, a["symbol"] or "", a["date"] or ""))
    with open(os.path.join(d, f"{day}.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "symbol", "rule", "details", "source_url"])
        for a in alerts:
            w.writerow([a["date"], a["symbol"], a["rule"], a["details"], a["url"]])
    counts = {}
    for a in alerts:
        counts[a["rule"]] = counts.get(a["rule"], 0) + 1
    md = [f"# FEIN alerts {day}", "",
          f"Event window {frm} to {to}. {'Alerts first seen today' if new_only else 'All alerts in window'}: {len(alerts)}. "
          "Research signals, not advice: open the source filing before acting.", ""]
    md += ["| rule | count |", "|---|---|"] + [f"| {k} | {counts[k]} |" for k in sorted(counts, key=lambda k: ORDER.index(k) if k in ORDER else 99)]
    cur = None
    for a in alerts:
        if a["rule"] != cur:
            cur = a["rule"]
            md += ["", f"## {cur}", "", "| date | symbol | details | source |", "|---|---|---|---|"]
        det = (a["details"] or "").replace("|", "/").replace("\n", " ")
        md.append(f"| {a['date']} | {a['symbol']} | {det} | {'[link](' + a['url'] + ')' if a['url'] else ''} |")
    with open(os.path.join(d, f"{day}.md"), "w") as f:
        f.write("\n".join(md) + "\n")
    return counts


def selftest():
    print("selftest 1/2: live known case - Indo Tech Transformers (INDOTECH) promoter pledge")
    con = C.db(":memory:")
    ok = True
    try:
        cur = C.nse_api("corporate-pledgedata", index="equities", symbol="INDOTECH")[0]["data"][0]
        sast = C.nse_api("corporate-sast-reg29", index="equities", symbol="INDOTECH")[0]["data"]
        pledged, total, prom = (C.num(cur["totPromoterShares"]), C.num(cur["totIssuedShares"]),
                                C.num(cur["totPromoterHolding"]))
        # The Nov-2025 encumbrance disclosure (SAST) shows the pledge rising by X shares to the current
        # level, so the pre-event level = after - acquired. Use it as the "previous snapshot".
        ev = next(r for r in sast if C.num(r.get("noOfShareAft")) == pledged and C.num(r.get("noOfShareAcq")))
        before = pledged - C.num(ev["noOfShareAcq"])
        row = lambda d, p: {"snapshot_date": d, "symbol": "INDOTECH", "company": cur["comName"], "shp_date": "2026-09-30",
                            "promoter_holding_pct": None, "pledged_pct_of_promoter": round(p / prom * 100, 2),
                            "pledged_pct_of_equity": round(p / total * 100, 2), "promoter_pledged_shares": p,
                            "promoter_shares": prom, "total_shares": total, "all_pledged_pct": None, "broadcast_dt": None}
        C.upsert(con, "pledges", [row("2025-11-06", before), row("2026-11-21", pledged)])
        print(f"  live: pledged {pledged:,.0f} of {total:,.0f} shares = {pledged / total * 100:.2f}% of equity "
              f"(NSE percTotShares {cur['percTotShares'].strip()}), {cur['percPromoterShares'].strip()}% of promoter holding")
        print(f"  before the {ev['acquirerDate']} encumbrance: {before:,.0f} shares = {before / total * 100:.2f}% of equity")
        got = rule_pledges(con, "2026-11-01", "2026-11-21")
        for a in got:
            print(f"  ALERT {a['rule']}: {a['details']}")
        fired = {a["rule"] for a in got}
        ok &= {"pledge_cross_50", "pledge_up"} <= fired
        print("  PASS" if ok else "  FAIL: expected pledge_cross_50 and pledge_up")
    except Exception as e:
        ok = False
        print(f"  FAIL (live fetch): {e}")

    print("selftest 2/2: offline rule checks on synthetic rows")
    con = C.db(":memory:")
    ann = lambda i, cat, text: {"source": "NSE", "id": str(i), "dt": "2026-11-20 10:00:00", "date": "2026-11-20",
                                "symbol": f"T{i}", "bse_code": None, "company": "T", "category": cat, "subject": cat,
                                "text": text, "url": "u"}
    C.upsert(con, "announcements", [
        ann(1, "Resignation of Statutory Auditor", "M/s ABC & Co, statutory auditors, have resigned citing non-receipt of information"),
        ann(2, "Resignation", "Resignation of Mr X as Chief Financial Officer of the company"),
        ann(3, "Credit Rating", "CARE has downgraded the long-term bank facilities to CARE BB"),
        ann(4, "Credit Rating", "ICRA has moved the rating to Issuer Not Cooperating category"),
        ann(5, "General Updates", "Disclosure of delay in payment of interest on NCDs due on 15-Nov-2026"),
        ann(6, "Disclosure under SEBI Takeover Regulations", "Disclosure for invocation of pledge of promoter shares by lender"),
        ann(7, "General Updates", "Statement that there is no default in payment of interest"),          # must NOT fire
        ann(8, "Appointment", "Appointment of Secretarial Auditor for FY27"),                             # must NOT fire
        ann(9, "Updates", "We certify that the company has made timely payment, with no delay in payment of interest"),  # NOT
        ann(10, "Corporate Insolvency Resolution Process", "NCLT has admitted the petition and initiated the corporate insolvency resolution process"),
    ])
    pit = lambda i, sym, who, mode, val: {"id": str(i), "dt": "2026-11-20 10:00:00", "date": "2026-11-20", "symbol": sym,
                                          "company": sym, "person": who, "category": "Promoter Group", "mode": mode,
                                          "tx_type": "Buy", "sec_type": "Equity Shares", "qty": 1000, "value": val,
                                          "before_pct": 1, "after_pct": 1.1, "trade_from": "2026-11-19", "trade_to": "2026-11-19", "url": "u"}
    C.upsert(con, "insider_trades", [pit(1, "AAA", "P ONE", "Market Purchase", 2e7), pit(2, "AAA", "P TWO", "Market Purchase", 5e6),
                                     pit(3, "BBB", "P THREE", "Market Sale", 6e7)])
    C.upsert(con, "deals", [{"date": "2026-11-20", "kind": "bulk", "symbol": "AAA", "company": "A", "client": "FUND",
                             "side": "BUY", "qty": 150000, "price": 100, "value_cr": 1.5, "remarks": "-"}] +
                    [{"date": "2026-11-20", "kind": "bulk", "symbol": "AAA", "company": "A", "client": "HFT DESK",   # round trip: NOT
                      "side": sd, "qty": 300000, "price": 100, "value_cr": 3.0, "remarks": "-"} for sd in ("BUY", "SELL")])
    C.upsert(con, "pledges", [{"snapshot_date": "2026-11-21", "symbol": "AAA", "company": "A", "shp_date": None,
                               "promoter_holding_pct": 50, "pledged_pct_of_promoter": 0, "pledged_pct_of_equity": 0,
                               "promoter_pledged_shares": 0, "promoter_shares": 5e6, "total_shares": 1e7,
                               "all_pledged_pct": 0, "broadcast_dt": None}])
    got = run_rules(con, "2026-11-20", "2026-11-21")
    fired = {}
    for a in got:
        fired.setdefault(a["rule"], set()).add(a["symbol"])
    expect = {"auditor_resignation": {"T1"}, "kmp_resignation": {"T2"}, "rating_downgrade": {"T3"},
              "rating_not_cooperating": {"T4"}, "default_delay": {"T5"}, "insolvency_new": {"T10"}, "pledge_invocation": {"T6"},
              "insider_buy": {"AAA"}, "insider_sell": {"BBB"}, "insider_cluster": {"AAA"}, "large_deal": {"AAA"}}
    for rule, syms in expect.items():
        good = fired.get(rule) == syms
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'} {rule:24s} expected {sorted(syms)} got {sorted(fired.get(rule, []))}")
    extra = {r: s for r, s in fired.items() if r not in expect}
    if extra:
        ok = False
        print(f"  FAIL unexpected alerts: {extra}")
    print("selftest:", "ALL PASS" if ok else "FAILURES above")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    t = C.today_ist()
    p.add_argument("--to", default=t.isoformat())
    p.add_argument("--from", dest="frm", help="default: --to minus 3 days")
    p.add_argument("--all", action="store_true", help="re-list alerts already emitted earlier")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        import logging
        logging.disable(logging.INFO)
        return selftest()
    C.setup_logging("detect")
    frm = a.frm or (dt.date.fromisoformat(a.to) - dt.timedelta(days=3)).isoformat()
    con = C.db()
    # pledge snapshots are dated by collection day, which can be after --to
    pledge_to = max(a.to, t.isoformat()) if a.to >= (t - dt.timedelta(days=1)).isoformat() else a.to
    alerts = []
    for fn in RULES:
        try:
            got = fn(con, frm, pledge_to if fn is rule_pledges else a.to)
            log.info("%-20s %d alerts", fn.__name__, len(got))
            alerts += got
        except Exception as e:
            log.error("%s failed: %s", fn.__name__, e)
    now = dt.datetime.now(C.IST).isoformat(timespec="seconds")
    new = []
    for al in alerts:
        seen = con.execute("SELECT 1 FROM alerts WHERE key=?", (al["key"],)).fetchone()
        if not seen:
            con.execute("INSERT INTO alerts VALUES(?,?,?,?,?,?,?)",
                        (al["key"], now, al["date"], al["symbol"], al["rule"], al["details"], al["url"]))
            new.append(al)
    con.commit()
    run_day = t.isoformat()
    if a.all:
        out = alerts
    else:  # everything first seen today, so a second run the same day does not blank the file
        out = [dict(r) for r in con.execute("SELECT * FROM alerts WHERE substr(first_seen,1,10)=?", (run_day,))]
    counts = write_outputs(out, run_day, frm, a.to, not a.all)
    log.info("detect %s..%s: %d alerts in window, %d new -> %s/alerts/%s.md  %s", frm, a.to, len(alerts), len(new),
             C.DATA, run_day, counts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
