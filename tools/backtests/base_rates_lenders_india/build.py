#!/usr/bin/env python3
"""India LENDER 5-year base-rate class (banks, SFBs, NBFCs, HFCs, financial institutions; mcap Rs 1,000-20,000 cr at T).
Roadmap stage 6 (decision card outside view), feeding stage 7 (Brier baselines). Lesson L41 (4).

Same snapshots, outcome definitions and missing-R5 rule as tools/backtests/base_rates_5y/build.py (India class), but a
CENSUS of lender candidates instead of a stratified sample (weight 1.0 per company), because the stratified solvency
panel excluded financials and its live-stratum sample holds too few in-band lenders.

Frame (fate-independent, built from lists that exist today):
  * BSE Active, Delisted and Suspended scrip lists, NSE delisted/suspended, IBBI CIRP/liquidation rows
    (research_notes/Universe/india_dead_companies_2026-11-22.csv + the cached BSE active list), equity codes only
    (BSE 5xxxxx), whose NAME matches a lender keyword (bank, financ, fin, housing, credit, leasing, capital, invest,
    money, micro, loan, homes ...);
  * plus every lender in research_notes/Backtests/india_pead_live/industry_map.csv (any name);
  * plus every financial page already cached by the solvency re-test (fetch_status.json fin=True);
  * plus a short explicit list of lenders whose names carry no keyword (REC, IFCI, PAISALO ...).
  Each candidate's screener page decides whether it is a LENDER (labels: Banks / NBFC / Housing Finance / Microfinance /
  Financial Institution; unlabeled pages with the bank template). Investment/holding companies, brokers, AMCs,
  insurers, 'Other Financial Services' are not lenders (listed in the audit for review when in band).
Snapshots T = 2016-09-30, 2018-09-30; FY0 rule, size rule (screener mcap-to-sales x TTM sales at the last weekly price
<= T, trading within 31 days), outcome window (T, T+5y] exactly as the solvency re-test (s2_fetch / s3_panel).
Mergers inside the window (PSU-bank amalgamations, GRUH, Capital First, Bharat Financial, SBI associates, Shriram City,
Equitas Holdings): the shareholder's path is chained into the acquirer at the target's last traded price
(R = target_last/target_T x acquirer(t)/acquirer(link)), so a merger is neither dropped nor counted as a failure.
Equity write-offs (LVB 2020, DHFL 2021) are explicit strict failures.
Outcomes: ge3x R5>=3 (price only); le_half R5<=0.5 or (no R5 and failed); fail = close <=0.2x T close within 5y,
liquidation, compulsory delisting, equity write-off. Median multiple: weighted median of R5 with failed-no-R5 = 0.
CIs: 2,000 bootstrap draws resampling companies (seed 20261125).

Usage: python3 build.py --phase frame|pages|charts|panel|all  (network phases polite: >=1.55 s, one stream, cached)
Standard library + system curl (via tools/detectors/solvency_screen.py). Research, not SEBI-registered advice.
"""
import argparse, collections, csv, datetime as dt, json, os, random, re, sys, time, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "backtests", "solvency_india"))
import common as K          # noqa: E402  (CACHE, SNAPS, addy, read_csv, write_csv, jload, jsave, SS, F)
import s2_fetch as S2       # noqa: E402  (page_for-style helpers, fy0_for, mcap_at)
import s3_panel as S3       # noqa: E402  (price_series, outcomes, d_or_none)

SS = K.SS
SEED = 20261125
LO, HI = 1000.0, 20000.0
OUT = os.path.join(ROOT, "research_notes", "Backtests", "base_rates_lenders_india_outputs")
STATUS = os.path.join(K.CACHE, "lender_status.json")
FRAME = os.path.join(K.CACHE, "lender_frame.csv")
FOREVER = 1e6

KW = re.compile(r"bank|financ|\bfin|fincorp|fincap|finvest|finlease|housing|credit|leasing|lease|hire purchase|capital|"
                r"invest|money|micro|loan|homes|muthoot|manappuram|shriram|gruh|ifci|rural electrification", re.I)
EXTRA = [("532955", "RECLTD", "REC Ltd"), ("500106", "IFCI", "IFCI Ltd"), ("532900", "PAISALO", "Paisalo Digital"),
         ("511218", "SHRIRAMFIN", "Shriram Finance / Shriram Transport"), ("532810", "PFC", "Power Finance Corp"),
         ("540530", "HUDCO", "HUDCO"), ("511243", "CHOLAFIN", "Cholamandalam Inv & Fin")]
# target BSE code -> (acquirer screener slug, effective date, source)
MERGERS = {
    "532121": ("BANKBARODA", "2019-04-01", "Dena Bank -> Bank of Baroda, 110 per 1000 (GoI amalgamation scheme 2019)"),
    "532401": ("BANKBARODA", "2019-04-01", "Vijaya Bank -> Bank of Baroda, 402 per 1000"),
    "532276": ("CANBK", "2020-04-01", "Syndicate Bank -> Canara Bank, 158 per 1000"),
    "532480": ("INDIANB", "2020-04-01", "Allahabad Bank -> Indian Bank, 115 per 1000"),
    "532418": ("UNIONBANK", "2020-04-01", "Andhra Bank -> Union Bank of India, 324 per 1000"),
    "532179": ("UNIONBANK", "2020-04-01", "Corporation Bank -> Union Bank of India, 330 per 1000"),
    "500315": ("PNB", "2020-04-01", "Oriental Bank of Commerce -> PNB, 1150 per 1000"),
    "533171": ("PNB", "2020-04-01", "United Bank of India -> PNB, 121 per 1000"),
    "511288": ("BANDHANBNK", "2019-10-17", "GRUH Finance -> Bandhan Bank, 568 per 1000"),
    "532938": ("IDFCFIRSTB", "2018-12-18", "Capital First -> IDFC First Bank, 139 per 10"),
    "533228": ("INDUSINDBK", "2019-07-04", "Bharat Financial Inclusion -> IndusInd Bank, 639 per 1000"),
    "501061": ("SBIN", "2017-04-01", "State Bank of Bikaner & Jaipur -> SBI, 28 per 10"),
    "532191": ("SBIN", "2017-04-01", "State Bank of Travancore -> SBI, 22 per 10"),
    "532200": ("SBIN", "2017-04-01", "State Bank of Mysore -> SBI, 22 per 10"),
    "532498": ("SHRIRAMFIN", "2022-12-21", "Shriram City Union Finance -> Shriram Finance, 1.55 per 1"),
    "539844": ("EQUITASBNK", "2023-03-31", "Equitas Holdings -> Equitas SFB, 231 per 100"),
}
# equity written off / extinguished (strict failure on the date)
WIPED = {"534690": ("2020-11-27", "Lakshmi Vilas Bank: RBI scheme, amalgamated into DBS Bank India, equity written off"),
         "511072": ("2021-09-30", "DHFL: IBC resolution (Piramal), equity extinguished, delisted")}

# screener slugs for codes whose BSE-code page is missing (found by NSE symbol, 25-Nov-2026)
ALT_SLUG = {"511288": "GRUH", "532498": "SHRIRAMCIT", "539844": "EQUITAS", "523756": "SREINFRA",
            "500111": "RELCAPITAL", "539874": "UJJIVAN"}
# DHFL has no page of its own: screener carries its pre-2021 history on Piramal Finance Ltd (bse:544597, cid 799; the
# DHFL entity absorbed Piramal Capital & Housing in 2021 and was listed again in 2025). Its rows ARE DHFL's outcome
# (crash to 0.03x, no price at T+5 -> counted as failed, <=0.5x). Labelled here so the panel says so.
NAME_NOTE = {"bse:544597": "DHFL (screener page now 'Piramal Finance Ltd'; pre-2021 prices are DHFL's)"}
# single-lender holding companies and NBFC-CICs whose screener label is 'Investment Company' (reviewed by hand)
KIND_OVERRIDE = {"bse:500111": "nbfc", "bse:539844": "nbfc", "bse:532659": "nbfc"}
# size at T where screener's market-cap-to-sales is missing or broken: shares (equity capital / FV 10 on the page,
# plus IPO shares) x price at T. Sources in the md; single-source -> flagged size_ambiguous.
# price series unusable (screener shows Rs 30,418 for a ~Rs 70 stock and the ratio path is not constant): excluded,
# counted in the survivorship audit. Syndicate Bank was in band at both T (~Rs 4,900 / ~5,700 cr) and merged into
# Canara Bank (158 per 1000, Apr-2020).
DATA_BROKEN = {"bse:532276": "Syndicate Bank: screener price series mis-scaled"}
SIZE_OVERRIDE = {
    ("bse:540065", "FY2016"): (11100.0, "RBL Bank: listed 31-Aug-2016; ~37 cr post-IPO shares x Rs 299 (screener)"),
    ("bse:541770", "FY2018"): (5300.0, "CreditAccess Grameen: listed 23-Aug-2018; ~14.3 cr shares x Rs 368 (screener)"),
}
NAME_LENDER = re.compile(r"\bbank\b|financ|fincorp|fincap|finvest|finlease|\bfin\b|housing fin|home fin|homes|credit|"
                         r"leasing|hire purchase|micro ?fin|loan|gruh", re.I)
REVIEWED_LENDERS = set()   # keys of ambiguous-name firms confirmed as lenders by hand (see the md)
NAME_AMBIG = re.compile(r"capital|invest|money", re.I)
LENDER_IND = re.compile(r"bank|non banking financial|nbfc|housing finance|microfinance|financial institution", re.I)
NOT_LENDER = re.compile(r"investment company|holding company|stockbroking|asset management|insurance|exchange|rating|"
                        r"distributor|fintech|depositor|other financial services", re.I)


def classify(lab, page, name=""):
    txt = " / ".join(lab.get(k, "") for k in ("Broad Industry", "Industry"))
    if txt.strip(" /"):
        if NOT_LENDER.search(txt):
            return "not_lender", txt
        if LENDER_IND.search(txt):
            kind = "bank" if re.search(r"bank", txt, re.I) and not re.search(r"non banking", txt, re.I) else (
                "hfc" if re.search("housing", txt, re.I) else "nbfc")
            return kind, txt
        return "not_lender", txt
    if "Financing Profit" in page or ">Deposits<" in page:
        title = page[page.find("<title>") + 7: page.find("</title>")] if "<title>" in page else ""
        return ("bank" if " bank" in title.lower() else "nbfc"), "unlabeled, lender template"
    # unlabeled (mostly merged / delisted firms): classify by name; ambiguous names are reviewed by hand when in band
    if re.search(r"\bbank\b", name, re.I):
        return "bank", "unlabeled, name"
    if NAME_LENDER.search(name):
        return ("hfc" if re.search("housing|home|gruh", name, re.I) else "nbfc"), "unlabeled, name"
    if NAME_AMBIG.search(name):
        return "ambiguous", "unlabeled, ambiguous name"
    return "not_lender", "unlabeled"


# ----------------------------------------------------------------------------- frame

def build_frame():
    rows = {}

    def add(code, nse, name, src):
        code = (code or "").strip()
        if not (code.isdigit() and code.startswith("5") and len(code) == 6):
            code = ""
        key = "bse:" + code if code else ("nse:" + nse.upper() if nse else None)
        if not key:
            return
        r = rows.setdefault(key, {"key": key, "bse_code": code, "nse_symbol": nse or "", "name": name, "sources": set()})
        r["sources"].add(src)
        if nse and not r["nse_symbol"]:
            r["nse_symbol"] = nse
    for x in json.load(open(os.path.join(K.CACHE, "bse_active.json"))):
        if KW.search((x.get("Scrip_Name") or "") + " " + (x.get("Issuer_Name") or "")):
            add(x["SCRIP_CD"], x.get("scrip_id") or "", x["Scrip_Name"], "bse_active")
    for d in K.read_csv(K.DEAD_CSV):
        if KW.search(d["company"]) or d["bse_code"] in MERGERS or d["bse_code"] in WIPED:
            add(d["bse_code"], d["nse_symbol"], d["company"], d["source"])
    for m in K.read_csv(os.path.join(ROOT, "research_notes", "Backtests", "india_pead_live", "industry_map.csv")):
        if LENDER_IND.search(m.get("industry", "") + " " + m.get("basic_industry", "")) and \
                not NOT_LENDER.search(m.get("basic_industry", "")):
            add(m.get("bse_code", ""), m["symbol"], m["symbol"], "industry_map")
    st = K.jload(os.path.join(K.CACHE, "fetch_status.json"), {})
    fr = {r["key"]: r for r in K.read_csv(os.path.join(K.CACHE, "frame.csv"))}
    for k, v in st.items():
        if v.get("fin") and k in fr:
            add(fr[k]["bse_code"], fr[k]["nse_symbol"], fr[k]["name"], "solvency_cache_fin")
    for code, nse, name in EXTRA:
        add(code, nse, name, "explicit")
    for code in list(MERGERS) + list(WIPED):
        add(code, "", code, "explicit")
    for code, slug in ALT_SLUG.items():
        add(code, slug, slug, "explicit")
    add("532659", "IDFC", "IDFC Ltd (holding company of IDFC First Bank)", "explicit")
    out = []
    for r in rows.values():
        r["sources"] = "|".join(sorted(r["sources"]))
        out.append(r)
    K.write_csv(FRAME, out, ["key", "bse_code", "nse_symbol", "name", "sources"])
    print("frame", len(out), collections.Counter(s for r in out for s in r["sources"].split("|")))


# ----------------------------------------------------------------------------- fetch

def page_for(r):
    for slug in [s for s in (r["bse_code"], r["nse_symbol"]) if s]:
        d = os.path.join(K.CACHE, "sc", slug)
        if os.path.exists(os.path.join(d, "404")):
            continue
        body = SS.cached(os.path.join(d, "page.html"), FOREVER,
                         lambda: SS.curl(f"{K.SCREENER}/company/{urllib.parse.quote(slug)}/"))
        if body and 'id="profit-loss"' in body:
            return slug, body
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "404"), "w").close()
    return None, None


def chart(slug, cid):
    d = os.path.join(K.CACHE, "sc", slug)
    txt = SS.cached(os.path.join(d, "chart.json"), FOREVER, lambda: SS.curl(
        f"{K.SCREENER}/api/company/{cid}/chart/?q=Price-Market+Cap+to+Sales-Sales&days=10000"))
    try:
        return json.loads(txt) if txt else {}
    except ValueError:
        return {}


def fetch(phase):
    SS.GAP = 1.55
    frame = K.read_csv(FRAME)
    st = K.jload(STATUS, {})
    t0, n = time.time(), 0
    for i, r in enumerate(frame, 1):
        s = st.setdefault(r["key"], {})
        if phase == "pages" and s.get("page") == "no_page" and r["bse_code"] in ALT_SLUG:
            s.clear()
        if phase == "pages" and s.get("industry") == "unlabeled":      # v2 classifier: names for unlabeled pages
            s["kind"], s["industry"] = classify({}, "", s.get("name") or r["name"])
        if phase == "pages" and r["key"] in KIND_OVERRIDE and s.get("page") == "ok":
            s["kind"] = KIND_OVERRIDE[r["key"]]
            s["industry"] = s["industry"].split(" [")[0] + " [holdco/CIC reviewed as lender]"
        try:
            if phase == "pages" and "page" not in s:
                slug, page = page_for(r)
                if not page:
                    s["page"] = "no_page"
                else:
                    lab = SS.labels(page)
                    kind, txt = classify(lab, page, SS.company_name(page) or r["name"])
                    s.update(page="ok", slug=slug, kind=kind, industry=txt, name=SS.company_name(page),
                             elig=S2.snapshot_eligibility(page),
                             cid=(re.search(r'data-company-id="(\d+)"', page) or [None, None])[1])
                n += 1
            elif phase == "charts" and s.get("page") == "ok" and s["kind"] != "not_lender" and \
                    any(s["elig"].values()) and "size" not in s:
                ch = chart(s["slug"], s["cid"])
                s["size"] = {sn: (S2.mcap_at(ch, T) if s["elig"].get(sn) else {"status": "no_annual_at_T"})
                             for sn, T in K.SNAPS.items()}
                n += 1
        except Exception as e:  # keep going; record
            s[phase + "_error"] = str(e)[:200]
            print("ERR", r["key"], phase, e, flush=True)
        if n and n % 40 == 0:
            K.jsave(STATUS, st)
        if i % 100 == 0:
            print(f"{phase} {i}/{len(frame)} req~{n} {time.time()-t0:.0f}s", flush=True)
    if phase == "charts":       # acquirers
        for slug in sorted(set(v[0] for v in MERGERS.values())):
            if ("acq:" + slug) not in st:
                page = SS.cached(os.path.join(K.CACHE, "sc", slug, "page.html"), FOREVER,
                                 lambda: SS.curl(f"{K.SCREENER}/company/{slug}/"))
                cid = (re.search(r'data-company-id="(\d+)"', page or "") or [None, None])[1]
                chart(slug, cid)
                st["acq:" + slug] = {"cid": cid}
    K.jsave(STATUS, st)
    print(f"phase {phase} done {time.time()-t0:.0f}s", flush=True)


# ----------------------------------------------------------------------------- panel

def chained_series(px, code):
    """Own weekly prices, then (for an in-window merger) target_last x acquirer(t)/acquirer(link)."""
    if code not in MERGERS or not px:
        return px, None
    slug, eff, _ = MERGERS[code]
    acq = S3.price_series(K.jload(os.path.join(K.CACHE, "sc", slug, "chart.json"), {}))
    if not acq:
        return px, "acquirer_missing"
    dl, pl = px[-1]
    base = [p for d, p in acq if d <= dl]
    if not base:
        return px, "acquirer_missing"
    a0 = base[-1]
    return px + [(d, pl * p / a0) for d, p in acq if d > dl], "chained:" + slug


def panel():
    frame = {r["key"]: r for r in K.read_csv(FRAME)}
    st = K.jload(STATUS, {})
    ev = collections.defaultdict(list)
    alias = {}
    for k, r in frame.items():
        if r["bse_code"]:
            alias[("bse", r["bse_code"])] = k
        if r["nse_symbol"]:
            alias[("nse", r["nse_symbol"].upper())] = k
    for d in K.read_csv(K.DEAD_CSV):
        k = alias.get(("bse", d["bse_code"])) or alias.get(("nse", d["nse_symbol"].upper()))
        if k:
            ev[k].append(d)
    rows, funnel, review = [], collections.Counter(), []
    seen_cid = set()
    for k, r in frame.items():
        s = st.get(k, {})
        if s.get("page") != "ok":
            funnel["no_page"] += 1
            continue
        if s["cid"] in seen_cid:          # same company reached by two identifiers
            funnel["duplicate_company"] += 1
            continue
        seen_cid.add(s["cid"])
        if k in DATA_BROKEN:
            funnel["lender_data_broken_excluded"] += 1
            continue
        if s["kind"] == "not_lender":
            funnel["not_lender"] += 1
            continue
        if s["kind"] == "ambiguous" and k not in REVIEWED_LENDERS:
            for sn in K.SNAPS:
                z = (s.get("size") or {}).get(sn) or {}
                if z.get("status") == "ok" and LO <= z["mcap"] <= HI:
                    review.append((s["name"], sn, round(z["mcap"])))
            funnel["ambiguous_name_not_counted"] += 1
            continue
        funnel["lender"] += 1
        ch = K.jload(os.path.join(K.CACHE, "sc", s["slug"], "chart.json"), {})
        px = S3.price_series(ch)
        code = r["bse_code"]
        for sn, T in K.SNAPS.items():
            z = dict((s.get("size") or {}).get(sn) or {"status": "no_annual_at_T" if not s["elig"].get(sn) else "no_chart"})
            ov = SIZE_OVERRIDE.get((k, sn))
            if ov and s["elig"].get(sn):
                z.update(status="ok", mcap=ov[0], mcap_lo=0.0, mcap_hi=1e9, override=ov[1])
                funnel[sn + "|size_override"] += 1
            if z.get("status") != "ok":
                funnel[sn + "|" + z["status"]] += 1
                continue
            if not (LO <= z["mcap"] <= HI):
                funnel[sn + "|out_of_band"] += 1
                continue
            srcs = r["sources"]
            evs = ev.get(k, [])
            cirp_before = any((S3.d_or_none(e["event_date"]) or dt.date.max) <= T for e in evs
                              if e["source"] in ("ibbi_cirp", "ibbi_liq"))
            if cirp_before:
                funnel[sn + "|in_insolvency_at_T"] += 1
                continue
            path, chain = chained_series(px, code)
            o = S3.outcomes(path, T, evs, srcs)
            end = K.addy(T, K.WIN_YEARS)
            wipe = WIPED.get(code)
            o["o_wiped"] = int(bool(wipe and T < dt.date.fromisoformat(wipe[0]) <= end))
            if o["o_wiped"]:
                o["o_fail"] = o["o_strict"] = 1
                o["r5"] = 0.0 if o["r5"] is None else min(o["r5"], 0.0)
            if chain and o.get("o_cdel") and code in MERGERS:   # merger-delisting is not compulsory delisting
                o["o_cdel"] = 0
                o["o_strict"] = int(o["o_liq"] or o["o_wiped"])
                o["o_fail"] = int(o["o_strict"] or o["o_px"])
            rows.append(dict(key=k, slug=s["slug"], name=NAME_NOTE.get(k, s["name"]), kind=s["kind"], industry=s["industry"], snap=sn,
                             mcap=round(z["mcap"], 1), size_ambiguous=int(z["mcap_lo"] < LO or z["mcap_hi"] > HI),
                             sources=srcs, chain=chain or "", **o))
            funnel[sn + "|panel"] += 1
    K.write_csv(os.path.join(OUT, "panel.csv"), rows)
    funnel["_ambiguous_in_band_review"] = review
    return rows, dict(funnel)


# ----------------------------------------------------------------------------- estimators

def flags(r):
    r5 = None if r["r5"] in ("", None) else float(r["r5"])
    fail = int(r["o_fail"]) == 1
    if r5 is not None:
        return r5 >= 3, r5 <= 0.5, fail, r5
    if fail:
        return False, True, True, 0.0
    return None, None, fail, None


def wmedian(v):
    v = sorted(v)
    return None if not v else (v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2)


def rates(rows):
    f = [flags(r) for r in rows]
    k = [x for x in f if x[0] is not None]
    out = {"n": len(rows), "n_tail": len(k),
           "p_ge_3x": sum(x[0] for x in k) / len(k) if k else None,
           "p_le_half": sum(x[1] for x in k) / len(k) if k else None,
           "p_blowup": sum(x[2] for x in f) / len(f) if f else None,
           "p_strict": sum(int(r["o_strict"]) for r in rows) / len(rows) if rows else None,
           "p_blowup_permanent": sum(1 for x in f if x[2] and (x[3] is None or x[3] <= 0.5)) / len(f) if f else None,
           "median_mult": wmedian([x[3] for x in f if x[3] is not None]),
           "excluded_no_r5_alive": sum(1 for x in f if x[0] is None)}
    return out


def bootstrap(rows, draws=2000, seed=SEED):
    rng = random.Random(seed)
    cl = collections.defaultdict(list)
    for r in rows:
        cl[r["key"]].append(r)
    cl = list(cl.values())
    acc = collections.defaultdict(list)
    for _ in range(draws):
        smp = [x for _ in cl for x in cl[rng.randrange(len(cl))]]
        for key, v in rates(smp).items():
            if key.startswith("p_") or key == "median_mult":
                if v is not None:
                    acc[key].append(v)
    ci = {}
    for key, v in acc.items():
        v.sort()
        ci[key] = [round(v[int(0.025 * (len(v) - 1))], 4), round(v[int(0.975 * (len(v) - 1))], 4)]
    return ci


def rnd(d):
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items()}


def analyse(draws):
    rows, funnel = panel()
    res = {"generated_by": "tools/backtests/base_rates_lenders_india/build.py", "seed": SEED, "draws": draws,
           "funnel": funnel, "point": rnd(rates(rows)), "ci95": bootstrap(rows, draws)}
    res["by_snapshot"] = {s: rnd(rates([r for r in rows if r["snap"] == s])) for s in K.SNAPS}
    res["by_kind"] = {kd: rnd(rates([r for r in rows if (r["kind"] == "bank") == (kd == "bank")]))
                      for kd in ("bank", "nbfc_hfc")}
    res["by_kind_ci95"] = {kd: bootstrap([r for r in rows if (r["kind"] == "bank") == (kd == "bank")], draws)
                           for kd in ("bank", "nbfc_hfc")}
    psu_merged = {"bse:" + c for c in ("532121", "532401", "532276", "532480", "532418", "532179", "500315", "533171",
                                       "501061", "532191", "532200")}
    psu = [r for r in rows if "public sector" in r["industry"].lower() or r["key"] in psu_merged]
    res["bank_public_sector_by_snapshot"] = {s: rnd(rates([r for r in psu if r["snap"] == s])) for s in K.SNAPS}
    res["nbfc_hfc_by_snapshot"] = {s: rnd(rates([r for r in rows if r["kind"] != "bank" and r["snap"] == s])) for s in K.SNAPS}
    res["bank_public_sector"] = rnd(rates(psu))
    res["bank_private_other"] = rnd(rates([r for r in rows if r["kind"] == "bank" and r not in psu]))
    res["live_today_only"] = rnd(rates([r for r in rows if "bse_active" in r["sources"] or "industry_map" in r["sources"]]))
    res["exclude_size_overrides"] = rnd(rates([r for r in rows if (r["key"], r["snap"]) not in SIZE_OVERRIDE]))
    res["exclude_size_ambiguous"] = rnd(rates([r for r in rows if not int(r["size_ambiguous"])]))
    res["chained_mergers"] = sorted(set((r["name"], r["chain"]) for r in rows if r["chain"]))
    res["failures"] = sorted([(r["name"], r["snap"], r["r5"], r["min_ratio"], "wiped" if r["o_wiped"] else
                               ("strict" if r["o_strict"] else "price")) for r in rows if r["o_fail"]], key=str)
    res["winners_3x"] = sorted([(r["name"], r["snap"], r["r5"]) for r in rows if r["r5"] not in (None, "") and float(r["r5"]) >= 3], key=str)
    res["excluded_alive_no_r5"] = [(r["name"], r["snap"], r["last_px_date"]) for r in rows if flags(r)[0] is None]
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1, default=str)
    print(json.dumps({k: res[k] for k in ("funnel", "point", "ci95", "by_snapshot", "by_kind", "bank_public_sector",
                                          "bank_private_other", "live_today_only", "exclude_size_overrides", "exclude_size_ambiguous")}, indent=1))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["frame", "pages", "charts", "panel", "all"], default="panel")
    ap.add_argument("--draws", type=int, default=2000)
    a = ap.parse_args(argv)
    if a.phase in ("frame", "all"):
        build_frame()
    for ph in ("pages", "charts"):
        if a.phase in (ph, "all"):
            fetch(ph)
    if a.phase in ("panel", "all"):
        analyse(a.draws)


if __name__ == "__main__":
    main()
