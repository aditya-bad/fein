"""Cohort-2 forward calls (prereg s2): said in the latest call (or the one before if not restated), deadline
2026-12-01 -> 2027-07-31, max 6 per company. Quotes checked against the transcript text. Imported by build.py."""

SECTOR = {'INTELLECT': 'Information Technology', 'RATEGAIN': 'Information Technology',
          'SFL': 'Consumer Durables', 'GREENLAM': 'Consumer Durables',
          'SUPRAJIT': 'Automobile and Auto Components', 'LANDMARK': 'Automobile and Auto Components'}
NAME = {'INTELLECT': 'Intellect Design Arena', 'RATEGAIN': 'RateGain Travel Technologies', 'SFL': 'Sheela Foam',
        'GREENLAM': 'Greenlam Industries', 'SUPRAJIT': 'Suprajit Engineering', 'LANDMARK': 'Landmark Cars'}

FY = {"type": "a", "auto": "structured", "kind": "india_fin", "period": "FY", "end": "2027-03-31", "check_from": "2027-04-15"}


def fin(metric, op, thr, guard, basis="consolidated", **kw):
    d = dict(FY); d.update({"metric": metric, "basis": basis, "op": op, "threshold": thr, "guard": guard}); d.update(kw)
    if metric.endswith("_pct"): d["round"] = 1
    return d


def doc(sym, subject, phrases, note, check_from, deadline, op=None, thr=None, typ="a", event_deadline=None):
    d = {"type": typ, "auto": "assisted", "kind": "doc_scan", "source": "nse", "symbol": sym, "from": "2026-11-26",
         "deadline": deadline, "subject": subject, "phrases": phrases}
    if op: d.update({"op": op, "threshold": thr})
    d["note"] = note
    d["check_from"] = check_from
    if event_deadline: d["event_deadline"] = event_deadline
    return d


# fields: sym, slug, group, said_on, quote, claim, rule, spec(dict), resolve_by
FWD = []
