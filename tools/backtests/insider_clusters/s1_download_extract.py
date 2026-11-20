#!/usr/bin/env python3
"""Step 1: download SEC 'Insider Transactions Data Sets' (quarterly, SEC's own parse of every
Form 3/4/5 XML) and extract open-market purchases (Form 4, TRANS_CODE == 'P', acquired 'A').

Why the data sets instead of sampling daily form.idx: they are the complete population of
Form 4 filings, so there is no sampling bias and far fewer HTTP calls (one zip per quarter).

Output: <out>/purchases.tsv  one row per purchase transaction with owner + plan flags.
Usage:  python3 s1_download_extract.py OUTDIR [--from 2020q4 --to 2025q1]
Standard library only. Downloaded zips are treated as data (never executed).
"""
import csv, io, os, re, sys, time, urllib.request, zipfile, argparse

UA = os.environ.get("SEC_UA", "fein-research admin@example.com")
BASE = "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{q}_form345.zip"
csv.field_size_limit(10**9)
PLAN_RE = re.compile(r"10b5-?1", re.I)


def quarters(a, b):
    y, q = int(a[:4]), int(a[5]); y2, q2 = int(b[:4]), int(b[5])
    while (y, q) <= (y2, q2):
        yield f"{y}q{q}"
        q += 1
        if q == 5: y, q = y + 1, 1


def fetch(q, rawdir):
    p = os.path.join(rawdir, f"{q}_form345.zip")
    if not os.path.exists(p):
        req = urllib.request.Request(BASE.format(q=q), headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=300) as r, open(p + ".part", "wb") as f:
            f.write(r.read())
        os.rename(p + ".part", p)
        time.sleep(1.0)
    return p


def rows(z, name):
    with z.open(name) as fh:
        rd = csv.DictReader(io.TextIOWrapper(fh, "utf-8", "replace"), delimiter="\t", quoting=csv.QUOTE_NONE)
        yield from rd


def ddmon(s):  # 31-MAR-2021 -> 2021-03-31
    from datetime import datetime
    try:
        return datetime.strptime(s.strip(), "%d-%b-%Y").date().isoformat()
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--from", dest="frm", default="2020q4"); ap.add_argument("--to", default="2025q1")
    a = ap.parse_args()
    rawdir = os.path.join(a.out, "raw"); os.makedirs(rawdir, exist_ok=True)
    outp = os.path.join(a.out, "purchases.tsv")
    cols = ["accession", "filing_date", "trans_date", "doc_type", "issuer_cik", "issuer_name", "ticker",
            "owner_cik", "owner_name", "relationship", "title", "n_owners", "shares", "price", "value",
            "shares_after", "direct", "plan_flag", "plan_footnote", "security"]
    n = 0
    with open(outp, "w", newline="") as fo:
        w = csv.writer(fo, delimiter="\t"); w.writerow(cols)
        for q in quarters(a.frm, a.to):
            z = zipfile.ZipFile(fetch(q, rawdir))
            # pass 1: purchase transactions
            tx = {}
            for r in rows(z, "NONDERIV_TRANS.tsv"):
                if r["TRANS_CODE"] == "P" and r["TRANS_ACQUIRED_DISP_CD"] == "A":
                    tx.setdefault(r["ACCESSION_NUMBER"], []).append(r)
            acc = set(tx)
            sub = {r["ACCESSION_NUMBER"]: r for r in rows(z, "SUBMISSION.tsv") if r["ACCESSION_NUMBER"] in acc}
            own = {}
            for r in rows(z, "REPORTINGOWNER.tsv"):
                if r["ACCESSION_NUMBER"] in acc:
                    own.setdefault(r["ACCESSION_NUMBER"], []).append(r)
            planfn = set()
            for r in rows(z, "FOOTNOTES.tsv"):
                if r["ACCESSION_NUMBER"] in acc and PLAN_RE.search(r.get("FOOTNOTE_TXT") or ""):
                    planfn.add(r["ACCESSION_NUMBER"])
            k = 0
            for ac, lst in tx.items():
                s = sub.get(ac)
                if not s or s["DOCUMENT_TYPE"] not in ("4", "4/A"):
                    continue
                os_ = own.get(ac, [{}])
                o = os_[0]
                pf = (s.get("AFF10B5ONE") or "").strip().lower() in ("1", "true")
                for t in lst:
                    try:
                        sh = float(t["TRANS_SHARES"] or 0); px = float(t["TRANS_PRICEPERSHARE"] or 0)
                    except ValueError:
                        continue
                    w.writerow([ac, ddmon(s["FILING_DATE"]), ddmon(t["TRANS_DATE"]), s["DOCUMENT_TYPE"],
                                s["ISSUERCIK"].lstrip("0"), s["ISSUERNAME"], s["ISSUERTRADINGSYMBOL"].strip().upper(),
                                o.get("RPTOWNERCIK", "").lstrip("0"), o.get("RPTOWNERNAME", ""),
                                o.get("RPTOWNER_RELATIONSHIP", ""), o.get("RPTOWNER_TITLE", ""), len(os_),
                                sh, px, round(sh * px, 2), t["SHRS_OWND_FOLWNG_TRANS"], t["DIRECT_INDIRECT_OWNERSHIP"],
                                int(pf), int(ac in planfn), t["SECURITY_TITLE"][:60]])
                    k += 1
            n += k
            print(f"{q}: {len(tx)} purchase filings, {k} rows (total {n})", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
