"""Unit tests for worksheet v1.3.1 input/output additions (L44): core EPS / trailing-vs-core P/E, and the plain-words
"DCF value below net debt" note. Regression: every stored live worksheet made by the current version must reproduce
exactly (numbers identical; Markdown identical apart from the new note lines). No network.

    python3 -m unittest discover -s tools/valuation/tests -v
"""
import copy
import glob
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.dirname(HERE)
sys.path.insert(0, VAL)
import worksheet as ws  # noqa: E402

NEW_LINE_MARKERS = (ws.DCF_BELOW_NET_DEBT, "Trailing P/E **", "> **Warning (L44):**")


def _base():
    d = copy.deepcopy(ws.TEMPLATE)
    d["base"]["pat"] = 90.0
    return d


def _run(d):
    return ws.run(ws.normalise(d))


def _strip_new(md):
    """Drop the lines v1.3.1 adds (and the blank line each one brings) so the old output can be compared."""
    out, skip_blank = [], False
    for ln in md.split("\n"):
        if any(m in ln for m in NEW_LINE_MARKERS):
            skip_blank = True
            continue
        if skip_blank and ln == "":
            skip_blank = False
            continue
        skip_blank = False
        out.append(ln)
    return "\n".join(out)


def _subset(old, new, path="$"):
    """Every key/value in old is present and equal in new (new may carry extra keys)."""
    if isinstance(old, dict):
        assert isinstance(new, dict), path
        for k, v in old.items():
            assert k in new, "%s.%s missing" % (path, k)
            _subset(v, new[k], "%s.%s" % (path, k))
    elif isinstance(old, list):
        assert isinstance(new, list) and len(old) == len(new), path
        for i, (a, b) in enumerate(zip(old, new)):
            _subset(a, b, "%s[%d]" % (path, i))
    else:
        assert old == new, "%s: %r != %r" % (path, old, new)


class LiveRegression(unittest.TestCase):
    def test_stored_live_worksheets_reproduce(self):
        checked = 0
        for inp in sorted(glob.glob(os.path.join(VAL, "live", "*.json"))):
            if inp.endswith("_worksheet.json"):
                continue
            stem = inp[:-5]
            if not (os.path.exists(stem + "_worksheet.json") and os.path.exists(stem + "_worksheet.md")):
                continue
            with open(stem + "_worksheet.json", encoding="utf-8") as f:
                old = json.load(f)
            d = ws.load_input(inp)
            res = ws.run(d)
            if old.get("version") != res["version"]:
                continue  # stored by an older worksheet version; not a like-for-like regression
            new = json.loads(json.dumps(ws._jsonable(res)))
            old.pop("generated", None)
            new.pop("generated", None)
            _subset(old, new, os.path.basename(stem))
            with open(stem + "_worksheet.md", encoding="utf-8") as f:
                md_old = f.read()
            md_new = ws.render(res) + "\n"
            self.assertEqual(md_old, _strip_new(md_new), os.path.basename(stem))
            checked += 1
        self.assertGreaterEqual(checked, 4)

    def test_old_inputs_get_no_core_keys(self):
        d = ws.normalise(_base())
        res = ws.run(d)
        self.assertNotIn("core", res["temperature"])
        self.assertIsNone(d["base"]["core_eps"])
        self.assertNotIn("_core_eps_method", d)
        self.assertNotIn("Trailing P/E **", ws.render(res))


class CoreEps(unittest.TestCase):
    def test_derived_from_exceptional_and_other_income(self):
        d = _base()
        d["base"].update({"exceptional_items_cr": 20.0, "other_income_cr": 10.0})
        res = _run(d)
        c = res["temperature"]["core"]
        self.assertAlmostEqual(c["core_eps"], (90.0 - 30.0 * 0.75) / 10.0)
        self.assertAlmostEqual(c["trailing_pe"], 100.0 / 9.0)
        self.assertAlmostEqual(c["core_pe"], 100.0 / 6.75)
        self.assertTrue(c["flag"])  # 9.0 / 6.75 - 1 = +33% > 25%
        md = ws.render(res)
        self.assertIn("Trailing P/E **11.1** vs core P/E **14.8**", md)
        self.assertIn("Warning (L44)", md)
        self.assertIn("core EPS (ex exceptional, ex other income)", md)

    def test_given_core_eps_small_gap_not_flagged(self):
        d = _base()
        d["base"]["core_eps"] = 8.0
        c = _run(d)["temperature"]["core"]
        self.assertEqual(c["method"], "given")
        self.assertAlmostEqual(c["gap"], 9.0 / 8.0 - 1)
        self.assertFalse(c["flag"])

    def test_top_level_keys_and_tax_override(self):
        d = _base()
        d["exceptional_items_cr"] = 40.0
        d["core_adj_tax_rate"] = 0.0
        c = _run(d)["temperature"]["core"]
        self.assertAlmostEqual(c["core_eps"], 5.0)

    def test_core_eps_negative(self):
        d = _base()
        d["base"]["exceptional_items_cr"] = 200.0
        res = _run(d)
        c = res["temperature"]["core"]
        self.assertIsNone(c["core_pe"])
        self.assertTrue(c["flag"])
        self.assertIn("n/a (core EPS ≤ 0)", ws.render(res))

    def test_core_does_not_change_valuation(self):
        a = _run(_base())
        d = _base()
        d["base"]["exceptional_items_cr"] = 30.0
        b = _run(d)
        self.assertEqual(a["scenarios"]["pw_value"], b["scenarios"]["pw_value"])
        self.assertEqual(a["scenarios"]["ev_mult5"], b["scenarios"]["ev_mult5"])
        self.assertEqual(a["twin"]["eps0"], b["twin"]["eps0"])


class DcfBelowNetDebt(unittest.TestCase):
    def test_flag_and_plain_words(self):
        d = _base()
        d["net_debt"] = 5000.0
        res = _run(d)
        bnd = res["scenarios"]["dcf_below_net_debt"]
        self.assertEqual(bnd["today"], ["bear", "base", "bull"])
        md = ws.render(res)
        self.assertIn(ws.DCF_BELOW_NET_DEBT, md)
        self.assertIn("DCF value below net debt — EV above 1x is an exit-multiple bet (L21, L44)", md)

    def test_absent_when_equity_positive(self):
        res = _run(_base())
        self.assertNotIn("dcf_below_net_debt", res["scenarios"])
        self.assertNotIn(ws.DCF_BELOW_NET_DEBT, ws.render(res))


if __name__ == "__main__":
    unittest.main()
