#!/usr/bin/env python3
"""Step 5: tickers + Yahoo v8 daily prices (2015-06-01 .. 2024-07-15) for every universe CIK.
Ticker candidates: current SEC tickers; for firms with none (mostly dead), the ticker prefix of the XBRL instance
file in the T-10-K (e.g. 'abc-20141231.xml'). Yahoo: short UA, >=1.1 s/call, missing cached as {"missing":true}."""
import json, os, re, sys, time, urllib.request, urllib.error
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import p, sec_get

P1, P2 = 1433116800, 1721001600
_last = [0.0]


def yahoo(t):
    fp = p("prices", t.replace("/", "_") + ".json")
    if os.path.exists(fp):
        return json.load(open(fp))
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t.replace('.', '-')}?period1={P1}&period2={P2}&interval=1d&events=split"
    res = {"missing": True, "why": "fail"}
    for i in range(4):
        w = 1.1 - (time.time() - _last[0])
        if w > 0: time.sleep(w)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.load(r)["chart"]["result"][0]
            ts = d.get("timestamp") or []
            if not ts:
                res = {"missing": True, "why": "no data"}; break
            q = d["indicators"]["quote"][0]
            res = {"ticker": t, "t": ts, "close": q.get("close"), "adj": d["indicators"]["adjclose"][0]["adjclose"],
                   "name": d["meta"].get("longName") or d["meta"].get("shortName"), "type": d["meta"].get("instrumentType")}
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                res = {"missing": True, "why": "404"}; break
            if e.code == 429:
                time.sleep(30 * (i + 1)); continue
            res = {"missing": True, "why": f"http {e.code}"}
        except Exception as e:
            res = {"missing": True, "why": str(e)[:80]}; time.sleep(3)
    os.makedirs(p("prices"), exist_ok=True)
    json.dump(res, open(fp, "w"))
    return res


def instance_ticker(cik, accn):
    d = sec_get(f"https://www.sec.gov/Archives/edgar/data/{cik}/{accn.replace('-', '')}/index.json",
                p("idx", f"{cik}_{accn}.json"))
    if not d:
        return None
    for it in d["directory"]["item"]:
        m = re.match(r"^([a-z][a-z0-9.]{0,6})-(19|20)\d{6}(_htm)?\.xml$", it["name"].lower())
        if m:
            return m.group(1).upper()
    return None


def main():
    rows = [json.loads(l) for l in open(p("universe.jsonl"))]
    tick = {}
    tp = p("tickers.json")
    if os.path.exists(tp):
        tick = {int(k): v for k, v in json.load(open(tp)).items()}
    by = {}
    for r in rows:
        by.setdefault(r["cik"], []).append(r)
    for cik, rs in by.items():
        if cik in tick:
            continue
        s = json.load(open(p("firms", f"{cik}.json")))
        cands = [t for t in (s.get("tickers") or []) if t]
        inst = set()
        for r in (rs if not cands else []):  # only firms with no current SEC ticker (mostly dead)
            t = instance_ticker(cik, r["accn"])
            if t: inst.add(t)
        tick[cik] = {"current": cands[:2], "instance": sorted(inst)}
    json.dump(tick, open(tp, "w"))
    allt = []
    for v in tick.values():
        for t in v["current"] + v["instance"]:
            if t not in allt: allt.append(t)
    print("tickers to fetch", len(allt), flush=True)
    miss = 0
    for i, t in enumerate(allt):
        miss += bool(yahoo(t).get("missing"))
        if i % 200 == 0:
            print(i, "missing", miss, flush=True)
    print("done", len(allt), "missing", miss)


if __name__ == "__main__":
    main()
