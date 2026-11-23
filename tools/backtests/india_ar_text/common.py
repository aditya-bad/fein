"""Shared paths/helpers for the Indian annual-report text-change pilot (Roadmap stage 3).
Pre-registration: research_notes/Backtests/india_annual_report_text.md. Research tool, not SEBI-registered advice.
One polite stream: NSE (tools/nse_fetch.py, >= 1.5 s) and screener (tools/detectors/solvency_screen.py, >= 1.5 s)
are called one after the other from a single process."""
import gzip, io, json, os, shutil, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "tools", "detectors"))
sys.path.insert(0, HERE)
import nse_fetch as N          # noqa: E402
import solvency_screen as SS   # noqa: E402
import sections as SEC         # noqa: E402
SCR = "/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad"
OUT = os.environ.get("BT_INDIA_AR", os.path.join(SCR, "bt_india_ar"))
SOLV_SC = os.path.join(SCR, "bt_solv_in", "sc")       # earlier screener cache (pages/charts by slug)
REPORT_OUT = os.path.join(ROOT, "research_notes", "Backtests", "india_annual_report_text_outputs")
N.MIN_GAP = 1.5
SS.GAP = 1.5
MAX_BYTES = 80 * 1024 * 1024


def jload(p, d=None):
    try:
        return json.load(open(p))
    except Exception:
        return d


def jdump(o, p):
    tmp = p + ".tmp"
    json.dump(o, open(tmp, "w"), ensure_ascii=False)
    os.replace(tmp, p)


def fetch_text(url, work):
    """Download one AR (PDF or ZIP of PDFs) into a fresh dir `work`, pdftotext every PDF (name order), delete all
    binaries, return the list of page texts. Downloads are untrusted: never executed, names not trusted."""
    if os.path.exists(work):
        shutil.rmtree(work)
    os.makedirs(work)
    b = N._get(url, binary=True)
    size = len(b)
    pdfs = []
    if b[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(b))
        names = sorted(n for n in z.namelist() if n.lower().endswith(".pdf"))
        for i, n in enumerate(names):
            if z.getinfo(n).file_size > MAX_BYTES:
                continue
            p = os.path.join(work, f"{i:03d}.pdf")
            with open(p, "wb") as f:
                f.write(z.read(n))
            pdfs.append(p)
    elif b[:5] == b"%PDF-" or b"%PDF" in b[:1024]:
        p = os.path.join(work, "000.pdf")
        open(p, "wb").write(b)
        pdfs.append(p)
    del b
    pages = []
    for p in pdfs:
        try:
            pages += SEC.pdf_pages(p)
        except Exception:
            pass
    shutil.rmtree(work, ignore_errors=True)
    return pages, size, len(pdfs)


def save_text(path, obj):
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)


def load_text(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)
