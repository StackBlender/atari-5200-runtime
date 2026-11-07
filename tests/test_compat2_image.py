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
from compat_image import compat_image
from compat2_image import compat2_image
from export_compat2_candidate import candidate,verify_checkout,EXTRA_INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN='3'*40
O=0xf800


class Compat2Tests(unittest.TestCase):
    def test_only_reviewed_bytes_change_and_fit(self):
        parent,before=compat_image();data,mapping=compat2_image()
        changed={i+O for i,(o,n) in enumerate(zip(parent,data)) if o!=n}
        allowed=({0xfcd9,0xfcda,0xfcdb,0xfca6,0xfca7,0xfe8c,0xfe8d,0xfe8e}|set(range(0xfce0,0xfcf0))
                 |set(range(0xfdc0,0xfdc0+29))|set(range(0xfde0,0xfded)))
        self.assertTrue(changed<=allowed,sorted(hex(a) for a in changed-allowed))
        self.assertEqual((len(data),mapping['used']-before['used']),(2048,16+29+13))
        self.assertEqual(data[-6:],parent[-6:])
        self.assertEqual(data[0x700:0x7fa],b'\xff'*250)
        self.assertIn('compat-v2',mapping['authored_capabilities'])

    def test_immediate_vector_default_policy(self):
        data,_=compat2_image()
        self.assertEqual(data[0x4d9:0x4dc],bytes.fromhex('4ce0fc'))
        self.assertEqual(data[0x4e0:0x4f0],bytes.fromhex('48ad0302c9fff00468' '6c0202' '68' '4ca0fc'))

    def test_timer_decrement_and_critic_order(self):
        data,_=compat2_image();c=data[0x5c0:0x5dd]
        self.assertEqual(c[:6],bytes.fromhex('e602d002e601'))          # frame counter unchanged
        self.assertEqual(c[6:19],bytes.fromhex('a203bd1c02f003de1c02ca10f5'))
        self.assertEqual(c[19:],bytes.fromhex('a503d0034c40fd4cb0fc'))  # CRITIC test, shadow update, exit
        self.assertEqual(data[0x4a6:0x4a8],bytes.fromhex('c0fd'))       # system_vbi enters here

    def test_deferred_vector_default_policy(self):
        data,_=compat2_image()
        self.assertEqual(data[0x68c:0x68f],bytes.fromhex('4ce0fd'))
        self.assertEqual(data[0x5e0:0x5ed],bytes.fromhex('ad0502c9ffd0034cb2fc6c0402'))

    def test_export_identity_and_pin_verification(self):
        data,mapping,text=candidate(PIN);manifest=json.loads(text);report=json.loads(mapping)
        self.assertEqual(report['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(manifest['image']['sha256'],report['sha256'])
        self.assertEqual(manifest['map_sha256'],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertTrue(manifest['version'].endswith('.compat-v2.candidate1'))
        self.assertFalse(manifest['provider_approved']);self.assertFalse(manifest['execution_verified'])
        for bad in ('e8f296d5a8fa693f13b5dd46259eafcb5567e88f','c1aaf9b2f3f3663f1263492dc4edabb8eb2c32df','4631c910bb07658827c04b9d5c244f35e4b4efc0'):
            with self.assertRaises(AssemblyError):candidate(bad)
        def pinned(cmd,**kw):return subprocess.CompletedProcess(cmd,0,stdout=b'different')
        with patch('subprocess.run',pinned):
            with self.assertRaises(AssemblyError):verify_checkout(ROOT,PIN)
        for relative in EXTRA_INPUTS:self.assertTrue((ROOT/relative).exists())


if __name__=='__main__':unittest.main()
