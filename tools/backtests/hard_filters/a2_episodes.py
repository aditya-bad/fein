"""Part A: hand-coded, point-in-time episode table for every memdb case_study (2026-11-21).

One row per company-EPISODE (duplicate records such as hidden-trap-X / X and false-alarm-X / X are merged).
label: W = winner (>=3x from T), T = trap (fraud / blow-up / >70% loss from T, not recovered within 5y),
       FA = winner that our flags-judgment library recorded as a false alarm (counts as a winner in the matrix).
sub (traps): fraud | lev (leverage / business blow-up) | bust (valuation or cycle round-trip after a run).
T = episode start (the date an investor would have been deciding). For traps: the peak / last calm date
before the first public shock. For winners: the record's start (trough / IPO / start of the measured leg).

Judgment flags use ONLY facts the record (or a dated filing) shows were public before T.
Codes: "Y" fired pre-T (evidence quoted), "N" checked/no pre-T evidence, "U" cannot be established pre-T.
"later" notes say when a flag first became public after T (early-warning value, not counted as a hit).
Mechanical flags (CFO/PAT, debt+negative CFO, FCF, debtor days, other income) are NOT coded here; they are
computed by a3_case_metrics.py from screener.in (India) / SEC companyfacts (US) fiscal years public before T.

Rules (insight:disqualifiers, 20-Nov-2026 version):
 HARD  H1a fake-cash signal (cash yield << deposit rates; big cash + big borrowing; trustee/escrow cash)
       H1b economics implausible for the business (unexplained margin/ROCE/growth vs physics or the leader)
       H1c profits not verifiable by outsiders (profit inside partners/segments nobody can audit; ~1% margin
           pass-through revenue)
       H2  auditor resignation citing disagreement / denied information, or qualified/adverse opinion
       H2b (broad variant tested here) any of: auditor exit mid-term, restatement / SEC 8-K 4.02 non-reliance,
           regulator-assessed misstatement (e.g. RBI NPA divergence), delayed results, within 5 years before T
       H3  credit rating 'issuer not cooperating'
       H4  SME / Telegram pump pattern
       H5  material related-party cash leakage to promoter entities
 GRADED G1 promoter pledge >25% of promoter holding (or rising)      [Indian values from BSE SHP XBRL]
        G3 dilution / preferential allotments / repeated equity raises in the 2y before T
        G4 high P/E: trailing P/E > 50 at T (or > 2x own median where the record gives it)
"""

H = ["H1a", "H1b", "H1c", "H2", "H2b", "H3", "H4", "H5"]
G = ["G1", "G3", "G4"]


def E(id_, label, sub, mkt, key, T, lender=False, recs=(), outcome="", **f):
    d = {"id": id_, "label": label, "sub": sub, "mkt": mkt, "key": key, "T": T, "lender": lender,
         "records": list(recs) or ["case_study:" + id_], "outcome": outcome, "flags": {}, "ev": {}, "later": {}}
    for k in H + G:
        v = f.get(k, "N")
        if isinstance(v, tuple):
            d["flags"][k], d["ev"][k] = v
        else:
            d["flags"][k] = v
    d["later"] = f.get("later", {})
    d["note"] = f.get("note", "")
    return d


EPISODES = [
    # ------------------------------ TRAPS: fraud / governance ------------------------------
    E("satyam-2009", "T", "fraud", "IN", None, "2008-06-30", recs=["case_study:satyam-2009", "case_study:hidden-trap-satyam-cash"],
      outcome="Rs 544 -> Rs 6-7 (-98%)",
      H1a=("Y", "FY08 accounts: ~Rs 5,000 cr cash earning far below FD rates while carrying debt (CLSA's Sep-2008 note used the same public FY08 numbers)"),
      G1=("U", "pledge disclosure only mandatory from Jan-2009"),
      later={"H5": "16-Dec-2008 Maytas related-party deal (3 weeks before the confession, after ~60% of the fall)",
             "H2b": "World Bank debarment / director exits Dec-2008"}),
    E("vakrangee", "T", "fraud", "IN", "VAKRANGEE", "2018-01-15", recs=["case_study:vakrangee-manpasand", "case_study:hidden-trap-vakrangee-roce-debt-free"],
      outcome="Rs 515 -> ~Rs 5 (-99%)",
      H1b=("Y", "OPM 24-26% and ROCE ~40% (FY15-17) in a rural kiosk franchise; no comparable earns that"),
      later={"H2": "PwC resigned Apr-2018"}),
    E("manpasand", "T", "fraud", "IN", "MANPASAND", "2018-04-30", recs=["case_study:vakrangee-manpasand", "case_study:hidden-trap-manpasand-growth"],
      outcome="suspended / ~-100%",
      H1b=("Y", "growth 33-44% faster than category leader Frooti; publicly questioned by a fund manager Dec-2016 (judgment call)"),
      later={"H2": "Deloitte resigned May-2018 citing denied revenue/capex data; next auditor quit 2019"}),
    E("cox-and-kings-2019", "T", "fraud", "IN", "COXKINGS", "2018-01-15", recs=["case_study:cox-and-kings-2019", "case_study:hidden-trap-cox-and-kings-brand"],
      outcome="Rs 250-400 -> Rs 2-3 (-99%)",
      H1b=("Y", "advance-paid travel business carrying heavy debt + large receivables/advances in FY15-17 accounts (WC sign contradicts model; judgment)"),
      later={"H5": "PwC lender audit (2019-20) found Rs 4,367 cr siphoned"}),
    E("ricoh-india-2016", "T", "fraud", "IN", "517496", "2015-08-01", recs=["case_study:ricoh-india-2016", "case_study:hidden-trap-ricoh-india-mnc-growth"],
      outcome=">Rs 1,000 -> suspended (-90%+)",
      H1b=("U", "revenue surge far above parent; not dated precisely enough to call pre-T"),
      later={"H2b": "Q2 FY16 results delayed + auditor refused to sign (Nov-2015)"}),
    E("gitanjali-gems", "T", "fraud", "IN", "532715", "2018-01-15", recs=["case_study:hidden-trap-gitanjali-receivables"],
      outcome="-61% in 7 days Feb-2018, then delisted",
      H5=("Y", "FY17 annual report: group-company receivables ~33% of total receivables"),
      H2=("U", "Mar-2017 auditor warning of default to LIC (nature of opinion not established)")),
    E("rajesh-exports", "T", "fraud", "IN", "RAJESHEXPO", "2022-08-01", recs=["case_study:hidden-trap-rajesh-exports-low-pe"],
      outcome="~Rs 947 -> Rs 48 (-95%); SEBI interim order Jun-2026 (allegations)",
      H1c=("Y", "0.4-1.1% operating margin on Rs 1.6-2.6 lakh cr pass-through gold revenue (FY15-22): profit not verifiable"),
      H2=("U", "frequent auditor changes noted, dates not established")),
    E("reliance-capital-adag", "T", "fraud", "IN", "RELCAPITAL", "2018-01-15", lender=True, outcome="equity wiped (IBC 2025)",
      H5=("U", "GPCL loans to group shells jumped in FY18-19 (FY18 data public only after T)"),
      later={"H2": "PwC resigned 2019 citing unresolved concerns", "H5": "GPCL loans Rs 900 -> 7,900 cr"}),
    E("gensol-2025", "T", "fraud", "IN", "GENSOL", "2024-06-30", outcome="~Rs 900-1,100 -> ~Rs 100 (-90%)",
      note="worked mini-run in the forensic course used FY24 data (public May-2024, before T)",
      later={"H5": "SEBI interim order 15-Apr-2025 (EV-loan diversion)", "H3": "rating downgrades Mar-2025"}),
    E("brightcom", "T", "fraud", "IN", "BCG", "2022-01-10", outcome="SEBI found ~Rs 1,280 cr inflated profit FY19-20; stock -90%+",
      G3=("U", "preferential allotments 2021-22 not in the record")),
    E("dhfl-2019", "T", "fraud", "IN", None, "2018-09-01", lender=True, recs=["case_study:dhfl-2019", "case_study:hidden-trap-dhfl-growth"],
      outcome="Rs 690 -> equity wiped", note="ALM mismatch (15-20y loans on short CP) is not in our rule set",
      later={"H5": "Cobrapost Jan-2019 (Rs 31,000 cr to promoter-linked shells)"}),
    E("yes-bank-2020", "T", "fraud", "IN", "YESBANK", "2018-08-20", lender=True, recs=["case_study:yes-bank-2020", "case_study:hidden-trap-yes-bank-roe"],
      outcome="Rs 393-404 -> Rs 5.6 (-98%)",
      H2b=("Y", "RBI-assessed NPA divergence Rs 4,177 cr (FY16) / Rs 6,355 cr (FY17), disclosed 2017"),
      later={"H2b": "RBI refused CEO extension Sep-2018"}),
    E("zee-essel-pledges-2019", "T", "lev", "IN", "ZEEL", "2018-01-15", outcome="~Rs 600 -> ~Rs 120 (Mar-2020), -80%",
      later={"H5": "letter of comfort / FD for group loans surfaced 2019"}),
    E("future-group-2020", "T", "lev", "IN", "FRETAIL", "2018-08-31", outcome="~Rs 550-600 -> Rs 2-5 (-99%)"),
    E("pc-jeweller-2018", "T", "lev", "IN", "PCJEWELLER", "2018-01-15", recs=["case_study:pc-jeweller-2018", "case_study:hidden-trap-pc-jeweller-inventory"],
      outcome="~Rs 600 -> teens (-95%+)",
      later={"H5": "promoter share 'gifts' Apr-2018; buyback withdrawn Jul-2018"}),
    E("adani-hindenburg-2023", "T", "lev", "IN", "ADANIENT", "2023-01-23", outcome="ADANIENT -70% (3,400 -> 1,017); allegations later closed by SEBI (RPT)",
      G4=("Y", "'very high P/E/P/B on capital-intensive businesses' (record)")),
    E("jet-airways-2019", "T", "lev", "IN", "JETAIRWAYS", "2018-01-15", outcome="~Rs 900 -> ~Rs 30 (-97%), liquidated",
      note="negative net worth for years: not in our rule set", later={"H2b": "Q1 FY19 results deferred Aug-2018"}),
    E("kingfisher-ub-2012", "T", "lev", "IN", "KFA", "2008-06-30", outcome="equity ~-99%", note="losses every year; negative net worth"),
    E("ilfs-2018", "T", "lev", "IN", "IL&FSTRANS", "2018-01-15", outcome="ITNL -90%+", note="interest cover <1x not in our rule set"),
    E("unitech-2008", "T", "lev", "IN", None, "2008-01-15", outcome="Rs 547 -> Rs 7 (-99%)"),
    E("suzlon", "T", "lev", "IN", None, "2008-01-15", outcome="Rs 431 -> Rs 1.5 (-99.6%)"),
    E("paytm-ipo-2021", "T", "lev", "IN", "PAYTM", "2021-11-18", outcome="Rs 2,150 -> ~Rs 440 (-79%) by Nov-2022",
      G4=("U", "loss-making: P/E undefined; ~50x sales")),
    E("sme-ipo-manipulation-2024-25", "T", "fraud", "IN", None, "2023-06-30", outcome="multiple SEBI orders; issues collapsed",
      H4=("Y", "circular: H4 was written from this very case set"), note="basket, not a single company"),
    E("wirecard-2020", "T", "fraud", "GL", None, "2018-09-04", recs=["case_study:wirecard-2020", "case_study:hidden-trap-wirecard-margins-cash"],
      outcome="EUR 190 -> EUR 1-3 (-99%)",
      H1c=("Y", "~half of profits via Asian third-party acquirers it did not control; FT 2015 / Zatarra 2016"),
      later={"H1a": "trustee-held EUR 1.9 bn cash (KPMG Apr-2020; EY Jun-2020)"}),
    E("luckin-coffee-2020", "T", "fraud", "GL", "LK", "2020-01-15", recs=["case_study:luckin-coffee-2020", "case_study:hidden-trap-luckin-growth"],
      outcome="$50 -> ~$1.4 (-97%)",
      G1=("Y", "chairman/founders pledged most shares for margin loans (IPO/follow-on filings)"),
      G3=("Y", "follow-on + convertible within months of the May-2019 IPO"),
      later={"H1b": "Muddy Waters store-video report 31-Jan-2020"}),
    E("evergrande-2021", "T", "lev", "GL", None, "2018-01-15", outcome="HK$30 -> HK$0.16, delisted (-99.5%)"),
    E("credit-suisse-2023", "T", "lev", "GL", None, "2021-01-04", lender=True, outcome="-94% to the UBS rescue",
      note="serial scandals = culture flag, not in our rule set", later={"H2b": "material weakness (PwC) Mar-2023"}),
    E("svb-2023", "T", "lev", "US", "SIVB", "2021-11-15", lender=True, outcome="$760 -> 0"),
    E("lehman-2008", "T", "lev", "US", None, "2007-02-01", lender=True, outcome="$86 -> ~0"),
    E("ge-2017-2018", "T", "lev", "US", "GE", "2016-07-01", recs=["case_study:ge-2017-2018", "case_study:hidden-trap-ge-smooth-earnings"],
      outcome="$32 -> $6.7 (-79%)"),
    E("valeant-2015", "T", "fraud", "US", "BHC", "2015-08-05", recs=["case_study:valeant-2015", "case_study:hidden-trap-valeant-eps-growth"],
      outcome="$262 -> ~$8 (-97%)", later={"H5": "undisclosed Philidor channel revealed Oct-2015"}),
    E("worldcom-2002", "T", "fraud", "US", None, "1999-06-30", outcome="$64 -> ~0"),
    E("enron-2001", "T", "fraud", "US", None, "2000-08-23", outcome="$90 -> <$1",
      H5=("U", "LJM/CFO-run SPEs were footnoted in the 1999 10-K but the record does not date the disclosure")),
    E("nikola-2020", "T", "fraud", "US", None, "2020-06-08", outcome="$94 -> ~0",
      note="pre-revenue SPAC mega-cap: a pump pattern our H4 (SME/Telegram) does not cover"),
    # ------------------------------ TRAPS: busts after a winning run ------------------------------
    E("super-micro-bust", "T", "bust", "US", "SMCI", "2024-03-08", recs=["case_study:super-micro-2023-2026"], outcome="-86% (Mar-Nov 2024)",
      H2b=("Y", "SEC 8-K item 4.02 non-reliance 15-Nov-2018; 2018 Nasdaq delisting for late filings; 2020 SEC settlement"),
      H5=("U", "related-party suppliers disclosed; leakage not established")),
    E("enphase-bust", "T", "bust", "US", "ENPH", "2022-12-05", recs=["case_study:enphase-2016-2025"], outcome="-90%",
      G4=("Y", "P/E ~100 at the peak (record)")),
    E("celsius-bust", "T", "bust", "US", "CELH", "2024-05-01", recs=["case_study:celsius-2020-2025"], outcome="-73% to -79%",
      H2b=("Y", "8-K 4.02 non-reliance 1-Mar-2022 (restatement; stock-comp, unrelated to the bust)"),
      G4=("Y", "P/E near 100 [unverified]")),
    E("novo-bust", "T", "bust", "GL", None, "2024-06-25", recs=["case_study:novo-nordisk-glp1-2016-2026"], outcome="-73%",
      G4=("N", "P/E ~40-45")),
    E("kpit-bust", "T", "bust", "IN", "KPITTECH", "2024-07-15", recs=["case_study:kpit-technologies-2020-2024"], outcome="-74%",
      G4=("Y", "P/E 86")),
    E("tata-elxsi-bust", "T", "bust", "IN", "TATAELXSI_sa", "2022-08-15", recs=["case_study:tata-elxsi-2009-2022"], outcome="-70%",
      G4=("Y", "P/E 103")),
    E("alkyl-amines-bust", "T", "bust", "IN", "ALKYLAMINE", "2021-07-15", recs=["case_study:alkyl-amines-2009-2021"], outcome="-71%",
      G4=("Y", "P/E 76")),
    E("symphony-bust", "T", "bust", "IN", "SYMPHONY", "2018-01-15", recs=["case_study:symphony-2009-2018"], outcome="-77%",
      G4=("Y", "P/E 84")),
    E("amazon-dotcom-bust", "T", "bust", "US", None, "1999-12-10", recs=["case_study:amazon-drawdown"], outcome="-94%, peak regained 2009",
      G4=("U", "loss-making")),
    # ------------------------------ WINNERS ------------------------------
    E("nvidia", "W", "", "US", "NVDA", "2016-01-04", outcome="~300x"),
    E("radico-khaitan", "W", "", "IN", "RADICO", "2017-03-31", outcome="~38x", G4=("N", "P/E ~18")),
    E("palantir-2022-2026", "W", "", "US", "PLTR", "2022-12-28", outcome="~35x peak", G4=("N", "loss/first profit; P/S 8.5")),
    E("hermes-lvmh-2009-2025", "W", "", "GL", None, "2009-03-09", outcome="~22-30x"),
    E("costco-2009-2026", "W", "", "US", "COST", "2009-03-09", recs=["case_study:costco-2009-2026", "case_study:false-alarm-costco-thin-margins-high-pe"],
      outcome="~29x", G4=("N", "P/E ~15 at T")),
    E("tsmc-2012-2026", "W", "", "GL", None, "2012-01-03", outcome="~24x", G4=("N", "~12-15x")),
    E("super-micro-2023-2026", "W", "", "US", "SMCI", "2023-01-03", outcome="~17-30x to Mar-2024 (then -86%)",
      H2b=("Y", "8-K 4.02 non-reliance Nov-2018 (within 5y); 2018 delisting; 2020 SEC accounting settlement"),
      G4=("N", "P/E ~10 at T")),
    E("constellation-software-2006-2026", "W", "", "GL", None, "2006-05-18", outcome="~300x"),
    E("axon-2017-2025", "W", "", "US", "AXON", "2017-04-05", outcome="~35x"),
    E("novo-nordisk-glp1-2016-2026", "W", "", "GL", None, "2021-01-04", outcome="~4x (2021-24)"),
    E("booking-priceline-2002-2025", "W", "", "US", None, "2002-10-01", outcome="~800x"),
    E("eli-lilly-2018-2025", "W", "", "US", "LLY", "2018-01-02", outcome="~10-13x", G4=("N", "~20x")),
    E("netflix-2002-2025", "W", "", "US", "NFLX", "2012-09-28", outcome="~150x from the 2012 low"),
    E("amd-2014-2025", "W", "", "US", "AMD", "2015-10-01", outcome="~140x"),
    E("shopify-2015-2025", "W", "", "GL", None, "2015-05-21", outcome="~100x to 2021"),
    E("enphase-2016-2025", "W", "", "US", "ENPH", "2017-06-30", outcome="~400x to 2022"),
    E("meta-2022-trough-rebound", "W", "", "US", "META", "2022-11-04", outcome="~9x", G4=("N", "P/E ~9")),
    E("mercadolibre-2007-2025", "W", "", "GL", None, "2007-08-10", outcome="~130x"),
    E("microsoft-nadella-2014-2025", "W", "", "US", "MSFT", "2014-02-04", outcome="~15x", G4=("N", "P/E ~13-15")),
    E("celsius-2020-2025", "W", "", "US", "CELH", "2020-03-16", outcome="~60-70x to 2024",
      H2b=("U", "8-K 4.01 auditor change May-2017; reason not read")),
    E("tesla-2010-2024", "W", "", "US", "TSLA", "2019-06-03", recs=["case_study:tesla-2010-2024", "case_study:false-alarm-tesla-losses-dilution"],
      outcome="~35x to 2021", G3=("Y", "repeated equity raises incl. May-2019 raise"), G4=("U", "loss-making")),
    E("monster-beverage-2002-2024", "W", "", "US", None, "2003-01-02", outcome="~1,000x"),
    E("apple-2016-2023-buffett", "W", "", "US", "AAPL", "2016-05-12", outcome="~8x", G4=("N", "P/E ~10-11")),
    E("apple-2003-2012", "W", "", "US", None, "2003-04-17", outcome="~110x"),
    E("dominos-2008-2021", "W", "", "US", "DPZ", "2010-01-04", outcome="~65x from 2010", G4=("N", "~10x")),
    E("amazon-1997-2021-compounding", "W", "", "US", None, "1997-05-15", recs=["case_study:amazon-1997-2021-compounding", "case_study:false-alarm-amazon-no-profits-capex"],
      outcome="~2,500x", G4=("U", "no profits")),
    E("asml-2012-2024", "W", "", "GL", None, "2012-07-10", outcome="~22x", G4=("N", "~20x")),
    E("bse-ltd-2020-2026", "W", "", "IN", "BSE", "2020-03-31", outcome="~91x", G4=("N", "P/E 14")),
    E("kaynes-technology-2022-2026", "W", "", "IN", "KAYNES", "2022-11-21", recs=["case_study:kaynes-technology-2022-2026", "case_study:kaynes-2025"],
      outcome="~10x (then -62%)", G4=("Y", "IPO P/E 104")),
    E("suzlon-turnaround-2020-2024", "W", "", "IN", "SUZLON", "2020-03-31", outcome="~49x",
      H3=("U", "2019-20 lender restructuring / D ratings; 'not cooperating' status not established"), G4=("U", "loss-making")),
    E("hal-2020-2024", "W", "", "IN", "HAL", "2020-05-31", recs=["case_study:hal-2020-2024", "case_study:false-alarm-hal-receivable-days"],
      outcome="~22x", G4=("N", "P/E 6.3")),
    E("dixon-technologies-2019-2025", "W", "", "IN", "DIXON", "2019-08-31", outcome="~47x", G4=("N", "P/E 39.5")),
    E("cdsl-2019-2024", "W", "", "IN", "CDSL", "2019-08-31", outcome="~21x", G4=("N", "P/E 16.7")),
    E("cochin-shipyard", "W", "", "IN", "COCHINSHIP", "2020-05-31", recs=["case_study:indian-shipyards-2020-2025"], outcome="~25x", G4=("N", "P/E 5.5")),
    E("mazagon-dock", "W", "", "IN", "MAZDOCK", "2020-10-12", recs=["case_study:indian-shipyards-2020-2025"], outcome="~42x", G4=("N", "P/E 7.1")),
    E("trent-2020-2024", "W", "", "IN", "TRENT", "2020-05-31", recs=["case_study:trent-2020-2024", "case_study:false-alarm-trent-150x-pe-and-lease-debt"],
      outcome="~19x", G4=("Y", "trailing P/E 155 (COVID-depressed EPS)")),
    E("kpit-technologies-2020-2024", "W", "", "IN", "KPITTECH", "2020-03-31", outcome="~42x", G4=("N", "P/E 8.5")),
    E("polycab-2019-2026", "W", "", "IN", "POLYCAB", "2019-04-16", outcome="~16x", G4=("N", "P/E 26.9")),
    E("alkyl-amines-2009-2021", "W", "", "IN", "ALKYLAMINE", "2019-01-15", outcome="14x (2019-21 leg; ~560x from 2009)", G4=("N", "P/E 18.6")),
    E("deepak-nitrite-2009-2021", "W", "", "IN", "DEEPAKNTR", "2018-06-30", outcome="12x (2018-21 leg)", G4=("Y", "P/E ~69 (EPS about to rise 20x)")),
    E("symphony-2009-2018", "W", "", "IN", None, "2012-01-02", outcome="19x (2012-18)", G4=("N", "P/E 15")),
    E("garware-technical-fibres-2013-2024", "W", "", "IN", None, "2013-01-01", outcome="~94x", G4=("N", "P/E 4.9")),
    E("avanti-feeds-2009-2017", "W", "", "IN", None, "2011-01-03", outcome="~400x", G4=("N", "P/E 12.6")),
    E("apl-apollo-2009-2026", "W", "", "IN", None, "2009-03-31", recs=["case_study:apl-apollo-2009-2026", "case_study:false-alarm-apl-apollo-low-margins"],
      outcome="~670x", G4=("N", "P/E 5")),
    E("caplin-point-2009-2026", "W", "", "IN", "CAPLIPOINT", "2020-03-31", outcome="~12x (2020-26 leg; ~1,800x from 2009)", G4=("N", "P/E ~10-13")),
    E("titan-2009-2026", "W", "", "IN", None, "2009-03-31", recs=["case_study:titan-2009-2026", "case_study:false-alarm-titan-negative-cfo-gold-loans"],
      outcome="~130x", G4=("N", "P/E 20.8"), note="the false-alarm record computed CFO/PAT over FY15-26 = hindsight relative to T"),
    E("balkrishna-industries-2009-2024", "W", "", "IN", None, "2009-03-31", outcome="~266x", G4=("N", "P/E 2.2")),
    E("bajaj-finance-2009-2021", "W", "", "IN", None, "2009-03-31", lender=True, recs=["case_study:bajaj-finance-2009-2021", "case_study:false-alarm-bajaj-finance-negative-cfo-qips"],
      outcome="~1,570x", G4=("N", "P/E 9")),
    E("astral-2009-2024", "W", "", "IN", None, "2009-03-31", outcome="~1,590x", G4=("N", "P/E 7.9")),
    E("tata-elxsi-2009-2022", "W", "", "IN", "TATAELXSI_sa", "2020-03-31", outcome="17x (2020-22 leg)", G4=("N", "P/E 15")),
    E("la-opala-2009-2015", "W", "", "IN", None, "2009-03-31", outcome="~198x", G4=("N", "P/E 17.5")),
    E("pidilite-2008-2026", "W", "", "IN", None, "2008-10-31", outcome="~80x", G4=("N", "P/E 15.7")),
    E("eicher-motors", "W", "", "IN", None, "2008-10-31", outcome="~196x", G4=("N", "P/E 12.8")),
    E("page-industries-2007-2022", "W", "", "IN", None, "2007-03-31", outcome="~197x", G4=("N", "P/E 26.6")),
    # ------------------------------ FALSE-ALARM-only episodes (winners that fired graded flags) ------------------------------
    E("false-alarm-info-edge-losses-low-roce", "FA", "", "IN", None, "2006-11-21", outcome="~40x"),
    E("false-alarm-eternal-zomato-losses-dilution", "FA", "", "IN", "ETERNAL", "2022-07-27", outcome="~7.8x from 2022 low",
      G3=("Y", "Blinkit share-swap approved Jun-2022; IPO + pre-IPO raises 2021"), G4=("U", "loss-making")),
    E("false-alarm-consumer-franchises-long-high-pe", "FA", "", "IN", None, "2005-01-03", outcome="Asian Paints ~90x, Pidilite ~148x, Page ~197x",
      G4=("U", "P/E 40-60 for years; value at the 2005 start not given")),
    E("false-alarm-reliance-jio-debt", "FA", "", "IN", None, "2016-06-30", outcome="~5.9x"),
    E("false-alarm-bharti-airtel-losses-debt", "FA", "", "IN", "BHARTIARTL", "2019-12-31", outcome="~4.8x from Dec-2019",
      G3=("Y", "~Rs 25,000 cr rights May-2019 (+ QIP/FCCB Jan-2020)"), G4=("U", "loss after the AGR provision")),
    E("false-alarm-hdfc-bank-expensive-bank", "FA", "", "IN", None, "2005-01-03", lender=True, outcome="~35x", G4=("N", "P/E 23-38, median 26")),
    E("false-alarm-netflix-negative-fcf", "FA", "", "US", "NFLX", "2019-12-31", outcome="~3.7x to 2025"),
    E("false-alarm-apollo-hospitals-promoter-pledge", "FA", "", "IN", "APOLLOHOSP", "2019-07-31", outcome="~7x"),
    E("false-alarm-dmart-permanent-high-pe", "FA", "", "IN", "DMART", "2017-03-21", outcome="~11.7x from IPO",
      G4=("Y", "P/E never below 66 since listing")),
]

EXCLUDED = {
    "case_study:porinju-2018-drawdown": "PMS fund drawdown, not a company episode",
    "case_study:archegos-ltcm": "funds, not listed companies",
    "case_study:capital-goods-2007": "sector index",
    "case_study:defence-psu-rerating": "sector theme",
    "case_study:jane-street-sebi-2025": "regulatory case on a trading firm",
    "case_study:india-psu-rally-2023-24": "sector rally",
    "case_study:india-ipo-mania-2021": "basket; Paytm and Eternal covered individually",
    "case_study:india-bull-2003-08": "market cycle",
    "case_study:franklin-templeton-debt-2020": "debt mutual fund",
    "case_study:karvy-2019": "unlisted broker (custody risk)",
    "case_study:byjus-2022-2024": "private company",
    "case_study:ftx-2022": "private company",
    "case_study:theranos-2015": "private company",
    "case_study:waaree-premier-energies-2024-2026": "neither winner (0.8x from first close) nor >70% loss",
}
