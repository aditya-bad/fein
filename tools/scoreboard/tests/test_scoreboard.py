"""Unit tests for tools/scoreboard (standard library unittest; no network).

    python3 -m unittest discover -s tools/scoreboard/tests -v
"""
import datetime as dt
import json
import math
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sb_common as C  # noqa: E402
import calls as K  # noqa: E402
import resolve as R  # noqa: E402
import scoreboard as S  # noqa: E402
import sources as SRC  # noqa: E402

D = dt.date


def call(i, p, base, o=None, method="base-rate", market="india", sector="fmcg", batch="batch1",
         resolve_by="2027-02-28", status="open", symbol="TEST"):
    return {"id": f"thesis:paper-call:{symbol}:c{i}", "ticker": symbol, "symbol": symbol, "market": market,
            "method": method, "probability": p, "base_rate_probability": base, "made_on": "2026-11-21",
            "resolve_by": resolve_by, "resolution_rule": "rule", "resolution_source": "", "sector": sector,
            "batch": batch, "title": f"call {i}", "status": status, "outcome": o,
            "data": {"resolved_on": "2027-02-01"} if o is not None else {}}


class Fake:
    """Stand-in for sources.Live: canned data, records every fetch."""

    def __init__(self, xbrl=None, scr=None, facts=None, yahoo=None, filings=None, pledge=None, docs=None, ann=None):
        self.xbrl, self.scr, self.facts = xbrl or {}, scr or {}, facts
        self.y, self.f, self.pl, self.docs, self.ann = yahoo or {}, filings or {}, pledge or [], docs or {}, ann or []
        self.calls = []

    def log(self, m):
        pass

    def india_xbrl(self, sym, basis, kind, end, first=True):
        self.calls.append("xbrl")
        v = self.xbrl.get((basis, kind, end))
        return dict(v, source="x", source_name="NSE integrated-filing XBRL", date="d") if v else None

    def screener_values(self, sym, basis, kind, end):
        self.calls.append("scr")
        v = self.scr.get((basis, kind, end))
        return dict(v, source="s", source_name="screener.in", date="d") if v else None

    def sec_facts(self, t):
        self.calls.append("sec")
        return self.facts

    def yahoo(self, sym, start, end, events="div|split"):
        self.calls.append("yahoo")
        return self.y[sym]

    def sec_filings(self, cik):
        self.calls.append("filings")
        return self.f.get(cik, [])

    def sec_cik(self, t):
        return 1

    def sec_filing_docs(self, cik, acc):
        return [("ex99.htm", "u:" + acc)]

    def nse_pledge_all(self):
        self.calls.append("pledge")
        return self.pl

    def nse_announcements(self, sym, frm, to):
        self.calls.append("ann")
        return self.ann

    def doc_text(self, url):
        return self.docs[url]


Q3 = D(2026, 12, 31)
OPM = {"type": "a", "auto": "structured", "kind": "india_fin", "metric": "opm_pct", "basis": "consolidated",
       "period": "Q", "end": "2026-12-31", "op": ">=", "threshold": 23.0, "round": 1, "guard": 0.3,
       "check_from": "2027-01-10"}


class TestScoring(unittest.TestCase):
    def test_brier_logloss_known_values(self):
        self.assertAlmostEqual(C.brier(0.8, 1), 0.04)
        self.assertAlmostEqual(C.brier(0.3, 0), 0.09)
        self.assertAlmostEqual(C.brier(0.5, 1), 0.25)
        self.assertAlmostEqual(C.logloss(0.8, 1), -math.log(0.8))
        self.assertAlmostEqual(C.logloss(0.0, 1), -math.log(0.01))   # clipped
        f = C.score_fields(0.6, 0.5, 0)
        self.assertEqual((f["brier"], f["brier_base"]), (0.36, 0.25))

    def test_metrics_and_skill(self):
        cs = [call(1, 0.8, 0.5, 1, status="resolved"), call(2, 0.3, 0.5, 0, status="resolved"),
              call(3, 0.6, 0.5, 0, status="resolved")]
        m = S.metrics(cs)
        self.assertEqual(m["n"], 3)
        self.assertAlmostEqual(m["brier"], (0.04 + 0.09 + 0.36) / 3)
        self.assertAlmostEqual(m["brier_base"], 0.25)
        self.assertAlmostEqual(m["skill"], 1 - ((0.49 / 3) / 0.25))
        self.assertEqual(m["wins"], 2)
        self.assertAlmostEqual(m["logloss_base"], math.log(2))

    def test_missing_base_excluded_from_skill(self):
        cs = [call(1, 0.9, None, 1, status="resolved"), call(2, 0.2, 0.4, 0, status="resolved")]
        m = S.metrics(cs)
        self.assertEqual((m["n"], m["n_base"]), (2, 1))
        self.assertAlmostEqual(m["brier"], (0.01 + 0.04) / 2)
        self.assertAlmostEqual(m["brier_paired"], 0.04)
        self.assertAlmostEqual(m["brier_base"], 0.16)

    def test_groups_and_calibration(self):
        cs = [call(1, 0.85, 0.5, 1, method="mgmt-tone", status="resolved"),
              call(2, 0.82, 0.5, 0, method="mgmt-tone", status="resolved"),
              call(3, 1.0, 0.9, 1, method="base-rate", status="resolved"),
              call(4, 0.05, 0.1, 0, method="base-rate", status="resolved")]
        g = S.by_group(cs, "method")
        self.assertAlmostEqual(g["mgmt-tone"]["brier"], (0.0225 + 0.6724) / 2)
        cal = S.calibration(cs)
        self.assertEqual(len(cal), 10)
        self.assertEqual(cal[8]["n"], 2)
        self.assertAlmostEqual(cal[8]["observed"], 0.5)
        self.assertEqual(cal[9]["n"], 1)      # p = 1.0 lands in the last bin
        self.assertEqual(cal[0]["n"], 1)
        md, s = S.build_report(cs + [call(9, 0.5, 0.5)], D(2027, 3, 1))
        self.assertIn("## Calibration (10 bins)", md)
        self.assertEqual((s["resolved"], s["open"]), (4, 1))

    def test_void_not_scored(self):
        cs = [call(1, 0.8, 0.5, 1, status="resolved"), call(2, 0.8, 0.5, None, status="void")]
        self.assertEqual(len(S.scored(cs)), 1)


class TestCurriculumBlock(unittest.TestCase):
    TEXT = "# Curriculum\n\n## Scoreboard\n| Date | x |\n|---|---|\n| a | b |\n\n## Next\nkeep me\n"

    def test_insert_then_replace_only_block(self):
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, "c.md")
            C.write_text(p, self.TEXT)
            S.update_curriculum(p, S.START + "\nv1\n" + S.END)
            t1 = C.read_text(p)
            self.assertIn("| a | b |\n\n" + S.START, t1)
            self.assertTrue(t1.endswith("## Next\nkeep me\n"))
            S.update_curriculum(p, S.START + "\nv2\n" + S.END)
            t2 = C.read_text(p)
            self.assertNotIn("v1", t2)
            self.assertEqual(t2.replace("v2", "v1"), t1)        # nothing else changed
            S.update_curriculum(p, S.START + "\nv2\n" + S.END)
            self.assertEqual(C.read_text(p), t2)                # idempotent


class TestClassifier(unittest.TestCase):
    def test_types(self):
        cases = {
            "YES if (ADBE close on 30-Jun-2027 ÷ 217.71) > (SPY close on 30-Jun-2027 ÷ 689.81).": "b",
            "YES if Optimum files a petition under Chapter 11 by 30-Jun-2027, per an 8-K.": "c",
            "YES if the FY27 cc revenue guidance announced with Q3 results has a midpoint strictly greater than 1.5%": "c",
            "YES if Q3 FY27 consolidated Operating Profit ÷ Sales on screener.in ≥23.0%": "a",
            "YES if NVIDIA's reported Q4 FY27 total revenue (8-K Item 2.02 earnings release) ≥ $133.9B.": "a",
            "YES if Tata Power states capacity added ≥2.5 GW (as Tata Power itself counts it)": "d",
            "YES if the NIM for Q4 is strictly greater than the NIM for Q3": "a",
        }
        for rule, t in cases.items():
            self.assertEqual(K.classify(rule)[0], t, rule)


def ind(sales, op):
    return {"sales_cr": sales, "op_profit_cr": op, "opm_pct": 100 * op / sales}


class TestIndiaResolver(unittest.TestCase):
    c = call(1, 0.42, 0.5)

    def test_not_due_uses_no_network(self):
        f = Fake()
        r = R.evaluate(self.c, OPM, f, D(2026, 11, 22))
        self.assertEqual(r["state"], "not_due")
        self.assertEqual(f.calls, [])

    def test_two_sources_agree(self):
        f = Fake(xbrl={("consolidated", "Q", Q3): ind(1000, 245)}, scr={("consolidated", "Q", Q3): ind(1000, 244)})
        r = R.evaluate(self.c, OPM, f, D(2027, 2, 1))
        self.assertEqual((r["state"], r["outcome"], r["confidence"]), ("resolved", 1, "verified"))

    def test_sources_disagree_goes_to_review(self):
        f = Fake(xbrl={("consolidated", "Q", Q3): ind(1000, 230.4)}, scr={("consolidated", "Q", Q3): ind(1000, 225.3)})
        r = R.evaluate(self.c, OPM, f, D(2027, 2, 1))
        self.assertEqual(r["state"], "review")
        self.assertIsNone(r["outcome"])

    def test_single_source_waits_until_resolve_by(self):
        f = Fake(xbrl={("consolidated", "Q", Q3): ind(1000, 210)})
        self.assertEqual(R.evaluate(self.c, OPM, f, D(2027, 2, 1))["state"], "waiting_data")
        r = R.evaluate(self.c, OPM, f, D(2027, 2, 28))
        self.assertEqual((r["state"], r["outcome"], r["confidence"]), ("resolved", 0, "single-source"))
        f2 = Fake(xbrl={("consolidated", "Q", Q3): ind(1000, 231)})       # 23.1%: inside the 0.3 guard
        self.assertEqual(R.evaluate(self.c, OPM, f2, D(2027, 3, 1))["state"], "review")

    def test_no_data_waits_then_overdue(self):
        self.assertEqual(R.evaluate(self.c, OPM, Fake(), D(2027, 1, 20))["state"], "waiting_data")
        r = R.evaluate(self.c, OPM, Fake(), D(2027, 3, 2))
        self.assertEqual(r["state"], "review")
        self.assertIn("OVERDUE", r["reason"])

    def test_company_reported_governs_near_threshold(self):
        sp = dict(OPM, threshold=22.0, guard=1.0, company_reported_governs=True)
        f = Fake(xbrl={("consolidated", "Q", Q3): ind(1000, 226)}, scr={("consolidated", "Q", Q3): ind(1000, 226)})
        self.assertEqual(R.evaluate(self.c, sp, f, D(2027, 2, 1))["state"], "review")
        f = Fake(xbrl={("consolidated", "Q", Q3): ind(1000, 240)}, scr={("consolidated", "Q", Q3): ind(1000, 240)})
        self.assertEqual(R.evaluate(self.c, sp, f, D(2027, 2, 1))["outcome"], 1)

    def test_growth_and_between(self):
        fy, fy0 = D(2027, 3, 31), D(2026, 3, 31)
        sp = dict(OPM, metric="sales_growth_pct", period="FY", end="2027-03-31", threshold=17.0, guard=0.5,
                  check_from="2027-04-15")
        c = call(2, 0.52, 0.55, resolve_by="2027-05-31")
        data = {("consolidated", "FY", fy): ind(1200, 100), ("consolidated", "FY", fy0): ind(1000, 90)}
        r = R.evaluate(c, sp, Fake(xbrl=data, scr=data), D(2027, 5, 10))
        self.assertEqual((r["state"], r["outcome"], r["value"]), ("resolved", 1, 20.0))
        sb = dict(OPM, metric="sales_cr", op="between", threshold=323, threshold_hi=371, guard=3, round=None)
        d2 = {("consolidated", "Q", Q3): ind(380, 40)}
        self.assertEqual(R.evaluate(self.c, sb, Fake(xbrl=d2, scr=d2), D(2027, 2, 10))["outcome"], 0)

    def test_pledge(self):
        sp = {"type": "a", "kind": "nse_pledge", "company_name": "Indo Tech Transformers Limited", "shp": "31-Mar-2027",
              "field": "percTotShares", "op": "<", "threshold": 57.93, "check_from": "2027-04-01"}
        c = call(3, 0.2, 0.3, resolve_by="2027-04-30")
        old = [{"comName": "Indo Tech Transformers Limited", "shp": "30-Sep-2026", "percTotShares": " 57.93"}]
        self.assertEqual(R.evaluate(c, sp, Fake(pledge=old), D(2027, 4, 10))["state"], "waiting_data")
        new = [{"comName": "Indo Tech Transformers Limited", "shp": "31-Mar-2027", "percTotShares": " 57.93"}]
        r = R.evaluate(c, sp, Fake(pledge=new), D(2027, 4, 20))
        self.assertEqual((r["state"], r["outcome"]), ("resolved", 0))     # no change = NO


def fact(val, start, end, form, filed, accn):
    return {"val": val, "start": start, "end": end, "form": form, "filed": filed, "accn": accn}


class TestSec(unittest.TestCase):
    FACTS = {"cik": 1, "facts": {"us-gaap": {"Revenues": {"units": {"USD": [
        fact(100.0, "2026-01-26", "2026-10-25", "10-Q", "2026-11-20", "q3"),
        fact(140.0, "2026-01-26", "2027-01-31", "10-K", "2027-02-26", "k1"),
        fact(90.0, "2025-01-27", "2026-01-25", "10-K", "2027-02-26", "k1"),
    ]}}}}}

    def test_q4_is_fy_minus_9m(self):
        v, e = R.sec_value(self.FACTS, "revenue", "Q4", "2027-01-31")
        self.assertEqual(v, 40.0)
        self.assertEqual(len(e), 2)
        g, _ = R.sec_value(self.FACTS, "revenue_growth_pct", "FY", "2027-01-31")
        self.assertAlmostEqual(g, 100 * (140 / 90 - 1))

    def test_op_margin_and_capex(self):
        f = {"cik": 1, "facts": {"us-gaap": {
            "Revenues": self.FACTS["facts"]["us-gaap"]["Revenues"],
            "OperatingIncomeLoss": {"units": {"USD": [fact(28.0, "2026-01-26", "2027-01-31", "10-K", "2027-02-26", "k1")]}},
            "PaymentsToAcquireProductiveAssets": {"units": {"USD": [fact(9.0, "2026-01-26", "2027-01-31", "10-K", "2027-02-26", "k1")]}}}}}
        m, e = R.sec_value(f, "op_margin_pct", "FY", "2027-01-31")
        self.assertAlmostEqual(m, 20.0)
        self.assertEqual(len(e), 2)
        self.assertEqual(R.sec_value(f, "capex", "FY", "2027-01-31")[0], 9.0)
        self.assertIsNone(R.sec_value(self.FACTS, "op_margin_pct", "FY", "2027-01-31"))   # no operating income tagged
        sp = {"type": "a", "kind": "sec_fact", "metric": "capex", "period": "FY", "fy_end": "2027-01-31",
              "op": "between", "threshold": 8.0, "threshold_hi": 9.0, "check_from": "2027-02-20"}
        r = R.evaluate(call(5, 0.6, 0.7, market="us", resolve_by="2027-03-10"), sp, Fake(facts=f), D(2027, 2, 27))
        self.assertEqual((r["state"], r["outcome"]), ("resolved", 1))

    def test_waits_for_10k(self):
        facts = {"cik": 1, "facts": {"us-gaap": {"Revenues": {"units": {"USD": self.FACTS["facts"]["us-gaap"]["Revenues"]["units"]["USD"][:1]}}}}}
        self.assertIsNone(R.sec_value(facts, "revenue", "Q4", "2027-01-31"))
        sp = {"type": "a", "kind": "sec_fact", "metric": "revenue", "period": "Q4", "fy_end": "2027-01-31",
              "op": ">=", "threshold": 41.0, "check_from": "2027-02-20"}
        c = call(4, 0.7, 0.85, market="us", resolve_by="2027-03-10")
        self.assertEqual(R.evaluate(c, sp, Fake(facts=facts), D(2027, 2, 21))["state"], "waiting_data")
        r = R.evaluate(c, sp, Fake(facts=self.FACTS), D(2027, 2, 27))
        self.assertEqual((r["state"], r["outcome"]), ("resolved", 0))


def bars(*pairs):
    return [(D.fromisoformat(a), b) for a, b in pairs]


class TestPriceAndEvents(unittest.TestCase):
    SP = {"type": "b", "kind": "price_relative", "symbol": "ABC", "bench": "SPY", "start": "2026-11-20",
          "end": "2027-06-30", "base_px": 100.0, "bench_px": 500.0, "check_from": "2027-07-02"}
    c = call(5, 0.42, 0.47, market="us", resolve_by="2027-06-30")

    def y(self, s_end, b_end, s0=100.0):
        return {"ABC": {"bars": bars(("2026-11-20", s0), ("2027-06-30", s_end), ("2027-07-01", 1)), "splits": [], "url": "y"},
                "SPY": {"bars": bars(("2026-11-20", 500.0), ("2027-06-30", b_end), ("2027-07-01", 1)), "splits": [], "url": "y"}}

    def test_price_relative(self):
        self.assertEqual(R.evaluate(self.c, self.SP, Fake(), D(2027, 6, 30))["state"], "not_due")
        r = R.evaluate(self.c, self.SP, Fake(yahoo=self.y(112.0, 550.0)), D(2027, 7, 2))
        self.assertEqual((r["state"], r["outcome"]), ("resolved", 1))       # +12% vs +10%
        r = R.evaluate(self.c, self.SP, Fake(yahoo=self.y(110.0, 550.0)), D(2027, 7, 2))
        self.assertEqual(r["outcome"], 0)                                   # tie is not "beats"
        r = R.evaluate(self.c, self.SP, Fake(yahoo=self.y(120.0, 550.0, s0=90.0)), D(2027, 7, 2))
        self.assertEqual(r["state"], "review")                              # start close != rule's base, no split
        stale = {k: {"bars": bars(("2026-11-20", v), ("2026-11-21", v)), "splits": [], "url": "y"}
                 for k, v in (("ABC", 100.0), ("SPY", 500.0))}
        r = R.evaluate(self.c, self.SP, Fake(yahoo=stale), D(2027, 7, 10))
        self.assertEqual((r["state"], r["outcome"]), ("review", None))      # never score on an old close

    def test_bankruptcy_8k(self):
        sp = {"type": "c", "kind": "sec_8k_item", "ciks": [7], "items": ["1.03"], "from": "2026-11-21",
              "deadline": "2027-06-30", "check_from": "2026-11-21"}
        c = call(6, 0.65, 0.55, market="us", resolve_by="2027-06-30")
        none = Fake(filings={7: [{"form": "8-K", "items": "2.02,9.01", "filingDate": "2027-02-10", "accessionNumber": "a"}]})
        self.assertEqual(R.evaluate(c, sp, none, D(2027, 3, 1))["state"], "waiting_data")
        r = R.evaluate(c, sp, none, D(2027, 7, 10))
        self.assertEqual((r["state"], r["proposal"]["outcome"]), ("review", 0))   # NO is only proposed
        hit = Fake(filings={7: [{"form": "8-K", "items": "1.03,9.01", "filingDate": "2027-03-03", "accessionNumber": "b"}]})
        r = R.evaluate(c, sp, hit, D(2027, 3, 4))
        self.assertEqual((r["state"], r["outcome"]), ("resolved", 1))

    def test_dividend(self):
        sp = {"type": "c", "kind": "yahoo_dividend", "symbol": "CAT", "min_amount": 1.745, "from": "2026-11-21",
              "deadline": "2027-06-30", "check_from": "2026-11-21"}
        c = call(7, 0.72, 0.75, market="us", resolve_by="2027-06-30")
        y = {"CAT": {"bars": [], "splits": [], "url": "y", "divs": [(D(2027, 1, 20), 1.63)]}}
        self.assertEqual(R.evaluate(c, sp, Fake(yahoo=y), D(2027, 3, 1))["state"], "waiting_data")
        y["CAT"]["divs"].append((D(2027, 7, 20), 1.76))
        self.assertEqual(R.evaluate(c, sp, Fake(yahoo=y), D(2027, 8, 1))["state"], "waiting_data")
        self.assertEqual(R.evaluate(c, sp, Fake(yahoo=y), D(2027, 9, 20))["state"], "review")
        y["CAT"]["divs"].append((D(2027, 6, 20), 1.76))
        r = R.evaluate(c, sp, Fake(yahoo=y), D(2027, 6, 21))
        self.assertEqual((r["state"], r["outcome"]), ("resolved", 1))

    def test_doc_scan_never_resolves(self):
        sp = {"type": "a", "kind": "doc_scan", "source": "nse", "symbol": "ICICIGI", "from": "2027-01-10",
              "subject": "result", "phrases": [r"combined ratio[^.\n]{0,60}?(\d{2,3}\.\d{1,2})\s?%"], "op": "<=",
              "threshold": 103.5, "check_from": "2027-01-10"}
        c = call(8, 0.55, 0.4, resolve_by="2027-02-15")
        ann = [{"desc": "Financial Results", "attchmntText": "results", "attchmntFile": "u1", "sort_date": "2027-01-20 18:00"}]
        f = Fake(ann=ann, docs={"u1": "The combined ratio for Q3 FY2027 was 102.9% vs 103.1%."})
        r = R.evaluate(c, sp, f, D(2027, 1, 21))
        self.assertEqual(r["state"], "review")
        self.assertIsNone(r["outcome"])
        self.assertEqual(r["proposal"]["outcome"], 1)
        self.assertAlmostEqual(r["proposal"]["value"], 102.9)
        r = R.evaluate(c, sp, Fake(ann=[]), D(2027, 1, 21))
        self.assertEqual(r["state"], "waiting_data")

    def test_word_numbers_in_snippets(self):
        sn, nums = R._snips("Organic sales also increased four percent versus the prior year.",
                            [r"[Oo]rganic sales[^.]{0,160}?(?:increased|grew)\s+(\d+(?:\.\d)?|[a-z]+)\s?(?:%|percent)"])
        self.assertEqual(nums, [4.0])


class TestSeedsAndDecisions(unittest.TestCase):
    def test_seed_record_and_merge(self):
        c = call(1, 0.7, 0.85)
        res = R.result("resolved", "ok", 0, 21.5, [R.ev(21.5, "https://x", "2027-02-01")], confidence="verified")
        rec = R.seed_record(c, OPM, res, D(2027, 2, 2), "auto:test")
        self.assertEqual((rec["id"], rec["type"], rec["status"]), (c["id"], "thesis", "resolved"))
        self.assertEqual(rec["data"]["outcome"], 0)
        self.assertAlmostEqual(rec["data"]["brier"], 0.49)
        self.assertAlmostEqual(rec["data"]["brier_base"], 0.7225)
        self.assertEqual(rec["sources"], ["https://x"])
        with tempfile.TemporaryDirectory() as t:
            p = R.write_seed([rec], D(2027, 2, 2), t)
            R.write_seed([rec, dict(rec, id="thesis:paper-call:Y:z")], D(2027, 2, 2), t)
            self.assertEqual(len(C.read_json(p)), 2)
            self.assertEqual(C.pending_seed_ids(t), {c["id"], "thesis:paper-call:Y:z"})

    def test_decisions(self):
        with tempfile.TemporaryDirectory() as t:
            p = os.path.join(t, "d.jsonl")
            C.write_text(p, '{"id": "a", "outcome": 1, "source": "https://s"}\n'
                               '{"id": "b", "outcome": 1}\n'                 # no source -> rejected
                               '{"id": "c", "outcome": "void", "note": "metric discontinued"}\n# comment\n')
            d = R.load_decisions(p)
            self.assertEqual(set(d), {"a", "c"})
            v = R.seed_record(call(2, 0.5, 0.5), None, R.decision_result(d["c"]), D(2027, 3, 1), "human:user")
            self.assertEqual(v["status"], "void")
            self.assertNotIn("brier", v["data"])

    def test_run_prefers_decision_and_skips_emitted(self):
        c1, c2 = call(1, 0.6, 0.5), call(2, 0.6, 0.5)
        rows = R.run([c1, c2], {}, Fake(), D(2027, 3, 1), {c1["id"]: {"id": c1["id"], "outcome": 1, "source": "s"}},
                     emitted={c2["id"]})
        self.assertEqual([r["state"] for _, _, r in rows], ["resolved", "skipped"])


class TestXbrl(unittest.TestCase):
    X = """<xbrli:context id="OneD"><xbrli:entity/><xbrli:period><xbrli:startDate>2026-10-01</xbrli:startDate>
    <xbrli:endDate>2026-12-31</xbrli:endDate></xbrli:period></xbrli:context>
    <xbrli:context id="FourD"><xbrli:entity/><xbrli:period><xbrli:startDate>2026-04-01</xbrli:startDate>
    <xbrli:endDate>2026-12-31</xbrli:endDate></xbrli:period></xbrli:context>
    <in-capmkt:RevenueFromOperations contextRef="OneD" unitRef="INR">10000000000</in-capmkt:RevenueFromOperations>
    <in-capmkt:Expenses contextRef="OneD" unitRef="INR">9000000000</in-capmkt:Expenses>
    <in-capmkt:FinanceCosts contextRef="OneD" unitRef="INR">100000000</in-capmkt:FinanceCosts>
    <in-capmkt:DepreciationDepletionAndAmortisationExpense contextRef="OneD" unitRef="INR">400000000</in-capmkt:DepreciationDepletionAndAmortisationExpense>
    <in-capmkt:RevenueFromOperations contextRef="FourD" unitRef="INR">30000000000</in-capmkt:RevenueFromOperations>"""

    def test_quarter_values(self):
        p = SRC.parse_nse_xbrl(self.X)
        v = SRC.xbrl_period_values(p, D(2026, 10, 1), D(2026, 12, 31))
        self.assertAlmostEqual(v["sales_cr"], 1000.0)
        self.assertAlmostEqual(v["op_profit_cr"], 1000 - (900 - 10 - 40))
        self.assertAlmostEqual(v["opm_pct"], 15.0)
        self.assertIsNone(SRC.xbrl_period_values(p, D(2026, 4, 1), D(2027, 3, 31)))   # FY not filed yet
        self.assertEqual(SRC.period_start("Q", D(2026, 12, 31)), D(2026, 10, 1))
        self.assertEqual(SRC.period_start("FY", D(2027, 3, 31)), D(2026, 4, 1))


class TestBankXbrl(unittest.TestCase):
    """IFBanking XBRL (banks): fixture = trimmed real UTKARSHBNK standalone Q2 FY27 filing (03-Nov-2026)."""
    FIX = os.path.join(HERE, "fixtures", "utkarshbnk_q2fy27_banking_xbrl.xml")
    Q2 = (D(2026, 7, 1), D(2026, 9, 30))

    def setUp(self):
        with open(self.FIX, encoding="utf-8") as f:
            self.text = f.read()
        self.p = SRC.parse_nse_xbrl(self.text)

    def test_bank_values_from_fixture(self):
        self.assertTrue(SRC.is_bank_xbrl(self.p))
        self.assertFalse(SRC.is_bank_xbrl(SRC.parse_nse_xbrl(TestXbrl.X)))
        self.assertIsNone(SRC.xbrl_period_values(self.p, *self.Q2))          # Ind AS path cannot read banks
        v = SRC.bank_period_values(self.p, *self.Q2)
        self.assertAlmostEqual(v["net_profit_cr"], -69.8522)
        self.assertAlmostEqual(v["interest_earned_cr"], 909.2562)
        self.assertAlmostEqual(v["nii_cr"], 909.2562 - 473.9499)
        self.assertAlmostEqual(v["opex_cr"], 917.0367 - 473.9499)
        self.assertAlmostEqual(v["ppop_cr"], 85.2439)
        self.assertAlmostEqual(v["gnpa_pct"], 5.96)                          # fraction 0.0596 -> %
        self.assertAlmostEqual(v["nnpa_pct"], 2.74)
        self.assertAlmostEqual(v["cet1_pct"], 12.78)
        self.assertAlmostEqual(v["advances_cr"], 19302.2407)                 # instant context at period end
        self.assertNotIn("crar_pct", v)                                      # total CRAR is not tagged
        h1 = SRC.bank_period_values(self.p, D(2026, 4, 1), D(2026, 9, 30))
        self.assertAlmostEqual(h1["net_profit_cr"], -103.7719)
        self.assertIsNone(SRC.bank_period_values(self.p, D(2026, 10, 1), D(2026, 12, 31)))   # not filed

    def _live(self, screener=None):
        text, end = self.text, self.Q2[1]

        class L(SRC.Live):
            def nse_filings(self, symbol):
                return [{"consolidated": "Standalone", "xbrl": "u", "qe_Date": "30-SEP-2026",
                         "type_Sub": "Original", "broadcast_Date": "03-Nov-2026 20:47:11"}]

            def screener_values(self, symbol, basis, kind, e):
                return dict(screener, source="s", source_name="screener.in", date="d") \
                    if screener and e == end else None
        orig = SRC.C.http_get
        SRC.C.http_get = lambda *a, **k: text
        self.addCleanup(setattr, SRC.C, "http_get", orig)
        return L(log=lambda m: None)

    def test_resolver_end_to_end_on_fixture(self):
        c = call(9, 0.45, 0.4, resolve_by="2026-11-30", symbol="UTKARSHBNK")
        gn = {"type": "a", "auto": "structured", "kind": "india_fin", "metric": "gnpa_pct", "basis": "standalone",
              "period": "Q", "end": "2026-09-30", "op": "<=", "threshold": 5.0, "round": 2, "guard": 0.1,
              "check_from": "2026-11-01"}
        r = R.evaluate(c, gn, self._live(), D(2026, 11, 20))
        self.assertEqual(r["state"], "waiting_data")                         # single source before resolve_by
        r = R.evaluate(c, gn, self._live(), D(2026, 11, 30))
        self.assertEqual((r["state"], r["outcome"], r["value"]), ("resolved", 0, 5.96))
        self.assertEqual(r["confidence"], "single-source")
        np_ = dict(gn, metric="net_profit_cr", op=">", threshold=0, guard=2, round=None)
        r = R.evaluate(c, np_, self._live({"sales_cr": 909, "op_profit_cr": -70, "net_profit_cr": -70}),
                       D(2026, 11, 20))
        self.assertEqual((r["state"], r["outcome"], r["confidence"]), ("resolved", 0, "verified"))
        self.assertEqual(r["evidence"][0]["source_name"], "NSE integrated-filing XBRL")
        r = R.evaluate(c, dict(np_, threshold=-69.9, op=">="), self._live({"sales_cr": 909, "op_profit_cr": -70,
                                                                             "net_profit_cr": -70}), D(2026, 11, 20))
        self.assertEqual(r["state"], "review")                               # XBRL -69.85 vs screener -70: sides differ

    def test_utkarsh_specs_now_structured(self):
        sp = C.load_specs()
        for k in ("q3fy27-net-profit-positive", "q4fy27-pat-67cr-plus", "gnpa-mar27-5pct-or-lower"):
            self.assertEqual(sp["thesis:paper-call:UTKARSHBNK:" + k]["auto"], "structured", k)
        for k in ("crar-mar27-16pct-plus", "fy27-glp-growth-25pct-plus"):               # not in IFBanking XBRL
            self.assertEqual(sp["thesis:paper-call:UTKARSHBNK:" + k]["auto"], "assisted", k)


class TestSpecs(unittest.TestCase):
    REQ = {"india_fin": {"metric", "basis", "period", "end", "op", "threshold"},
           "sec_fact": {"metric", "period", "fy_end", "op", "threshold"},
           "nse_pledge": {"company_name", "shp", "field", "op", "threshold"},
           "price_relative": {"symbol", "bench", "start", "end", "base_px", "bench_px"},
           "sec_8k_item": {"ciks", "items", "from", "deadline"},
           "yahoo_dividend": {"symbol", "min_amount", "from", "deadline"},
           "doc_scan": {"source", "phrases"}}

    def test_specs_well_formed(self):
        import re
        for i, s in C.load_specs().items():
            self.assertIn(s["type"], "abcd", i)
            self.assertIn(s["auto"], ("structured", "assisted", "human"), i)
            self.assertTrue(self.REQ[s["kind"]] <= set(s), i)
            self.assertTrue(s.get("check_from"), i)
            for rx in s.get("phrases", []):
                re.compile(rx)
            if s["kind"] == "doc_scan":
                self.assertNotEqual(s["auto"], "structured", i)   # text never auto-resolves


if __name__ == "__main__":
    unittest.main()
