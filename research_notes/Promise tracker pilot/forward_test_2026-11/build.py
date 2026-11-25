#!/usr/bin/env python3
"""Promise-credibility forward test, Nov-2026 cohort (roadmap stage 3 -> 7).

Applies the pre-registered rule (prereg.md in this folder, sha256 990c8180...) to the hand-built ledgers below:
  p0  = leave-one-out sector-peer strict delivery rate in the promise's category group (fallbacks per prereg s4)
  SAC = mean over the company's resolved past promises of (y - p0(group of that promise))
  P_cred = clip(p0 + N/(N+20) * SAC, 0.05, 0.95)  (P_cred = p0 if N < 3);  P_base = p0
Writes: ledger.json, memdb/seeds/2026-11-25_promise_forward_test.json, specs_lines.txt (one-line specs to append).
Run from the repo root: python3 -I "research_notes/Promise tracker pilot/forward_test_2026-11/build.py"
Research, not SEBI-registered advice.
"""
import json, os

ROOT = os.getcwd()
HERE = os.path.join(ROOT, "research_notes", "Promise tracker pilot", "forward_test_2026-11")
MADE = "2026-11-25"
K = 20

GROUP = {'revenue_growth': 'revenue', 'order_inflow': 'revenue', 'order_book': 'revenue', 'deal_wins': 'revenue',
         'margin': 'margin', 'capacity_commissioning': 'dates', 'capex': 'dates', 'new_product': 'dates',
         'approval_regulatory': 'dates', 'm&a': 'dates', 'customer_win': 'dates',
         'debt_reduction': 'balance_sheet', 'working_capital': 'balance_sheet'}

SECTOR = {'JASH': 'Capital Goods', 'KIRLOSBROS': 'Capital Goods', 'RISHABH': 'Capital Goods', 'ANUP': 'Capital Goods',
          'NEOGEN': 'Chemicals', 'GALAXYSURF': 'Chemicals', 'YASHO': 'Chemicals', 'TATVA': 'Chemicals',
          'KRSNAA': 'Healthcare', 'ORCHPHARMA': 'Healthcare', 'SYNGENE': 'Healthcare', 'SHILPAMED': 'Healthcare'}
NAME = {'JASH': 'Jash Engineering', 'KIRLOSBROS': 'Kirloskar Brothers', 'RISHABH': 'Rishabh Instruments',
        'ANUP': 'The Anup Engineering', 'NEOGEN': 'Neogen Chemicals', 'GALAXYSURF': 'Galaxy Surfactants',
        'YASHO': 'Yasho Industries', 'TATVA': 'Tatva Chintan Pharma Chem', 'KRSNAA': 'Krsnaa Diagnostics',
        'ORCHPHARMA': 'Orchid Pharma', 'SYNGENE': 'Syngene International', 'SHILPAMED': 'Shilpa Medicare'}

# ---- past promises: (symbol, said_on, group, y, title, evidence) ; y strict: delivered=1 else 0 ----
PAST = [
 ('JASH', '2025-02-13', 'revenue', 1, 'FY25 consolidated revenue Rs 675 cr', 'FY25 consolidated sales Rs 735 cr (screener)'),
 ('JASH', '2025-08-08', 'revenue', 0, 'FY26 consolidated revenue Rs 860 cr (restated Rs 825 cr in Nov-25 without saying so)', 'FY26 Rs 736 cr (screener) = 86%'),
 ('JASH', '2025-08-08', 'revenue', 0, 'Consolidated order book Rs 1,100 cr by 31-Mar-2026', 'Q4FY26 call: Rs 899 cr as on 1-May-2026'),
 ('JASH', '2025-05-06', 'other', 0, 'Waterfront (US sub) to break even in FY26', 'Q4FY26 call: "minor increase in revenue and reduction in losses"'),
 ('JASH', '2025-05-06', 'dates', 0, 'Pithampur SEZ plant commissioned Dec-2025/Jan-2026', 'Q3FY26 call (16-Feb-26): plant ready, commercial production "from the beginning of April"'),
 ('KIRLOSBROS', '2025-05-15', 'revenue', 0, 'Double-digit revenue growth (FY26; "that hasn\'t changed")', 'FY26 consolidated sales +1.0% (4,492 -> 4,538, screener); Q4FY26 call: double-digit growth "impacted" by Q1-Q3'),
 ('RISHABH', '2025-02-07', 'margin', 1, 'Lumel Alucast EBITDA breakeven in the next 1-2 quarters', 'Q4FY25 call: "for Q4 it is at breakeven"; Q1FY26 "successful turnaround of Lumel Alucast"'),
 ('RISHABH', '2025-05-27', 'margin', 1, 'Lumel Alucast positive EBITDA by end FY26', 'Q4FY26 call: Alucast adjusted EBITDA margin FY26 1.4%'),
 ('RISHABH', '2025-08-14', 'dates', 0, 'Nashik MIDC/Trishala buildings complete by Mar-2026', 'Q4FY26 call: capex complete, facilities "almost ready and under commissioning"; Q1FY27 "partial commissioning"'),
 ('RISHABH', '2025-11-17', 'margin', 1, 'FY26 consolidated EBITDA ~Rs 100 cr (raised to Rs 115-120 cr adjusted, Feb-26)', 'FY26 operating profit ~Rs 127 cr (screener 775 x 16.4%)'),
 ('ANUP', '2025-01-31', 'revenue', 1, 'FY25 revenue growth ~30%', 'Q4FY25 call: FY25 revenue Rs 751 cr, +36.5%'),
 ('ANUP', '2025-01-31', 'margin', 1, 'FY25 EBITDA margin ~23%', 'Q4FY25 call: EBITDA Rs 172.8 cr at 23%'),
 ('ANUP', '2025-05-13', 'revenue', 0, 'FY26 revenue growth ~25% (cut to 15-20% in Aug-25, acknowledged)', 'FY26 sales +12.1% (733 -> 822, screener)'),
 ('ANUP', '2025-05-13', 'margin', 1, 'FY26 EBITDA margin over 20%', 'FY26 OPM 21.5% (screener)'),
 ('ANUP', '2025-05-13', 'dates', 1, 'Kheda Phase-2 expansion commissioned by Q3FY26', 'Q3FY26 call (4-Feb-26): "completed Phase 2 as planned", Kheda fully operational'),
 ('ANUP', '2025-11-10', 'revenue', 1, 'Pending order book Rs 700-750 cr at 1-Apr-2026', 'Q4FY26 call: pending order book ~Rs 770 cr'),
 ('NEOGEN', '2025-02-03', 'revenue', 0, 'FY26 standalone revenue Rs 950-1,000 cr (withdrawn after Mar-25 Dahej fire)', 'Q4FY25 call: revised to Rs 775-850 cr (acknowledged) -> withdrawn = 0'),
 ('NEOGEN', '2025-02-03', 'margin', 1, 'EBITDA margin 18% +/- 1-1.5% (FY25)', 'FY25 OPM 17.5% (screener)'),
 ('NEOGEN', '2025-05-19', 'dates', 0, 'Dahej salts +1,100 t commissioned by Sep-2025', 'Q3FY26 call: timeline now Mar-2026 (was Dec-2025)'),
 ('GALAXYSURF', '2025-05-19', 'revenue', 0, 'FY26 volume growth ~8%', 'Q4FY26 call: AMET -15% in Q4, RoW +4% FY, India flattish-to-up: group volume well below 8% (inferred from regional data; single-source)'),
 ('GALAXYSURF', '2025-05-19', 'margin', 1, 'FY26 EBITDA/MT Rs 20,500-21,500', 'Quarterly EBITDA/MT ~20,000-20,160 in FY26 (Q1, Q3, Q4 calls) = >=95% of 20,500 (amount rule)'),
 ('YASHO', '2025-02-12', 'revenue', 0, 'FY26 revenue Rs 950-1,000 cr (= 40-50% growth, restated May/Jul-25)', 'FY26 sales Rs 830 cr, +22.8% (screener)'),
 ('YASHO', '2025-05-05', 'balance_sheet', 0, 'Net debt/EBITDA ~3.5x by FY26', 'Q1FY27 call: 3.75x at end of Q4FY26'),
 ('YASHO', '2025-05-05', 'other', 0, '70% capacity utilisation by Q4FY26', 'Q3FY26 call: "could not achieve the full utilization in FY26 what we anticipated"'),
 ('YASHO', '2025-05-05', 'balance_sheet', 0, 'Working capital 110-115 days by FY26', 'Q1FY26 call already re-set to ~150 days by March (unacknowledged move)'),
 ('TATVA', '2025-05-05', 'revenue', 1, 'FY26 "a year of good growth" with H2 recovery', 'FY26 sales +32% (383 -> 506, screener)'),
 ('KRSNAA', '2025-05-13', 'balance_sheet', 0, 'Receivables ~90-100 days by FY26', 'Q4FY26 call: 139 days'),
 ('KRSNAA', '2025-08-12', 'revenue', 1, 'Retail ~8% of revenue by FY26', 'Q4FY26 call: retail ~8% of FY26 revenue'),
 ('KRSNAA', '2025-11-10', 'margin', 0, 'Retail (RPL) business breakeven in Q4FY26', 'Q2FY27 call: "operationally breakeven in the month of September [2026] more or less"'),
 ('ORCHPHARMA', '2025-05-26', 'dates', 0, 'Dhanuka Laboratories merger completed within FY26', 'Q1FY27 call: merger effective 10-Jul-2026'),
 ('ORCHPHARMA', '2025-05-26', 'revenue', 0, 'Combined business revenue > Rs 1,500 cr (FY26)', 'Q1FY27 call: restated FY26 combined revenue below plan (screener FY26 Rs 1,233 cr)'),
 ('ORCHPHARMA', '2025-05-26', 'margin', 0, 'Combined business EBITDA ~Rs 175 cr (FY26)', 'FY26 operating profit ~Rs 48 cr (screener); combined gross margin fell to 32%'),
 ('SYNGENE', '2025-04-24', 'revenue', 0, 'FY26 revenue growth mid-single-digit (constant currency)', 'FY26 sales +2.7% reported (3,642 -> 3,739, screener); no cc beat found'),
 ('SYNGENE', '2025-07-24', 'margin', 1, 'FY26 EBITDA margin in the mid-20s', 'FY26 OPM 24.6% (screener)'),
 ('SYNGENE', '2025-07-24', 'dates', 0, 'Bayview (US) biologics facility operational in FY26', 'Q4FY26 call: "moving toward operationalization"'),
 ('SHILPAMED', '2025-05-26', 'revenue', 1, 'FY26 revenue to grow vs FY25', 'FY26 sales +19.8% (1,281 -> 1,535, screener)'),
]

# ---- forward calls ----
# fields: sym, slug, group, said_on, quote, claim, rule, spec(dict), resolve_by
FY = {"type": "a", "auto": "structured", "kind": "india_fin", "period": "FY", "end": "2027-03-31", "check_from": "2027-04-15"}
def fin(metric, op, thr, guard, basis="consolidated", **kw):
    d = dict(FY); d.update({"metric": metric, "basis": basis, "op": op, "threshold": thr, "guard": guard}); d.update(kw)
    if metric.endswith("_pct"): d["round"] = 1
    return d
def doc(sym, subject, phrases, note, check_from, deadline, op=None, thr=None, typ="a", event_deadline=None):
    d = {"type": typ, "auto": "assisted", "kind": "doc_scan", "source": "nse", "symbol": sym, "from": "2026-11-25",
         "deadline": deadline, "subject": subject, "phrases": phrases}
    if op: d.update({"op": op, "threshold": thr})
    d["note"] = note
    d["check_from"] = check_from
    if event_deadline: d["event_deadline"] = event_deadline
    return d
RES_FY = "Q4FY27 results, press release / investor presentation and Q4FY27 earnings call transcript (NSE)"
FWD = [
 # Capital Goods
 ('JASH', 'fy27-revenue-831cr-plus', 'revenue', '2026-05-27', 'project INR875 crore for the current year revenue (Q4FY26); "we should be able to meet the projections which were made in the beginning" (Q2FY27)',
  'Jash Engineering (JASH) FY27 consolidated revenue >= Rs 831 cr (95% of the Rs 875 cr guide)', 'YES if FY27 consolidated revenue from operations >= Rs 831 cr (NSE XBRL + screener).', fin("sales_cr", ">=", 831, 8), '2027-06-15'),
 ('JASH', 'fy27-pat-100cr-plus', 'other', '2026-08-12', '"we are expecting Rs.100 crore plus profit this year" (Q1FY27)',
  'Jash Engineering (JASH) FY27 consolidated net profit >= Rs 100 cr', 'YES if FY27 consolidated profit for the period >= Rs 100 cr (floor, strict).', fin("net_profit_cr", ">=", 100, 2), '2027-06-15'),
 ('JASH', 'fy27-rodney-hunt-usd33mn-plus', 'revenue', '2026-11-04', '"we definitely achieve the USD 35-36 million turnover this year in the USA" (Q2FY27; also Q1FY27)',
  'Jash Engineering (JASH) FY27 Rodney Hunt (USA) revenue >= USD 33.25 mn (95% of 35)', 'YES if the company states FY27 Rodney Hunt / US revenue >= USD 33.25 mn (or INR equivalent at the stated rate) in its Q4FY27 presentation or call.',
  doc('JASH', 'result|presentation|transcript', ["Rodney Hunt[^.\\n]{0,160}(USD|\\$|million|crore)"], "company-reported segment figure; USD 33.25 mn floor", "2027-05-01", "2027-06-30", ">=", 33.25), '2027-06-30'),
 ('JASH', 'q3fy27-129cr-orders-finalised', 'revenue', '2026-11-04', '"orders worth around INR 129 crore are currently under negotiation and are expected to be finalized during this quarter" (Q2FY27)',
  'Jash Engineering (JASH) finalises the ~Rs 129 cr of orders under negotiation by 31-Dec-2026', 'YES if the Q3FY27 call/presentation or an NSE filing states these orders (or order inflow in Oct-Dec 2026 including them, >= Rs 123 cr of the named negotiations) were finalised by 31-Dec-2026; a statement that they slipped = NO.',
  doc('JASH', 'transcript|presentation|order', ["(order|negotiat)[^.\\n]{0,200}(finali[sz]|received|booked)"], "event: finalised by 31-Dec-2026; read Q3FY27 call", "2027-01-20", "2027-03-15", typ="c", event_deadline="2026-12-31"), '2027-03-15'),
 ('KIRLOSBROS', 'fy27-standalone-revenue-growth-9p5pct-plus', 'revenue', '2026-08-03', '"We remain confident of delivering double-digit revenue growth in FY27 over FY26 for our standalone business" (Q1 and Q2 FY27 opening remarks)',
  'Kirloskar Brothers (KIRLOSBROS) FY27 standalone revenue growth >= 9.5% (double-digit less 0.5 pp tolerance)', 'YES if FY27 standalone revenue from operations growth vs FY26 >= 9.5% (NSE XBRL standalone + screener standalone).',
  fin("sales_growth_pct", ">=", 9.5, 0.5, basis="standalone"), '2027-06-15'),
 ('RISHABH', 'fy27-eei-adj-ebitda-133cr-plus', 'margin', '2026-05-18', '"the EEI business remains on track to achieve its full year guidance of INR140 crores to INR150 crores adjusted EBITDA" (Q2FY27)',
  'Rishabh Instruments (RISHABH) FY27 EEI adjusted EBITDA >= Rs 133 cr (95% of Rs 140 cr)', 'YES if the company-reported FY27 EEI (electrical, electronics & instruments) adjusted EBITDA >= Rs 133 cr (Q4FY27 presentation/call).',
  doc('RISHABH', 'result|presentation|transcript', ["EEI[^.\\n]{0,160}adjusted EBITDA[^.\\n]{0,80}"], "company-defined segment metric; Rs 133 cr floor", "2027-05-01", "2027-06-30", ">=", 133), '2027-06-30'),
 ('RISHABH', 'fy27-eei-revenue-growth-19pct-plus', 'revenue', '2026-11-16', '"We remain committed to our earlier guidelines of targeting 20% to 25% growth in the EEI segment" (Q2FY27)',
  'Rishabh Instruments (RISHABH) FY27 EEI segment revenue growth >= 19% (20% less tolerance)', 'YES if company-reported FY27 EEI revenue growth YoY >= 19.0%.',
  doc('RISHABH', 'result|presentation|transcript', ["EEI[^.\\n]{0,160}(grew|growth)[^.\\n]{0,40}%"], "segment growth; 19.0% floor", "2027-05-01", "2027-06-30", ">=", 19.0), '2027-06-30'),
 ('RISHABH', 'fy27-alucast-adj-ebitda-breakeven', 'margin', '2026-08-17', '"I believe that we would be able to breakeven the adjusted EBITDA for the full year by end of FY27" (Lumel Alucast, Q1FY27; Q2FY27 "+/-1-2%")',
  'Rishabh Instruments (RISHABH) FY27 Lumel Alucast adjusted EBITDA margin >= -0.3% (breakeven)', 'YES if company-reported FY27 Lumel Alucast (HPDC) adjusted EBITDA margin >= -0.3%.',
  doc('RISHABH', 'result|presentation|transcript', ["Alucast[^.\\n]{0,200}EBITDA[^.\\n]{0,80}%"], "segment margin; breakeven -0.3% floor", "2027-05-01", "2027-06-30", ">=", -0.3), '2027-06-30'),
 ('ANUP', 'fy27-revenue-798cr-plus', 'revenue', '2026-11-06', '"we should end the year with a revenue between INR840 crores to INR860 crores" (Q2FY27)',
  'The Anup Engineering (ANUP) FY27 consolidated revenue >= Rs 798 cr (95% of Rs 840 cr)', 'YES if FY27 consolidated revenue from operations >= Rs 798 cr.', fin("sales_cr", ">=", 798, 8), '2027-06-15'),
 ('ANUP', 'fy27-ebitda-114cr-plus', 'margin', '2026-11-06', '"with an EBITDA in the range of INR120 crores to INR128 crores" (Q2FY27)',
  'The Anup Engineering (ANUP) FY27 consolidated EBITDA >= Rs 114 cr (95% of Rs 120 cr)', 'YES if FY27 consolidated operating profit (revenue - operating expenses, excl. other income) >= Rs 114 cr.', fin("op_profit_cr", ">=", 114, 3), '2027-06-15'),
 ('ANUP', 'opening-order-book-apr27-760cr-plus', 'revenue', '2026-11-06', '"come 1st of April 2027, we should open the year with an order book position of INR800 crores to INR900 crores" (Q2FY27)',
  'The Anup Engineering (ANUP) pending order book at 1-Apr-2027 >= Rs 760 cr (95% of Rs 800 cr)', 'YES if the Q4FY27 call/presentation states the pending order book at 31-Mar/1-Apr-2027 (or "as on date" in the Q4 call if no year-end figure) >= Rs 760 cr.',
  doc('ANUP', 'result|presentation|transcript', ["(pending )?order book[^.\\n]{0,120}(INR|Rs\\.?)\\s?[\\d,]+"], "company-reported; Rs 760 cr floor", "2027-05-01", "2027-06-30", ">=", 760), '2027-06-30'),
 ('ANUP', 'fy27-mabel-revenue-62cr-plus', 'revenue', '2026-11-06', '"we should end the year close to about INR65 crores to INR70 crores coming from Mabel" (Q2FY27)',
  'The Anup Engineering (ANUP) FY27 Mabel Engineers revenue >= Rs 62 cr (95% of Rs 65 cr)', 'YES if company-reported FY27 Mabel Engineers revenue >= Rs 62 cr.',
  doc('ANUP', 'result|presentation|transcript', ["Mabel[^.\\n]{0,160}(INR|Rs\\.?)\\s?[\\d,.]+"], "subsidiary revenue; Rs 62 cr floor", "2027-05-01", "2027-06-30", ">=", 62), '2027-06-30'),
 # Chemicals
 ('NEOGEN', 'fy27-revenue-1100cr-plus', 'revenue', '2026-11-02', '"this year should be INR 1,100 crore plus kind of revenue, is what I am expecting" (Q2FY27)',
  'Neogen Chemicals (NEOGEN) FY27 consolidated revenue >= Rs 1,100 cr', 'YES if FY27 consolidated revenue from operations >= Rs 1,100 cr (floor, strict).', fin("sales_cr", ">=", 1100, 11), '2027-06-15'),
 ('NEOGEN', 'fy27-standalone-revenue-1000cr-plus', 'revenue', '2026-07-27', '"We feel the base business should be able to cross INR 1,000 crore in the current financial year" (Q1FY27)',
  'Neogen Chemicals (NEOGEN) FY27 standalone (base business) revenue >= Rs 1,000 cr', 'YES if FY27 standalone revenue from operations >= Rs 1,000 cr (floor, strict).', fin("sales_cr", ">=", 1000, 10, basis="standalone"), '2027-06-15'),
 ('NEOGEN', 'fy27-standalone-opm-16p2pct-plus', 'margin', '2026-07-27', '"For EBITDA margin in the current year, our base is 18% plus-minus 1%, 1.5%" (Q1FY27)',
  'Neogen Chemicals (NEOGEN) FY27 standalone operating margin >= 16.2% (18% - 1.5 pp - 0.3 pp tolerance)', 'YES if FY27 standalone operating profit / revenue >= 16.2%.', fin("opm_pct", ">=", 16.2, 0.3, basis="standalone"), '2027-06-15'),
 ('NEOGEN', 'fy27-battery-revenue-285cr-plus', 'revenue', '2026-07-27', '"we are looking at INR 300 crore kind of revenue for the current year for the battery business" (Q1FY27)',
  'Neogen Chemicals (NEOGEN) FY27 battery-materials (Neogen Ionics + salts/electrolyte) revenue >= Rs 285 cr', 'YES if company-reported FY27 battery-materials revenue >= Rs 285 cr (95% of 300); if not stated, consolidated minus standalone revenue is used.',
  doc('NEOGEN', 'result|presentation|transcript', ["(battery|Ionics|electrolyte)[^.\\n]{0,160}(INR|Rs\\.?)\\s?[\\d,.]+\\s?crore"], "company-reported; fallback consolidated - standalone", "2027-05-01", "2027-06-30", ">=", 285), '2027-06-30'),
 ('NEOGEN', 'fy27-working-capital-180-days-or-less', 'balance_sheet', '2026-11-02', '"we would be somewhere, around 180 days, is what we are targetting by the end of the current financial year" (Q2FY27)',
  'Neogen Chemicals (NEOGEN) working-capital days <= 180 at 31-Mar-2027', 'YES if the company-reported working-capital days at FY27 end <= 180 (ceiling, strict).',
  doc('NEOGEN', 'result|presentation|transcript', ["working capital[^.\\n]{0,120}days"], "company-defined; 180-day ceiling", "2027-05-01", "2027-06-30", "<=", 180), '2027-06-30'),
 ('GALAXYSURF', 'fy27-volume-growth-5p5pct-plus', 'revenue', '2026-08-14', '"we maintain our volume guidance at 6% to 8% for the full-year FY26-27" (Q1FY27)',
  'Galaxy Surfactants (GALAXYSURF) FY27 volume growth >= 5.5% (6% less 0.5 pp)', 'YES if company-reported FY27 total volume growth YoY >= 5.5%.',
  doc('GALAXYSURF', 'result|presentation|transcript', ["volume[^.\\n]{0,80}(grew|growth)[^.\\n]{0,40}%"], "company KPI; 5.5% floor", "2027-05-01", "2027-06-30", ">=", 5.5), '2027-06-30'),
 ('GALAXYSURF', 'fy27-ebitda-per-mt-22800-plus', 'margin', '2026-08-14', '"increased the range of the EBITDA per metric ton guidance ... to INR 24,000 to INR 25,000 per metric ton" (Q1FY27)',
  'Galaxy Surfactants (GALAXYSURF) FY27 EBITDA per MT >= Rs 22,800 (95% of Rs 24,000)', 'YES if company-reported FY27 EBITDA/MT >= Rs 22,800.',
  doc('GALAXYSURF', 'result|presentation|transcript', ["EBITDA per (metric )?(ton|tonne|MT)[^.\\n]{0,80}[\\d,]{5,6}"], "company KPI; Rs 22,800 floor", "2027-05-01", "2027-06-30", ">=", 22800), '2027-06-30'),
 ('YASHO', 'fy27-opm-20pct-plus', 'margin', '2026-10-29', '"the guidance was 20% plus on an EBITDA, and we stand by to that the commitment of 20% plus" (Q2FY27)',
  'Yasho Industries (YASHO) FY27 consolidated operating margin >= 20.0%', 'YES if FY27 consolidated operating profit / revenue >= 20.0% (floor, strict).', fin("opm_pct", ">=", 20.0, 0.3), '2027-06-15'),
 ('YASHO', 'fy27-utilisation-69p7pct-plus', 'other', '2026-08-03', '"FY27, we are expecting to ramp up to 75% utilization"; Q4FY26: "guidance of 70%, 75% utilization"',
  'Yasho Industries (YASHO) FY27 capacity utilisation >= 69.7% (70% less 0.3 pp)', 'YES if company-reported FY27 (full-year) capacity utilisation >= 69.7%.',
  doc('YASHO', 'result|presentation|transcript', ["utili[sz]ation[^.\\n]{0,80}%"], "company KPI; 69.7% floor", "2027-05-01", "2027-06-30", ">=", 69.7), '2027-06-30'),
 ('YASHO', 'fy27-capex-237cr-plus', 'dates', '2026-08-03', '"we have increased our FY27 capital expenditure plan to Rs. 250 crores" (Q1FY27; Q2FY27 "committed a capex of INR250 crores this year")',
  'Yasho Industries (YASHO) FY27 capex >= Rs 237.5 cr (95% of Rs 250 cr)', 'YES if FY27 consolidated cash-flow "purchase of property, plant & equipment (incl. CWIP)" or company-stated FY27 capex >= Rs 237.5 cr.',
  doc('YASHO', 'result|presentation|transcript', ["(capex|capital expenditure|purchase of property)[^.\\n]{0,120}[\\d,.]+"], "FY27 cash-flow statement in the Q4 results; Rs 237.5 cr floor", "2027-05-01", "2027-06-30", ">=", 237.5), '2027-06-30'),
 ('TATVA', 'fy27-revenue-growth-23p75pct-plus', 'revenue', '2026-07-17', '"25%, 30% growth is what we forecasted, and that\'s what we stick to" (Q1FY27)',
  'Tatva Chintan Pharma Chem (TATVA) FY27 consolidated revenue growth >= 23.75% (25% less 5% of target)', 'YES if FY27 consolidated revenue from operations growth vs FY26 >= 23.75%.', fin("sales_growth_pct", ">=", 23.75, 0.5), '2027-06-15'),
 ('TATVA', 'two-pharma-products-commercial-by-dec26', 'dates', '2026-05-16', '"We have one product getting into commercialization in Q1 and the other two products will get into commercial production from Q3" (Q4FY26)',
  'Tatva Chintan Pharma Chem (TATVA) starts commercial production of the other two pharma products by 31-Dec-2026', 'YES if the Q3FY27 call/presentation or an NSE filing states both remaining pharma products entered commercial production/supplies on or before 31-Dec-2026; one of two or a slip = NO.',
  doc('TATVA', 'transcript|presentation|result', ["pharma[^.\\n]{0,200}(commerciali[sz]|commercial (production|supplies))"], "event by 31-Dec-2026; read Q3FY27 call", "2027-01-20", "2027-03-15", typ="c", event_deadline="2026-12-31"), '2027-03-15'),
 ('TATVA', 'hybrid-battery-commercial-supply-by-dec26', 'dates', '2025-10-31', '"We can now clearly visualize commercialization on these batteries to begin in 2026" (Q2FY26); Q1FY27: "steadily moving towards commercial supply"',
  'Tatva Chintan Pharma Chem (TATVA) begins commercial supply to its hybrid-battery electrolyte-salt customer by 31-Dec-2026', 'YES if a call/presentation/filing dated <= 15-Mar-2027 states commercial (not trial/validation) supplies to the hybrid-battery customer began on or before 31-Dec-2026.',
  doc('TATVA', 'transcript|presentation|result', ["hybrid[^.\\n]{0,200}(commercial|supply|supplies)"], "event by 31-Dec-2026; trial orders do not count", "2027-01-20", "2027-03-15", typ="c", event_deadline="2026-12-31"), '2027-03-15'),
 # Healthcare
 ('KRSNAA', 'receivable-days-120-or-less-mar27', 'balance_sheet', '2026-05-26', '"Our improvement journey to sub 120 days guided for FY \'27 remains on track" (Q4FY26)',
  'Krsnaa Diagnostics (KRSNAA) receivable days < 120 at 31-Mar-2027', 'YES if company-reported receivable days at FY27 end are below 120 (ceiling, strict; 120 = NO).',
  doc('KRSNAA', 'result|presentation|transcript', ["receivable[^.\\n]{0,80}\\d{2,3} days"], "company KPI; sub-120 ceiling", "2027-05-01", "2027-06-30", "<", 120), '2027-06-30'),
 ('KRSNAA', 'fy27-cash-based-revenue-380cr-plus', 'revenue', '2026-11-03', '"By the end of FY \'27, we expect our cash-based revenues to contribute almost 40% to 45% ... aggregating to approximately INR400 crores for the year" (Q2FY27)',
  'Krsnaa Diagnostics (KRSNAA) FY27 cash-based revenue >= Rs 380 cr (95% of Rs 400 cr)', 'YES if company-reported FY27 cash-based (retail + cash PPP) revenue >= Rs 380 cr.',
  doc('KRSNAA', 'result|presentation|transcript', ["cash[- ]based[^.\\n]{0,160}"], "company-defined; Rs 380 cr floor", "2027-05-01", "2027-06-30", ">=", 380), '2027-06-30'),
 ('KRSNAA', 'retail-ebitda-positive-q4fy27', 'margin', '2026-11-03', '"we are hoping to be absolute breakeven ... by quarter 3 and early quarter 4" and "exiting FY \'27 with the sheer positive EBITDA numbers for the retail front" (Q2FY27)',
  'Krsnaa Diagnostics (KRSNAA) retail business EBITDA positive in Q4FY27', 'YES if the company states retail-business EBITDA for Q4FY27 (Jan-Mar 2027) was positive (> 0).',
  doc('KRSNAA', 'result|presentation|transcript', ["retail[^.\\n]{0,200}(EBITDA|break ?even)"], "segment; Q4FY27 retail EBITDA > 0", "2027-05-01", "2027-06-30", typ="c"), '2027-06-30'),
 ('KRSNAA', 'fy27-rajasthan-revenue-95cr-plus', 'revenue', '2026-05-26', '"Rajasthan, we believe the revenue potential to be in the range of about INR100 crores to INR150 crores on a full year basis" (Q4FY26, answering "this year")',
  'Krsnaa Diagnostics (KRSNAA) FY27 Rajasthan project revenue >= Rs 95 cr (95% of Rs 100 cr)', 'YES if company-reported FY27 Rajasthan revenue >= Rs 95 cr.',
  doc('KRSNAA', 'result|presentation|transcript', ["Rajasthan[^.\\n]{0,160}(INR|Rs\\.?)\\s?[\\d,.]+"], "project revenue; Rs 95 cr floor", "2027-05-01", "2027-06-30", ">=", 95), '2027-06-30'),
 ('ORCHPHARMA', 'fy27-ebitda-margin-11p7pct-plus', 'margin', '2026-05-26', '"should we at least for FY \'27 assume a 12% EBITDA margin for the base business? -- Yes, ... we are targeting something around that" (Q4FY26)',
  'Orchid Pharma (ORCHPHARMA) FY27 EBITDA margin >= 11.7% as the company reports it (12% less 0.3 pp)', 'YES if the company-reported FY27 EBITDA margin (base/combined business as the company presents it) >= 11.7%. Screener OPM differs from company EBITDA for Orchid, so the company figure governs.',
  doc('ORCHPHARMA', 'result|presentation|transcript', ["EBITDA margin[^.\\n]{0,60}%"], "company EBITDA governs (screener differs); 11.7% floor", "2027-05-01", "2027-06-30", ">=", 11.7), '2027-06-30'),
 ('ORCHPHARMA', 'cefiderocol-plant-commissioned-by-dec26', 'dates', '2026-11-17', '"Our current target remains commissioning by December 2026, followed by validation and initial batches between January and March of \'27" (Q2FY27)',
  'Orchid Pharma (ORCHPHARMA) commissions the cefiderocol plant by 31-Dec-2026', 'YES if an NSE filing, press release or the Q3FY27 call states the cefiderocol facility was commissioned (mechanically complete/operational) on or before 31-Dec-2026; an inauguration alone is not commissioning unless the text says the plant is commissioned.',
  doc('ORCHPHARMA', 'transcript|press|presentation|inaugur', ["cefiderocol[^.\\n]{0,200}(commission|operational|inaugur)"], "event by 31-Dec-2026", "2027-01-15", "2027-03-15", typ="c", event_deadline="2026-12-31"), '2027-03-15'),
 ('SYNGENE', 'fy27-ebitda-margin-ex-fx-23p7pct-plus', 'margin', '2026-07-30', '"we should be able to hold on to the guidance of mid-20s" (Q1FY27); Q2FY27: "no change in the EBITDA guidance ... excluding the forex loss at mid-20"',
  'Syngene International (SYNGENE) FY27 EBITDA margin excluding forex/hedge loss >= 23.7% (mid-20s low end 24% less 0.3 pp)', 'YES if the company-reported FY27 EBITDA margin before forex/hedge losses >= 23.7%.',
  doc('SYNGENE', 'result|press|presentation|transcript', ["EBITDA margin[^.\\n]{0,80}%"], "company figure ex-forex governs; 23.7% floor", "2027-04-25", "2027-06-30", ">=", 23.7), '2027-06-30'),
 ('SYNGENE', 'fy27-revenue-decline-3p5pct-or-better', 'revenue', '2026-07-30', '"guiding for a slight decline in revenue" (revised to "degrowth of low single digits", Q1FY27)',
  'Syngene International (SYNGENE) FY27 consolidated revenue growth >= -3.5% (low-single-digit decline, -3% less 0.5 pp)', 'YES if FY27 consolidated revenue from operations growth vs FY26 >= -3.5%.', fin("sales_growth_pct", ">=", -3.5, 0.5), '2027-06-15'),
 ('SHILPAMED', 'peptide-block-commissioned-by-mar27', 'dates', '2026-08-05', '"block will complete commissioning by end of FY27" (Q1FY27); "on track to commission one of the largest integrated peptide manufacturing capacities by the end of FY \'27" (Q2FY27)',
  'Shilpa Medicare (SHILPAMED) commissions its integrated peptide manufacturing block by 31-Mar-2027', 'YES if a document dated <= 14-Jun-2027 states the peptide block was commissioned on or before 31-Mar-2027.',
  doc('SHILPAMED', 'transcript|presentation|result|press', ["peptide[^.\\n]{0,200}(commission|operational)"], "event by 31-Mar-2027", "2027-04-15", "2027-06-14", typ="c", event_deadline="2027-03-31"), '2027-06-14'),
 ('SHILPAMED', 'aflibercept-india-launch-by-mar27', 'dates', '2026-08-05', '"Aflibercept, has had its clinical studies successfully completed, and we remain on track for launch in India market in FY27" (Q1FY27)',
  'Shilpa Medicare (SHILPAMED) launches its aflibercept biosimilar in India by 31-Mar-2027', 'YES if a filing, press release or call dated <= 14-Jun-2027 states the aflibercept biosimilar was launched (commercial sales, own or partner) in India on or before 31-Mar-2027; approval alone = NO.',
  doc('SHILPAMED', 'transcript|presentation|result|press|launch', ["[Aa]flibercept[^.\\n]{0,200}(launch|commerciali)"], "event by 31-Mar-2027", "2027-04-15", "2027-06-14", typ="c", event_deadline="2027-03-31"), '2027-06-14'),
 ('SHILPAMED', 'nor-udca-global-phase2-start-by-mar27', 'dates', '2026-08-05', '"we will be starting global Phase II clinical studies in FY27" (Nor-UDCA, Q1FY27)',
  'Shilpa Medicare (SHILPAMED) starts the global Phase II study of Nor-UDCA by 31-Mar-2027', 'YES if a document dated <= 14-Jun-2027 states the global (Europe/US) Phase II study started (first site initiated or first patient dosed) on or before 31-Mar-2027; regulatory approval to start alone = NO.',
  doc('SHILPAMED', 'transcript|presentation|result|press', ["(Nor-?UDCA|norUDCA)[^.\\n]{0,200}(Phase ?II|Phase 2)"], "event by 31-Mar-2027", "2027-04-15", "2027-06-14", typ="c", event_deadline="2027-03-31"), '2027-06-14'),
 ('SHILPAMED', 'two-biosimilars-human-studies-by-mar27', 'dates', '2026-11-05', '"In FY \'27, 2 of our biosimilars will be entering human studies for Europe and RoW markets" (Q2FY27)',
  'Shilpa Medicare (SHILPAMED) puts two biosimilars into human studies (Europe/RoW) by 31-Mar-2027', 'YES if a document dated <= 14-Jun-2027 states that two biosimilars entered human (clinical) studies on or before 31-Mar-2027; one = NO.',
  doc('SHILPAMED', 'transcript|presentation|result|press', ["biosimilar[^.\\n]{0,200}(human|clinical|Phase)"], "event by 31-Mar-2027; needs 2", "2027-04-15", "2027-06-14", typ="c", event_deadline="2027-03-31"), '2027-06-14'),
 ('SHILPAMED', 'two-nbe-phase1-by-mar27', 'dates', '2026-11-05', '"both partnership programs with Alveolus Bio and mAb Tree Biologics ... will be entering Phase I human studies in FY \'27" (Q2FY27)',
  'Shilpa Medicare (SHILPAMED) starts Phase I human studies for both NBE partnership programs (Alveolus Bio, mAb Tree) by 31-Mar-2027', 'YES if a document dated <= 14-Jun-2027 states both programs dosed a first human subject / started Phase I on or before 31-Mar-2027; one = NO.',
  doc('SHILPAMED', 'transcript|presentation|result|press', ["(Alveolus|mAb ?Tree|NBE)[^.\\n]{0,200}(Phase ?I|human)"], "event by 31-Mar-2027; needs both", "2027-04-15", "2027-06-14", typ="c", event_deadline="2027-03-31"), '2027-06-14'),
]

def td_ledgers():
    out = []
    for f, default in [('2026-11-21_promises_TD_peers.json', None), ('2026-11-19_promises_SKIPPER.json', 'SKIPPER')]:
        for r in json.load(open(os.path.join(ROOT, 'memdb', 'seeds', f))):
            if r.get('type') != 'promise': continue
            s = r['data'].get('status')
            if s in (None, 'pending', 'unverifiable'): continue
            sym = (r.get('tickers') or [default])[0] or default
            out.append((sym, GROUP.get(r['data'].get('category'), 'other'), 1 if s == 'delivered' else 0))
    return out

def rate(rows):
    return (sum(y for _, _, y in rows) / len(rows), len(rows)) if rows else (None, 0)

def main():
    td = td_ledgers()
    past = [(s, g, y) for s, _, g, y, _, _ in PAST]
    allrows = past + [(s, g, y) for s, g, y in td]
    sec_of = dict(SECTOR); sec_of.update({'KEC': 'Capital Goods', 'KPIL': 'Capital Goods', 'SKIPPER': 'Capital Goods'})

    def p0(sym, grp):
        peers = [r for r in allrows if r[0] != sym and sec_of.get(r[0]) == SECTOR[sym]]
        r, n = rate([x for x in peers if x[1] == grp])
        if n >= 8: return r, n, f"sector peers ({SECTOR[sym]}), group '{grp}'"
        r2, n2 = rate(peers)
        if n2 >= 8: return r2, n2, f"sector peers ({SECTOR[sym]}), all groups (group '{grp}' n={n} < 8)"
        r3, n3 = rate([x for x in allrows if x[0] != sym and x[1] == grp])
        if n3 >= 8: return r3, n3, f"pooled all cohort + T&D companies, group '{grp}' (sector pool n={n2} < 8)"
        return 0.5, 0, "no base rate (0.5)"

    cred = {}
    for sym in SECTOR:
        mine = [(g, y) for s, g, y in past if s == sym]
        res = [y - p0(sym, g)[0] for g, y in mine]
        N = len(mine); sac = sum(res) / N if N else 0.0
        w = N / (N + K)
        cred[sym] = {'N': N, 'hits': sum(y for _, y in mine), 'hit_rate': round(sum(y for _, y in mine) / N, 3) if N else None,
                     'sac': round(sac, 3), 'w': round(w, 3), 'active': N >= 3}
    # tercile by SAC (active and inactive alike, ties broken by symbol) -- reported only
    order = sorted(SECTOR, key=lambda s: (cred[s]['sac'], s), reverse=True)
    for i, s in enumerate(order): cred[s]['tercile'] = 'top' if i < 4 else ('middle' if i < 8 else 'bottom')

    recs, specs, calls = [], [], []
    for sym, slug, grp, said, quote, claim, rule, spec, rby in FWD:
        base, nb, basis = p0(sym, grp)
        c = cred[sym]
        pc = base + c['w'] * c['sac'] if c['active'] else base
        pc = min(0.95, max(0.05, pc)); base_r = round(base, 2); pc_r = round(pc, 2)
        praw = round(min(0.95, max(0.05, base + c['sac'])), 2) if c['N'] else base_r
        cid = f"thesis:paper-call:{sym}:{slug}-pft"
        adj = (f"p0 = {base:.3f} ({basis}, n={nb}); SAC {c['sac']:+.3f} x w {c['w']:.3f} (N={c['N']}) -> P_cred = {pc_r}"
               if c['active'] else f"p0 = {base:.3f} ({basis}, n={nb}); N={c['N']} < 3 so P_cred = P_base = {pc_r}")
        body = (f"Promise-credibility forward test, Nov-2026 cohort (NOT a recommendation; not buy/sell). {NAME[sym]} ({sym}). "
                f"Probability {pc_r} (naive sector base rate {base_r}) that: {claim}. Probabilities set only by the pre-registered rule "
                f"(research_notes/Promise tracker pilot/forward_test_2026-11/prereg.md s4): {adj}. Evidence: call of {said}: {quote}. "
                f"Resolution: {rule} Source: {RES_FY if spec.get('kind') == 'india_fin' else 'company Q3/Q4 FY27 filings, presentations and call transcripts (NSE)'}. "
                f"Resolve by {rby}; score Brier of P_cred vs P_base (prereg s5).")
        data = {"probability": pc_r, "base_rate_probability": base_r, "probability_raw_unshrunk": praw,
                "method": "promise-tracker credibility (sector-adjusted, rule-generated; forward test 2026-11)",
                "made_on": MADE, "resolve_by": rby, "resolution_rule": rule,
                "resolution_source": RES_FY if spec.get('kind') == 'india_fin' else "company filings/presentations/transcripts (NSE)",
                "base_rate_reasoning": f"Naive forecaster = leave-one-out strict delivery rate of {SECTOR[sym]} peers in group '{grp}' ({basis}, n={nb}). No company-specific information.",
                "adjustment_rule": "P_cred = clip(p0 + N/(N+20) x SAC, 0.05, 0.95); SAC = mean(y - p0(group)) over the company's resolved past promises (strict: delivered=1, else 0); N<3 -> P_cred = p0. P_base = p0.",
                "adjustment_applied": adj, "sector_adjusted_score": c['sac'], "sac_shrink_weight": c['w'], "sac_n_scored": c['N'],
                "credibility_tercile": c['tercile'], "promise_group": grp, "promise_said_on": said, "promise_quote": quote,
                "sector": SECTOR[sym], "company_name": NAME[sym], "cohort": "promise-forward-test-2026-11",
                "prereg": "research_notes/Promise tracker pilot/forward_test_2026-11/prereg.md", "outcome": None, "brier": None}
        tags = ["paper-call", "method-test", "promise-forward-test", "credibility-generated", "promise-tracker", "india",
                "sector-" + SECTOR[sym].lower().replace(' ', '-'), "cat-" + grp]
        recs.append({"type": "thesis", "id": cid, "title": f"Paper call: {claim}", "body": body, "tickers": [sym], "tags": tags,
                     "date": MADE, "status": "open", "confidence": "single-source", "data": data,
                     "sources": [f"https://www.screener.in/company/{sym}/consolidated/"]})
        specs.append(f' "{cid}": ' + json.dumps(spec, ensure_ascii=False))
        due = spec.get('event_deadline') or spec.get('end') or rby
        calls.append({'id': cid, 'sym': sym, 'group': grp, 'claim': claim, 'p_cred': pc_r, 'p_base': base_r, 'p_raw': praw,
                      'due': due, 'resolve_by': rby, 'auto': spec['auto'], 'kind': spec['kind']})

    seed = os.path.join(ROOT, 'memdb', 'seeds', '2026-11-25_promise_forward_test.json')
    json.dump(recs, open(seed, 'w'), indent=1, ensure_ascii=False)
    open(os.path.join(HERE, 'specs_lines.txt'), 'w').write(",\n".join(specs) + "\n")
    json.dump({'past': [dict(zip(['sym', 'said_on', 'group', 'y', 'title', 'evidence'], p)) for p in PAST],
               'credibility': cred, 'calls': calls,
               'td_rows': len(td)}, open(os.path.join(HERE, 'ledger.json'), 'w'), indent=1, ensure_ascii=False)
    for s in SECTOR:
        c = cred[s]; print(f"{s:11s} {SECTOR[s]:13s} N={c['N']} hits={c['hits']} SAC={c['sac']:+.3f} w={c['w']:.3f} {c['tercile']}")
    for c in calls: print(f"{c['due']} {c['sym']:10s} {c['group']:13s} Pc={c['p_cred']:.2f} Pb={c['p_base']:.2f} {c['auto']}")
    print(len(recs), 'calls ->', seed)

if __name__ == '__main__':
    main()
