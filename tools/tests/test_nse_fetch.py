"""Tests for tools/nse_fetch.py summary mode (--limit; no silent 15-row cut). No network.

    python3 -m unittest discover -s tools/tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nse_fetch as nf  # noqa: E402

ROWS = [{"an_dt": "2026-11-%02d" % (i + 1), "symbol": "X", "desc": "d%d" % i, "attchmntText": "t" * 200,
         "attchmntFile": "f%d.pdf" % i} for i in range(20)]


class SummaryLines(unittest.TestCase):
    def test_default_prints_all(self):
        out = nf.summary_lines("announcements", ROWS)
        self.assertEqual(out[0], "announcements: 20 rows")
        self.assertEqual(len(out), 21)
        self.assertFalse(any("showing" in x for x in out))

    def test_limit_says_showing_n_of_m(self):
        out = nf.summary_lines("announcements", ROWS, 5)
        self.assertEqual(len(out), 1 + 5 + 1)
        self.assertTrue(out[-1].startswith("showing 5 of 20 rows"))

    def test_limit_above_count(self):
        out = nf.summary_lines("announcements", ROWS, 50)
        self.assertEqual(len(out), 21)

    def test_row_format_unchanged(self):
        line = nf.summary_lines("announcements", ROWS[:1])[1]
        self.assertEqual(line, "2026-11-01 | X | d0 | %s | f0.pdf" % ("t" * 90))

    def test_other_commands_and_non_list(self):
        self.assertEqual(len(nf.summary_lines("pledge", ROWS, 3)), 5)
        self.assertEqual(nf.summary_lines("pledge", {"a": 1}), ["pledge: 1 rows"])

    def test_flag_parses(self):
        import argparse  # noqa: F401
        src = open(nf.__file__, encoding="utf-8").read()
        self.assertIn('"--limit"', src)
        self.assertNotIn("rows[:15]", src)


if __name__ == "__main__":
    unittest.main()
