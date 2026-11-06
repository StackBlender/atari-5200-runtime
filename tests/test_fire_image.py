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
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from emitter import AssemblyError, OPCODES
from fire_image import fire_image, ServiceImage
from keypad_window_image import keypad_window_image
from export_fire_candidate import candidate, verify_fire_checkout, EXTRA_INPUTS
from export_candidate import INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN="1"*40


class FireImageTests(unittest.TestCase):
    def test_exact_bottom_sampling_baseline_store_and_callback_reload(self):
        data,report=fire_image()
        expected=bytes.fromhex(
            "ad0006 c901 d047 a200 8e1906 bd10c0 49ff 2901 8d1b06 "
            "bd1006 2902 0d1b06 8d1b06 bd1006 cd1b06 f018 "
            "8d1a06 ad1b06 9d1006 ad1406 f00a ac1b06 8a ae1a06 2096ff "
            "ae1906 e8 e004 d0c0 a901 8d1406 4c1afd")
        self.assertEqual(data[0x700:0x751],expected)
        self.assertEqual(report["symbols"]["bottom_fire"],0xFF00)

    def test_exact_top_independent_kr2_baseline_and_clobber_safe_rotate(self):
        data,report=fire_image()
        expected=bytes.fromhex(
            "ae0206 ad0fe8 49ff 2908 4a 4a 8d1b06 bd1006 2901 0d1b06 8d1b06 "
            "bd1006 cd1b06 f018 8d1a06 ad1b06 9d1006 bd1506 f00a "
            "ac1b06 8a ae1a06 2096ff ae0206 a901 9d1506 4c59fd 6c0802")
        self.assertEqual(data[0x751:0x799],expected)
        self.assertEqual(report["symbols"]["top_fire"],0xFF51)
        self.assertEqual(report["symbols"]["fire_callback_bridge"],0xFF96)

    def test_exact_routing_branches_and_only_reviewed_changes(self):
        data,_=fire_image();parent,_=keypad_window_image()
        self.assertEqual(data[0x496:0x499],bytes.fromhex("4c51ff"))
        self.assertEqual(data[0x556:0x559],bytes.fromhex("4c00ff"))
        self.assertEqual(data[0x4E2:0x4E4],bytes.fromhex("f0b2"))
        self.assertEqual(0xFCE4-78,0xFC96)
        self.assertEqual(data[0x4F6:0x4F9],bytes.fromhex("4c51ff"))
        allowed=set(range(0x496,0x499))|set(range(0x556,0x559))|set(range(0x4E2,0x4E4))|set(range(0x4F6,0x4F9))|set(range(0x700,0x799))
        self.assertTrue({i for i,(a,b) in enumerate(zip(data,parent)) if a!=b}<=allowed)
        self.assertEqual(data[:0x489],parent[:0x489])
        self.assertEqual(data[-6:],parent[-6:])
        self.assertEqual(hashlib.sha256(parent).hexdigest(),"3c1b419b9af94645ea537126d21e464f90f05013689ef7132656680d62d4207a")

    def test_exact_cumulative_fit_and_variant_only_margin(self):
        original=dict(OPCODES);data,report=fire_image()
        self.assertEqual((len(data),report["used"],report["remaining"]),(2048,1902,146))
        self.assertEqual(report["used"]-1504,398)
        self.assertEqual(1904-report["used"],2)
        self.assertEqual(report["remaining"]-90,56)
        self.assertEqual(data[0x799:0x7A0],b"\xff"*7)
        self.assertEqual(data[0x7A0:0x7FA],b"\xff"*90)
        rows={r["name"]:r["used"] for r in report["allocations"]}
        self.assertEqual(rows,dict(font=1024,startup=120,interrupts=167,input=166,clocks=96,display=95,shared=75,fire=153,margin=0,vectors=6))
        old=json.loads((ROOT/"docs/allocation-plan.json").read_text())
        self.assertEqual(next(r for r in old["regions"] if r["name"]=="margin")["start"],0xFF00)
        self.assertEqual(OPCODES,original)

    def test_reviewed_allocation_and_aggregate_overflow_stop(self):
        read=Path.read_text
        for name,end in (("fire",0xFF9F),("margin",0xFFF9)):
            allocation=json.loads((ROOT/"docs/fire-allocation.json").read_text())
            next(r for r in allocation["regions"] if r["name"]==name)["end"]=end
            def changed(path,*args,**kwargs):
                return json.dumps(allocation) if path==ROOT/"docs/fire-allocation.json" else read(path,*args,**kwargs)
            with patch.object(Path,"read_text",changed),self.assertRaises(AssemblyError):fire_image()
        finish=ServiceImage.finish
        def too_large(image):
            data,report=finish(image);report["used"]=1905;return data,report
        with patch.object(ServiceImage,"finish",too_large),self.assertRaises(AssemblyError):fire_image()

    def test_profile_readiness_aged_sources_limits_and_false_labels(self):
        data,mapping,encoded=candidate(PIN);m=json.loads(encoded);p=m["cooperating_cart"]
        self.assertEqual(m["runtime_abi"],"sb52-dev-input-fire-v3")
        self.assertEqual(p["required_cart_declaration"],"sb52-dev-input-fire-v3-ram600-61f-unlatched-v1")
        self.assertEqual(p["fire_callback"]["vector"],0x208)
        self.assertEqual(p["fire_callback"]["return"],"RTS")
        self.assertEqual(p["fire_policy"]["maximum_callbacks_per_vbi"],6)
        self.assertTrue(p["fire_policy"]["bitmap_sources_independently_aged"])
        for flag in ("unknown_is_release","busy_callback_protected_snapshot_coherent","step_exit_poll_cadence_equivalent","gractl_violation_automatically_detected","critic_freezes_irq_capture"):
            self.assertFalse(p["fire_policy"][flag])
        self.assertEqual([(r["start"],r["end_exclusive"]) for r in p["reserved"]],[(0x60B,0x610),(0x61C,0x620)])
        self.assertEqual(m["capabilities"],[])
        for flag in ("execution_verified","provider_approved","retail_compatibility"):self.assertFalse(m[flag])
        self.assertTrue(all(v is False for k,v in m["timing"].items() if k.endswith("verified")))
        self.assertEqual(m["timing"]["default_vbi_full_cycle_target"],4096)
        self.assertEqual(m["timing"]["full_cycle_target"],4096)
        self.assertEqual(m["image"]["sha256"],hashlib.sha256(data).hexdigest())
        self.assertEqual(m["map_sha256"],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertEqual(m["provenance"]["allocation_sha256"],hashlib.sha256((ROOT/"docs/fire-allocation.json").read_bytes()).hexdigest())

    def test_every_pinned_input_checked_before_cli_output(self):
        def fake(command,**kwargs):
            name=command[-1].split(":",1)[1]
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch("subprocess.run",side_effect=fake):verify_fire_checkout(ROOT,PIN)
        for target in (*INPUTS,*EXTRA_INPUTS):
            def changed(command,**kwargs):
                name=command[-1].split(":",1)[1]
                return subprocess.CompletedProcess(command,0,b"changed" if name==target else (ROOT/name).read_bytes())
            with patch("subprocess.run",side_effect=changed),self.assertRaises(AssemblyError):verify_fire_checkout(ROOT,PIN)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"out"
            result=subprocess.run([sys.executable,str(ROOT/"tools/export_fire_candidate.py"),"--source-revision","fce294b7448a7c5a1a35e6c5e5ed5611ee36473f","--output-dir",str(out)],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2);self.assertFalse(out.exists())

    def test_fresh_unexported_image_map_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for part in ("a","b"):
                subprocess.run([sys.executable,str(ROOT/"tools/fire_image.py"),"--output-dir",str(root/part)],check=True,capture_output=True,timeout=10)
            for name in ("fire.bin","fire-map.json"):
                self.assertEqual((root/"a"/name).read_bytes(),(root/"b"/name).read_bytes())
