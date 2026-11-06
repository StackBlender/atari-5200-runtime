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
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from emitter import AssemblyError, OPCODES
from fire_bridge_image import fire_bridge_image, ServiceImage
from fire_image import fire_image
from export_fire_bridge_candidate import candidate, verify_fire_bridge_checkout, EXTRA_INPUTS
from export_candidate import INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN='1'*40


class FireBridgeImageTests(unittest.TestCase):
    def test_exact_full_relocated_fragment_and_hooks(self):
        data,report=fire_bridge_image()
        expected=bytes.fromhex(
            'ad0006 c901 d040 a200 8e1906 bd10c0 49ff 2901 8d1b06 '
            'bd1006 2902 0d1b06 8d1b06 bd1006 cd1b06 f011 '
            '8d1a06 ad1b06 9d1006 ad1406 f003 2088ff '
            'ae1906 e8 e004 d0c7 a901 8d1406 4c1afd '
            'ae0206 ad0fe8 49ff 2908 4a 4a 8d1b06 bd1006 2901 0d1b06 8d1b06 '
            'bd1006 cd1b06 f011 8d1a06 ad1b06 9d1006 bd1506 f003 '
            '2088ff ae0206 a901 9d1506 4c59fd '
            'ac1b06 8a ae1a06 6c0802')
        self.assertEqual(len(expected),146)
        self.assertEqual(data[0x700:0x792],expected)
        self.assertEqual(data[0x496:0x499],bytes.fromhex('4c4aff'))
        self.assertEqual(data[0x4E2:0x4E4],bytes.fromhex('f0b2'))
        self.assertEqual(data[0x4F6:0x4F9],bytes.fromhex('4c4aff'))
        self.assertEqual(data[0x556:0x559],bytes.fromhex('4c00ff'))
        self.assertEqual(report['symbols']['top_fire'],0xFF4A)
        self.assertEqual(report['symbols']['fire_callback_bridge'],0xFF88)

    def test_cumulative_fit_reserve_and_only_approved_differences(self):
        before=dict(OPCODES);data,report=fire_bridge_image();old,_=fire_image()
        self.assertEqual((len(data),report['used'],report['remaining']),(2048,1895,153))
        self.assertEqual((report['used']-1504,1904-report['used'],report['remaining']-90),(391,9,63))
        self.assertEqual(data[0x792:0x7A0],b'\xff'*14)
        self.assertEqual(data[0x7A0:0x7FA],b'\xff'*90)
        allowed=set(range(0x496,0x499))|set(range(0x4F6,0x4F9))|set(range(0x700,0x799))
        self.assertTrue({i for i,(a,b) in enumerate(zip(data,old)) if a!=b}<=allowed)
        self.assertEqual(data[:0x496],old[:0x496])
        self.assertEqual(data[0x4F9:0x700],old[0x4F9:0x700])
        self.assertEqual(data[-6:],old[-6:])
        self.assertEqual(hashlib.sha256(old).hexdigest(),'e937064b0d1fe33d0f75cfe4dba89bcbec953adc215f83ed51ce4fee8705f815')
        self.assertEqual({r['name']:r['used'] for r in report['allocations']},dict(font=1024,startup=120,interrupts=167,input=166,clocks=96,display=95,shared=75,fire=146,margin=0,vectors=6))
        self.assertEqual(OPCODES,before)

    def test_exact_return_pcs_shared_setup_and_post_callback_reload(self):
        data,report=fire_bridge_image()
        # JSR pushes the address of its last operand; RTS adds one.
        self.assertEqual(data[0x737:0x73A],bytes.fromhex('2088ff'))
        self.assertEqual(data[0x77A:0x77D],bytes.fromhex('2088ff'))
        self.assertEqual(data[0x73A:0x73D],bytes.fromhex('ae1906'))
        self.assertEqual(data[0x77D:0x780],bytes.fromhex('ae0206'))
        self.assertEqual(data[0x788:0x792],bytes.fromhex('ac1b06 8a ae1a06 6c0802'))
        for pc,resume in ((0xFF37,0xFF3A),(0xFF7A,0xFF7D)):
            self.assertEqual(pc+2+1,resume)
        self.assertEqual(report['symbols']['bottom_next'],0xFF3A)
        self.assertEqual(report['symbols']['top_baseline'],0xFF7D)

    def test_allocation_and_budget_deviations_still_stop(self):
        read=Path.read_text
        allocation=json.loads((ROOT/'docs/fire-allocation.json').read_text())
        next(r for r in allocation['regions'] if r['name']=='fire')['end']=0xFFA1
        def changed(path,*args,**kwargs):
            return json.dumps(allocation) if path==ROOT/'docs/fire-allocation.json' else read(path,*args,**kwargs)
        with patch.object(Path,'read_text',changed),self.assertRaises(AssemblyError):fire_bridge_image()
        finish=ServiceImage.finish
        def oversized(image):
            data,report=finish(image);report['used']=1905;return data,report
        with patch.object(ServiceImage,'finish',oversized),self.assertRaises(AssemblyError):fire_bridge_image()

    def test_manifest_preserves_semantic_profile_false_labels_and_new_identity(self):
        data,mapping,encoded=candidate(PIN);m=json.loads(encoded)
        self.assertEqual(m['runtime_abi'],'sb52-dev-input-fire-v3')
        self.assertEqual(m['cooperating_cart'],json.loads((ROOT/'docs/fire-profile.json').read_text()))
        self.assertTrue(m['version'].endswith('both-fire-v1.bridge-refactor-v1.candidate1'))
        self.assertEqual(m['authored_capabilities'][-1],'both-fire-v1')
        self.assertEqual(m['capabilities'],[])
        for flag in ('execution_verified','provider_approved','retail_compatibility'):self.assertFalse(m[flag])
        self.assertTrue(all(v is False for k,v in m['timing'].items() if k.endswith('verified')))
        self.assertEqual(m['timing']['default_vbi_full_cycle_target'],4096)
        self.assertEqual(m['image']['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(m['map_sha256'],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertEqual(m['provenance']['allocation_sha256'],hashlib.sha256((ROOT/'docs/fire-allocation.json').read_bytes()).hexdigest())

    def test_every_source_input_verified_and_old_pin_cli_refuses(self):
        def fake(command,**kwargs):
            name=command[-1].split(':',1)[1]
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch('subprocess.run',side_effect=fake):verify_fire_bridge_checkout(ROOT,PIN)
        for target in (*INPUTS,*EXTRA_INPUTS):
            def changed(command,**kwargs):
                name=command[-1].split(':',1)[1]
                return subprocess.CompletedProcess(command,0,b'changed' if name==target else (ROOT/name).read_bytes())
            with patch('subprocess.run',side_effect=changed),self.assertRaises(AssemblyError):verify_fire_bridge_checkout(ROOT,PIN)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out'
            result=subprocess.run([sys.executable,str(ROOT/'tools/export_fire_bridge_candidate.py'),'--source-revision','a2a7455627a9ea3905464c295562debee2efec7d','--output-dir',str(out)],capture_output=True,timeout=10)
            self.assertEqual(result.returncode,2);self.assertFalse(out.exists())

    def test_fresh_process_reproducibility(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for part in ('a','b'):
                subprocess.run([sys.executable,str(ROOT/'tools/fire_bridge_image.py'),'--output-dir',str(root/part)],check=True,capture_output=True,timeout=10)
            for name in ('fire-bridge.bin','fire-bridge-map.json'):
                self.assertEqual((root/'a'/name).read_bytes(),(root/'b'/name).read_bytes())
