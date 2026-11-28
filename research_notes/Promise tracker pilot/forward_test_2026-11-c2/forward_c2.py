"""Cohort-2 forward calls (prereg s2): said in the latest call (or the one before if not restated), deadline
2026-12-01 -> 2027-07-31, max 6 per company. Quotes checked against the transcript text. Imported by build.py."""

SECTOR = {'INTELLECT': 'Information Technology', 'RATEGAIN': 'Information Technology',
          'SFL': 'Consumer Durables', 'GREENLAM': 'Consumer Durables',
          'SUPRAJIT': 'Automobile and Auto Components', 'LANDMARK': 'Automobile and Auto Components'}
NAME = {'INTELLECT': 'Intellect Design Arena', 'RATEGAIN': 'RateGain Travel Technologies', 'SFL': 'Sheela Foam',
        'GREENLAM': 'Greenlam Industries', 'SUPRAJIT': 'Suprajit Engineering', 'LANDMARK': 'Landmark Cars'}

FY = {"type": "a", "auto": "structured", "kind": "india_fin", "period": "FY", "end": "2027-03-31", "check_from": "2027-04-15"}


def fin(metric, op, thr, guard, basis="consolidated", **kw):
    d = dict(FY); d.update({"metric": metric, "basis": basis, "op": op, "threshold": thr, "guard": guard}); d.update(kw)
    if metric.endswith("_pct"): d["round"] = 1
    return d


def doc(sym, subject, phrases, note, check_from, deadline, op=None, thr=None, typ="a", event_deadline=None):
    d = {"type": typ, "auto": "assisted", "kind": "doc_scan", "source": "nse", "symbol": sym, "from": "2026-11-26",
         "deadline": deadline, "subject": subject, "phrases": phrases}
    if op: d.update({"op": op, "threshold": thr})
    d["note"] = note
    d["check_from"] = check_from
    if event_deadline: d["event_deadline"] = event_deadline
    return d


# fields: sym, slug, group, said_on, quote, claim, rule, spec(dict), resolve_by
FWD = [
 # Information Technology
 ('INTELLECT', 'quarterly-revenue-900cr-by-q4fy27', 'revenue', '2026-10-30', '"We are definitely confident of crossing Rs 900 crore in the next two quarters" (Q2FY27; Q1-Q2 revenue ~Rs 850 cr)',
  'Intellect Design Arena (INTELLECT) reports consolidated quarterly revenue >= Rs 900 cr in Q3FY27 or Q4FY27', 'YES if consolidated revenue from operations for the quarter ending 31-Dec-2026 or 31-Mar-2027 is >= Rs 900 cr (floor, strict; NSE XBRL / screener quarterly).',
  doc('INTELLECT', 'result|presentation|transcript', ["[Rr]evenue[^.\\n]{0,120}(INR|Rs\\.?|₹)\\s?[\\d,.]+\\s?(crore|cr)"], "quarterly revenue floor Rs 900 cr in Q3 or Q4 FY27 (screener quarters decide)", "2027-01-25", "2027-06-15", ">=", 900), '2027-06-15'),
 ('INTELLECT', 'quarterly-cost-base-735cr-or-less-q4fy27', 'other', '2026-10-30', '"over the next few quarters, my cost will not increase in proportion ... It will remain between Rs 680 crore and Rs 700 crore" (Q2FY27)',
  'Intellect Design Arena (INTELLECT) Q4FY27 consolidated operating expenses (revenue - EBITDA) <= Rs 735 cr (105% of the Rs 700 cr ceiling)', 'YES if consolidated expenses excl. depreciation, interest and other income for Jan-Mar 2027 (screener "Expenses") are <= Rs 735 cr.',
  doc('INTELLECT', 'result|presentation', ["(total )?(expenses|cost)[^.\\n]{0,80}[\\d,.]+"], "screener quarterly Expenses for Q4FY27; ceiling Rs 735 cr", "2027-04-25", "2027-06-15", "<=", 735), '2027-06-15'),
 ('INTELLECT', 'fy27-revenue-growth-11p4pct-plus', 'revenue', '2026-05-09', '"Design-wise, we are still looking at 20%; whether we achieve 15%, 14%, or 12%" (Q4FY26)',
  'Intellect Design Arena (INTELLECT) FY27 consolidated revenue growth >= 11.4% (12% low end less 5% of target)', 'YES if FY27 consolidated revenue from operations growth vs FY26 >= 11.4%.', fin("sales_growth_pct", ">=", 11.4, 0.6), '2027-06-15'),
 ('INTELLECT', 'fy27-gross-margin-55p7pct-plus', 'margin', '2026-07-31', '"we had said that we would like to hover around 56-57% of gross margin" (Q1FY27; current quarter 57%)',
  'Intellect Design Arena (INTELLECT) FY27 gross margin as the company reports it >= 55.7% (56% less 0.3 pp)', 'YES if the company-reported FY27 gross margin (Q4FY27 presentation/call) >= 55.7%.',
  doc('INTELLECT', 'result|presentation|transcript', ["[Gg]ross margin[^.\\n]{0,80}%"], "company KPI; 55.7% floor", "2027-05-01", "2027-06-30", ">=", 55.7), '2027-06-30'),
 # Consumer Durables
 ('GREENLAM', 'fy27-revenue-growth-15p2pct-plus', 'revenue', '2026-11-06', '"revenue guidance for the year as a whole, this will be in the range of around 16%-18%, which we have earlier also guided 18%-20%" (Q2FY27)',
  'Greenlam Industries (GREENLAM) FY27 consolidated revenue growth >= 15.2% (16% low end less 5% of target)', 'YES if FY27 consolidated revenue from operations growth vs FY26 >= 15.2%.', fin("sales_growth_pct", ">=", 15.2, 0.8), '2027-06-15'),
 ('GREENLAM', 'fy27-net-debt-down-95cr-plus', 'balance_sheet', '2026-11-06', '"Difficult to say whether it will be exact 100, but it will be very close" (net debt reduction FY27; Q1FY27 "close to around INR100-odd crores")',
  'Greenlam Industries (GREENLAM) cuts net debt by >= Rs 95 cr in FY27 (95% of ~Rs 100 cr)', 'YES if company-reported net debt at 31-Mar-2027 is at least Rs 95 cr below net debt at 31-Mar-2026 (Q4FY27 presentation/call; else borrowings minus cash & investments from the FY27 balance sheet).',
  doc('GREENLAM', 'result|presentation|transcript', ["[Nn]et debt[^.\\n]{0,120}[\\d,.]+"], "company net debt FY27 vs FY26; reduction >= Rs 95 cr", "2027-05-01", "2027-06-30", ">=", 95), '2027-06-30'),
 ('GREENLAM', 'ap-laminate-lines-commercial-by-mar27', 'dates', '2026-11-06', '"we are adding two more lines in Andhra Pradesh plant, and that\'s running on schedule, and we should be able to begin commercial production by Q4 of this FY" (Q2FY27)',
  'Greenlam Industries (GREENLAM) starts commercial production on the two new Andhra Pradesh laminate lines by 31-Mar-2027', 'YES if a document dated <= 14-Jun-2027 states commercial production on the new AP laminate lines began on or before 31-Mar-2027; trial runs or one line only = NO.',
  doc('GREENLAM', 'transcript|presentation|result|commercial|press', ["(Andhra|Naidupeta|laminate)[^.\\n]{0,200}(commercial production|commissioned|operational)"], "event by 31-Mar-2027; both lines", "2027-04-15", "2027-06-14", typ="c", event_deadline="2027-03-31"), '2027-06-14'),
 ('GREENLAM', 'fy27-plywood-ebitda-breakeven', 'margin', '2026-08-10', '"we are expecting EBITDA breakeven in this year" (plywood, Q1FY27; Q4FY26 "plywood and chipboard ... breakeven in this financial year"; Q2FY27 "we should stop losing money at the EBITDA level in the plywood and allied business")',
  'Greenlam Industries (GREENLAM) FY27 plywood (and allied) segment EBITDA >= 0', 'YES if the company-reported FY27 plywood / plywood & allied EBITDA is >= 0 (breakeven or positive).',
  doc('GREENLAM', 'result|presentation|transcript', ["[Pp]lywood[^.\\n]{0,200}EBITDA[^.\\n]{0,80}"], "segment EBITDA >= 0", "2027-05-01", "2027-06-30", ">=", 0), '2027-06-30'),
 ('GREENLAM', 'fy27-chipboard-ebitda-breakeven', 'margin', '2026-06-04', '"plywood and chipboard, we expect both of these segments to breakeven in this financial year" (Q4FY26)',
  'Greenlam Industries (GREENLAM) FY27 chipboard (particle board) segment EBITDA >= 0', 'YES if the company-reported FY27 chipboard / particle-board EBITDA is >= 0.',
  doc('GREENLAM', 'result|presentation|transcript', ["([Cc]hipboard|[Pp]article board)[^.\\n]{0,200}EBITDA[^.\\n]{0,80}"], "segment EBITDA >= 0", "2027-05-01", "2027-06-30", ">=", 0), '2027-06-30'),
 ('GREENLAM', 'fy27-laminate-revenue-growth-9p5pct-plus', 'revenue', '2026-11-06', '"Whether 10%, 12% we will be able to achieve, probably it will be in that range, but may not be 10% to 12%" (laminates, Q2FY27; Q1FY27 "we still stand by that it can grow 10% to 12%")',
  'Greenlam Industries (GREENLAM) FY27 laminate segment revenue growth >= 9.5% (10% less 0.5 pp)', 'YES if company-reported FY27 laminates (& allied) revenue growth YoY >= 9.5%.',
  doc('GREENLAM', 'result|presentation|transcript', ["[Ll]aminate[^.\\n]{0,160}(grew|growth)[^.\\n]{0,40}%"], "segment growth; 9.5% floor", "2027-05-01", "2027-06-30", ">=", 9.5), '2027-06-30'),
 # Automobile and Auto Components
 ('SUPRAJIT', 'fy27-revenue-growth-9p5pct-plus', 'revenue', '2026-08-07', '"on a consolidated basis, we will grow in double digits ... the guidance that we gave in our press release dated 25th May 2026, still holds" (Q1FY27; reaffirmed Q2FY27)',
  'Suprajit Engineering (SUPRAJIT) FY27 consolidated revenue growth >= 9.5% (double-digit less 0.5 pp)', 'YES if FY27 consolidated revenue from operations growth vs FY26 >= 9.5%.', fin("sales_growth_pct", ">=", 9.5, 0.5), '2027-06-15'),
 ('SUPRAJIT', 'fy27-operational-ebitda-margin-11p7pct-plus', 'margin', '2026-11-12', '"we are just standing by that margin that guidance we have given in the beginning of the year ... the consolidated" 12%-13.5% (Q2FY27; "these are all operational numbers", Q1FY27)',
  'Suprajit Engineering (SUPRAJIT) FY27 consolidated operational EBITDA margin >= 11.7% (12% less 0.3 pp), as the company reports it', 'YES if the company-reported FY27 consolidated (operational) EBITDA margin >= 11.7%; if the company gives none, screener FY27 OPM governs.',
  doc('SUPRAJIT', 'result|presentation|transcript|press', ["EBITDA[^.\\n]{0,120}%"], "company operational EBITDA governs; fallback screener OPM; 11.7% floor", "2027-05-01", "2027-06-30", ">=", 11.7), '2027-06-30'),
 ('SUPRAJIT', 'fy27-gcm-ebitda-margin-9p7pct-plus', 'margin', '2026-11-12', '"our guidance of between 10% - 12% is very much intact, and I don\'t expect any change in that" (Global Cables & Mechatronics, Q2FY27)',
  'Suprajit Engineering (SUPRAJIT) FY27 Global Cables & Mechatronics (GCM) EBITDA margin >= 9.7% (10% less 0.3 pp)', 'YES if company-reported FY27 GCM EBITDA margin >= 9.7%.',
  doc('SUPRAJIT', 'result|presentation|transcript|press', ["(GCM|Global Cables)[^.\\n]{0,200}EBITDA[^.\\n]{0,80}%"], "segment margin; 9.7% floor", "2027-05-01", "2027-06-30", ">=", 9.7), '2027-06-30'),
 ('SUPRAJIT', 'fy27-gcm-revenue-growth-9p5pct-plus', 'revenue', '2026-11-12', '"maybe the second half may not be 22%, 24%, but we still see a strong double-digit growth based on the current commitments" (GCM, Q2FY27; Q1FY27 "Global Cables and Mechatronics will also have a double-digit growth")',
  'Suprajit Engineering (SUPRAJIT) FY27 Global Cables & Mechatronics (GCM) revenue growth >= 9.5%', 'YES if company-reported FY27 GCM revenue growth YoY >= 9.5%.',
  doc('SUPRAJIT', 'result|presentation|transcript|press', ["(GCM|Global Cables)[^.\\n]{0,200}(grew|growth)[^.\\n]{0,40}%"], "segment growth; 9.5% floor", "2027-05-01", "2027-06-30", ">=", 9.5), '2027-06-30'),
 ('SUPRAJIT', 'fy27-capex-190cr-plus', 'dates', '2026-11-12', '"We have said that this year our capex will be around INR200 crore" (Q2FY27; Q4FY26 "INR 200 crores")',
  'Suprajit Engineering (SUPRAJIT) FY27 capex >= Rs 190 cr (95% of Rs 200 cr)', 'YES if FY27 consolidated cash-flow purchase of property, plant & equipment (incl. CWIP and intangibles) or company-stated FY27 capex >= Rs 190 cr.',
  doc('SUPRAJIT', 'result|presentation|transcript', ["(capex|capital expenditure|purchase of property)[^.\\n]{0,120}[\\d,.]+"], "FY27 cash-flow statement; Rs 190 cr floor", "2027-05-01", "2027-06-30", ">=", 190), '2027-06-30'),
 ('SUPRAJIT', 'ev-2w-drum-brake-production-by-dec26', 'dates', '2026-11-12', '"this quarter actually we are going into production for our first drum brake system for a key EV two-wheeler in Bengaluru" (Q2FY27)',
  'Suprajit Engineering (SUPRAJIT) starts production of its first EV two-wheeler drum brake system by 31-Dec-2026', 'YES if the Q3FY27 call/presentation or a filing dated <= 15-Mar-2027 states series production/supplies of the EV two-wheeler drum brake began on or before 31-Dec-2026; a slip = NO.',
  doc('SUPRAJIT', 'transcript|presentation|result', ["drum brake[^.\\n]{0,200}(production|supplies|SOP)"], "event by 31-Dec-2026; read Q3FY27 call", "2027-01-20", "2027-03-15", typ="c", event_deadline="2026-12-31"), '2027-03-15'),
 ('LANDMARK', 'fy27-capex-76cr-plus', 'dates', '2026-11-13', '"it would be a little higher than that ... it would maybe another INR30 crores or so" (on the ~INR 50 cr FY27 capex guide, Q2FY27)',
  'Landmark Cars (LANDMARK) FY27 capex >= Rs 76 cr (95% of ~Rs 80 cr = Rs 50 cr guide + Rs 30 cr)', 'YES if FY27 consolidated cash-flow purchase of property, plant & equipment (incl. CWIP; excl. right-of-use assets) or company-stated FY27 capex >= Rs 76 cr.',
  doc('LANDMARK', 'result|presentation|transcript', ["(capex|capital expenditure|purchase of property)[^.\\n]{0,120}[\\d,.]+"], "FY27 cash-flow statement; Rs 76 cr floor", "2027-05-01", "2027-06-30", ">=", 76), '2027-06-30'),
 ('LANDMARK', 'mumbai-workshops-merged-by-feb27', 'dates', '2026-11-13', '"I spoke about three workshops becoming one in Mumbai, where I\'m sure we\'ll call you all maybe in the next 2-3 months" (Jogeshwari, Q2FY27)',
  'Landmark Cars (LANDMARK) opens the merged Mumbai (Jogeshwari) workshop replacing three workshops by 28-Feb-2027', 'YES if a filing, press release or the Q3/Q4 FY27 call dated <= 14-May-2027 states the consolidated Mumbai workshop was operational/inaugurated on or before 28-Feb-2027.',
  doc('LANDMARK', 'transcript|presentation|press|inaugur', ["(Jogeshwari|Mumbai)[^.\\n]{0,200}(workshop|inaugurat|operational)"], "event by 28-Feb-2027", "2027-02-15", "2027-05-14", typ="c", event_deadline="2027-02-28"), '2027-05-14'),
 ('LANDMARK', 'q4fy27-new-car-proforma-ebitda-1p2pct-plus', 'margin', '2026-08-12', 'Analyst: "quarter 3 and 4 will be a more normalized quarter with like an EBITDA margin of 1.5% on pro forma on new car sales?" CFO: "Yes, it would be a normalized quarter" (Q1FY27)',
  'Landmark Cars (LANDMARK) Q4FY27 new-car pro forma EBITDA margin >= 1.2% (1.5% less 0.3 pp), as the company reports it', 'YES if the company-reported new-vehicle (pro forma) EBITDA margin for Q4FY27 (Jan-Mar 2027) >= 1.2%.',
  doc('LANDMARK', 'result|presentation|transcript', ["new (car|vehicle)[^.\\n]{0,160}EBITDA[^.\\n]{0,80}%"], "company segment KPI; 1.2% floor", "2027-05-01", "2027-06-30", ">=", 1.2), '2027-06-30'),
]
