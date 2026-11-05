# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from cartridge_candidate import communication_area, diagnostic_candidate
from emitter import AssemblyError

TITLE = "01234567890123456789"


class CartridgeCandidateTests(unittest.TestCase):
    def test_independent_metadata_bytes(self):
        expected = bytes.fromhex("50 51 52 53 54 55 56 57 58 59 50 51 52 53 54 55 56 57 58 59 52 56 00 80")
        self.assertEqual(communication_area(TITLE, "26", 0x8000), expected)
        self.assertEqual(len(expected), 24)

    def test_digit_convention_all_values(self):
        for digit in range(10):
            self.assertEqual(communication_area(str(digit)*20, str(digit)*2, 0x4000)[:22],
                             bytes([0x50+digit])*22)

    def test_title_and_year_reject_non_ascii_and_wrong_types(self):
        bad_titles = ["", TITLE[:-1], TITLE+"0", "A"+TITLE[1:], "０"*20,
                      "٠"*20, "0"*19+"\n", b"0"*20, 0, None, True]
        for title in bad_titles:
            with self.subTest(title=title), self.assertRaises(AssemblyError):
                communication_area(title, "26", 0x8000)
        for year in ["", "2", "026", "2A", "２６", 26, True, None, b"26"]:
            with self.subTest(year=year), self.assertRaises(AssemblyError):
                communication_area(TITLE, year, 0x8000)

    def test_entry_bounds_and_little_endian(self):
        self.assertEqual(communication_area(TITLE, "00", 0x4000)[-2:], b"\x00\x40")
        self.assertEqual(communication_area(TITLE, "99", 0xBFE7)[-2:], b"\xe7\xbf")
        for address in [0x3FFF, 0xBFE8, 0xC000, 0xFFFF, -1, True, 32768.0, "32768"]:
            with self.subTest(address=address), self.assertRaises(AssemblyError):
                communication_area(TITLE, "26", address)

    def test_full_layout_with_independent_holes_and_capture(self):
        image, report = diagnostic_candidate(TITLE, "26")
        self.assertEqual(len(image), 32768)
        self.assertEqual(image[:0x4000], bytes(0x4000))
        self.assertEqual(image[0x4000:0x401A], bytes.fromhex(
            "8d0030 8e0130 8c0230 08 68 8d0330 ba 8e0430 a9a5 8d0530 4c1780"))
        self.assertEqual(image[0x401A:0x7FE8], bytes(0x3FCE))
        self.assertEqual(image[0x7FE8:], bytes.fromhex(
            "505152535455565758595051525354555657585952560080"))
        self.assertEqual(report["cartridge_sha256"], hashlib.sha256(image).hexdigest())
        for key in ["runtime_provider", "execution_approved", "mapper_review_approved",
                    "reference_execution_approved", "original_measurement_claim"]:
            self.assertIs(report[key], False)
        # The embedded fragment descriptor deliberately retains its original scope.
        self.assertFalse(report["capture"]["executable_cartridge"])
        self.assertEqual(report["purpose"], "unapproved-diagnostic-cartridge-candidate")

    def test_fragment_boundary_never_overwrites_metadata(self):
        image, report = diagnostic_candidate(TITLE, "26", 0xBFCE, 0x3FFA)
        self.assertEqual(image[0x7FE5:0x7FE8], bytes.fromhex("4ce5bf"))
        self.assertEqual(image[0x7FE8:0x7FEC], bytes.fromhex("50515253"))
        self.assertEqual(report["capture"]["result_start"], 0x3FFA)
        image, _ = diagnostic_candidate(TITLE, "26", 0x4000, 0x220)
        self.assertEqual(image[:3], bytes.fromhex("8d2002"))
        for entry, result in [(0xBFCF, 0x3000), (0x8000, 0x21F),
                              (0x8000, 0x3FFB), (True, 0x3000), (0x8000, True)]:
            with self.subTest(entry=entry, result=result), self.assertRaises(AssemblyError):
                diagnostic_candidate(TITLE, "26", entry, result)

    def test_fresh_process_reproducibility_and_no_host_paths(self):
        script = Path(__file__).resolve().parents[1] / "tools/cartridge_candidate.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ["one", "two"]:
                subprocess.run([sys.executable, str(script), "--title", TITLE,
                                "--year-digits", "26", "--output-dir", str(root/name)],
                               check=True, capture_output=True, timeout=10)
            for name in ["entry-candidate.bin", "entry-candidate.json"]:
                self.assertEqual((root/"one"/name).read_bytes(), (root/"two"/name).read_bytes())
            report = json.loads((root/"one/entry-candidate.json").read_text())
            self.assertNotIn(str(root), json.dumps(report))

    def test_invalid_cli_leaves_no_output(self):
        script = Path(__file__).resolve().parents[1] / "tools/cartridge_candidate.py"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/"not-created"
            result = subprocess.run([sys.executable, str(script), "--title", TITLE,
                                     "--year-digits", "FF", "--output-dir", str(output)],
                                    capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b"")
            self.assertFalse(output.exists())
