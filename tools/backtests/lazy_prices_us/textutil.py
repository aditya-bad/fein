"""HTML/iXBRL -> plain text, section extraction, similarity. Standard library only."""
import html, math, re
from collections import Counter

_HIDDEN = re.compile(r"<ix:header>.*?</ix:header>|<(script|style|head)\b.*?</\1>|<!--.*?-->", re.S | re.I)
_BLOCK = re.compile(r"<(?:/?(?:p|div|br|tr|li|h\d|table|td)\b)[^>]*>", re.I)
_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"[ \t\r\f\v    ​]+")


def html_to_text(raw):
    s = raw.decode("utf-8", "ignore") if isinstance(raw, bytes) else raw
    # some primary docs are SGML wrappers or plain text
    s = _HIDDEN.sub(" ", s)
    s = _BLOCK.sub("\n", s)
    s = _TAG.sub(" ", s)
    s = html.unescape(s)
    s = _WS.sub(" ", s)
    s = re.sub(r"\n\s*", "\n", s)
    return s.strip()


SEP = r"[\s\.\:\-–—,]*"
SECTIONS = {
    "1a": (re.compile(r"(?:^|\n)\s*item\s*1a\b" + SEP + r"risk\s+factors", re.I),
           re.compile(r"(?:^|\n)\s*item\s*(?:1b\b|1c\b|2\b" + SEP + r"(?:description\s+of\s+)?propert)", re.I)),
    "7": (re.compile(r"(?:^|\n)\s*item\s*7\b(?!\s*a\b)" + SEP + r"management", re.I),
          re.compile(r"(?:^|\n)\s*item\s*(?:7a\b|8\b" + SEP + r"financial)", re.I)),
}


def section(text, key, minlen=1500):
    st, en = SECTIONS[key]
    starts = [m.start() for m in st.finditer(text)]
    ends = [m.start() for m in en.finditer(text)]
    best = ""
    for s in starts:
        e = next((x for x in ends if x > s), None)
        if e is not None and e - s > len(best):
            best = text[s:e]
    return best if len(best) >= minlen else ""


_TOK = re.compile(r"[a-z]{2,}")


def tf(text):
    return Counter(_TOK.findall(text.lower()))


def cosine(a, b):
    if not a or not b:
        return None
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values())); nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else None


def jaccard(a, b):
    if not a or not b:
        return None
    A, B = set(a), set(b)
    return len(A & B) / len(A | B)
