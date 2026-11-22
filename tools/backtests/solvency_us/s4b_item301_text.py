#!/usr/bin/env python3
"""Step 4b (deviation, documented): classify 8-K item 3.01 filings as listing-rule failure vs voluntary
transfer/other. The pre-registered O_delist (3.01 + Form 25/15 + no merger) turned out, on audit, to be dominated by
voluntary exchange transfers (Nasdaq <-> NYSE). Rule: CAUSE if the 8-K text has non-compliance language
(deficiency / not in compliance / minimum bid / failure to satisfy / delinquen* / late filing / suspend*) and no
transfer language overrides it. Docs are cached as plain text; they are untrusted data and only keyword-scanned."""
import gzip, json, os, re, sys, time, urllib.request
from datetime import date
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import p, UA

CAUSE = re.compile(r"not in compliance|non-?compliance|deficien|minimum bid|failure to (satisfy|comply|meet)|"
                   r"delinquen|did not (timely )?file|failed to (timely )?file|suspend|no longer (meets|complies)|"
                   r"does not (meet|satisfy|comply)|below the (minimum|continued listing)|hearings? panel|determined to delist", re.I)
TRANSFER = re.compile(r"transfer(ring)?\b.{0,60}\blisting|to list .{0,80}on the (new york stock exchange|nyse|nasdaq)|"
                      r"(begin|commence|expects? to) .{0,40}trad(e|ing) on (the )?(new york stock exchange|nyse|nasdaq)|switch(ing)? (its|our) listing", re.I)
HEADING = re.compile(r"item\s*3\s*\.\s*0\s*1\.?\W*notice of delisting or failure to satisfy a continued listing rule or standard\W*(transfer of listing)?", re.I)
_last = [0.0]


def fetch_text(url, path):
    if os.path.exists(path):
        return open(path).read()
    w = 0.13 - (time.time() - _last[0])
    if w > 0: time.sleep(w)
    _last[0] = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
        with urllib.request.urlopen(req, timeout=60) as r:
            b = r.read()
            if r.headers.get("Content-Encoding") == "gzip": b = gzip.decompress(b)
        t = re.sub(r"<[^>]+>", " ", b.decode("utf-8", "replace"))
        t = re.sub(r"&nbsp;|&#160;", " ", t); t = re.sub(r"\s+", " ", t)
    except Exception as e:
        t = f"__ERROR__ {e}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(t)
    return t


def main():
    ev = [json.loads(l) for l in open(p("events.jsonl"))]
    out = {}
    for e in ev:
        if not (e["i301"] and e["delist_date"] and not e["merger_date"] and not e["O_bk"]):
            continue
        cik = e["cik"]; T = date.fromisoformat(e["T"]); E = T.replace(year=T.year + 5)
        fl = json.load(open(p("firms", f"{cik}.json")))["filings"]
        docs = [x for x in fl if x[0] in ("8-K", "8-K/A") and "3.01" in (x[3] or "").split(",") and T < date.fromisoformat(x[1]) <= E]
        cls = []
        for x in sorted(docs, key=lambda x: x[1])[:6]:
            acc = x[4]
            t = fetch_text(f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}/{x[5]}", p("doc301", f"{cik}_{acc}.txt"))
            t = HEADING.sub(" [ITEM 3.01] ", t)
            c = bool(CAUSE.search(t)); tr = bool(TRANSFER.search(t))
            m = CAUSE.search(t)
            cls.append({"date": x[1], "cause": c, "transfer": tr, "snip": t[max(0, m.start() - 80): m.end() + 80] if m else ""})
        out[f"{cik}|{e['T']}"] = {"docs": cls, "cause": any(d["cause"] and not d["transfer"] for d in cls)}
    json.dump(out, open(p("item301_class.json"), "w"), indent=1)
    print("checked", len(out), "cause", sum(v["cause"] for v in out.values()))


if __name__ == "__main__":
    main()
