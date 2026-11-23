"""Section finder for Indian annual-report text (pdftotext, reading order, pages split on form feed).
Roadmap stage 3 (signals). Research tool, not SEBI-registered advice.

Each page gets a label from heading-like lines in its first HEAD_LINES non-empty lines (short line, pattern covers
most of it); a page without a heading inherits the previous page's label. A page whose head hits >= 3 different
labels is a contents page (label TOC, resets inheritance). Labels:
  MDA  management discussion and analysis          CG    corporate governance report
  BRSR business responsibility (and sustainability) report   DR  board's / directors' report (incl. annexures)
  AUD  independent auditor's report + its annexures (CARO = Annexure A/B "Companies (Auditor's Report) Order")
  FS   balance sheet / P&L / cash flow / notes     NOT   notice of AGM      SEC secretarial audit report
Sections used: MDA = the longest contiguous run of MDA pages (cap 60 pages). AUD is found in the text, not by page
label: the first "Independent Auditor's Report" heading followed by "To the Members", up to the standalone
"Balance Sheet as at" (or the next report start = consolidated), cap 200k chars; it includes CARO (Annexure A/B).
Standalone comes first in Indian ARs. BRSR pages are never used."""
import re, subprocess

HEAD_LINES = 12
PAT = [
    ("BRSR", r"business\s+responsibility\s*(?:(?:and|&)\s*sustainability)?\s*report(?:ing)?|^brsr$|^section\s*[-–]?\s*a\s*[:\-–]?\s*general\s+disclosures"),
    ("AUD", r"independent\s+auditor['’`s]*\s*report|^annexure\s*[-–]?\s*[ab12i]*\s*(?:to|referred).{0,60}auditor['’`s]*\s*report"),
    ("MDA", r"management['’`s]*\s+discussion\s*(?:and|&)\s*analysis"),
    ("CG", r"(?:report\s+on\s+)?corporate\s+governance(?:\s+report)?$"),
    ("SEC", r"secretarial\s+audit\s+report"),
    ("DR", r"^(?:the\s+)?(?:board['’`s]*|directors['’`s]*)\s+report|^report\s+of\s+(?:the\s+)?(?:board|directors)"),
    ("FS", r"^(?:standalone\s+|consolidated\s+)?(?:balance\s+sheet|statement\s+of\s+profit\s+(?:and|&)\s+loss|"
           r"(?:statement\s+of\s+)?cash\s+flow\s+statement|statement\s+of\s+cash\s+flows?|statement\s+of\s+changes\s+in\s+equity|"
           r"notes\s+(?:forming\s+part\s+of|to)\s+(?:the\s+)?(?:standalone\s+|consolidated\s+)?financial\s+statements)"),
    ("NOT", r"^notice\s+of\s+(?:the\s+)?[\w-]*\s*(?:\(\w+\)\s*)?annual\s+general\s+meeting|^notice\s+is\s+hereby\s+given"),
]
CPAT = [(k, re.compile(p, re.I)) for k, p in PAT]
NEG_AUD = re.compile(r"certificate|compliance\s+with.*corporate\s+governance", re.I)


def pdf_pages(pdf):
    r = subprocess.run(["pdftotext", "-q", pdf, "-"], capture_output=True, timeout=600)
    return r.stdout.decode("utf-8", "replace").split("\f")


def _labels_in_head(page):
    head = [l.strip() for l in page.split("\n") if l.strip()][:HEAD_LINES]
    # headings are often broken over two lines ("BUSINESS RESPONSIBILITY &" / "SUSTAINABILITY REPORT")
    cand = []
    for i, l in enumerate(head):
        cand.append(l)
        if i + 1 < len(head) and len(l) < 60 and len(head[i + 1]) < 60:
            cand.append(l + " " + head[i + 1])
    hits = []
    for l in cand:
        if len(l) > 110:
            continue
        ll = re.sub(r"[\s ]+", " ", l).strip(" .:-–|0123456789")
        for k, rx in CPAT:
            m = rx.search(ll)
            if not m:
                continue
            if k == "AUD" and NEG_AUD.search(ll):
                continue
            # heading-like: pattern covers >= 45% of the line
            if len(m.group(0)) >= 0.45 * max(len(ll), 1):
                hits.append(k)
                break
    return hits


def label_pages(pages):
    out, cur = [], "OTHER"
    for p in pages:
        h = _labels_in_head(p)
        if len(set(h)) >= 3:
            out.append("TOC"); cur = "OTHER"; continue
        if h:
            # prefer a real section start over running headers like FS inside AUD; take the first hit
            cur = h[0]
        out.append(cur)
    return out


AUD_START = re.compile(r"independent\s+auditor['’`s]*\s+report", re.I)
MEMBERS = re.compile(r"to\s+the\s+(?:members|shareholders)", re.I)
AUD_END = re.compile(r"^[ \t■•▪]*(?:standalone\s+)?balance\s+sheet(?:\s+as\s+at[^\n]{0,40})?[ \t]*$|"
                     r"^[ \t■•▪]*statement\s+of\s+assets\s+and\s+liabilities", re.I | re.M)
CARO = re.compile(r"auditor['’`s]*\s+report\s*\)\s*order", re.I)
MAX_AUD, MAX_MDA_PAGES = 200_000, 60


def auditor_section(text):
    """First 'Independent Auditor's Report' heading followed within 1,000 chars by 'To the Members' -> up to the
    first line that is just '(Standalone) Balance Sheet [as at ...]' >= 8,000 chars later, or the next report start (consolidated), cap 200k."""
    for m in AUD_START.finditer(text):
        if not MEMBERS.search(text, m.end(), m.end() + 400):
            continue
        if re.search(r"balance\s+sheet", text[m.end():m.end() + 250], re.I):
            continue                      # contents / divider page ("... Report 136 Standalone Balance Sheet 137")
        st = m.start()
        ends = [x.start() for x in [AUD_END.search(text, st + 8000)] if x]
        for m2 in AUD_START.finditer(text, st + 8000):
            if MEMBERS.search(text, m2.end(), m2.end() + 1000) and not re.search(
                    r"annexure", text[max(0, m2.start() - 120):m2.start()], re.I):
                ends.append(m2.start()); break
        en = min(ends + [st + MAX_AUD])
        return text[st:en]
    return ""


def sections(pages):
    lab = label_pages(pages)
    runs, cur = [], []
    for i, l in enumerate(lab):
        if l == "MDA":
            cur.append(i)
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    mda = max(runs, key=len)[:MAX_MDA_PAGES] if runs else []
    aud = auditor_section("\n".join(pages))
    return {"labels": lab, "MDA": "\n".join(pages[i] for i in mda), "AUD": aud,
            "n_pages": len(pages), "pg_MDA": mda, "caro": bool(CARO.search(aud)),
            "n_BRSR": sum(l == "BRSR" for l in lab), "chars": sum(len(p) for p in pages)}
TOK = re.compile(r"[a-z]{2,}")


def words(t):
    return set(TOK.findall(t.lower()))


def jaccard(a, b):
    A, B = words(a), words(b)
    return len(A & B) / len(A | B) if (A or B) else None
