#!/usr/bin/env python3
"""FEIN decision card (roadmap stage 6) + paper-call emitter (stage 7).

Standard library only (runs on a Raspberry Pi, Python >= 3.7).

Assembles ONE card from:
  stage 2  hard-filter results (non-overridable) and graded flags
  stage 3  signal flags: earnings-surprise quintile avoid flag (L17/L19), sector-adjusted promise
           credibility (L18), detector alerts
  stage 4  deep-dive soft flags and the written override log (insight:flag-override-template)
  stage 5  the valuation worksheet (tools/valuation/worksheet.py) run on the company input file
and writes:
  - a Markdown card filled into tools/decision/decision_card.md
  - a JSON list of memdb records: 3 dated paper calls (P >=3x, P <=0.5x, P blow-up over 5 years) and one
    decision record, in the memdb seed format, so the card is scored automatically later.

Usage:
  python3 decision_card.py card.json -o card.md --calls calls.json
  python3 decision_card.py --template > new_card.json

The output is a RULE OUTPUT, not a recommendation. Until the phase-B gate in memory/roadmap.md is passed,
every size is a paper size. Research, not SEBI-registered advice.
"""
import argparse
import datetime as _dt
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "valuation"))
import worksheet as ws  # noqa: E402

CARD_VERSION = "1.1 (2026-11-23; market-specific PEAD gate, base-rate CIs/size band, v1.3 worksheet lines)"
PEAD_AVOID_QUINTILES = (1, 2)          # L19: bottom two SUE quintiles
# v1.1 (L34): the avoid gate is calibrated for India only (bottom two quintiles: L17, L19, L31, confirmed 3 times).
# US: no PEAD back-test on file and the SUE proxy cut-points are uncalibrated -> quintile shown, never blocks.
PEAD_GATE_MARKETS = {"india": PEAD_AVOID_QUINTILES, "us": None}
PEAD_AVOID_CAL_DAYS = 92               # ~63 trading days
OPEN_FLAG_LIMIT = 3                    # insight:flag-override-template: 3+ open soft flags -> need variant view
CREDIBILITY_GAP = -0.15                # sector-adjusted credibility this far below peers counts as an open flag
EDGE_CLAIM_RATIO = 2.0                 # model P(>=3x) > 2x base rate (or P(<=0.5x) < 0.5x) = an edge claim
TIER_CAPS = {"core": 0.05, "satellite": 0.04, "speculative": 0.02}  # strategy:position-sizing, strategy:thorp-kelly
# 5-point Gauss-Hermite (probabilists') nodes/weights: integrates a lognormal scenario for the Kelly sum
GH = [(0.0, 0.533333), (1.355626, 0.222076), (-1.355626, 0.222076), (2.856970, 0.011257), (-2.856970, 0.011257)]

TEMPLATE = {
    "worksheet": "../valuation/examples/TICKER.json",
    "decision_date": "2026-11-21", "practice": True, "analyst": "Claude",
    "deep_dive": "research_notes/Deep dives/TICKER_practice.md",
    "thesis": "One sentence: what the business will do that matters, by when.",
    "variant_view": None,
    "stage2": {"source": "where the checks came from",
               "hard": [{"rule": "H1a fake-cash signal", "status": "pass|fail|unknown", "evidence": ""}],
               "graded": [{"rule": "G1 pledge > 25%", "status": "fired|clear|unknown", "evidence": ""}]},
    "stage3": {"pead": {"applicable": True, "quintile": None, "event_date": None, "note": ""},
               "credibility": {"score": None, "peer_median": None, "n": None, "category": "", "note": ""},
               "detectors": [{"name": "", "date": "", "detail": "", "severity": "low|med|high"}]},
    "stage4": {"soft_flags": [{"flag": "", "status": "open|cleared|confirmed|adjusted|watch",
                               "changes_mind": "", "review": ""}],
               "override_log": [{"date": "", "flag": "", "decision": "", "why": ""}]},
    "base_rate_class": "india_survivors_2020_25_mcap_ge400",
    "sizing": {"tier": "satellite", "kelly_fraction": 0.25, "max_pct_at_cost": None,
               "portfolio_value": 1.0, "adv_value": None, "adv_pct": 0.10, "days_to_exit": 5},
    "kill_criteria": [{"if": "", "measure": "", "by": "YYYY-MM-DD"}],
    "pre_mortem": [""],
    "review_date": None,
}


# ----------------------------------------------------------------------------- helpers

def _load_json(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.lstrip().startswith(("#", "//"))]
    return json.loads("".join(lines))


def _date(s):
    return _dt.date.fromisoformat(str(s)[:10])


def _add_years(d, n):
    try:
        return d.replace(year=d.year + n)
    except ValueError:  # 29-Feb
        return d.replace(year=d.year + n, day=28)


pct = ws.pct
num = ws.num
mult = ws.mult


def _table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        out.append("| " + " | ".join("" if c is None else str(c) for c in r) + " |")
    return "\n".join(out)


def _kelly(outcomes, hurdle):
    """Growth-optimal fraction of capital for a 5-yr bet vs the hurdle (index) alternative.
    outcomes: list of (prob, multiple). Maximise sum p*ln(1 + f*(M/H - 1)) for f in [0, 1]."""
    best_f, best_g = 0.0, 0.0
    for i in range(1, 1001):
        f = i / 1000.0
        g = 0.0
        ok = True
        for p, m in outcomes:
            x = 1 + f * (m / hurdle - 1)
            if x <= 0:
                ok = False
                break
            g += p * math.log(x)
        if ok and g > best_g:
            best_f, best_g = f, g
    return best_f, best_g


def _outcomes(sc, sigma):
    out = []
    for r in sc["scenarios"]:
        if not r.get("mult5"):
            return None
        for z, w in GH:
            out.append((r["prob"] * w, r["mult5"] * math.exp(sigma * z)))
    bl = sc["blowup"]
    if bl["prob"]:
        out.append((bl["prob"], bl["multiple"]))
    return out


def _pe_stage5_lines(lines, wd, wres):
    """Stage-5 bullet lines for the default (P/E, value-driver DCF) worksheet."""
    rv, sc, tw, tp = wres["reverse"], wres["scenarios"], wres["twin"], wres["temperature"]
    bc = wd["base_case"]
    lines.append("- **Reverse DCF** (CoE %s, TG %s, ROIIC %s): revenue CAGR %s for %d years at a %s→%s NOPAT margin; "
                 "or year-1 growth %s fading to %s. Base case IRR at today's price: %s."
                 % (pct(wd["coe"]), pct(wd["terminal_growth"]), pct(wd["roiic"], 0),
                    pct(rv["g_base_margin"]), wd["years"], pct(wd["nopat_margin"]), pct(bc["margin_end"]),
                    pct(rv["g_fade_start"]), pct(wd["terminal_growth"]), pct(rv["implied_coe_base"])))
    if rv.get("path") and rv["path"]["max_reinv_rate"] > 1:
        lines.append("- Feasibility: the implied path needs reinvestment above 100%% of NOPAT (peak %s) at ROIIC %s."
                     % (pct(rv["path"]["max_reinv_rate"], 0), pct(wd["roiic"], 0)))
    if sc.get("pw_value") is not None:
        lines.append("- **Scenario DCF:** probability-weighted value %s (%s vs price); bear %s (%s)."
                     % (num(sc["pw_value"], 1), pct(sc["pw_vs_price"], 0), num(sc["bear_value"], 1),
                        pct(sc["downside_bear"], 0)))
    if tw:
        row3 = [r for r in tw["table"] if r["target"] == 3]
        if row3:
            cells = "; ".join("exit P/E %s → EPS CAGR %s" % (num(c["exit_pe"]), pct(c["eps_cagr"], 0))
                              for c in row3[0]["cells"])
            lines.append("- **Twin engine, 3x in 5 yrs** from P/E %s: %s. Track record: %s %s."
                         % (num(tw["pe0"]), cells, pct(tw.get("hist_eps_cagr")), tw.get("hist_eps_note", "")))
    for r in tp["rows"][:1]:
        lines.append("- **Temperature:** P/E %s; own history: %s; sector: %s%s."
                     % (num(r["pe"]), r.get("own_band"),
                        r.get("sector_band", "no peers given"),
                        (" (%s of sector median)" % mult(r["vs_sector"])) if r.get("vs_sector") else ""))
    if tp.get("market"):
        lines.append("- **Market:** %s P/E %s: %s." % (tp["market"]["index"], num(tp["market"]["pe"]),
                                                       tp["market"]["note"]))


def _v13_lines(lines, wd, wres):
    """v1.1 card: worksheet v1.3 outputs (cash tax, reinvestment realism, exit-multiple bet)."""
    if wd.get("cash_tax_rate") is not None:
        lines.append("- **Cash tax:** %s → %s (book %s); FCF includes the deferral, EPS does not."
                     % (pct(wd["cash_tax_rate"]), pct(wd["cash_tax_rate_end"]), pct(wd["tax_rate"])))
    rz = wres.get("realism")
    if rz:
        lines.append("- **Reinvestment realism:** last-5y incremental ROIC %s; price-implied ROIIC on the base path %s; %s."
                     % (pct(rz["history"]), pct(rz["rows"][-1]["roiic"]) if rz["rows"][-1]["roiic"] is not None
                        else "none up to 300% (on this growth/margin path no ROIIC reproduces the price)",
                        ("**flag** (>5 pts): " + "; ".join(rz["flagged"])) if rz["flagged"] else "no flag"))
    eb = wres["scenarios"].get("exit_bet")
    if eb:
        lines.append("- **Exit-multiple bet (L21):** exit P/E used %s vs DCF-consistent %s vs own median %s. EV of the "
                     "5-yr multiple at the used exits %s, at DCF exits %s, at the own median %s (hurdle %s)."
                     % ("/".join(num(x["exit_pe"]) for x in eb["rows"]), "/".join(num(x["dcf_pe5"]) for x in eb["rows"]),
                        num(eb["own_median"]) if eb["own_median"] else "n/a (n=%d)" % eb["n_hist"],
                        mult(eb["ev_stated"]), mult(eb["ev_dcf"]), mult(eb["ev_own"]), mult(eb["hurdle"])))


def _bank_stage5_lines(wd, wres):
    """Stage-5 bullet lines for the bank-mode (P/B-ROE, residual income) worksheet (v1.1)."""
    rv, sc, tw, tp, sn = wres["reverse"], wres["scenarios"], wres["twin"], wres["temperature"], wres["snapshot"]
    bc = wd["base_case"]
    out = ["- **Reverse P/B** (CoE %s, g %s): P/B %s fully diluted (%s undiluted) needs ROE **%s forever**; "
           "today's ROE on diluted book %s means the market is using a CoE of **%s**. Justified P/B on the base "
           "case's long-run ROE %s: %s. Base-case IRR at today's price: %s."
           % (pct(wd["coe"]), pct(wd["terminal_growth"]), mult(sn["pb"]), mult(sn["pb_undiluted"]),
              pct(rv["roe_implied_gordon"]), pct(rv.get("roe_now")), pct(rv.get("coe_implied_at_current_roe")),
              pct(bc["roe_end"]), mult(rv["justified_pb_base"]), pct(rv["irr_base"]))]
    if sc.get("pw_value") is not None:
        out.append("- **Residual-income scenarios:** probability-weighted value %s (%s vs price); bear %s (%s). "
                   "Exit P/B used vs RIM-consistent P/B at year 5: %s."
                   % (num(sc["pw_value"], 1), pct(sc["pw_vs_price"], 0), num(sc["bear_value"], 1),
                      pct(sc["downside_bear"], 0), "; ".join("%s %s vs %s" % (x["name"], mult(x["exit_pb"]), mult(x["rim_pb5"]))
                                                            for x in sc["scenarios"])))
    row3 = [r for r in (tw or {}).get("table", []) if r["target"] == 3]
    if row3:
        out.append("- **Twin engine on book, 3x in 5 yrs** from P/B %s: %s."
                   % (mult(tw["pb0"]), "; ".join("exit P/B %s → BVPS CAGR %s" % (mult(c["exit_pb"]), pct(c["bv_cagr"], 0))
                                                 for c in row3[0]["cells"])))
    for r in tp["rows"][:1]:
        out.append("- **Temperature:** P/B %s; own history: %s (%s of own median %s); sector: %s%s. P/E %s."
                   % (mult(r["pb"]), r.get("own_band"), mult(r.get("vs_own")), mult(tp.get("own_median")),
                      r.get("sector_band", "no peers given"),
                      (" (%s of peer median)" % mult(r["vs_sector"])) if r.get("vs_sector") else "", num(tp.get("pe"))))
    st = wres.get("stress")
    if st:
        r2 = [r for r in st["rows"] if abs(r["loss_rate"] - 0.02) < 1e-9]
        out.append("- **Book stress:** leverage %s; an extra 2%% loan loss (post-tax) is %s of book."
                   % (mult(st["leverage"]), pct(r2[0]["pct_of_book"], 0) if r2 else "n/a"))
    if tp.get("market"):
        out.append("- **Market:** %s P/E %s: %s." % (tp["market"]["index"], num(tp["market"]["pe"]), tp["market"]["note"]))
    return out


# ----------------------------------------------------------------------------- assemble

def build(card, card_path):
    base_dir = os.path.dirname(os.path.abspath(card_path))
    wpath = card["worksheet"]
    if not os.path.isabs(wpath):
        wpath = os.path.join(base_dir, wpath)
    wd = ws.load_input(wpath)
    wres = ws.run(wd)
    rates = _load_json(os.path.join(HERE, "base_rates.json"))
    dd = _date(card["decision_date"])
    practice = bool(card.get("practice") or wd.get("practice"))
    gates = []        # (gate, result, blocks_sizing)
    F = {}

    # --- header
    F["company"] = wd.get("company")
    F["ticker"] = wd.get("ticker")
    F["decision_date"] = dd.isoformat()
    F["card_version"] = CARD_VERSION
    F["worksheet_version"] = wres["version"]
    F["deep_dive"] = card.get("deep_dive") or "none"
    F["price_line"] = "%s %s on %s (%s)" % (wd.get("currency", ""), num(wd["price"], 2), wd.get("as_of"),
                                           "see worksheet notes for the source")
    F["banner"] = ("> **TEST MATERIAL. No verdict, no buy/sell/watchlist call (lesson L9).** This card was produced "
                   "to test the template. Every scenario input is an illustrative [EST]; the rule output below is "
                   "what the written rules compute from those inputs, nothing more." if practice else
                   "> Phase A: every size on this card is a **paper size** until the phase-B gate in "
                   "`memory/roadmap.md` is passed.")
    F["thesis"] = card.get("thesis") or "_Not written. A card without a one-line thesis is incomplete._"
    vv = card.get("variant_view")
    F["variant_view"] = vv if vv else "_None written._"

    # --- stage 5 summary
    rv, sc, tw, tp = wres["reverse"], wres["scenarios"], wres["twin"], wres["temperature"]
    bc = wd["base_case"]
    lines = []
    if wres.get("mode") == "bank":   # v1.1 (FEDERALBNK dry run): P/B-ROE / residual-income worksheet
        lines += _bank_stage5_lines(wd, wres)
    else:
        _pe_stage5_lines(lines, wd, wres)
        _v13_lines(lines, wd, wres)
    lines.append("- Full worksheet: `%s` (re-run `python3 tools/valuation/worksheet.py <input>`)."
                 % os.path.relpath(wpath, os.path.join(HERE, "..", "..")))
    F["price_implies"] = "\n".join(lines)

    # --- stage 2
    s2 = card.get("stage2") or {}
    hard = s2.get("hard") or []
    graded = s2.get("graded") or []
    rows = [[h["rule"], h.get("status", "unknown").upper(), h.get("evidence", "")] for h in hard]
    txt = ["Source: %s" % s2.get("source", "not stated"), "", _table(["Hard rule", "Status", "Evidence"], rows)
           if rows else "_No hard-filter results supplied._"]
    if graded:
        txt += ["", _table(["Graded flag", "Status", "Evidence"],
                           [[g["rule"], g.get("status", "unknown").upper(), g.get("evidence", "")] for g in graded])]
    F["stage2"] = "\n".join(txt)
    fails = [h for h in hard if h.get("status") == "fail"]
    unknown = [h for h in hard if h.get("status", "unknown") == "unknown"]
    if not hard:
        gates.append(("Stage 2 hard filters", "NOT RUN → size 0 until run", True))
    elif fails:
        gates.append(("Stage 2 hard filters", "DISQUALIFIED by %s (no override possible)"
                      % ", ".join(h["rule"] for h in fails), True))
    elif unknown:
        gates.append(("Stage 2 hard filters", "INCOMPLETE: %d of %d rules unchecked (%s) → size 0 until checked"
                      % (len(unknown), len(hard), ", ".join(h["rule"] for h in unknown)), True))
    else:
        gates.append(("Stage 2 hard filters", "passed (%d rules)" % len(hard), False))
    graded_fired = [g for g in graded if g.get("status") == "fired"]

    # --- stage 3
    s3 = card.get("stage3") or {}
    t3 = []
    extra_open = []
    pe = s3.get("pead") or {}
    if pe.get("applicable") is False:
        t3.append("- **Earnings-surprise (PEAD) avoid flag:** not applicable. %s" % pe.get("note", ""))
        gates.append(("Stage 3 PEAD avoid flag", "n/a", False))
    elif pe.get("quintile") is None:
        t3.append("- **Earnings-surprise (PEAD) avoid flag:** no live quintile. %s" % pe.get("note", ""))
        gates.append(("Stage 3 PEAD avoid flag", "unknown (no live quintile): does not block, noted", False))
    else:
        q = int(pe["quintile"])
        ev = _date(pe["event_date"]) if pe.get("event_date") else None
        until = ev + _dt.timedelta(days=PEAD_AVOID_CAL_DAYS) if ev else None
        gate_q = PEAD_GATE_MARKETS.get(wd["market"], PEAD_AVOID_QUINTILES)
        if gate_q is None:
            would = q in PEAD_AVOID_QUINTILES and until is not None and dd <= until
            t3.append("- **Earnings-surprise (PEAD):** SUE quintile %d (event %s). **No PEAD gate for %s stocks:** the "
                      "avoid rule is calibrated on Indian data only (L19/L31); US cut-points are uncalibrated. %s%s"
                      % (q, pe.get("event_date"), wd["market"].upper(),
                         "Shown for information (it would sit in an India-style avoid window). " if would else "",
                         pe.get("note", "")))
            gates.append(("Stage 3 PEAD avoid flag", "not gated (%s: uncalibrated); quintile %d noted"
                          % (wd["market"].upper(), q), False))
        else:
            active = q in gate_q and until is not None and dd <= until
            t3.append("- **Earnings-surprise (PEAD):** SUE quintile %d (event %s). Avoid flag %s%s. Rule L19: bottom two "
                    "quintiles = avoid/exit for ≥63 trading days." % (q, pe.get("event_date"),
                                                                     "**ACTIVE**" if active else "not active",
                                                                     (" until %s" % until) if active else ""))
            gates.append(("Stage 3 PEAD avoid flag", ("ACTIVE until %s → WAIT" % until) if active else "clear", active))
    cr = s3.get("credibility") or {}
    if cr.get("score") is None:
        t3.append("- **Promise credibility:** not scored. %s" % cr.get("note", ""))
    elif cr.get("peer_median") is None:
        t3.append("- **Promise credibility:** %s absolute (%s, n=%s). **No peer base rate → not usable as a signal "
                  "(L18).** %s" % (pct(cr["score"], 0), cr.get("category", ""), cr.get("n"), cr.get("note", "")))
    else:
        adj = cr["score"] - cr["peer_median"]
        t3.append("- **Promise credibility:** %s vs peer median %s → sector-adjusted %+.0f pts (%s, n=%s). %s"
                  % (pct(cr["score"], 0), pct(cr["peer_median"], 0), 100 * adj, cr.get("category", ""),
                     cr.get("n"), cr.get("note", "")))
        if adj < CREDIBILITY_GAP:
            extra_open.append("credibility %+.0f pts vs peers" % (100 * adj))
    dets = s3.get("detectors") or []
    if dets:
        t3.append("")
        t3.append(_table(["Detector alert", "Date", "Detail", "Severity"],
                         [[x.get("name"), x.get("date"), x.get("detail"), x.get("severity", "low")] for x in dets]))
        extra_open += ["detector: %s" % x.get("name") for x in dets if x.get("severity") == "high"]
    else:
        t3.append("- **Detector alerts:** none supplied.")
    F["stage3"] = "\n".join(t3)

    # --- stage 4
    s4 = card.get("stage4") or {}
    flags = s4.get("soft_flags") or []
    opens = [f for f in flags if f.get("status") == "open"]
    watch = [f for f in flags if f.get("status") == "watch"]
    t4 = []
    if flags:
        t4.append(_table(["Soft flag", "Status", "What changes my mind", "Review"],
                         [[f["flag"], f.get("status", "open").upper(), f.get("changes_mind", ""), f.get("review", "")]
                          for f in flags]))
    n_open = len(opens) + len(extra_open) + len(graded_fired)
    t4.append("")
    t4.append("**Open soft flags: %d** (%d from the deep dive%s%s), plus %d dated watch item(s). Rule: ≥%d open "
              "soft flags means no position without a written variant view."
              % (n_open, len(opens),
                 (", %d graded stage-2 flag(s)" % len(graded_fired)) if graded_fired else "",
                 (", %d from stage 3: %s" % (len(extra_open), "; ".join(extra_open))) if extra_open else "",
                 len(watch), OPEN_FLAG_LIMIT))
    log = s4.get("override_log") or []
    if log:
        t4.append("")
        t4.append("Override log (a management explanation alone never clears a flag; L10, L12):")
        t4.append("")
        t4.append(_table(["Date", "Flag", "Decision", "Why (external evidence)"],
                         [[x.get("date"), x.get("flag"), x.get("decision"), x.get("why")] for x in log]))
    F["stage4"] = "\n".join(t4)
    if n_open >= OPEN_FLAG_LIMIT and not vv:
        gates.append(("Stage 4 soft flags", "%d open, no variant view → NO POSITION" % n_open, True))
    else:
        gates.append(("Stage 4 soft flags", "%d open%s" % (n_open, ", variant view written" if vv else ""), False))

    # --- probabilities vs base rates
    cls_name = card.get("base_rate_class")
    cls = rates["classes"].get(cls_name) if cls_name else None
    cls_note = ""
    if cls_name and cls is None and (cls_name + "_deprecated") in rates["classes"]:
        cls = rates["classes"][cls_name + "_deprecated"]
        cls_note = " **Deprecated class** (%s)" % cls.get("deprecated", "")
    if cls_name and cls is None:
        raise ValueError("unknown base_rate_class %r (see tools/decision/base_rates.json)" % cls_name)

    def br(k):
        return cls.get(k) if cls else None
    probs = [("P(≥3x in 5 yrs)", sc.get("p_ge_3x"), br("p_ge_3x")),
             ("P(≤0.5x in 5 yrs)", sc.get("p_le_half"), br("p_le_half")),
             ("P(blow-up)", sc.get("p_blowup"), br("p_blowup"))]
    prow = []
    edge_claims = []
    for label, p, b in probs:
        ratio = (p / b) if (p is not None and b) else None
        bcell = pct(b, 1) if b is not None else "n/a"
        key = {"P(≥3x in 5 yrs)": "p_ge_3x", "P(≤0.5x in 5 yrs)": "p_le_half", "P(blow-up)": "p_blowup"}[label]
        if b is not None and cls and (cls.get("ci95") or {}).get(key):
            lo_, hi_ = cls["ci95"][key]
            bcell += " [95%% CI %s–%s]" % (pct(lo_, 1), pct(hi_, 1))
        prow.append([label, pct(p, 0), bcell, mult(ratio) if ratio else "n/a"])
        if ratio is not None and (ratio > EDGE_CLAIM_RATIO or ratio < 1 / EDGE_CLAIM_RATIO):
            edge_claims.append("%s is %.2fx the base rate" % (label, ratio))
    ptxt = [_table(["Event", "Model (worksheet)", "Base rate", "Model ÷ base"], prow), ""]
    if cls:
        ptxt.append("Base-rate class: **%s** (n=%s, %s-yr horizon). Source: %s. Caveats: %s%s"
                    % (cls["label"], cls.get("n"), cls.get("horizon_years"), cls["source"], cls["caveats"], cls_note))
        band = cls.get("size_band")
        if band:
            size = wres["snapshot"].get("mcap")
            if size is not None and wd.get("units") == band.get("units") and not (band["min"] <= size <= band["max"]):
                ptxt.append("")
                ptxt.append("> **Size outside the class:** market cap %s %s vs the class band %s–%s %s (%s). No class "
                            "on file fits better; read the base rates as the nearest class, not as this stock's."
                            % (num(size), wd.get("units"), num(band["min"]), num(band["max"]), band["units"],
                               band["measure"]))
    else:
        ptxt.append("Base-rate class: none chosen.")
    ptxt.append("Blow-up = %s" % rates["blowup_definition"])
    ptxt.append("")
    ptxt.append("Model probabilities come from the scenario multiples with lognormal dispersion σ=%.2f (worksheet "
                "block b). They are only as good as the scenario inputs." % wd["dispersion"])
    if edge_claims:
        ptxt.append("")
        ptxt.append("> **Departure from the outside view:** %s. A model this far from the base rate (either way) is a "
                    "claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias "
                    "of the class (see caveats), or pull the probabilities toward the base rate."
                    % "; ".join(edge_claims))
        if not vv:
            gates.append(("Outside-view check", "model departs from base rate with no variant view → shrink", False))
    F["probabilities"] = "\n".join(ptxt)

    # --- expected value
    hurdle = sc.get("hurdle_mult5")
    evtxt = []
    if sc.get("ev_mult5") is not None:
        evtxt.append(_table(["EV of 5-yr multiple", "EV CAGR", "Median multiple", "Hurdle (index %s/yr)" %
                             pct(wd["hurdle_cagr"], 0), "Prob-weighted DCF value", "Bear downside"],
                            [[mult(sc["ev_mult5"]), pct(sc["ev_cagr5"]), mult(sc["median_mult5"]), mult(hurdle),
                              "%s (%s)" % (num(sc["pw_value"], 1), pct(sc["pw_vs_price"], 0)),
                              pct(sc["downside_bear"], 0)]]))
        evtxt.append("")
        evtxt.append("Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the "
                     "market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows "
                     "justify). When they disagree, the card says so; the gap itself is information.")
        below = sc["ev_mult5"] < hurdle
        gates.append(("Expected value vs hurdle", "EV %s vs hurdle %s → %s" % (
            mult(sc["ev_mult5"]), mult(hurdle), "below hurdle → size 0" if below else "above hurdle"), below))
    else:
        evtxt.append("_No scenario multiples: give exit_pe for every scenario in the worksheet input._")
        gates.append(("Expected value vs hurdle", "not computable → size 0", True))
    F["expected_value"] = "\n".join(evtxt)

    # --- sizing
    sz = card.get("sizing") or {}
    tier = sz.get("tier", "satellite")
    cap = sz.get("max_pct_at_cost") or TIER_CAPS.get(tier, 0.04)
    kf = sz.get("kelly_fraction", 0.25)
    outs = _outcomes(sc, wd["dispersion"]) if sc.get("scenarios") else None
    f_star = None
    if outs and hurdle:
        f_star, _ = _kelly(outs, hurdle)
    kelly_size = f_star * kf if f_star is not None else None
    liq = None
    if sz.get("adv_value") and sz.get("portfolio_value"):
        liq = sz.get("adv_pct", 0.10) * sz["adv_value"] * sz.get("days_to_exit", 5) / sz["portfolio_value"]
    cands = [x for x in (kelly_size, cap, liq) if x is not None]
    rule_size = min(cands) if cands and kelly_size is not None else 0.0
    blocked = [g for g in gates if g[2]]
    final = 0.0 if blocked else rule_size
    srows = [
        ["Full Kelly f* (5-yr bet vs index hurdle, scenario outcomes)", pct(f_star, 1)],
        ["× Kelly fraction %.2f" % kf, pct(kelly_size, 1)],
        ["Cap: max %% at cost (%s tier)" % tier, pct(cap, 1)],
        ["Cap: liquidity (%s of ADV × %s days ÷ portfolio)" % (pct(sz.get("adv_pct", 0.10), 0),
                                                             sz.get("days_to_exit", 5)),
         pct(liq, 1) if liq is not None else "n/a (ADV not supplied)"],
        ["Rule size before gates = min(fractional Kelly, caps)", pct(rule_size, 1)],
        ["**Size after gates** (%s)" % ("blocked by: " + "; ".join(g[0] for g in blocked) if blocked else "no gate blocks"),
         "**%s**" % pct(final, 1)],
    ]
    stxt = [_table(["Sizing step", "Value"], srows), ""]
    stxt.append("Written rule: size = min(Kelly fraction × f*, tier cap at cost, liquidity cap); any blocking gate "
                "→ 0. f* maximises E[ln(1 + f·(M/H − 1))] over the scenario outcomes (each scenario spread by "
                "5-point Gauss-Hermite on the same σ, blow-up as a point mass), with H = the index hurdle "
                "multiple. Fractional Kelly because the inputs are opinions (strategy:thorp-kelly); tier caps from "
                "strategy:position-sizing (max 5% at cost, satellites 3.5–4%, speculative 1–3%).")
    if practice:
        stxt.append("")
        stxt.append("_Practice mode: this is the mechanical output of the rule on illustrative inputs, NOT a "
                    "position size for anyone._")
    F["sizing"] = "\n".join(stxt)

    # --- kill criteria, pre-mortem, review
    kc = card.get("kill_criteria") or []
    undated = [k for k in kc if not k.get("by")]
    F["kill_criteria"] = _table(["#", "Kill if…", "Measured by", "Check by"],
                                [[i + 1, k.get("if"), k.get("measure"), k.get("by") or "**UNDATED (fix)**"]
                                 for i, k in enumerate(kc)]) if kc else "_None written: a card without kill criteria is incomplete._"
    if not kc or undated:
        gates.append(("Kill criteria", "missing or undated → card incomplete", True))
    pm = card.get("pre_mortem") or []
    F["pre_mortem"] = "\n".join("%d. %s" % (i + 1, x) for i, x in enumerate(pm)) if pm else "_Not written._"
    F["premortem_year"] = str(dd.year + 5)
    rd = card.get("review_date")
    if not rd:
        dates = sorted(k["by"] for k in kc if k.get("by"))
        rd = dates[0] if dates else (dd + _dt.timedelta(days=91)).isoformat()
    F["review_date"] = rd

    # --- gate log & headline
    F["gate_log"] = _table(["Gate", "Result", "Blocks size?"], [[g[0], g[1], "yes" if g[2] else "no"] for g in gates])
    if blocked:
        head = "size 0: blocked by %s" % "; ".join("%s (%s)" % (g[0], g[1]) for g in blocked)
    else:
        head = "rule size %s of portfolio at cost" % pct(final, 1)
    F["gate_headline"] = ("**Practice, no verdict.** Mechanical rule output: " + head) if practice else head

    # --- paper calls
    tick = wd.get("ticker")
    entry = _date(wd.get("as_of") or card["decision_date"])
    resolve = _add_years(entry, 5)
    slug_date = dd.isoformat()
    calls = []
    specs = [
        ("ge3x", "≥3.0x", sc.get("p_ge_3x"), br("p_ge_3x"),
         "YES if the total-return multiple (adjusted close incl. dividends reinvested, splits/bonuses adjusted) from "
         "%s (entry %s %s) to the last close on or before %s is ≥ 3.0." % (entry, wd.get("currency"), num(wd["price"], 2), resolve)),
        ("le0p5x", "≤0.5x", sc.get("p_le_half"), br("p_le_half"),
         "YES if the total-return multiple from %s (entry %s %s) to the last close on or before %s is ≤ 0.5, or the "
         "stock is delisted/suspended below that level." % (entry, wd.get("currency"), num(wd["price"], 2), resolve)),
        ("blowup", "blow-up", sc.get("p_blowup"), br("p_blowup"),
         "YES if between %s and %s: %s" % (entry, resolve, rates["blowup_definition"])),
    ]
    ids = []
    tags_mkt = "india" if wd["market"] == "india" else "us"
    for key, label, p, b, rule in specs:
        if p is None:
            continue
        cid = "thesis:paper-call:%s:card-%s-5y-%s" % (tick, slug_date, key)
        ids.append(cid)
        tags = ["paper-call", "method-test", "decision-card", "stage-6", "valuation", tags_mkt]
        if practice:
            tags.append("practice-example")
        calls.append({
            "type": "thesis", "id": cid,
            "title": "Paper call: %s 5-year outcome %s from %s (decision card v1)" % (wd.get("company"), label, entry),
            "body": ("Forward test of the decision-card method (NOT a recommendation; not buy/sell%s). Probability %.2f "
                     "(base rate %s, class %s) that: %s Model: worksheet scenarios %s with σ=%.2f; reverse DCF base-case "
                     "IRR %s; card rule output: %s. Score with Brier vs the base rate."
                     % ("; PRACTICE EXAMPLE built from test inputs" if practice else "", p,
                        "%.3f" % b if b is not None else "n/a", cls_name, rule,
                        ", ".join("%s %s→%s" % (r["name"], pct(r["prob"], 0), mult(r["mult5"])) for r in sc["scenarios"]),
                        wd["dispersion"], pct(rv.get("implied_coe_base", rv.get("irr_base"))), head)),
            "tickers": [tick], "tags": tags, "date": slug_date, "status": "open",
            "data": {"probability": round(p, 4), "base_rate_probability": b,
                     "base_rate_reasoning": (cls["label"] + ". " + cls["caveats"]) if cls else "no class chosen",
                     "method": "decision-card-v1", "made_on": slug_date, "resolve_by": resolve.isoformat(),
                     "entry_date": entry.isoformat(), "entry_price": wd["price"], "currency": wd.get("currency"),
                     "resolution_rule": rule,
                     "resolution_source": "NSE/BSE or exchange adjusted closes (Yahoo adj close / Kite), corporate actions",
                     "practice": practice, "outcome": None, "brier": None},
            "sources": wd.get("sources") or [],
            "confidence": "unverified" if practice else "single-source",
        })
    F["paper_call_ids"] = ", ".join("`%s`" % i for i in ids) if ids else "none (no scenario probabilities)"
    decision = {
        "type": "decision", "id": "decision:card:%s:%s" % (tick, slug_date),
        "title": "Decision card %s %s (%s)" % (tick, slug_date, "practice, no verdict" if practice else "paper"),
        "body": ("Decision card v1 for %s. Rule output: %s. Thesis: %s Variant view: %s Open soft flags: %d. "
                 "P(≥3x) %s vs base %s; P(≤0.5x) %s vs base %s; EV 5-yr multiple %s vs hurdle %s. Review %s."
                 % (wd.get("company"), head, F["thesis"], vv or "none", n_open, pct(sc.get("p_ge_3x"), 0),
                    pct(br("p_ge_3x"), 0), pct(sc.get("p_le_half"), 0), pct(br("p_le_half"), 1),
                    mult(sc.get("ev_mult5")), mult(hurdle), rd)),
        "tickers": [tick], "tags": ["decision-card", "stage-6", tags_mkt] + (["practice-example"] if practice else []),
        "date": slug_date,
        "data": {"gates": [{"gate": g[0], "result": g[1], "blocks": g[2]} for g in gates], "size_after_gates": final,
                 "rule_size": rule_size, "kelly_f_star": f_star, "open_soft_flags": n_open, "review_date": rd,
                 "kill_criteria": kc, "override_log": log, "paper_calls": ids, "practice": practice},
        "sources": wd.get("sources") or [],
        "confidence": "unverified" if practice else "single-source",
        "links": [{"to": i, "rel": "about"} for i in ids],
    }
    return F, calls + [decision], wres


def fill(template_text, fields):
    def rep(m):
        k = m.group(1)
        if k not in fields:
            raise KeyError("template placeholder {{%s}} has no value" % k)
        return str(fields[k])
    return re.sub(r"\{\{(\w+)\}\}", rep, template_text)


def main(argv=None):
    ap = argparse.ArgumentParser(description="FEIN decision card (stage 6) + paper calls (stage 7)")
    ap.add_argument("card", nargs="?", help="card input JSON")
    ap.add_argument("-o", "--out", help="write the Markdown card here (default stdout)")
    ap.add_argument("--calls", help="write paper-call + decision records (memdb seed format) here")
    ap.add_argument("--with-worksheet", action="store_true", help="append the full worksheet section to the card")
    ap.add_argument("--template", action="store_true", help="print a blank card input")
    a = ap.parse_args(argv)
    if a.template:
        print(json.dumps(TEMPLATE, indent=2))
        return 0
    if not a.card:
        ap.error("card input required (or --template)")
    card = _load_json(a.card)
    fields, records, wres = build(card, a.card)
    with open(os.path.join(HERE, "decision_card.md"), encoding="utf-8") as f:
        md = fill(f.read(), fields)
    if a.with_worksheet:
        md += "\n\n## Appendix: valuation worksheet\n\n" + ws.render(wres, heading_level=3)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(md + "\n")
    else:
        print(md)
    if a.calls:
        with open(a.calls, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
