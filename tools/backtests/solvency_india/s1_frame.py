#!/usr/bin/env python3
"""Step 1: population frame and stratified sample (fate-independent lists, no outcome used).

Frame = every company on BSE's Active, Delisted or Suspended scrip lists, plus NSE-only active symbols, plus
NSE-delisted / IBBI rows with an NSE symbol but no BSE code. One row per company (key ISIN > BSE code > NSE symbol).
Strata (pre-registered):
  D  distress lists  : appears in IBBI CIRP / liquidation / NCLT rows, NSE compulsory or liquidation delisting,
                       NSE suspension or BSE suspended list            -> census (all fetched)
  X  BSE delisted, not D (mergers, voluntary, old, reason unknown)     -> simple random sample
  L  live (BSE active or NSE active), not D                            -> simple random sample
Weights = stratum population / stratum sample. Output: $CACHE/frame.csv
"""
import argparse, collections, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K

DISTRESS = {"ibbi_cirp", "ibbi_liq", "ibbi_nclt", "nse_suspended", "bse_suspended"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-live", type=int, default=900)
    ap.add_argument("--n-delisted", type=int, default=500)
    ap.add_argument("--seed", type=int, default=20161)
    a = ap.parse_args()
    comp = {}          # key -> record
    alias = {}         # any identifier -> key

    def get(isin="", bse="", nse="", name=""):
        ids = [("isin", isin), ("bse", bse), ("nse", nse.upper() if nse else "")]
        for t, v in ids:
            if v and (t, v) in alias:
                k = alias[(t, v)]
                break
        else:
            k = next((f"{t}:{v}" for t, v in ids if v), None)
            if k is None:
                return None
            comp[k] = {"key": k, "isin": "", "bse_code": "", "nse_symbol": "", "name": name, "sources": set()}
        r = comp[k]
        for (t, v), f in zip(ids, ("isin", "bse_code", "nse_symbol")):
            if v:
                alias[(t, v)] = k
                r[f] = r[f] or v
        r["name"] = r["name"] or name
        return r

    for st in ("Active",):
        for d in json.load(open(os.path.join(K.CACHE, "bse_active.json"))):
            r = get(d.get("ISIN_NUMBER", ""), d.get("SCRIP_CD", ""), "", d.get("Issuer_Name") or d.get("Scrip_Name"))
            r["sources"].add("bse_active")
    for d in K.read_csv(os.path.join(K.CACHE, "nse_equity_l.csv")):
        d = {k.strip(): v.strip() for k, v in d.items()}
        if d.get("SERIES") not in ("EQ", "BE", "BZ", "SM", "ST"):
            continue
        r = get(d.get("ISIN NUMBER", ""), "", d.get("SYMBOL", ""), d.get("NAME OF COMPANY", ""))
        r["sources"].add("nse_active")
    unretrievable = collections.Counter()
    for d in K.read_csv(K.DEAD_CSV):
        src = d["source"]
        if src == "nse_delisted":
            src = "nse_delisted_voluntary" if "voluntary" in d["event"] else "nse_delisted_forced"
        r = get(d["isin"], d["bse_code"], d["nse_symbol"], d["company"])
        if r is None:
            unretrievable[src] += 1
            continue
        r["sources"].add(src)
    rows = []
    for r in comp.values():
        s = r["sources"]
        if s & (DISTRESS | {"nse_delisted_forced"}):
            stratum = "D"
        elif s & {"bse_active", "nse_active"}:
            stratum = "L"
        else:
            stratum = "X"     # bse_delisted / nse voluntary delisting only
        r["stratum"] = stratum
        r["slug"] = r["bse_code"] or r["nse_symbol"]
        r["sources"] = "|".join(sorted(s))
        rows.append(r)
    rows.sort(key=lambda r: r["key"])
    pop = collections.Counter(r["stratum"] for r in rows)
    rng = random.Random(a.seed)
    take = {"D": None, "L": a.n_live, "X": a.n_delisted}
    out = []
    for s in ("D", "X", "L"):
        grp = [r for r in rows if r["stratum"] == s]
        smp = grp if take[s] is None or take[s] >= len(grp) else rng.sample(grp, take[s])
        w = len(grp) / len(smp)
        for r in sorted(smp, key=lambda r: r["key"]):
            r["weight"] = round(w, 4)
            out.append(r)
    # alternate slugs: if BSE code 404s, try NSE symbol
    K.write_csv(os.path.join(K.CACHE, "frame.csv"), out,
                ["key", "stratum", "weight", "slug", "bse_code", "nse_symbol", "isin", "name", "sources"])
    meta = {"population": dict(pop), "sample": dict(collections.Counter(r["stratum"] for r in out)),
            "seed": a.seed, "identifier_less_rows_dropped": dict(unretrievable)}
    K.jsave(os.path.join(K.CACHE, "frame_meta.json"), meta)
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
