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
from export_candidate import candidate, verify_checkout, INPUTS


class ExportCandidateTests(unittest.TestCase):
    def test_complete_identity_and_independent_image(self):
        data, mapping, text = candidate("a"*40)
        manifest=json.loads(text)
        report=json.loads(mapping)
        self.assertEqual(len(data),2048)
        self.assertEqual(hashlib.sha256(data).hexdigest(),
                         "b2d8ebb8d0070f2aee1bd79d7adfee85b88797702cb96035ab3a18e9bd37f68d")
        self.assertEqual(manifest["image"],dict(origin=0xF800,size=2048,sha256=hashlib.sha256(data).hexdigest()))
        self.assertEqual(manifest["map_sha256"],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertEqual(manifest["source_revision"],"a"*40)
        self.assertEqual(report["source_revision"],"a"*40)
        self.assertEqual(manifest["schema"],1)
        self.assertEqual(manifest["abi"],1)
        self.assertEqual(manifest["fault_symbols"],dict(nmi_fault=0xFC80,irq_fault=0xFC83,startup_fault=0xFC86))

    def test_export_does_not_depend_on_execution_gate(self):
        _,_,text=candidate("b"*40)
        manifest=json.loads(text)
        self.assertEqual(manifest["authored_capabilities"],["cold-start-digits-v1"])
        self.assertEqual(manifest["capabilities"],[])
        self.assertIs(manifest["execution_verified"],False)
        self.assertIs(manifest["provider_approved"],False)
        self.assertIs(manifest["timing"]["full_cycles_verified"],False)
        self.assertEqual(manifest["reset_policy"]["supported"],["cold"])
        self.assertTrue(manifest["reset_policy"]["reject_unsupported_before_mutation"])
        self.assertEqual(manifest["mapper"]["board"],"Linear32K")

    def test_revision_types_and_format_reject(self):
        for revision in [None,True,123,"a"*39,"a"*41,"A"*40,"g"*40,"HEAD","-"*40]:
            with self.subTest(revision=revision), self.assertRaises(AssemblyError):
                candidate(revision)

    def test_deterministic_revision_bound_manifest(self):
        first=candidate("a"*40)
        self.assertEqual(candidate("a"*40),first)
        second=candidate("b"*40)
        self.assertEqual(first[0],second[0])
        self.assertNotEqual(first[1],second[1])
        self.assertNotEqual(first[2],second[2])
        self.assertNotIn(str(Path(__file__).resolve().parents[1]),first[2])

    def test_modified_pinned_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            # Controlled Git transport result: checks the mismatch gate itself,
            # not a purported real-source or runtime execution receipt.
            (root/"CMakeLists.txt").write_bytes(b"modified")
            with patch("export_candidate.subprocess.run",return_value=subprocess.CompletedProcess([],0,b"pinned",b"")):
                with self.assertRaisesRegex(AssemblyError,"differs from pinned"):
                    verify_checkout(root,"a"*40)

    def test_all_declared_inputs_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in INPUTS:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b"same")
            with patch("export_candidate.subprocess.run",return_value=subprocess.CompletedProcess([],0,b"same",b"")) as run:
                verify_checkout(root,"a"*40)
                self.assertEqual(run.call_count,len(INPUTS))

    def test_invalid_cli_creates_no_outputs(self):
        script=Path(__file__).resolve().parents[1]/"tools/export_candidate.py"
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/"absent"
            result=subprocess.run([sys.executable,str(script),"--source-revision","HEAD",
                                   "--output-dir",str(output)],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2)
            self.assertEqual(result.stdout,b"")
            self.assertFalse(output.exists())
