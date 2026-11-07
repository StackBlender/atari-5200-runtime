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
from cart_owned_diagnostic_image import cart_owned_diagnostic_image
from export_cart_owned_diagnostic_candidate import candidate as parent_candidate,EXTRA_INPUTS as PARENT_INPUTS
from linear8k_guarded_image import linear8k_guarded_image,PARENT_REVISION,PARENT_IMAGE,PROFILE
from export_linear8k_guarded_candidate import candidate,verify_checkout,EXTRA_INPUTS
from linear8k_probe import original_linear8k_probe,READS
ROOT=Path(__file__).resolve().parents[1]
PIN='1'*40


class Linear8KTests(unittest.TestCase):
    def test_all2048_cpu_bytes_fit_symbols_services_capabilities_unchanged(self):
        before,old=cart_owned_diagnostic_image();data,mapping=linear8k_guarded_image()
        self.assertEqual(data,before);self.assertEqual(hashlib.sha256(data).hexdigest(),PARENT_IMAGE)
        self.assertEqual((len(data),mapping['used'],mapping['remaining']),(2048,1556,492))
        self.assertEqual(data[0x700:0x7fa],b'\xff'*250)
        for key in ('symbols','allocations','metadata_policy','nominal_startup','authored_capabilities','ownership_policy'):
            self.assertEqual(mapping[key],old[key])
        self.assertEqual(mapping['target'],PROFILE)
        self.assertEqual(mapping['mapper'],dict(board='Linear8K',program_size=8192,successful_load_required=True))
        self.assertEqual(mapping['parent_source_revision'],PARENT_REVISION)

    def test_native_gate_data_excludes_openbus_and_both_metadata_aliases(self):
        _,mapping=linear8k_guarded_image();contract=mapping['public_contract'];guard=contract['native_guard_requirement']
        self.assertEqual(guard['allowed_entry_cpu'],[[0x8000,0x9fe8],[0xa000,0xbfe8]])
        self.assertEqual(guard['metadata_alias_cpu'],[[0x9fe8,0xa000],[0xbfe8,0xc000]])
        self.assertEqual(guard['canonical_entry_payload'],[8190,8192])
        self.assertEqual(guard['pre_mutation_routes'],['cold','system-power','state-import'])
        self.assertEqual(guard['entry_rejection_classification'],'pre-power-entry')
        for key in ('actual_handoff_equals_immutable_entry','actual_handoff_in_allowed_entry',
                    'pending_nmi_refusal_retained','cpu_cheat_hook_overlay_negative_required'):
            self.assertIs(guard[key],True)
        self.assertIs(guard['cheats_overlays_live_configuration_supported'],False)
        for key in ('additional_emulated_ram_bytes','additional_stack_bytes','additional_helper_calls','additional_native_payload_fields'):
            self.assertIs(type(guard[key]),int);self.assertEqual(guard[key],0)
        parent=json.loads((ROOT/'docs/cart-owned-diagnostic-profile.json').read_text())
        for key in ('initialization','irq','ownership'):self.assertEqual(contract[key],parent[key])
        # DATA arithmetic only, not a CPU validator or native admission result.
        allowed=lambda n:any(a<=n<b for a,b in guard['allowed_entry_cpu'])
        accepted={0x8000,0x9fe7,0xa000,0xbfe7}
        refused={0x3fff,0x4000,0x7fff,0x9fe8,0x9fff,0xbfe8,0xbfff,0xc000}
        self.assertTrue(all(allowed(n) for n in accepted));self.assertTrue(all(not allowed(n) for n in refused))

    def test_new_complete_identity_and_false_flags_not_cpu_guard_capability(self):
        data,map_text,text=candidate(PIN);m=json.loads(text);report=json.loads(map_text)
        old_data,old_map,old_text=parent_candidate(PIN);old=json.loads(old_text)
        self.assertEqual(data,old_data);self.assertEqual(m['authored_capabilities'],old['authored_capabilities'])
        self.assertNotEqual(text,old_text);self.assertNotEqual(map_text,old_map)
        self.assertNotEqual(m['profile'],old['profile']);self.assertNotEqual(m['version'],old['version'])
        self.assertIn('.linear8k-guarded-v1.',m['version']);self.assertLessEqual(len(m['version']),255)
        self.assertEqual(m['runtime_abi'],old['runtime_abi'])
        self.assertEqual(m['metadata_policy'],old['metadata_policy']);self.assertEqual(m['timing'],old['timing'])
        self.assertEqual(m['capabilities'],[])
        for key in ('execution_verified','provider_approved','retail_compatibility'):self.assertIs(m[key],False)
        self.assertTrue(all(value is False for key,value in m['timing'].items() if key.endswith('verified')))
        self.assertEqual(m['map_sha256'],hashlib.sha256(map_text.encode()).hexdigest())
        self.assertEqual(m['native_guard_requirement'],report['native_guard_requirement'])
        self.assertEqual(m['provenance']['parent_source_revision'],PARENT_REVISION)
        self.assertEqual(m['provenance']['public_contract_sha256'],report['public_contract_sha256'])
        self.assertNotIn('cooperating_cart',m);self.assertNotIn('linear8k-immutable-entry-guard-v1',m['authored_capabilities'])

    def test_parent_bytes_and_typed_guard_ownership_cannot_drift(self):
        data,mapping=cart_owned_diagnostic_image();changed=bytearray(data);changed[0]^=1
        with patch('linear8k_guarded_image.cart_owned_diagnostic_image',return_value=(bytes(changed),mapping)),self.assertRaises(AssemblyError):linear8k_guarded_image()
        for key,value in (('used',1557),('remaining',491),('target','other')):
            with patch('linear8k_guarded_image.cart_owned_diagnostic_image',return_value=(data,{**mapping,key:value})),self.assertRaises(AssemblyError):linear8k_guarded_image()
        original=(ROOT/'docs/cart-owned-diagnostic-profile.json').read_bytes()
        valid=json.loads((ROOT/'docs/linear8k-guarded-profile.json').read_text())
        changes=(lambda x:x['native_guard_requirement'].update(allowed_entry_cpu=[[0x4000,0xbfe8]]),
                 lambda x:x['native_guard_requirement'].update(actual_handoff_equals_immutable_entry=False),
                 lambda x:x['native_guard_requirement'].update(additional_native_payload_fields=False),
                 lambda x:x['mapper'].update(program_size=32768),
                 lambda x:x['initialization']['shadows'][0].update(cold=False),
                 lambda x:x['ownership'].update(runtime_input_reservation=[0x600,0x620]))
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'docs').mkdir();(root/'docs/cart-owned-diagnostic-profile.json').write_bytes(original)
            for change in changes:
                bad=copy.deepcopy(valid);change(bad);(root/'docs/linear8k-guarded-profile.json').write_text(json.dumps(bad))
                with patch('linear8k_guarded_image.ROOT',root),self.assertRaises(AssemblyError):linear8k_guarded_image()
            (root/'docs/linear8k-guarded-profile.json').write_text(json.dumps(valid))
            (root/'docs/cart-owned-diagnostic-profile.json').write_bytes(original+b' ')
            with patch('linear8k_guarded_image.ROOT',root),self.assertRaises(AssemblyError):linear8k_guarded_image()

    def test_recursive_frozen_parent_and_each_new_input_pin_bound(self):
        def good(command,**kwargs):
            _,relative=command[-1].split(':',1)
            return subprocess.CompletedProcess(command,0,(ROOT/relative).read_bytes())
        with patch('subprocess.run',side_effect=good):verify_checkout(ROOT,PIN)
        for revision,names in ((PARENT_REVISION,PARENT_INPUTS),(PIN,(*EXTRA_INPUTS,'tools/emitter.py'))):
            for relative in names:
                def changed(command,**kwargs):
                    source,name=command[-1].split(':',1)
                    content=b'changed' if (source,name)==(revision,relative) else (ROOT/name).read_bytes()
                    return subprocess.CompletedProcess(command,0,content)
                with patch('subprocess.run',side_effect=changed),self.assertRaises(AssemblyError):verify_checkout(ROOT,PIN)

    def test_parent_pin_refusal_and_fresh_process_identity(self):
        for value in (PARENT_REVISION,'89af2dcc1d889585d6c9dde2fa12a3db30ce3045','bad'):
            with self.assertRaises(AssemblyError):candidate(value)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);output=root/'refused'
            result=subprocess.run([sys.executable,str(ROOT/'tools/export_linear8k_guarded_candidate.py'),
                '--source-revision',PARENT_REVISION,'--output-dir',str(output)],capture_output=True,timeout=20)
            self.assertEqual(result.returncode,2);self.assertFalse(output.exists())
            snippet="from export_linear8k_guarded_candidate import candidate;from pathlib import Path;import sys;x,m,d=candidate('1'*40);p=Path(sys.argv[1]);p.mkdir();(p/'image').write_bytes(x);(p/'map').write_text(m);(p/'manifest').write_text(d)"
            for name in ('a','b'):
                subprocess.run([sys.executable,'-B','-c',snippet,str(root/name)],cwd=ROOT/'tools',check=True,capture_output=True,timeout=20)
            for name in ('image','map','manifest'):self.assertEqual((root/'a'/name).read_bytes(),(root/'b'/name).read_bytes())

    def test_original_exact8192_probe_code_alias_markers_and_metadata_copies(self):
        for entry in (0x8000,0xa000):
            for ff in (False,True):
                data,report=original_linear8k_probe(entry,ff)
                self.assertEqual(len(data),8192);self.assertEqual(hashlib.sha256(data).hexdigest(),report['sha256'])
                self.assertEqual(data[:9],bytes((0x8d,0,0x30,0x8e,1,0x30,0x8c,2,0x30)))
                self.assertEqual((data[0x100],data[0x1100],data[0x1fe7]),(0x35,0xa7,0x6d))
                self.assertEqual(data[0x1fe8:0x1ffc],bytes([0x50])*20)
                self.assertEqual(data[-4:-2],bytes((0,255)) if ff else bytes((0x52,0x56)))
                self.assertEqual(data[-2:],entry.to_bytes(2,'little'))
                self.assertEqual(report['metadata_expected'],list(data[0x1fe8:]))
                self.assertIn(bytes((0xbd,0xe8,0x9f,0x9d,0x40,0x30,0xbd,0xe8,0xbf,0x9d,0x60,0x30)),data[:report['code_bytes']])
                self.assertFalse(report['native_execution_verified']);self.assertFalse(report['open_bus_value_assumed'])
                self.assertEqual([r['cpu_address'] for r in report['reads']],list(READS))
                for row in report['reads']:
                    if row['cpu_address']<0x8000:self.assertIsNone(row['expected'])
                    else:self.assertEqual(row['expected'],data[(row['cpu_address']-0x8000)%8192])

    def test_original_probe_refuses_other_layouts_and_cli_reproduces(self):
        for entry,ff in ((0x4000,False),(0x9fe8,False),(0xbfe8,False),(0xa000,1)):
            with self.assertRaises(AssemblyError):original_linear8k_probe(entry,ff)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in ('a','b'):
                subprocess.run([sys.executable,'-B',str(ROOT/'tools/linear8k_probe.py'),
                    '--second-ff','--output-dir',str(root/name)],check=True,capture_output=True,timeout=10)
            for name in ('original-linear8k.bin','original-linear8k.json'):
                self.assertEqual((root/'a'/name).read_bytes(),(root/'b'/name).read_bytes())


if __name__=='__main__':unittest.main()
