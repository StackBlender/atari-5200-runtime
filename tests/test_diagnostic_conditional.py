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
from diagnostic_cold_image import diagnostic_cold_image
from diagnostic_conditional_image import diagnostic_conditional_image,metadata_fragment,PARENT_REVISION,PARENT_SHA256
from export_diagnostic_conditional_candidate import candidate,verify_checkout,EXTRA_INPUTS
from export_diagnostic_cold_candidate import EXTRA_INPUTS as B1_INPUTS
from export_timer_candidate import EXTRA_INPUTS as TIMER_INPUTS
from export_candidate import INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN='1'*40


class DiagnosticConditionalTests(unittest.TestCase):
    def test_only_year_prefix_changes_with_identical_entry_fit_init_and_reserve(self):
        parent,before=diagnostic_cold_image();data,mapping=diagnostic_conditional_image()
        self.assertEqual(hashlib.sha256(parent).hexdigest(),PARENT_SHA256)
        changed=[i for i,(a,b) in enumerate(zip(parent,data)) if a!=b]
        self.assertTrue(changed);self.assertTrue(all(0x580<=i<0x59a for i in changed))
        self.assertEqual(data[:0x580],parent[:0x580]);self.assertEqual(data[0x59a:],parent[0x59a:])
        self.assertEqual((len(data),mapping['used'],mapping['remaining']),(2048,1556,492))
        self.assertEqual(mapping['allocations'],before['allocations'])
        self.assertEqual(data[0x700:0x7fa],b'\xff'*250)
        self.assertEqual(data[0x460:0x463],bytes.fromhex('2080fd'))
        self.assertEqual(mapping['symbols']['cart_handoff'],0xfc6b)
        self.assertEqual(mapping['ownership_policy'],before['ownership_policy']);self.assertNotIn('public_contract',mapping)
        self.assertEqual(hashlib.sha256(data).hexdigest(),'5936e46d08c7991231a52dfb6c1a404a7a0d1ab505a51b2c5e09a569d7ad20e4')

    def test_independent_encodings_and_branch_worksheet_secondFF_skips_first_read(self):
        fragment,symbols=metadata_fragment()
        self.assertEqual(fragment,bytes.fromhex('adfdbf c9ff f013 c950 9026 c95a b022 '
            'adfcbf c950 901b c95a b017 adffbf c940 9010 c9c0 b00c c9bf d007 '
            'adfebf c9e8 b001 60 4c86fc'))
        self.assertEqual(len(fragment),52)
        for offset,target in ((5,26),(9,49),(13,49),(20,49),(24,49),(31,49),(35,49),(39,48),(46,49)):
            self.assertEqual(offset+2+int.from_bytes(fragment[offset+1:offset+2],'little',signed=True),target)
        self.assertEqual(fragment[:3],bytes.fromhex('adfdbf'))
        self.assertEqual(fragment[15:18],bytes.fromhex('adfcbf'))
        self.assertEqual(symbols['conditional_entry_check'],0xfd80+26)
        self.assertTrue(all(address>>8==0xfd for address in symbols.values()))

    def test_exhaustive_declared_year_policy_356_pairs_not_a_CPU_execution(self):
        _,mapping,text=candidate(PIN);policy=json.loads(text)['metadata_policy']
        self.assertEqual(policy['first_year_rule'],'any-byte-if-and-only-if-second-FF-otherwise-numeric')
        self.assertEqual((policy['numeric_year_min'],policy['numeric_year_max'],policy['second_year_alternative']),(80,89,255))
        # Enumerate the declarative admitted set only. No opcode/register/flag/
        # chip execution; independent native tests must exercise all65536pairs.
        allowed={(first,second) for first in range(256) for second in range(256)
            if second==policy['second_year_alternative'] or
            (policy['numeric_year_min']<=first<=policy['numeric_year_max'] and
             policy['numeric_year_min']<=second<=policy['numeric_year_max'])}
        expected={(first,255) for first in range(256)}|{(a,b) for a in range(80,90) for b in range(80,90)}
        self.assertEqual(allowed,expected);self.assertEqual(len(allowed),356)
        self.assertEqual(65536-len(allowed),65180)
        _,old=diagnostic_cold_image();self.assertNotIn('first_year_rule',old['metadata_policy'])
        self.assertEqual(old['metadata_policy']['first_year_min'],80)
        self.assertEqual(json.loads(mapping)['metadata_policy'],policy)
        for first in (0,79,90,255):
            self.assertIn((first,255),allowed)
            for second in (0,79,80,89,90,254):self.assertNotIn((first,second),allowed)

    def test_numeric_and_FF_nominal_worksheets_identity_flags_provenance(self):
        data,mapping,text=candidate(PIN);manifest=json.loads(text);report=json.loads(mapping)
        normal=(4+2+2+2+2+2+2)+(4+2+2+2+2);ff=4+2+3;old=2+22*19-1
        self.assertEqual((normal,ff,old),(28,9,419))
        timing=report['nominal_startup']
        self.assertEqual((timing['numeric_normal_cycles'],timing['numeric_boundary_cycles']),(1148-old+normal,1155-old+normal))
        self.assertEqual((timing['ff_normal_cycles'],timing['ff_boundary_cycles']),(1148-old+ff,1155-old+ff))
        self.assertEqual((timing['ff_normal_instructions'],timing['ff_boundary_instructions']),(422-(177-3),425-(177-3)))
        self.assertEqual(manifest['profile'],'ntsc-four-port-diagnostic-conditional-development')
        self.assertIn('.diagnostic-conditional-v1.',manifest['version'])
        self.assertEqual(manifest['timing']['base_cycles_max'],764)
        self.assertEqual(manifest['timing']['diagnostic_second_ff_base_cycles_max'],745)
        self.assertEqual(manifest['timing']['full_cycle_target'],4096)
        self.assertEqual(manifest['runtime_abi'],'sb52-dev-cc65-v1')
        self.assertNotIn('public_contract',manifest);self.assertNotIn('cooperating_cart',manifest)
        self.assertEqual(manifest['capabilities'],[])
        for key in ('execution_verified','provider_approved','retail_compatibility'):self.assertIs(manifest[key],False)
        self.assertTrue(all(v is False for k,v in manifest['timing'].items() if k.endswith('verified')))
        self.assertEqual(manifest['provenance']['parent_source_revision'],PARENT_REVISION)
        self.assertEqual(manifest['provenance']['parent_image_sha256'],PARENT_SHA256)
        self.assertEqual(manifest['provenance']['startup_source_sha256'],hashlib.sha256((ROOT/'tools/diagnostic_conditional_image.py').read_bytes()).hexdigest())
        self.assertEqual(manifest['image']['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(manifest['map_sha256'],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertIs(manifest['metadata_policy']['historical_bypass'],False)

    def test_parent_shape_identity_and_entry_drift_refuse(self):
        data,mapping=diagnostic_cold_image();changed=bytearray(data);changed[0]^=1
        with patch('diagnostic_conditional_image.diagnostic_cold_image',return_value=(bytes(changed),mapping)),self.assertRaises(AssemblyError):diagnostic_conditional_image()
        for key,value in (('used',1557),('remaining',491),('symbols',{**mapping['symbols'],'validate_metadata':0xfd81})):
            with patch('diagnostic_conditional_image.diagnostic_cold_image',return_value=(data,{**mapping,key:value})),self.assertRaises(AssemblyError):diagnostic_conditional_image()
        fragment,symbols=metadata_fragment();changed=bytearray(fragment);changed[26]^=1
        with patch('diagnostic_conditional_image.metadata_fragment',return_value=(bytes(changed),symbols)),self.assertRaises(AssemblyError):diagnostic_conditional_image()

    def test_every_parent_new_pin_old_pin_refusal_and_fresh_process_equality(self):
        def good(command,**kwargs):
            _,name=command[-1].split(':',1)
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch('subprocess.run',side_effect=good):verify_checkout(ROOT,PIN)
        for revision,names in (('ac9b47e50c213b08022e78bdef64662569cd3d29',(*INPUTS,*TIMER_INPUTS)),
            (PARENT_REVISION,(*INPUTS,*TIMER_INPUTS,*B1_INPUTS)),(PIN,(*INPUTS,*TIMER_INPUTS,*B1_INPUTS,*EXTRA_INPUTS))):
            for name in names:
                def changed(command,**kwargs):
                    source,relative=command[-1].split(':',1)
                    value=b'changed' if (source,relative)==(revision,name) else (ROOT/relative).read_bytes()
                    return subprocess.CompletedProcess(command,0,value)
                with patch('subprocess.run',side_effect=changed),self.assertRaises(AssemblyError):verify_checkout(ROOT,PIN)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);output=root/'refuse'
            result=subprocess.run([sys.executable,str(ROOT/'tools/export_diagnostic_conditional_candidate.py'),
                '--source-revision',PARENT_REVISION,'--output-dir',str(output)],capture_output=True,timeout=20)
            self.assertEqual(result.returncode,2);self.assertFalse(output.exists())
            snippet="from export_diagnostic_conditional_candidate import candidate;from pathlib import Path;import sys;x,m,d=candidate('1'*40);p=Path(sys.argv[1]);p.mkdir();(p/'image').write_bytes(x);(p/'map').write_text(m);(p/'manifest').write_text(d)"
            for name in ('a','b'):
                subprocess.run([sys.executable,'-c',snippet,str(root/name)],cwd=ROOT/'tools',check=True,capture_output=True,timeout=10)
            for name in ('image','map','manifest'):self.assertEqual((root/'a'/name).read_bytes(),(root/'b'/name).read_bytes())

    def test_real_pinned_cli_and_cmake_consumer_properties_order_and_bytes(self):
        pin='89af2dcc1d889585d6c9dde2fa12a3db30ce3045'
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);direct=root/'cli'
            subprocess.run([sys.executable,str(ROOT/'tools/export_diagnostic_conditional_candidate.py'),
                '--source-revision',pin,'--output-dir',str(direct)],check=True,capture_output=True,timeout=30)
            fields=('SB5200_IMAGE_FILE','SB5200_MANIFEST_FILE','SB5200_MAP_FILE','SB5200_SOURCE_REVISION')
            properties='\\n'.join('$<TARGET_PROPERTY:sb5200-diagnostic-conditional-image,'+field+'>' for field in fields)+'\\n'
            (root/'check.py').write_text("from pathlib import Path\nimport sys\nv=Path(sys.argv[1]).read_text().splitlines()\nassert len(v)==4\nassert all(Path(p).is_absolute() and Path(p).is_file() for p in v[:3])\nPath(sys.argv[2]).write_text('verified')\n")
            (root/'CMakeLists.txt').write_text('cmake_minimum_required(VERSION 3.20)\nproject(conditional_consumer LANGUAGES NONE)\n'
                +f'add_subdirectory("{ROOT}" module)\ninclude("{ROOT}/cmake/diagnostic-conditional-candidate.cmake")\n'
                +f'file(GENERATE OUTPUT "${{CMAKE_BINARY_DIR}}/properties" CONTENT "{properties}")\n'
                +'add_custom_command(OUTPUT "${CMAKE_BINARY_DIR}/verified" COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/check.py" "${CMAKE_BINARY_DIR}/properties" "${CMAKE_BINARY_DIR}/verified" DEPENDS sb5200-diagnostic-conditional-image VERBATIM)\n'
                +'add_custom_target(consume ALL DEPENDS "${CMAKE_BINARY_DIR}/verified")\n')
            build=root/'build'
            subprocess.run(['cmake','-S',str(root),'-B',str(build),'-G','Ninja',
                '-DSB5200_DIAGNOSTIC_CONDITIONAL_SOURCE_REVISION='+pin],check=True,capture_output=True,timeout=30)
            subprocess.run(['cmake','--build',str(build),'--target','consume'],check=True,capture_output=True,timeout=30)
            properties=(build/'properties').read_text().splitlines()
            self.assertEqual(len(properties),4);self.assertEqual(properties[3],pin)
            for value,name in zip(properties[:3],('startup.bin','startup-manifest.json','startup-map.json')):
                self.assertTrue(Path(value).is_absolute())
                self.assertEqual(Path(value).read_bytes(),(direct/name).read_bytes())
            self.assertTrue((build/'verified').is_file())
            manifest=json.loads((direct/'startup-manifest.json').read_bytes())
            self.assertEqual(manifest['source_revision'],pin)
            self.assertEqual(manifest['image']['sha256'],'5936e46d08c7991231a52dfb6c1a404a7a0d1ab505a51b2c5e09a569d7ad20e4')
