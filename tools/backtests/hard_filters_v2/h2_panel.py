#!/usr/bin/env python3
"""Step 2: compute the pre-registered v2 rules for every row of the solvency_india panel (reads caches only).
Rules (see research_notes/Backtests/hard_filters_india_v2.md): A CFO/PAT 5y<0.3 (A7 <0.7); B25/B50 pledge at T;
B_rise; C debt>=1.5x in 3y with sum3y CFO<0; D50 other income/PBT 3y >50% (D30); E debtor days x1.5 in 3y (E60);
ANY, ANY_np, TWO+. Output: research_notes/Backtests/hard_filters_india_v2_outputs/panel_v2.csv, coverage.json."""
import collections, datetime as dt, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common2 as C
sys.path.insert(0, os.path.join(C.ROOT, "tools", "backtests", "hard_filters"))
import hfcommon as H  # screener table parser (keys: sales, oi, pbt, pat, debt, cfo, debtor_days ...)
from h1_pledge_fetch import targets

K = C.K
cov = collections.Counter()


def s_(v):
    v = [x for x in v if x is not None]
    return sum(v) if v else None


def fin_rules(fy, y0):
    g = lambda f, y: fy.get(y, {}).get(f)
    out = {}
    # (a) CFO/PAT, up to 5 years ending y0, years with both values, >= 3 years
    yrs = [y for y in range(y0 - 4, y0 + 1) if g("cfo", y) is not None and g("pat", y) is not None]
    if len(yrs) < 3:
        out["cfo_pat"], out["A"], out["A7"] = None, None, None
        cov["A_unknown_few_years"] += 1
    else:
        sc, sp = sum(g("cfo", y) for y in yrs), sum(g("pat", y) for y in yrs)
        if sp <= 0:
            out["cfo_pat"], out["A"], out["A7"] = None, None, None
            cov["A_unknown_pat_sum_nonpos"] += 1
        else:
            r = sc / sp
            out["cfo_pat"], out["A"], out["A7"] = round(r, 3), int(r < 0.3), int(r < 0.7)
    # (c) debt growth with negative CFO
    d0, d3 = g("debt", y0), g("debt", y0 - 3)
    c3 = [g("cfo", y) for y in (y0 - 2, y0 - 1, y0)]
    if d0 is None or d3 is None or any(v is None for v in c3):
        out["C"] = None
        cov["C_unknown"] += 1
    else:
        grew = (d0 >= 1.5 * d3) if d3 > 0 else (d0 > 0.05 * (g("sales", y0) or 0) and d0 > 0)
        out["C"] = int(bool(grew) and sum(c3) < 0)
    out["debt_g3"] = round(d0 / d3, 2) if d0 is not None and d3 else None
    out["cfo_3y"] = round(sum(c3), 2) if all(v is not None for v in c3) else None
    # (d) other income share of PBT, 3 years (>= 2 with both)
    yy = [y for y in (y0 - 2, y0 - 1, y0) if g("oi", y) is not None and g("pbt", y) is not None]
    if len(yy) < 2:
        out["oi_pbt"], out["D50"], out["D30"] = None, None, None
        cov["D_unknown_few_years"] += 1
    else:
        oi, pbt = sum(g("oi", y) for y in yy), sum(g("pbt", y) for y in yy)
        if pbt <= 0:
            out["oi_pbt"], out["D50"], out["D30"] = None, None, None
            cov["D_unknown_pbt_nonpos"] += 1
        else:
            r = oi / pbt
            out["oi_pbt"], out["D50"], out["D30"] = round(r, 3), int(r > 0.5), int(r > 0.3)
    # (e) receivable days
    dd0, dd3 = g("debtor_days", y0), g("debtor_days", y0 - 3)
    if dd0 is None or dd3 is None or dd3 <= 0:
        out["E"], out["E60"], out["dd_ratio"] = None, None, None
        cov["E_unknown"] += 1
    else:
        r = dd0 / dd3
        out["dd_ratio"], out["E"], out["E60"] = round(r, 3), int(r > 1.5), int(r > 1.5 and dd0 >= 60)
    out["debtor_days"] = dd0
    return out


def xval(body, tag, ctx):
    m = re.search(r"<in-bse-shp:%s contextRef=\"%s(?:_ContextI|I)\"[^>]*>\s*([0-9.]+)" % (tag, ctx), body)
    return float(m.group(1)) if m else None


def pledge_from(path):
    if not os.path.exists(path):
        return None, "xml_missing"
    body = open(path, errors="replace").read()
    P = "ShareholdingOfPromoterAndPromoterGroup"
    prom = xval(body, "NumberOfShares", P)
    pl = xval(body, "PledgedOrEncumberedNumberOfShares", P)
    decl = re.search(r"WhetherAnySharesHeldByPromotersArePledgeOrOtherwiseEncumbered\" ?[^>]*>\s*(true|false)", body) or \
        re.search(r"WhetherAnySharesHeldByPromotersArePledgeOrOtherwiseEncumbered[^>]*>\s*(true|false)", body)
    if prom is None:
        if "<in-bse-shp:" not in body:
            return None, "not_xbrl"
        if decl and decl.group(1) == "false":
            return 0.0, "ok_declared_none"
        return None, "parse_fail"
    if prom == 0:
        return 0.0, "ok_no_promoter"
    if pl is None:
        pct = xval(body, "PledgedOrEncumberedSharesHeldAsPercentageOfTotalNumberOfShares", P)
        if pct is not None:
            return pct, "ok_pct_tag"
        if decl and decl.group(1) == "true":
            return None, "parse_fail_declared_true"
        return 0.0, "ok_no_pledge_tag"
    return round(100 * pl / prom, 2), "ok"


def pledge_rules(code, T):
    if not code:
        return {"pledge": None, "pledge_status": "no_bse_code"}
    lp = os.path.join(C.CACHE2, "shp", code, "list.json")
    if not os.path.exists(lp):
        return {"pledge": None, "pledge_status": "list_not_fetched"}
    tg = targets(K.jload(lp, []), T)
    if "at_T" not in tg:
        return {"pledge": None, "pledge_status": "no_shp_in_window"}
    x = tg["at_T"]
    u = x.get("xbrlurl") or ""
    if not u.endswith(".xml"):
        return {"pledge": None, "pledge_status": "no_xml", "shp_qtr": x.get("qtr")}
    v, st = pledge_from(os.path.join(C.CACHE2, "shp", code, os.path.basename(u)))
    o = {"pledge": v, "pledge_status": st, "shp_qtr": x.get("qtr"), "shp_filed": (x.get("filing_date_time") or "")[:10]}
    pv = None
    if "prior" in tg and (tg["prior"].get("xbrlurl") or "").endswith(".xml"):
        pv, _ = pledge_from(os.path.join(C.CACHE2, "shp", code, os.path.basename(tg["prior"]["xbrlurl"])))
    o["pledge_prior"] = pv
    return o


def main():
    frame = {r["key"]: r for r in K.read_csv(os.path.join(K.CACHE, "frame.csv"))}
    st = K.jload(os.path.join(K.CACHE, "fetch_status.json"), {})
    rows = K.read_csv(C.PANEL)
    out, cache = [], {}
    for r in rows:
        slug = r["slug"]
        if slug not in cache:
            cache[slug] = H.parse_screener(os.path.join(K.CACHE, "sc", slug, "page.html"))
        fin = cache[slug]
        fy0 = dt.date.fromisoformat(r["fy0"])
        y0 = fy0.year
        row = dict(r)
        if y0 not in fin["FY"] or fin["FY"][y0].get("pat") is None:
            cov["fy0_not_in_parse"] += 1
            row.update({k: None for k in ("A", "A7", "C", "D50", "D30", "E", "E60")})
        else:
            row.update(fin_rules(fin["FY"], y0))
        code = frame[r["key"]]["bse_code"] or (fin.get("BSE") or "")
        T = K.SNAPS[r["snap"]]
        p = pledge_rules(code, T)
        cov["pledge_" + p["pledge_status"]] += 1
        row.update(p)
        v = p.get("pledge")
        row["B25"] = None if v is None else int(v > 25)
        row["B50"] = None if v is None else int(v > 50)
        pv = p.get("pledge_prior")
        row["B_rise"] = None if v is None or pv is None else int(v >= pv + 10)
        comps = [row["A"], row["B25"], row["C"], row["D50"], row["E"]]
        row["ANY"] = 1 if 1 in comps else (0 if None not in comps else None)
        c2 = [row["A"], row["C"], row["D50"], row["E"]]
        row["ANY_np"] = 1 if 1 in c2 else (0 if None not in c2 else None)
        nf = sum(1 for c in comps if c == 1)
        nk = sum(1 for c in comps if c is not None)
        row["n_flags"] = nf
        row["TWO"] = 1 if nf >= 2 else (0 if nf + (5 - nk) < 2 else None)
        # comparison outcome with old Part B
        r5 = row["r5"]
        if r5 not in ("", None):
            row["loss50"] = int(float(r5) < 0.5)
        else:
            row["loss50"] = 1 if row["o_fail"] == "1" else None
        out.append(row)
    os.makedirs(C.OUT, exist_ok=True)
    K.write_csv(os.path.join(C.OUT, "panel_v2.csv"), out)
    cj = dict(sorted(cov.items()))
    for k in ("A", "A7", "B25", "B50", "B_rise", "C", "D50", "D30", "E", "E60", "ANY", "ANY_np", "TWO"):
        cj["known_" + k] = sum(1 for x in out if x[k] is not None)
        cj["fired_" + k] = sum(1 for x in out if x[k] == 1)
    K.jsave(os.path.join(C.OUT, "coverage.json"), cj)
    print(json.dumps(cj, indent=1))


if __name__ == "__main__":
    main()
