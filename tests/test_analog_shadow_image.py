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
from analog_shadow_image import analog_shadow_image
from dli_dispatch_image import dli_dispatch_image
from export_analog_candidate import candidate, verify_analog_checkout, EXTRA_INPUTS
from export_candidate import INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN="1"*40


class AnalogShadowTests(unittest.TestCase):
    def test_exact_prime_startup_and_handoff(self):
        data,report=analog_shadow_image(); prior,_=dli_dispatch_image()
        expected=bytes.fromhex(
            "a903 8d0fe8 a904 8d1fc0 8d0be8 20b0fe 18 b8 a000 a200 a900 6cfebf")
        self.assertEqual(len(expected),27)
        self.assertEqual(data[0x400:0x464],prior[0x400:0x464])
        self.assertEqual(data[0x464:0x47F],expected)
        self.assertEqual(data[0x47F],255)
        self.assertEqual(report["symbols"]["cart_handoff"],0xFC7C)
        self.assertEqual(data[0x471:0x474],bytes.fromhex("20b0fe"))

    def test_exact_analog_pending_copy_restart_and_critic_routing(self):
        data,report=analog_shadow_image()
        expected=bytes.fromhex(
            "ad08e8 d02d ad00e8 8511 ad01e8 8512 ad02e8 8513 ad03e8 8514 "
            "ad04e8 8515 ad05e8 8516 ad06e8 8517 ad07e8 8518 a900 8d0be8 4c50fe")
        self.assertEqual(len(expected),53)
        self.assertEqual(data[0x540:0x575],expected)
        self.assertEqual(report["symbols"]["analog_transfer"],0xFD40)
        self.assertEqual(report["symbols"]["analog_exit"],0xFD72)
        self.assertEqual(0xFD45+45,0xFD72)
        self.assertEqual(data[0x5F0:0x600],bytes.fromhex(
            "e601 d002 e602 a503 d003 4c40fd 4cb0fc"))

    def test_only_intended_differences_fit_and_no_extra_reserves(self):
        data,report=analog_shadow_image();prior,old=dli_dispatch_image()
        allowed=set(range(0x464,0x47F))|set(range(0x540,0x575))|set(range(0x5FA,0x5FD))
        self.assertTrue({i for i,(a,b) in enumerate(zip(data,prior)) if a!=b}<=allowed)
        for name,value in old["symbols"].items():
            if name!="cart_handoff":self.assertEqual(report["symbols"][name],value)
        self.assertEqual(hashlib.sha256(prior).hexdigest(),
            "374465be3cfce3d15c10c7899f4fedbd8cf854b23ee1734b9302c7049e55e05c")
        self.assertEqual((len(data),report["used"],report["remaining"]),(2048,1384,664))
        rows={row["name"]:row for row in report["allocations"]}
        for name,used in [("startup",127),("input",53),("interrupts",51),("display",63)]:
            self.assertEqual(rows[name]["used"],used)
        self.assertEqual(rows["margin"]["used"],0)
        self.assertEqual(data[0x700:0x7FA],b"\xff"*250)

    def test_manifest_false_labels_timing_and_identity(self):
        data,mapping,encoded=candidate(PIN);m=json.loads(encoded)
        self.assertEqual(m["version"],
            "cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.dli-dispatch-v1.analog-shadow-v1.candidate1")
        self.assertEqual(m["authored_capabilities"],
            ["cold-start-digits-v1","vbi-clock-v1","display-shadow-v1","dli-dispatch-v1","analog-shadow-v1"])
        self.assertEqual(m["source_revision"],PIN)
        self.assertEqual(json.loads(mapping)["source_revision"],PIN)
        self.assertEqual(m["image"]["sha256"],hashlib.sha256(data).hexdigest())
        self.assertEqual(m["map_sha256"],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertEqual(m["symbols"]["cart_handoff"],0xFC7C)
        self.assertEqual(m["capabilities"],[])
        for key in ["execution_verified","provider_approved","retail_compatibility"]:
            self.assertFalse(m[key])
        for key in ["full_cycles_verified","default_vbi_full_cycles_verified",
                    "dli_dispatch_full_cycles_verified"]:self.assertFalse(m["timing"][key])
        expected={"base_cycles_max":1131,"default_vbi_base_cycles_min":240,
                  "default_vbi_base_cycles_max":245,"analog_complete_base_cycles":71,
                  "analog_pending_base_cycles":10,"pending_vbi_base_cycles_min":179,
                  "pending_vbi_base_cycles_max":184}
        for key,value in expected.items():self.assertEqual(m["timing"][key],value)
        self.assertTrue(m["startup_interrupt_acceptance_observation_required"])
        for invalid in ["main","a"*39,"A"*40,True,None]:
            with self.assertRaises(AssemblyError):candidate(invalid)

    def test_each_pinned_input_refusal(self):
        calls=[]
        def fake(command,**kwargs):
            name=command[-1].split(":",1)[1];calls.append(name)
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch("subprocess.run",side_effect=fake):verify_analog_checkout(ROOT,PIN)
        self.assertEqual(calls,list(INPUTS)+list(EXTRA_INPUTS))
        for target in list(INPUTS)+list(EXTRA_INPUTS):
            def mismatch(command,**kwargs):
                name=command[-1].split(":",1)[1]
                return subprocess.CompletedProcess(command,0,
                    b"changed" if name==target else (ROOT/name).read_bytes())
            with patch("subprocess.run",side_effect=mismatch),self.assertRaises(AssemblyError):
                verify_analog_checkout(ROOT,PIN)

    def test_fresh_process_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ["a","b"]:
                subprocess.run([sys.executable,str(ROOT/"tools/analog_shadow_image.py"),
                    "--output-dir",str(root/name)],check=True,capture_output=True,timeout=10)
            for name in ["analog-shadow.bin","analog-shadow-map.json"]:
                self.assertEqual((root/"a"/name).read_bytes(),(root/"b"/name).read_bytes())

    def test_real_prior_source_pin_refuses_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/"out"
            result=subprocess.run([sys.executable,str(ROOT/"tools/export_analog_candidate.py"),
                "--source-revision","258bc0cc764a0614ec8443a89d242a8f1fe8cb5e",
                "--output-dir",str(output)],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2)
            self.assertFalse(output.exists())
