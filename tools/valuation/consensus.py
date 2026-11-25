#!/usr/bin/env python3
"""Analyst-consensus snapshot from Yahoo Finance (unofficial quoteSummary API).

Usage:  python3 tools/valuation/consensus.py RELIANCE.NS HARSHA.NS AVGO [--out file.json]
For each symbol prints trailing P/E, forward P/E, forward EPS, and the EPS estimate + number of analysts for the
current/next quarter and fiscal year. Use it as a *cross-check* on our own scenarios (stage 5), never as an input we trust:
  - few or zero analysts on most Indian small caps (that absence is itself information: low coverage);
  - forward EPS is often "adjusted"/non-GAAP while trailing P/E is reported earnings (e.g. AVGO), so the two P/Es are not
    like-for-like;
  - consensus is a single-source estimate; record it dated (as_of) and compare later with what was actually reported.
Standard library + system curl only (same pattern as the other fetch tools)."""
import json, os, subprocess, sys, tempfile, datetime

UA = "Mozilla/5.0"

def _curl(args):
    return subprocess.run(["curl", "-s", "-A", UA] + args, capture_output=True, text=True, timeout=40).stdout

def session():
    jar = tempfile.NamedTemporaryFile(delete=False, suffix=".txt").name
    _curl(["-c", jar, "https://fc.yahoo.com", "-o", os.devnull])
    crumb = _curl(["-b", jar, "https://query2.finance.yahoo.com/v1/test/getcrumb"]).strip()
    if not crumb or len(crumb) > 40:
        raise SystemExit("could not get a Yahoo crumb")
    return jar, crumb

def raw(x):
    return (x or {}).get("raw") if isinstance(x, dict) else None

def snapshot(sym, jar, crumb):
    url = (f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{sym}"
           f"?modules=summaryDetail,defaultKeyStatistics,earningsTrend&crumb={crumb}")
    d = json.loads(_curl(["-b", jar, url]) or "{}").get("quoteSummary", {})
    if not d.get("result"):
        return {"symbol": sym, "error": str(d.get("error"))}
    r = d["result"][0]
    sd, ks = r.get("summaryDetail", {}), r.get("defaultKeyStatistics", {})
    trend = {}
    for t in r.get("earningsTrend", {}).get("trend", []):
        e = t.get("earningsEstimate", {})
        trend[t.get("period")] = {"end": t.get("endDate"), "eps_avg": raw(e.get("avg")), "eps_low": raw(e.get("low")),
                                  "eps_high": raw(e.get("high")), "analysts": raw(e.get("numberOfAnalysts"))}
    return {"symbol": sym, "as_of": datetime.date.today().isoformat(), "source": "Yahoo quoteSummary (unofficial)",
            "price_prev_close": raw(sd.get("previousClose")), "currency": sd.get("currency"),
            "trailing_pe": raw(sd.get("trailingPE")), "forward_pe": raw(sd.get("forwardPE")) or raw(ks.get("forwardPE")),
            "forward_eps": raw(ks.get("forwardEps")), "trailing_eps": raw(ks.get("trailingEps")),
            "analysts_next_fy": (trend.get("+1y") or {}).get("analysts"), "trend": trend}

def main(argv):
    out = None
    if "--out" in argv:
        i = argv.index("--out"); out = argv[i + 1]; argv = argv[:i] + argv[i + 2:]
    if not argv:
        print(__doc__); return 2
    jar, crumb = session()
    rows = [snapshot(s, jar, crumb) for s in argv]
    for r in rows:
        if "error" in r:
            print(f"{r['symbol']:15s} ERROR {r['error']}"); continue
        n = r["analysts_next_fy"]
        print(f"{r['symbol']:15s} prev close {r['price_prev_close']}  trailing P/E {r['trailing_pe'] and round(r['trailing_pe'],1)}  "
              f"forward P/E {r['forward_pe'] and round(r['forward_pe'],1)}  analysts(next FY) {n if n is not None else 0}")
    if out:
        json.dump(rows, open(out, "w"), indent=1)
    os.unlink(jar)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
