#!/usr/bin/env python3
"""Step 3: build the (company, snapshot) panel: flags at T (solvency_screen.inputs/flags on annual data cut at FY0),
size, and outcomes in (T, T+5y]. Reads caches only (no network). Output: research_notes/.../solvency_india_outputs/panel.csv
and funnel.json."""
import collections, datetime as dt, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K

SS, F = K.SS, K.F


def events_by_key(frame):
    alias = {}
    for r in frame:
        for t, f in (("isin", "isin"), ("bse", "bse_code"), ("nse", "nse_symbol")):
            if r[f]:
                alias.setdefault((t, r[f].upper()), r["key"])
    ev = collections.defaultdict(list)
    for d in K.read_csv(K.DEAD_CSV):
        k = None
        for t, f in (("isin", "isin"), ("bse", "bse_code"), ("nse", "nse_symbol")):
            if d[f] and (t, d[f].upper()) in alias:
                k = alias[(t, d[f].upper())]
                break
        if k:
            ev[k].append(d)
    return ev


def load_sched(d):
    out = {}
    for parent, _ in SS.SCHEDULES:
        p = os.path.join(d, re.sub(r"\W+", "_", parent).lower() + ".json")
        out[parent] = K.jload(p, {}) or {}
    return out


def price_series(chart):
    for ds in (chart or {}).get("datasets", []):
        if ds["metric"] == "Price":
            return [(dt.date.fromisoformat(a), float(b)) for a, b, *_ in ds["values"] if b not in (None, "")]
    return []


def cut(fin, fy0):
    return {"FY": {d: v for d, v in fin["FY"].items() if d <= fy0},
            "BS": {d: v for d, v in fin["BS"].items() if d <= fy0}}


def d_or_none(s):
    try:
        return dt.date.fromisoformat(s) if s else None
    except ValueError:
        return None


def outcomes(px, T, evs, sources):
    end = K.addy(T, K.WIN_YEARS)
    o = {}
    pT = [p for d, p in px if d <= T][-1]
    win = [(d, p) for d, p in px if T < d <= end]
    last = px[-1][0] if px else None
    o["px_T"] = pT
    o["min_ratio"] = round(min((p for _, p in win), default=pT) / pT, 4) if pT > 0 else None
    o["o_px"] = int(o["min_ratio"] is not None and o["min_ratio"] <= 0.2)
    o["last_px_date"] = last.isoformat() if last else ""
    stopped = last is not None and T < last <= end - dt.timedelta(days=90)
    o["stopped_in_window"] = int(stopped)
    cirp = [d_or_none(e["event_date"]) for e in evs if e["source"] == "ibbi_cirp"]
    liq = [(d_or_none(e["event_date"]), e) for e in evs if e["source"] == "ibbi_liq"]
    o["cirp_before_T"] = int(any(d and d <= T for d in cirp) or any(d and d <= T for d, _ in liq))
    o["o_cirp"] = int(any(d and T < d <= end for d in cirp))
    o_liq, undated = 0, 0
    for d, _ in liq:
        if d and T < d <= end:
            o_liq = 1
        elif d is None:
            if o["o_cirp"] or stopped:
                o_liq = 1
            else:
                undated = 1
    o["o_liq"], o["liq_undated"] = o_liq, undated
    nse = [d_or_none(e["event_date"]) for e in evs if e["source"] == "nse_delisted"
           and ("compulsory" in e["event"] or "liquidation" in e["event"])]
    o["o_cdel"] = int(any(d and T < d <= end for d in nse) or ("bse_suspended" in sources and stopped))
    o["o_fail"] = int(o["o_liq"] or o["o_cdel"] or o["o_px"])
    o["o_strict"] = int(o["o_liq"] or o["o_cdel"])
    # R5
    at_end = [(d, p) for d, p in px if d <= end]
    if at_end and (end - at_end[-1][0]).days <= 31 and pT > 0:
        o["r5"] = round(at_end[-1][1] / pT, 4)
    else:
        o["r5"] = None
    if o["r5"] is not None:
        o["winner"] = int(o["r5"] >= 3)
    else:
        o["winner"] = 0 if o["o_fail"] else None
    return o


def main():
    frame = K.read_csv(os.path.join(K.CACHE, "frame.csv"))
    st = K.jload(os.path.join(K.CACHE, "fetch_status.json"), {})
    ev = events_by_key(frame)
    fun = collections.Counter()
    rows = []
    for r in frame:
        s = st.get(r["key"], {})
        strat = r["stratum"]
        fun[(strat, "frame_sampled")] += 1
        if s.get("page") != "ok":
            fun[(strat, "no_page" if s.get("page") == "no_page" else "not_fetched")] += 1
            continue
        if s["fin"]:
            fun[(strat, "financial")] += 1
            continue
        d = os.path.join(K.CACHE, "sc", s["slug"])
        page = chart = None
        for sn, T in K.SNAPS.items():
            key = (strat, sn)
            if not s["elig"].get(sn):
                fun[key + ("no_annual_at_T",)] += 1
                continue
            z = (s.get("size") or {}).get(sn)
            if not z:
                fun[key + ("chart_not_fetched",)] += 1
                continue
            if z["status"] != "ok":
                fun[key + (z["status"],)] += 1
                continue
            if not (K.MCAP_LO <= z["mcap"] <= K.MCAP_HI):
                fun[key + ("out_of_size_band",)] += 1
                continue
            if s.get("sched") != "ok":
                fun[key + ("schedules_missing",)] += 1
                continue
            if page is None:
                page = open(os.path.join(d, "page.html"), errors="replace").read()
                chart = K.jload(os.path.join(d, "chart.json"), {})
                fin = F.parse_screener(page)
                sched = load_sched(d)
                px = price_series(chart)
            fy0 = dt.date.fromisoformat(s["elig"][sn])
            x = SS.inputs(cut(fin, fy0), sched)
            if x is None:
                fun[key + ("inputs_none",)] += 1
                continue
            f = SS.flags(x)
            o = outcomes(px, T, ev.get(r["key"], []), r["sources"])
            if o["cirp_before_T"]:
                fun[key + ("in_insolvency_at_T",)] += 1
                continue
            fun[key + ("panel",)] += 1
            bs0 = fin["BS"][fy0]
            inv = bs0.get("investments")
            std, cash, cfo = x["std"], x["cash"], x["cfo"]
            if std is None:
                s3i = 0 if x["debt0"] == 0 else None
            elif cash is None or cfo is None:
                s3i = 0 if std <= 0 else None
            else:
                s3i = int(std > 0 and std > cash + (inv or 0) + 0.5 * cfo)
            row = {"key": r["key"], "stratum": strat, "weight": float(r["weight"]), "slug": s["slug"],
                   "name": s.get("name", ""), "industry": s.get("industry", ""), "snap": sn, "fy0": fy0.isoformat(),
                   "mcap": round(z["mcap"], 1), "size_ambiguous": int(z["mcap_lo"] < K.MCAP_LO <= z["mcap_hi"] or
                                                                     z["mcap_lo"] <= K.MCAP_HI < z["mcap_hi"]),
                   "sources": r["sources"]}
            row.update({k: x[k] for k in ("net_worth", "ebit", "interest", "std", "cash", "cfo", "fcf", "dividends",
                                          "debt0", "debt1", "assets")})
            row["investments"] = inv
            row.update({k: f[k] for k in ("icr", "s1raw", "s1", "s2", "s2b", "s3", "s4", "s5", "s5b", "s5_us")})
            row["s0"] = None if x["ebit"] is None else int(x["ebit"] < 0)
            row["s3_india"] = s3i
            row.update(o)
            rows.append(row)
    os.makedirs(K.OUTDIR, exist_ok=True)
    K.write_csv(os.path.join(K.OUTDIR, "panel.csv"), rows)
    fj = {"|".join(k): v for k, v in sorted(fun.items())}
    K.jsave(os.path.join(K.OUTDIR, "funnel.json"), fj)
    print(json.dumps(fj, indent=1))
    print("panel rows", len(rows))


if __name__ == "__main__":
    main()
