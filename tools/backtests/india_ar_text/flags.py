"""Auditor-section adverse-item detector (pre-registered H3). Keyword in a sentence WITHOUT a negator in that
sentence. Current vs prior year: a category is NEW if it has >= 1 hit now and none last year. Every new hit is
then checked by hand (s3 writes the sentences to auditor_flags.tsv). Research tool, not SEBI-registered advice."""
import re

NEG = re.compile(r"\b(?:no|not|nil|none|neither|nor|without|never)\b|n't", re.I)
CATS = {
    "EOM": r"emphasis\s+of\s+matters?",
    "QUAL": r"(?<!un)qualified\s+(?:opinion|conclusion)|adverse\s+opinion|disclaimer\s+of\s+opinion|"
            r"do\s+not\s+express\s+an\s+opinion",
    "MUGC": r"material\s+uncertainty\s+relat\w*\s+to\s+going\s+concern",
    "ICFR_MW": r"material\s+weakness(?:es)?\s+(?:has|have)\s+been\s+identified|following\s+material\s+weakness",
    "DEFAULT": r"(?:has|have)\s+(?:been\s+)?default(?:ed)?\s+in\s+(?:the\s+)?(?:repayment|payment)",
    "CASHLOSS": r"(?:has|have)\s+incurred\s+cash\s+loss",
    "AUD_RESIGN": r"resignation\s+of\s+(?:the\s+)?statutory\s+auditor",
    "ST_LT": r"short[\s-]term\s+basis\s+(?:have|has)\s+been\s+used\s+for\s+long[\s-]term",
    "CARO_GC": r"material\s+uncertainty\s+exists\s+as\s+on\s+the\s+date\s+of\s+the\s+audit\s+report",
    "FRAUD": r"fraud\s+(?:by|on)\s+the\s+company[^.;]{0,60}(?:has|have)\s+been\s+noticed|"
             r"(?:following|instances?\s+of)\s+fraud",
    "DUES": r"(?:following|below)\s+(?:undisputed\s+)?(?:statutory\s+)?dues[^.;]{0,120}(?:arrears|outstanding)[^.;]{0,80}"
            r"(?:more\s+than|exceeding)\s+six\s+months",
}
CRX = {k: re.compile(v, re.I) for k, v in CATS.items()}
# negators allowed in these categories' own phrase (they are part of the adverse wording)
NEG_OK = {"QUAL": re.compile(r"do\s+not\s+express", re.I)}


def sentences(t):
    t = re.sub(r"\s+", " ", t)
    return re.split(r"(?<=[.;:])\s+(?=[A-Z(\[])", t)


def hits(text):
    out = {}
    for s in sentences(text or ""):
        for k, rx in CRX.items():
            m = rx.search(s)
            if not m:
                continue
            s2 = NEG_OK[k].sub("", s) if k in NEG_OK else s
            if NEG.search(s2):
                continue
            # boilerplate: "whether a material uncertainty exists", "if we conclude that"
            if re.search(r"\bwhether\b|\bif\s+(?:we|our)\b|\bin\s+the\s+event\b|\bsuch\s+as\b", s, re.I):
                continue
            out.setdefault(k, []).append(s[:600])
    return out


def new_items(cur, prior):
    hc, hp = hits(cur), hits(prior)
    return {k: v for k, v in hc.items() if k not in hp}
