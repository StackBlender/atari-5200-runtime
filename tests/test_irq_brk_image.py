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
from irq_brk_image import irq_brk_image
from analog_shadow_image import analog_shadow_image
from export_irq_candidate import candidate, verify_irq_checkout, EXTRA_INPUTS
from export_candidate import INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN="1"*40


class IrqBrkTests(unittest.TestCase):
    def test_exact_classifier_branch_and_vectors(self):
        data,report=irq_brk_image()
        expected=bytes.fromhex("48 8a 48 ba e8 e8 e8 bd0001 2910 d006 68 aa 68 6c0002 68 aa 68 6c0e02")
        self.assertEqual(len(expected),26)
        self.assertEqual(data[0x500:0x51A],expected)
        self.assertEqual(report["symbols"]["irq_classifier"],0xFD00)
        self.assertEqual(report["symbols"]["irq_dispatch"],0xFD0E)
        self.assertEqual(report["symbols"]["brk_dispatch"],0xFD14)
        self.assertEqual(0xFD0E+6,0xFD14)
        self.assertEqual(data[-6:],bytes.fromhex("c0fc 00fc 00fd"))

    def test_stack_index_algebra_all_256_positions(self):
        # Static layout arithmetic only: no instruction or CPU interpreter.
        # Hardware pushes PC high/low/P; dispatcher pushes A/X, then X+3.
        for interrupted_sp in range(256):
            p_address=0x100+((interrupted_sp-2)&255)
            saved_sp=(interrupted_sp-5)&255
            index=(saved_sp+3)&255
            self.assertEqual(0x100+index,p_address)
            self.assertLessEqual(0x100+index,0x1FF)
            slots=[(interrupted_sp-offset)&255 for offset in range(5)]
            self.assertEqual(len(set(slots)),5)
        # Absolute0103+X would escape stack page for these actual wrap cases.
        for saved_sp in [253,254,255]:self.assertGreater(0x103+saved_sp,0x1FF)

    def test_only_new_body_and_hardware_vector_differ(self):
        data,report=irq_brk_image();prior,old=analog_shadow_image()
        allowed=set(range(0x500,0x51A))|{0x7FE,0x7FF}
        self.assertTrue({i for i,(a,b) in enumerate(zip(data,prior)) if a!=b}<=allowed)
        for name,value in old["symbols"].items():self.assertEqual(report["symbols"][name],value)
        self.assertEqual(hashlib.sha256(prior).hexdigest(),
            "32343a567399b3b4f9c142bde446fe89397267267d51a89393553fdab9471290")
        self.assertEqual(data[0x400:0x47F],prior[0x400:0x47F])
        self.assertEqual(data[0x480:0x489],bytes.fromhex("4c80fc 4c83fc 4c86fc"))

    def test_fit_and_preserved_margins(self):
        data,report=irq_brk_image()
        self.assertEqual((len(data),report["used"],report["remaining"]),(2048,1410,638))
        rows={row["name"]:row for row in report["allocations"]}
        for name,used in [("startup",127),("interrupts",77),("input",53),("display",63)]:
            self.assertEqual(rows[name]["used"],used)
        self.assertEqual(rows["margin"]["used"],0)
        self.assertEqual(data[0x700:0x7FA],b"\xff"*250)
        self.assertEqual(data[0x47F],255)

    def test_manifest_false_labels_and_dispatch_contract(self):
        data,mapping,encoded=candidate(PIN);m=json.loads(encoded)
        self.assertEqual(m["version"],
            "cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.dli-dispatch-v1.analog-shadow-v1.irq-brk-dispatch-v1.candidate1")
        self.assertEqual(m["authored_capabilities"],
            ["cold-start-digits-v1","vbi-clock-v1","display-shadow-v1","dli-dispatch-v1","analog-shadow-v1","irq-brk-dispatch-v1"])
        self.assertEqual(m["source_revision"],PIN)
        self.assertEqual(json.loads(mapping)["source_revision"],PIN)
        self.assertEqual(m["image"]["sha256"],hashlib.sha256(data).hexdigest())
        self.assertEqual(m["map_sha256"],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertEqual(m["symbols"]["irq_classifier"],0xFD00)
        self.assertEqual(m["fault_symbols"]["irq_fault"],0xFC83)
        self.assertEqual(m["symbols"]["cart_handoff"],0xFC7C)
        self.assertEqual(m["capabilities"],[])
        for key in ["execution_verified","provider_approved","retail_compatibility"]:
            self.assertFalse(m[key])
        for key in ["full_cycles_verified","default_vbi_full_cycles_verified",
                    "dli_dispatch_full_cycles_verified","irq_dispatch_full_cycles_verified"]:
            self.assertFalse(m["timing"][key])
        for key,value in {"base_cycles_max":1131,"default_vbi_base_cycles_min":240,
                "default_vbi_base_cycles_max":245,"irq_dispatch_base_cycles":39,
                "brk_dispatch_base_cycles":40,"irq_dispatch_full_cycle_target":128}.items():
            self.assertEqual(m["timing"][key],value)
        self.assertTrue(m["startup_interrupt_acceptance_observation_required"])
        for invalid in ["main","a"*39,"A"*40,True,None]:
            with self.assertRaises(AssemblyError):candidate(invalid)

    def test_each_pinned_input_refusal(self):
        calls=[]
        def fake(command,**kwargs):
            name=command[-1].split(":",1)[1];calls.append(name)
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch("subprocess.run",side_effect=fake):verify_irq_checkout(ROOT,PIN)
        self.assertEqual(calls,list(INPUTS)+list(EXTRA_INPUTS))
        for target in list(INPUTS)+list(EXTRA_INPUTS):
            def mismatch(command,**kwargs):
                name=command[-1].split(":",1)[1]
                return subprocess.CompletedProcess(command,0,
                    b"changed" if name==target else (ROOT/name).read_bytes())
            with patch("subprocess.run",side_effect=mismatch),self.assertRaises(AssemblyError):
                verify_irq_checkout(ROOT,PIN)

    def test_fresh_process_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ["a","b"]:
                subprocess.run([sys.executable,str(ROOT/"tools/irq_brk_image.py"),
                    "--output-dir",str(root/name)],check=True,capture_output=True,timeout=10)
            for name in ["irq-brk.bin","irq-brk-map.json"]:
                self.assertEqual((root/"a"/name).read_bytes(),(root/"b"/name).read_bytes())

    def test_real_prior_source_pin_refuses_without_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/"out"
            result=subprocess.run([sys.executable,str(ROOT/"tools/export_irq_candidate.py"),
                "--source-revision","a6c406e4cee090b8044eea3b9b6c7a5b6391b3ab",
                "--output-dir",str(output)],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2)
            self.assertFalse(output.exists())
