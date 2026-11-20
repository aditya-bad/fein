#!/usr/bin/env python3
"""Step 3: market cap + sector for events, and a point-in-time control universe.

Market cap at event = dei:EntityCommonStockSharesOutstanding (cover page, latest XBRL frame
whose period end is <= event date, within 200 days) x insider VWAP (unadjusted, at the time).
Multi-class firms report one class in frames -> mcap can be understated (caveat).
Sector: SIC code from data.sec.gov/submissions (current SIC; rarely changes).
Control universe: every issuer that had ANY Form 4 filed in the same quarter (ticker as filed
then, so delisted firms are included at the universe stage) and a shares-outstanding frame.
Usage: python3 s3_size_sector.py OUTDIR
"""
import csv, io, json, os, sys, zipfile, bisect
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import sec_fetch as S  # polite SEC getter (UA + spacing + backoff)

csv.field_size_limit(10**9)
QTRS = [f"CY{y}Q{q}I" for y in range(2020, 2026) for q in range(1, 5)]


def frames(out):
    fd = os.path.join(out, "frames"); os.makedirs(fd, exist_ok=True)
    sh = {}  # cik -> sorted list of (end, val)
    for q in QTRS:
        p = os.path.join(fd, f"dei_{q}.json")
        if not os.path.exists(p):
            try:
                txt = S.get(f"https://data.sec.gov/api/xbrl/frames/dei/EntityCommonStockSharesOutstanding/shares/{q}.json")
            except Exception as e:
                print("frame fail", q, e, file=sys.stderr); continue
            open(p, "w").write(txt)
        for r in json.load(open(p))["data"]:
            sh.setdefault(str(r["cik"]), []).append((r["end"], float(r["val"])))
    for k in sh: sh[k].sort()
    return sh


def shares_at(sh, cik, d):
    from datetime import date
    lst = sh.get(cik) or []
    i = bisect.bisect_right(lst, (d, float("inf"))) - 1
    if i < 0: return None
    end, v = lst[i]
    if (date.fromisoformat(d) - date.fromisoformat(end)).days > 200: return None
    return v


def sic_for(out, ciks):
    p = os.path.join(out, "sic.json")
    cache = json.load(open(p)) if os.path.exists(p) else {}
    todo = [c for c in ciks if c not in cache]
    print(f"SIC lookups needed: {len(todo)}", file=sys.stderr)
    for i, c in enumerate(todo):
        try:
            d = S.get_json(f"https://data.sec.gov/submissions/CIK{int(c):010d}.json")
            cache[c] = {"sic": d.get("sic") or "", "sicd": d.get("sicDescription") or "", "tickers": d.get("tickers") or [],
                        "exch": d.get("exchanges") or [], "name": d.get("name")}
        except Exception as e:
            cache[c] = {"sic": "", "sicd": f"ERR {e}", "tickers": [], "exch": []}
        if i % 200 == 0:
            json.dump(cache, open(p, "w")); print(f"  sic {i}/{len(todo)}", file=sys.stderr, flush=True)
    json.dump(cache, open(p, "w"))
    return cache


def universe(out):
    """issuer cik -> {quarter: ticker} from all Form 4 SUBMISSION rows."""
    uni = {}
    raw = os.path.join(out, "raw")
    for fn in sorted(os.listdir(raw)):
        if not fn.endswith("_form345.zip"): continue
        q = fn[:6]
        with zipfile.ZipFile(os.path.join(raw, fn)).open("SUBMISSION.tsv") as fh:
            for r in csv.DictReader(io.TextIOWrapper(fh, "utf-8", "replace"), delimiter="\t", quoting=csv.QUOTE_NONE):
                if r["DOCUMENT_TYPE"] in ("4", "4/A"):
                    t = r["ISSUERTRADINGSYMBOL"].strip().upper()
                    if t and t not in ("NONE", "N/A", "NA"):
                        uni.setdefault(r["ISSUERCIK"].lstrip("0"), {})[q] = t
    return uni


def main(out):
    sh = frames(out)
    ev = list(csv.DictReader(open(os.path.join(out, "events_raw.tsv")), delimiter="\t"))
    for e in ev:
        s = shares_at(sh, e["issuer_cik"], e["event_date"])
        e["shares_out"] = s or ""
        e["mcap_m"] = round(s * float(e["vwap"]) / 1e6, 1) if s else ""
    uni = universe(out)
    json.dump(uni, open(os.path.join(out, "universe_tickers.json"), "w"))
    # SIC for events in a broad size range (100M-20B) + whole universe with frames (for controls)
    ev_ciks = {e["issuer_cik"] for e in ev if e["mcap_m"] and 100 <= e["mcap_m"] <= 20000}
    uni_ciks = {c for c in uni if c in sh}
    print(f"events {len(ev)}; with mcap {sum(1 for e in ev if e['mcap_m'])}; in 100M-20B {len(ev_ciks)} issuers; universe w/ shares {len(uni_ciks)}", file=sys.stderr)
    sic = sic_for(out, sorted(ev_ciks | uni_ciks))
    for e in ev:
        s = sic.get(e["issuer_cik"], {})
        e["sic"] = s.get("sic", ""); e["sicd"] = s.get("sicd", "")
    with open(os.path.join(out, "events_sized.tsv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ev[0]), delimiter="\t"); w.writeheader(); w.writerows(ev)


if __name__ == "__main__":
    main(sys.argv[1])
