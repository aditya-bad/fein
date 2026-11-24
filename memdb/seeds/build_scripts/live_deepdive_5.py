#!/usr/bin/env python3
"""Build memdb/seeds/2026-11-24_live_deepdive_5.json (LIVE deep dive #5, UTKARSHBNK). Run from repo root.
Merges hand-written live calls + analysis/variant/insight/event records with the card's paper calls
(tools/decision/live/UTKARSHBNK_paper_calls.json, card v1.4)."""
import json

T = "UTKARSHBNK"
D = "2026-11-24"
AN = "analysis:utkarshbnk-live-deepdive-2026-11"
SRC = ["research_notes/Deep dives/UTKARSHBNK_live.md"]
TAGS = ["paper-call", "deepdive-generated", "live", "india", "sector-banks", "sector-sfb", "method-test"]
PRE = ("Deep-dive-generated forward test (NOT a recommendation; not buy/sell). Live deep dive #5, company drawn at random "
       "(seed 20261202) from IT/software services + banks/NBFCs in the Rs 1,000-20,000 cr band (method test, L9/L21). ")

CALLS = [
 ("fy27-glp-growth-25pct-plus", "cat-growth", "Utkarsh SFB FY27 gross loan portfolio growth is >= 25% (management guidance 25-30%)",
  0.05, 0.50, "2027-05-31",
  "YES if gross loan portfolio at 31-Mar-2027, as reported in the Q4 FY27 press release/investor presentation, is >= Rs 24,165 cr (Rs 19,332 cr at 31-Mar-2026 x 1.25).",
  "NSE Reg-30 press release / investor presentation Q4 FY27",
  "Generic: Indian managements mostly meet numeric guidance while dates slip (L26) [EST 0.5].",
  "H1 FY27 GLP +3.8% (19,332 -> 20,062); H2 needs +20.4% (~Rs 4,100 cr) in six months vs +3.6% in H2 FY26; the same ~25% growth guided in Nov-2025 for FY26 came out at -1.7%; JLG still shrinking."),
 ("q3fy27-net-profit-positive", "cat-profit", "Utkarsh SFB reports a net profit (> 0) for Q3 FY27",
  0.20, 0.14, "2027-02-28",
  "YES if net profit after tax for the quarter ended 31-Dec-2026, as first reported (standalone; the bank has no subsidiaries), is > 0.",
  "NSE integrated-filing XBRL (banking: ProfitLossForThePeriod) / press release",
  "Laplace on the last 5 quarters: 0 of 5 profitable -> (0+1)/(5+2) = 0.14.",
  "Q2 PPOP 85 was flattered by a ~Rs 39 cr unexplained drop in staff cost; normal PPOP ~70-100 vs provisions guided 'declining' from 166 (credit cost 3.3%): central PBT about -Rs 40 to -60 cr."),
 ("q4fy27-pat-67cr-plus", "cat-profit", "Utkarsh SFB Q4 FY27 net profit is >= Rs 67 cr (~10% annualised ROE: management's 'double-digit ROE exit FY27')",
  0.10, 0.50, "2027-05-31",
  "YES if net profit after tax for the quarter ended 31-Mar-2027, as first reported, is >= Rs 67 cr (10% x Rs 2,676 cr net worth / 4).",
  "NSE integrated-filing XBRL / press release Q4 FY27",
  "Generic guidance-met rate (L26) [EST 0.5].",
  "Needs PPOP ~Rs 160 cr+ with credit cost ~2% inside two quarters; from Q2's -70 that is a Rs 137 cr swing; past profitability dates (May-2025: after H1 FY26) were missed."),
 ("gnpa-mar27-5pct-or-lower", "cat-asset-quality", "Utkarsh SFB gross NPA ratio at 31-Mar-2027 is <= 5.0%",
  0.45, 0.50, "2027-05-31",
  "YES if the GNPA % (bank's headline definition, advances incl. IBPC) at 31-Mar-2027 as first reported is <= 5.00% (Sep-2026: 5.96%).",
  "NSE integrated-filing XBRL (PercentageOfGrossNpa) / press release Q4 FY27",
  "Direction-of-trend coin [EST 0.5]: GNPA % fell in 5 of the last 6 quarters but by write-offs/ARC sales.",
  "Gross additions ~Rs 200-240 cr/qtr vs upgrades+recoveries ~65 and write-offs ~60-100; Q4 write-offs and an ARC sale are habitual (FY26 Q4 ARC Rs 624 cr), so <= 5% needs ~Rs 140 cr net reduction plus growth: close to even."),
 ("crar-mar27-16pct-plus", "cat-capital", "Utkarsh SFB total CRAR at 31-Mar-2027 is >= 16.0%",
  0.80, 0.86, "2027-05-31",
  "YES if capital adequacy ratio (Basel III, total) at 31-Mar-2027 as reported in the Q4 FY27 press release/Pillar 3 is >= 16.00% (Sep-2026: 17.05%).",
  "Press release / Pillar 3 DF-11 / XBRL",
  "Laplace on the last 5 reported quarter-ends, all >= 16%: (5+1)/(5+2) = 0.86.",
  "Rs 200 cr more Tier 2 planned in Q3; RWA +4-8% in H2 at the realistic growth; small losses: ~16.5-17.5% central. Risk: faster growth or a further intangible/DTA deduction."),
 ("equity-raise-approved-by-nov27", "cat-capital", "Utkarsh SFB board approves an equity raise (QIP, rights or preferential) by 30-Nov-2027",
  0.45, 0.30, "2027-11-30",
  "YES if a Reg-30 board outcome approving a QIP, rights issue or preferential issue of equity (not ESOPs, not Tier 2/AT1 debt) is filed between 24-Nov-2026 and 30-Nov-2027.",
  "NSE/BSE Reg-30 board outcomes",
  "[EST] roughly 1 in 3 Indian small-cap lenders approve an equity raise in any 12-month window.",
  "MD (04-Nov-2026): no equity this FY, 'sometime in the next financial year ... We may not require this'; CRAR cushion Rs 306 cr vs 25-30% growth plans; post-merger holders may prefer a QIP."),
 ("reverse-merger-effective-by-jun27", "cat-corporate", "The amalgamation of Utkarsh CoreInvest into Utkarsh SFB becomes effective by 30-Jun-2027",
  0.60, 0.65, "2027-06-30",
  "YES if by 30-Jun-2027 the bank files that the NCLT-sanctioned scheme has become effective (or allots shares to UCL shareholders / cancels UCL's holding).",
  "NSE/BSE Reg-30 filings; NCLT Allahabad orders",
  "[EST] NCLT second-motion petitions typically get sanction 3-12 months after filing; filed 05-Apr-2026, hearings 23-Jul, 22-Oct and 19-Nov-2026.",
  "Regulatory NOCs (RBI, NSE/BSE) received and creditors/shareholders approved; management says 'next few months'; NCLT calendars slip."),
 ("beats-nifty500-to-sep27", "price-relative", "Utkarsh SFB price return beats the Nifty 500 from 23-Nov-2026 to 30-Sep-2027",
  0.40, 0.44, "2027-09-30",
  "YES if UTKARSHBNK.NS close on 30-Sep-2027 / 11.71 > ^CRSLDX close on 30-Sep-2027 / 23,748.15; price return, last close on or before 30-Sep-2027.",
  "Yahoo v8 daily closes (UTKARSHBNK.NS, ^CRSLDX); NSE bhavcopy",
  "Share of small caps beating the index over ~10 months, skewed below 0.5 [EST, as in live deep dives #1, #3, #4].",
  "Recovery is partly priced (1.09x CET1 book); likely below-book raise and the post-merger PE supply overhang vs a possible return to profit; peers ESAF/Suryoday re-rated after their turn."),
]


def call_rec(slug, cat, title, p, base, by, rule, src, base_why, ours):
    return {"type": "thesis", "id": f"thesis:paper-call:{T}:{slug}", "title": f"Paper call: {title}",
            "body": PRE + f"Probability {p} (naive base rate {base}) that: {rule[7:] if rule.startswith('YES if ') else rule} "
                    f"Our reasoning: {ours} Naive base: {base_why} Resolution: {rule} Source: {src}. Resolve by {by}; "
                    "score with Brier vs the base rate.",
            "tickers": [T], "tags": TAGS + [cat], "date": D, "status": "open",
            "data": {"probability": p, "base_rate_probability": base, "method": "deep-dive protocol v1.4 (live #5, IT/lender frame; bank mode)",
                     "made_on": D, "resolve_by": by, "resolution_rule": rule, "resolution_source": src,
                     "base_rate_reasoning": base_why, "live": True, "practice": False, "outcome": None, "brier": None},
            "sources": SRC, "links": [{"to": AN, "rel": "generated_by"}], "confidence": "single-source"}


recs = [{
 "type": "analysis", "id": AN,
 "title": "Utkarsh Small Finance Bank (UTKARSHBNK) - LIVE deep dive #5, first live lender (protocol v1.4 bank mode, stages 2-7): method test, no verdict; card v1.4 size 0; 8 live calls",
 "body": ("LIVE method test (L9, L21): random draw (Random(20261202)) from 70 IT/software (36) + bank/NBFC (34) names in the India "
          "Rs 1,000-20,000 cr band at the 23-Nov-2026 close; lenders hand-classified before the shuffle (no industry_map.csv). No buy/sell "
          "verdict. Research, not advice. SKIP: KPITTECH (PEAD Q2 FY27 SUE -0.81 -> quintile 1, event 28-Oct-2026, inside the avoid window). "
          "SUBJECT: UTKARSHBNK (walk #2), a microfinance-born SFB (1,110 outlets, 18,300 staff, GLP Rs 20,062 cr, deposits Rs 23,869 cr). "
          "S2 bank form passed: unmodified FY26 audit (new joint auditors), no RBI divergence or penalty, CRAR 17.05% vs 15%, ratings A- "
          "(two notches down in 12 months), pledge 0, PEAD Q5. FINDINGS: (1) FY26 loss Rs 1,151 cr; GNPA 12.4% -> 5.9% mostly via write-offs "
          "and ARC sales (FY26 write-offs + ARC 1,743 > slippage 1,724; ARC sale Rs 1,515 cr principal for Rs 207 cr); (2) Tier-1 15.13% -> "
          "12.78% in Q2 FY27: CET1 deductions DTA 495 + intangibles 246 (new core banking capitalised; Pillar 3 DF-11) - unasked on the call; "
          "CET1 book Rs 1,907 cr = Rs 10.71/share vs price 11.71; (3) Q2 PPOP +34% QoQ leaned on personnel cost -16% QoQ with headcount up - "
          "unexplained; (4) capital cushion Rs 306 cr vs 25-30% growth guidance -> below-book raise likely FY28; (5) growth/profit guidance "
          "missed repeatedly; (6) L40: Bihar Micro Finance Institutions Act 2026 (banks exempt from registration, recovery rules apply; Bihar 44% "
          "of JLG) absent from AR FY26 and calls; CGFMU government guarantee is a provisioning input; (7) reverse merger of holdco UCL (swap "
          "699:100) makes 42.7% PE/DFI-held stake directly liquid. VALUATION (bank mode, Rs 500 cr raise at Rs 11 assumed): P/B 0.78x reported "
          "(0.82x diluted), 1.09x CET1 book; implied ROE 11.2% forever (13.2% on CET1 book); base IRR 12.0%; EV 1.24x raw / 1.29x anchored "
          "(w=0.3, non-financial class) vs hurdle 1.76x -> size 0. Calls: 8 live + 3 card calls."),
 "tickers": [T], "tags": ["deep-dive", "live", "method-test", "india", "sector-banks", "sector-sfb", "stage-2", "stage-3", "stage-4", "stage-5", "stage-6", "stage-7"],
 "date": D, "status": "done",
 "data": {"seed": 20261202, "frame_close": "2026-11-23", "frame_in_range": 809, "eligible": 70, "skips": ["KPITTECH (d) PEAD Q1"],
          "price": 11.71, "pb_reported": 0.78, "pb_diluted": 0.82, "pb_cet1_book": 1.09, "bvps": 15.04, "cet1_bvps": 10.71,
          "crar": 0.1705, "tier1": 0.1278, "gnpa_pct": 5.96, "nnpa_pct": 2.74, "fy26_pat_cr": -1150.98, "h1fy27_pat_cr": -103.77,
          "implied_roe_gordon": 0.112, "irr_base": 0.12, "ev_raw": 1.24, "ev_anchored": 1.29, "hurdle": 1.76, "anchor_w": 0.3,
          "card_version": "1.4", "worksheet_version": "1.1-bank", "size": 0, "peer_pb_median": 1.01},
 "sources": SRC + ["tools/valuation/live/UTKARSHBNK_worksheet.md", "tools/decision/live/UTKARSHBNK_card.md",
                   "research_notes/Deep dives/UTKARSHBNK_selection/prereg_selection.md"],
 "links": [{"to": "insight:lender-blowup-signals", "rel": "applies"}, {"to": "insight:subsidised-input-roic-and-renewal-risk", "rel": "applies"}],
 "confidence": "verified"},
 {"type": "thesis", "id": f"thesis:{T}:variant-view-2026-11",
  "title": "Utkarsh SFB (UTKARSHBNK) variant view, Nov 2026: the market prices a recovery (1.09x CET1 book); evidence leans negative vs the company's framing; no claimable mispricing",
  "body": ("Market: 0.78x reported book but 1.09x CET1 book; price needs ~11% ROE forever (13% on CET1 book), close to a haircut FY28 "
           "target of ~15%. Ours: GNPA improvement is write-off/ARC driven; Q2 PPOP leaned on an unexplained staff-cost drop; Tier-1 fell 235 bp "
           "on intangible/DTA deductions; capital cushion Rs 306 cr vs 25-30% growth guidance -> below-book raise likely; guidance misses; PE "
           "overhang after the holdco merger. Offsets: NIM 6.3%, CoF down, LCR 177%, CE 99.5%, peers recovered. Proves us wrong: two profitable "
           "quarters with credit cost < 2.5% and an equity raise at or above book. Scored by thesis:paper-call:UTKARSHBNK:*."),
  "tickers": [T], "tags": ["variant-perception", "live", "deepdive-generated", "india", "sector-banks", "stage-6"], "date": D, "status": "open",
  "data": {"market_view": "recovery to ~11-13% ROE priced (1.09x CET1 book)", "our_view": "no edge; evidence leans negative",
           "proves_wrong": "two profitable quarters, credit cost < 2.5%, raise at >= book"},
  "sources": SRC, "links": [{"to": AN, "rel": "found_in"}], "confidence": "single-source"},
 {"type": "insight", "id": "insight:lender-book-quality-cet1-deductions",
  "title": "For a loss-making lender, value on CET1 book, not reported book: DTA and capitalised software can be a third of net worth and move capital ratios without a loss",
  "body": ("Utkarsh SFB, Sep-2026: net worth Rs 2,676 cr but CET1 Rs 1,907 cr after deducting DTA (Rs 495 cr, recognised on an 'independent "
           "expert's opinion' after a Rs 1,507 cr pre-tax loss) and intangibles (Rs 53 -> 246 cr when a new core banking system was "
           "capitalised). Tier-1 fell 235 bp in one quarter on a Rs 69 cr fall in net worth; nobody asked on the call. Rule: for any lender with "
           "recent losses read Pillar 3 DF-11 (rows 9-10), compute P/CET1-book beside P/B, and treat DTA recognised on losses as an option on "
           "future profits (CET1 already excludes it). Also: when the deck shows Tier-1 moving more than net worth / RWA explains, find the "
           "deduction."),
  "tickers": [T], "tags": ["technique", "deep-dive", "banks", "india", "looks-good-flag", "l2", "l8", "capital"], "date": D, "status": "open",
  "data": {"net_worth_cr": 2676.33, "cet1_cr": 1906.7, "dta_cr": 495.45, "intangibles_cr": 245.67, "tier1_jun26": 0.1513, "tier1_sep26": 0.1278},
  "sources": SRC + ["https://www.utkarsh.bank.in/uploads/pdf/our-policy/template_ten/Basel_III_Pillar_3_Disclosures_as_on_September_30_2026.pdf"],
  "links": [{"to": AN, "rel": "found_in"}], "confidence": "verified"},
 {"type": "insight", "id": "insight:mfi-gnpa-writeoff-arc-walk",
  "title": "Microfinance lenders 'cure' GNPA by write-offs and ARC sales at ~14 paise on the rupee: rebuild the NPA walk before believing an asset-quality turn",
  "body": ("Utkarsh SFB FY26: GNPA additions Rs 1,724 cr; reductions Rs 2,119 cr = write-offs 1,089 + ARC sale 654 + upgrades/recoveries only 375. "
           "ARC sale FY26: Rs 1,515 cr principal (428,864 accounts) for Rs 207 cr consideration (13.6%), SRs fully provided. GNPA % fell 12.4% -> 5.9% "
           "(Sep-25 -> Sep-26) mostly by removal, not cure. Same trap as Federal Bank (v1.3 protocol). Use net slippage (additions - upgrades - "
           "recoveries) per quarter and the write-off pool recovery rate as the asset-quality KPI."),
  "tickers": [T], "tags": ["technique", "banks", "microfinance", "india", "looks-good-flag", "l2", "asset-quality"], "date": D, "status": "open",
  "data": {"fy26_additions": 1724.31, "fy26_writeoffs": 1089.6, "fy26_arc": 653.7, "fy26_upgrades_recoveries": 375.49, "arc_recovery_pct": 13.6},
  "sources": SRC, "links": [{"to": AN, "rel": "found_in"}, {"to": "insight:lender-blowup-signals", "rel": "extends"}], "confidence": "verified"},
 {"type": "event", "id": "event:bihar-microfinance-act-2026",
  "title": "Bihar Micro Finance Institutions (Regulation of Money Lending and Prevention of Coercive Actions) Act 2026 (Act 11 of 2026; Gazette 11-May-2026)",
  "body": ("Assembly passed 26-Feb-2026; MFI/NBFC stocks incl. Utkarsh SFB fell 5-11% (press). Requires state registration and other rules for "
           "money-lending entities; s.2(2) exempts scheduled commercial banks, RRBs, RBI-registered NBFCs and HFCs from the Act's lending "
           "provisions, but s.2(3) applies its coercive-recovery and borrower-protection provisions to them in Bihar. Utkarsh: Bihar = 44% of "
           "JLG, 48% of MBBL; not mentioned in AR FY26 or the May/Aug/Nov-2026 calls (L40 disclosure flag)."),
  "tickers": [T, "FUSION", "CREDITACC", "SPANDANA", "SATIN"], "tags": ["policy", "microfinance", "india", "state-law", "sector-nbfc", "sector-banks"],
  "date": "2026-05-11", "status": "open", "data": {"act_no": "11 of 2026", "assembly_pass": "2026-02-26", "banks_exempt_registration": True},
  "sources": ["https://prsindia.org/files/bills_acts/acts_states/bihar/2026/Act11of2026BR.pdf",
              "https://www.angelone.in/news/stocks/bihar-mfi-bill-2026-triggers-up-to-11-share-price-drop-in-l-t-finance-utkarsh-small-finance-bank-and-fusion-finance"],
  "links": [{"to": AN, "rel": "found_in"}], "confidence": "verified"},
]
recs += [call_rec(*c) for c in CALLS]
card = json.load(open("tools/decision/live/UTKARSHBNK_paper_calls.json"))
for r in card:
    r.setdefault("tags", [])
    for t in ("live", "deepdive-generated", "sector-banks", "sector-sfb"):
        if t not in r["tags"]:
            r["tags"].append(t)
    r.setdefault("links", []).append({"to": AN, "rel": "generated_by"})
recs += card
json.dump(recs, open("memdb/seeds/2026-11-24_live_deepdive_5.json", "w"), indent=1, ensure_ascii=False)
print(len(recs), "records")
