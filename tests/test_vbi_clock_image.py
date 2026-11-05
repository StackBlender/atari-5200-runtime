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
from startup_image import startup_image
from vbi_clock_image import ServiceImage, vbi_clock_image
from export_vbi_candidate import candidate, verify_vbi_checkout, EXTRA_INPUTS
from export_candidate import INPUTS

ROOT = Path(__file__).resolve().parents[1]
PIN = "1"*40


class VbiClockTests(unittest.TestCase):
    def test_exact_startup_and_defaults(self):
        data, report = vbi_clock_image()
        expected = bytes.fromhex(
            "78 d8 a2ff 9a a900 "
            "8d0ed4 8d00d4 8d0ee8 8d0fe8 8d01e8 8d03e8 8d05e8 8d07e8 "
            "8d1dc0 8d1bc0 8d1ac0 a902 8d01d4 a9f8 8d09d4 a900 8d0fd4 "
            "a218 9500 ca 10fb a200 a986 9d0002 e8 a9fc 9d0002 e8 e01c d0f0 "
            "a9a0 8d0202 a9fc 8d0302 a9b0 8d0402 a9fc 8d0502 "
            "20b0fe 18 b8 a000 a200 a900 6cfebf")
        self.assertEqual(len(expected),114)
        self.assertEqual(data[0x400:0x472],expected)
        self.assertEqual(data[0x472:0x480],b"\xff"*14)
        self.assertEqual(report["symbols"]["cart_handoff"],0xFC6F)
        self.assertEqual(report["symbols"]["system_vbi"],0xFCA0)
        self.assertEqual(report["symbols"]["vbi_exit"],0xFCB0)

    def test_exact_classifier_and_source_branch(self):
        data, report = vbi_clock_image()
        self.assertEqual(data[0x480:0x489],bytes.fromhex("4c80fc 4c83fc 4c86fc"))
        self.assertEqual(data[0x489:0x49A],bytes.fromhex("48 ad0fd4 29e0 c940 d0ed 8d0fd4 68 6c0202"))
        self.assertEqual(report["symbols"]["nmi_classifier"],0xFC89)
        self.assertEqual(data[-6:],bytes.fromhex("89fc 00fc 83fc"))

    def test_exact_register_stack_and_clock_paths(self):
        data, report = vbi_clock_image()
        self.assertEqual(data[0x4A0:0x4A8],bytes.fromhex("48 8a 48 98 48 4cf0fd"))
        self.assertEqual(data[0x4B0:0x4B6],bytes.fromhex("68 a8 68 aa 68 40"))
        self.assertEqual(data[0x5F0:0x600],bytes.fromhex("e601 d002 e602 a503 d003 6c0402 4cb0fc"))
        self.assertEqual(report["symbols"]["check_critic"],0xFDF6)
        self.assertEqual(report["symbols"]["critical_exit"],0xFDFD)

    def test_fit_reserves_and_baseline_assets_helper(self):
        data, report = vbi_clock_image()
        baseline, _ = startup_image()
        self.assertEqual(len(data),2048)
        self.assertEqual((report["used"],report["remaining"]),(1244,804))
        rows={r["name"]:r for r in report["allocations"]}
        for name,used in [("font",1024),("startup",114),("interrupts",40),
                          ("clocks",16),("shared",44),("vectors",6)]:
            self.assertEqual(rows[name]["used"],used)
        for name in ["input","display","margin"]:
            row=rows[name]
            self.assertEqual(row["used"],0)
            self.assertEqual(data[row["start"]-0xF800:row["end"]-0xF800],b"\xff"*(row["end"]-row["start"]))
        self.assertEqual(data[:1024],baseline[:1024])
        self.assertEqual(data[0x6B0:0x6DC],baseline[0x6B0:0x6DC])
        self.assertEqual(hashlib.sha256(baseline).hexdigest(),"b2d8ebb8d0070f2aee1bd79d7adfee85b88797702cb96035ab3a18e9bd37f68d")
        self.assertEqual(report["capabilities"],[])
        self.assertFalse(report["execution_verified"])
        self.assertFalse(report["provider_approved"])

    def test_local_encodings_strict_operands_and_no_global_mutation(self):
        before=dict(OPCODES)
        for mnemonic,mode,operand,expected in [("AND","imm",0xE0,"29e0"),
                ("INC","zp",1,"e601"),("TXA","impl",None,"8a"),
                ("TYA","impl",None,"98"),("TAX","impl",None,"aa"),("TAY","impl",None,"a8")]:
            image=ServiceImage([Region("code",0xF800,0x10000,"code")])
            image.instruction(mnemonic,mode,operand)
            self.assertEqual(image.data[:len(bytes.fromhex(expected))],bytes.fromhex(expected))
        for operand in [-1,256,True,"x",None]:
            with self.assertRaises(AssemblyError):
                ServiceImage([Region("code",0xF800,0x10000,"code")]).instruction("INC","zp",operand)
        with self.assertRaises(AssemblyError):
            ServiceImage([Region("code",0xF800,0x10000,"code")]).instruction("TAX","impl",1)
        vbi_clock_image()
        self.assertEqual(OPCODES,before)

    def test_manifest_identity_version_symbols_and_false_flags(self):
        image,map_text,manifest_text=candidate(PIN)
        mapping=json.loads(map_text); manifest=json.loads(manifest_text)
        self.assertEqual(manifest["source_revision"],PIN)
        self.assertEqual(mapping["source_revision"],PIN)
        self.assertEqual(manifest["version"],"cold-start-digits-v1.vbi-clock-v1.candidate1")
        self.assertEqual(manifest["image"]["sha256"],hashlib.sha256(image).hexdigest())
        self.assertEqual(manifest["map_sha256"],hashlib.sha256(map_text.encode()).hexdigest())
        self.assertEqual(manifest["symbols"],mapping["symbols"])
        self.assertEqual(manifest["symbols"]["cart_handoff"],0xFC6F)
        self.assertEqual(manifest["authored_capabilities"],["cold-start-digits-v1","vbi-clock-v1"])
        self.assertEqual(manifest["capabilities"],[])
        for key in ["execution_verified","provider_approved","retail_compatibility"]:
            self.assertFalse(manifest[key])
        self.assertFalse(manifest["timing"]["full_cycles_verified"])
        self.assertFalse(manifest["timing"]["default_vbi_full_cycles_verified"])
        self.assertTrue(manifest["startup_interrupt_acceptance_observation_required"])
        self.assertNotEqual(candidate("2"*40)[1:],(map_text,manifest_text))
        for bad in ["main","a"*39,"A"*40,True,None]:
            with self.assertRaises(AssemblyError): candidate(bad)

    def test_every_export_input_verified_and_mismatch_rejected(self):
        calls=[]
        def fake(command,**kwargs):
            relative=command[-1].split(":",1)[1]; calls.append(relative)
            return subprocess.CompletedProcess(command,0,(ROOT/relative).read_bytes())
        with patch("subprocess.run",side_effect=fake): verify_vbi_checkout(ROOT,PIN)
        self.assertEqual(calls,list(INPUTS)+list(EXTRA_INPUTS))
        for target in list(INPUTS)+list(EXTRA_INPUTS):
            def mismatch(command,**kwargs):
                relative=command[-1].split(":",1)[1]
                return subprocess.CompletedProcess(command,0,b"changed" if relative==target else (ROOT/relative).read_bytes())
            with patch("subprocess.run",side_effect=mismatch), self.assertRaises(AssemblyError):
                verify_vbi_checkout(ROOT,PIN)

    def test_fresh_process_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ["a","b"]:
                subprocess.run([sys.executable,str(ROOT/"tools/vbi_clock_image.py"),"--output-dir",str(root/name)],
                               check=True,capture_output=True,timeout=10)
            for name in ["vbi-clock.bin","vbi-clock-map.json"]:
                self.assertEqual((root/"a"/name).read_bytes(),(root/"b"/name).read_bytes())

    def test_stale_pin_cli_fails_before_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/"out"
            result=subprocess.run([sys.executable,str(ROOT/"tools/export_vbi_candidate.py"),
                "--source-revision","711a2e986f7906f45aebd310e6330fd7ffc338bf","--output-dir",str(output)],
                capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2)
            self.assertFalse(output.exists())
