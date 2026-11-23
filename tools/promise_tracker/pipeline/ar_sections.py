#!/usr/bin/env python3
"""AR mode, stage 2: cut each annual report down to its forward-looking sections and write them as
"turns" in the concall schema, so candidates.py / score.py / report.py run unchanged.

    python3 -I ar_sections.py SUNFLAG [--cache AR_ROOT]          # all reports in the AR manifest
    python3 -I ar_sections.py --txt AR_FY26.txt --print           # one file, ad hoc (shows the zone + blocks)

What is kept (the "zone"): the Chairman's / MD's message, the Board's (Directors') Report body, the
Management Discussion & Analysis, and the energy-conservation / technology-absorption annexure (small companies
list planned machines and capacity there). What is cut: the AGM Notice, every other Annexure (CSR, secretarial audit...), the BRSR, the Corporate Governance Report, auditors' reports and the financial
statements, plus statutory boilerplate paragraphs (Sections/Rules, AGM, directors' appointments, deposits,
vigil mechanism, IEPF...) and the MD&A safe-harbour disclaimer.
Inside the zone, every block becomes one management "turn" with section "opening" (an annual report is
volunteered disclosure; nothing is prompted):
  * prose blocks are reflowed (pdftotext -layout breaks every line) and labelled with the nearest sub-heading
    ("8. PROJECTS", "Sunflag's Performance and Outlook", "Opportunities and Threats"...);
  * tables (status-of-projects / mines / capex tables) are rebuilt row by row: columns are found from the
    whitespace gutters shared by the block's lines, rows start at a serial number (or a filled first column),
    and each row becomes one turn "<name> | <cells> | <status text>" labelled with the row's name cell, so
    the asset name travels with its status sentence.
  * `focus` = True when the sub-heading is one the task cares about: state of affairs, outlook, future,
    opportunities, projects, expansion, capex, mines, commissioning, strategy.
Text normalisation (recorded in the turn as `normalised`; the raw block is kept in `raw`): Indian fiscal
years written "FY 2026-27" / "financial year 2026-27" / "2026-27" become "FY27"; "Sep-2026" / "Sept. 2026" /
"Sep'26" become "September 2026"; "Q3 of FY 2026-27" becomes "Q3FY27". candidates.py would otherwise read
"FY 2026-27" as FY26 and miss abbreviated months.
Output: <ar_root>/<SYMBOL>/turns/<submission date>.json (same schema as turns.py, plus `ar_sections`).
"""
import argparse
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C  # noqa: E402
from turns import SAFE_HARBOUR  # noqa: E402

START_RX = re.compile(r"conservation\s+of\s+energy|technology\s+absorption|board'?s?['’]?\s+report|directors['’]?\s*report|management['’]?s?\s+discussion|"
                      r"chair(?:man|person)['’]?s?\s+(?:message|speech|letter|statement|communiqu\w+|desk|address|review)|"
                      r"message\s+from|from\s+the\s+chair(?:man|person)|letter\s+to\s+(the\s+)?(share|stake)holders|"
                      r"managing\s+director['’]?s?\s+(message|desk|letter)|from\s+the\s+desk|md['’]?s\s+(message|desk)", re.I)
STOP_RX = re.compile(r"\bnotice\b|annexure|business\s+responsibility|corporate\s+governance|auditor|"
                     r"financial\s+statements|balance\s+sheet|statement\s+of\s+profit|secretarial|form\s+no|"
                     r"corporate\s+social|\bCSR\b|sustainability\s+report|esg\s+report|integrated\s+report\s+framework|"
                     r"cash\s+flow\s+statement|notes\s+to|significant\s+accounting|general\s+shareholder|"
                     r"route\s+map|proxy\s+form|attendance\s+slip|dividend\s+distribution\s+policy", re.I)
FOCUS_RX = re.compile(r"state\s+of\s+(the\s+)?(company['’]?s?\s+)?affairs|outlook|future|prospect|opportunit|project|"
                      r"expansion|capex|capital\s+expenditure|mine|mining|commission|strategy|strategic|plan|"
                      r"growth|capacity|new\s+(plant|unit|facility|product)|performance|operations|business\s+review|"
                      r"way\s+forward|road\s?map|initiatives|developments|threats|order\s+book|investments?", re.I)
BOILER_RX = re.compile(
    r"\bSection\s+\d+|\bRegulation\s+\d+|\bRule\s+\d+|Companies\s+Act|Listing\s+Regulations|annual\s+general\s+meeting|"
    r"\bAGM\b|retire[sd]?\s+by\s+rotation|re-?appoint|independent\s+director|key\s+managerial|vigil\s+mechanism|"
    r"whistle|public\s+deposits|IEPF|investor\s+education|unclaimed|e-?voting|secretarial\s+standard|cost\s+audit|"
    r"statutory\s+auditor|internal\s+financial\s+control|related\s+party\s+transactions?\s+(entered|were)|"
    r"sexual\s+harassment|insolvency\s+and\s+bankruptcy\s+code|one[\s-]time\s+settlement|"
    r"directors['’]?\s+responsibility|going\s+concern\s+basis|annual\s+return|extract\s+of|"
    r"board\s+evaluation|familiari[sz]ation|nomination\s+and\s+remuneration|maternity\s+benefit|"
    r"particulars\s+of\s+(loans|employees)|ratio\s+of\s+(the\s+)?remuneration|"
    r"acknowledg(e)?ment|place\s*:|for\s+and\s+on\s+behalf", re.I)
PROJECT_RX = re.compile(r"project|plant|capacity|expan|commission|mine|block|capex|greenfield|brownfield|"
                        r"clearance|lease|facility|unit\b|line\b|launch|order|acqui|target|expected|likely|by\s+FY", re.I)

MON3 = {"jan": "January", "feb": "February", "mar": "March", "apr": "April", "may": "May", "jun": "June",
        "jul": "July", "aug": "August", "sep": "September", "oct": "October", "nov": "November", "dec": "December"}


def normalise(t):
    """FY 2026-27 -> FY27; Sep-2026 -> September 2026; Q3 of FY 2026-27 -> Q3FY27 (see module doc)."""
    def fy(m):
        a, b = int(m.group("a")), int(m.group("b"))
        if (a + 1) % 100 != b % 100:
            return m.group(0)
        return f"FY{b % 100:02d}"
    t = re.sub(r"\b(Q[1-4]|H[12])\s*(?:of\s+)?(?:the\s+)?(?:FY|F\.Y\.|financial\s+year|fiscal(?:\s+year)?)\s*"
               r"'?20(?P<a>\d\d)\s*[-–/]\s*(?:20)?(?P<b>\d\d)\b",
               lambda m: (m.group(1).upper() + fy(m)) if fy(m).startswith("FY") else m.group(0), t, flags=re.I)
    t = re.sub(r"\b(?:FY|F\.Y\.|financial\s+year|fiscal(?:\s+year)?)\s*'?20(?P<a>\d\d)\s*[-–/]\s*(?:20)?(?P<b>\d\d)\b",
               fy, t, flags=re.I)
    t = re.sub(r"(?<![\d.\-/])20(?P<a>\d\d)\s?[-–]\s?(?P<b>\d\d)(?![\d.\-/%])", fy, t)
    t = re.sub(r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|"
               r"Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?"
               r"(?:\s?[-'’]\s?(20\d\d|\d\d)|[ ,]{1,2}(20\d\d))\b(?![\d,/]|\.\d)",
               lambda m: MON3[m.group(1)[:3].lower()] + " " + ((m.group(2) or m.group(3)) if len(m.group(2) or m.group(3)) == 4
                                                               else "20" + m.group(2)),
               t)
    t = re.sub(r"\b(first|second|third|fourth|1st|2nd|3rd|4th)\s+(quarter|half)\s+of\s+(?:the\s+)?FY\s?(\d\d)\b",
               lambda m: ("Q" if m.group(2).lower() == "quarter" else "H") +
               str({"fir": 1, "1st": 1, "sec": 2, "2nd": 2, "thi": 3, "3rd": 3, "fou": 4, "4th": 4}[m.group(1).lower()[:3]]) +
               "FY" + m.group(3), t, flags=re.I)
    return t


# ------------------------------------------------------------------ zone
def is_heading(line):
    s = line.strip()
    if not (3 <= len(s) <= 90) or re.search(r"\s\d{1,3}$", s):   # TOC rows end in a page number
        return False
    letters = [c for c in s if c.isalpha()]
    if len(letters) < 4:
        return False
    up = sum(c.isupper() for c in letters) / len(letters)
    lead = len(line) - len(line.lstrip())
    return up >= 0.75 or (lead >= 25 and len(s) <= 60 and not s.endswith((".", ",")))


def major_heading(line):
    """Report-level heading: a short stand-alone line in UPPER or Title Case, not a numbered item inside a
    report ("19. AUDITORS"), not a TOC row (no wide gaps, no page number)."""
    s = line.strip()
    if not (3 <= len(s) <= 70) or re.search(r"\S {3,}\S", s) or re.search(r"\s\d{1,3}$", s):
        return False
    if re.match(r"^(\d{1,2}|[ivxIVX]{1,4}|[a-hA-H])[\.\)]\s", s) or len(s.split()) > 10 or s.endswith((".", ",")):
        return False
    letters = [c for c in s if c.isalpha()]
    if len(letters) < 4:
        return False
    if sum(c.isupper() for c in letters) / len(letters) >= 0.75:
        return True
    long_w = [x for x in s.split() if len(re.sub(r"\W", "", x)) >= 4]
    return bool(long_w) and sum(x[:1].isupper() for x in long_w) / len(long_w) >= 0.6


def find_zone(lines, top=None):
    """Return [(start, end, label)] line spans inside the forward-looking zone. Report-level sections start on a
    new page, so with `top` (indices of the first lines of each page) only headings there count; this stops a
    "CORPORATE GOVERNANCE REPORT" sub-item inside a two-column Directors' Report from closing the zone."""
    spans, cur, label = [], None, None
    for i, ln in enumerate(lines):
        if (top is not None and i not in top) or not major_heading(ln):
            continue
        s = ln.strip()
        if STOP_RX.search(s) and not re.search(r"management['’]?s?\s+discussion|conservation\s+of\s+energy|"
                                               r"technology\s+absorption", s, re.I):
            if cur is not None:
                spans.append((cur, i, label))
                cur = None
        elif START_RX.search(s) and not re.search(r"\bto\s+the\b|forms?\s+part|^(mr|ms|mrs|dr|shri|smt)\b", s, re.I):
            if cur is not None and re.sub(r"^\s*\d+\.\s*", "", s).title() == label:
                continue   # running page header ("Directors' Report" on every page)
            if cur is not None:
                spans.append((cur, i, label))
            cur, label = i, re.sub(r"^\s*\d+\.\s*", "", s).title()
    if cur is not None:
        spans.append((cur, len(lines), label))
    # a START heading quoted in running text produces tiny spans; keep spans of >= 15 lines
    spans = [s for s in spans if s[1] - s[0] >= 15]
    return spans


# ------------------------------------------------------------------ two-column pages
def split_columns(page):
    """If >= 35% of a page's long lines have a second text run starting at the same column (after a gap of
    4+ spaces, between columns 30 and 110), the page is set in two columns: return the left column's lines
    followed by the right column's lines. Tables (whose left parts are themselves gappy) are left alone."""
    lines = page.split("\n")
    long_lines = [ln for ln in lines if len(ln.strip()) > 40]
    if len(long_lines) < 8:
        return lines
    cand = Counter()
    for ln in lines:
        for m in re.finditer(r"\S( {4,})\S", ln):
            if 30 <= m.end(1) <= 110:
                cand[m.end(1)] += 1
    if not cand:
        return lines
    best = max(cand, key=lambda c: cand[c] + cand.get(c - 1, 0) + cand.get(c + 1, 0))
    n = cand[best] + cand.get(best - 1, 0) + cand.get(best + 1, 0)
    if n < 0.35 * len(long_lines):
        return lines
    cut = best - 1
    lefts, rights, split_left = [], [], []
    for ln in lines:
        if len(ln) > cut + 1 and ln[cut - 1:cut + 1].strip() == "" and ln[cut - 1:].strip():
            split_left.append(ln[:cut])
            k = cut - 1
            while k < len(ln) and ln[k] == " ":
                k += 1
            lefts.append(ln[:cut].rstrip())
            rights.append(ln[k:])
        elif len(ln) > cut + 1 and ln[:cut].strip() == "":
            lefts.append("")
            rights.append(ln.strip())
        else:
            lefts.append(ln)
            rights.append("")
    # a table (status of mines, financial summary) also has an aligned column: its left parts are gappy too
    multi = sum(1 for x in split_left if re.search(r"\S {3,}\S", x.strip()))
    if multi >= 3 and multi > 0.1 * len(split_left):
        return lines
    return lefts + [""] + rights


# ------------------------------------------------------------------ blocks
def is_tabular(ln):
    return bool(re.search(r"\S {3,}\S", ln.strip()))


SERIAL_RX = re.compile(r"(\d{1,2}|[ivx]{1,4}|[a-h])[\.\)]?", re.I)


def rebuild_table(rows):
    """Lines of one table block -> list of (name, row_text).
    Each line is cut into chunks at runs of >= 3 spaces (so words are never split); chunk start positions are
    clustered into columns (tolerance 3 chars); a chunk belongs to the nearest column on its left. A row starts
    at a serial-number chunk in the leftmost column (or, in tables without serials, at a filled first column)."""
    rows = [r.rstrip() for r in rows if r.strip()]
    if not rows:
        return []
    chunked = []
    for r in rows:
        ch = []
        for m in re.finditer(r"\S+(?: {1,2}\S+)*", r):
            sm = re.match(r"((?:\d{1,2}|[ivx]{1,4})[\.\)]?)( {1,2})(?=[A-Z(])", m.group(0)) if not ch else None
            if sm:   # "9 Surjagad 6 Iron ore Block": serial glued to the name cell
                ch.append((m.start(), sm.group(1)))
                ch.append((m.start() + sm.end(), m.group(0)[sm.end():]))
            else:
                ch.append((m.start(), m.group(0)))
        chunked.append(ch)
    starts = sorted(st for ch in chunked for st, _ in ch)
    cols = []
    for st in starts:
        if cols and st - cols[-1][-1] <= 3:
            cols[-1].append(st)
        else:
            cols.append([st])
    cols = [min(c) for c in cols if len(c) >= 2] or [0]
    if len(cols) < 2:
        return [("", re.sub(r"\s{2,}", " ", " ".join(r.strip() for r in rows)))]

    def col_of(st):
        k = 0
        for i, c in enumerate(cols):
            if c <= st + 3:
                k = i
        return k
    left = min(st for ch in chunked for st, _ in ch)
    serial = sum(1 for ch in chunked if len(ch) > 1 and ch[0][0] <= left + 12 and SERIAL_RX.fullmatch(ch[0][1]))
    out, cur = [], None
    for ch in chunked:
        if not ch:
            continue
        first = ch[0]
        if serial >= 2:
            starts_row = len(ch) > 1 and first[0] <= left + 12 and bool(SERIAL_RX.fullmatch(first[1]))
        else:
            starts_row = col_of(first[0]) == 0
        if starts_row or cur is None:
            cur = {}
            out.append(cur)
        for st, txt in ch:
            cur.setdefault(col_of(st), []).append(txt)
    res = []
    for row in out:
        cells = [re.sub(r"\s+", " ", " ".join(row[k])).strip() for k in sorted(row)]
        name = next((c for c in cells if c and not re.fullmatch(r"[\divx\.\)\(a-h]+", c, re.I)), "")
        res.append((name[:120], " | ".join(c for c in cells if c)))
    return res


def heading_line(ln):
    """A sub-heading inside the zone: short, no closing punctuation, and either upper case, numbered
    ("8. PROJECTS", "b) Opportunities"), or Title Case ("Sunflag's Performance and Outlook")."""
    s = ln.strip()
    w = s.split()
    if not (1 <= len(w) <= 12) or len(s) > 80 or s.endswith((".", ",", ";", ":-")) or not s[:1].isalnum():
        return False
    if is_heading(ln):
        return True
    if re.match(r"^(\d{1,2}|[ivx]{1,4}|[a-h])[\.\)]\s+[A-Z]", s) and len(w) <= 10:
        return True
    long_w = [x for x in w if len(re.sub(r"\W", "", x)) >= 4]
    return len(w) <= 8 and s[:1].isupper() and bool(long_w) and \
        sum(x[:1].isupper() for x in long_w) / len(long_w) >= 0.6 and not re.search(r"\d{3,}", s)


def blocks(lines):
    """Zone lines -> [(kind, label, text, raw)] with kind 'prose'|'row'|'heading'."""
    out, buf, tab, label = [], [], [], None

    def flush_prose():
        if buf:
            raw = "\n".join(buf)
            txt = re.sub(r"\s+", " ", " ".join(x.strip() for x in buf)).strip()
            txt = re.sub(r"(\w)- (\w)", r"\1\2", txt) if re.search(r"\w- \w", txt) else txt
            out.append(("prose", label, txt, raw))
            buf.clear()

    def flush_tab():
        if tab:
            if sum(1 for x in tab if x.strip()) <= 1:   # one stray line with a wide space: prose
                buf.extend(x for x in tab if x.strip())
            else:
                flush_prose()
                for name, txt in rebuild_table(tab):
                    out.append(("row", name or label, txt, "\n".join(tab)))
            tab.clear()

    def table_continues(i):
        """the next few non-blank lines are still table-like (wrapped cells of the same table)"""
        nxt = [x for x in lines[i + 1:i + 6] if x.strip()][:3]
        return any(is_tabular(x) or len(x) - len(x.lstrip()) >= 20 for x in nxt)

    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s:
            if tab:
                tab.append(ln)   # blank lines inside a table are common
            continue
        if re.fullmatch(r"\d{1,3}|page \d+.*", s, re.I):   # page numbers
            continue
        if is_tabular(ln):
            if buf and not tab:
                flush_prose()
            tab.append(ln)
            continue
        if tab:
            # a non-tabular line right after table rows may be a wrapped cell: keep it in the table if indented
            if len(ln) - len(ln.lstrip()) >= 20 or (len(s) < 60 and table_continues(i)):
                tab.append(ln)
                continue
            flush_tab()
        if heading_line(ln):
            flush_prose()
            label = re.sub(r"^\s*(\d{1,2}|[ivx]{1,4}|[a-h])[\.\)]\s*", "", s).strip(" :-")
            out.append(("heading", label, s, s))
            continue
        buf.append(ln)
    flush_tab()
    flush_prose()
    return out


def keep_block(kind, label, text):
    if kind == "heading" or len(text.split()) < 6:
        return False
    if SAFE_HARBOUR.search(text) and re.search(r"forward|projection|estimate", text, re.I):
        return False
    if BOILER_RX.search(text) and not PROJECT_RX.search(text):
        return False
    return True


def doc_turns(text):
    """Full AR text -> (turns, sections, zone_found)."""
    pages = text.split("\f")
    lines, top = [], set()
    for pg in pages:
        pl = split_columns(pg)
        nb = [k for k, x in enumerate(pl) if x.strip()][:8]
        top |= {len(lines) + k for k in nb}
        lines += pl
    spans = find_zone(lines, top)
    zone_found = sum(b - a for a, b, _ in spans) >= 300
    if not zone_found:
        spans = find_zone(lines)
        zone_found = sum(b - a for a, b, _ in spans) >= 300
    if not zone_found:   # fallback: everything before the auditors' report, minus the Notice
        end = next((i for i, ln in enumerate(lines) if is_heading(ln) and re.search(r"auditor", ln, re.I)
                    and i > 200), len(lines))
        spans = [(0, end, "Annual report (no section headings found)")]
    turns, secs = [], []
    for a, b, sec in spans:
        bl = blocks(lines[a + 1:b])
        kept = 0
        for kind, label, txt, raw in bl:
            if not keep_block(kind, label, txt):
                continue
            ntxt = normalise(txt)
            speaker = sec or "Annual report"
            turns.append({"i": len(turns), "label": label or sec, "speaker": f"{speaker} (annual report)",
                          "role": "management", "section": "opening", "text": ntxt, "raw": raw[:4000],
                          "normalised": ntxt != txt, "kind": kind, "ar_section": sec,
                          "focus": bool(FOCUS_RX.search(label or "")) or kind == "row",
                          "question_i": None, "analyst_firm": None, "role_basis": "ar-section"})
            kept += 1
        secs.append({"section": sec, "start_line": a, "end_line": b, "blocks": len(bl), "kept": kept})
    return turns, secs, zone_found


def process_symbol(sym, root):
    man = C.load_json(os.path.join(C.sym_dir(root, sym), "manifest.json"), [])
    if not man:
        raise SystemExit("no AR manifest; run ar_fetch.py first")
    tdir = C.sym_dir(root, sym, "turns")
    for m in man:
        if m.get("skip"):
            print(f"skip {m['quarter']} {m['file']}: scanned/too short")
            continue
        text = open(m["txt"], errors="replace").read()
        turns, secs, ok = doc_turns(text)
        doc = {"symbol": sym, "call_date": m["call_date"], "quarter": m["quarter"], "source_url": m["url"],
               "roster": [], "company_roster": [], "turns": turns, "label_report": {}, "mode": "annual_report",
               "doc_kind": m.get("kind"), "ar_sections": secs, "zone_found": ok}
        C.save_json(os.path.join(tdir, m["call_date"] + ".json"), doc)
        words = sum(len(t["text"].split()) for t in turns)
        print(f"{m['quarter']} {m['call_date']}: zone {'ok' if ok else 'NOT FOUND (fallback)'}; "
              f"{len(secs)} sections; {len(turns)} blocks kept ({sum(t['kind'] == 'row' for t in turns)} table rows), "
              f"{words} words of {m['words']} ({100 * words / max(1, m['words']):.0f}%)")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol", nargs="?")
    p.add_argument("--cache", help="AR-mode cache root (default $PT_CACHE/ar)")
    p.add_argument("--txt")
    p.add_argument("--print", action="store_true")
    a = p.parse_args(argv)
    if a.txt:
        turns, secs, ok = doc_turns(open(a.txt, errors="replace").read())
        for s in secs:
            print("SECTION", s)
        if a.print:
            for t in turns:
                print(f"[{t['i']}] {t['kind']} <{t['label']}>{' *' if t['focus'] else ''} {t['text'][:400]}\n")
        return
    if not a.symbol:
        p.error("symbol or --txt required")
    import ar_fetch
    process_symbol(a.symbol.upper(), ar_fetch.ar_root(a.cache))


if __name__ == "__main__":
    main()
