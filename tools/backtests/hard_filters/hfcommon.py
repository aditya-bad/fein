"""Shared helpers for the hard-filter back-test (Part A case studies, Part B universe snapshot).

parse_screener(path) -> {"basis", "FY": {year: {field: value}}, "BSE": code or None}
    Annual tables of a cached screener.in company page (profit-loss, balance-sheet, cash-flow, ratios).
    Fiscal year = calendar year of the 'Mar YYYY' (or other month) column; values in Rs crore.
metrics_at(fy, last_fy) -> mechanical filter metrics using only fiscal years <= last_fy.
    The caller decides last_fy from the snapshot date (point-in-time rule: an Indian FY ending in
    March is treated as public only from 30 September of that year, i.e. after the annual report).
Screener pages are restated/current, not point-in-time: a known limitation (see report).
"""
import html
import re

ROWS = {
    "sales": "sales", "revenue": "sales", "operating profit": "op", "financing profit": "op",
    "other income": "oi", "interest": "interest", "depreciation": "dep", "profit before tax": "pbt",
    "net profit": "pat", "equity capital": "eqcap", "reserves": "reserves", "borrowings": "debt",
    "total liabilities": "ta", "investments": "inv", "cash from operating activity": "cfo",
    "cash from investing activity": "cfi", "cash from financing activity": "cff",
    "free cash flow": "fcf", "debtor days": "debtor_days", "inventory days": "inv_days",
    "working capital days": "wc_days", "roce %": "roce", "opm %": "opm", "financing margin %": "opm",
    "deposits": "deposits",
}
SECTIONS = ("profit-loss", "balance-sheet", "cash-flow", "ratios")


def _num(s):
    s = s.replace(",", "").replace("%", "").strip()
    if s in ("", "-", "--"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_screener(path):
    page = open(path, errors="replace").read()
    out = {"basis": "consolidated" if "basis:consolidated" in page[:80] else "standalone", "FY": {}}
    m = re.search(r"bseindia\.com/[^\"']*?/(\d{6})/", page)
    out["BSE"] = m.group(1) if m else None
    for sec in SECTIONS:
        i = page.find('id="%s"' % sec)
        if i < 0:
            continue
        j = page.find("</table>", i)
        t = page[i:j]
        heads = [html.unescape(re.sub(r"<[^>]+>|\s+", " ", x)).strip() for x in re.findall(r"<th[^>]*>(.*?)</th>", t, re.S)]
        cols = heads[1:]
        years, mons = [], []
        for h in cols:
            mm = re.match(r"([A-Za-z]{3})\s+(\d{4})", h)
            years.append(int(mm.group(2)) if mm else None)
            mons.append(mm.group(1) if mm else None)
        fym = max(set(x for x in mons if x), key=mons.count) if any(mons) else None
        years = [y if mo == fym else None for y, mo in zip(years, mons)]   # drop half-year columns
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
            tds = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x))).strip()
                   for x in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
            if not tds:
                continue
            label = re.sub(r"\s*\+$", "", tds[0]).strip().lower()
            f = ROWS.get(label)
            if not f:
                continue
            for y, v in zip(years, tds[1:]):
                if y is None:
                    continue
                val = _num(v)
                if val is not None:
                    out["FY"].setdefault(y, {})[f] = val
    return out


def _s(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) if vals else None


def metrics_at(fy, last_fy, n=5):
    """Mechanical filter metrics from fiscal years (last_fy-n+1 .. last_fy)."""
    ys = [y for y in sorted(fy) if y <= last_fy][-n:]
    if len(ys) < 3:
        return {"n_years": len(ys)}
    g = lambda f, y: fy.get(y, {}).get(f)
    cfo = [g("cfo", y) for y in ys]
    pat = [g("pat", y) for y in ys]
    fcf = [g("fcf", y) for y in ys]
    m = {"n_years": len(ys), "first_fy": ys[0], "last_fy": ys[-1]}
    sc, sp = _s(cfo), _s(pat)
    m["sum_cfo"], m["sum_pat"], m["sum_fcf"] = sc, sp, _s(fcf)
    m["cfo_pat"] = round(sc / sp, 3) if sc is not None and sp and sp > 0 else None
    m["pat_nonpos"] = sp is not None and sp <= 0
    d0, d1 = g("debt", ys[-4]) if len(ys) >= 4 else g("debt", ys[0]), g("debt", ys[-1])
    m["debt_start"], m["debt_end"] = d0, d1
    cfo3 = _s(cfo[-3:])
    m["sum_cfo_3y"] = cfo3
    if d0 is None or d1 is None:
        m["debt_growth"] = None
    elif d0 > 0:
        m["debt_growth"] = round(d1 / d0, 2)
    else:                                   # from zero debt: 'grew' only if debt now material (>5% of sales)
        s_last = g("sales", ys[-1]) or 0
        m["debt_growth"] = 99.0 if d1 > 0.05 * s_last else 1.0
    eq = (g("eqcap", ys[-1]) or 0) + (g("reserves", ys[-1]) or 0)
    m["equity"] = eq
    m["de"] = round(d1 / eq, 2) if d1 is not None and eq > 0 else None
    oi, pbt = g("oi", ys[-1]), g("pbt", ys[-1])
    oi3, pbt3 = _s([g("oi", y) for y in ys[-3:]]), _s([g("pbt", y) for y in ys[-3:]])
    m["oi_pbt"] = round(oi / pbt, 3) if oi is not None and pbt and pbt > 0 else None
    m["oi_pbt_3y"] = round(oi3 / pbt3, 3) if oi3 is not None and pbt3 and pbt3 > 0 else None
    dd = [g("debtor_days", y) for y in ys]
    m["debtor_days"] = dd[-1]
    m["debtor_days_d2"] = (dd[-1] - dd[-3]) if dd[-1] is not None and len(dd) >= 3 and dd[-3] is not None else None
    s = [g("sales", y) for y in ys]
    m["sales_cagr"] = round((s[-1] / s[0]) ** (1 / (len(ys) - 1)) - 1, 3) if s[0] and s[-1] and s[0] > 0 and s[-1] > 0 else None
    eqc = [g("eqcap", y) for y in ys]
    m["eqcap_growth"] = round(eqc[-1] / eqc[-4], 2) if len(eqc) >= 4 and eqc[-4] and eqc[-1] else None
    return m


# mechanical rule definitions (shared by Part A and Part B)
def rules(m, lender=False):
    """-> {rule: True/False/None}; None = not computable (or not applicable for lenders)."""
    r = {}
    if m.get("n_years", 0) < 3:
        return {k: None for k in ("F1_cfo_pat_lt_0.7", "F1b_cfo_pat_lt_0.3", "G2_debt_up_neg_cfo",
                                  "G5_neg_fcf", "G6_debtor_days", "F2_other_income")}
    na = lender
    cp = m.get("cfo_pat")
    if na:
        r["F1_cfo_pat_lt_0.7"] = r["F1b_cfo_pat_lt_0.3"] = r["G2_debt_up_neg_cfo"] = r["G5_neg_fcf"] = None
    else:
        if m.get("pat_nonpos"):
            r["F1_cfo_pat_lt_0.7"] = r["F1b_cfo_pat_lt_0.3"] = None   # loss-makers: ratio undefined
        else:
            r["F1_cfo_pat_lt_0.7"] = None if cp is None else cp < 0.7
            r["F1b_cfo_pat_lt_0.3"] = None if cp is None else cp < 0.3
        dg, c3 = m.get("debt_growth"), m.get("sum_cfo_3y")
        r["G2_debt_up_neg_cfo"] = None if dg is None or c3 is None else (dg >= 1.5 and (m.get("debt_end") or 0) > 0 and c3 < 0)
        f = m.get("sum_fcf")
        r["G5_neg_fcf"] = None if f is None else f < 0
    dd, d2 = m.get("debtor_days"), m.get("debtor_days_d2")
    r["G6_debtor_days"] = None if dd is None else (dd > 120 or (d2 is not None and d2 > 30))
    o = m.get("oi_pbt_3y")
    r["F2_other_income"] = None if (o is None or lender) else o > 0.30   # lenders: other income = fees
    if lender:
        r["G6_debtor_days"] = None
    return r
