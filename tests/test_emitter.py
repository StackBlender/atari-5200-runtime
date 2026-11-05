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
from emitter import AssemblyError, Image, Region, report_json
from layout_fixture import fixture


def image():
    return Image([Region("code", 0xF800, 0xFC00, "code"),
                  Region("assets", 0xFC00, 0xFFFA, "asset"),
                  Region("vectors", 0xFFFA, 0x10000, "vectors")])


def vectors(im, name="entry"):
    im.vectors(nmi=name, reset=name, irq=name)


class EmitterTests(unittest.TestCase):
    def test_fixture_encoding_and_budget(self):
        data, report = fixture()
        self.assertEqual(len(data), 2048)
        self.assertEqual(data[:4], bytes([0x4C, 0x00, 0xF8, 0x40]))
        self.assertEqual(data[-6:], bytes([3, 0xF8, 0, 0xF8, 3, 0xF8]))
        self.assertEqual(data[4:-6], bytes([255]) * 2038)
        self.assertEqual(report["used"], 10)
        self.assertEqual(report["remaining"], 2038)
        self.assertEqual(report["allocations"][0]["remaining"], 60)
        self.assertEqual(report["capabilities"], [])
        self.assertIsNone(report["runtime_abi"])
        self.assertEqual(report["sha256"], hashlib.sha256(data).hexdigest())

    def test_forward_backward_and_little_endian(self):
        im = image()
        im.label("entry")
        im.instruction("LDX", "imm", 3)
        im.label("loop")
        im.instruction("DEX")
        im.instruction("BNE", "rel", "loop")
        im.instruction("JSR", "abs", "sub")
        im.instruction("JMP", "abs", "entry")
        im.label("sub")
        im.instruction("LDA", "abs", "original_asset")
        im.instruction("RTS")
        im.org(0xFC00)
        im.label("original_asset")
        im.bytes(0x55, 0xAA)
        vectors(im)
        data, _ = im.finish()
        self.assertEqual(data[:16], bytes([0xA2, 3, 0xCA, 0xD0, 0xFD,
                                         0x20, 0x0B, 0xF8, 0x4C, 0, 0xF8,
                                         0xAD, 0, 0xFC, 0x60, 0xFF]))

    def test_relative_limits(self):
        for delta in (-128, 127):
            im = image()
            target = 0xF900 + 2 + delta
            im.org(target)
            im.label("target")
            im.instruction("NOP")
            im.org(0xF900)
            im.instruction("BNE", "rel", "target")
            vectors(im, "target")
            data, _ = im.finish()
            self.assertEqual(data[0x101], delta & 255)

    def test_relative_overflow(self):
        for delta in (-129, 128):
            im = image()
            im.org(0xF900 + 2 + delta)
            im.label("target")
            im.instruction("NOP")
            im.org(0xF900)
            im.instruction("BEQ", "rel", "target")
            vectors(im, "target")
            with self.assertRaisesRegex(AssemblyError, "out of range"):
                im.finish()

    def test_bad_layouts(self):
        layouts = [[], [Region("short", 0xF800, 0xFFFF, "code")],
                   [Region("bad", 0xF7FF, 0x10000, "code")],
                   [Region("bad", 0xF800, 0x10001, "code")],
                   [Region("bad", 0xF800, 0x10000, "unknown")],
                   [Region("one", 0xF800, 0xFFFF, "code"),
                    Region("two", 0xFFFE, 0x10000, "asset")],
                   [Region("same", 0xF800, 0xFC00, "code"),
                    Region("same", 0xFC00, 0x10000, "asset")]]
        for regions in layouts:
            with self.subTest(regions=regions), self.assertRaises(AssemblyError):
                Image(regions)

    def test_write_overflow_is_atomic(self):
        im = image()
        im.org(0xFBFF)
        with self.assertRaises(AssemblyError):
            im.instruction("LDX", "imm", 1)
        self.assertEqual(im.pc, 0xFBFF)
        self.assertEqual(im.written, set())
        im.org(0xFFFF)
        with self.assertRaises(AssemblyError):
            im.bytes(1, 2)

    def test_overlap_rejected(self):
        im = image()
        im.instruction("NOP")
        im.org(0xF800)
        with self.assertRaisesRegex(AssemblyError, "overlapping writes"):
            im.instruction("NOP")

    def test_duplicate_label(self):
        im = image()
        im.label("entry")
        with self.assertRaises(AssemblyError):
            im.label("entry")

    def test_undefined_target(self):
        im = image()
        im.label("entry")
        im.instruction("JMP", "abs", "missing")
        vectors(im)
        with self.assertRaisesRegex(AssemblyError, "unresolved"):
            im.finish()

    def test_unwritten_target(self):
        im = image()
        im.label("entry")
        im.instruction("JMP", "abs", "unused")
        im.org(0xF900)
        im.label("unused")
        vectors(im)
        with self.assertRaisesRegex(AssemblyError, "unwritten"):
            im.finish()

    def test_control_target_must_be_instruction(self):
        for target in (0xF801, 0xFC00):
            im = image()
            im.label("entry")
            im.instruction("LDX", "imm", 0xEA)
            im.org(target)
            im.label("bad")
            if target == 0xFC00:
                im.bytes(0xEA)
            vectors(im, "bad")
            with self.assertRaisesRegex(AssemblyError, "not an emitted instruction"):
                im.finish()

    def test_vectors_required_once(self):
        im = image()
        im.label("entry")
        im.instruction("NOP")
        with self.assertRaisesRegex(AssemblyError, "missing CPU vectors"):
            im.finish()
        vectors(im)
        with self.assertRaisesRegex(AssemblyError, "already emitted"):
            vectors(im)

    def test_reserved_and_assets_not_executable(self):
        im = Image([Region("reserved", 0xF800, 0x10000, "reserved")])
        with self.assertRaises(AssemblyError):
            im.bytes(1)
        im = image()
        im.org(0xFC00)
        with self.assertRaises(AssemblyError):
            im.instruction("NOP")

    def test_operand_and_instruction_validation(self):
        cases = [("BRA", "rel", "entry"), ("LDA", "guess", 1),
                 ("LDX", "imm", 256), ("STA", "zp", -1),
                 ("LDA", "abs", 65536), ("NOP", "impl", 0),
                 ("BNE", "rel", 0xF800), ("LDX", "imm", True)]
        for args in cases:
            im = image()
            with self.subTest(args=args), self.assertRaises(AssemblyError):
                im.instruction(*args)
            self.assertEqual(im.pc, 0xF800)
            self.assertFalse(im.written)

    def test_bytes_and_origin_validation(self):
        for values in ((-1,), (256,), (1, 2, None)):
            im = image()
            with self.assertRaises(AssemblyError):
                im.bytes(*values)
            self.assertFalse(im.written)
        for address in (0xF7FF, 0x10000, 1.5):
            with self.assertRaises(AssemblyError):
                image().org(address)

    def test_repeat_finish_is_stable(self):
        im = image()
        im.label("entry")
        im.instruction("JMP", "abs", "entry")
        vectors(im)
        first = im.finish()
        self.assertEqual(im.finish(), first)
        self.assertEqual(json.loads(report_json(first[1])), first[1])

    def test_cli_fresh_process_reproducibility(self):
        script = Path(__file__).resolve().parents[1] / "tools/layout_fixture.py"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("first", "second"):
                subprocess.run([sys.executable, str(script), "--output-dir", str(root / name)],
                               check=True, timeout=10, capture_output=True)
            for name in ("layout-test.bin", "layout-test.json"):
                self.assertEqual((root / "first" / name).read_bytes(),
                                 (root / "second" / name).read_bytes())
