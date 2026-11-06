# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"tools"))
from emitter import AssemblyError, OPCODES, Region
from keypad_irq_image import keypad_irq_image, ServiceImage
from timer_dispatch_image import timer_dispatch_image
from export_keypad_irq_candidate import candidate, verify_keypad_irq_checkout, EXTRA_INPUTS
from export_candidate import INPUTS
ROOT = Path(__file__).resolve().parents[1]
PIN = "1"*40


class KeypadIRQTests(unittest.TestCase):
    def test_exact_irq_frame_source_priority_and_branch_bridges(self):
        image, report = keypad_irq_image()
        self.assertEqual(image[0x489:0x496], bytes.fromhex("48 8a 48 98 48 a901 8d0106 4c75fd"))
        expected = bytes.fromhex(
            "ad0ee8 49ff 2500 aa 29b8 d052 8a 2940 d017 "
            "8a 2901 d04b 8a 2902 d049 8a 2904 d047 "
            "a900 8d0106 4cb0fc")
        self.assertEqual(len(expected), 40)
        self.assertEqual(image[0x575:0x59D], expected)
        self.assertEqual(image[0x5D3:0x5DF], bytes.fromhex("4c83fc 4c28fe 4c14fe 4c00fe"))
        self.assertEqual(report["symbols"]["system_input_irq"],0xFC89)
        # Parent's wrap-safe classifier removes its temporary saves BEFORE
        # entering this sole AXY frame; no timer prologue is chained afterward.
        old, _ = timer_dispatch_image()
        self.assertEqual(image[0x500:0x51A], old[0x500:0x51A])

    def test_exact_first_handler_read_normalization_publication_and_ack(self):
        image, report = keypad_irq_image()
        expected = bytes.fromhex(
            "ad0006 c901 d023 ad0306 c902 d01c ad0506 d017 "
            "ad0206 c904 b01c ad09e8 291e 4a f014 "
            "8d0406 a901 8d0506 a500 29bf 8500 8d0ee8 4c95fd")
        self.assertEqual(len(expected),54)
        self.assertEqual(image[0x59D:0x5D3],expected)
        self.assertEqual(report["symbols"]["keyboard_ack"],0xFDC7)
        # Algebra checks just the documented bit projection, not chip capture.
        for raw in range(256):
            self.assertEqual((raw & 0x1E) >> 1, (raw//2)%16)

    def test_exact_timer_transactions_busy_cleared_after_final_mask_write(self):
        image, _ = keypad_irq_image()
        expected = bytes.fromhex(
            "a500 29fb 8d0ee8 a500 8d0ee8 a900 8d0106 6c1a02 "
            "a500 29fd 8d0ee8 a500 8d0ee8 a900 8d0106 6c1802 "
            "a500 29fe 8d0ee8 a500 8d0ee8 a900 8d0106 6c1602")
        self.assertEqual(len(expected),60)
        self.assertEqual(image[0x600:0x63C],expected)
        self.assertEqual(image[0x63C:0x650],b"\xff"*20)

    def test_cold_ram_clear_fast_prime_handoff_and_helper(self):
        image, report = keypad_irq_image()
        tail=bytes.fromhex("20dcfe a900 a21f 9d0006 ca 10fa a906 8d0fe8 a904 8d1fc0 8d0be8 20b0fe 18 b8 a000 a200 a900 6cfebf")
        self.assertEqual(image[0x450:0x478],tail)
        self.assertEqual(report["symbols"]["cart_handoff"],0xFC75)
        self.assertEqual(report["symbols"]["zero_input_state"],0xFC57)
        self.assertEqual(image[0x6DC:0x6FB],bytes.fromhex(
            "a9a0 8d0202 a9fc 8d0302 a9b0 8d0402 a9fc 8d0502 a989 8d0002 a9fc 8d0102 60"))
        self.assertEqual(image[-6:],bytes.fromhex("c0fc 00fc 00fd"))

    def test_actual_fit_only_reviewed_ranges_and_all_prior_bytes(self):
        image, report = keypad_irq_image();old, _ = timer_dispatch_image()
        self.assertEqual((len(image),report["used"],report["remaining"]),(2048,1613,435))
        allowed=set(range(0x450,0x480))|set(range(0x489,0x496))|set(range(0x575,0x5DF))|set(range(0x600,0x650))|{0x6F1,0x6F6}
        self.assertTrue({i for i,(a,b) in enumerate(zip(image,old)) if a!=b}<=allowed)
        self.assertEqual(hashlib.sha256(old).hexdigest(),"eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550")
        self.assertEqual(image[0x700:0x7FA],b"\xff"*250)
        rows={a["name"]:a["used"] for a in report["allocations"]}
        self.assertEqual(rows,dict(font=1024,startup=120,interrupts=90,input=159,clocks=76,display=63,shared=75,margin=0,vectors=6))

    def test_new_opcode_local_only_and_strict(self):
        original=dict(OPCODES)
        image=ServiceImage([Region("code",0xF800,0x10000,"code")])
        image.instruction("LSR")
        self.assertEqual(image.data[0],0x4A)
        for invalid in (0,True,"A"):
            with self.assertRaises(AssemblyError):image.instruction("LSR",operand=invalid)
        keypad_irq_image()
        self.assertEqual(OPCODES,original)

    def test_new_identity_cart_contract_false_labels_and_unknown_timing(self):
        image,mapping,encoded=candidate(PIN);manifest=json.loads(encoded)
        self.assertEqual(manifest["runtime_abi"],"sb52-dev-input-v2")
        self.assertTrue(manifest["version"].endswith("keypad-irq-latch-v1.candidate1"))
        self.assertEqual(json.loads(mapping)["runtime_abi"],manifest["runtime_abi"])
        profile=manifest["cooperating_cart"]
        self.assertEqual(profile["ram"],dict(start=0x600,end_exclusive=0x620,cold_fill=0))
        self.assertEqual(profile["application_ram_min"],0x620)
        self.assertEqual(profile["reserved"],dict(start=0x606,end_exclusive=0x620,cold_fill=0))
        self.assertEqual([f["address"] for f in profile["fields"]],list(range(0x600,0x606)))
        for key in ("automatic_port_rotation","fire_service","event_callbacks","legacy_cc65_profile_compatible"):
            self.assertFalse(profile[key])
        self.assertTrue(profile["successful_preflight_before_power"])
        self.assertEqual(manifest["capabilities"],[])
        for key in ("execution_verified","provider_approved","retail_compatibility"):
            self.assertFalse(manifest[key])
        self.assertTrue(all(value is False for key,value in manifest["timing"].items() if key.endswith("verified")))
        self.assertEqual(manifest["image"]["sha256"],hashlib.sha256(image).hexdigest())
        self.assertEqual(manifest["map_sha256"],hashlib.sha256(mapping.encode()).hexdigest())
        for bad in ("main","A"*40,"a"*39,True):
            with self.assertRaises(AssemblyError):candidate(bad)

    def test_every_generation_input_checked_and_each_dirty_source_refused(self):
        calls=[]
        def fake(command,**kwargs):
            name=command[-1].split(":",1)[1];calls.append(name)
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch("subprocess.run",side_effect=fake):verify_keypad_irq_checkout(ROOT,PIN)
        self.assertEqual(calls,list(INPUTS)+list(EXTRA_INPUTS))
        for target in (*INPUTS,*EXTRA_INPUTS):
            def mismatch(command,**kwargs):
                name=command[-1].split(":",1)[1]
                return subprocess.CompletedProcess(command,0,b"changed" if name==target else (ROOT/name).read_bytes())
            with patch("subprocess.run",side_effect=mismatch),self.assertRaises(AssemblyError):
                verify_keypad_irq_checkout(ROOT,PIN)

    def test_fresh_process_generation_and_prior_pin_refuses_before_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ("a","b"):
                subprocess.run([sys.executable,str(ROOT/"tools/keypad_irq_image.py"),"--output-dir",str(root/name)],check=True,capture_output=True,timeout=10)
            for name in ("keypad-irq.bin","keypad-irq-map.json"):
                self.assertEqual((root/"a"/name).read_bytes(),(root/"b"/name).read_bytes())
            result=subprocess.run([sys.executable,str(ROOT/"tools/export_keypad_irq_candidate.py"),"--source-revision","ac9b47e50c213b08022e78bdef64662569cd3d29","--output-dir",str(root/"out")],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2)
            self.assertFalse((root/"out").exists())
