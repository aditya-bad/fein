#!/usr/bin/env python3
"""Stage 2: split transcript text into speaker turns.

    python3 -I turns.py SYMBOL [--cache DIR] [--roster "Name A,Name B"]   # all calls in manifest
    python3 -I turns.py --txt file.txt [--print]                          # one file, ad hoc

Output per call: <cache>/<SYMBOL>/turns/<call_date>.json
    {"symbol","call_date","quarter","source_url","roster":[{name,role}],
     "turns":[{"i","label","speaker","role","section","text","question_i","analyst_firm","role_basis"}],
     "label_report":{label: {"role","n","basis"}}}

role    = management | analyst | moderator | host
section = opening (management before the first question = volunteered)
          qa      (answers to analysts = prompted)
          closing (management after the moderator asks for closing remarks = volunteered)

Unreliable labels (pilot lesson): pdftotext labels come as "Paramjit Soni", "Parmjit Soni",
"Paramjit Sonis", "Management", "Aditya Dujari :" etc.  Roles are decided in this order:
  1. the cover-page MANAGEMENT roster, unioned over every call of the company (+ --roster,
     + rosters.json next to this script), fuzzy-matched (difflib) on full name / surname;
  2. generic labels ("Management", "Company", "Speaker") -> management;
  3. names the moderator announces ("next question is from the line of X from Y") -> analyst;
  4. anything else: content vote (questions vs "we/our" answers, position after a question).
`role_basis` records which rule fired so a reviewer can audit it.
Boilerplate removed: cover letter, page headers/footers (repeated lines, "Page n of m"),
safe-harbour / forward-looking-statement disclaimers, operator housekeeping.
"""
import argparse
import difflib
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

LABEL_RX = re.compile(r"^\s{0,8}([A-Z][A-Za-z\.\'’\-]*(?:\s+[A-Z][A-Za-z\.\'’\-]*){0,4})\s*:\s?(.*)$")
NOT_LABELS = {"tel", "subject", "scrip code", "regd. office", "corporate office", "date", "dn", "encl",
              "cin", "dated", "email", "e-mail", "website", "phone", "fax", "symbol", "note", "registered office",
              "management", "moderator", "isin", "web", "mobile", "ph", "for", "nse", "bse", "address",
              "regd office", "kind attn", "attn", "ref", "url", "q", "a", "and", "the", "also", "so", "but"}
GENERIC_MGMT = {"management", "company", "speaker", "company speaker", "company management",
                "unidentified company speaker", "unknown speaker"}
HONORIFIC = re.compile(r"^(mr|ms|mrs|dr|shri|smt|prof|ca)\.?\s+", re.I)
SAFE_HARBOUR = re.compile(
    r"forward[\s-]+looking|safe[\s-]+harbou?r|risks? and uncertaint|actual results (may|might|could) differ|"
    r"undertake no obligation|does not undertake|not (be )?construed|disclaimer|"
    r"listen[\s-]+only mode|press(ing)? star then|touch[\s-]?tone|conference is being recorded|"
    r"signal an operator", re.I)
ANNOUNCE_RX = re.compile(
    r"(?:question|questions|follow[\s-]up)\s+(?:is\s+|comes\s+)?(?:from|on)\s+(?:the\s+line\s+of\s+)?"
    r"(?:Mr\.?|Ms\.?|Mrs\.?|Dr\.?)?\s*([A-Z][A-Za-z\.\'’]+(?:\s+[A-Z][A-Za-z\.\'’]+){0,3})"
    r"(?:\s+(?:from|of|with)\s+([A-Z][A-Za-z&\.\'’ ]{1,60}?))?(?:[\.,]|\s+(?:Please|please|Go|go)\b|$)")
CLOSING_RX = re.compile(r"closing (comments|remarks|statement|thoughts)|concluding (comments|remarks)|"
                        r"last question|hand the (conference|call|floor) (back|over) to the management for", re.I)
HANDOVER_RX = re.compile(r"(hand|handing|turn) (the )?(call|conference|floor|it) over|over to you", re.I)
FIRST_Q_RX = re.compile(r"(first|next) question|question[\s-]and[\s-]answer session|begin the q", re.I)

HERE = os.path.dirname(os.path.abspath(__file__))


def norm_name(s):
    s = HONORIFIC.sub("", s.strip().strip(".:").strip())
    s = re.sub(r"\s+", " ", s)
    return s.title()


def parse_roster(text):
    """Names in the cover-page 'MANAGEMENT:' block (until MODERATOR/ANALYST/first label)."""
    m = re.search(r"^\s*(?:MANAGEMENT|COMPANY PARTICIPANTS|SPEAKERS?|PANELISTS?)\s*:?(.*?)"
                  r"^\s*(?:MODERATOR|ANALYSTS?|HOSTS?|Moderator)\s*:", text[:20000], re.S | re.M)
    if not m:
        return []
    block = re.sub(r"\s+", " ", m.group(1))
    out = []
    for piece in re.split(r"\b(?:MR|MS|MRS|DR|SHRI|SMT|PROF)\.?\s+", block):
        piece = piece.strip(" ,;")
        if not piece:
            continue
        parts = re.split(r"\s*[–—]\s*|\s+-\s+|,\s+", piece, maxsplit=1)
        name = norm_name(parts[0])
        role = parts[1].strip(" –—-") if len(parts) > 1 else ""
        if 1 <= len(name.split()) <= 5 and len(name) < 45 and not re.search(r"\d", name):
            out.append({"name": name, "role": role.title()[:80]})
    return out


def extra_roster(symbol):
    path = os.path.join(HERE, "rosters.json")
    d = C.load_json(path, {}) or {}
    return [{"name": n, "role": "(rosters.json)"} for n in d.get((symbol or "").upper(), [])]


def name_match(label, names):
    """Fuzzy match a speaker label to a list of full names. Returns (name, score) or (None, 0)."""
    lab = norm_name(re.sub(r"[’']s?$", "", label)).lower()
    lt = lab.split()
    best, bs = None, 0.0
    for n in names:
        nl = n.lower()
        nt = nl.split()
        r = difflib.SequenceMatcher(None, lab, nl).ratio()
        if len(lt) == 1:  # single-token label: equal (fuzzy) to a first or last name
            r = max(r, max(difflib.SequenceMatcher(None, lt[0], t).ratio() for t in nt) - 0.05)
        elif len(nt) >= 2:
            # surname + first name similar (handles 'Parmjit Soni', 'Paramjit Sonis', dropped middle name)
            sur = difflib.SequenceMatcher(None, lt[-1], nt[-1]).ratio()
            first = difflib.SequenceMatcher(None, lt[0], nt[0]).ratio()
            if sur >= 0.8 and first >= 0.7:
                r = max(r, (sur + first) / 2)
        if r > bs:
            best, bs = n, r
    return (best, bs) if bs >= 0.8 else (None, bs)


def canonical(name, names):
    """'Paramjit Soni' -> 'Paramjit Singh Soni' when both are in the roster."""
    t = name.lower().split()
    longer = [n for n in names if len(n.split()) > len(t) and n.lower().split()[0] == t[0]
              and n.lower().split()[-1] == t[-1]]
    return max(longer, key=len) if longer else name


def clean_lines(text):
    lines = text.replace("\f", "\n").split("\n")
    stripped = [ln.strip() for ln in lines]
    cnt = Counter(s for s in stripped if s)
    out = []
    for ln, s in zip(lines, stripped):
        if not s:
            out.append("")
            continue
        if re.fullmatch(r"(Page\s*)?\d+\s*(of\s*\d+)?|Page \d+", s, re.I):
            continue
        # repeated short header/footer lines (company name, call date, logo garbage)
        if cnt[s] >= 3 and len(s.split()) <= 9 and not LABEL_RX.match(ln):
            continue
        if len(s) <= 3 and not re.search(r"[a-z]{2}", s):
            continue
        out.append(ln)
    return out


def join_text(parts):
    t = ""
    for p in parts:
        p = p.strip()
        if not p:
            if t and not t.endswith("\n"):
                t += "\n"
            continue
        if t.endswith("-") and p[:1].islower():
            t = t[:-1] + p
        elif not t or t.endswith("\n"):
            t += p
        else:
            t += " " + p
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


def strip_safe_harbour(t):
    sents = re.split(r"(?<=[\.\?!])\s+(?=[A-Z“\"])", t)
    keep = [s for s in sents if not SAFE_HARBOUR.search(s)]
    return " ".join(keep).strip(), len(sents) - len(keep)


def raw_turns(text):
    lines = clean_lines(text)
    # body starts at the first 'Moderator:' (or first label after the roster block)
    start = next((i for i, ln in enumerate(lines) if re.match(r"^\s{0,8}Moderator\s*:", ln)), None)
    if start is None:
        start = next((i for i, ln in enumerate(lines) if re.match(r"^\s{0,8}Operator\s*:", ln)), 0)
    turns, cur, buf = [], None, []
    for ln in lines[start:]:
        m = LABEL_RX.match(ln)
        ok = False
        if m:
            lab = m.group(1).strip()
            low = lab.lower().rstrip(".")
            words = lab.split()
            ok = (low not in NOT_LABELS or low in ("management", "moderator")) and len(lab) <= 40 \
                and len(words) <= 5 and not lab.isupper() or low in ("moderator", "management")
            # a real label starts the line near column 0 and is followed by wide spacing or text
            if ok and len(ln) - len(ln.lstrip()) > 4:
                ok = False
        if ok:
            if cur is not None:
                turns.append((cur, join_text(buf)))
            cur, buf = m.group(1).strip(), [m.group(2)]
        else:
            buf.append(ln)
    if cur is not None:
        turns.append((cur, join_text(buf)))
    return [(lab, txt) for lab, txt in turns if txt]


def qness(t):
    """>0 looks like a question, <0 looks like an answer."""
    tl = t.lower()
    q = t.count("?") * 2 + len(re.findall(r"\b(my (first |next |last |second )?question|could you|can you|"
                                         r"would you|just wanted to|wanted to understand|what is the|how do you|"
                                         r"congratulations|thank you for the opportunity)\b", tl))
    a = len(re.findall(r"\b(we|our|us)\b", tl)) / 4 + len(re.findall(r"\b(yes|no|so,? basically|see,)\b", tl[:60]))
    return q - a


def split_turns(text, roster_names, symbol=None):
    rt = raw_turns(text)
    labels = Counter(lab for lab, _ in rt)
    announced = {}  # analyst name -> firm
    for lab, t in rt:
        if lab.lower().startswith("moderator") or lab.lower() == "operator":
            for m in ANNOUNCE_RX.finditer(t):
                announced[norm_name(m.group(1))] = (m.group(2) or "").strip()
    # roles per label
    role_of, basis_of, speaker_of = {}, {}, {}
    for lab in labels:
        low = norm_name(lab).lower()
        if low in ("moderator", "operator"):
            role_of[lab], basis_of[lab], speaker_of[lab] = "moderator", "label", "Moderator"
            continue
        if low in GENERIC_MGMT:
            role_of[lab], basis_of[lab], speaker_of[lab] = "management", "generic-label", "Management (unnamed)"
            continue
        n, sc = name_match(lab, roster_names)
        n = canonical(n, roster_names) if n else n
        an, asc = name_match(lab, list(announced))
        if n and (not an or sc >= asc):
            role_of[lab], basis_of[lab], speaker_of[lab] = "management", f"roster~{sc:.2f}", n
        elif an:
            role_of[lab], basis_of[lab], speaker_of[lab] = "analyst", f"announced~{asc:.2f}", an
        else:
            role_of[lab], basis_of[lab], speaker_of[lab] = None, None, norm_name(lab)
    # host broker analyst: introduced by moderator before management speaks ("hand over to Mr. X from ...")
    first_mod = next((t for lab, t in rt if role_of.get(lab) == "moderator"), "")
    for lab in labels:
        if role_of[lab] is None:
            last = norm_name(lab).split()[-1]
            if re.search(r"\b" + re.escape(last) + r"\b", first_mod, re.I) and HANDOVER_RX.search(first_mod):
                role_of[lab], basis_of[lab] = "host", "introduced-by-moderator"
    # content vote for the rest
    for lab in labels:
        if role_of[lab] is None:
            votes = [qness(t) for l2, t in rt if l2 == lab]
            avg = sum(votes) / len(votes)
            role_of[lab] = "analyst" if avg > 0 else "management"
            basis_of[lab] = f"content-vote({avg:+.1f})"
    # build turns with sections
    out, section, seen_q, last_q = [], "opening", False, None
    for i, (lab, t) in enumerate(rt):
        role = role_of[lab]
        if role == "moderator":
            if FIRST_Q_RX.search(t):
                seen_q = True
                section = "qa"
            if seen_q and CLOSING_RX.search(t) and re.search(r"closing|concluding|hand", t, re.I):
                section = "closing"
        if role == "analyst" and section == "opening" and i > 2:
            # an analyst speaking before the moderator announced Q&A
            section, seen_q = "qa", True
        clean, n_sh = strip_safe_harbour(t)
        if not clean:
            continue
        # an unlabelled answer inside an analyst label (label lost): long, we/our heavy, no '?'
        rb = basis_of[lab]
        if role in ("analyst", "management") and section == "opening" and not any(
                o["role"] == "management" for o in out) and re.search(
                r"on behalf of|I welcome|we have with us|hand (it |the call )?over to the management", clean, re.I):
            role, rb = "host", rb + "+override(host-intro)"
        elif role == "analyst" and section == "qa" and qness(clean) < -6 and len(clean) > 600 and "?" not in clean:
            role, rb = "management", rb + "+override(answer-like)"
        rec = {"i": len(out), "label": lab, "speaker": speaker_of[lab], "role": role, "section": section,
               "text": clean, "role_basis": rb}
        if n_sh:
            rec["safe_harbour_sentences_removed"] = n_sh
        if role == "analyst":
            last_q = rec["i"]
            rec["analyst_firm"] = announced.get(speaker_of[lab], "")
        elif role == "management" and section == "qa":
            rec["question_i"] = last_q
        out.append(rec)
    report = {lab: {"role": role_of[lab], "speaker": speaker_of[lab], "n": labels[lab], "basis": basis_of[lab]}
              for lab in labels}
    return out, report


def process_symbol(symbol, root, extra=None):
    sdir = C.sym_dir(root, symbol)
    man = C.load_json(os.path.join(sdir, "manifest.json"), [])
    if not man:
        raise SystemExit("no manifest; run fetch.py first")
    skipped = [m for m in man if m.get("skip")]
    for m in skipped:   # v1.1: cover letters / scanned PDFs produced junk turns ("Re", "Sub") in v1
        print(f"skip {m['quarter']} {m['file']}: " + ("cover letter only" if m.get("cover_letter_only") else "scanned/too short"))
    man = [m for m in man if not m.get("skip")]
    # one call per quarter: prefer a local (website) copy over anything else
    byq = {}
    for m in man:
        if m["quarter"] not in byq or m.get("source") == "local":
            byq[m["quarter"]] = m
    man = sorted(byq.values(), key=lambda m: m["call_date"])
    texts = {m["file"]: open(m["txt"], errors="replace").read() for m in man}
    roster = []
    for m in man:
        for r in parse_roster(texts[m["file"]]):
            if r["name"] not in [x["name"] for x in roster]:
                roster.append(r)
    roster += extra_roster(symbol)
    roster += [{"name": norm_name(n), "role": "(--roster)"} for n in (extra or []) if n.strip()]
    names = [r["name"] for r in roster]
    tdir = C.sym_dir(root, symbol, "turns")
    for m in man:
        turns, rep = split_turns(texts[m["file"]], names, symbol)
        call_roster = parse_roster(texts[m["file"]])
        doc = {"symbol": symbol, "call_date": m["call_date"], "quarter": m["quarter"], "source_url": m["url"],
               "roster": call_roster, "company_roster": roster, "turns": turns, "label_report": rep}
        C.save_json(os.path.join(tdir, m["call_date"] + ".json"), doc)
        roles = Counter(t["role"] for t in turns)
        secs = Counter(t["section"] for t in turns if t["role"] == "management")
        inferred = [f"{lab}->{v['role']}({v['basis']})" for lab, v in rep.items()
                    if v["basis"] and not v["basis"].startswith(("roster", "announced", "label"))]
        print(f"{m['quarter']} {m['call_date']}: {len(turns)} turns {dict(roles)} mgmt-sections {dict(secs)}"
              + (f"\n    inferred: {', '.join(inferred)}" if inferred else ""))
    print("roster:", "; ".join(names))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol", nargs="?")
    p.add_argument("--cache")
    p.add_argument("--txt")
    p.add_argument("--roster", help="comma-separated extra management names")
    p.add_argument("--print", action="store_true")
    a = p.parse_args(argv)
    extra = (a.roster or "").split(",") if a.roster else []
    if a.txt:
        text = open(a.txt, errors="replace").read()
        names = [r["name"] for r in parse_roster(text)] + [norm_name(n) for n in extra]
        turns, rep = split_turns(text, names)
        if a.print:
            for t in turns:
                tag = {"management": "**", "analyst": "Q ", "moderator": "[M]", "host": "[H]"}[t["role"]]
                print(f"{tag} {t['speaker']} ({t['section']}): {t['text'][:300 if t['role'] != 'management' else 4000]}\n")
        else:
            print(json.dumps({"roster": names, "label_report": rep, "turns": turns}, ensure_ascii=False, indent=1))
        return
    if not a.symbol:
        p.error("SYMBOL or --txt required")
    process_symbol(a.symbol.upper(), C.cache_root(a.cache), extra)


if __name__ == "__main__":
    main()
