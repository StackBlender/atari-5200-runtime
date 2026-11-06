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
from printable_glyphs import DRAWINGS, asset, glyph
from fire_bridge_image import fire_bridge_image
ROOT=Path(__file__).resolve().parents[1]


class PrintableGlyphTests(unittest.TestCase):
    def test_full_repertoire_cells_and_distinct_original_shapes(self):
        data,_=asset()
        self.assertEqual(set(DRAWINGS),set(map(chr,range(32,127))))
        self.assertEqual(len(data),760)
        cells=[data[index:index+8] for index in range(0,760,8)]
        self.assertEqual(cells[0],bytes(8))
        self.assertTrue(all(any(cell) for cell in cells[1:]))
        self.assertEqual(len(set(cells)),95)
        self.assertTrue(all(value&0x83==0 for value in data))

    def test_selected_independently_expected_letter_digit_punctuation_pixels(self):
        for char,expected in {
            'A':'102844447c444400','0':'38444c5464443800',
            'a':'000038043c443c00','z':'00007c0810207c00',
            '?':'3844040810001000','!':'1010101000100000',
        }.items():
            self.assertEqual(glyph(DRAWINGS[char]),bytes.fromhex(expected))
        self.assertEqual(glyph('#..../.#.../..#../...#./....#'),bytes.fromhex('4020100804000000'))
        self.assertTrue(all(glyph(DRAWINGS[c])[7] for c in 'gjpqy'))
        self.assertTrue(all(glyph(DRAWINGS[c])[7]==0 for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))

    def test_malformed_geometry_and_incomplete_repertoire_fail(self):
        for drawing in ('','....','......','...../'*8+'.....','..X..',1,None):
            with self.subTest(drawing=drawing),self.assertRaises(ValueError):glyph(drawing)
        with patch.dict(DRAWINGS,{'\x7f':'.....'}),self.assertRaises(ValueError):asset()
        with patch.dict(DRAWINGS,{'A':'bad'}),self.assertRaises(ValueError):asset()

    def test_metadata_is_unbound_and_never_runtime_approval(self):
        data,encoded=asset();report=json.loads(encoded)
        self.assertEqual(report['purpose'],'standalone-original-printable-glyphs-only')
        for field in ('runtime_abi','atari_encoding','bank_address'):self.assertIsNone(report[field])
        for field in ('provider_approved','execution_verified'):self.assertIs(report[field],False)
        self.assertEqual(report['capabilities'],[])
        self.assertEqual((report['glyph_count'],report['bytes_per_glyph'],report['ascii_first'],report['ascii_last']),(95,8,32,126))
        self.assertEqual(report['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(report['source_sha256'],hashlib.sha256((ROOT/'tools/printable_glyphs.py').read_bytes()).hexdigest())

    def test_no_accepted_image_or_original_font_change(self):
        data,report=fire_bridge_image()
        self.assertEqual(hashlib.sha256(data).hexdigest(),'c5fd8df1564c28e5ed4c5aad9f8eabdc64a62e32de28e8dcce6bfae7ea533d24')
        self.assertEqual(report['used'],1895)
        self.assertEqual(data[0x7a0:0x7fa],b'\xff'*90)

    def test_fresh_cli_is_reproducible_and_matches_direct_asset(self):
        with tempfile.TemporaryDirectory() as tmp:
            directories=[Path(tmp)/name for name in ('a','b')]
            for directory in directories:
                subprocess.run([sys.executable,str(ROOT/'tools/printable_glyphs.py'),'--output-dir',str(directory)],check=True,capture_output=True,timeout=10)
            data,report=asset()
            for directory in directories:
                self.assertEqual((directory/'printable-glyphs.bin').read_bytes(),data)
                self.assertEqual((directory/'printable-glyphs.json').read_text(),report)
