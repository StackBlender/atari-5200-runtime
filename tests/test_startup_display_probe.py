# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from emitter import AssemblyError
from startup_display_probe import bitmap,startup_display_probe
from export_startup_display_probes import export
ROOT=Path(__file__).resolve().parents[1]
CASES=[(board,entry,control,ff) for board,entries in
       (('Linear32K',(0x8000,)),('Linear8K',(0x8000,0xa000)))
       for entry,control,ff in itertools.product(entries,('direct','shadow'),(False,True))]


class StartupDisplayTests(unittest.TestCase):
    def test_independent_all240_original_geometric_bytes(self):
        top=bytes.fromhex('d5 55 55 55 55 aa aa aa aa ab')
        bottom=bytes.fromhex('ea aa aa aa aa 55 55 55 55 57')
        marker4=bytes.fromhex('d5 f5 55 55 55 aa aa aa aa ab')
        marker5=bytes.fromhex('d5 d5 55 55 55 aa aa aa aa ab')
        center_top=bytes.fromhex('d5 55 55 55 50 0a aa aa aa ab')
        center_bottom=bytes.fromhex('ea aa aa aa a0 05 55 55 55 57')
        expected=b'\xff'*10+top*3+marker4+marker5+top*4+center_top*2+center_bottom*2+bottom*9+b'\xff'*10
        self.assertEqual(len(expected),240)
        self.assertEqual(bitmap(),expected)

    def test_all12_exact_layout_metadata_and_zero_holes(self):
        for board,entry,control,ff in CASES:
            with self.subTest(board=board,entry=entry,control=control,ff=ff):
                data,m=startup_display_probe(board,entry,control,ff)
                size=32768 if board=='Linear32K' else 8192
                offset=0x4000 if board=='Linear32K' else 0
                self.assertEqual(len(data),size)
                self.assertEqual(data[-24:],b'P'*20+(b'\x00\xff' if ff else b'RV')+entry.to_bytes(2,'little'))
                self.assertEqual(data[offset+0x400:offset+0x420],bytes.fromhex('707070480010')+b'\x08'*23+bytes.fromhex('410008'))
                self.assertEqual(data[offset+0x500:offset+0x5f0],bitmap())
                self.assertEqual(data[offset:offset+3],bytes.fromhex('8d0030'))
                occupied=set(range(*m['code_payload']))|set(range(offset+0x400,offset+0x420))|set(range(offset+0x500,offset+0x5f0))|set(range(size-24,size))
                self.assertTrue(all(value==0 for i,value in enumerate(data) if i not in occupied))
                self.assertEqual(m['sha256'],hashlib.sha256(data).hexdigest())
                self.assertEqual(m['application_ram_write_windows'],[[0x800,0x820],[0x1000,0x10f0],[0x3000,0x300a]])
                self.assertLessEqual(m['code_cpu'][1],entry+0x400)

    def test_independent_capture_prefix_and_counter_carry_bytes(self):
        capture=bytes.fromhex('8d0030 8e0130 8c0230 08 68 8d0330 ba 8e0430 a9a5 8d0530')
        self.assertEqual(len(capture),23)
        for case in CASES:
            data,m=startup_display_probe(*case);offset=m['code_payload'][0]
            self.assertEqual(data[offset:offset+23],capture)
            loop=m['progress_loop_cpu'];start=offset+loop-m['entry']
            self.assertEqual(data[start:start+11],bytes.fromhex('ee0630 d003 ee0730 4c')+loop.to_bytes(2,'little'))
            self.assertEqual(m['first_opcode'],[0x8d,0,0x30])
            self.assertEqual(m['extra_stack_bytes'],1)

    def test_distinct_control_bytes_and_dma_last_no_new_vectors(self):
        values=((0xd402,0),(0xd403,8),(0xc012,0),(0xc013,0),(0xc014,0),(0xc015,0),
                (0xc016,6),(0xc017,10),(0xc018,14),(0xc019,0),(0xc01a,0),(0xd400,0x22))
        shadows=(5,6,8,9,10,11,12,13,14,15,16,7)
        for control in ('direct','shadow'):
            data,m=startup_display_probe(control=control)
            start=0x4000+m['setup_cpu']-0x8000
            if control=='direct':
                expected=b''.join(bytes((0xa9,v,0x8d,a&255,a>>8)) for a,v in values)
            else:
                expected=b''.join(bytes((0xa9,v,0x85,s)) for s,(_,v) in zip(shadows,values))+bytes.fromhex('a9408d0ed4')
            self.assertEqual(data[start:start+len(expected)],expected)
            self.assertEqual(data[start+len(expected):start+len(expected)+5],bytes.fromhex('a95a8d0830'))
            writes=[i['operand'] for i in m['instructions_after_capture'] if i['mnemonic']=='STA' and i['mode']=='abs']
            self.assertFalse(any(0x200<=a<0x21c for a in writes))
            self.assertEqual(m['public_shadow_writes'],[] if control=='direct' else list(shadows))

    def test_explicit_types_modes_and_unsupported_boards_rejected(self):
        for kwargs in ({'board':'OneChip16K'},{'board':'Linear32K','entry':0xa000},
                       {'entry':True},{'entry':0x7fff},{'board':'Linear8K','entry':0x9fe8},
                       {'control':'automatic'},{'second_ff':1}):
            with self.assertRaises(AssemblyError):startup_display_probe(**kwargs)

    def test_no_execution_reference_or_pixel_origin_claim(self):
        for case in CASES:
            _,m=startup_display_probe(*case)
            for field in ('native_execution_verified','provider_approved','private_input_used','cpu_engine','reference_role','new_runtime_service'):
                self.assertIs(m[field],False)
            self.assertIsNone(m['callback_origin']);self.assertIsNone(m['canonical_rgba_values'])
            self.assertEqual((m['max_ordinary_returns'],m['external_timeout_seconds']),(8,10))
            self.assertEqual(m['field_hires_pixels'],[320,192])

    def test_fresh_process_reproducibility_and_invalid_cli_no_output(self):
        with tempfile.TemporaryDirectory() as name:
            paths=[Path(name)/value for value in ('first','second')]
            for out in paths:
                subprocess.run([sys.executable,'-B',str(ROOT/'tools/startup_display_probe.py'),
                    '--board','Linear8K','--entry','0xa000','--control','shadow','--second-ff','--output-dir',str(out)],check=True,capture_output=True)
            for filename in ('original-startup-display.bin','original-startup-display.json'):
                self.assertEqual((paths[0]/filename).read_bytes(),(paths[1]/filename).read_bytes())
            out=Path(name)/'invalid'
            p=subprocess.run([sys.executable,'-B',str(ROOT/'tools/startup_display_probe.py'),'--board','Linear8K','--entry','0x9fe8','--control','direct','--output-dir',str(out)],capture_output=True)
            self.assertEqual(p.returncode,2);self.assertFalse(out.exists())

    def test_bad_or_mutated_pin_refuses_before_output(self):
        with tempfile.TemporaryDirectory() as name:
            out=Path(name)/'rejected'
            for revision in ('HEAD','1'*39,'G'*40):
                with self.assertRaises(ValueError):export(revision,out)
                self.assertFalse(out.exists())
            with patch('export_startup_display_probes.subprocess.run') as run:
                run.return_value.stdout=b'mutated input'
                with self.assertRaisesRegex(ValueError,'frozen input differs'):export('1'*40,out)
            self.assertFalse(out.exists())

    def test_real_frozen_twelve_case_export_in_fresh_processes(self):
        revision='30968a02ff474a21abcdb19faa8eac12c260c107'
        with tempfile.TemporaryDirectory() as name:
            outputs=[Path(name)/part for part in ('first','second')]
            for output in outputs:
                subprocess.run([sys.executable,'-B',str(ROOT/'tools/export_startup_display_probes.py'),
                    '--source-revision',revision,'--output-dir',str(output)],check=True,capture_output=True)
            first,second=outputs
            self.assertEqual(sorted(p.name for p in first.iterdir()),sorted(p.name for p in second.iterdir()))
            self.assertEqual(len(list(first.iterdir())),25)
            for item in first.iterdir():
                self.assertEqual(item.read_bytes(),(second/item.name).read_bytes())
            index=json.loads((first/'index.json').read_text())
            self.assertEqual(index['source_revision'],revision)
            self.assertEqual(len(index['source_inputs']),6)
            self.assertEqual(len(index['cases']),12)
            self.assertEqual(len({x['sha256'] for x in index['cases']}),12)
            for item in index['cases']:
                data=(first/(item['name']+'.bin')).read_bytes()
                descriptor=first/(item['name']+'.json')
                self.assertEqual(len(data),item['bytes'])
                self.assertEqual(hashlib.sha256(data).hexdigest(),item['sha256'])
                self.assertEqual(hashlib.sha256(descriptor.read_bytes()).hexdigest(),item['report_sha256'])
                mapping=json.loads(descriptor.read_text())
                self.assertEqual(mapping['source_revision'],revision)
                self.assertEqual(mapping['source_inputs'],index['source_inputs'])
                runtime=mapping['required_runtime']
                self.assertEqual(runtime['new_native_guard_required'],mapping['board']=='Linear8K')
                if mapping['board']=='Linear8K':
                    self.assertIsNone(runtime['qualified_native_revision'])
                    self.assertEqual(runtime['source_revision'],'2e8fd5152908e0c06d018d04bbfd9d07d1298703')
                else:
                    self.assertEqual(runtime['qualified_native_revision'],'138fad844c5c1877acd080bb7239b92d7e0bab9b')
            rejected=Path(name)/'parent-rejected'
            p=subprocess.run([sys.executable,'-B',str(ROOT/'tools/export_startup_display_probes.py'),
                '--source-revision','728adf499f4f4f2400d9260a58b35c1f97d230a0','--output-dir',str(rejected)],capture_output=True)
            self.assertEqual(p.returncode,2);self.assertFalse(rejected.exists())


if __name__=='__main__':unittest.main()
