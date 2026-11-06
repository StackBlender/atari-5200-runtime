# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from emitter import AssemblyError
from diagnostic_conditional_image import diagnostic_conditional_image
from export_diagnostic_conditional_candidate import candidate as b2,EXTRA_INPUTS as B2_INPUTS
from export_diagnostic_cold_candidate import EXTRA_INPUTS as B1_INPUTS
from export_ordinary_ram_candidate import EXTRA_INPUTS as B0_INPUTS
from export_timer_candidate import EXTRA_INPUTS as TIMER_INPUTS
from export_candidate import INPUTS
from cart_owned_diagnostic_image import (cart_owned_diagnostic_image,IMAGE_PARENT_REVISION,
    IMAGE_PARENT_SHA256,OWNERSHIP_PARENT_REVISION,OWNERSHIP_PARENT_SHA256,PROFILE)
from export_cart_owned_diagnostic_candidate import candidate,verify_checkout,EXTRA_INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN='1'*40


class CartOwnedDiagnosticTests(unittest.TestCase):
    def test_exact_all2048_parent_bytes_fit_symbols_assets_vectors_timing_preserved(self):
        parent,before=diagnostic_conditional_image();data,mapping=cart_owned_diagnostic_image()
        self.assertEqual(data,parent);self.assertEqual(hashlib.sha256(data).hexdigest(),IMAGE_PARENT_SHA256)
        for key in ('allocations','symbols','used','remaining','metadata_policy','nominal_startup'):
            self.assertEqual(mapping[key],before[key])
        self.assertEqual((len(data),mapping['used'],mapping['remaining']),(2048,1556,492))
        self.assertEqual(data[0x700:0x7fa],b'\xff'*250)
        self.assertEqual(mapping['target'],PROFILE)
        self.assertNotEqual(mapping['ownership_policy'],before['ownership_policy'])
        self.assertEqual(mapping['parent_source_revision'],IMAGE_PARENT_REVISION)
        self.assertEqual(mapping['ownership_parent_source_revision'],OWNERSHIP_PARENT_REVISION)

    def test_rebound_contract_new_hash_and_exact_all_individual_parent_values(self):
        old_bytes=(ROOT/'docs/ordinary-ram-profile.json').read_bytes();old=json.loads(old_bytes)
        new_bytes=(ROOT/'docs/cart-owned-diagnostic-profile.json').read_bytes();new=json.loads(new_bytes)
        self.assertEqual(hashlib.sha256(old_bytes).hexdigest(),OWNERSHIP_PARENT_SHA256)
        expected=copy.deepcopy(old);expected.update(profile=PROFILE,purpose='original-cart-owned-conditional-cold-development')
        self.assertEqual(new,expected);self.assertNotEqual(hashlib.sha256(new_bytes).hexdigest(),OWNERSHIP_PARENT_SHA256)
        self.assertEqual(new['initialization'],old['initialization'])
        self.assertEqual((len(new['initialization']['shadows']),len(new['initialization']['vectors'])),(25,14))
        self.assertEqual(new['ownership']['consumer_ram'],[540,16384]);self.assertEqual(new['ownership']['explicitly_ceded'],[540,544])
        self.assertIsNone(new['ownership']['runtime_input_reservation'])
        self.assertIsNone(new['irq']['required_runtime_keyboard_callback'])
        self.assertIs(new['irq']['mandatory_extra_ram_cart_declaration'],False)
        _,mapping=cart_owned_diagnostic_image()
        self.assertEqual(mapping['public_contract'],new)
        self.assertEqual(mapping['public_contract_sha256'],hashlib.sha256(new_bytes).hexdigest())
        self.assertEqual(mapping['ownership_parent_contract_sha256'],OWNERSHIP_PARENT_SHA256)

    def test_complete_identity_distinguishes_same_image_same_synthetic_source(self):
        data,mapping,text=candidate(PIN);manifest=json.loads(text);report=json.loads(mapping)
        parent,parent_map,parent_text=b2(PIN);before=json.loads(parent_text)
        self.assertEqual(data,parent);self.assertEqual(manifest['source_revision'],before['source_revision'])
        self.assertNotEqual(manifest['profile'],before['profile']);self.assertNotEqual(manifest['version'],before['version'])
        self.assertNotEqual(manifest['map_sha256'],before['map_sha256']);self.assertNotEqual(text,parent_text)
        self.assertEqual(manifest['profile'],PROFILE);self.assertIn('.cart-owned-diagnostic-v1.',manifest['version'])
        self.assertLessEqual(len(manifest['version']),255)
        self.assertEqual(manifest['runtime_abi'],'sb52-dev-cc65-v1');self.assertEqual(manifest['timing'],before['timing'])
        self.assertEqual(manifest['metadata_policy'],before['metadata_policy'])
        self.assertEqual(manifest['public_contract']['profile'],PROFILE)
        self.assertNotEqual(manifest['public_contract']['profile'],'ntsc-four-port-cart-owned-irq-development')
        self.assertNotIn('cooperating_cart',manifest);self.assertNotIn('character_mapping',manifest)
        self.assertEqual(manifest['capabilities'],[])
        for field in ('execution_verified','provider_approved','retail_compatibility'):self.assertIs(manifest[field],False)
        self.assertTrue(all(v is False for k,v in manifest['timing'].items() if k.endswith('verified')))
        self.assertEqual(manifest['timing']['full_cycle_target'],4096)
        self.assertEqual(manifest['provenance']['public_contract_sha256'],report['public_contract_sha256'])
        self.assertNotEqual(manifest['provenance']['public_contract_sha256'],manifest['provenance']['ownership_parent_contract_sha256'])
        self.assertEqual(manifest['provenance']['parent_source_revision'],IMAGE_PARENT_REVISION)
        self.assertEqual(manifest['provenance']['ownership_parent_source_revision'],OWNERSHIP_PARENT_REVISION)
        self.assertEqual(manifest['provenance']['startup_source_sha256'],hashlib.sha256((ROOT/'tools/cart_owned_diagnostic_image.py').read_bytes()).hexdigest())
        self.assertEqual(manifest['map_sha256'],hashlib.sha256(mapping.encode()).hexdigest())
        # Identity fields differ; native reciprocal pre-mutation refusal must
        # still be independently proved, not inferred from these hashes.

    def test_parent_identity_ownership_rebinding_and_typed_values_cannot_drift(self):
        data,mapping=diagnostic_conditional_image();altered=bytearray(data);altered[0]^=1
        with patch('cart_owned_diagnostic_image.diagnostic_conditional_image',return_value=(bytes(altered),mapping)),self.assertRaises(AssemblyError):cart_owned_diagnostic_image()
        for field,value in (('used',1557),('remaining',491),('target','other'),('ownership_policy','already-combined')):
            with patch('cart_owned_diagnostic_image.diagnostic_conditional_image',return_value=(data,{**mapping,field:value})),self.assertRaises(AssemblyError):cart_owned_diagnostic_image()
        old=(ROOT/'docs/ordinary-ram-profile.json').read_bytes();valid=json.loads((ROOT/'docs/cart-owned-diagnostic-profile.json').read_bytes())
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'docs').mkdir();(root/'docs/ordinary-ram-profile.json').write_bytes(old)
            changes=(lambda x:x.update(profile='ntsc-four-port-cart-owned-irq-development'),
                lambda x:x['ownership'].update(consumer_ram=[544,16384]),
                lambda x:x['ownership'].update(runtime_input_reservation=[1536,1568]),
                lambda x:x['initialization']['vectors'][0].update(cold=0xfc86),
                lambda x:x['initialization']['shadows'][0].update(cold=False))
            for change in changes:
                bad=copy.deepcopy(valid);change(bad);(root/'docs/cart-owned-diagnostic-profile.json').write_text(json.dumps(bad))
                with patch('cart_owned_diagnostic_image.ROOT',root),self.assertRaises(AssemblyError):cart_owned_diagnostic_image()
            (root/'docs/cart-owned-diagnostic-profile.json').write_text(json.dumps(valid))
            (root/'docs/ordinary-ram-profile.json').write_bytes(old+b' ')
            with patch('cart_owned_diagnostic_image.ROOT',root),self.assertRaises(AssemblyError):cart_owned_diagnostic_image()

    def test_every_immutable_parent_and_new_source_input_is_bound(self):
        def good(command,**kwargs):
            _,relative=command[-1].split(':',1)
            return subprocess.CompletedProcess(command,0,(ROOT/relative).read_bytes())
        with patch('subprocess.run',side_effect=good):verify_checkout(ROOT,PIN)
        base=(*INPUTS,*TIMER_INPUTS)
        cases=(('ac9b47e50c213b08022e78bdef64662569cd3d29',base),
            (OWNERSHIP_PARENT_REVISION,(*base,*B0_INPUTS,*B1_INPUTS)),
            (IMAGE_PARENT_REVISION,(*base,*B1_INPUTS,*B2_INPUTS)),
            (PIN,(*base,*B0_INPUTS,*B1_INPUTS,*B2_INPUTS,*EXTRA_INPUTS)))
        for revision,names in cases:
            for relative in set(names):
                def changed(command,**kwargs):
                    source,name=command[-1].split(':',1)
                    data=b'changed' if (source,name)==(revision,relative) else (ROOT/name).read_bytes()
                    return subprocess.CompletedProcess(command,0,data)
                with patch('subprocess.run',side_effect=changed),self.assertRaises(AssemblyError):verify_checkout(ROOT,PIN)

    def test_parent_source_reuse_refuses_and_fresh_process_reproduces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for index,revision in enumerate((IMAGE_PARENT_REVISION,OWNERSHIP_PARENT_REVISION)):
                with self.assertRaises(AssemblyError):candidate(revision)
                output=root/str(index)
                result=subprocess.run([sys.executable,str(ROOT/'tools/export_cart_owned_diagnostic_candidate.py'),
                    '--source-revision',revision,'--output-dir',str(output)],capture_output=True,timeout=20)
                self.assertEqual(result.returncode,2);self.assertFalse(output.exists())
            snippet="from export_cart_owned_diagnostic_candidate import candidate;from pathlib import Path;import sys;x,m,d=candidate('1'*40);p=Path(sys.argv[1]);p.mkdir();(p/'image').write_bytes(x);(p/'map').write_text(m);(p/'manifest').write_text(d)"
            for name in ('a','b'):
                subprocess.run([sys.executable,'-c',snippet,str(root/name)],cwd=ROOT/'tools',check=True,capture_output=True,timeout=10)
            for name in ('image','map','manifest'):self.assertEqual((root/'a'/name).read_bytes(),(root/'b'/name).read_bytes())
