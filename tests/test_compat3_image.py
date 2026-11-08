# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from emitter import AssemblyError
from compat2_image import compat2_image
from compat3_image import compat3_image
from export_compat3_candidate import candidate,verify_checkout,EXTRA_INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN='3'*40
O=0xf800


class Compat3Tests(unittest.TestCase):
    def test_only_reviewed_bytes_change_and_fit(self):
        parent,before=compat2_image();data,mapping=compat3_image()
        changed={i+O for i,(o,n) in enumerate(zip(parent,data)) if o!=n}
        allowed=set(range(0xfc8d,0xfc9c))|{0xfcf9,0xfcfa,0xfcfb}|{0xff05,0xff06,0xff07}|set(range(0xff4c,0xff7d))
        self.assertTrue(changed<=allowed,sorted(hex(a) for a in changed-allowed))
        self.assertEqual((len(data),mapping['used']-before['used']),(2048,37))
        self.assertEqual(data[-6:],parent[-6:])
        self.assertEqual(data[0x77d:0x7fa],b'\xff'*125)           # rest of the reserve untouched
        self.assertIn('compat-v3',mapping['authored_capabilities'])
        self.assertIn('compat-v2',mapping['authored_capabilities'])

    def test_key_vector_check(self):
        data,mapping=compat3_image()
        self.assertEqual(data[0x48d:0x490],bytes.fromhex('4c4cff'))        # old check now jumps to the new one
        self.assertEqual(data[0x74c:0x761],bytes.fromhex('ad0902c9fff00c0901c9fdd0034c20ff6c08026840'))
        # BEQ at FF51 (+0C) lands on PLA/RTI at FF5F; BNE at FF57 (+3) lands on JMP ($0208) at FF5C
        self.assertEqual(0xff53+0x0c,0xff5f);self.assertEqual(0xff59+3,0xff5c)
        self.assertEqual(data[0x75f:0x761],bytes.fromhex('6840'))
        self.assertEqual(mapping['symbols']['irq_key_vector_check'],0xff4c)

    def test_break_vector_check(self):
        data,mapping=compat3_image()
        self.assertEqual(data[0x4f0:0x4fc],bytes.fromhex('68a868aab0034c8dfc4c61ff'))
        self.assertEqual(data[0x761:0x76d],bytes.fromhex('ad0d02c9ffd00268406c0c02'))
        self.assertEqual(0xff68+2,0xff6a)                                   # BNE skips PLA/RTI
        self.assertEqual(mapping['symbols']['irq_break_vector_check'],0xff61)

    def test_unsupported_source_is_dropped_not_faulted(self):
        data,mapping=compat3_image()
        self.assertEqual(data[0x700:0x708],bytes.fromhex('8a29c0d0034c6dff'))
        self.assertEqual(data[0x76d:0x77d],bytes.fromhex('a9008d0ee8a5008d0ee8' '68a868aa6840'))
        self.assertEqual(mapping['symbols']['irq_drop_unsupported'],0xff6d)

    def test_export_identity_and_pin_verification(self):
        data,mapping,text=candidate(PIN);manifest=json.loads(text);report=json.loads(mapping)
        self.assertEqual(manifest['source_revision'],PIN);self.assertEqual(report['source_revision'],PIN)
        self.assertEqual(report['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(manifest['image']['sha256'],report['sha256'])
        self.assertEqual(manifest['map_sha256'],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertTrue(manifest['version'].endswith('.compat-v3.candidate1'))
        self.assertFalse(manifest['provider_approved']);self.assertFalse(manifest['execution_verified'])
        for bad in ('e8f296d5a8fa693f13b5dd46259eafcb5567e88f','c1aaf9b2f3f3663f1263492dc4edabb8eb2c32df','214e1e4a3caabc3c17693bd5271d2e9ce0761428','9ecf093f50f139bbcc1be08cb98a5cb11e252081'):
            with self.assertRaises(AssemblyError):candidate(bad)
        def pinned(cmd,**kw):return subprocess.CompletedProcess(cmd,0,stdout=b'different')
        with patch('subprocess.run',pinned):
            with self.assertRaises(AssemblyError):verify_checkout(ROOT,PIN)
        for relative in EXTRA_INPUTS:self.assertTrue((ROOT/relative).exists())


if __name__=='__main__':unittest.main()
