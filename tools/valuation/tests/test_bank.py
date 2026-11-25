"""Unit tests for bank mode v1.2 (CET1 book side by side, scenario-only dilution, J-curve ROE path; L41).
Synthetic inputs plus a regression on the stored FEDERALBNK / UTKARSHBNK worksheets. No network.

    python3 -m unittest discover -s tools/valuation/tests -v
"""
import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.dirname(HERE)
sys.path.insert(0, VAL)
import worksheet as ws  # noqa: E402
import bank  # noqa: E402

BASE = {
    "mode": "bank", "company": "Synthetic Bank", "ticker": "SYNB", "market": "india", "practice": True,
    "currency": "INR", "units": "INR cr", "as_of": "2026-11-25", "price": 100.0, "shares": 100.0,
    "book_value": 10000.0, "base": {"pat": 1200.0, "roe_reported": 0.12, "loans": 80000.0, "assets": 120000.0},
    "coe": 0.125, "terminal_growth": 0.05, "years": 10, "dispersion": 0.30, "payout": 0.10,
    "scenarios": [
        {"name": "bear", "prob": 0.30, "roe_start": 0.08, "roe_end": 0.11, "exit_pb": 0.8},
        {"name": "base", "prob": 0.55, "roe_start": 0.12, "roe_end": 0.14, "exit_pb": 1.2},
        {"name": "bull", "prob": 0.13, "roe_start": 0.15, "roe_end": 0.16, "exit_pb": 1.8},
    ],
    "blowup": {"prob": 0.02, "multiple": 0.2},
}


def run(mut=None):
    d = copy.deepcopy(BASE)
    if mut:
        mut(d)
    d = bank.normalise(d, ws.MARKET_DEFAULTS)
    return d, ws.run(d)


def scen(res, name):
    return next(x for x in res["scenarios"]["scenarios"] if x["name"] == name)


class TestBackwardCompatible(unittest.TestCase):
    def test_stored_worksheets_unchanged(self):
        for t in ("examples/FEDERALBNK", "live/UTKARSHBNK", "live/UTKARSHBNK_cet1book"):
            p = os.path.join(VAL, t + ".json")
            with open(os.path.join(VAL, t + "_worksheet.json")) as fh:
                old = json.load(fh)
            r = ws.run(ws.load_input(p))
            self.assertAlmostEqual(r["scenarios"]["ev_mult5"], old["scenarios"]["ev_mult5"], places=9, msg=t)
            self.assertAlmostEqual(r["reverse"]["irr_base"], old["reverse"]["irr_base"], places=9, msg=t)
            self.assertAlmostEqual(r["scenarios"]["pw_value"], old["scenarios"]["pw_value"], places=9, msg=t)

    def test_no_cet1_fields_without_input(self):
        _, r = run()
        self.assertIsNone(r["snapshot"]["p_cet1"])
        self.assertNotIn("cet1", r["scenarios"])
        self.assertNotIn("p_cet1", r["reverse"])

    def test_linear_path_default(self):
        self.assertEqual(bank.roe_series(0.1, 0.2, 3), [0.1, 0.15000000000000002, 0.2])


class TestCet1Book(unittest.TestCase):
    def setUp(self):
        self.d, self.r = run(lambda d: d.update(cet1_book=70.0))

    def test_side_by_side_snapshot_and_reverse(self):
        s, rv = self.r["snapshot"], self.r["reverse"]
        self.assertAlmostEqual(s["p_cet1"], 100 / 70.0)
        self.assertAlmostEqual(s["pb"], 1.0)
        self.assertAlmostEqual(s["cet1_gap_ps"], 30.0)
        # required ROE forever on CET1 book: g + P/C (CoE - g)
        self.assertAlmostEqual(rv["roe_implied_gordon_cet1"], 0.05 + (100 / 70.0) * 0.075)
        self.assertGreater(rv["roe_implied_gordon_cet1"], rv["roe_implied_gordon"])
        self.assertAlmostEqual(rv["roe_now_cet1"], 0.12 * 100 / 70.0)

    def test_value_basis_independent_multiple_is_not(self):
        _, r0 = run()
        for a, b in zip(r0["scenarios"]["scenarios"], self.r["scenarios"]["scenarios"]):
            self.assertAlmostEqual(a["value_ps"], b["value_ps"])
            self.assertAlmostEqual(a["mult5"], b["mult5"])           # primary stays on reported book
            self.assertLess(b["mult5_cet1"], b["mult5"])             # same exit P/B on a smaller book
            self.assertAlmostEqual(b["cet1_bvps5"], b["bvps5"] - 30.0)
            self.assertAlmostEqual(b["value_ps_deductions_worthless"], b["value_ps"] - 30.0)
        self.assertLess(self.r["scenarios"]["cet1"]["ev_mult5"], self.r["scenarios"]["ev_mult5"])

    def test_exit_p_cet1_given_and_rim(self):
        def m(d):
            d["cet1_book"] = 70.0
            d["scenarios"][1]["exit_p_cet1"] = 1.2 * 100 / 70.0
            d["scenarios"][2]["exit_p_cet1"] = "rim"
        _, r = run(m)
        b = scen(r, "base")
        self.assertEqual(b["exit_p_cet1_how"], "given")
        self.assertGreater(b["mult5_cet1"], scen(self.r, "base")["mult5_cet1"])
        u = scen(r, "bull")
        self.assertEqual(u["exit_p_cet1_how"], "rim")
        self.assertAlmostEqual(u["exit_p_cet1"], u["rim_p_cet1_5"])

    def test_book_basis_cet1_switches_primary(self):
        _, r = run(lambda d: d.update(cet1_book=70.0, book_basis="cet1"))
        sc = r["scenarios"]
        self.assertAlmostEqual(sc["ev_mult5"], sc["cet1"]["ev_mult5"])
        self.assertAlmostEqual(sc["reported"]["ev_mult5"], self.r["scenarios"]["ev_mult5"])

    def test_book_basis_cet1_needs_input(self):
        with self.assertRaises(ValueError):
            run(lambda d: d.update(book_basis="cet1"))

    def test_gap_runoff_raises_cet1_book(self):
        _, r = run(lambda d: d.update(cet1_book=70.0, cet1_gap_runoff_years=5))
        b = scen(r, "base")
        self.assertAlmostEqual(b["cet1_bvps5"], b["bvps5"])          # gap fully used up by year 5

    def test_render(self):
        md = ws.render(self.r)
        self.assertIn("P/CET1", md)
        self.assertIn("CET1 basis, side by side", md)


class TestScenarioDilution(unittest.TestCase):
    def test_bear_only_raise_below_book(self):
        _, r0 = run()

        def m(d):
            d["dilution"] = [{"name": "rescue raise", "scenarios": ["bear"], "year": 2, "cash_in": 2000.0,
                              "issue_price": 50.0}]
        _, r = run(m)
        self.assertLess(scen(r, "bear")["bvps5"], scen(r0, "bear")["bvps5"])
        self.assertLess(scen(r, "bear")["value_ps"], scen(r0, "bear")["value_ps"])
        self.assertAlmostEqual(scen(r, "bear")["share_mult5"], 1.4)
        for n in ("base", "bull"):
            self.assertAlmostEqual(scen(r, n)["bvps5"], scen(r0, n)["bvps5"])
            self.assertAlmostEqual(scen(r, n)["value_ps"], scen(r0, n)["value_ps"])
        self.assertAlmostEqual(r["snapshot"]["bvps"], r0["snapshot"]["bvps"])   # not applied up front
        self.assertIn("rescue raise", ws.render(r))

    def test_raise_at_book_with_roe_equal_coe_leaves_value_at_book(self):
        def m(d):
            d["payout"] = 0.0
            d["scenarios"] = [{"name": "flat", "prob": 0.98, "roe_start": 0.125, "roe_end": 0.125, "exit_pb": 1.0}]
            d["base_case"] = d["scenarios"][0]
            b1 = 100.0 * 1.125           # BVPS at the end of year 1 (no payout)
            d["dilution"] = [{"name": "at book", "scenarios": ["flat"], "year": 1, "shares": 10.0, "cash_in": 10.0 * b1}]
        _, r = run(m)
        self.assertAlmostEqual(scen(r, "flat")["value_ps"], 100.0, places=6)
        self.assertAlmostEqual(scen(r, "flat")["pv_dirty"], 0.0, places=9)

    def test_below_book_raise_dirty_surplus_negative(self):
        def m(d):
            d["dilution"] = [{"name": "cheap", "scenarios": ["base"], "year": 1, "shares": 50.0, "cash_in": 2500.0}]
        _, r = run(m)
        self.assertLess(scen(r, "base")["pv_dirty"], 0)

    def test_unknown_scenario_warns(self):
        d, _ = run(lambda d: d.update(dilution=[{"name": "x", "scenarios": ["nope"], "shares": 1.0}]))
        self.assertTrue(any("names no existing scenario" in w for w in d["_warnings"]))

    def test_upfront_entries_unchanged(self):
        d, r = run(lambda d: d.update(dilution=[{"name": "warrants", "shares": 10.0, "cash_in": 1000.0}]))
        self.assertAlmostEqual(r["snapshot"]["bvps"], 11000.0 / 110.0)


class TestRoePath(unittest.TestCase):
    def test_j_curve_shape(self):
        p = {"shape": "j", "trough": -0.04, "trough_year": 2, "recover_by": 6, "power": 1.0}
        s = bank.roe_series(0.04, 0.14, 10, bank._norm_path(p, "x"))
        self.assertAlmostEqual(s[0], 0.04)
        self.assertAlmostEqual(s[1], -0.04)
        self.assertEqual(min(s), s[1])
        self.assertTrue(all(abs(v - 0.14) < 1e-12 for v in s[5:]))
        self.assertTrue(all(b > a for a, b in zip(s[1:6], s[2:6])))

    def test_power_controls_speed(self):
        f = lambda pw: bank.roe_series(0.04, 0.14, 10, bank._norm_path(
            {"shape": "j", "trough": -0.04, "trough_year": 2, "recover_by": 8, "power": pw}, "x"))
        self.assertGreater(f(0.5)[3], f(1.0)[3])
        self.assertLess(f(2.0)[3], f(1.0)[3])

    def test_explicit_list_then_interpolates(self):
        s = bank.roe_series(0.1, 0.15, 6, [0.02, 0.05])
        self.assertEqual(s[:2], [0.02, 0.05])
        self.assertAlmostEqual(s[-1], 0.15)

    def test_j_curve_in_scenario_lowers_value_vs_linear(self):
        _, r0 = run()

        def m(d):
            d["scenarios"][0]["roe_path"] = {"shape": "j", "trough": -0.05, "trough_year": 2, "recover_by": 6, "power": 1.5}
        _, r = run(m)
        self.assertLess(scen(r, "bear")["value_ps"], scen(r0, "bear")["value_ps"])
        self.assertAlmostEqual(scen(r, "base")["value_ps"], scen(r0, "base")["value_ps"])
        self.assertIn("J-curve", ws.render(r))

    def test_bad_path_rejected(self):
        with self.assertRaises(ValueError):
            run(lambda d: d["scenarios"][0].update(roe_path={"shape": "j", "trough_year": 3, "recover_by": 2, "trough": 0}))
        with self.assertRaises(ValueError):
            run(lambda d: d["scenarios"][0].update(roe_path={"shape": "s"}))


if __name__ == "__main__":
    unittest.main()
