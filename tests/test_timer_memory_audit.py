# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from timer_dispatch_image import timer_dispatch_image
from timer_memory_audit import AuditError,audit,_analyze,TIMER_SHA256
ROOT=Path(__file__).resolve().parents[1]


class TimerMemoryAuditTests(unittest.TestCase):
    def test_every_code_byte_and_conditional_memory_ownership(self):
        data,_=timer_dispatch_image();report=audit(data)
        self.assertEqual((report['instruction_count'],report['code_bytes_covered']),(220,474))
        self.assertEqual(report['image_sha256'],TIMER_SHA256)
        self.assertEqual(report['ram_write_ranges'],[[0,0x18],[0x100,0x21b]])
        self.assertEqual(report['ram_read_ranges'],[[0,3],[5,0x10],[0x100,0x207],[0x20e,0x20f],[0x216,0x21b]])
        self.assertEqual(report['application_operand_accesses'],[])
        self.assertEqual(report['cc65_conio_operand_accesses'],[])
        self.assertIs(report['execution_verified'],False)
        self.assertIs(report['ordinary_profile_approved'],False)
        self.assertEqual(report['software_pointer_frontiers'],[0x200,0x202,0x204,0x206,0x20e,0x216,0x218,0x21a,0xbffe])
        self.assertIn('consumer callback/cart code',report['external_boundaries'])

    def test_zero_vector_metadata_and_default_target_guards_fail_closed(self):
        data,_=timer_dispatch_image()
        for offset in (0x438,0x44d,0x6b1,0x6dd):
            changed=bytearray(data);changed[offset]^=1
            with self.subTest(offset=offset),self.assertRaises(AuditError):_analyze(bytes(changed))

    def test_application_ram_store_and_read_are_rejected_independently_of_hash(self):
        data,_=timer_dispatch_image()
        for offset in (0x408,0x4c2): # STA abs at FC07, LDA abs at FCC1
            changed=bytearray(data);changed[offset:offset+2]=(0x21c).to_bytes(2,'little')
            with self.subTest(offset=offset),self.assertRaises(AuditError):_analyze(bytes(changed))

    def test_unreviewed_opcode_branch_call_and_pointer_do_not_disappear(self):
        data,_=timer_dispatch_image();report=audit(data)
        cases=[]
        changed=bytearray(data);changed[0x401]=0xea;cases.append(bytes(changed))
        for kind in ('branch','call','indirect'):
            row=next(row for row in report['instructions'] if row['access']==kind and (kind=='call' or row['pc']>=0xfe00))
            changed=bytearray(data);offset=row['pc']-0xf800+1
            if kind=='branch':changed[offset]=0xff # target operand, not instruction
            else:changed[offset:offset+2]=(0x4000 if kind=='call' else 0x20c).to_bytes(2,'little')
            cases.append(bytes(changed))
        for changed in cases:
            with self.assertRaises(AuditError):_analyze(changed)

    def test_only_the_known_qualified_image_is_admitted(self):
        data,_=timer_dispatch_image()
        for value in (data[:-1],bytes(2048),bytearray(data)):
            with self.assertRaises(AuditError):audit(value)
        changed=bytearray(data);changed[0x403]^=1
        with self.assertRaises(AuditError):audit(bytes(changed))

    def test_fresh_cli_report_reproducibility_and_normal_refusal(self):
        data,_=timer_dispatch_image()
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'original-timer.bin';path.write_bytes(data)
            command=[sys.executable,str(ROOT/'tools/timer_memory_audit.py'),str(path)]
            first=subprocess.run(command,capture_output=True,check=True,timeout=10)
            second=subprocess.run(command,capture_output=True,check=True,timeout=10)
            self.assertEqual(first.stdout,second.stdout)
            self.assertEqual(json.loads(first.stdout),audit(data))
            path.write_bytes(data[:-1])
            refusal=subprocess.run(command,capture_output=True,timeout=10)
            self.assertEqual(refusal.returncode,2);self.assertEqual(refusal.stdout,b'')
