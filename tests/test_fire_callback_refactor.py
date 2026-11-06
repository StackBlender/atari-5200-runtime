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
from fire_callback_refactor import refactor_fragment
from fire_service_fragment import fire_fragment
from fire_image import fire_image
ROOT=Path(__file__).resolve().parents[1]


class CallbackRefactorTests(unittest.TestCase):
    def test_independent_bottom_encoding_shared_setup_uses_one_call(self):
        data,report=refactor_fragment()
        expected=bytes.fromhex(
            'ad0006 c901 d040 a200 8e1906 bd10c0 49ff 2901 8d1b06 '
            'bd1006 2902 0d1b06 8d1b06 bd1006 cd1b06 f011 '
            '8d1a06 ad1b06 9d1006 ad1406 f003 2088f8 '
            'ae1906 e8 e004 d0c7 a901 8d1406 4c1afd')
        self.assertEqual(data[:74],expected)
        self.assertEqual(report['offsets']['bottom_next'],58)
        self.assertEqual(report['offsets']['bottom_skip'],71)

    def test_independent_top_encoding_and_argument_bridge(self):
        data,report=refactor_fragment()
        expected=bytes.fromhex(
            'ae0206 ad0fe8 49ff 2908 4a 4a 8d1b06 bd1006 2901 0d1b06 8d1b06 '
            'bd1006 cd1b06 f011 8d1a06 ad1b06 9d1006 bd1506 f003 '
            '2088f8 ae0206 a901 9d1506 4c59fd '
            'ac1b06 8a ae1a06 6c0802')
        self.assertEqual(data[74:],expected)
        self.assertEqual(report['offsets']['top_baseline'],125)
        self.assertEqual(report['offsets']['fire_callback_bridge'],136)
        # Setup is moved into the existing tail bridge, not another JSR/RTS.
        self.assertEqual(data[136:],bytes.fromhex('ac1b06 8a ae1a06 6c0802'))
        self.assertEqual(report['additional_bridge_stack_bytes'],0)
        self.assertEqual(report['setup_plus_call_bridge_nominal_cycles'],4+2+4+6+5)

    def test_measured_size_projection_and_no_approval_inference(self):
        data,report=refactor_fragment()
        self.assertEqual(len(data),146)
        self.assertEqual(report['code_bytes_saved'],7)
        self.assertEqual(report['projected_cumulative_written'],1895)
        self.assertEqual(report['projected_extra_above_timer'],391)
        self.assertEqual(400-report['projected_extra_above_timer'],9)
        self.assertEqual(report['projected_nonmargin_free'],63)
        self.assertEqual(report['accepted_nonmargin_free'],56)
        self.assertEqual(report['sha256'],hashlib.sha256(data).hexdigest())
        self.assertIsNone(report['runtime_abi'])
        self.assertEqual(report['capabilities'],[])
        for flag in ('execution_verified','provider_approved','cumulative_allocation_approved','refactor_review_accepted'):
            self.assertFalse(report[flag])

    def test_accepted_image_and_original_fragment_unchanged(self):
        old,_=fire_fragment();image,_=fire_image()
        self.assertEqual(hashlib.sha256(old).hexdigest(),'9ea001fd9af9eb2d95f19cd9f219760b6d4deb270bb30eb1ae480453c44d5cb1')
        self.assertEqual(hashlib.sha256(image).hexdigest(),'e937064b0d1fe33d0f75cfe4dba89bcbec953adc215f83ed51ce4fee8705f815')
        self.assertEqual(image[0x7A0:0x7FA],b'\xff'*90)

    def test_fresh_process_only_fragment_and_descriptor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for part in ('a','b'):
                subprocess.run([sys.executable,str(ROOT/'tools/fire_callback_refactor.py'),'--output-dir',str(root/part)],check=True,capture_output=True,timeout=10)
            self.assertEqual({p.name for p in (root/'a').iterdir()},{'callback-refactor.bin','callback-refactor.json'})
            for name in ('callback-refactor.bin','callback-refactor.json'):
                self.assertEqual((root/'a'/name).read_bytes(),(root/'b'/name).read_bytes())
            self.assertEqual(json.loads((root/'a/callback-refactor.json').read_text())['fragment_size'],146)
