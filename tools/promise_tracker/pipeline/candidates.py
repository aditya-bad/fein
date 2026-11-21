#!/usr/bin/env python3
"""Stage 3: rule-based extraction of forward-looking candidate sentences.

    python3 -I candidates.py SYMBOL [--cache DIR] [--min-tier B] [--emit-prompts DIR]

Reads <cache>/<SYMBOL>/turns/*.json, writes <cache>/<SYMBOL>/candidates.jsonl, one row per
candidate sentence from a MANAGEMENT turn:
    id, symbol, call_date, quarter, source_url, speaker, section, volunteered (opening/closing
    remarks) vs prompted (Q&A), question (the analyst question it answers, trimmed),
    sentence, context (prev + sentence + next), tier (A strong / B directional), score, signals,
    category (first guess), metric_terms, numbers [{low, high, unit, comparator, raw}],
    deadline {date, precision, raw, assumed}, all_deadlines
The rules aim for HIGH RECALL; precision is the LLM's job (llm_extract_prompt.md).
--emit-prompts writes one ready-to-run prompt file per call (template + that call's
candidates) for `claude -p` / `gemini` on the Pi; see README.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ lexicons
FUTURE_STRONG = re.compile(
    r"\b(guidance|guiding|guide[ds]?|target(?:s|ed|ing)?|aspir\w*|expect(?:s|ed|ing|ation)?|anticipat\w*|"
    r"envisag\w*|foresee\w*|project(?:ed|ing|ion)s?|outlook|we will|we'll|we shall|will (?:be|see|reach|grow|achieve|"
    r"come|start|cross|have|get|continue|improve|deliver|complete|commission|double|touch|go|remain|maintain|add|"
    r"generate|reduce|become|launch|begin|happen|stay|close|end|ramp|exceed|surpass|move|take|clock|hit|do)|"
    r"going to|plan(?:s|ned|ning)? to|intend\w*|aim(?:s|ed|ing)? (?:to|at|for)|look(?:ing)? (?:at|to|for)ward|"
    r"looking at (?:a |an )?(?:growth|margin|revenue|\d)|on track|confident (?:of|that)|should (?:be|see|reach|grow|come|"
    r"cross|start|get|improve|happen|go)|would (?:be|see|reach|grow|come|start|cross|get|improve)|likely to|"
    r"set to|poised to|in the pipeline|committed to|visibility|(?:I'm|I am|we're|we are|we'll be|we can|I can|you can) "
    r"(?:\w+ )?look(?:ing)? at|could be|may see|might see|(?:I|we)'d like to|would like to|(?:my|our|the) goal|hoping|hope to|"
    r"scheduled|to start from|endeavou?r|we (?:do )?believe|(?:don't |do not )?want to|aspiration|road ?map|"
    r"work(?:ing)? towards|should be (?:possible|able)|we can (?:do|achieve|reach|see|deliver|easily)|reasonable expectation|"
    r"would not be surprised|indication|sustainable|ensure|we see (?:a |an )?(?:growth|margin|revenue|potential)|"
    r"(?:will|would|should) (?:\w+ )?(?:be|come|happen|start))\b", re.I)
FUTURE_WEAK = re.compile(
    r"\b(will|would|should|could|hopefully|hope|going forward|in future|in the future|coming (?:year|quarter|years|"
    r"quarters|months)|next (?:year|quarter|fiscal|financial year|few|two|three|\d|half|month|12|18|24)|"
    r"by (?:the )?end of|over the next|within (?:the next|\d|a |one|two|three|six|twelve)|from next|"
    r"remaining (?:quarters?|part|months)|rest of the year|second half|H2|sustain\w*|maintain\w*|"
    r"long[\s-]term|medium[\s-]term|near[\s-]term|short[\s-]term|aspiration|remains?|continue[sd]?|possibly|probably|"
    r"maybe|full year|for the year|this year|year after|may|might|can)\b", re.I)
QUAL = re.compile(r"\b(flat|flattish|in line|sequential\w*|turnaround|normali[sz]\w*|recover\w*|neutral|better than|similar|"
                  r"healthier|higher|lower|improv\w*|range[\s-]bound|peak|highest|best|stable|strong|robust|sustain\w*|"
                  r"breakeven|break even|positive|negative|reduc\w*|increas\w*|expan\w*|grow\w*|decline|de-?grow\w*)\b", re.I)
PAST = re.compile(
    r"\b(we (?:have )?(?:reported|achieved|delivered|recorded|posted|clocked|registered|completed|secured|received|"
    r"booked|saw|had|did|grew|were|was)|stood at|came in at|was at|were at|during the (?:quarter|year|period|first half)|"
    r"in the (?:last|previous|past) (?:quarter|year)|last year|year-on-year|YoY|compared to|as against|versus last|"
    r"as of (?:now|today|date)|so far)\b", re.I)
NUM = re.compile(
    r"(?:(?:INR|Rs\.?|₹|USD|US\$|\$|EUR|€)\s?\d[\d,]*(?:\.\d+)?\s*(?:crores?|cr\.?|lakhs?|million|mn|billion|bn|"
    r"thousand|k)?|\d[\d,]*(?:\.\d+)?\s*(?:%|percent|per cent|bps|basis points|crores?|cr\b|lakh|million|mn\b|"
    r"billion|bn\b|tonnes?|tons?|MT\b|MTPA|KTPA|MW|GW|GWh|days|x\b|times|units|acres)|"
    r"\b(?:mid|high|low|early|late)[\s-](?:teens?|single[\s-]digits?|double[\s-]digits?|twenties|20s)\b|"
    r"\b(?:double|single)[\s-]digit\b|\b(?:double|triple|doubling|tripling|halve)\b|\bteens?\b)", re.I)
TIMELINE = re.compile(
    r"\b(FY\s?['’]?\s?\d{2,4}|F\d{2}|CY\s?['’]?\s?\d{2,4}|Q[1-4]\s?(?:FY)?\s?['’]?\s?\d{0,4}|H[12]\s?(?:FY)?\s?['’]?\s?\d{0,4}|"
    r"(?:first|second|third|fourth|1st|2nd|3rd|4th) (?:quarter|half)|this (?:year|quarter|fiscal|financial year|month)|"
    r"current (?:year|quarter|fiscal|financial year)|next (?:year|quarter|fiscal|financial year|\w+ (?:years|quarters|months))|"
    r"(?:in|over|within) (?:the )?(?:next |coming )?(?:\d+|one|two|three|four|five|six|twelve|eighteen|few|couple of)"
    r"(?:\s?(?:to|-)\s?(?:\d+|two|three|four|five))? (?:years?|quarters?|months?)|"
    r"by (?:the )?end of|(?:January|February|March|April|May|June|July|August|September|October|November|December)"
    r"(?:\s+20\d\d)?|20[2-4]\d|calendar (?:year )?20\d\d|year[\s-]end|end of (?:the )?(?:year|quarter)|"
    r"going forward|long[\s-]term|medium[\s-]term|quarter [1-4]|full year|year after|for the year)\b", re.I)
CATEGORIES = [  # (category, regex) — first match wins, order matters
    ("order_book", r"order ?book|backlog|unexecuted"),
    ("order_inflow", r"order (?:inflow|intake|win|booking)s?|inflows?|orders?\b|bid(?:s|ding)? pipeline|L1\b"),
    ("margin", r"margins?|ebitda|ebit\b|gross profit|profitability|bps"),
    ("capex", r"capex|capital expenditure|invest(?:ing|ment) of|spend(?:ing)? (?:of|about|around)"),
    ("capacity_commissioning", r"capacit\w*|commission\w*|plant|facility|greenfield|brownfield|warehouse|"
                               r"MTPA|tonnes|line\b|expansion|operational|go live|set ?up"),
    ("debt_reduction", r"\bdebt|borrowing|finance cost|interest cost|leverage|net cash|gearing|deleverag"),
    ("working_capital", r"working capital|receivable|debtor|inventory|cash conversion|\bdays\b|payable"),
    ("m&a", r"acqui\w+|inorganic|merger|M&A|takeover|buyout"),
    ("dividend_payout", r"dividend|payout|buy ?back"),
    ("fundraise", r"rights issue|QIP|preferential|fund ?rais|raise (?:capital|equity|funds)|dilution"),
    ("new_product", r"launch\w*|new product|approval|USFDA|qualif\w+|certif\w+|patent|develop(?:ing|ment) of"),
    ("customer_win", r"customer|client|OEM|contract"),
    ("revenue_growth", r"revenue|top[\s-]?line|sales|turnover|growth|grow\w*|volume|business"),
    ("profit", r"\bPAT\b|net profit|profit after tax|EPS|bottom[\s-]?line|earnings"),
    ("returns", r"ROCE|ROE|return on"),
    ("cash_flow", r"cash flow|FCF|free cash|cash generation|internal accrual"),
]
CAT_RX = [(c, re.compile(r, re.I)) for c, r in CATEGORIES]
METRIC_ANY = re.compile("|".join(r for _, r in CATEGORIES) + r"|utili[sz]ation|market share|export|mix|share of|"
                        r"segment|aftermarket|run[\s-]rate", re.I)
QUAL_RANGES = {  # qualitative magnitudes -> (low, high) %
    "low single": (1, 3), "mid single": (4, 6), "high single": (7, 9), "single digit": (1, 9),
    "low double": (10, 12), "double digit": (10, None), "low teen": (11, 13), "mid teen": (14, 16),
    "mid-teen": (14, 16), "high teen": (17, 19), "early twenties": (20, 23), "teens": (11, 19), "teen": (11, 19),
}
ABBREV = re.compile(r"\b(Mr|Ms|Mrs|Dr|Rs|No|Nos|vs|approx|Ltd|Co|Inc|Pvt|St|Jr|Sr|e\.g|i\.e|etc|Fig|Mn|Bn|Cr)\.", re.I)
NUMWORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
            "ten": 10, "twelve": 12, "eighteen": 18, "few": 3, "couple of": 2, "a": 1}
MONTH_RX = r"(January|February|March|April|May|June|July|August|September|October|November|December)"


def sentences(text):
    t = ABBREV.sub(lambda m: m.group(0)[:-1] + "§", text)
    parts = re.split(r"(?<=[\.\?!…])\s+(?=[A-Z“\"'(\d])|\n+", t)
    out = []
    for p in parts:
        p = p.replace("§", ".").strip()
        if not p:
            continue
        # very long spoken run-ons: split on ' and ' / '; ' after 70 words to keep quotes focused
        words = p.split()
        if len(words) > 90:
            chunks = re.split(r";\s+|,\s+(?:and|but|so)\s+(?=we|our|the|it|this)", p)
            buf = ""
            for c in chunks:
                buf = (buf + ", " + c) if buf else c
                if len(buf.split()) > 35:
                    out.append(buf)
                    buf = ""
            if buf:
                out.append(buf)
        else:
            out.append(p)
    return out


# ------------------------------------------------------------------ numbers
def parse_num(s):
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


UNIT_RX = r"(%|percent|per cent|bps|basis points|crores?|cr\b|lakhs?|million|mn\b|billion|bn\b|tonnes?|tons?|MTPA|KTPA|MT\b|MW|GW|days|x\b|times)"
CURR_RX = r"(INR|Rs\.?|₹|USD|US\$|\$|EUR|€)"


def norm_unit(u, curr=None):
    u = (u or "").lower().strip(".")
    if u in ("%", "percent", "per cent"):
        return "%"
    if u in ("bps", "basis points"):
        return "bps"
    if u.startswith("cr"):
        return ("USD " if curr and "$" in curr or curr and "usd" in curr.lower() else "INR ") + "cr"
    if u.startswith("lakh"):
        return "lakh"
    if u in ("million", "mn"):
        return ("USD " if curr and ("$" in curr or "usd" in curr.lower()) else "INR " if curr else "") + "mn"
    if u in ("billion", "bn"):
        return ("USD " if curr and ("$" in curr or "usd" in curr.lower()) else "INR " if curr else "") + "bn"
    if u.startswith("ton") or u in ("mtpa", "ktpa", "mt"):
        return "tonnes" if u not in ("mtpa", "ktpa") else u.upper()
    return u or (curr or "")


def extract_numbers(s):
    out = []
    used = []
    # ranges: 'INR 4,500 crores to INR 5,000 crores', '20% to 25%', '20-25%', 'between 18 and 20%'
    rng = re.compile(r"(?:between\s+)?" + CURR_RX + r"?\s?(\d[\d,]*(?:\.\d+)?)\s*" + UNIT_RX + r"?\s*"
                     r"(?:to|-|–|and|or)\s*" + CURR_RX + r"?\s?(\d[\d,]*(?:\.\d+)?)\s*" + UNIT_RX, re.I)
    for m in rng.finditer(s):
        lo, hi = parse_num(m.group(2)), parse_num(m.group(5))
        unit = norm_unit(m.group(6) or m.group(3), m.group(1) or m.group(4))
        if lo is not None and hi is not None and lo <= hi * 1.0001 and (hi - lo) < max(abs(hi), 1) * 3:
            out.append({"low": lo, "high": hi, "unit": unit, "comparator": "range", "raw": m.group(0).strip()})
            used.append(m.span())
    single = re.compile(r"(at least|minimum|more than|over|above|in excess of|upwards of|north of|beyond|"
                        r"less than|below|under|up to|upto|maximum|around|about|approximately|nearly|close to|~)?\s*"
                        + CURR_RX + r"?\s?(\d[\d,]*(?:\.\d+)?)\s*" + UNIT_RX + r"(\s*(?:plus|\+|and above|odd))?", re.I)
    for m in single.finditer(s):
        if any(a <= m.start(3) < b for a, b in used):
            continue
        v = parse_num(m.group(3))
        if v is None:
            continue
        q = (m.group(1) or "").lower()
        plus = bool(m.group(5))
        comp = ">=" if plus or q in ("at least", "minimum", "more than", "over", "above", "in excess of", "upwards of",
                                      "north of", "beyond") else "<=" if q in ("less than", "below", "under", "up to",
                                                                              "upto", "maximum") else "~"
        out.append({"low": v, "high": v, "unit": norm_unit(m.group(4), m.group(2)), "comparator": comp,
                    "raw": m.group(0).strip()})
    sl = s.lower()
    for k, (lo, hi) in QUAL_RANGES.items():
        if re.search(r"\b" + k.replace(" ", r"[\s-]") + r"s?\b", sl):
            out.append({"low": lo, "high": hi, "unit": "%", "comparator": "range" if hi else ">=", "raw": k,
                        "qualitative": True})
            break
    for w, f in (("double", 2.0), ("triple", 3.0), ("doubling", 2.0), ("tripling", 3.0)):
        if re.search(r"\b" + w + r"\b", sl) and not re.search(r"double[\s-]digit", sl):
            out.append({"low": f, "high": f, "unit": "x", "comparator": ">=", "raw": w, "qualitative": True})
            break
    return out


# ------------------------------------------------------------------ deadlines
def _fy(y):
    y = int(y)
    return y + 2000 if y < 100 else y


def month_end(y, m):
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def extract_deadlines(s, call):
    """Return list of {date, precision, raw, assumed} resolved relative to the call date.
    Ambiguous expressions resolve to the LATER plausible date (pilot rule) and say so."""
    out = []
    cfy = C.fy_of(call)
    cq, cqfy = C.fq_of(call)
    sl = s

    def add(d, prec, raw, assumed=None):
        out.append({"date": d.isoformat(), "precision": prec, "raw": raw, "assumed": assumed})

    for m in re.finditer(r"\bQ([1-4])\s?(?:FY)?\s?['’]?\s?(\d{2,4})\b", sl, re.I):
        add(C.quarter_end(m.group(1), _fy(m.group(2))), "quarter", m.group(0))
    for m in re.finditer(r"\b(?:Q([1-4])|quarter ([1-4])|(first|second|third|fourth|1st|2nd|3rd|4th) quarter)\b(?!\s?(?:FY)?\s?['’]?\s?\d\d)", sl, re.I):
        q = int(m.group(1) or m.group(2)) if (m.group(1) or m.group(2)) else {"first": 1, "1st": 1, "second": 2, "2nd": 2, "third": 3, "3rd": 3,
                                                "fourth": 4, "4th": 4}[m.group(3).lower()]
        fy = cfy
        if C.quarter_end(q, fy) < call - dt.timedelta(days=60):
            fy += 1
        add(C.quarter_end(q, fy), "quarter", m.group(0), f"Q{q} taken as FY{fy % 100}")
    for m in re.finditer(r"\bH([12])\s?(?:FY)?\s?['’]?\s?(\d{2,4})\b", sl, re.I):
        fy = _fy(m.group(2))
        add(C.quarter_end(2 if m.group(1) == "1" else 4, fy), "half-year", m.group(0))
    for m in re.finditer(r"\b(?:(second|first) half|H([12]))\b(?!\s?(?:FY)?\s?['’]?\s?\d)(\s+of\s+(?:the\s+)?(next|this|current) year)?", sl, re.I):
        h = 2 if (m.group(1) or "").lower() == "second" or m.group(2) == "2" else 1
        fy = cfy + (1 if (m.group(3) and "next" in m.group(3).lower()) else 0)
        d_fiscal = C.quarter_end(4 if h == 2 else 2, fy)
        if d_fiscal < call - dt.timedelta(days=30):
            fy += 1
            d_fiscal = C.quarter_end(4 if h == 2 else 2, fy)
        cy = call.year + (1 if (m.group(3) and "next" in m.group(3).lower()) else 0)
        d_cal = dt.date(cy, 12 if h == 2 else 6, 31 if h == 2 else 30)
        d = max(d_fiscal, d_cal)
        add(d, "half-year", m.group(0), "fiscal vs calendar half ambiguous; later date taken")
    for m in re.finditer(r"\b(?:FY|F|fiscal|financial year)\s?['’]?\s?(20\d{2}|\d{2})\b", sl, re.I):
        fy = _fy(m.group(1))
        if 2015 <= fy <= 2045:
            add(C.fy_end(fy), "fiscal-year", m.group(0))
    for m in re.finditer(r"\b(?:CY|calendar(?: year)?)\s?['’]?\s?(20\d{2}|\d{2})\b", sl, re.I):
        add(dt.date(_fy(m.group(1)), 12, 31), "fiscal-year", m.group(0), "calendar year")
    for m in re.finditer(r"\b(this|current|the current|next|coming) (year|fiscal(?: year)?|financial year)\b", sl, re.I):
        nxt = m.group(1).lower() in ("next", "coming")
        fy = cfy + nxt
        d = C.fy_end(fy)
        if m.group(2).lower() == "year":
            d_cal = dt.date(call.year + nxt, 12, 31)
            if d_cal > d:
                add(d_cal, "fiscal-year", m.group(0), "calendar vs fiscal year ambiguous; later date taken")
                continue
            add(d, "fiscal-year", m.group(0), "fiscal year assumed (later than calendar)")
            continue
        add(d, "fiscal-year", m.group(0))
    for m in re.finditer(r"\b(this|current|next|coming) quarter\b", sl, re.I):
        qe = C.quarter_end_of(call)
        if m.group(1).lower() in ("next", "coming"):
            qe = C.quarter_end_of(qe + dt.timedelta(days=5))
        add(qe, "quarter", m.group(0))
    for m in re.finditer(r"\b(?:in|over|within|for) (?:the )?(?:next |coming )?(\d+|one|two|three|four|five|six|twelve|"
                         r"eighteen|few|couple of|a)(?:\s?(?:to|-|or)\s?(\d+|two|three|four|five|six))? (years?|quarters?|months?)\b",
                         sl, re.I):
        n = m.group(2) or m.group(1)
        n = NUMWORDS.get(n.lower(), None) if not n.isdigit() else int(n)
        if not n:
            continue
        unit = m.group(3).lower()
        days = n * (365 if unit.startswith("year") else 91 if unit.startswith("quarter") else 30.5)
        d = call + dt.timedelta(days=days)
        d = C.quarter_end_of(d)
        add(d, "multi-year" if unit.startswith("year") else "quarter", m.group(0), "upper end of span from call date")
    for m in re.finditer(r"\b(?:by |till |until |before |in |from |end of |starting )?" + MONTH_RX + r"(?:\s+(20\d\d|'\d\d))?\b", sl):
        mon = C.MONTHS[m.group(1).lower()]
        if m.group(2):
            y = _fy(m.group(2).strip("'"))
        else:
            y = call.year if mon >= call.month else call.year + 1
            if mon == call.month and "may" == m.group(1).lower() and not m.group(0).lower().startswith(("by", "in", "from", "end", "till", "until")):
                continue  # the verb 'May'
        if m.group(1) == "May" and not m.group(2) and not re.match(r"(by|in|from|end of|till|until)", m.group(0), re.I):
            continue
        add(month_end(y, mon), "month", m.group(0))
    for m in re.finditer(r"\b(?:by |before )?(?:the )?end of (?:the )?(?:this |current )?(year|calendar year|fiscal|financial year)\b", sl, re.I):
        d = max(dt.date(call.year if call.month <= 12 else call.year + 1, 12, 31), C.fy_end(cfy))
        if d < call:
            d = C.fy_end(cfy + 1)
        add(d, "fiscal-year", m.group(0), "'end of the year' ambiguous (Dec vs Mar); later date taken")
    for m in re.finditer(r"\b(?:by|in|till|until|before)\s+(20[2-4]\d)\b", sl):
        y = int(m.group(1))
        add(max(dt.date(y, 12, 31), C.fy_end(y)), "fiscal-year", m.group(0), "bare year: CY vs FY ambiguous; later date taken")
    for m in re.finditer(r"\b(long[\s-]term|medium[\s-]term|near[\s-]term|going forward|in the coming years|over the years|"
                         r"in due course|soon|shortly)\b", sl, re.I):
        out.append({"date": None, "precision": "vague", "raw": m.group(0), "assumed": None})
    # drop deadlines that are in the past relative to the call (they describe history, e.g. 'FY24 base')
    fut = [d for d in out if d["date"] is None or dt.date.fromisoformat(d["date"]) >= call - dt.timedelta(days=45)]
    return fut


def primary_deadline(dls):
    dated = [d for d in dls if d["date"]]
    if not dated:
        return dls[0] if dls else None
    order = {"quarter": 0, "month": 0, "half-year": 1, "fiscal-year": 2, "multi-year": 3}
    # the latest specific date mentioned is usually the target date ('by FY28', not 'FY26 base')
    return max(dated, key=lambda d: (d["date"], -order.get(d["precision"], 4)))


def category_of(s):
    for c, rx in CAT_RX:
        if rx.search(s):
            return c
    return "other"


def score_sentence(s, call, context=None):
    fs = len(FUTURE_STRONG.findall(s))
    fw = len(FUTURE_WEAK.findall(s))
    nums = extract_numbers(s)
    dls = extract_deadlines(s, call)
    tl = bool(TIMELINE.search(s))
    met = METRIC_ANY.findall(s)
    past = len(PAST.findall(s))
    fut_dated = any(d["date"] and dt.date.fromisoformat(d["date"]) > call + dt.timedelta(days=20) for d in dls)
    qual = QUAL.findall(s)
    met_ctx = METRIC_ANY.findall(context or "") if not met else []
    f = 2 * fs + fw + 2 * fut_dated
    pen = past if fs == 0 else 0
    score = f + 1.5 * bool(nums) + 0.5 * bool(qual) + 1.5 * bool(dls or tl) + 1.0 * bool(met) \
        + 0.5 * bool(met_ctx) - 1.0 * pen
    sig = {"future_strong": fs, "future_weak": fw, "future_dated": fut_dated, "numbers": len(nums),
           "qualitative": len(qual), "timeline": bool(dls or tl), "metric": bool(met),
           "metric_from_context": bool(met_ctx), "past": past}
    tier = None
    if f >= 1 and (met or met_ctx) and (nums or fut_dated or (qual and (dls or tl))) and score >= 4 and pen < 2:
        tier = "A"
    elif f >= 1 and (nums or qual or dls or tl or met) and (met or met_ctx or nums) and score >= 3:
        tier = "B"
    metric_terms = sorted({x.lower() for x in (met or met_ctx) if isinstance(x, str)})[:8]
    return tier, score, sig, nums, dls, metric_terms


def extract_call(doc, min_tier="B"):
    call = dt.date.fromisoformat(doc["call_date"])
    turns = doc["turns"]
    out = []
    for t in turns:
        if t["role"] != "management":
            continue
        q = None
        if t.get("question_i") is not None:
            q = turns[t["question_i"]]["text"][:500]
        sents = sentences(t["text"])
        for j, s in enumerate(sents):
            if len(s.split()) < 5:
                continue
            if s.rstrip().endswith("?") and not (j + 1 < len(sents) and re.match(
                    r"(the answer is yes|yes|absolutely|definitely|certainly)", sents[j + 1], re.I)):
                continue
            ctx = " ".join(sents[max(0, j - 1): j + 2])
            tier, score, sig, nums, dls, met = score_sentence(s, call, ctx + " " + (q or "")[-300:])
            if tier is None or (min_tier == "A" and tier != "A"):
                continue
            pd = primary_deadline(dls)
            out.append({
                "id": f"cand:{doc['symbol']}:{doc['call_date']}:{t['i']:03d}-{j:02d}",
                "symbol": doc["symbol"], "call_date": doc["call_date"], "quarter": doc.get("quarter"),
                "source_url": doc.get("source_url"), "speaker": t["speaker"], "speaker_basis": t.get("role_basis"),
                "section": t["section"], "volunteered": t["section"] in ("opening", "closing"),
                "question": q, "sentence": s, "context": ctx, "tier": tier, "score": round(score, 2),
                "signals": sig, "category": category_of(s), "metric_terms": met, "numbers": nums,
                "deadline": pd, "all_deadlines": dls,
            })
    return out


def emit_prompts(cands, outdir, symbol):
    tmpl = open(os.path.join(HERE, "llm_extract_prompt.md")).read()
    os.makedirs(outdir, exist_ok=True)
    by = {}
    for c in cands:
        by.setdefault(c["call_date"], []).append(c)
    paths = []
    for d, cs in sorted(by.items()):
        slim = [{k: c[k] for k in ("id", "speaker", "section", "question", "context", "sentence", "category",
                                   "numbers", "deadline")} for c in cs]
        for s in slim:
            if s["question"]:
                s["question"] = s["question"][:300]
        body = tmpl.replace("{{SYMBOL}}", symbol).replace("{{CALL_DATE}}", d).replace(
            "{{QUARTER}}", cs[0].get("quarter") or "").replace("{{N}}", str(len(cs))).replace(
            "{{CANDIDATES_JSONL}}", "\n".join(json.dumps(s, ensure_ascii=False) for s in slim))
        p = os.path.join(outdir, f"{symbol}_{d}_prompt.md")
        open(p, "w").write(body)
        paths.append(p)
    return paths


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol")
    p.add_argument("--cache")
    p.add_argument("--min-tier", default="B", choices=["A", "B"])
    p.add_argument("--emit-prompts", metavar="DIR")
    a = p.parse_args(argv)
    sym = a.symbol.upper()
    root = C.cache_root(a.cache)
    files = sorted(glob.glob(os.path.join(C.sym_dir(root, sym, "turns"), "*.json")))
    if not files:
        raise SystemExit("no turns; run turns.py first")
    allc = []
    for f in files:
        doc = C.load_json(f)
        cs = extract_call(doc, a.min_tier)
        allc += cs
        na = sum(c["tier"] == "A" for c in cs)
        print(f"{doc.get('quarter')} {doc['call_date']}: {len(cs)} candidates (A {na}, B {len(cs) - na}), "
              f"volunteered {sum(c['volunteered'] for c in cs)}")
    out = os.path.join(C.sym_dir(root, sym), "candidates.jsonl")
    C.write_jsonl(out, allc)
    print("wrote", out, len(allc))
    if a.emit_prompts:
        for pth in emit_prompts(allc, a.emit_prompts, sym):
            print("prompt:", pth)


if __name__ == "__main__":
    main()
