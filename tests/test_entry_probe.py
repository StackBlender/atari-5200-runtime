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
from emitter import AssemblyError, fixed_instruction
from entry_probe import capture_fragment


class EntryProbeTests(unittest.TestCase):
    def test_independent_capture_encoding(self):
        data, descriptor = capture_fragment(0x8000, 0x3000)
        self.assertEqual(data, bytes.fromhex(
            "8d0030 8e0130 8c0230 08 68 8d0330 ba 8e0430 a9a5 8d0530 4c1780"))
        self.assertEqual(len(data), 26)
        self.assertEqual(descriptor["slots"],
                         {"a": 0, "x": 1, "y": 2, "p_pushed": 3, "sp": 4, "complete": 5})
        self.assertFalse(descriptor["execution_approved"])
        self.assertFalse(descriptor["executable_cartridge"])
        self.assertEqual(descriptor["stack_extra_bytes"], 1)
        self.assertEqual(descriptor["stack_net_change"], 0)
        self.assertEqual(descriptor["p_known_mask"], 0xCF)
        self.assertEqual(descriptor["fragment_sha256"], hashlib.sha256(data).hexdigest())

    def test_boundary_layout_and_relocation(self):
        data, _ = capture_fragment(0x4000, 0x220)
        self.assertEqual(data[:9], bytes.fromhex("8d2002 8e2102 8c2202"))
        self.assertEqual(data[-3:], bytes.fromhex("4c1740"))
        data, _ = capture_fragment(0xBFCE, 0x3FFA)
        self.assertEqual(data[-3:], bytes.fromhex("4ce5bf"))
        self.assertEqual(data[20:23], bytes.fromhex("8dff3f"))
        for entry, result in ((0x3FFF, 0x3000), (0xBFCF, 0x3000),
                              (0x8000, 0x21F), (0x8000, 0x3FFB),
                              (True, 0x3000), (0x8000, 3.5)):
            with self.subTest(entry=entry, result=result), self.assertRaises(AssemblyError):
                capture_fragment(entry, result)

    def test_fixed_encoding_validation(self):
        self.assertEqual(fixed_instruction("STX", "abs", 0xFFFF), bytes.fromhex("8effff"))
        for args in (("BNE", "rel", "loop"), ("PHP", "impl", 1),
                     ("STY", "abs", -1), ("STA", "abs", True),
                     ("LDA", "imm", "label"), ("JMP", "abs", "label")):
            with self.subTest(args=args), self.assertRaises(AssemblyError):
                fixed_instruction(*args)

    def test_fresh_process_fragment_and_descriptor(self):
        script = Path(__file__).resolve().parents[1] / "tools/entry_probe.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("one", "two"):
                subprocess.run([sys.executable, str(script), "--entry-address", "0x8000",
                                "--result-start", "0x3000", "--output-dir", str(root / name)],
                               check=True, capture_output=True, timeout=10)
            for name in ("entry-capture.bin", "entry-capture.json"):
                self.assertEqual((root / "one" / name).read_bytes(), (root / "two" / name).read_bytes())
            descriptor = json.loads((root / "one/entry-capture.json").read_text())
            self.assertNotIn(str(root), json.dumps(descriptor))
