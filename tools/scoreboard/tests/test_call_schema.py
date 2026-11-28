"""Regression (28-Nov-2026): gold/macro calls used 'p'/'made'; scenario sets have no single probability.
One such record crashed calls.py, resolve.py and scoreboard.py for every call."""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sb_common as C  # noqa: E402


def rec(id_, data):
    return {"id": id_, "tickers": ["GOLD"], "tags": ["paper-call"], "title": "Paper call: x", "data": data,
            "date": "2026-11-28"}


class CallSchema(unittest.TestCase):
    def test_short_p_and_made(self):
        c = C.normalise(rec("a", {"p": 0.35, "made": "2026-11-27", "resolve_by": "2027-06-30"}))
        self.assertEqual(c["probability"], 0.35)
        self.assertEqual(c["made_on"], "2026-11-27")

    def test_probability_wins_over_p(self):
        self.assertEqual(C.normalise(rec("b", {"probability": 0.6, "p": 0.1}))["probability"], 0.6)

    def test_scenario_set_raises(self):
        with self.assertRaises(C.NotBinaryCall):
            C.normalise(rec("c", {"p": {"base": 0.5, "bad": 0.5}}))
        with self.assertRaises(C.NotBinaryCall):
            C.normalise(rec("d", {"ours": {"base": 1.0}}))

    def test_load_calls_skips_bad_keeps_good(self):
        rows = [rec("good", {"probability": 0.4}), rec("scen", {"p": {"x": 1.0}})]
        with mock.patch.object(C, "load_call_records", return_value=rows):
            out = C.load_calls()
        self.assertEqual([c["id"] for c in out], ["good"])


if __name__ == "__main__":
    unittest.main()
