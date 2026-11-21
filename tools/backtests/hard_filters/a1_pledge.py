#!/usr/bin/env python3
"""Part A helper: promoter pledge (% of promoter holding) from the BSE shareholding-pattern XBRL of a
given quarter -- the last quarter whose SHP was FILED before the episode date T (point-in-time).

  python3 a1_pledge.py OUT.json BSE_CODE:YYYY-MM-DD [BSE_CODE:YYYY-MM-DD ...]

For each code it lists the BSE SHP filings (SHPQNewFormat), keeps those with filing_date_time < T,
takes the latest, downloads its XBRL and reads PledgedOrEncumbered* for the promoter context.
Older SHPs (pre ~2016) may have no XBRL; those come back as status no_xml (pledge unknown)."""
import json, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import bse_fetch as b  # noqa: E402

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def get(url):
    r = subprocess.run(["curl", "-sS", "--http2", "--compressed", "-A", UA, "-H", "Referer: https://www.bseindia.com/",
                        "--max-time", "60", url], capture_output=True, timeout=90)
    return r.stdout.decode("utf-8", "replace")


def pledge_at(code, T):
    lst = b.api("SHPQNewFormat/w", scripcode=code, qtrid="", Type="EQ").get("Table", [])
    prior = [x for x in lst if (x.get("filing_date_time") or "9999")[:10] < T]
    if not prior:
        return {"status": "no_prior_shp"}
    x = max(prior, key=lambda z: z["filing_date_time"])
    res = {"qtr": x["qtr"], "filed": x["filing_date_time"][:10], "xbrlurl": x.get("xbrlurl")}
    if not (x.get("xbrlurl") or "").endswith(".xml"):
        # older filings: try the previous few, else unknown
        res["status"] = "no_xml"
        return res
    time.sleep(1.5)
    body = get("https://www.bseindia.com" + x["xbrlurl"])
    def val(tag, ctx):
        # two schema generations: '<Ctx>_ContextI' (2019+) and '<Ctx>I' (older)
        m = re.search(r"<in-bse-shp:%s contextRef=\"%s(?:_ContextI|I)\"[^>]*>\s*([0-9.]+)" % (tag, ctx), body)
        return float(m.group(1)) if m else None
    P = "ShareholdingOfPromoterAndPromoterGroup"
    res["pledge_pct_of_promoter"] = val("PledgedOrEncumberedSharesHeldAsPercentageOfTotalNumberOfShares", P)
    res["promoter_shares"] = val("NumberOfShares", P)
    res["total_shares"] = val("NumberOfShares", "ShareholdingPattern")
    if res["promoter_shares"] and res["total_shares"]:
        res["promoter_pct"] = round(100 * res["promoter_shares"] / res["total_shares"], 2)
    res["status"] = "ok" if res["pledge_pct_of_promoter"] is not None or res["promoter_shares"] else "parse_fail"
    return res


if __name__ == "__main__":
    out = sys.argv[1]
    data = json.load(open(out)) if os.path.exists(out) else {}
    for arg in sys.argv[2:]:
        code, T = arg.split(":")
        k = code + ":" + T
        if k in data and data[k].get("status") == "ok":
            continue
        try:
            data[k] = pledge_at(code, T)
        except Exception as e:  # network / format
            data[k] = {"status": "error", "err": str(e)[:200]}
        print(k, data[k], flush=True)
        json.dump(data, open(out, "w"), indent=1)
