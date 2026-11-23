#!/usr/bin/env python3
"""Step 3a: as-of-event flags (pledge B25/B50 from the latest fetched June-quarter SHP filed before the event;
S1/S2/S4/S5-India from the latest standalone annual column ending <= event - 6 months) and the 12-month halving
outcome, for every event in bt_pead_surv/events_w.tsv. Caches only, no network.
Output: $BT_COMB/events_flags.tsv, $BT_COMB/c3_coverage.json. Pre-registration: combined_avoid_india.md."""
import bisect, collections, csv, datetime as dt, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common3 as C
import solvency_screen as SS
from s3_panel import cut                     # solvency_india: annual columns <= FY0
from h2_panel import pledge_from             # hard_filters_v2: pledge % from SHP XBRL (unchanged)
from c2_fetch_bse import june_shps, find

cov = collections.Counter()
CF = "Cash from Financing Activity"


def load_price_fns():
    """Reuse india_pead_survivorship/s4_events.load_px (the event file's own weekly-close builder) without running s4."""
    src = open(os.path.join(C.ROOT, "tools", "backtests", "india_pead_survivorship", "s4_events.py")).read()
    src = src.split("\nlive_syms = ")[0].replace("import common as K", "")
    import importlib.util
    sp = importlib.util.spec_from_file_location("surv_common", os.path.join(C.ROOT, "tools", "backtests",
                                                "india_pead_survivorship", "common.py"))
    Km = importlib.util.module_from_spec(sp); sp.loader.exec_module(Km)
    g = {"__file__": os.path.join(C.ROOT, "tools", "backtests", "india_pead_survivorship", "s4_events.py"), "K": Km}
    exec(compile(src, "s4_events_head", "exec"), g)
    return g


def pledge_at(code, ev):
    if not code: return None, "no_bse_code", None
    lp = find(code, "list.json")
    if not lp: return None, "list_not_fetched", None
    best = None
    for y, x in june_shps(C.jl(lp, [])).items():
        fd = dt.date.fromisoformat(x["filing_date_time"][:10])
        qe = dt.date(y, 6, 30)
        if fd < ev and (ev - qe).days <= 456 and (best is None or fd > best[0]): best = (fd, x)
    if not best: return None, "no_june_shp_in_window", None
    u = best[1].get("xbrlurl") or ""
    if not u.endswith(".xml"): return None, "no_xml", best[0]
    p = find(code, os.path.basename(u))
    if not p or not os.path.exists(p): return None, "xml_not_fetched", best[0]
    v, s = pledge_from(p)
    return v, s, best[0]


def main():
    ids = C.id_maps()
    ssc = C.jl(os.path.join(C.OUT, "status_sc.json"), {})
    G = load_price_fns()
    px = {}
    fins = {}
    rows = list(csv.DictReader(open(os.path.join(C.SURV, "events_w.tsv")), delimiter="\t"))
    for sym in dict.fromkeys(r["sym"] for r in rows):
        u = next(r["u"] for r in rows if r["sym"] == sym)
        px[sym] = G["load_px"](G["K"].V1 if u == "L" else G["K"].OUT, sym, u == "M")
        s = ssc.get(sym, {})
        if s.get("page") and os.path.exists(s["page"]):
            page = open(s["page"], errors="replace").read()
            lab = SS.labels(page)
            fin = SS.F.parse_screener(page)
            sched = {CF: C.jl(s.get("cf", ""), {}) or {}}
            fins[sym] = (fin, sched, int(SS.is_financial(lab, page)))
    glast = max(p["d"][-1] for p in px.values() if p)
    out = []
    for r in rows:
        sym = r["sym"]; ev = dt.date.fromisoformat(r["event"][:10]); entry = dt.date.fromisoformat(r["entry"])
        o = {k: r[k] for k in ("sym", "u", "cls", "distress", "qe", "event", "entry", "mcap_cr", "sue", "r13", "cA13",
                               "r26", "cA26")}
        # pledge
        v, s, fd = pledge_at(ids[sym].get("bse_code"), ev)
        cov["pledge_" + s] += 1
        o.update(pledge=v, pledge_status=s, shp_filed=fd, B25=None if v is None else int(v > 25),
                 B50=None if v is None else int(v > 50))
        # annual flags
        o.update(fy0=None, S1=None, S2=None, S4=None, S5=None, icr=None, fin=None)
        if sym not in fins:
            cov["annual_no_page"] += 1
        else:
            fin, sched, isf = fins[sym]; o["fin"] = isf
            lim = ev - dt.timedelta(days=183)
            c = [d for d in fin["FY"] if d <= lim and d in fin["BS"]]
            if not c:
                cov["annual_no_fy0"] += 1
            else:
                fy0 = max(c)
                if (ev - fy0).days > 731:
                    cov["annual_fy0_too_old"] += 1
                else:
                    x = SS.inputs(cut(fin, fy0), sched)
                    if x is None: cov["annual_inputs_none"] += 1
                    else:
                        f = SS.flags(x); cov["annual_ok"] += 1
                        o.update(fy0=fy0, S1=f["s1"], S2=f["s2"], S4=f["s4"], S5=f["s5"],
                                 icr=None if f["icr"] is None else round(f["icr"], 3))
        comps = [o["B25"], o["S2"], o["S5"]]
        if 1 in comps: o["RED"] = 1
        elif o["B25"] is not None and o["S2"] is not None: o["RED"] = 0
        else: o["RED"] = None
        o["RED_u0"] = 1 if 1 in comps else 0
        # halving within 52 weeks of entry
        p = px.get(sym)
        o["halve12"] = None
        if p:
            i0 = bisect.bisect_left(p["d"], entry)
            if i0 < len(p["d"]) and p["d"][i0] == entry:
                c0 = p["c"][i0]; end = entry + dt.timedelta(days=364)
                w = [cc for d, cc in zip(p["d"][i0 + 1:], p["c"][i0 + 1:]) if d <= end]
                hv = int(bool(w) and min(w) <= 0.5 * c0)
                last = p["d"][-1]
                if not hv and last < end - dt.timedelta(days=7) and last >= glast - dt.timedelta(days=14):
                    cov["halve_drop_data_end"] += 1
                else:
                    o["halve12"] = hv; o["halve_series_ended"] = int(last < end - dt.timedelta(days=7))
            else:
                cov["halve_entry_not_in_px"] += 1
        else:
            cov["halve_no_px"] += 1
        cov["RED_" + str(o["RED"])] += 1
        out.append(o)
    cols = list(dict.fromkeys(k for o in out for k in o))
    with open(os.path.join(C.OUT, "events_flags.tsv"), "w") as f:
        f.write("\t".join(cols) + "\n")
        for o in out:
            f.write("\t".join("" if o.get(c) is None else str(o[c]) for c in cols) + "\n")
    C.js(os.path.join(C.OUT, "c3_coverage.json"), dict(sorted(cov.items())))
    print(json.dumps(dict(sorted(cov.items())), indent=1))


if __name__ == "__main__":
    main()
