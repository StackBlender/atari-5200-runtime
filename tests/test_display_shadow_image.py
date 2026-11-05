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
from display_shadow_image import display_shadow_image
from export_display_candidate import candidate, verify_display_checkout, EXTRA_INPUTS
from export_candidate import INPUTS
from vbi_clock_image import vbi_clock_image
from startup_image import startup_image
ROOT = Path(__file__).resolve().parents[1]
PIN = "1"*40


class DisplayShadowTests(unittest.TestCase):
    def test_independent_exact_transfer_bytes_and_order(self):
        data, report = display_shadow_image()
        expected = bytes.fromhex(
            "a505 8d02d4 a506 8d03d4 "
            "a508 8d12c0 a509 8d13c0 a50a 8d14c0 a50b 8d15c0 "
            "a50c 8d16c0 a50d 8d17c0 a50e 8d18c0 a50f 8d19c0 "
            "a510 8d1ac0 a507 8d00d4 6c0402")
        self.assertEqual(len(expected), 63)
        self.assertEqual(data[0x650:0x68F], expected)
        self.assertEqual(report["symbols"]["display_transfer"], 0xFE50)
        self.assertEqual(data[0x68F:0x6B0], b"\xff"*33)

    def test_critic_routing_and_old_image_only_intended_byte_differences(self):
        data, report = display_shadow_image()
        prior, old_report = vbi_clock_image()
        self.assertEqual(data[0x5F0:0x600], bytes.fromhex(
            "e601 d002 e602 a503 d003 4c50fe 4cb0fc"))
        allowed = set(range(0x5FA, 0x5FD)) | set(range(0x650, 0x68F))
        actual = {i for i, (a,b) in enumerate(zip(data,prior)) if a != b}
        self.assertTrue(actual <= allowed)
        self.assertEqual(actual & set(range(0x5FA,0x5FD)), set(range(0x5FA,0x5FD)))
        for name, value in old_report["symbols"].items():
            self.assertEqual(report["symbols"][name], value)
        self.assertEqual(hashlib.sha256(prior).hexdigest(),
            "62df6162ac3accdfa19769c8f2dcd450c510e385fa71f98ec7912f61d449fa54")
        self.assertEqual(hashlib.sha256(startup_image()[0]).hexdigest(),
            "b2d8ebb8d0070f2aee1bd79d7adfee85b88797702cb96035ab3a18e9bd37f68d")

    def test_fit_and_full_reserved_range(self):
        data, report = display_shadow_image()
        self.assertEqual(len(data), 2048)
        self.assertEqual((report["used"], report["remaining"]), (1307,741))
        rows = {row["name"]:row for row in report["allocations"]}
        for name, used in [("font",1024),("startup",114),("interrupts",40),
                           ("clocks",16),("display",63),("shared",44),("vectors",6)]:
            self.assertEqual(rows[name]["used"], used)
        for name in ["input","margin"]:
            row=rows[name]
            self.assertEqual(row["used"],0)
            self.assertEqual(data[row["start"]-0xF800:row["end"]-0xF800],
                             b"\xff"*(row["end"]-row["start"]))

    def test_manifest_bound_to_image_map_and_false_approvals(self):
        data, mapping, encoded = candidate(PIN)
        manifest = json.loads(encoded)
        self.assertEqual(manifest["version"],
            "cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.candidate1")
        self.assertEqual(manifest["image"]["sha256"],hashlib.sha256(data).hexdigest())
        self.assertEqual(manifest["map_sha256"],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertEqual(manifest["source_revision"], PIN)
        self.assertEqual(json.loads(mapping)["source_revision"], PIN)
        self.assertEqual(manifest["symbols"]["display_transfer"],0xFE50)
        self.assertEqual(manifest["authored_capabilities"],
            ["cold-start-digits-v1","vbi-clock-v1","display-shadow-v1"])
        self.assertEqual(manifest["capabilities"],[])
        for key in ["execution_verified","provider_approved","retail_compatibility"]:
            self.assertFalse(manifest[key])
        for key in ["full_cycles_verified","default_vbi_full_cycles_verified"]:
            self.assertFalse(manifest["timing"][key])
        self.assertEqual(manifest["timing"]["default_vbi_base_cycles_min"],168)
        self.assertEqual(manifest["timing"]["default_vbi_base_cycles_max"],173)
        self.assertNotEqual(candidate("2"*40)[1:], (mapping,encoded))
        for bad in ["HEAD", "a"*39, "A"*40, True, None]:
            with self.assertRaises(AssemblyError): candidate(bad)

    def test_every_generation_input_pinned_and_mismatch_fails(self):
        calls=[]
        def fake(command,**kwargs):
            relative=command[-1].split(":",1)[1]; calls.append(relative)
            return subprocess.CompletedProcess(command,0,(ROOT/relative).read_bytes())
        with patch("subprocess.run",side_effect=fake): verify_display_checkout(ROOT,PIN)
        self.assertEqual(calls,list(INPUTS)+list(EXTRA_INPUTS))
        for target in list(INPUTS)+list(EXTRA_INPUTS):
            def mismatch(command,**kwargs):
                relative=command[-1].split(":",1)[1]
                return subprocess.CompletedProcess(command,0,
                    b"changed" if relative==target else (ROOT/relative).read_bytes())
            with patch("subprocess.run",side_effect=mismatch), self.assertRaises(AssemblyError):
                verify_display_checkout(ROOT,PIN)

    def test_fresh_process_reproducibility(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ["a","b"]:
                subprocess.run([sys.executable,str(ROOT/"tools/display_shadow_image.py"),
                    "--output-dir",str(root/name)],check=True,capture_output=True,timeout=10)
            for name in ["display-shadow.bin","display-shadow-map.json"]:
                self.assertEqual((root/"a"/name).read_bytes(),(root/"b"/name).read_bytes())

    def test_prior_vbi_pin_export_fails_without_creating_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/"out"
            result=subprocess.run([sys.executable,str(ROOT/"tools/export_display_candidate.py"),
                "--source-revision","ba90c8550c1be1c85b5aa7d6810e1ee6c6031656",
                "--output-dir",str(output)],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2)
            self.assertFalse(output.exists())
