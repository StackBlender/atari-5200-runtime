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
from keypad_window_image import keypad_window_image, ServiceImage
from keypad_irq_image import keypad_irq_image
from export_keypad_window_candidate import candidate, verify_keypad_window_checkout, EXTRA_INPUTS
from export_candidate import INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN="1"*40


class KeypadWindowTests(unittest.TestCase):
    def test_exact_ascending_analog_loop_and_four_port_rotation(self):
        data, report=keypad_window_image()
        self.assertEqual(data[0x540:0x559],bytes.fromhex("ad08e8 d011 a200 bd00e8 9511 e8 e008 d0f6 a900 8d0be8 4c1afd"))
        self.assertEqual(data[0x559:0x570],bytes.fromhex("ae0206 e8 8a 2903 8d0206 0904 8d1fc0 a901 8d0306 4c50fe"))
        self.assertEqual(report["symbols"]["analog_copy"],0xFD47)
        self.assertEqual(report["symbols"]["window_rotate"],0xFD59)
        self.assertEqual([0xE800+x for x in range(8)],list(range(0xE800,0xE808)))
        self.assertEqual([0x11+x for x in range(8)],list(range(0x11,0x19)))
        for p in range(4):self.assertEqual((((p+1)&3)|4)&3,(p+1)%4)

    def test_exact_busy_enabled_port_phase_guards_and_control_branches(self):
        data,_=keypad_window_image()
        expected=bytes.fromhex("ad0106 d089 ad0006 c901 d082 ae0206 e004 b00e ad0306 c901 f0c5 c902 d003 4c3cfe 4c83fc")
        self.assertEqual(len(expected),36)
        self.assertEqual(data[0x51A:0x53E],expected)
        self.assertEqual(data[0x4A8:0x4AE],bytes.fromhex("4c50fe 6c0a02"))

    def test_exact_invalid_window_defers_before_any_ack_or_publication(self):
        data,_=keypad_window_image()
        self.assertEqual(data[0x63C:0x650],bytes.fromhex("ad0506 d09e a500 2940 f009 ad0ee8 2940 f002 d08f"))
        self.assertEqual(data[0x5DF:0x5EB],bytes.fromhex("a500 29bf 8500 8d0ee8 4cdcfc"))

    def test_exact_contact_compare_store_callback_and_clobber_safe_rotation(self):
        data,report=keypad_window_image()
        expected=bytes.fromhex("ad0406 dd0606 f075 a8 bd0606 8d0a06 98 9d0606 8a ae0a06 20abfc 4c59fd 4c8ffe")
        self.assertEqual(data[0x4DC:0x4FC],expected)
        self.assertEqual(report["symbols"]["window_arm_bridge"],0xFCF9)
        # RTS callback JSR atFCF3 pushesFCF5 and resumesFCF6 -> unconditional
        # rotate reloads port from RAM; callback scratchAXY/flags cannot alter it.
        self.assertEqual(data[0x4F3:0x4F9],bytes.fromhex("20abfc 4c59fd"))

    def test_exact_fresh_arm_initializes_none_and_phase_before_enabled_mask(self):
        data,_=keypad_window_image()
        expected=bytes.fromhex("a900 8d0506 a9ff 8d0406 a902 8d0306 a500 29bf 8d0ee8 0940 8500 8d0ee8 4c50fe")
        self.assertEqual(len(expected),32)
        self.assertEqual(data[0x68F:0x6AF],expected)

    def test_full_fit_and_only_allowed_changes_preserve_kernel_startup_font(self):
        data,report=keypad_window_image();old,_=keypad_irq_image()
        self.assertEqual((len(data),report["used"],report["remaining"]),(2048,1746,302))
        allowed=set(range(0x540,0x575))|set(range(0x51A,0x53E))|set(range(0x4A8,0x4AE))|set(range(0x4DC,0x4FC))|set(range(0x63C,0x650))|set(range(0x5DF,0x5EB))|set(range(0x68F,0x6AF))
        self.assertTrue({i for i,(a,b) in enumerate(zip(data,old)) if a!=b}<=allowed)
        self.assertEqual(data[:0x480],old[:0x480])
        self.assertEqual(data[0x575:0x5DF],old[0x575:0x5DF])
        self.assertEqual(data[0x600:0x63C],old[0x600:0x63C])
        self.assertEqual(data[0x700:0x7FA],b"\xff"*250)
        self.assertEqual(data[-6:],old[-6:])
        self.assertEqual(hashlib.sha256(old).hexdigest(),"2fa0cbdbace0d70bab06953fef5bf08e065c6c6247a8a67692718307e75d6ef8")
        self.assertEqual({a["name"]:a["used"] for a in report["allocations"]},dict(font=1024,startup=120,interrupts=164,input=166,clocks=96,display=95,shared=75,margin=0,vectors=6))

    def test_local_new_encodings_bounds_and_no_global_mutation(self):
        original=dict(OPCODES)
        for mnemonic,mode,value,expected in (("ORA","imm",64,"0940"),("CMP","absx",0x606,"dd0606"),("LDX","abs",0x60A,"ae0a06")):
            image=ServiceImage([Region("code",0xF800,0x10000,"code")]);image.instruction(mnemonic,mode,value)
            self.assertEqual(bytes(image.data[:len(bytes.fromhex(expected))]),bytes.fromhex(expected))
            for bad in (-1,65536,True,None):
                with self.assertRaises(AssemblyError):image.instruction(mnemonic,mode,bad)
        keypad_window_image();self.assertEqual(OPCODES,original)

    def test_profile_callbacks_activation_false_approvals_hashes(self):
        data,mapping,encoded=candidate(PIN);m=json.loads(encoded);p=m["cooperating_cart"]
        self.assertEqual(m["runtime_abi"],"sb52-dev-input-v2")
        self.assertTrue(m["version"].endswith("keypad-windows-v1.candidate1"))
        self.assertTrue(p["automatic_port_rotation"] and p["event_callbacks"])
        self.assertFalse(p["fire_service"])
        self.assertEqual(p["key_callback"]["vector"],0x20A)
        self.assertEqual(p["key_callback"]["return"],"RTS")
        self.assertEqual(p["activation"]["committed_keys_fill"],255)
        self.assertTrue(p["activation"]["nmi_disabled"])
        self.assertEqual(p["reserved"]["start"],0x60B)
        self.assertEqual(m["capabilities"],[])
        for key in ("execution_verified","provider_approved","retail_compatibility"):self.assertFalse(m[key])
        self.assertTrue(all(v is False for k,v in m["timing"].items() if k.endswith("verified")))
        self.assertEqual(m["image"]["sha256"],hashlib.sha256(data).hexdigest())
        self.assertEqual(m["map_sha256"],hashlib.sha256(mapping.encode()).hexdigest())

    def test_all_pinned_inputs_refuse_and_prior_pin_fails_before_output(self):
        def fake(command,**kwargs):
            name=command[-1].split(":",1)[1]
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch("subprocess.run",side_effect=fake):verify_keypad_window_checkout(ROOT,PIN)
        for target in (*INPUTS,*EXTRA_INPUTS):
            def changed(command,**kwargs):
                name=command[-1].split(":",1)[1]
                return subprocess.CompletedProcess(command,0,b"changed" if name==target else (ROOT/name).read_bytes())
            with patch("subprocess.run",side_effect=changed),self.assertRaises(AssemblyError):verify_keypad_window_checkout(ROOT,PIN)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for n in ("a","b"):
                subprocess.run([sys.executable,str(ROOT/"tools/keypad_window_image.py"),"--output-dir",str(root/n)],check=True,capture_output=True,timeout=10)
            for n in ("keypad-window.bin","keypad-window-map.json"):
                self.assertEqual((root/"a"/n).read_bytes(),(root/"b"/n).read_bytes())
            result=subprocess.run([sys.executable,str(ROOT/"tools/export_keypad_window_candidate.py"),"--source-revision","b2e2b40d8c11326f1684635e35832fcc50f9f2d6","--output-dir",str(root/"out")],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2);self.assertFalse((root/"out").exists())
