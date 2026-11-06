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
from timer_dispatch_image import timer_dispatch_image
from timer_experiment import PARENT_REVISION,PARENT_SHA256
from ordinary_ram_image import ordinary_ram_image
from diagnostic_cold_image import diagnostic_cold_image,metadata_fragment
from export_ordinary_ram_candidate import candidate as b0,verify_checkout as verify0,EXTRA_INPUTS as INPUTS0
from export_diagnostic_cold_candidate import candidate as b1,verify_checkout as verify1,EXTRA_INPUTS as INPUTS1
from export_candidate import INPUTS
from export_timer_candidate import EXTRA_INPUTS as TIMER_INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN='1'*40


class TimerExperimentTests(unittest.TestCase):
    def test_b0_identical_rom_and_complete_individual_initialization_ownership(self):
        parent,before=timer_dispatch_image();data,mapping=ordinary_ram_image()
        self.assertEqual(data,parent);self.assertEqual(hashlib.sha256(data).hexdigest(),PARENT_SHA256)
        for field in ('allocations','symbols','used','remaining'):self.assertEqual(mapping[field],before[field])
        contract=mapping['public_contract'];ownership=contract['ownership']
        self.assertEqual(ownership['runtime_shadows'],[0,25]);self.assertEqual(ownership['runtime_vectors'],[512,540])
        self.assertEqual(ownership['consumer_zero_page'],[25,256]);self.assertEqual(ownership['consumer_ram'],[540,16384])
        self.assertEqual(ownership['explicitly_ceded'],[540,544]);self.assertIsNone(ownership['runtime_input_reservation'])
        self.assertEqual(ownership['additional_runtime_ram_bytes'],0)
        names=['pokmsk','rtclok_low','rtclok_high','critic','atract','sdlst_low','sdlst_high','sdmctl',
            'pcolr0','pcolr1','pcolr2','pcolr3','color0','color1','color2','color3','color4',
            'paddl0','paddl1','paddl2','paddl3','paddl4','paddl5','paddl6','paddl7']
        self.assertEqual(contract['initialization']['shadows'],[dict(name=n,address=i,cold=0) for i,n in enumerate(names)])
        vectors=['vinter','vvblki','vvblkd','vdslst','vkeybd','vkeypd','vbrkky','vbreak','vserin','vseror','vseroc','vtimr1','vtimr2','vtimr4']
        self.assertEqual(contract['initialization']['vectors'],[dict(name=n,address=512+2*i,
            cold={0:0xfe00,1:0xfca0,2:0xfcb0}.get(i,0xfc86)) for i,n in enumerate(vectors)])
        self.assertEqual(contract['irq']['default_timer_supported_mask'],7)
        self.assertIsNone(contract['irq']['required_runtime_keyboard_callback'])

    def test_b1_only_new52byte_validator_and_two_call_operand_bytes(self):
        parent,before=timer_dispatch_image();data,mapping=diagnostic_cold_image()
        allowed={0x461,0x462,*range(0x580,0x5b4)}
        self.assertTrue(all(i in allowed for i,(a,b) in enumerate(zip(parent,data)) if a!=b))
        self.assertEqual(data[:0x461],parent[:0x461]);self.assertEqual(data[0x463:0x580],parent[0x463:0x580])
        self.assertEqual(data[0x5b4:],parent[0x5b4:]);self.assertEqual(data[0x460:0x463],bytes.fromhex('2080fd'))
        self.assertEqual((len(data),mapping['used'],mapping['remaining']),(2048,1556,492))
        self.assertEqual(sum(a['used'] for a in mapping['allocations']),1556)
        for region in mapping['allocations']:
            previous=next(a for a in before['allocations'] if a['name']==region['name'])
            self.assertEqual(region['used']-previous['used'],52 if region['name']=='input' else 0)
        self.assertEqual(data[0x700:0x7fa],b'\xff'*250)
        self.assertEqual(mapping['symbols']['cart_handoff'],0xfc6b)
        self.assertEqual(mapping['symbols']['validate_metadata'],0xfd80)
        self.assertEqual(mapping['symbols']['legacy_validate_metadata'],0xfeb0)
        self.assertNotIn('public_contract',mapping)

    def test_b1_independent_encodings_branch_targets_and_timing_worksheet(self):
        fragment,symbols=metadata_fragment()
        # Worksheet offsets first-year0/second11/entry26/RTS48/fault49.
        expected=bytes.fromhex('adfcbf c950 902a c95a b026 adfdbf c9ff f008 '
            'c950 901b c95a b017 adffbf c940 9010 c9c0 b00c c9bf d007 '
            'adfebf c9e8 b001 60 4c86fc')
        self.assertEqual(fragment,expected);self.assertEqual(len(fragment),52)
        for offset,target in ((5,49),(9,49),(16,26),(20,49),(24,49),(31,49),(35,49),(39,48),(46,49)):
            displacement=int.from_bytes(fragment[offset+1:offset+2],'little',signed=True)
            self.assertEqual(offset+2+displacement,target)
        self.assertEqual(symbols['diagnostic_entry_check'],0xfd80+26)
        # First numeric always precedes second-yearFF branch; no title read.
        self.assertEqual(fragment[:3],bytes.fromhex('adfcbf'));self.assertEqual(fragment[11:14],bytes.fromhex('adfdbf'))
        old=2+22*19-1;first=4+2+2+2+2;numeric=first+4+2+2+2+2+2+2;ff=first+4+2+3
        self.assertEqual((old,numeric,ff),(419,28,21))
        _,mapping=diagnostic_cold_image();timing=mapping['nominal_startup']
        self.assertEqual((timing['numeric_normal_cycles'],timing['numeric_boundary_cycles']),
            (1148-(old-numeric),1155-(old-numeric)))
        self.assertEqual((timing['ff_normal_cycles'],timing['ff_boundary_cycles']),
            (1148-(old-ff),1155-(old-ff)))
        self.assertEqual((timing['numeric_normal_instructions'],timing['ff_normal_instructions']),
            (422-(177-12),422-(177-8)))

    def test_separate_manifests_versions_hashes_false_flags_and_provenance(self):
        manifests=[]
        for build,profile,script in ((b0,'ntsc-four-port-cart-owned-irq-development','ordinary_ram'),
                                    (b1,'ntsc-four-port-diagnostic-cold-development','diagnostic_cold')):
            data,mapping,text=build(PIN);manifest=json.loads(text);report=json.loads(mapping);manifests.append(manifest)
            self.assertEqual(manifest['profile'],profile);self.assertIn(script.replace('_','-')+'-v1',manifest['version'])
            self.assertEqual(manifest['runtime_abi'],'sb52-dev-cc65-v1');self.assertEqual(manifest['capabilities'],[])
            self.assertNotIn('cooperating_cart',manifest);self.assertNotIn('character_mapping',manifest)
            for flag in ('execution_verified','provider_approved','retail_compatibility'):self.assertIs(manifest[flag],False)
            self.assertTrue(all(v is False for k,v in manifest['timing'].items() if k.endswith('verified')))
            self.assertEqual(manifest['timing']['full_cycle_target'],4096)
            self.assertEqual(manifest['map_sha256'],hashlib.sha256(mapping.encode()).hexdigest())
            self.assertEqual(manifest['image']['sha256'],hashlib.sha256(data).hexdigest())
            self.assertEqual(manifest['provenance']['parent_source_revision'],PARENT_REVISION)
            self.assertEqual(manifest['provenance']['startup_source_sha256'],hashlib.sha256((ROOT/f'tools/{script}_image.py').read_bytes()).hexdigest())
            self.assertEqual(manifest['symbols'],report['symbols'])
        self.assertIn('public_contract',manifests[0]);self.assertNotIn('metadata_policy',manifests[0])
        self.assertNotIn('public_contract',manifests[1]);self.assertIn('through021F',manifests[1]['ownership_policy'])
        self.assertEqual(manifests[0]['timing']['base_cycles_max'],1155)
        self.assertEqual(manifests[1]['timing']['base_cycles_max'],764)
        self.assertEqual(manifests[1]['timing']['diagnostic_second_ff_base_cycles_max'],757)
        self.assertEqual(manifests[1]['metadata_policy']['first_year_max'],89)
        self.assertEqual(manifests[1]['metadata_policy']['second_year_alternative'],255)
        self.assertIs(manifests[1]['metadata_policy']['historical_bypass'],False)

    def test_parent_and_reviewed_contract_drift_fail(self):
        data,mapping=timer_dispatch_image();altered=bytearray(data);altered[0]^=1
        for build in (ordinary_ram_image,diagnostic_cold_image):
            with patch('timer_experiment.timer_dispatch_image',return_value=(bytes(altered),mapping)),self.assertRaises(AssemblyError):build()
            with patch('timer_experiment.timer_dispatch_image',return_value=(data,{**mapping,'used':1505})),self.assertRaises(AssemblyError):build()
        valid=json.loads((ROOT/'docs/ordinary-ram-profile.json').read_bytes())
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'docs').mkdir()
            for group,key,value in (('ownership','consumer_ram',[544,16384]),('ownership','runtime_input_reservation',[1536,1568]),
                                    ('irq','default_timer_supported_mask',71)):
                bad=copy.deepcopy(valid);bad[group][key]=value
                (root/'docs/ordinary-ram-profile.json').write_text(json.dumps(bad))
                with patch('ordinary_ram_image.ROOT',root),self.assertRaises(AssemblyError):ordinary_ram_image()
            bad=copy.deepcopy(valid);bad['initialization']['shadows'][0]['cold']=1
            (root/'docs/ordinary-ram-profile.json').write_text(json.dumps(bad))
            with patch('ordinary_ram_image.ROOT',root),self.assertRaises(AssemblyError):ordinary_ram_image()

    def test_every_inherited_and_new_input_pinned_against_parent_and_source(self):
        def good(command,**kwargs):
            _,relative=command[-1].split(':',1)
            return subprocess.CompletedProcess(command,0,(ROOT/relative).read_bytes())
        for verify,extra in ((verify0,INPUTS0),(verify1,INPUTS1)):
            with patch('subprocess.run',side_effect=good):verify(ROOT,PIN)
            for revision,names in ((PARENT_REVISION,(*INPUTS,*TIMER_INPUTS)),(PIN,(*INPUTS,*TIMER_INPUTS,*extra))):
                for name in names:
                    def changed(command,**kwargs):
                        source,relative=command[-1].split(':',1)
                        data=b'changed' if (source,relative)==(revision,name) else (ROOT/relative).read_bytes()
                        return subprocess.CompletedProcess(command,0,data)
                    with patch('subprocess.run',side_effect=changed),self.assertRaises(AssemblyError):verify(ROOT,PIN)

    def test_old_pin_refuses_before_output_and_fresh_process_reproduces_each(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('ordinary_ram','diagnostic_cold'):
                script=ROOT/f'tools/export_{name}_candidate.py'
                out=root/name
                result=subprocess.run([sys.executable,str(script),'--source-revision',PARENT_REVISION,'--output-dir',str(out)],capture_output=True,timeout=20)
                self.assertEqual(result.returncode,2);self.assertFalse(out.exists())
                snippet=f"from export_{name}_candidate import candidate;from pathlib import Path;import sys;x,m,d=candidate('1'*40);r=Path(sys.argv[1]);r.mkdir();(r/'image').write_bytes(x);(r/'map').write_text(m);(r/'manifest').write_text(d)"
                for suffix in ('a','b'):
                    subprocess.run([sys.executable,'-c',snippet,str(root/(name+suffix))],cwd=ROOT/'tools',capture_output=True,check=True,timeout=10)
                for field in ('image','map','manifest'):
                    self.assertEqual((root/(name+'a')/field).read_bytes(),(root/(name+'b')/field).read_bytes())
