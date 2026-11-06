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
from opaque_title_image import opaque_title_image
from character_bank_image import character_bank_image,pack_geometry,PARENT_REVISION,PARENT_SHA256
from export_character_bank_candidate import candidate,verify_character_bank_checkout,EXTRA_INPUTS
from export_candidate import INPUTS
from export_fire_bridge_candidate import EXTRA_INPUTS as BRIDGE_INPUTS
from export_opaque_title_candidate import EXTRA_INPUTS as OPAQUE_INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN='1'*40
DIGITS=bytes.fromhex('3c42420042423c00 0002020002020000 3c02023c40403c00 '
    '3c02023c02023c00 0042423c02020000 3c40403c02023c00 '
    '3c40403c42423c00 3c02020002020000 3c42423c42423c00 3c42423c02023c00')


class CharacterBankTests(unittest.TestCase):
    def test_independent_all_geometry_packing_and_original_digit_cells(self):
        # Own normative DATA -> independently packed expected cells, not the
        # bank/emitter output as its own expected-pixel source.
        document=json.loads((ROOT/'assets/printable-geometry.json').read_bytes())
        cells=document['geometry']['glyphs']
        original=b''.join(bytes(int(row.replace('.','0').replace('#','1'),2)
            for row in cells[str(label)]) for label in range(32,127))
        self.assertEqual(len(original),760)
        self.assertEqual(hashlib.sha256(original).hexdigest(),'674bd8776ac83d517654b3d6ca2720e5b6d69f5e084c2bd35052c19c074f547a')
        data,report=character_bank_image()
        for index in range(64):
            expected=DIGITS[(index-16)*8:(index-15)*8] if 16<=index<=25 else original[index*8:(index+1)*8]
            self.assertEqual(data[index*8:(index+1)*8],expected,index)
        self.assertEqual(data[0x80:0xd0],DIGITS)
        self.assertEqual(data[0x280:0x2d0],DIGITS)
        # Deliberately chosen A and underscore edge pixels, independent constants.
        self.assertEqual(data[33*8:34*8],bytes.fromhex('102844447c444400'))
        self.assertEqual(data[63*8:64*8],bytes.fromhex('0000000000007c00'))
        self.assertEqual(data[:8],bytes(8))
        self.assertEqual(report['font_geometry']['sha256'],hashlib.sha256(original).hexdigest())

    def test_exact_parent_high_bank_code_symbols_budget_and_reserve_preserved(self):
        parent,before=opaque_title_image();data,report=character_bank_image()
        self.assertEqual(hashlib.sha256(parent).hexdigest(),PARENT_SHA256)
        self.assertEqual(hashlib.sha256(data).hexdigest(),'c7caa810132d16ae55b75077e6d5138b5ad388a0094cedaee1eee091cb4a6598')
        changes=[i for i,(a,b) in enumerate(zip(parent,data)) if a!=b]
        self.assertTrue(changes);self.assertLess(max(changes),512)
        self.assertEqual(data[512:],parent[512:])
        self.assertEqual(data[0x7a0:0x7fa],b'\xff'*90)
        self.assertEqual((len(data),report['used'],report['remaining']),(2048,1895,153))
        for key in ('symbols','allocations','metadata_policy','nominal_startup'):
            self.assertEqual(report[key],before[key])
        self.assertEqual(report['parent_source_revision'],PARENT_REVISION)

    def test_manifest_identity_original_policy_provenance_and_no_approval(self):
        data,mapping,text=candidate(PIN);manifest=json.loads(text);report=json.loads(mapping)
        self.assertIn('.original64-v1.candidate1',manifest['version'])
        self.assertLessEqual(len(manifest['version']),255)
        self.assertEqual(manifest['runtime_abi'],'sb52-dev-input-fire-v3')
        self.assertEqual(manifest['cooperating_cart'],json.loads((ROOT/'docs/fire-profile.json').read_text()))
        self.assertEqual(manifest['profile'],'ntsc-four-port-cooperating-input-fire-development')
        self.assertEqual(manifest['capabilities'],[])
        for key in ('execution_verified','provider_approved','retail_compatibility'):self.assertIs(manifest[key],False)
        self.assertTrue(all(v is False for k,v in manifest['timing'].items() if k.endswith('verified')))
        self.assertEqual(manifest['timing']['base_cycles_max'],1098)
        self.assertEqual(manifest['timing']['full_cycle_target'],4096)
        policy=manifest['character_mapping']
        self.assertEqual((policy['label_first'],policy['label_last'],policy['index_bias'],policy['glyph_count']),(32,95,-32,64))
        self.assertIs(policy['historical_encoding'],False)
        self.assertIs(policy['remaining_ascii_unbound'],True)
        self.assertEqual((policy['retained_digit_indices'],policy['legacy_digit_indices']),([16,25],[80,89]))
        self.assertEqual(report['character_mapping'],policy)
        self.assertEqual(manifest['font_geometry'],report['font_geometry'])
        self.assertEqual(manifest['provenance']['parent_source_revision'],PARENT_REVISION)
        self.assertEqual(manifest['provenance']['startup_source_sha256'],hashlib.sha256((ROOT/'tools/character_bank_image.py').read_bytes()).hexdigest())
        self.assertEqual(manifest['font_geometry']['source_data_sha256'],hashlib.sha256((ROOT/'assets/printable-geometry.json').read_bytes()).hexdigest())
        self.assertEqual(manifest['image']['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(manifest['map_sha256'],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertEqual(manifest['authored_capabilities'][-1],'original64-font-v1')

    def test_invalid_geometry_repertoire_dimensions_pixels_and_provenance_refuse(self):
        valid=json.loads((ROOT/'assets/printable-geometry.json').read_bytes())
        changes=(lambda x:x.update(source_revision='2'*40),lambda x:x.update(sha256='0'*64),
            lambda x:x.update(license='unknown'),lambda x:x['geometry'].update(bit_order='LSB-left'),
            lambda x:x['geometry']['glyphs'].pop('32'),
            lambda x:x['geometry']['glyphs'].update({'127':['........']*8}),
            lambda x:x['geometry']['glyphs'].update({'32':['........']*7}),
            lambda x:x['geometry']['glyphs'].update({'32':['.......']*8}),
            lambda x:x['geometry']['glyphs'].update({'32':['.......X']*8}),
            lambda x:x['geometry']['glyphs'].update({'32':['.......#']*8}),
            lambda x:x['geometry']['glyphs'].update({'32':None}),
            lambda x:x['geometry'].update(glyphs=[]))
        for change in changes:
            altered=copy.deepcopy(valid);change(altered)
            with self.assertRaises(AssemblyError):pack_geometry(altered)

    def test_parent_identity_and_fit_drift_refuse_before_composition(self):
        data,mapping=opaque_title_image();changed=bytearray(data);changed[1024]^=1
        with patch('character_bank_image.opaque_title_image',return_value=(bytes(changed),mapping)),self.assertRaises(AssemblyError):character_bank_image()
        for field,value in (('used',1905),('remaining',152)):
            with patch('character_bank_image.opaque_title_image',return_value=(data,{**mapping,field:value})),self.assertRaises(AssemblyError):character_bank_image()

    def test_every_old_and_new_generation_input_pinned_and_old_pin_refuses(self):
        def normal(command,**kwargs):
            _,name=command[-1].split(':',1)
            return subprocess.CompletedProcess(command,0,(ROOT/name).read_bytes())
        with patch('subprocess.run',side_effect=normal):verify_character_bank_checkout(ROOT,PIN)
        for revision,names in ((PARENT_REVISION,(*INPUTS,*BRIDGE_INPUTS,*OPAQUE_INPUTS)),
                               (PIN,(*INPUTS,*BRIDGE_INPUTS,*OPAQUE_INPUTS,*EXTRA_INPUTS))):
            for relative in names:
                def changed(command,**kwargs):
                    source,name=command[-1].split(':',1)
                    data=b'changed' if (source,name)==(revision,relative) else (ROOT/name).read_bytes()
                    return subprocess.CompletedProcess(command,0,data)
                with patch('subprocess.run',side_effect=changed),self.assertRaises(AssemblyError):verify_character_bank_checkout(ROOT,PIN)
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'out'
            process=subprocess.run([sys.executable,str(ROOT/'tools/export_character_bank_candidate.py'),
                '--source-revision',PARENT_REVISION,'--output-dir',str(output)],capture_output=True,timeout=10)
            self.assertEqual(process.returncode,2);self.assertFalse(output.exists())

    def test_fresh_process_composition_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('a','b'):
                subprocess.run([sys.executable,str(ROOT/'tools/character_bank_image.py'),'--output-dir',str(root/name)],check=True,capture_output=True,timeout=10)
            for name in ('character-bank.bin','character-bank-map.json'):
                self.assertEqual((root/'a'/name).read_bytes(),(root/'b'/name).read_bytes())

    def test_real_pinned_cli_and_cmake_consumer_properties_order_and_bytes(self):
        pin='46b485ddff275af0f66b29b5a2388f8668cc9e11'
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);direct=root/'cli'
            subprocess.run([sys.executable,str(ROOT/'tools/export_character_bank_candidate.py'),
                '--source-revision',pin,'--output-dir',str(direct)],check=True,capture_output=True,timeout=30)
            fields=('SB5200_IMAGE_FILE','SB5200_MANIFEST_FILE','SB5200_MAP_FILE','SB5200_SOURCE_REVISION')
            properties='\\n'.join('$<TARGET_PROPERTY:sb5200-character-bank-image,'+field+'>' for field in fields)+'\\n'
            (root/'check.py').write_text("from pathlib import Path\nimport sys\nv=Path(sys.argv[1]).read_text().splitlines()\nassert len(v)==4\nassert all(Path(p).is_absolute() and Path(p).is_file() for p in v[:3])\nPath(sys.argv[2]).write_text('verified')\n")
            (root/'CMakeLists.txt').write_text('cmake_minimum_required(VERSION 3.20)\nproject(character_bank_consumer LANGUAGES NONE)\n'
                +f'add_subdirectory("{ROOT}" module)\ninclude("{ROOT}/cmake/character-bank-candidate.cmake")\n'
                +f'file(GENERATE OUTPUT "${{CMAKE_BINARY_DIR}}/properties" CONTENT "{properties}")\n'
                +'add_custom_command(OUTPUT "${CMAKE_BINARY_DIR}/verified" COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/check.py" "${CMAKE_BINARY_DIR}/properties" "${CMAKE_BINARY_DIR}/verified" DEPENDS sb5200-character-bank-image VERBATIM)\n'
                +'add_custom_target(consume ALL DEPENDS "${CMAKE_BINARY_DIR}/verified")\n')
            build=root/'build'
            subprocess.run(['cmake','-S',str(root),'-B',str(build),'-G','Ninja',
                '-DSB5200_CHARACTER_BANK_SOURCE_REVISION='+pin],check=True,capture_output=True,timeout=30)
            subprocess.run(['cmake','--build',str(build),'--target','consume'],check=True,capture_output=True,timeout=30)
            properties=(build/'properties').read_text().splitlines()
            self.assertEqual(len(properties),4);self.assertEqual(properties[3],pin)
            for value,name in zip(properties[:3],('startup.bin','startup-manifest.json','startup-map.json')):
                self.assertTrue(Path(value).is_absolute())
                self.assertEqual(Path(value).read_bytes(),(direct/name).read_bytes())
            self.assertTrue((build/'verified').is_file())
            manifest=json.loads((direct/'startup-manifest.json').read_bytes())
            self.assertEqual(manifest['source_revision'],pin)
            self.assertEqual(manifest['image']['sha256'],'c7caa810132d16ae55b75077e6d5138b5ad388a0094cedaee1eee091cb4a6598')
