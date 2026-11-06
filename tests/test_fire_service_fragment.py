# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from emitter import AssemblyError, OPCODES, Region
from fire_service_fragment import fire_fragment, FragmentImage
from keypad_window_image import keypad_window_image
ROOT=Path(__file__).resolve().parents[1]


class FireFragmentTests(unittest.TestCase):
    def test_exact_four_bottom_sources_preserve_top_and_separate_baseline(self):
        data,report=fire_fragment()
        expected=bytes.fromhex(
            "ad0006 c901 d047 a200 8e1906 bd10c0 49ff 2901 8d1b06 "
            "bd1006 2902 0d1b06 8d1b06 bd1006 cd1b06 f018 "
            "8d1a06 ad1b06 9d1006 ad1406 f00a ac1b06 8a ae1a06 2096f8 "
            "ae1906 e8 e004 d0c0 a901 8d1406 4c1afd")
        self.assertEqual(len(expected),81)
        self.assertEqual(data[:81],expected)
        self.assertEqual(report["offsets"]["bottom_next"],65)
        self.assertEqual(report["offsets"]["bottom_skip"],78)

    def test_exact_selected_top_independent_shift_baseline_and_callback(self):
        data,report=fire_fragment()
        expected=bytes.fromhex(
            "ae0206 ad0fe8 49ff 2908 4a 4a 8d1b06 bd1006 2901 0d1b06 8d1b06 "
            "bd1006 cd1b06 f018 8d1a06 ad1b06 9d1006 bd1506 f00a "
            "ac1b06 8a ae1a06 2096f8 ae0206 a901 9d1506 4c59fd 6c0802")
        self.assertEqual(data[81:],expected)
        self.assertEqual(report["offsets"]["top_baseline"],139)
        self.assertEqual(report["offsets"]["fire_callback_bridge"],150)

    def test_nonrunnable_scope_and_exact_budget_failure_projection(self):
        data,report=fire_fragment()
        self.assertEqual(len(data),153)
        self.assertNotEqual(len(data),2048)
        self.assertEqual(report["fragment_size"],153)
        self.assertEqual(report["sha256"],hashlib.sha256(data).hexdigest())
        self.assertEqual(report["purpose"],"nonrunnable-fire-service-fragment")
        self.assertIsNone(report["runtime_abi"])
        self.assertEqual(report["capabilities"],[])
        for flag in ("execution_verified","provider_approved","cumulative_allocation_approved","fits_current_extra_ceiling","fits_current_nonmargin_space"):
            self.assertFalse(report[flag])
        self.assertEqual(report["projected_cumulative_written"],1902)
        self.assertEqual(report["projected_extra_above_timer"],398)
        self.assertEqual((report["proposed_code_block_bytes"],report["proposed_margin_remaining"]),(160,90))
        self.assertEqual(2048-1902-90,56)

    def test_proposed_allocation_is_complete_and_keeps_font_vectors_reserved(self):
        proposal=json.loads((ROOT/"docs/fire-allocation-proposal.json").read_text())
        current=json.loads((ROOT/"docs/allocation-plan.json").read_text())
        regions=sorted(proposal["regions"],key=lambda r:r["start"])
        self.assertEqual(regions[0]["start"],0xF800)
        self.assertEqual(regions[-1]["end"],0x10000)
        for a,b in zip(regions,regions[1:]):self.assertEqual(a["end"],b["start"])
        rows={r["name"]:r for r in regions}
        self.assertEqual(rows["fire"],dict(name="fire",kind="code",start=0xFF00,end=0xFFA0))
        self.assertEqual(rows["margin"],dict(name="margin",kind="reserved",start=0xFFA0,end=0xFFFA))
        self.assertEqual(proposal["ram"]["cooperating_cart_input"],dict(start=0x600,end=0x620))
        self.assertFalse(proposal["planning_review_accepted"])
        self.assertEqual({r["name"]:r for r in current["regions"]}["margin"]["start"],0xFF00)

    def test_new_local_encodings_strict_and_old_candidate_unmodified(self):
        before=dict(OPCODES)
        for op,expected in (("ORA","0d1b06"),("CMP","cd1b06"),("LDY","ac1b06")):
            image=FragmentImage([Region("code",0xF800,0x10000,"code")])
            image.instruction(op,"abs",0x061B)
            self.assertEqual(bytes(image.data[:3]),bytes.fromhex(expected))
            for bad in (-1,65536,True,None):
                with self.assertRaises(AssemblyError):image.instruction(op,"abs",bad)
        fire_fragment()
        self.assertEqual(OPCODES,before)
        parent,_=keypad_window_image()
        self.assertEqual(hashlib.sha256(parent).hexdigest(),"3c1b419b9af94645ea537126d21e464f90f05013689ef7132656680d62d4207a")

    def test_fresh_process_reproducible_only_fragment_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for part in ("a","b"):
                subprocess.run([sys.executable,str(ROOT/"tools/fire_service_fragment.py"),"--output-dir",str(root/part)],check=True,capture_output=True,timeout=10)
            for name in ("fire-service-fragment.bin","fire-service-fragment.json"):
                self.assertEqual((root/"a"/name).read_bytes(),(root/"b"/name).read_bytes())
            self.assertEqual(len(list((root/"a").iterdir())),2)
