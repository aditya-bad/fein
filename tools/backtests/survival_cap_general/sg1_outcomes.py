#!/usr/bin/env python3
"""Step 1: outcomes for the general survival-cap test (pre-registration: research_notes/Backtests/
survival_cap_general_india.md). Caches only, no network. Research tool, not SEBI-registered advice.
Sample E: events_flags.tsv (combined_avoid) + XS52/XS156 vs size-matched controls (survivorship-check control rule,
extended to 52/156 weeks; data-end-censored windows dropped), WIN3 (156w ratio >= 3), FAIL3 (<= 0.2x within 156w, or
series stops within 156w and firm on a distress list).
Sample P: panel_v2.csv (2016/2018 snapshots) + H12 (<= 0.5x px_T within 52w), XS52/XS156 vs same-snap size-matched
weighted controls, from cached screener charts.
Output: research_notes/Backtests/survival_cap_general_outputs/{events_out.tsv, panel_out.tsv, sg1_coverage.json}."""
import bisect, collections, csv, datetime as dt, glob, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "backtests", "combined_avoid"))
import common3 as C  # noqa: E402  (paths; pins solvency common)
OUT = os.path.join(ROOT, "research_notes", "Backtests", "survival_cap_general_outputs")
EV = os.path.join(ROOT, "research_notes", "Backtests", "combined_avoid_outputs", "events_flags.tsv")
PANEL = os.path.join(ROOT, "research_notes", "Backtests", "hard_filters_india_v2_outputs", "panel_v2.csv")
HS = (52, 156)
cov = collections.Counter()


def s4_head():
    """exec india_pead_survivorship/s4_events.py up to its main loop (load_px, load_universe, exit_idx, miss)."""
    import importlib.util
    d = os.path.join(ROOT, "tools", "backtests", "india_pead_survivorship")
    sp = importlib.util.spec_from_file_location("surv_common", os.path.join(d, "common.py"))
    Km = importlib.util.module_from_spec(sp); sp.loader.exec_module(Km)
    src = open(os.path.join(d, "s4_events.py")).read().split("\nlive_syms = ")[0].replace("import common as K", "")
    g = {"__file__": os.path.join(d, "s4_events.py"), "K": Km}
    exec(compile(src, "s4_head", "exec"), g)
    return g


def ret(px, i0, h, glast, exit_idx):
    """(return, censored). Censored = window cut short only because the data end (last close >= glast - 14d)."""
    j, early = exit_idx(px, i0, h)
    if j <= i0: return None, True
    if early and px["d"][-1] >= glast - dt.timedelta(days=14): return None, True
    return px["c"][j] / px["c"][i0] - 1, False


def sample_e():
    G = s4_head(); K = G["K"]
    live = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(K.V1, "results", "*.json")))
    data = G["load_universe"](K.V1, live, "L")
    data.update(G["load_universe"](K.OUT, sorted(G["miss"]), "M"))
    glast = max(v["px"]["d"][-1] for v in data.values())
    rows = list(csv.DictReader(open(EV), delimiter="\t"))
    # controls per entry Friday
    ents = sorted({r["entry"] for r in rows})
    ctrl = {}
    for a_ in ents:
        a = dt.date.fromisoformat(a_)
        for h in HS:
            m, rr, who = [], [], []
            for s2, v2 in data.items():
                px2 = v2["px"]; ia = px2["di"].get(a)
                if ia is None or ia < 50: continue
                mm = px2["mc"][ia]
                if not mm == mm: continue
                x, cen = ret(px2, ia, h, glast, G["exit_idx"])
                if cen: continue
                m.append(mm); rr.append(x); who.append(s2)
            ctrl[(a_, h)] = (np.array(m), np.array(rr), np.array(who))
    out = []
    for r in rows:
        o = dict(r); v = data.get(r["sym"])
        for h in HS: o[f"r{h}"] = o[f"c{h}"] = o[f"xs{h}"] = ""
        o["win3"] = o["fail3"] = ""
        if v is None: cov["E_no_px"] += 1; out.append(o); continue
        px = v["px"]; i0 = px["di"].get(dt.date.fromisoformat(r["entry"]))
        if i0 is None: cov["E_entry_not_in_px"] += 1; out.append(o); continue
        mc = float(r["mcap_cr"])
        for h in HS:
            x, cen = ret(px, i0, h, glast, G["exit_idx"])
            if cen: cov[f"E_censored_{h}"] += 1; continue
            m, rr, who = ctrl[(r["entry"], h)]
            sel = (m >= 0.5 * mc) & (m <= 2 * mc) & (who != r["sym"])
            o[f"r{h}"] = x
            if sel.sum() >= 5:
                o[f"c{h}"] = float(rr[sel].mean()); o[f"xs{h}"] = x - o[f"c{h}"]
            else: cov[f"E_few_controls_{h}"] += 1
        # FAIL3 / WIN3 over 156 weeks
        c0 = px["c"][i0]; end = px["d"][i0] + dt.timedelta(days=7 * 156 + 3)
        w = [c for d, c in zip(px["d"][i0 + 1:], px["c"][i0 + 1:]) if d <= end]
        crash = bool(w) and min(w) <= 0.2 * c0
        stopped = px["d"][-1] < end - dt.timedelta(days=7) and px["d"][-1] < glast - dt.timedelta(days=14)
        censored = px["d"][-1] < end - dt.timedelta(days=7) and not stopped
        f = crash or (stopped and r["distress"] == "1")
        o["fail3"] = int(f) if (f or not censored) else ""
        o["win3"] = "" if o["r156"] == "" else int(o["r156"] >= 2.0)
        cov["E_events"] += 1
        out.append(o)
    return out


def chart(slug):
    j = C.jl(os.path.join(C.SOLV, "sc", slug, "chart.json"), {}) or {}
    for ds in j.get("datasets", []):
        if ds["metric"] == "Price":
            return [(dt.date.fromisoformat(a), float(b)) for a, b, *_ in ds["values"] if b not in (None, "")]
    return []


def sample_p():
    T0 = {"FY2016": dt.date(2016, 9, 30), "FY2018": dt.date(2018, 9, 30)}
    rows = list(csv.DictReader(open(PANEL)))
    for r in rows:
        T = T0[r["snap"]]; px = chart(r["slug"])
        r["h12"] = r["pr52"] = r["pr156"] = ""
        pre = [p for d, p in px if d <= T]
        if not pre or pre[-1] <= 0: cov["P_no_px"] += 1; continue
        pT = pre[-1]
        w = [p for d, p in px if T < d <= T + dt.timedelta(days=364)]
        r["h12"] = int(bool(w) and min(w) <= 0.5 * pT)
        for h in HS:
            e = [p for d, p in px if d <= T + dt.timedelta(days=7 * h + 3)]
            r[f"pr{h}"] = e[-1] / pT - 1          # firm that stopped trading: return to its last close
        cov["P_ok"] += 1
    for h in HS:
        for r in rows:
            r[f"xs{h}"] = ""
            if r[f"pr{h}"] == "": continue
            mc = float(r["mcap"])
            cs = [(float(x["weight"]), x[f"pr{h}"]) for x in rows if x is not r and x["snap"] == r["snap"]
                  and x[f"pr{h}"] != "" and 0.5 * mc <= float(x["mcap"]) <= 2 * mc]
            if len(cs) >= 5:
                r[f"xs{h}"] = r[f"pr{h}"] - sum(a * b for a, b in cs) / sum(a for a, _ in cs)
            else: cov[f"P_few_controls_{h}"] += 1
    return rows


def write(path, rows, cols):
    with open(path, "w") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join(("%.6g" % r[c]) if isinstance(r.get(c), float) else str(r.get(c, "")) for c in cols) + "\n")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    E = sample_e()
    ecols = ["sym", "u", "cls", "distress", "qe", "entry", "mcap_cr", "sue", "fin", "pledge", "B25", "B50", "S1", "S2",
             "S4", "S5", "icr", "RED", "halve12", "r52", "c52", "xs52", "r156", "c156", "xs156", "win3", "fail3"]
    write(os.path.join(OUT, "events_out.tsv"), E, ecols)
    P = sample_p()
    pcols = ["key", "stratum", "weight", "slug", "name", "industry", "snap", "mcap", "s1", "s2", "s4", "s5", "icr",
             "pledge", "B25", "B50", "o_fail", "o_strict", "winner", "r5", "h12", "pr52", "xs52", "pr156", "xs156"]
    write(os.path.join(OUT, "panel_out.tsv"), P, pcols)
    json.dump(dict(cov), open(os.path.join(OUT, "sg1_coverage.json"), "w"), indent=1)
    print(dict(cov))
