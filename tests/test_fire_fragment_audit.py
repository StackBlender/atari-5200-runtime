# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"tools"))
from fire_fragment_audit import AuditError, audit
from fire_service_fragment import fire_fragment
ROOT = Path(__file__).resolve().parents[1]


class FireAuditTests(unittest.TestCase):
    def test_exact_conditional_footprint_and_callback_contract(self):
        data, _ = fire_fragment()
        result = audit(data)
        self.assertEqual(result["writes"], list(range(0x610, 0x61C)))
        self.assertEqual(result["reads"], [0x600, 0x602, *range(0x610, 0x61C),
                                          *range(0xC010, 0xC014), 0xE80F])
        self.assertEqual(result["call_offsets"], [62, 136])
        self.assertEqual(result["callback_pointer"], 0x208)
        self.assertEqual(result["maximum_bridge_stack_bytes"], 2)
        self.assertEqual(result["indexed_x_range_assumption"], [0, 3])
        self.assertFalse(result["execution_verified"])
        self.assertFalse(result["allocation_approved"])

    def test_every_protected_register_write_is_refused(self):
        data, _ = fire_fragment()
        # A valid STA abs slot cannot be redirected into IRQ/mask/selector,
        # scan/reset/audio/NMI/latch control, key publication or font storage.
        for address in (0, 0x600, 0x601, 0x602, 0x605, 0x606, 0xC01D,
                        0xC01F, 0xD40E, 0xD40F, 0xE800, 0xE80A,
                        0xE80B, 0xE80E, 0xE80F, 0xF800):
            mutated = bytearray(data)
            mutated[20:22] = address.to_bytes(2, "little")
            with self.subTest(address=address), self.assertRaises(AuditError):
                audit(bytes(mutated))

    def test_write_only_readback_and_wrong_index_bases_refused(self):
        data, _ = fire_fragment()
        for offset, address in ((85, 0xC01D), (85, 0xC01F), (13, 0xC014),
                                (122, 0x611)):
            mutated = bytearray(data)
            mutated[offset:offset+2] = address.to_bytes(2, "little")
            with self.subTest(offset=offset), self.assertRaises(AuditError):
                audit(bytes(mutated))

    def test_branch_operand_cross_routine_and_callback_escape_refused(self):
        data, _ = fire_fragment()
        for displacement in (1, 74, 143):
            mutated = bytearray(data)
            mutated[6] = displacement
            with self.subTest(displacement=displacement), self.assertRaises(AuditError):
                audit(bytes(mutated))
        for offset, target in ((63, 0xF897), (79, 0xFC80), (151, 0x20A)):
            mutated = bytearray(data)
            mutated[offset:offset+2] = target.to_bytes(2, "little")
            with self.subTest(offset=offset), self.assertRaises(AuditError):
                audit(bytes(mutated))

    def test_unsupported_control_opcodes_size_and_type_refused(self):
        data, _ = fire_fragment()
        for opcode in (0x58, 0x78, 0x40, 0x60, 0x48, 0x00, 0xFF):
            with self.subTest(opcode=opcode), self.assertRaises(AuditError):
                audit(bytes([opcode])+data[1:])
        for bad in (data[:-1], data+b"x", bytearray(data), None):
            with self.assertRaises(AuditError):
                audit(bad)

    def test_cli_rejection_has_no_success_report_and_valid_is_deterministic(self):
        data, _ = fire_fragment()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"fragment.bin"
            path.write_bytes(data)
            command = [sys.executable, str(ROOT/"tools/fire_fragment_audit.py"), str(path)]
            a = subprocess.run(command, capture_output=True, timeout=10)
            b = subprocess.run(command, capture_output=True, timeout=10)
            self.assertEqual(a.returncode, 0)
            self.assertEqual(a.stdout, b.stdout)
            self.assertEqual(json.loads(a.stdout), audit(data))
            path.write_bytes(data[:-1])
            rejected = subprocess.run(command, capture_output=True, timeout=10)
            self.assertEqual(rejected.returncode, 2)
            self.assertEqual(rejected.stdout, b"")
            self.assertIn(b"audit rejected", rejected.stderr)
