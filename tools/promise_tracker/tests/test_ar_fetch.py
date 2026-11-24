"""Tests for ar_fetch ZIP/PDF handling (run: python3 -m pytest tools/promise_tracker/tests -q, or python3 this_file).
Builds tiny real PDFs in memory; needs pdftotext (poppler-utils) for the text checks."""
import io
import os
import shutil
import sys
import tempfile
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import ar_fetch  # noqa: E402

HAS_PDFTOTEXT = shutil.which("pdftotext") is not None


def make_pdf(text, pad=0):
    """Minimal valid one-page PDF showing `text`; `pad` adds a comment to make the file bigger."""
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
            b"/Resources << /Font << /F1 5 0 R >> >> >>",
            b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out = bytearray(b"%PDF-1.4\n" + (b"%" + b"x" * pad + b"\n" if pad else b""))
    offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    x = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for o in offs:
        out += b"%010d 00000 n \n" % o
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)
    return bytes(out)


def make_zip(members):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in members:
            z.writestr(name, data)
    return b.getvalue()


class Info:
    def __init__(self, filename, size):
        self.filename, self.file_size = filename, size

    def is_dir(self):
        return self.filename.endswith("/")


class PickMembers(unittest.TestCase):
    def test_prefers_annual_report_over_larger_notice(self):
        got = ar_fetch.pick_zip_members([Info("AGM_Notice.pdf", 9_000_000), Info("Annual_Report_2024.pdf", 5_000_000),
                                         Info("BRSR.pdf", 7_000_000)])
        self.assertEqual(got, ["Annual_Report_2024.pdf"])

    def test_largest_when_names_uninformative(self):
        got = ar_fetch.pick_zip_members([Info("a.pdf", 10), Info("b.pdf", 999), Info("readme.txt", 5000)])
        self.assertEqual(got, ["b.pdf"])

    def test_numbered_parts_joined(self):
        got = ar_fetch.pick_zip_members([Info("AR Part 2.pdf", 50), Info("AR Part 1.pdf", 60), Info("Notice.pdf", 80)])
        self.assertEqual(got, ["AR Part 1.pdf", "AR Part 2.pdf"])

    def test_no_pdf_and_junk_members(self):
        self.assertEqual(ar_fetch.pick_zip_members([Info("x/", 0), Info("__MACOSX/._ar.pdf", 10), Info("ar.txt", 9)]), [])


class Extract(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_corrupt_zip_raises_valueerror(self):
        for bad in (b"PK\x03\x04" + b"\x00garbage" * 50, make_zip([("ar.pdf", make_pdf("X"))])[:-40]):
            with self.assertRaises(ValueError):
                ar_fetch.extract(bad, "https://x/AR.zip", self.d, "AR_FY24")

    def test_zip_without_pdf_raises_valueerror(self):
        with self.assertRaises(ValueError):
            ar_fetch.extract(make_zip([("note.txt", b"hi")]), "https://x/AR.zip", self.d, "AR_FY24")

    def test_neither_pdf_nor_zip(self):
        with self.assertRaises(ValueError):
            ar_fetch.extract(b"<html>blocked</html>", "https://x/AR.pdf", self.d, "AR_FY24")

    @unittest.skipUnless(HAS_PDFTOTEXT, "pdftotext missing")
    def test_zip_listed_as_pdf_detected_by_magic_and_best_member_used(self):
        z = make_zip([("Notice_of_AGM.pdf", make_pdf("NOTICEONLY", pad=5000)),
                      ("Annual Report 2023-24.pdf", make_pdf("ANNUALREPORTTEXT", pad=2000)),
                      ("fake.pdf", b"not a pdf")])
        text, n = ar_fetch.extract(z, "https://x/AR_123.pdf", self.d, "AR_FY24")
        self.assertEqual(n, 1)
        self.assertIn("ANNUALREPORTTEXT", text)
        self.assertNotIn("NOTICEONLY", text)
        self.assertEqual(os.listdir(self.d), [])     # temp PDF/TXT deleted

    @unittest.skipUnless(HAS_PDFTOTEXT, "pdftotext missing")
    def test_plain_pdf(self):
        text, n = ar_fetch.extract(make_pdf("HELLOAR"), "https://x/AR.zip", self.d, "AR_FY25")
        self.assertEqual(n, 1)
        self.assertIn("HELLOAR", text)


class AddDocSkips(unittest.TestCase):
    def test_corrupt_year_skipped_not_crash(self):
        root = tempfile.mkdtemp()
        orig = ar_fetch.FE.http_get
        ar_fetch.FE.http_get = lambda url: b"PK\x03\x04corrupt-zip-bytes" * 10
        try:
            import datetime as dt
            manifest = {}
            ar_fetch.add_doc(manifest, "TEST", root, "AR_FY23", "https://x/AR.zip", dt.date(2023, 8, 1),
                             "annual_report", "ARFY23", 2023)
            self.assertEqual(manifest, {})
            self.assertFalse(os.path.exists(os.path.join(root, "TEST", "txt", "AR_FY23.txt")))
        finally:
            ar_fetch.FE.http_get = orig
            shutil.rmtree(root)


if __name__ == "__main__":
    unittest.main()
