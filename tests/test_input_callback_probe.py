# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"tools"))
from emitter import AssemblyError
from input_callback_probe import recorder_fragment, decode_snapshot
ROOT = Path(__file__).resolve().parents[1]


class InputRecorderTests(unittest.TestCase):
    def test_independent_complete_encoding_and_publication(self):
        data, report = recorder_fragment()
        self.assertEqual(data, bytes.fromhex(
            "8d0207 a900 4c1080 8d0207 a901 4c1080 "
            "8d0507 8e0307 8c0407 ae0007 e020 b02a ae0107 "
            "ad0507 9d0008 e8 ad0207 9d0008 e8 "
            "ad0307 9d0008 e8 ad0407 9d0008 e8 "
            "8e0107 ae0007 e8 8e0007 60 a901 8d0607 60"))
        self.assertEqual(len(data),80)
        self.assertEqual(report["fire_entry"],0x8008)
        self.assertEqual(report["full_entry"],0x804A)
        for flag in ("executable_cartridge", "execution_verified", "runtime_provider", "allocation_approved", "hardware_timing_verified"):
            self.assertFalse(report[flag])
        self.assertEqual(report["extra_stack_bytes"],0)
        # Independent nominal cycle worksheet, including callback RTS.
        self.assertEqual(report["nominal_callback_cycles"],9+24+4*(4+5+2)+20)
        self.assertEqual(report["nominal_full_cycles_max"],9+21+12+1)

    def test_relocation_nonoverlap_and_exact_boundaries(self):
        data, report = recorder_fragment(0xBF98, 0x3FF9, 0x620)
        self.assertEqual(data[:8], bytes.fromhex("8dfb3f a900 4ca8bf"))
        self.assertEqual(data[35:42],bytes.fromhex("adfe3f 9d2006 e8"))
        self.assertEqual(report["buffer_start"]+report["buffer_size"],0x6A0)
        recorder_fragment(control=0x620,buffer=0x627)  # adjacent is allowed
        for args in ((0xBF99,0x700,0x800),(0x3FFF,0x700,0x800),
                     (True,0x700,0x800),(0x8000,0x61F,0x800),
                     (0x8000,0x700,0x3F81),(0x8000,0x800,0x800),
                     (0x8000,0x87F,0x800),(0x8000,0x7FA,0x800)):
            with self.subTest(args=args), self.assertRaises(AssemblyError):
                recorder_fragment(*args)

    def test_decode_synthetic_order_full_buffer_and_overflow(self):
        events = bytes((1,0,0,1, 1,3,3,2, 0,2,0xFF,15, 1,2,0,2))
        control = bytes((4,16,2,0,2,1,0))
        result=decode_snapshot(control,events+bytes(128-len(events)))
        self.assertEqual([(e["kind"],e["port"]) for e in result["events"]],
                         [("fire",0),("fire",3),("key",2),("fire",2)])
        self.assertFalse(result["acquisition_verified"])
        full=bytes((0,0,0xFF,1))*32
        self.assertEqual(len(decode_snapshot(bytes((32,128,0,0,0,0,1)),full)["events"]),32)
        self.assertTrue(decode_snapshot(bytes((32,128,0,0,0,0,1)),full)["overflow"])
        self.assertEqual(decode_snapshot(bytes(7),bytes([255])*128)["events"],[])

    def test_invalid_controls_and_events_refuse(self):
        for control in (bytes(6),bytes((33,132,0,0,0,0,0)),
                        bytes((1,0,0,0,0,0,0)),bytes((0,0,0,0,0,0,1)),
                        bytes((32,128,0,0,0,0,2)),bytearray(7)):
            with self.assertRaises(AssemblyError):decode_snapshot(control,bytes(128))
        for event in ((2,0,0,1),(0,4,1,2),(0,0,0,1),(0,0,1,1),
                      (1,0,3,4),(1,0,255,0)):
            with self.subTest(event=event),self.assertRaises(AssemblyError):
                decode_snapshot(bytes((1,4,0,0,0,0,0)),bytes(event)+bytes(124))
        with self.assertRaises(AssemblyError):decode_snapshot(bytes(7),bytes(127))

    def test_fresh_cli_determinism_and_failure_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            cmd=[sys.executable,str(ROOT/"tools/input_callback_probe.py")]
            for part in ("a","b"):
                subprocess.run(cmd+["--output-dir",str(root/part)],check=True,capture_output=True,timeout=10)
            for name in ("input-callback.bin","input-callback.json"):
                self.assertEqual((root/"a"/name).read_bytes(),(root/"b"/name).read_bytes())
            self.assertEqual(json.loads((root/"a/input-callback.json").read_text())["size"],80)
            failed=subprocess.run(cmd+["--control","0x610","--output-dir",str(root/"bad")],capture_output=True,timeout=10)
            self.assertEqual(failed.returncode,2)
            self.assertFalse((root/"bad").exists())
