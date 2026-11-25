"""Unit tests for decision card v1.2: survival cap (L35) and outside-view tail anchoring (L36).
Synthetic inputs only; no network.

    python3 -m unittest discover -s tools/decision/tests -v
"""
import copy
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
DEC = os.path.dirname(HERE)
sys.path.insert(0, DEC)
import decision_card as dc  # noqa: E402

SYN_CARD = os.path.join(DEC, "examples", "SYNTHETIC_card.json")


class TestSurvivalCap(unittest.TestCase):
    def test_not_india_never_triggers(self):
        r = dc.survival_cap("us", True, {"pledge_pct_of_promoter": 0.9, "interest_cover": 0.5})
        self.assertEqual(r["status"], "n/a")
        self.assertFalse(r["blocks"])

    def test_pead_inactive_caps_not_blocks(self):
        # v1.3 (L39): outside the PEAD window the red flag caps size instead of blocking
        r = dc.survival_cap("india", False, {"pledge_pct_of_promoter": 0.9, "interest_cover": 0.5})
        self.assertEqual(r["status"], "TRIGGERED")
        self.assertEqual(r["mode"], "cap")
        self.assertFalse(r["blocks"])
        self.assertEqual(r["cap_size"], dc.SURVIVAL_MIN_SIZE)

    def test_pead_inactive_clear(self):
        r = dc.survival_cap("india", False, {"pledge_pct_of_promoter": 0.1, "interest_cover": 4.0})
        self.assertEqual(r["status"], "clear")
        self.assertIsNone(r["mode"])

    def test_pead_inactive_unchecked_caps(self):
        r = dc.survival_cap("india", False, {"interest_cover": 4.0})
        self.assertEqual(r["status"], "UNCHECKED")
        self.assertEqual(r["mode"], "cap")

    def test_financial_skips_interest_cover(self):
        r = dc.survival_cap("india", False, {"pledge_pct_of_promoter": 0.0, "interest_cover": 1.1, "is_financial": True})
        self.assertEqual(r["status"], "clear")
        r = dc.survival_cap("india", False, {"pledge_pct_of_promoter": 0.0, "is_financial": True})
        self.assertEqual(r["status"], "clear")

    def test_pledge_trigger(self):
        r = dc.survival_cap("india", True, {"pledge_pct_of_promoter": 0.30, "interest_cover": 5.0})
        self.assertEqual(r["status"], "TRIGGERED")
        self.assertTrue(r["blocks"])

    def test_icr_trigger(self):
        r = dc.survival_cap("india", True, {"pledge_pct_of_promoter": 0.0, "interest_cover": 1.2})
        self.assertEqual(r["status"], "TRIGGERED")

    def test_thresholds_are_strict(self):
        r = dc.survival_cap("india", True, {"pledge_pct_of_promoter": 0.25, "interest_cover": 1.5})
        self.assertEqual(r["status"], "clear")
        self.assertFalse(r["blocks"])

    def test_s5_alone_does_not_trigger(self):
        r = dc.survival_cap("india", True, {"pledge_pct_of_promoter": 0.0, "interest_cover": 8.0, "s5_india": "fired"})
        self.assertEqual(r["status"], "clear")

    def test_unchecked_treated_as_triggered(self):
        r = dc.survival_cap("india", True, {"interest_cover": 8.0})
        self.assertEqual(r["status"], "UNCHECKED")
        self.assertTrue(r["blocks"])

    def test_already_owned_flag_carried(self):
        r = dc.survival_cap("india", True, {"pledge_pct_of_promoter": 0.6, "interest_cover": 3, "already_owned": True})
        self.assertTrue(r["already_owned"])


class TestAnchoring(unittest.TestCase):
    def test_weight_default(self):
        self.assertEqual(dc.anchor_weight(None)[0], 0.5)
        self.assertEqual(dc.anchor_weight({})[0], 0.5)

    def test_lower_weight_needs_evidence(self):
        self.assertEqual(dc.anchor_weight({"base_weight": 0.3})[0], 0.5)
        self.assertEqual(dc.anchor_weight({"base_weight": 0.3, "evidence": "net cash, 40-yr record"})[0], 0.3)

    def test_weight_floor_and_cap(self):
        self.assertEqual(dc.anchor_weight({"base_weight": 0.1, "evidence": "x"})[0], 0.25)
        self.assertEqual(dc.anchor_weight({"base_weight": 0.8})[0], 0.8)
        self.assertEqual(dc.anchor_weight({"base_weight": 2})[0], 1.0)

    def test_anchor_p(self):
        self.assertAlmostEqual(dc.anchor_p(0.02, 0.15, 0.5), 0.085)
        self.assertAlmostEqual(dc.anchor_p(0.02, 0.15, 0.25), 0.0525)
        self.assertEqual(dc.anchor_p(0.02, None, 0.5), 0.02)
        self.assertIsNone(dc.anchor_p(None, 0.15, 0.5))

    def test_anchor_outcomes_hits_targets(self):
        outs = [(0.48, 2.0, False), (0.30, 1.2, False), (0.20, 0.4, False), (0.02, 0.1, True)]
        res, pl = dc.anchor_outcomes(outs, 0.10, 0.25)
        self.assertAlmostEqual(sum(p for p, _ in res), 1.0)
        self.assertAlmostEqual(sum(p for p, m in res if m == 0.1), 0.10)
        self.assertAlmostEqual(sum(p for p, m in res if m <= 0.5), 0.25)
        self.assertAlmostEqual(pl, 0.25)
        # shape above 0.5x kept: 2.0 and 1.2 keep their 48:30 ratio
        d = dict((m, p) for p, m in res)
        self.assertAlmostEqual(d[2.0] / d[1.2], 0.48 / 0.30)

    def test_floor_at_blowup(self):
        outs = [(0.9, 2.0, False), (0.08, 0.4, False), (0.02, 0.1, True)]
        res, pl = dc.anchor_outcomes(outs, 0.12, 0.05)   # base-rate blow-up above base-rate <=0.5x
        self.assertAlmostEqual(pl, 0.12)
        self.assertAlmostEqual(sum(p for p, m in res if m <= 0.5), 0.12)

    def test_fallback_loss_point(self):
        outs = [(0.98, 2.0, False), (0.02, 0.1, True)]
        res, _ = dc.anchor_outcomes(outs, 0.05, 0.10)
        self.assertAlmostEqual(sum(p for p, m in res if m == dc.ANCHOR_FALLBACK_LOSS_MULT), 0.05)
        self.assertAlmostEqual(sum(p for p, _ in res), 1.0)

    def test_fatter_tail_lowers_ev(self):
        outs = [(0.80, 2.0, False), (0.18, 0.4, False), (0.02, 0.1, True)]
        res, _ = dc.anchor_outcomes(outs, 0.10, 0.30)
        self.assertLess(sum(p * m for p, m in res), sum(p * m for p, m, _ in outs))


class TestCoreAssetThreat(unittest.TestCase):
    """v1.4 (L40): manual core-asset licence/lease threat triggers the survival cap like a red flag."""
    T = {"description": "land lease expired Jul-2023; lessor opposes renewal in the Supreme Court",
         "source": "SC filing", "date": "2026-11-24"}

    def test_triggers_cap_outside_pead(self):
        r = dc.survival_cap("india", False, {"pledge_pct_of_promoter": 0.0, "interest_cover": 20.0,
                                             "core_asset_threat": self.T})
        self.assertEqual(r["status"], "TRIGGERED")
        self.assertEqual(r["mode"], "cap")
        self.assertTrue(any("core-asset licence/lease threat (L40)" in x for x in r["reasons"]))

    def test_triggers_block_in_pead(self):
        r = dc.survival_cap("india", True, {"pledge_pct_of_promoter": 0.0, "interest_cover": 20.0,
                                            "core_asset_threat": self.T})
        self.assertEqual(r["mode"], "block")
        self.assertTrue(r["blocks"])

    def test_missing_inputs_still_listed(self):
        r = dc.survival_cap("india", False, {"core_asset_threat": self.T})
        self.assertEqual(r["status"], "TRIGGERED")
        self.assertTrue(any("not checked" in x for x in r["reasons"]))

    def test_empty_threat_ignored(self):
        for t in (None, {}, {"description": "  "}):
            r = dc.survival_cap("india", False, {"pledge_pct_of_promoter": 0.0, "interest_cover": 20.0,
                                                 "core_asset_threat": t})
            self.assertEqual(r["status"], "clear")


class TestBuildIntegration(unittest.TestCase):
    """End-to-end on the fictional SYNTHETIC card (every gate clears in v1.1)."""

    def _build(self, mutate):
        card = dc._load_json(SYN_CARD)
        card["worksheet"] = os.path.normpath(os.path.join(os.path.dirname(SYN_CARD), card["worksheet"]))
        mutate(card)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(card, f)
            path = f.name
        try:
            return dc.build(card, path)
        finally:
            os.unlink(path)

    @staticmethod
    def _pead_active(card):
        card.setdefault("stage3", {})["pead"] = {"applicable": True, "quintile": 1, "event_date": card["decision_date"]}

    def test_baseline_opens(self):
        F, recs, _ = self._build(lambda c: None)
        dec = recs[-1]["data"]
        self.assertGreater(dec["size_after_gates"], 0)
        self.assertIsNotNone(dec["ev_mult5_anchored"])

    def test_survival_cap_blocks_and_asks_question(self):
        def m(c):
            self._pead_active(c)
            c["survival"] = {"pledge_pct_of_promoter": 0.40, "interest_cover": 4.0}
        F, recs, _ = self._build(m)
        dec = recs[-1]["data"]
        self.assertEqual(dec["size_after_gates"], 0.0)
        self.assertEqual(dec["survival_cap"]["status"], "TRIGGERED")
        self.assertIn("Balance-sheet question", F["stage3"])
        self.assertIn("Stage 3 survival cap", F["gate_log"])

    def test_general_cap_limits_size(self):
        def m(c):
            c["survival"] = {"pledge_pct_of_promoter": 0.40, "interest_cover": 4.0}
        F, recs, _ = self._build(m)
        dec = recs[-1]["data"]
        self.assertEqual(dec["survival_cap"]["mode"], "cap")
        self.assertGreater(dec["size_after_gates"], 0)
        self.assertLessEqual(dec["size_after_gates"], dc.SURVIVAL_MIN_SIZE)
        self.assertIn("Balance-sheet question", F["stage3"])

    def test_general_cap_owned_no_additions(self):
        def m(c):
            c["survival"] = {"pledge_pct_of_promoter": 0.0, "interest_cover": 1.2, "already_owned": True}
        F, recs, _ = self._build(m)
        self.assertEqual(recs[-1]["data"]["size_after_gates"], 0.0)

    def test_survival_clear_when_flags_clear(self):
        def m(c):
            self._pead_active(c)
            c["survival"] = {"pledge_pct_of_promoter": 0.0, "interest_cover": 9.0}
        F, recs, _ = self._build(m)
        self.assertEqual(recs[-1]["data"]["survival_cap"]["status"], "clear")
        self.assertNotIn("Balance-sheet question", F["stage3"])

    def test_heavy_anchor_feeds_ev_gate(self):
        # put the card on the v2 India class (blow-up 15%) with full weight on the base rate
        def m(c):
            c["base_rate_class"] = "india_nonfin_1000_20000cr_5y"
            c["tail_anchor"] = {"base_weight": 1.0}
        F, recs, _ = self._build(m)
        dec = recs[-1]["data"]
        self.assertLess(dec["ev_mult5_anchored"], dec["ev_mult5_raw"])
        self.assertAlmostEqual(dec["p_blowup_anchored"], 0.1537, places=4)
        calls = {r["id"].rsplit("-", 1)[-1]: r["data"] for r in recs[:-1]}
        self.assertIsNotNone(calls["blowup"]["anchored_probability"])
        self.assertNotEqual(calls["blowup"]["probability"], calls["blowup"]["anchored_probability"])

    def test_core_asset_threat_caps_card(self):
        def m(c):
            c["survival"] = {"pledge_pct_of_promoter": 0.0, "interest_cover": 9.0,
                             "core_asset_threat": TestCoreAssetThreat.T}
        F, recs, _ = self._build(m)
        dec = recs[-1]["data"]
        self.assertEqual(dec["survival_cap"]["mode"], "cap")
        self.assertLessEqual(dec["size_after_gates"], dc.SURVIVAL_MIN_SIZE)
        self.assertIn("core-asset licence/lease threat (L40)", F["stage3"])
        self.assertIn("core-asset licence/lease threat (L40)", F["gate_log"])

    def test_core_asset_threat_blocks_in_pead(self):
        def m(c):
            self._pead_active(c)
            c["survival"] = {"pledge_pct_of_promoter": 0.0, "interest_cover": 9.0,
                             "core_asset_threat": TestCoreAssetThreat.T}
        F, recs, _ = self._build(m)
        self.assertEqual(recs[-1]["data"]["size_after_gates"], 0.0)
        self.assertIn("core-asset licence/lease threat (L40)", F["stage3"])

    def _build_with_blowup(self, p_blowup):
        """SYNTHETIC worksheet copy with a fat documented blow-up tail, on the India v2 class (base blow-up ~15%)."""
        tmp = tempfile.mkdtemp()
        def m(c):
            w = dc._load_json(c["worksheet"])
            w["blowup"] = {"prob": p_blowup, "multiple": 0.1}
            rest = 1 - p_blowup
            tot = sum(x["prob"] for x in w["scenarios"])
            for x in w["scenarios"]:
                x["prob"] = x["prob"] * rest / tot
            path = os.path.join(tmp, "ws.json")
            with open(path, "w") as f:
                json.dump(w, f)
            c["worksheet"] = path
            c["base_rate_class"] = "india_nonfin_1000_20000cr_5y"
        try:
            return self._build(m)
        finally:
            import shutil
            shutil.rmtree(tmp)

    def test_anchor_lowered_warning(self):
        # base class blow-up 15%: a model blow-up above that gets LOWERED by anchoring -> warning
        F, recs, _ = self._build_with_blowup(0.40)
        self.assertIn(dc.ANCHOR_LOWERED_WARNING, F["probabilities"])
        self.assertIn(dc.ANCHOR_LOWERED_WARNING, F["gate_log"])
        self.assertIn("P(blow-up)", recs[-1]["data"]["anchor_lowered_tails"])

    def test_no_warning_when_anchoring_raises_tails(self):
        F, recs, _ = self._build(lambda c: c.update(base_rate_class="india_nonfin_1000_20000cr_5y"))
        if recs[-1]["data"]["anchor_lowered_tails"]:
            self.skipTest("synthetic worksheet tails already above the base rate")
        self.assertNotIn(dc.ANCHOR_LOWERED_WARNING, F["probabilities"])


class TestLenderClass(unittest.TestCase):
    """v1.5 (L41): lenders get the India lender base-rate class."""
    RATES = {"classes": {"india_nonfin_1000_20000cr_5y": {}, "india_lender_1000_20000cr_5y": {}}}

    def test_non_lender_keeps_class(self):
        n, note = dc.resolve_base_rate_class({"base_rate_class": "india_nonfin_1000_20000cr_5y"}, {"market": "india"},
                                             {"mode": "pe"}, self.RATES)
        self.assertEqual(n, "india_nonfin_1000_20000cr_5y")
        self.assertEqual(note, "")

    def test_each_lender_marker_switches(self):
        for card, wd, wres in (({"is_lender": True}, {"market": "india"}, {}),
                               ({"survival": {"is_financial": True}}, {"market": "india"}, {}),
                               ({}, {"market": "india", "mode": "bank"}, {"mode": "bank"})):
            card = dict(card, base_rate_class="india_nonfin_1000_20000cr_5y")
            n, note = dc.resolve_base_rate_class(card, wd, wres, self.RATES)
            self.assertEqual(n, "india_lender_1000_20000cr_5y")
            self.assertIn("auto-selected", note)

    def test_lock_keeps_card_class(self):
        n, note = dc.resolve_base_rate_class({"is_lender": True, "base_rate_class": "india_nonfin_1000_20000cr_5y",
                                              "base_rate_class_lock": True}, {"market": "india"}, {}, self.RATES)
        self.assertEqual(n, "india_nonfin_1000_20000cr_5y")
        self.assertIn("locks", note)

    def test_us_lender_has_no_class(self):
        n, note = dc.resolve_base_rate_class({"is_lender": True, "base_rate_class": "us_float_500m_10b_5y"},
                                             {"market": "us"}, {}, self.RATES)
        self.assertEqual(n, "us_float_500m_10b_5y")
        self.assertIn("no US lender class", note)

    def test_lender_class_on_file(self):
        rates = dc._load_json(os.path.join(DEC, "base_rates.json"))
        c = rates["classes"][dc.LENDER_CLASSES["india"]]
        for k in ("p_ge_3x", "p_le_half", "p_blowup", "n", "ci95", "size_band", "label", "source", "caveats"):
            self.assertIn(k, c)
        self.assertEqual(c["sector"], "lender")

    def test_live_lender_card_uses_lender_class(self):
        cp = os.path.join(DEC, "live", "UTKARSHBNK_card.json")
        card = dc._load_json(cp)
        F, recs, _ = dc.build(card, cp)
        self.assertIn("Lender class auto-selected", F["probabilities"])
        rates = dc._load_json(os.path.join(DEC, "base_rates.json"))
        self.assertIn(rates["classes"][dc.LENDER_CLASSES["india"]]["label"], F["probabilities"])


if __name__ == "__main__":
    unittest.main()
