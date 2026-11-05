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
from dli_dispatch_image import dli_dispatch_image
from display_shadow_image import display_shadow_image
from export_dli_candidate import candidate, verify_dli_checkout, EXTRA_INPUTS
from export_candidate import INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN="1"*40


class DliDispatchTests(unittest.TestCase):
    def test_independent_classifier_and_branch_destinations(self):
        data, report=dli_dispatch_image()
        self.assertEqual(data[0x4C0:0x4DC],bytes.fromhex(
            "48 ad0fd4 29e0 c940 f00b c980 d0b2 8d0fd4 68 6c0602 8d0fd4 68 6c0202"))
        self.assertEqual(report["symbols"]["nmi_classifier"],0xFCC0)
        self.assertEqual(report["symbols"]["vbi_source"],0xFCD5)
        self.assertEqual(0xFCCA+11,0xFCD5)
        self.assertEqual(0xFCCE-78,0xFC80)
        self.assertEqual(data[-6:],bytes.fromhex("c0fc 00fc 83fc"))

    def test_only_intended_differences_and_preserved_startup_contract(self):
        data, report=dli_dispatch_image()
        prior, prior_report=display_shadow_image()
        allowed=set(range(0x489,0x49A))|set(range(0x4C0,0x4DC))|{0x7FA,0x7FB}
        actual={i for i,(a,b) in enumerate(zip(data,prior)) if a!=b}
        self.assertTrue(actual<=allowed)
        self.assertEqual(data[0x489:0x49A],b"\xff"*17)
        self.assertEqual(data[0x400:0x472],prior[0x400:0x472])
        self.assertEqual(data[0x480:0x489],bytes.fromhex("4c80fc 4c83fc 4c86fc"))
        self.assertEqual(data[0x4A0:0x4A8],bytes.fromhex("48 8a 48 98 48 4cf0fd"))
        self.assertEqual(data[0x4B0:0x4B6],bytes.fromhex("68 a8 68 aa 68 40"))
        for name,value in prior_report["symbols"].items():
            if name!="nmi_classifier": self.assertEqual(report["symbols"][name],value)
        self.assertEqual(hashlib.sha256(prior).hexdigest(),
            "1992e64b05d096e479c9532b14a77839bad182428b459a3ca8862ede51acb364")

    def test_full_fit_and_reserved_bounds(self):
        data,report=dli_dispatch_image()
        self.assertEqual((len(data),report["used"],report["remaining"]),(2048,1318,730))
        rows={row["name"]:row for row in report["allocations"]}
        self.assertEqual(rows["interrupts"]["used"],51)
        self.assertEqual(rows["display"]["used"],63)
        for name in ["input","margin"]:
            row=rows[name];self.assertEqual(row["used"],0)
            self.assertEqual(data[row["start"]-0xF800:row["end"]-0xF800],
                             b"\xff"*(row["end"]-row["start"]))

    def test_manifest_false_labels_and_identity(self):
        data,mapping,encoded=candidate(PIN);m=json.loads(encoded)
        self.assertEqual(m["version"],
            "cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.dli-dispatch-v1.candidate1")
        self.assertEqual(m["authored_capabilities"],
            ["cold-start-digits-v1","vbi-clock-v1","display-shadow-v1","dli-dispatch-v1"])
        self.assertEqual(m["source_revision"],PIN)
        self.assertEqual(json.loads(mapping)["source_revision"],PIN)
        self.assertEqual(m["image"]["sha256"],hashlib.sha256(data).hexdigest())
        self.assertEqual(m["map_sha256"],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertEqual(m["symbols"]["nmi_classifier"],0xFCC0)
        self.assertEqual(m["capabilities"],[])
        for key in ["execution_verified","provider_approved","retail_compatibility"]:
            self.assertFalse(m[key])
        for key in ["full_cycles_verified","default_vbi_full_cycles_verified",
                    "dli_dispatch_full_cycles_verified"]: self.assertFalse(m["timing"][key])
        self.assertEqual(m["timing"]["default_vbi_base_cycles_min"],169)
        self.assertEqual(m["timing"]["default_vbi_base_cycles_max"],174)
        self.assertEqual(m["timing"]["dli_dispatch_base_cycles"],30)
        self.assertEqual(m["timing"]["dli_dispatch_full_cycle_target"],128)
        self.assertTrue(m["startup_interrupt_acceptance_observation_required"])
        for invalid in ["main","a"*39,"A"*40,True,None]:
            with self.assertRaises(AssemblyError):candidate(invalid)

    def test_each_pinned_input_refusal(self):
        calls=[]
        def fake(command,**kwargs):
            name=command[-1].split(":",1)[1];calls.append(name)
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch("subprocess.run",side_effect=fake):verify_dli_checkout(ROOT,PIN)
        self.assertEqual(calls,list(INPUTS)+list(EXTRA_INPUTS))
        for target in list(INPUTS)+list(EXTRA_INPUTS):
            def mismatch(command,**kwargs):
                name=command[-1].split(":",1)[1]
                return subprocess.CompletedProcess(command,0,
                    b"changed" if name==target else (ROOT/name).read_bytes())
            with patch("subprocess.run",side_effect=mismatch),self.assertRaises(AssemblyError):
                verify_dli_checkout(ROOT,PIN)

    def test_fresh_process_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ["a","b"]:
                subprocess.run([sys.executable,str(ROOT/"tools/dli_dispatch_image.py"),
                    "--output-dir",str(root/name)],check=True,capture_output=True,timeout=10)
            for name in ["dli-dispatch.bin","dli-dispatch-map.json"]:
                self.assertEqual((root/"a"/name).read_bytes(),(root/"b"/name).read_bytes())

    def test_real_prior_source_pin_refuses_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/"out"
            result=subprocess.run([sys.executable,str(ROOT/"tools/export_dli_candidate.py"),
                "--source-revision","9d7071f837ec513905b4a2f9718e269c7662b90c",
                "--output-dir",str(output)],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2)
            self.assertFalse(output.exists())
