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
from emitter import AssemblyError
from timer_dispatch_image import timer_dispatch_image
from irq_brk_image import irq_brk_image
from export_timer_candidate import candidate, verify_timer_checkout, EXTRA_INPUTS
from export_candidate import INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN="1"*40


class TimerDispatchTests(unittest.TestCase):
    def test_exact_pending_priority_and_ack_paths(self):
        data,report=timer_dispatch_image()
        expected=bytes.fromhex(
            "48 8a 48 98 48 ad0ee8 49ff 2500 aa 29f8 d03c "
            "8a 2901 d028 8a 2902 d014 8a 2904 f02d "
            "a500 29fb 8d0ee8 a500 8d0ee8 6c1a02 "
            "a500 29fd 8d0ee8 a500 8d0ee8 6c1802 "
            "a500 29fe 8d0ee8 a500 8d0ee8 6c1602 4c83fc")
        self.assertEqual(len(expected),80)
        self.assertEqual(data[0x600:0x650],expected)
        for key,value in {"system_timer":0xFE00,"timer4":0xFE20,
                "timer2":0xFE2F,"timer1":0xFE3E,"timer_fault":0xFE4D}.items():
            self.assertEqual(report["symbols"][key],value)
        self.assertEqual(0xFE11+60,0xFE4D)
        self.assertEqual(0xFE16+40,0xFE3E)
        self.assertEqual(0xFE1B+20,0xFE2F)
        self.assertEqual(0xFE20+45,0xFE4D)

    def test_exact_startup_helper_and_return_locations(self):
        data,report=timer_dispatch_image();old,_=irq_brk_image()
        self.assertEqual(data[0x400:0x450],old[0x400:0x450])
        tail=bytes.fromhex("20dcfe a903 8d0fe8 a904 8d1fc0 8d0be8 20b0fe 18 b8 a000 a200 a900 6cfebf")
        self.assertEqual(len(tail),30)
        self.assertEqual(data[0x450:0x46E],tail)
        self.assertEqual(data[0x46E:0x480],b"\xff"*18)
        helper=bytes.fromhex("a9a0 8d0202 a9fc 8d0302 a9b0 8d0402 a9fc 8d0502 a900 8d0002 a9fe 8d0102 60")
        self.assertEqual(len(helper),31)
        self.assertEqual(data[0x6DC:0x6FB],helper)
        self.assertEqual(report["symbols"]["initialize_services"],0xFEDC)
        self.assertEqual(report["symbols"]["cart_handoff"],0xFC6B)
        self.assertEqual(data[0x460:0x463],bytes.fromhex("20b0fe"))

    def test_preserved_old_bytes_and_all_other_labels(self):
        data,report=timer_dispatch_image();prior,old=irq_brk_image()
        allowed=set(range(0x450,0x47F))|set(range(0x600,0x650))|set(range(0x6DC,0x6FB))
        self.assertTrue({i for i,(a,b) in enumerate(zip(data,prior)) if a!=b}<=allowed)
        for name,value in old["symbols"].items():
            if name!="cart_handoff":self.assertEqual(report["symbols"][name],value)
        self.assertEqual(hashlib.sha256(prior).hexdigest(),
            "2b257c582044af2308699c6a0f327dca674ed79bd95eed2da7cea2537ead0675")
        self.assertEqual(data[-6:],bytes.fromhex("c0fc 00fc 00fd"))

    def test_full_allocation_and_reserves(self):
        data,report=timer_dispatch_image()
        self.assertEqual((len(data),report["used"],report["remaining"]),(2048,1504,544))
        rows={row["name"]:row for row in report["allocations"]}
        for name,used in [("startup",110),("interrupts",77),("input",53),
                          ("clocks",96),("display",63),("shared",75)]:
            self.assertEqual(rows[name]["used"],used)
        self.assertEqual(rows["margin"]["used"],0)
        self.assertEqual(data[0x700:0x7FA],b"\xff"*250)
        self.assertEqual(data[0x6FB:0x700],b"\xff"*5)

    def test_new_local_opcodes_and_strict_operands(self):
        from emitter import OPCODES,Region
        from timer_dispatch_image import ServiceImage
        before=dict(OPCODES)
        for mnemonic,mode,value,encoded in [("EOR","imm",255,b"\x49\xff"),
                                            ("AND","zp",0,b"\x25\x00")]:
            image=ServiceImage([Region("code",0xF800,0x10000,"code")])
            image.instruction(mnemonic,mode,value)
            self.assertEqual(bytes(image.data[:2]),encoded)
            for bad in [-1,256,True,None,"0"]:
                with self.assertRaises(AssemblyError):image.instruction(mnemonic,mode,bad)
        timer_dispatch_image();self.assertEqual(OPCODES,before)

    def test_manifest_identity_and_false_approvals(self):
        data,mapping,encoded=candidate(PIN);m=json.loads(encoded)
        self.assertEqual(m["version"],
            "cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.dli-dispatch-v1.analog-shadow-v1.irq-brk-dispatch-v1.timer-dispatch-v1.candidate1")
        self.assertEqual(m["authored_capabilities"],
            ["cold-start-digits-v1","vbi-clock-v1","display-shadow-v1","dli-dispatch-v1","analog-shadow-v1","irq-brk-dispatch-v1","timer-dispatch-v1"])
        self.assertEqual(m["source_revision"],PIN)
        self.assertEqual(json.loads(mapping)["source_revision"],PIN)
        self.assertEqual(m["image"]["sha256"],hashlib.sha256(data).hexdigest())
        self.assertEqual(m["map_sha256"],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertEqual(m["symbols"]["system_timer"],0xFE00)
        self.assertEqual(m["symbols"]["cart_handoff"],0xFC6B)
        self.assertEqual(m["capabilities"],[])
        for key in ["execution_verified","provider_approved","retail_compatibility"]:
            self.assertFalse(m[key])
        for key in ["full_cycles_verified","default_vbi_full_cycles_verified",
                    "dli_dispatch_full_cycles_verified","irq_dispatch_full_cycles_verified",
                    "timer_full_cycles_verified"]:self.assertFalse(m["timing"][key])
        for key,value in {"base_cycles_max":1155,"default_vbi_base_cycles_min":240,
                "default_vbi_base_cycles_max":245,"timer1_body_base_cycles":56,
                "timer2_body_base_cycles":62,"timer4_body_base_cycles":67,
                "timer_complete_full_cycle_target":256}.items():
            self.assertEqual(m["timing"][key],value)
        for invalid in ["main","a"*39,"A"*40,True,None]:
            with self.assertRaises(AssemblyError):candidate(invalid)

    def test_each_pinned_input_refusal(self):
        calls=[]
        def fake(command,**kwargs):
            name=command[-1].split(":",1)[1];calls.append(name)
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch("subprocess.run",side_effect=fake):verify_timer_checkout(ROOT,PIN)
        self.assertEqual(calls,list(INPUTS)+list(EXTRA_INPUTS))
        for target in list(INPUTS)+list(EXTRA_INPUTS):
            def mismatch(command,**kwargs):
                name=command[-1].split(":",1)[1]
                return subprocess.CompletedProcess(command,0,
                    b"changed" if name==target else (ROOT/name).read_bytes())
            with patch("subprocess.run",side_effect=mismatch),self.assertRaises(AssemblyError):
                verify_timer_checkout(ROOT,PIN)

    def test_fresh_process_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ["a","b"]:
                subprocess.run([sys.executable,str(ROOT/"tools/timer_dispatch_image.py"),
                    "--output-dir",str(root/name)],check=True,capture_output=True,timeout=10)
            for name in ["timer-dispatch.bin","timer-dispatch-map.json"]:
                self.assertEqual((root/"a"/name).read_bytes(),(root/"b"/name).read_bytes())

    def test_real_prior_source_pin_refuses_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/"out"
            result=subprocess.run([sys.executable,str(ROOT/"tools/export_timer_candidate.py"),
                "--source-revision","42762a73a0caa72b7753bd5aa4380cf9a63c573f",
                "--output-dir",str(output)],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2)
            self.assertFalse(output.exists())
