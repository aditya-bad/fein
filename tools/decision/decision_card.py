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

CARD_VERSION = "1.5 (2026-11-25; lender base-rate class auto-selected for lenders, L41; 1.4 core-asset threat, L40)"
# v1.5 (L41): a card whose firm is marked as a lender - card "is_lender": true, survival.is_financial = true, or a
# bank-mode worksheet - and whose market has a lender class uses that class instead of a non-financial class. Set
# "base_rate_class_lock": true to keep the class named on the card (the card then says so).
LENDER_CLASSES = {"india": "india_lender_1000_20000cr_5y"}
PEAD_AVOID_QUINTILES = (1, 2)          # L19: bottom two SUE quintiles
# v1.1 (L34): the avoid gate is calibrated for India only (bottom two quintiles: L17, L19, L31, confirmed 3 times).
# US: no PEAD back-test on file and the SUE proxy cut-points are uncalibrated -> quintile shown, never blocks.
PEAD_GATE_MARKETS = {"india": PEAD_AVOID_QUINTILES, "us": None}
PEAD_AVOID_CAL_DAYS = 92               # ~63 trading days
OPEN_FLAG_LIMIT = 3                    # insight:flag-override-template: 3+ open soft flags -> need variant view
CREDIBILITY_GAP = -0.15                # sector-adjusted credibility this far below peers counts as an open flag
EDGE_CLAIM_RATIO = 2.0                 # model P(>=3x) > 2x base rate (or P(<=0.5x) < 0.5x) = an edge claim
# v1.2 survival cap (L35, decision:pead-avoid-plus-redflag-survival-cap): India only. In the PEAD avoid window
# (bottom-two SUE quintile, <=63 trading days) AND (promoter pledge > 25% of promoter holding OR interest cover < 1.5x)
# -> 0 new money (hold-review if already owned) + a mandatory balance-sheet question. S5-India alone is NOT a trigger.
SURVIVAL_PLEDGE = 0.25                 # fraction of the promoter holding pledged (strictly above)
SURVIVAL_ICR = 1.5                     # interest cover, x (strictly below)
# v1.3 general survival cap (L39, survival_cap_general_india.md): India, OUTSIDE the PEAD window, the same trigger
# (pledge > 25% or, for non-financials, interest cover < 1.5x) caps the position at the starter size, no additions.
# Inside the PEAD window the v1.2 rule (0 new money) still applies. Interest cover is not applied to lenders.
SURVIVAL_MIN_SIZE = 0.01               # starter size, fraction of portfolio at cost
SURVIVAL_QUESTION = ("Balance-sheet question (mandatory): can the company service its debt and can the promoter meet a "
                     "margin call through a 12-month stress (no refinancing, a further 30% share-price fall)? Answer from "
                     "the debt schedule, maturity profile, pledge-lender terms and rating letters, not from management.")
# v1.2 tail anchoring (L36): anchored P = w*base + (1-w)*model for P(blow-up) and P(<=0.5x); w defaults to 0.5,
# can go below 0.5 only with a written evidence note, never below 0.25. The anchored tails feed the EV gate and Kelly.
# v1.4 (L40): a manual survival input `survival.core_asset_threat` = {"description", "source", "date"} (a government
# land lease / licence / concession / PPP the business depends on is expiring, contested or being withdrawn) fires the
# survival cap exactly like a red flag in both modes (PEAD window -> 0 new money; otherwise starter size, no additions).
# The pledge / interest-cover screen cannot see legal or licence risk. Tail anchoring that LOWERS a model tail (base
# rate below our documented estimate) is flagged on the card: ANCHOR_LOWERED_WARNING.
CORE_ASSET_THREAT_REASON = "core-asset licence/lease threat (L40)"
ANCHOR_LOWERED_WARNING = "anchoring lowered documented tails — check evidence note"
ANCHOR_WEIGHT_DEFAULT = 0.5
ANCHOR_WEIGHT_MIN = 0.25
ANCHOR_FALLBACK_LOSS_MULT = 0.35       # extra <=0.5x mass with no model outcome in that bucket goes here
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
    "survival": {"pledge_pct_of_promoter": None, "interest_cover": None, "already_owned": False, "as_of": "",
                 "source": "", "note": "India only; PEAD window -> 0 new money (v1.2), else starter-size cap (v1.3)",
                 "core_asset_threat": None},   # v1.4 optional: {"description": "", "source": "", "date": ""}
    "tail_anchor": {"base_weight": 0.5, "evidence": None},
    "base_rate_class": "india_nonfin_1000_20000cr_5y",
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


def core_asset_threat_reason(surv):
    """v1.4 (L40): reason text for a manual core-asset threat, or None. Accepts a dict (description, source, date)
    or a plain string; empty / None / a dict without a description means no threat."""
    t = (surv or {}).get("core_asset_threat")
    if not t:
        return None
    if isinstance(t, str):
        t = {"description": t}
    desc = (t.get("description") or "").strip()
    if not desc:
        return None
    meta = ", ".join(x for x in ((t.get("source") or "").strip(), str(t.get("date") or "").strip()) if x)
    return "%s: %s%s" % (CORE_ASSET_THREAT_REASON, desc, (" [%s]" % meta) if meta else "")


def survival_cap(market, pead_active, surv):
    """Survival cap v1.4 (L35 + L39 + L40). A manual surv['core_asset_threat'] (v1.4) triggers it like a red flag. Returns dict(status, triggered, blocks, mode, cap_size, reasons, already_owned).
    status: 'n/a' (not India), 'clear', 'TRIGGERED', 'UNCHECKED'. mode: 'block' (PEAD avoid window active: 0 new money,
    v1.2) or 'cap' (no PEAD window: size <= SURVIVAL_MIN_SIZE, no additions, v1.3). UNCHECKED (a needed input missing)
    is treated as triggered until checked, like a stage-2 unknown. Interest cover is skipped for lenders
    (surv['is_financial']). S5-India / S1 are deliberately not inputs (L35, L39: no incremental signal)."""
    surv = surv or {}
    owned = bool(surv.get("already_owned"))
    if market != "india":
        return {"status": "n/a", "triggered": False, "blocks": False, "mode": None, "cap_size": None, "reasons": [],
                "already_owned": owned}
    fin = bool(surv.get("is_financial"))
    pl, icr = surv.get("pledge_pct_of_promoter"), (None if fin else surv.get("interest_cover"))
    reasons, missing = [], []
    if pl is None:
        missing.append("promoter pledge")
    elif pl > SURVIVAL_PLEDGE:
        reasons.append("promoter pledge %s of promoter holding (> %s)" % (pct(pl, 0), pct(SURVIVAL_PLEDGE, 0)))
    if icr is None:
        if not fin: missing.append("interest cover")
    elif icr < SURVIVAL_ICR:
        reasons.append("interest cover %sx (< %sx)" % (num(icr, 2), num(SURVIVAL_ICR, 1)))
    cat = core_asset_threat_reason(surv)
    if cat:
        reasons.append(cat)
    if reasons:
        status = "TRIGGERED"
        if missing:
            reasons.append("also not checked: %s" % ", ".join(missing))
    elif missing:
        status = "UNCHECKED"
        reasons = ["not checked: %s" % ", ".join(missing)]
    else:
        status = "clear"
    trig = status in ("TRIGGERED", "UNCHECKED")
    mode = ("block" if pead_active else "cap") if trig else None
    return {"status": status, "triggered": trig, "blocks": mode == "block", "mode": mode,
            "cap_size": SURVIVAL_MIN_SIZE if mode == "cap" else None, "reasons": reasons, "already_owned": owned}


def anchor_weight(spec):
    """Weight on the base rate. Default 0.5; below 0.5 only with a written evidence note; floor 0.25; max 1.
    Returns (weight, note)."""
    spec = spec or {}
    w = spec.get("base_weight")
    ev = (spec.get("evidence") or "").strip()
    if w is None:
        return ANCHOR_WEIGHT_DEFAULT, "default"
    w = float(w)
    if w > 1:
        return 1.0, "capped at 1.0"
    if w < ANCHOR_WEIGHT_DEFAULT and not ev:
        return ANCHOR_WEIGHT_DEFAULT, "requested %.2f ignored: no written evidence note" % w
    if w < ANCHOR_WEIGHT_MIN:
        return ANCHOR_WEIGHT_MIN, "requested %.2f raised to the %.2f floor; evidence: %s" % (w, ANCHOR_WEIGHT_MIN, ev)
    return w, ("evidence: %s" % ev) if w < ANCHOR_WEIGHT_DEFAULT else "stated"


def anchor_p(p_model, p_base, w):
    """Outside-view-anchored probability = w*base + (1-w)*model. None base -> model (no anchor)."""
    if p_model is None:
        return None
    if p_base is None:
        return p_model
    return w * p_base + (1 - w) * p_model


def _outcomes_tagged(sc, sigma):
    """Like _outcomes but each item is (prob, multiple, is_blowup); the blow-up point is always present."""
    out = []
    for r in sc["scenarios"]:
        if not r.get("mult5"):
            return None
        for z, w in GH:
            out.append((r["prob"] * w, r["mult5"] * math.exp(sigma * z), False))
    bl = sc["blowup"]
    out.append((bl["prob"] or 0.0, bl["multiple"], True))
    return out


def anchor_outcomes(outs, pa, pl):
    """Reweight a tagged outcome list so that P(blow-up) = pa and P(multiple <= 0.5) = pl.
    Groups: A = blow-up point; B = other outcomes <= 0.5x; C = outcomes > 0.5x. Each group is scaled in proportion
    (shape kept). If the blow-up multiple is <= 0.5, the <=0.5x target is floored at pa (a blow-up is a <=0.5x
    outcome in the model). If B has no mass but needs some, a point at ANCHOR_FALLBACK_LOSS_MULT is added.
    Returns (outcomes as (prob, multiple), effective pl)."""
    bl_mult = [m for _, m, b in outs if b][0]
    bl_in_loss = bl_mult <= 0.5
    if bl_in_loss:
        pl = max(pl, pa)
        tgt = {"A": pa, "B": pl - pa, "C": 1 - pl}
    else:
        pl = min(pl, 1 - pa)
        tgt = {"A": pa, "B": pl, "C": 1 - pa - pl}
    grp = lambda m, b: "A" if b else ("B" if m <= 0.5 else "C")  # noqa: E731
    mass = {"A": 0.0, "B": 0.0, "C": 0.0}
    for p, m, b in outs:
        mass[grp(m, b)] += p
    res = []
    for p, m, b in outs:
        g = grp(m, b)
        if g == "A":
            res.append((tgt["A"], m))
        elif mass[g] > 0:
            res.append((p * tgt[g] / mass[g], m))
    if mass["B"] <= 0 and tgt["B"] > 0:
        res.append((tgt["B"], ANCHOR_FALLBACK_LOSS_MULT))
    if mass["C"] <= 0 and tgt["C"] > 0:   # degenerate: nothing above 0.5x in the model; keep mass at 1x
        res.append((tgt["C"], 1.0))
    return [(p, m) for p, m in res if p > 0], pl


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


def is_lender(card, wd=None, wres=None):
    """v1.5: the card marks the firm as a lender / financial (any of three inputs)."""
    return bool(card.get("is_lender") or (card.get("survival") or {}).get("is_financial")
                or (wres or {}).get("mode") == "bank"
                or str((wd or {}).get("mode", "")).lower() in ("bank", "nbfc", "lender"))


def resolve_base_rate_class(card, wd, wres, rates):
    """Return (class name, note). Lenders get the market's lender class unless the card locks its own class."""
    name = card.get("base_rate_class")
    if not is_lender(card, wd, wres):
        return name, ""
    mkt = str((wd or {}).get("market", "india")).lower()
    lc = LENDER_CLASSES.get(mkt)
    if not lc or lc not in rates["classes"]:
        return name, (" **Lender, but no %s lender class on file:** the class above is non-financial and cannot see "
                      "bank leverage; weight the tails accordingly." % mkt.upper())
    if name == lc:
        return name, ""
    if card.get("base_rate_class_lock") and name:
        return name, (" **Lender class %s available but the card locks %s** (base_rate_class_lock); say why in the "
                      "override log." % (lc, name))
    return lc, (" **Lender class auto-selected (v1.5, L41)** in place of %s." % (name or "no class"))


# ----------------------------------------------------------------------------- input validation (L42)
# Input checks only: they never change a number on a valid card. Fraction fields must be in [0, 1]; a value > 1
# almost always means a percent was typed (31 for 0.31), so the card refuses to build rather than guess.
FRACTION_FIELDS = [
    (("stage3", "credibility", "score"), "promise credibility score"),
    (("stage3", "credibility", "peer_median"), "peer-median credibility"),
    (("survival", "pledge_pct_of_promoter"), "promoter pledge (share of the promoter holding)"),
    (("tail_anchor", "base_weight"), "tail-anchor weight on the base rate"),
    (("sizing", "kelly_fraction"), "Kelly fraction"),
    (("sizing", "adv_pct"), "share of average daily value"),
    (("sizing", "max_pct_at_cost"), "max position at cost"),
]


class CardInputError(ValueError):
    pass


def _fraction_error(where, label, v):
    hint = (" It looks like a percent: write %s, not %s." % (("%g" % (v / 100.0)), ("%g" % v))) if 1 < v <= 100 else ""
    return "%s (%s) must be a fraction in [0, 1]; got %r.%s" % (where, label, v, hint)


def _check_fraction(errors, where, label, v):
    if v is None or isinstance(v, bool):
        return
    if not isinstance(v, (int, float)):
        errors.append("%s (%s) must be a number in [0, 1]; got %r." % (where, label, v))
        return
    if v < 0 or v > 1 or v != v:
        errors.append(_fraction_error(where, label, v))


def _raw_worksheet(path):
    with open(path, encoding="utf-8") as f:
        return json.loads("".join(ln for ln in f if not ln.lstrip().startswith(("#", "//"))))


def validate_card(card, raw_ws=None):
    """Raise CardInputError if any fraction field (credibility, pledge, tail weight, sizing fractions, and the
    worksheet's scenario / blow-up probabilities) is outside [0, 1]. Lists every bad field at once."""
    errors = []
    for keys, label in FRACTION_FIELDS:
        v = card
        for k in keys:
            v = v.get(k) if isinstance(v, dict) else None
        _check_fraction(errors, ".".join(keys), label, v)
    if raw_ws:
        for i, sc in enumerate(raw_ws.get("scenarios") or []):
            if isinstance(sc, dict):
                _check_fraction(errors, "worksheet scenarios[%d] (%s).prob" % (i, sc.get("name", "?")),
                                "scenario probability", sc.get("prob"))
        bc = raw_ws.get("base_case")
        if isinstance(bc, dict):
            _check_fraction(errors, "worksheet base_case.prob", "scenario probability", bc.get("prob"))
        bl = raw_ws.get("blowup")
        if isinstance(bl, dict):
            _check_fraction(errors, "worksheet blowup.prob", "blow-up probability", bl.get("prob"))
    if errors:
        raise CardInputError("card input validation failed:\n  - " + "\n  - ".join(errors))


def base_rate_warnings(cls_name, cls, rates):
    """Warnings (never blocks) for a deprecated base-rate class or one with null tails."""
    out = []
    if not cls_name or cls is None:
        return out
    if cls.get("deprecated") or (cls_name + "_deprecated") in rates["classes"] or cls_name.endswith("_deprecated"):
        out.append("base-rate class %r is DEPRECATED (%s). Old cards re-run unchanged; new cards should name a "
                   "current class." % (cls_name, cls.get("deprecated") or "see base_rates.json"))
    nulls = [k for k in ("p_ge_3x", "p_le_half", "p_blowup") if cls.get(k) is None]
    if nulls:
        out.append("base-rate class %r has null %s: those probabilities are not compared with a base rate%s."
                   % (cls_name, ", ".join(nulls), " and the raw model left tail is used unanchored"
                      if any(k != "p_ge_3x" for k in nulls) else ""))
    return out


# ----------------------------------------------------------------------------- assemble

def build(card, card_path):
    base_dir = os.path.dirname(os.path.abspath(card_path))
    wpath = card["worksheet"]
    if not os.path.isabs(wpath):
        wpath = os.path.join(base_dir, wpath)
    validate_card(card, _raw_worksheet(wpath))
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
    pead_active = False
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
            pead_active = active
            t3.append("- **Earnings-surprise (PEAD):** SUE quintile %d (event %s). Avoid flag %s%s. Rule L19: bottom two "
                    "quintiles = avoid/exit for ≥63 trading days." % (q, pe.get("event_date"),
                                                                     "**ACTIVE**" if active else "not active",
                                                                     (" until %s" % until) if active else ""))
            gates.append(("Stage 3 PEAD avoid flag", ("ACTIVE until %s → WAIT" % until) if active else "clear", active))
    # survival cap (India): pledge > 25% or interest cover < 1.5x. PEAD avoid window -> 0 new money (v1.2);
    # otherwise -> starter size, no additions (v1.3, L39)
    sv_in = card.get("survival") or s3.get("survival") or {}
    sv = survival_cap(wd["market"], pead_active, sv_in)
    if sv["status"] == "n/a":
        t3.append("- **Survival cap (v1.3):** not applicable (India only).")
        if core_asset_threat_reason(sv_in):
            t3.append("  - **Core-asset threat recorded (L40), not applied (survival cap is India only): %s.** "
                      "Weigh it by hand." % core_asset_threat_reason(sv_in))
        gates.append(("Stage 3 survival cap", "n/a", False))
    elif sv["mode"] == "cap":
        t3.append("- **Survival cap (v1.3, general): %s** (%s). Outside the PEAD window a red flag still roughly "
                  "2.5x the 12-month halving risk and 5x the 3-year failure risk (L39: 17.8%% vs 7.1%%; 14.4%% vs 2.8%%), "
                  "but flagged firms also produce more 3x winners, so the rule is a size cap, not a veto: **at most "
                  "%s of the portfolio at cost, no additions while the flag stands**. %s"
                  % (sv["status"], "; ".join(sv["reasons"]), pct(SURVIVAL_MIN_SIZE, 0),
                     "Unchecked inputs are treated as triggered until checked. " if sv["status"] == "UNCHECKED" else ""))
        t3.append("  - %s" % SURVIVAL_QUESTION)
        gates.append(("Stage 3 survival cap", "%s (%s) → size cap %s, no additions; balance-sheet question open"
                      % (sv["status"], "; ".join(sv["reasons"]), pct(SURVIVAL_MIN_SIZE, 0)), False))
    else:
        if sv["status"] == "clear":
            t3.append("- **Survival cap (v1.3):** clear: pledge %s of promoter holding and "
                      "interest cover %sx are inside the limits (> %s / < %sx)."
                      % (pct(sv_in.get("pledge_pct_of_promoter"), 0), num(sv_in.get("interest_cover"), 2),
                         pct(SURVIVAL_PLEDGE, 0), num(SURVIVAL_ICR, 1)))
            gates.append(("Stage 3 survival cap", "clear", False))
        else:
            act = ("**already owned → HOLD-REVIEW: no additions, review against the balance-sheet question**"
                   if sv["already_owned"] else "**0 new money**")
            t3.append("- **Survival cap (v1.2): %s** (%s). PEAD avoid window plus a red flag roughly triples 12-month "
                      "halving risk (L35: 17.6%% vs 6.1%%). Rule: %s (independent of the EV gate). %s%s%s"
                      % (sv["status"], "; ".join(sv["reasons"]), act,
                         "Unchecked inputs are treated as triggered until checked. " if sv["status"] == "UNCHECKED" else "",
                         ("Source: %s %s. " % (sv_in.get("source", ""), sv_in.get("as_of", ""))) if sv_in.get("source") else "",
                         sv_in.get("note", "") if sv_in.get("note") else ""))
            t3.append("  - %s" % SURVIVAL_QUESTION)
            gates.append(("Stage 3 survival cap", "%s (%s) → %s; balance-sheet question open"
                          % (sv["status"], "; ".join(sv["reasons"]),
                             "hold-review, no new money" if sv["already_owned"] else "0 new money"), True))
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
    cls_name, cls_note = resolve_base_rate_class(card, wd, wres, rates)
    cls = rates["classes"].get(cls_name) if cls_name else None
    if cls_name and cls is None and (cls_name + "_deprecated") in rates["classes"]:
        cls = rates["classes"][cls_name + "_deprecated"]
        cls_note += " **Deprecated class** (%s)" % cls.get("deprecated", "")
    if cls_name and cls is None:
        raise ValueError("unknown base_rate_class %r (see tools/decision/base_rates.json)" % cls_name)
    F["_input_warnings"] = base_rate_warnings(cls_name, cls, rates)   # stderr only; the card text is unchanged

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
    # v1.2 tail anchoring (L36)
    aw, aw_note = anchor_weight(card.get("tail_anchor"))
    anc = {"p_blowup": anchor_p(sc.get("p_blowup"), br("p_blowup"), aw),
           "p_le_half": anchor_p(sc.get("p_le_half"), br("p_le_half"), aw)}
    anchored_on = cls is not None and any(br(k) is not None for k in anc)
    if anchored_on:
        for row, key in ((prow[1], "p_le_half"), (prow[2], "p_blowup")):
            row.append(pct(anc[key], 1) if br(key) is not None else "n/a (no base rate)")
        prow[0].append("not anchored")
    lowered = [lbl for lbl, key in (("P(≤0.5x)", "p_le_half"), ("P(blow-up)", "p_blowup"))
               if anchored_on and br(key) is not None and sc.get(key) is not None and anc[key] < sc[key] - 1e-12]
    hdr = ["Event", "Model (worksheet)", "Base rate", "Model ÷ base"] + (
        ["Anchored (w=%.2f on base)" % aw] if anchored_on else [])
    ptxt = [_table(hdr, prow), ""]
    if anchored_on:
        ptxt.append("**Outside-view anchoring (v1.2, L36):** anchored P = %.2f × base rate + %.2f × model for P(≤0.5x) "
                    "and P(blow-up) (weight: %s). The expected-value gate and Kelly use the anchored tails; the "
                    "paper calls keep the raw model probability (with the anchored one alongside), so Brier scoring "
                    "can tell which was better. This is a calibration safeguard, not a change to the hurdle. The "
                    "default weight is 0.5; a lower weight needs a written evidence note, never below %.2f."
                    % (aw, 1 - aw, aw_note, ANCHOR_WEIGHT_MIN))
        ptxt.append("")
        if lowered:
            ptxt.append("> **WARNING: %s** (%s: the class base rate is below our model tail, so anchoring made the card "
                        "more optimistic, L40). If the model tail rests on company-specific evidence (a lease expiry, a "
                        "licence dispute, a debt wall), the raw tail is the honest number: write that evidence in the "
                        "deep dive and size off the raw tail by hand; the mechanical size below uses the anchored one."
                        % (ANCHOR_LOWERED_WARNING, ", ".join(lowered)))
            ptxt.append("")
            gates.append(("Tail anchoring (v1.4 warning)", "%s: %s" % (ANCHOR_LOWERED_WARNING, ", ".join(lowered)), False))
    else:
        ptxt.append("**Outside-view anchoring (v1.2):** no base rate on file for the tails → raw model tails used in "
                    "the EV gate and Kelly (nothing to anchor to).")
        ptxt.append("")
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

    # --- anchored outcome distribution (v1.2): used by the EV gate and Kelly
    hurdle = sc.get("hurdle_mult5")
    touts = _outcomes_tagged(sc, wd["dispersion"]) if sc.get("scenarios") else None
    outs_raw = [(p, m) for p, m, _ in touts] if touts else None
    outs_anc, ev_anc, pl_eff = outs_raw, sc.get("ev_mult5"), anc["p_le_half"]
    if touts and anchored_on:
        pa = anc["p_blowup"] if br("p_blowup") is not None else sc.get("p_blowup") or 0.0
        pl_t = anc["p_le_half"] if br("p_le_half") is not None else sc.get("p_le_half") or 0.0
        outs_anc, pl_eff = anchor_outcomes(touts, pa, pl_t)
        # keep the worksheet's EV convention (scenario mult5 as the mean): shift it by the reweighting effect
        ev_anc = sc["ev_mult5"] + (sum(p * m for p, m in outs_anc) - sum(p * m for p, m in outs_raw))

    # --- expected value
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
        if anchored_on:
            evtxt.append("")
            evtxt.append("**Anchored EV (v1.2, used by the gate):** %s (raw model %s). Tails reweighted to P(blow-up) %s "
                         "and P(≤0.5x) %s%s; the rest of the distribution is scaled in proportion, its shape kept."
                         % (mult(ev_anc), mult(sc["ev_mult5"]), pct(anc["p_blowup"] if br("p_blowup") is not None
                                                                     else sc.get("p_blowup"), 1),
                            pct(pl_eff, 1), " (floored at the anchored blow-up: a blow-up ends ≤0.5x in the model)"
                            if anc["p_le_half"] is not None and pl_eff > anc["p_le_half"] + 1e-12 else ""))
        below = ev_anc < hurdle
        gates.append(("Expected value vs hurdle", "EV %s%s vs hurdle %s → %s" % (
            mult(ev_anc), (" anchored (raw %s)" % mult(sc["ev_mult5"])) if anchored_on else "", mult(hurdle),
            "below hurdle → size 0" if below else "above hurdle"), below))
    else:
        evtxt.append("_No scenario multiples: give exit_pe for every scenario in the worksheet input._")
        gates.append(("Expected value vs hurdle", "not computable → size 0", True))
    F["expected_value"] = "\n".join(evtxt)

    # --- sizing
    sz = card.get("sizing") or {}
    tier = sz.get("tier", "satellite")
    cap = sz.get("max_pct_at_cost") or TIER_CAPS.get(tier, 0.04)
    kf = sz.get("kelly_fraction", 0.25)
    f_star = f_star_raw = None
    if outs_anc and hurdle:
        f_star, _ = _kelly(outs_anc, hurdle)
        f_star_raw = _kelly(outs_raw, hurdle)[0] if anchored_on else f_star
    kelly_size = f_star * kf if f_star is not None else None
    liq = None
    if sz.get("adv_value") and sz.get("portfolio_value"):
        liq = sz.get("adv_pct", 0.10) * sz["adv_value"] * sz.get("days_to_exit", 5) / sz["portfolio_value"]
    cands = [x for x in (kelly_size, cap, liq) if x is not None]
    rule_size = min(cands) if cands and kelly_size is not None else 0.0
    blocked = [g for g in gates if g[2]]
    final = 0.0 if blocked else rule_size
    if sv["mode"] == "cap":               # v1.3 general survival cap: starter size, no additions if already owned
        final = 0.0 if sv["already_owned"] else min(final, SURVIVAL_MIN_SIZE)
    sv_owned_note = (sv["triggered"] and sv["already_owned"])
    srows = [
        ["Full Kelly f* (5-yr bet vs index hurdle, %s)" % ("anchored outcomes; raw model %s" % pct(f_star_raw, 1)
                                                            if anchored_on else "scenario outcomes"), pct(f_star, 1)],
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
    if sv["mode"] == "cap":
        stxt.append("")
        stxt.append("**Survival cap (v1.3, general):** red flag outside the PEAD window → size capped at %s of the "
                    "portfolio at cost, no additions (%s). A size cap, not a veto: flagged firms halve and fail far more "
                    "often but also produce more 3x winners (L39). The cap lapses when the flag clears."
                    % (pct(SURVIVAL_MIN_SIZE, 0), "already owned → hold, 0 new money" if sv["already_owned"]
                       else "final size %s" % pct(final, 1)))
    if sv["mode"] == "block":
        stxt.append("")
        stxt.append("**Survival cap (v1.2):** %s. Chosen policy: 0 new money rather than a minimum size, because the "
                    "red flag is a solvency risk, not a valuation question; the cap lapses when the PEAD window ends "
                    "or the red flag clears; the balance-sheet question must be answered on the card either way."
                    % ("already owned → hold-review (no additions)" if sv_owned_note else "0 new money"))
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
    anc_by_key = {"ge3x": None, "le0p5x": anc["p_le_half"] if anchored_on and br("p_le_half") is not None else None,
                  "blowup": anc["p_blowup"] if anchored_on and br("p_blowup") is not None else None}
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
                     "anchored_probability": round(anc_by_key[key], 4) if anc_by_key[key] is not None else None,
                     "anchor_weight": aw if anc_by_key[key] is not None else None,
                     "base_rate_reasoning": (cls["label"] + ". " + cls["caveats"]) if cls else "no class chosen",
                     "method": "decision-card-v1", "card_version": CARD_VERSION.split(" ")[0], "made_on": slug_date, "resolve_by": resolve.isoformat(),
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
                 "survival_cap": sv, "anchor_weight": aw if anchored_on else None, "ev_mult5_raw": sc.get("ev_mult5"),
                 "ev_mult5_anchored": ev_anc, "p_blowup_anchored": anc["p_blowup"] if anchored_on else None,
                 "p_le_half_anchored": anc["p_le_half"] if anchored_on else None,
                 "anchor_lowered_tails": lowered,
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
    try:
        fields, records, wres = build(card, a.card)
    except CardInputError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    for w in fields.get("_input_warnings", []):
        print("WARNING: %s" % w, file=sys.stderr)
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
