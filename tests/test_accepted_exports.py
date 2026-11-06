# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from verify_accepted_exports import validate
ROOT=Path(__file__).resolve().parents[1]


class AcceptedExportTests(unittest.TestCase):
    def test_wrong_bindings_flags_and_artifact_bytes_are_not_accepted(self):
        data=bytes(range(256))*8 # synthetic data, not a runtime program
        digest=hashlib.sha256(data).hexdigest();pin='1'*40
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)
            def fixture():
                mapping=dict(source_revision=pin,sha256=digest,symbols={'fixture':0xfc00})
                encoded=json.dumps(mapping).encode()
                manifest=dict(source_revision=pin,image=dict(origin=0xf800,size=2048,sha256=digest),
                    map_sha256=hashlib.sha256(encoded).hexdigest(),symbols=mapping['symbols'],
                    capabilities=[],execution_verified=False,provider_approved=False,
                    retail_compatibility=False,timing={'full_cycles_verified':False})
                (directory/'startup.bin').write_bytes(data)
                (directory/'startup-map.json').write_bytes(encoded)
                (directory/'startup-manifest.json').write_text(json.dumps(manifest))
                return manifest
            fixture();validate(directory,pin,digest)
            for key,value in (
                ('source_revision','2'*40),('capabilities',['not-approved']),
                ('execution_verified',True),('provider_approved',True),
                ('retail_compatibility',True),('timing',{'full_cycles_verified':True}),
                ('map_sha256','0'*64),('symbols',{'different':0xfc00}),
                ('image',dict(origin=0xf900,size=2048,sha256=digest)),
            ):
                with self.subTest(key=key):
                    manifest=fixture();manifest[key]=value
                    (directory/'startup-manifest.json').write_text(json.dumps(manifest))
                    with self.assertRaises(ValueError):validate(directory,pin,digest)
            fixture();(directory/'startup.bin').write_bytes(data[:-1]+b'\0')
            with self.assertRaises(ValueError):validate(directory,pin,digest)
            fixture();(directory/'startup-map.json').write_text('{}')
            with self.assertRaises(KeyError):validate(directory,pin,digest)

    def test_all_eleven_real_pins_and_parent_consumer_in_fresh_process(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/verify_accepted_exports.py'),'--cmake'],
            capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('Eleven immutable development exports PASS',result.stdout)
        self.assertIn('CMake dependency/four properties/triple byte equality PASS',result.stdout)
