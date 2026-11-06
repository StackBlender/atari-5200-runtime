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
from emitter import AssemblyError
from fire_bridge_image import fire_bridge_image
from opaque_title_image import opaque_title_image, PARENT_SHA256, PARENT_REVISION
from export_opaque_title_candidate import candidate,verify_opaque_title_checkout,EXTRA_INPUTS
from export_candidate import INPUTS
from export_fire_bridge_candidate import EXTRA_INPUTS as PARENT_INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN='1'*40


class OpaqueTitleTests(unittest.TestCase):
    def test_exact_only_byte_change_and_unchanged_fit_font_reserve_vectors(self):
        parent,before=fire_bridge_image();data,report=opaque_title_image()
        self.assertEqual(hashlib.sha256(parent).hexdigest(),PARENT_SHA256)
        self.assertEqual([i for i,(old,new) in enumerate(zip(parent,data)) if old!=new],[0x6b1])
        self.assertEqual((parent[0x6b1],data[0x6b1]),(0,20))
        self.assertEqual(data[0x6b0:0x6b5],bytes.fromhex('a214bde8bf'))
        self.assertEqual((len(data),report['used'],report['remaining']),(2048,1895,153))
        self.assertEqual(report['allocations'],before['allocations'])
        self.assertEqual(report['symbols'],before['symbols'])
        self.assertEqual(data[:1024],parent[:1024])
        self.assertEqual(data[0x7a0:0x7fa],b'\xff'*90)
        self.assertEqual(data[-6:],parent[-6:])
        self.assertEqual(report['parent_source_revision'],PARENT_REVISION)

    def test_independent_nominal_metadata_timing_worksheet(self):
        _,report=opaque_title_image();timing=report['nominal_startup']
        # LDX2 + n*(LDA4/CMP2/BCC2/CMP2/BCS2/INX2/CPX2/BNE3),
        # with the final not-taken branch saving one. No page crossing/stalls.
        old=2+22*(4+2+2+2+2+2+2+3)-1
        new=2+2*(4+2+2+2+2+2+2+3)-1
        self.assertEqual((old,new,old-new),(419,39,380))
        self.assertEqual(timing,dict(normal_cycles=1471-380,boundary_cycles=1478-380,
            skipped_title_iterations=20,cycles_saved=380,helper_cycles=39,instructions_saved=20*8))

    def test_new_manifest_identity_policy_provenance_false_flags_and_same_abi(self):
        data,mapping,encoded=candidate(PIN);manifest=json.loads(encoded);report=json.loads(mapping)
        self.assertTrue(manifest['version'].startswith('cold-start-opaque-title-v1.'))
        self.assertEqual(manifest['runtime_abi'],'sb52-dev-input-fire-v3')
        self.assertEqual(manifest['profile'],'ntsc-four-port-cooperating-input-fire-development')
        self.assertEqual(manifest['cooperating_cart'],json.loads((ROOT/'docs/fire-profile.json').read_text()))
        self.assertEqual(manifest['metadata_policy'],dict(title_bytes=20,title='opaque',year_bytes=2,year_min=80,year_max=89,diagnostic_bypass=False))
        self.assertEqual(manifest['metadata_policy'],report['metadata_policy'])
        self.assertEqual(manifest['authored_capabilities'][-1],'opaque-title-v1')
        self.assertEqual(manifest['capabilities'],[])
        for flag in ('execution_verified','provider_approved','retail_compatibility'):self.assertIs(manifest[flag],False)
        self.assertTrue(all(v is False for k,v in manifest['timing'].items() if k.endswith('verified')))
        self.assertEqual(manifest['timing']['base_cycles_max'],1098)
        self.assertEqual(manifest['timing']['full_cycle_target'],4096)
        self.assertEqual(manifest['image']['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(manifest['map_sha256'],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertEqual(manifest['provenance']['startup_source_sha256'],hashlib.sha256((ROOT/'tools/opaque_title_image.py').read_bytes()).hexdigest())
        self.assertEqual(manifest['provenance']['parent_source_revision'],PARENT_REVISION)

    def test_parent_drift_symbol_or_budget_mismatch_stops(self):
        data,mapping=fire_bridge_image();changed=bytearray(data);changed[0]^=1
        with patch('opaque_title_image.fire_bridge_image',return_value=(bytes(changed),mapping)),self.assertRaises(AssemblyError):opaque_title_image()
        for field,value in [('used',1905),('symbols',{**mapping['symbols'],'validate_metadata':0xfeaf})]:
            with patch('opaque_title_image.fire_bridge_image',return_value=(data,{**mapping,field:value})),self.assertRaises(AssemblyError):opaque_title_image()

    def test_every_inherited_and_new_input_verified_at_both_generations(self):
        def result(command,**kwargs):
            name=command[-1].split(':',1)[1]
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch('subprocess.run',side_effect=result):verify_opaque_title_checkout(ROOT,PIN)
        for revision,names in ((PARENT_REVISION,(*INPUTS,*PARENT_INPUTS)),(PIN,(*INPUTS,*PARENT_INPUTS,*EXTRA_INPUTS))):
            for relative in names:
                def changed(command,**kwargs):
                    source,name=command[-1].split(':',1)
                    value=b'changed' if (source,name)==(revision,relative) else (ROOT/name).read_bytes()
                    return subprocess.CompletedProcess(command,0,value)
                with patch('subprocess.run',side_effect=changed),self.assertRaises(AssemblyError):verify_opaque_title_checkout(ROOT,PIN)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out'
            process=subprocess.run([sys.executable,str(ROOT/'tools/export_opaque_title_candidate.py'),'--source-revision',PARENT_REVISION,'--output-dir',str(out)],capture_output=True,timeout=10)
            self.assertEqual(process.returncode,2);self.assertFalse(out.exists())

    def test_fresh_process_artifacts_are_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('a','b'):
                subprocess.run([sys.executable,str(ROOT/'tools/opaque_title_image.py'),'--output-dir',str(root/name)],check=True,capture_output=True,timeout=10)
            for name in ('opaque-title.bin','opaque-title-map.json'):
                self.assertEqual((root/'a'/name).read_bytes(),(root/'b'/name).read_bytes())
