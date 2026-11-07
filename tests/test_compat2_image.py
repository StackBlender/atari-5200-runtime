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
                 |set(range(0xfdc0,0xfdc0+29))|set(range(0xfde0,0xfded))
                 |set(range(0xfe4d,0xfe50))|set(range(0xfe95,0xfea1))|set(range(0xff00,0xff4c))|set(range(0xfcf0,0xfcfc))|set(range(0xfc8d,0xfc9c))|set(range(0xfdf0,0xfe00))
                 |set(range(0xfc00,0xfc0f))|set(range(0xfc74,0xfc7c)))
        self.assertTrue(changed<=allowed,sorted(hex(a) for a in changed-allowed))
        self.assertEqual((len(data),mapping['used']-before['used']),(2048,165))
        self.assertEqual(data[-6:],parent[-6:])
        self.assertEqual(data[0x74c:0x7fa],b'\xff'*174)          # rest of the reserve untouched
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

    def test_key_and_break_services(self):
        data,mapping=compat2_image()
        self.assertEqual(data[0x64d:0x650],bytes.fromhex('4c00ff'))      # unsupported-source branch targets enter the classifier
        self.assertEqual(data[0x700:0x708],bytes.fromhex('8a29c0d0034c83fc'))   # no bit 6/7 pending: fault as before
        self.assertEqual(data[0x4f0:0x4fc],bytes.fromhex('68a868aab0034c8dfc6c0c02'))   # restore X/Y; break, key
        self.assertEqual(data[0x48d:0x49c],bytes.fromhex('ad09020901c9fdd0034c20ff6c0802'))  # own $0208 handler is called
        self.assertEqual(data[0x720:0x73c],bytes.fromhex('8a489848ad09e84a290faabd3cffae0b02f008e8f0056c0a024cb2fc'))
        table=data[0x73c:0x74c]
        self.assertEqual(sorted(table),list(range(16)))     # table is a permutation
        for raw,value in ((0x1f,1),(0x05,0),(0x07,10),(0x03,11),(0x19,12),(0x11,13),(0x09,14),(0x0b,9)):
            self.assertEqual(table[(raw>>1)&15],value)        # observed KBCODE bits 4..1 -> value
        self.assertEqual(mapping['symbols']['key_value_table'],0xff3c)

    def test_default_vector_table(self):
        data,mapping=compat2_image()
        table=data[0x695:0x6a1]
        vectors=[table[i]|table[i+1]<<8 for i in range(0,12,2)]
        self.assertEqual(vectors,[0xfc03,0xfcb8,0xfcb2,0xfcdd,0xfc8d,0xfcb2])
        self.assertEqual(data[0x4dd],0x40)                                 # $FCDD is a bare RTI (DLI default)
        self.assertEqual(data[0x4dc:0x4de],bytes.fromhex('6840'))
        self.assertEqual(mapping['symbols']['default_vector_table'],0xfe95)

    def test_irq_default_entry_and_reset_entry(self):
        data,mapping=compat2_image()
        self.assertEqual(data[0x403:0x406],bytes.fromhex('4c00fe'))        # $FC03 = JMP $FE00
        self.assertEqual(data[0x400:0x403],bytes.fromhex('4c74fc'))        # reset entry
        self.assertEqual(data[0x474:0x47c],bytes.fromhex('78d8a2ff9a4c06fc'))
        self.assertEqual(data[0x406:0x40f],bytes.fromhex('a9008d0ed48d00d4ea'))
        self.assertEqual(data[0x40f:0x412],bytes.fromhex('8d0ee8'))        # callable boundary unchanged

    def test_export_identity_and_pin_verification(self):
        data,mapping,text=candidate(PIN);manifest=json.loads(text);report=json.loads(mapping)
        self.assertEqual(manifest['source_revision'],PIN);self.assertEqual(report['source_revision'],PIN)
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
