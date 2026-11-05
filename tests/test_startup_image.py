# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"tools"))
from emitter import AssemblyError, fixed_instruction
from startup_image import startup_image, original_font


class StartupImageTests(unittest.TestCase):
    def test_independent_reset_program_bytes(self):
        data, _ = startup_image()
        expected = bytes.fromhex(
            "78 d8 a2ff 9a a900 "
            "8d0ed4 8d00d4 8d0ee8 8d0fe8 8d01e8 8d03e8 8d05e8 8d07e8 "
            "8d1dc0 8d1bc0 8d1ac0 a902 8d01d4 a9f8 8d09d4 a900 8d0fd4 "
            "a218 9500 ca 10fb a200 a986 9d0002 e8 a9fc 9d0002 e8 e01c d0f0 "
            "20b0fe 18 b8 a000 a200 a900 6cfebf")
        self.assertEqual(len(expected), 94)
        self.assertEqual(data[0x400:0x45E], expected)
        self.assertEqual(data[0x45E:0x480], b"\xff"*34)

    def test_independent_helper_bytes_and_branches(self):
        data, report = startup_image()
        expected = bytes.fromhex(
            "a200 bde8bf c950 9020 c95a b01c e8 e016 d0f0 "
            "adffbf c940 9010 c9c0 b00c c9bf d007 adfebf c9e8 b001 60 4c86fc")
        self.assertEqual(len(expected), 44)
        self.assertEqual(data[0x6B0:0x6DC], expected)
        self.assertEqual(data[0x6DC:0x700], b"\xff"*36)
        symbols = report["symbols"]
        self.assertEqual(symbols["validate_digit"], 0xFEB2)
        self.assertEqual(symbols["valid_metadata"], 0xFED8)
        self.assertEqual(symbols["invalid_metadata"], 0xFED9)
        self.assertEqual(symbols["cart_handoff"], 0xFC5B)

    def test_exact_fault_loops_and_cpu_vectors(self):
        data, _ = startup_image()
        self.assertEqual(data[0x480:0x489], bytes.fromhex("4c80fc 4c83fc 4c86fc"))
        self.assertEqual(data[-6:], bytes.fromhex("80fc 00fc 83fc"))

    def test_original_digit_pixels_and_blank_glyphs(self):
        font = original_font()
        digits = bytes.fromhex(
            "3c42420042423c00 0002020002020000 3c02023c40403c00 "
            "3c02023c02023c00 0042423c02020000 3c40403c02023c00 "
            "3c40403c42423c00 3c02020002020000 3c42423c42423c00 3c42423c02023c00")
        self.assertEqual(font[:0x280], bytes(0x280))
        self.assertEqual(font[0x280:0x2D0], digits)
        self.assertEqual(font[0x2D0:], bytes(0x130))
        data, _ = startup_image()
        self.assertEqual(data[:1024], font)

    def test_allocation_fit_and_unimplemented_reservations(self):
        data, report = startup_image()
        self.assertEqual(len(data), 2048)
        self.assertEqual(report["used"], 1177)
        self.assertEqual(report["remaining"], 871)
        rows = {row["name"]: row for row in report["allocations"]}
        for name, used in [("font",1024),("startup",94),("interrupts",9),("shared",44),("vectors",6)]:
            self.assertEqual(rows[name]["used"],used)
        for name in ["input","clocks","display","margin"]:
            self.assertEqual(rows[name]["used"],0)
            self.assertEqual(data[rows[name]["start"]-0xF800:rows[name]["end"]-0xF800],
                             b"\xff"*(rows[name]["end"]-rows[name]["start"]))
        self.assertEqual(rows["margin"]["remaining"],250)
        self.assertEqual(report["sha256"],hashlib.sha256(data).hexdigest())
        self.assertEqual(report["capabilities"],[])
        self.assertEqual(report["authored_capabilities"],["cold-start-digits-v1"])
        self.assertFalse(report["execution_verified"])
        self.assertFalse(report["provider_approved"])

    def test_new_factual_encodings_and_bounds(self):
        for instruction, mode, operand, expected in [
            ("CLC","impl",None,"18"),("CLV","impl",None,"b8"),
            ("CMP","imm",0x50,"c950"),("CPX","imm",22,"e016"),
            ("STA","zpx",0,"9500"),("STA","absx",0x200,"9d0002"),
            ("LDA","absx",0xBFE8,"bde8bf"),("JMP","ind",0xBFFE,"6cfebf")]:
            with self.subTest(instruction=instruction):
                self.assertEqual(fixed_instruction(instruction,mode,operand),bytes.fromhex(expected))
        for mode, operand in [("zpx",256),("absx",65536),("ind",65536),("ind",True)]:
            with self.subTest(mode=mode), self.assertRaises(AssemblyError):
                fixed_instruction("JMP" if mode=="ind" else "STA",mode,operand)

    def test_fresh_process_image_and_map(self):
        script=Path(__file__).resolve().parents[1]/"tools/startup_image.py"
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ["one","two"]:
                subprocess.run([sys.executable,str(script),"--output-dir",str(root/name)],
                               check=True,capture_output=True,timeout=10)
            for name in ["startup.bin","startup-map.json"]:
                self.assertEqual((root/"one"/name).read_bytes(),(root/"two"/name).read_bytes())
            report=json.loads((root/"one/startup-map.json").read_text())
            self.assertNotIn(str(root),json.dumps(report))
