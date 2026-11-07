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
from callable_reset_image import callable_reset_image,RESET,END,ENTRY
from compat_image import compat_image
from export_compat_candidate import candidate,verify_checkout,EXTRA_INPUTS
from test_callable_reset_image import run_reinit
ROOT=Path(__file__).resolve().parents[1]
PIN='2'*40
O=0xf800


class CompatTests(unittest.TestCase):
    def test_only_reviewed_bytes_change_and_fit(self):
        parent,before=callable_reset_image();data,mapping=compat_image()
        changed={i+O for i,(o,n) in enumerate(zip(parent,data)) if o!=n}
        allowed=set(range(0xfc00+0x63,0xfc00+0x8d))|{0xfdf1,0xfdf5,0xfccd,0xfcdc,0xfcdd}|set(range(0xfcb0,0xfcbb))
        self.assertTrue(changed<=allowed,sorted(hex(a) for a in changed-allowed))
        self.assertEqual((len(data),mapping['used'],mapping['remaining']),(2048,1572,476))
        self.assertEqual(data[0x700:0x7fa],b'\xff'*250)          # reserve untouched
        self.assertEqual(data[-6:],parent[-6:])                  # vectors unchanged
        self.assertEqual(data[0x480:0x489],parent[0x480:0x489])  # fault stubs
        self.assertEqual(mapping['symbols']['nmi_spurious'],0xfcdc)
        self.assertIn('compat-v1',mapping['authored_capabilities'])

    def test_vbi_enabled_before_handoff_and_callable_layout_kept(self):
        data,_=compat_image();code=data[0x400:]
        i=code.index(bytes.fromhex('2080fd'))+3
        self.assertEqual(code[i:i+5],bytes.fromhex('a9408d0ed4'))      # LDA #$40, STA NMIEN
        self.assertEqual(code[END:END+3],bytes.fromhex('6cfebf'))
        self.assertEqual(code[ENTRY:ENTRY+3],bytes.fromhex('8d0ee8'))
        copied=run_reinit(data)
        self.assertEqual((copied['a'],copied['x'],copied['y'],copied['carry'],copied['overflow']),(0,0,0,0,0))
        self.assertEqual(copied['pc'],0x2100+END)
        self.assertIn((0xd40e,0x40),copied['stores'])
        self.assertEqual(copied['stores'].index((0xd40e,0x40)),len(copied['stores'])-1)   # last hardware write
        real=run_reinit(data,rom_start=0xfc0f)
        self.assertEqual(real['pc'],0xfc8a)

    def test_exit_entry_at_fcb2_and_default_vbi_alias(self):
        data,mapping=compat_image()
        self.assertEqual(data[0x4b0:0x4b8],bytes.fromhex('eaea68a868aa6840'))   # exit sequence starts at $FCB2
        self.assertEqual(data[0x4b8:0x4bb],bytes.fromhex('4ca0fc'))             # JMP system_vbi
        self.assertEqual(mapping['symbols']['vbi_exit_entry'],0xfcb2)
        self.assertEqual(mapping['symbols']['system_vbi'],0xfca0)

    def test_frame_counter_low_byte_is_0002(self):
        data,_=compat_image();body=data[0x5f0:0x5fb]
        self.assertEqual(body[:6],bytes.fromhex('e602d002e601'))       # INC 02; BNE +2; INC 01
        self.assertEqual(body[6:10],bytes.fromhex('a503d003'))         # CRITIC test unchanged

    def test_unflagged_nmi_returns_instead_of_faulting(self):
        data,_=compat_image();c=data[0x4c0:0x4de]
        self.assertEqual(c[:10],bytes.fromhex('48ad0fd429e0c940f00b'))
        self.assertEqual(c[0x0a:0x0d],bytes.fromhex('c980d0'))
        self.assertEqual(0xfcce+c[0x0d],0xfcdc)                        # BNE lands on spurious exit
        self.assertEqual(c[0x1c:0x1e],bytes.fromhex('6840'))           # PLA, RTI
        self.assertEqual(c[0x15:0x1c],bytes.fromhex('8d0fd4686c0202'))  # VBI path unchanged

    def test_export_identity_and_pin_verification(self):
        data,mapping,text=candidate(PIN);manifest=json.loads(text);report=json.loads(mapping)
        self.assertEqual(manifest['source_revision'],PIN);self.assertEqual(report['source_revision'],PIN)
        self.assertEqual(report['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(manifest['image']['sha256'],report['sha256'])
        self.assertEqual(manifest['map_sha256'],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertTrue(manifest['version'].endswith('.compat-v1.candidate1'))
        self.assertEqual((manifest['timing']['base_cycles_max'],manifest['timing']['diagnostic_second_ff_base_cycles_max']),(777,758))
        self.assertFalse(manifest['provider_approved']);self.assertFalse(manifest['execution_verified'])
        for bad in ('e8f296d5a8fa693f13b5dd46259eafcb5567e88f','c1aaf9b2f3f3663f1263492dc4edabb8eb2c32df'):
            with self.assertRaises(AssemblyError):candidate(bad)
        def pinned(cmd,**kw):return subprocess.CompletedProcess(cmd,0,stdout=b'different')
        with patch('subprocess.run',pinned):
            with self.assertRaises(AssemblyError):verify_checkout(ROOT,PIN)
        for relative in EXTRA_INPUTS:self.assertTrue((ROOT/relative).exists())


if __name__=='__main__':unittest.main()
