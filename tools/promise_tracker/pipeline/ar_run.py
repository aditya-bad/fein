#!/usr/bin/env python3
"""AR mode, stages 3-6: annual reports -> candidates -> promises -> evidence from the next report -> score -> report.

    python3 -I ar_run.py SUNFLAG [--n 5] [--cache AR_ROOT] [--as-of YYYY-MM-DD] [--out DIR]
                         [--promises FILE] [--emit-prompts DIR] [--no-screener] [--tags t1,t2] [--skip-fetch]

For Indian companies with NO earnings calls. Every annual report is one "call" dated at its NSE submission date
(ar_fetch.py), its forward-looking sections become management "turns" (ar_sections.py), and then the concall
pipeline runs UNCHANGED on a separate cache root: candidates.py (rule filter) -> score.py (numbers + chains) ->
report.py (MCS, candour, seed). What this file adds:
  1. annotate()        joins each candidate to its AR block (sub-heading, table-row name, focus flag).
  2. build_promises()  rule-based structuring (no LLM needed): keeps forward statements whose subject is the
                       company (not the economy or the industry), with a project/target word and a future marker;
                       sets category (AR categories: capacity_commissioning, approval_regulatory, capex, ...),
                       the asset key (the table row's name or a rare proper noun such as "Bajna"), the milestone
                       (ec / fc / lease / production / commissioning / ...), and chain_key = asset:milestone, so
                       score.py's chain rule sees a re-dated milestone across reports as a goalpost move.
                       With --promises FILE (e.g. llm_extract.py output on this cache root) this step is skipped.
  3. evidence()        the next reports are the evidence: for each promise, sentences in LATER reports that
                       name the asset (and milestone) are classified done / pending / dropped and dated
                       (dd.mm.yyyy, "21st April, 2026"...). Status rules (deadline d):
                         done on or before d                              -> delivered
                         done within 6 months after d                     -> partly
                         done later, or still pending in a report after d -> missed
                         dropped/lapsed/de-allocated (stated)             -> withdrawn
                         no later report mentions it, deadline passed     -> pending + suggested "silently-dropped?"
                         deadline not reached / no report after d yet     -> pending (tracking evidence kept)
                       Vague deadlines default to the FY two years after the report (score.py rule) and are flagged.
                       The result goes in `status` (+ `evidence`, `status_basis` = "ar-evidence(auto)"); report.py's
                       hybrid rule still lets numbers (score.py auto) and human overrides win.
  4. fix_chains()      score.py's chain rule turns a quietly re-dated milestone into moved-goalpost unless the numbers
                       delivered it; in AR mode a milestone the evidence shows DONE ON TIME keeps "delivered".
Human corrections: <out>/<SYMBOL>_overrides.jsonl, as in run.py. Seed output is never written into memdb/seeds.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C  # noqa: E402
import candidates as CA  # noqa: E402
import ar_fetch  # noqa: E402
import ar_sections  # noqa: E402

COMPANY_RX = re.compile(r"\b(we|our|your company|the company|company['’]s|your directors|the board|"
                        r"(?:the|our|its) (?:\w+ )?(?:division|segment|business|subsidiary|plant|unit)s?|"
                        r"management (?:is|remains|expects|plans)|its (?:new|proposed|ongoing))\b", re.I)
MACRO_RX = re.compile(r"\b(economy|economic|GDP|global|world|worldwide|India['’]s|the country|nation(?:al)?|industry|"
                      r"sector|government['’]s|policy|IMF|inflation|monsoon|market size|demand for steel|"
                      r"geopolitic|tariff|central bank|RBI|interest rates?|consumption|per capita|population|"
                      r"crude steel|Viksit|Make in India|Atmanirbhar|domestic demand|CAGR|market (?:size|value)|"
                      r"projected value|(?:the|global|indian|print|book|steel|lubricants?) market (?:is|was|will|stood))\b", re.I)
PROJECT_RX = re.compile(r"project|plant|capacity|expan\w*|commission\w*|mine|mining|block|capex|capital expenditure|"
                        r"greenfield|brownfield|clearance|lease|licen[cs]e|facility|unit\b|line\b|launch\w*|"
                        r"order book|acqui\w*|subsidiary|joint venture|\bJV\b|new product|approval|production|"
                        r"debottleneck\w*|upgrad\w*|install\w*|set(?:ting)? up|construct\w*|revenue|turnover|margin|"
                        r"EBITDA|debt|borrowing|repay\w*|dividend|export|target|market (?:coverage|share|presence|reach)|"
                        r"presence|footprint|network|distribut\w*|stake|alliance|partner\w*|certif\w*|diversif\w*", re.I)
FUTURE_RX = re.compile(r"\b(will|shall|expected|expects?|likely|anticipat\w*|plan(?:s|ned|ning)?|propos\w*|intend\w*|"
                       r"target(?:s|ed|ing)? (?:to|of|for)|aim(?:s|ed|ing)? (?:to|at)|envisag\w*|scheduled|to be (?:commissioned|completed|started|operational|set up)|"
                       r"under (?:implementation|construction|execution)|in (?:the )?pipeline|going forward|"
                       r"upcoming|next (?:year|financial year|fiscal)|by FY\d\d|by (?:the )?end of|to acquire|"
                       r"explor\w+ (?:opportunit|the possibilit|options)|seek(?:s|ing)? to|in the process of)\b", re.I)
PAST_ONLY_RX = re.compile(r"\b(has been|have been|was|were|had|during the year|under review|as on 31)\b", re.I)
MILESTONES = [
    ("ec", r"environment(?:al)? clearance|\bEC\b"),
    ("fc", r"forest clearance|stage[\s-]?(?:I|1|II|2)\b|\bFC\b|wildlife clearance"),
    ("lease", r"mining lease|\bML\b|lease deed|composite licen[cs]e|vesting order|\bCMDPA\b|\bMDPA\b"),
    ("production", r"commercial production|start(?:ing)? (?:of )?(?:mining|production)|mine opening|"
                   r"commence\w* (?:mining|production|operations?)|production (?:will|to) (?:start|commence)"),
    ("commissioning", r"commission\w*|trial run|trial production|go live|operational|COD\b"),
    ("completion", r"complet\w*"),
    ("capacity", r"capacity|expansion|debottleneck\w*|brownfield|greenfield"),
    ("launch", r"launch\w*|new product"),
    ("approval", r"approv\w*|clearance|licen[cs]e|permission|NOC\b|consent"),
    ("acquisition", r"acqui\w*|stake|joint venture|\bJV\b"),
]
MS_RX = [(k, re.compile(r, re.I)) for k, r in MILESTONES]
GENERIC = set("""the a an and of at in on for to by from with village tah tahsil dist district taluka iron ore coal
block mine mines mining plant plants unit units project projects phase new steel power limited ltd private pvt company
companies group india indian maharashtra gujarat karnataka odisha orissa jharkhand chhattisgarh madhya pradesh uttar
andhra telangana tamil nadu kerala rajasthan punjab haryana bihar bengal west east north south central uttarakhand
assam goa delhi new mumbai nagpur state government ministry board directors director mr ms dr shri hon'ble high court
supreme coal-block manganese bauxite limestone phosphorite captive commercial ha hectare area mineral status present
name sr no s.n particulars fy financial year letter intent loi environment environmental forest clearance stage mtpa
mt tpa kwh mw crore lakh rs inr usd your our we it this that these those its their during under as per total
annual report management discussion analysis direct reduction rolled products melting blast furnace hot metal pig
renewable solar wind energy hydro thermal capital expenditure expansion one two three four five six seven eight
nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty
seventy eighty ninety hundred thousand lakhs crores only rupees consequently further however besides also jointly
joint venture subsidiary associate cin""".split())
DONE_RX = re.compile(
    r"\b(?:has|have|had) (?:also )?(?:been )?(?:obtained|received|granted|accorded|executed|commissioned|completed|signed|"
    r"started|commenced|achieved|approved|issued|operationali[sz]ed|acquired)\b|"
    r"\b(?:was|were|is|are) (?:successfully )?(?:obtained|received|granted|accorded|executed|commissioned|completed|"
    r"signed|started|commenced|approved|issued|operationali[sz]ed|acquired)\b|"
    r"\b(?:obtained|received|granted|executed|commissioned|completed|commenced|signed|approved|issued)\s+(?:on|in|during|vide|from|by)\b|"
    r"\bcommercial (?:production|operations?) (?:has |have )?(?:started|commenced|began)\b|"
    r"\b(?:began|commenced|started) (?:on|in)\b|"
    r"\b(?:commissioned|completed|commenced|launched|installed|acquired|executed|obtained)\s+(?:its|the|our|a|an|all)\b", re.I)
DURING_YEAR_RX = re.compile(r"during the (?:year|financial year|period)(?: under review)?|in the year under review", re.I)
PENDING_RX = re.compile(r"\b(pending|awaited|under process|in progress|yet to|under (?:consideration|implementation|"
                        r"construction|execution|examination)|applied for|application|submitted|likely|expected|"
                        r"sub[\s-]?judice|stayed|in the process)\b", re.I)
DROP_RX = re.compile(r"\b(surrender\w*|abandon\w*|withdrawn|withdrew|terminat\w*|cancel\w*|de-?allocat\w*|lapsed|"
                     r"not (?:to )?(?:pursue|proceed)|dropped|shelved|put on hold|decided not)\b", re.I)
ACK_RX = re.compile(r"\b(delay\w*|postpon\w*|deferred|revised|rescheduled|due to|on account of|owing to|slipp\w*)\b", re.I)
EVD_DATE_RX = re.compile(r"\b(\d{1,2})[./-](\d{1,2})[./-](20\d\d)\b")


# ------------------------------------------------------------------ helpers
def load_turn_docs(root, sym):
    out = {}
    for f in sorted(glob.glob(os.path.join(root, sym, "turns", "*.json"))):
        d = C.load_json(f)
        out[d["call_date"]] = d
    return dict(sorted(out.items()))


def company_words(docs, sym):
    names = Counter()
    for d in docs.values():
        for t in d["turns"][:400]:
            for m in re.finditer(r"\b([A-Z][A-Za-z&]+)(?:\s+[A-Z][A-Za-z&\.]+){0,5}\s+(?:Limited|Ltd)\b", t["text"]):
                names[m.group(1)] += 1
    top = [w for w, _ in names.most_common(3) if w.lower() not in GENERIC]
    return {w.lower() for w in top[:1]} | {sym.lower()}


def milestones_of(text):
    return [k for k, rx in MS_RX if rx.search(text)]


def asset_key(label, text, df, cwords):
    """The asset a statement is about: first non-generic capitalised word of a table row's name cell, else the
    rarest capitalised non-generic word in the sentence (document frequency <= 40 blocks)."""
    def toks(s):
        return [w for w in re.findall(r"\b[A-Z][a-zA-Z]{3,}\b", s or "")
                if w.lower() not in GENERIC and w.lower() not in cwords and w.lower() not in CA.C.MONTHS]
    if label:
        lt = toks(label)
        if lt and df.get(lt[0].lower(), 0) <= 60:
            return lt[0].lower()
    # prose: only a rare capitalised word that names a physical asset ("Bajna block", "Blooming Mill", "Rewari plant")
    first = (re.match(r"\W*([A-Za-z]+)", text or "") or [None, None])[1]
    tt = [w for w in toks(text) if w != first and df.get(w.lower(), 99) <= 40 and re.search(
        r"\b" + re.escape(w) + r"\b(?:\s+[\w&-]+){0,3}?\s+(?:plant|mine|mines|block|unit|project|facility|mill|line|"
        r"factory|works|park|terminal|furnace|warehouse|site)\b", text, re.I)]
    if tt:
        return min(tt, key=lambda w: df.get(w.lower(), 99)).lower()
    return None


def doc_freq(docs):
    df = Counter()
    for d in docs.values():
        for t in d["turns"]:
            for w in {w.lower() for w in re.findall(r"\b[A-Z][a-zA-Z]{3,}\b", t["text"] + " " + (t.get("label") or ""))}:
                df[w] += 1
    return df


def parse_evd_date(s):
    for m in EVD_DATE_RX.finditer(s):
        try:
            yield m.start(), dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            pass
    for pos, d in C.find_dates(s):
        yield pos, d


# ------------------------------------------------------------------ 1. annotate candidates
def annotate(root, sym, docs):
    path = os.path.join(root, sym, "candidates.jsonl")
    rows = C.read_jsonl(path)
    for r in rows:
        m = re.search(r":(\d+)-(\d+)$", r["id"])
        t = docs[r["call_date"]]["turns"][int(m.group(1))]
        r.update(ar_label=t.get("label"), ar_kind=t.get("kind"), ar_focus=t.get("focus"), ar_section=t.get("ar_section"),
                 ar_block=t["text"][:1500], source_doc=docs[r["call_date"]].get("quarter"))
    C.write_jsonl(path, rows)
    return rows


# ------------------------------------------------------------------ 2. promises
def ar_deadline(c):
    """candidates.py resolves deadlines for a spoken call. In an annual report, "this/current year" is the year under
    review and "31st March, 2026" is a balance-sheet date, so: drop deadlines read from a full date on or before the
    filing date, and drop 'this/current year' phrases; keep the latest remaining specific date."""
    filed = dt.date.fromisoformat(c["call_date"])
    s = c["sentence"]
    past_dates = [(pos, d) for pos, d in C.find_dates(s) if d <= filed] + \
        [(pos, d) for pos, d in parse_evd_date(s) if d <= filed]
    keep = []
    for d in c.get("all_deadlines") or []:
        raw = d.get("raw") or ""
        if re.search(r"\b(this|current|the current)\s+(year|fiscal|financial year|quarter)", raw, re.I):
            continue
        if d.get("precision") == "month" and any(raw.split()[-1].lower()[:3] in s[pos:pos + 25].lower()
                                                 for pos, _ in past_dates):
            continue
        if d.get("date") and d["date"] <= c["call_date"]:
            continue
        keep.append(d)
    return CA.primary_deadline(keep) if keep else None



AR_CATEGORY = [
    ("approval_regulatory", r"clearance|\bEC\b|\bFC\b|licen[cs]e|lease|approval|permission|NOC\b|consent|vesting"),
    ("capacity_commissioning", r"commission\w*|capacity|expan\w*|plant|mine opening|production|greenfield|brownfield|"
                               r"set(?:ting)? up|construct\w*|debottleneck\w*|install\w*|block|mine\b"),
]


def ar_category(c, text):
    base = c.get("category") or "other"
    if base in ("revenue_growth", "margin", "profit", "debt_reduction", "dividend_payout", "capex", "working_capital",
                "returns", "cash_flow", "fundraise", "m&a") and (c.get("numbers") or base in ("capex", "m&a", "fundraise")):
        return base
    for cat, rx in AR_CATEGORY:
        if re.search(rx, text, re.I):
            return cat
    return "other" if base in ("order_inflow", "order_book") else base


def build_promises(cands, docs, sym):
    df = doc_freq(docs)
    cw = company_words(docs, sym)
    out, seen = [], set()
    drop = Counter()
    for c in cands:
        s = c["sentence"]
        if c["call_date"] not in docs:
            continue
        is_row = c.get("ar_kind") == "row"
        def names_co(x):
            return bool(COMPANY_RX.search(x)) or any(re.search(r"\b" + re.escape(w) + r"(?:['’]s)?\b", x, re.I) for w in cw)
        # subject = the company: in the sentence, or in the sentence before it (pdftotext splits "The Company has
        # entered into a Share Purchase Agreement on June 07, 2025, to acquire ...")
        own = is_row or names_co(s) or names_co(c.get("context") or "")
        if not own:
            drop["not about the company"] += 1
            c["ar_drop"] = "not about the company"
            continue
        if MACRO_RX.search(s) and not (is_row or names_co(s)):
            drop["macro/industry"] += 1
            c["ar_drop"] = "macro/industry"
            continue
        if not PROJECT_RX.search(s + " " + (c.get("ar_label") or "")):
            drop["no project/target word"] += 1
            c["ar_drop"] = "no project/target word"
            continue
        dl = ar_deadline(c) or {}
        if is_row and not FUTURE_RX.search(s):
            drop["table row without a future marker"] += 1
            c["ar_drop"] = "table row without a future marker"
            continue
        fut_dated = bool(dl.get("date")) and dl["date"] > c["call_date"]
        if not (FUTURE_RX.search(s) or (fut_dated and names_co(s))):
            drop["no future marker"] += 1
            c["ar_drop"] = "no future marker"
            continue
        if PAST_ONLY_RX.search(s) and not FUTURE_RX.search(s):
            drop["past tense"] += 1
            c["ar_drop"] = "past tense"
            continue
        if re.search(r"\b(lakh|crore)\b.*\bas compared to\b|net (profit|loss) for the year under review", s, re.I) or \
                (re.search(r"\b(as against|as compared to|compared to|vis-?[aà]-?vis|increased to|decreased to|"
                           r"declined to|stood at)\b", s, re.I) and not FUTURE_RX.search(s)):
            drop["past result"] += 1
            c["ar_drop"] = "past result"
            continue
        # a forward statement whose own date had already passed when the report was filed ("will go for
        # recertification in June 2023" in a report filed July 2023): copied text, a disclosure-quality flag
        stale = [d0.get("raw") for d0 in CA.extract_deadlines(s, dt.date.fromisoformat(c["call_date"]) - dt.timedelta(days=400))
                 if d0.get("date") and d0["date"] < c["call_date"] and d0.get("precision") in ("month", "quarter")]
        key = (c["call_date"], re.sub(r"\W+", " ", s.lower())[:160])
        if key in seen:
            continue
        seen.add(key)
        ms = milestones_of(s)
        asset = asset_key(c.get("ar_label") if is_row else None, s, df, cw)
        cat = ar_category(c, s)
        said = c["call_date"]
        if dl.get("date"):
            deadline, prec = dl["date"], dl.get("precision")
        else:
            deadline, prec = C.fy_end(C.fy_of(dt.date.fromisoformat(said)) + 2).isoformat(), "vague"
        if prec != "vague" and deadline > (dt.date.fromisoformat(said) + dt.timedelta(days=3650)).isoformat():
            prec = "multi-year"
        nums = c.get("numbers") or []
        n0 = nums[0] if nums else {}
        spec = "precise" if (nums and prec not in ("vague", "multi-year")) else \
            "range" if (nums or prec not in ("vague",)) else "vague"
        if asset:
            metric = f"{asset.title()} " + (ms[0] if ms else cat.replace("_", " "))
        else:   # content words, so score.py's metric-token clustering only joins genuine restatements
            cw_ = [w for w in re.findall(r"[A-Za-z][a-z]{4,}", s) if w.lower() not in GENERIC and
                   w.lower() not in ("company", "which", "their", "there", "these", "would", "could", "continue")]
            metric = " ".join(dict.fromkeys(w.lower() for w in cw_))[:80] or cat.replace("_", " ")
        target = ", ".join(n["raw"] for n in nums[:3]) or (f"{ms[0] if ms else 'milestone'} by {dl.get('raw') or deadline}")
        slug = C.slugify(f"{asset or ''} {ms[0] if ms else ''} {' '.join(s.split()[:8])}", 48)
        pid = f"promise:{sym}:{said}:{slug}"
        while any(p["id"] == pid for p in out):
            pid += "-2"
        mat = 3 if (is_row or c.get("ar_focus")) and cat in ("capacity_commissioning", "approval_regulatory", "capex") and \
            prec not in ("vague",) else 1 if (spec == "vague" and not c.get("ar_focus")) else 2
        out.append({
            "id": pid, "symbol": sym, "said_on": said, "speaker": c.get("speaker"), "quote": s,
            "context": c.get("context"), "source_doc": f"{c.get('source_doc')} annual report ({c.get('ar_section')}"
                                                       f"{'; table row ' + str(c.get('ar_label'))[:60] if is_row else ''})",
            "source_url": c.get("source_url"), "category": cat, "metric": metric, "target": target,
            "target_low": n0.get("low"), "target_high": n0.get("high"), "unit": n0.get("unit"),
            "comparator": n0.get("comparator"), "deadline": deadline, "deadline_precision": prec,
            "deadline_raw": dl.get("raw"), "deadline_assumed": dl.get("assumed") if dl else "vague: FY+2 default",
            "chain_key": f"{asset}:{ms[0]}" if asset and ms else None, "asset": asset, "milestones": ms,
            "acknowledges_revision": bool(ACK_RX.search(s)), "specificity": spec, "materiality": mat,
            "volunteered": True, "prompted": False, "tier": c.get("tier"), "candidate_id": c["id"],
            "mode": "annual_report", "title": f"{metric}: {target}"[:140],
            "stale_at_filing": stale[0] if stale and FUTURE_RX.search(s) else None})
    return out, drop


# ------------------------------------------------------------------ 3. evidence from later reports
def sentences_about(doc, p):
    """Later-report sentences about the promise's asset (and milestone when the promise names one)."""
    hits = []
    asset = p.get("asset")
    ms = p.get("milestones") or []
    rx_ms = [rx for k, rx in MS_RX if k in ms]
    for t in doc["turns"]:
        hay = (t.get("label") or "") + " " + t["text"]
        if asset and not re.search(r"\b" + re.escape(asset) + r"\b", hay, re.I):
            continue
        mt = {w for w in re.findall(r"[a-z]{5,}", (p.get("quote") or "").lower()) if w not in GENERIC}
        if not asset and len(mt & set(re.findall(r"[a-z]{5,}", hay.lower()))) < 3:
            continue
        for s in CA.sentences(t["text"]):
            if asset and t.get("kind") != "row" and not re.search(r"\b" + re.escape(asset) + r"\b", s, re.I):
                continue
            if not asset:
                # no asset: same topic needs >= 30% content-word overlap and a company subject, not macro text
                sw = set(re.findall(r"[a-z]{5,}", s.lower()))
                if len(mt & sw) / max(1, len(mt | sw)) < 0.3 or MACRO_RX.search(s) or not COMPANY_RX.search(s):
                    continue
            score = sum(1 for rx in rx_ms if rx.search(s))
            hits.append((score, s, t))
    if rx_ms and any(h[0] for h in hits):
        hits = [h for h in hits if h[0]]
    return hits


MA_DONE_RX = re.compile(r"successful bidder|letter of intent|\bLOI\b|vesting order|acquired|acquisition of|"
                        r"allotted|allocated to the company", re.I)


def ma_evidence(doc, p):
    """m&a / 'looking to acquire mines' promises name no asset: a later report's new allocation is the evidence."""
    out = []
    for t in doc["turns"]:
        for s in CA.sentences(t["text"]):
            if MA_DONE_RX.search(s) and not MACRO_RX.search(s) and not re.search(r"\b(will|likely|expected)\b", s, re.I):
                dates = [x for _, x in parse_evd_date(s) if x > dt.date.fromisoformat(p["said_on"])]
                if dates:
                    out.append((1, s, t))
    return out


def classify(s):
    if DROP_RX.search(s):
        return "dropped"
    if DONE_RX.search(s) and not re.search(r"\b(likely|expected|will|yet to)\b", s, re.I):
        return "done"
    if PENDING_RX.search(s) or FUTURE_RX.search(s):
        return "pending"
    return "mention"


def evidence(promises, docs, as_of):
    dates = sorted(docs)
    for p in promises:
        dl = dt.date.fromisoformat(p["deadline"][:10])
        later = [d for d in dates if d > p["said_on"]]
        trail = []
        done_at, dropped, pending_after = None, None, None
        for d in later:
            hits = sentences_about(docs[d], p)
            if not hits and not p.get("asset") and p.get("category") == "m&a":
                hits = ma_evidence(docs[d], p)
            kinds = [(classify(s), s) for _, s, _ in hits]
            for k, s in kinds:
                trail.append({"doc": docs[d].get("quarter"), "filed": d, "kind": k, "text": s[:300]})
            dn = [s for k, s in kinds if k == "done"]
            if dn and not done_at:
                ds = [x for _, x in parse_evd_date(" ".join(dn)) if x <= dt.date.fromisoformat(d)]
                if ds:   # a milestone row lists several dated steps: the latest is the milestone; a new acquisition: the first
                    done_at = (min(ds) if p.get("category") == "m&a" else max(ds), dn[0], d, "dated")
                elif DURING_YEAR_RX.search(" ".join(dn)):   # "during the year" = by the reported FY's end
                    done_at = (C.fy_end(C.fy_of(dt.date.fromisoformat(d)) - 1), dn[0], d, "by end of the reported FY")
                else:
                    done_at = (dt.date.fromisoformat(d), dn[0], d, "report date")
            if any(k == "dropped" for k, _ in kinds) and not dropped:
                dropped = (d, next(s for k, s in kinds if k == "dropped"))
            if any(k == "pending" for k, _ in kinds) and dt.date.fromisoformat(d) > dl and not pending_after:
                pending_after = (d, next(s for k, s in kinds if k == "pending"))
        p["evidence_trail"] = trail[:8]
        st, basis, ev = "pending", None, None
        if done_at:
            when, s, d, how = done_at
            if when <= dl:
                st = "delivered"
            elif (when - dl).days <= 183:
                st = "partly"
            else:
                st = "missed"
            basis = f"done {when} ({how}) vs deadline {dl}"
            ev = f"{docs[d].get('quarter')} (filed {d}): {s[:300]}"
            if how != "dated" and st != "delivered":
                basis += "; completion date not stated, upper bound used"
        elif dropped:
            st, basis = "withdrawn", "later report states it lapsed/was dropped"
            ev = f"filed {dropped[0]}: {dropped[1][:300]}"
        elif dl < as_of and pending_after and p.get("asset"):
            st, basis = "missed", f"still pending in a report filed after the deadline {dl}"
            ev = f"filed {pending_after[0]}: {pending_after[1][:300]}"
        elif dl < as_of and pending_after:
            # no named asset: a loosely matched 'pending' sentence is not proof of a miss
            st, basis = "pending", f"deadline {dl} passed; later text on the topic is not conclusive"
            p["suggested_status"] = "missed?"
            p["suggestion_basis"] = f"filed {pending_after[0]}: {pending_after[1][:200]}"
        elif dl < as_of and any(d > dl.isoformat() for d in later):
            st, basis = "pending", "deadline passed; no later report mentions it"
            p["suggested_status"] = "silently-dropped?"
            p["suggestion_basis"] = "not mentioned in any annual report filed after the deadline (read it: maybe done, or immaterial)"
        elif dl < as_of:
            basis = f"deadline {dl} passed but no annual report filed since; check filings/next AR"
        else:
            basis = f"deadline {dl} not reached"
        if p.get("deadline_precision") == "vague" and st in ("missed",):
            basis += "; vague deadline (FY+2 default)"
        p["status"] = st
        p["status_basis"] = "ar-evidence(auto): " + (basis or "")
        if ev:
            p["evidence"] = ev
        if st in ("partly", "missed", "withdrawn"):
            # candour proxy: does the evidence sentence itself explain the slip?
            p["admitted_unprompted"] = bool(ACK_RX.search(ev or "")) or st == "withdrawn"
    return promises


# ------------------------------------------------------------------ asset tracker (the hand "status table" ledger)
QTY_RX = re.compile(r"(\d[\d,]*\.?\d*)\s*(MT|million tons|million tonnes|tonnes|MTPA|MW|lakh tonnes)\b", re.I)


def asset_tracker(docs, sym):
    """asset -> {report: status text} from table rows (and focus prose) across all reports, with flags:
    unchanged quantity (same reserve/capacity figure in consecutive reports), asset gone from the table,
    and 'during the year' sentences repeated verbatim (stale text)."""
    df = doc_freq(docs)
    cw = company_words(docs, sym)
    track = defaultdict(dict)
    rows = [(d, t, asset_key(t.get("label"), t["text"], df, cw)) for d, doc in docs.items() for t in doc["turns"]
            if t.get("kind") == "row"]
    keys = {a for _, _, a in rows if a}
    not_asset = re.compile(r"^\W*(?:\d+\W*)?(?:Mr|Ms|Mrs|Dr|Shri|Smt)\b|contract|ordinary course|nature of|"
                           r"remuneration|salary|designation|JV\b|rights basis", re.I)
    useful = {a for _, t, a in rows if a and (milestones_of(t["text"]) or QTY_RX.search(t["text"]))} - \
        {a for _, t, a in rows if a and not_asset.search((t.get("label") or "") + " " + t["text"][:80])}
    for d, t, a in rows:
        # a row whose name cell names several known assets (rows merged by the PDF layout) counts for each
        cells = t["text"].split(" | ")
        names_txt = " ".join(c for c in cells if c is not max(cells, key=len)) if len(cells) > 2 else (t.get("label") or "")
        names = {w.lower() for w in re.findall(r"\b[A-Z][a-zA-Z]{3,}\b", names_txt + " " + (t.get("label") or ""))} & keys
        for k in ({a} | names) & useful:
            cells = t["text"].split(" | ")
            status = max(cells, key=len) if cells else t["text"]
            prev = track[k].get(d)
            track[k][d] = (prev + " / " if prev else "") + status
    flags = []
    dates = sorted(docs)
    for a, by in track.items():
        seen = [d for d in dates if d in by]
        for x, y in zip(seen, seen[1:]):
            qx = {q.group(0).lower() for q in QTY_RX.finditer(by[x])}
            qy = {q.group(0).lower() for q in QTY_RX.finditer(by[y])}
            same = qx & qy
            if same:
                flags.append({"asset": a, "flag": "unchanged quantity", "reports": [docs[x]["quarter"], docs[y]["quarter"]],
                              "value": sorted(same)[:3]})
        if seen and seen[-1] != dates[-1] and len(seen) >= 1:
            gone = [docs[d]["quarter"] for d in dates if d > seen[-1]]
            flags.append({"asset": a, "flag": "not in later status tables", "reports": gone[:3], "value": None})
    # stale text: the same 'during the year ...' claim in consecutive reports
    sents = {}
    for d, doc in docs.items():
        sents[d] = {re.sub(r"\W+", " ", s.lower()).strip(): s for t in doc["turns"] for s in CA.sentences(t["text"])
                    if DURING_YEAR_RX.search(s) and DONE_RX.search(s) and len(s.split()) >= 6}
    for x, y in zip(dates, dates[1:]):
        for k in sents[x].keys() & sents[y].keys():
            flags.append({"asset": None, "flag": "same 'done during the year' sentence repeated",
                          "reports": [docs[x]["quarter"], docs[y]["quarter"]], "value": sents[y][k][:160]})
    return {a: {docs[d]["quarter"]: v[:400] for d, v in sorted(by.items())} for a, by in sorted(track.items())}, flags


def tracker_md(track, flags, docs):
    qs = [docs[d]["quarter"] for d in sorted(docs)]
    out = ["| Asset | " + " | ".join(qs) + " |", "|---|" + "---|" * len(qs)]
    for a, by in track.items():
        out.append(f"| {a} | " + " | ".join((by.get(q) or "—")[:160].replace("|", "/") for q in qs) + " |")
    out.append("")
    out += [f"- **{f['flag']}**: {f['asset'] or ''} {', '.join(f['reports'])} {f['value'] or ''}" for f in flags]
    return "\n".join(out) + "\n"


def fix_chains(rows):
    n = 0
    for p in rows:
        if p.get("auto_status_final") in ("moved-goalpost", "withdrawn") and p.get("status") == "delivered":
            p["auto_status_basis"] = (p.get("auto_status_basis") or "") + "; AR evidence: delivered on time -> kept delivered"
            p["auto_status_final"] = "delivered"
            n += 1
    return n


# ------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--cache", help="AR-mode cache root (default $PT_CACHE/ar)")
    ap.add_argument("--out")
    ap.add_argument("--as-of")
    ap.add_argument("--promises", help="use these promises (e.g. llm_extract.py output) instead of the rule builder")
    ap.add_argument("--emit-prompts", metavar="DIR", help="also write LLM prompts (candidates.py format)")
    ap.add_argument("--no-screener", action="store_true")
    ap.add_argument("--csv")
    ap.add_argument("--tags", default="")
    ap.add_argument("--skip-fetch", action="store_true", help="reuse the cached manifest/text")
    ap.add_argument("--presentations", action="store_true")
    a = ap.parse_args(argv)
    sym = a.symbol.upper()
    root = ar_fetch.ar_root(a.cache)
    co = ["--cache", root]
    out = a.out or C.sym_dir(root, sym, "out")
    os.makedirs(out, exist_ok=True)
    as_of = dt.date.fromisoformat(a.as_of) if a.as_of else dt.date.today()
    if not a.skip_fetch:
        ar_fetch.main([sym, "--n", str(a.n)] + co + (["--presentations"] if a.presentations else []))
    ar_sections.process_symbol(sym, root)
    CA.main([sym] + co + (["--emit-prompts", a.emit_prompts] if a.emit_prompts else []))
    docs = load_turn_docs(root, sym)
    cands = annotate(root, sym, docs)
    if a.promises:
        prom = C.read_jsonl(a.promises)
        for p in prom:
            p.setdefault("asset", None)
            p.setdefault("milestones", milestones_of(p.get("quote") or ""))
    else:
        prom, drop = build_promises(cands, docs, sym)
        print(f"promises: {len(prom)} from {len(cands)} candidates; dropped {dict(drop)}")
    evidence(prom, docs, as_of)
    track, flags = asset_tracker(docs, sym)
    C.save_json(os.path.join(out, f"{sym}_assets.json"), {"assets": track, "flags": flags})
    open(os.path.join(out, f"{sym}_assets.md"), "w").write(tracker_md(track, flags, docs))
    print(f"asset tracker: {len(track)} assets, {len(flags)} flags -> {sym}_assets.md")
    ppath = os.path.join(root, sym, "promises_ar.jsonl")
    C.write_jsonl(ppath, prom)
    import run as R
    ppath = R.merge_overrides(ppath, os.path.join(out, f"{sym}_overrides.jsonl"))
    import score
    import report
    scored = os.path.join(out, f"{sym}_scored.jsonl")
    score.main([sym, "--promises", ppath, "--out", scored, "--as-of", as_of.isoformat()] + co
               + (["--no-screener"] if a.no_screener else []) + (["--csv", a.csv] if a.csv else []))
    rows = C.read_jsonl(scored)
    n = fix_chains(rows)
    C.write_jsonl(scored, rows)
    print(f"AR chain fix: {n} promise(s) kept delivered (evidence on time)")
    report.main([sym, "--scored", scored, "--seed-out", os.path.join(out, f"{sym}_seed.json"),
                 "--md-out", os.path.join(out, f"{sym}_credibility.md"),
                 "--json-out", os.path.join(out, f"{sym}_summary.json"),
                 "--company-tags", ",".join(x for x in ["ar-mode"] + a.tags.split(",") if x),
                 "--as-of", as_of.isoformat()] + co)


if __name__ == "__main__":
    main()
