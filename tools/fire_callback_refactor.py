# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Measure a standalone callback-bridge refactor; not a runtime image.

The accepted cumulative image and existing fragment remain immutable. No
cumulative authoring/allocation permission or native equivalence is inferred.
"""
import argparse
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError, Image, Region, integer, report_json
from keypad_window_image import ServiceImage


class FragmentImage(ServiceImage):
    def instruction(self, mnemonic, mode="impl", operand=None):
        additions = {("ORA", "abs"):0x0D, ("CMP", "abs"):0xCD, ("LDY", "abs"):0xAC}
        if (mnemonic, mode) not in additions:
            return super().instruction(mnemonic, mode, operand)
        value=integer(operand,0,65535,"operand")
        start=self.pc
        self._write([additions[(mnemonic,mode)],value&255,value>>8],{"code"})
        self.instructions.add(start)


def refactor_fragment():
    image=FragmentImage([Region("fragment",0xF800,0xF8C0,"code"),
                         Region("unused",0xF8C0,0xFFFA,"reserved"),
                         Region("fixup-only-vectors",0xFFFA,0x10000,"vectors")])
    emit=image.instruction
    image.org(0xF800)
    image.label("bottom_fire")
    emit("LDA","abs",0x0600)
    emit("CMP","imm",1)
    emit("BNE","rel","bottom_skip")
    emit("LDX","imm",0)
    image.label("bottom_loop")
    emit("STX","abs",0x0619)
    emit("LDA","absx",0xC010)
    emit("EOR","imm",0xFF)
    emit("AND","imm",1)
    emit("STA","abs",0x061B)
    emit("LDA","absx",0x0610)
    emit("AND","imm",2)
    emit("ORA","abs",0x061B)
    emit("STA","abs",0x061B)
    emit("LDA","absx",0x0610)
    emit("CMP","abs",0x061B)
    emit("BEQ","rel","bottom_next")
    emit("STA","abs",0x061A)
    emit("LDA","abs",0x061B)
    emit("STA","absx",0x0610)
    emit("LDA","abs",0x0614)
    emit("BEQ","rel","bottom_next")
    emit("JSR","abs","fire_callback_bridge")
    image.label("bottom_next")
    emit("LDX","abs",0x0619)
    emit("INX")
    emit("CPX","imm",4)
    emit("BNE","rel","bottom_loop")
    emit("LDA","imm",1)
    emit("STA","abs",0x0614)
    image.label("bottom_skip")
    emit("JMP","abs",0xFD1A)  # separately pinned window_entry continuation
    image.label("top_fire")
    emit("LDX","abs",0x0602)
    emit("LDA","abs",0xE80F)
    emit("EOR","imm",0xFF)
    emit("AND","imm",8)
    emit("LSR")
    emit("LSR")
    emit("STA","abs",0x061B)
    emit("LDA","absx",0x0610)
    emit("AND","imm",1)
    emit("ORA","abs",0x061B)
    emit("STA","abs",0x061B)
    emit("LDA","absx",0x0610)
    emit("CMP","abs",0x061B)
    emit("BEQ","rel","top_baseline")
    emit("STA","abs",0x061A)
    emit("LDA","abs",0x061B)
    emit("STA","absx",0x0610)
    emit("LDA","absx",0x0615)
    emit("BEQ","rel","top_baseline")
    emit("JSR","abs","fire_callback_bridge")
    image.label("top_baseline")
    emit("LDX","abs",0x0602)
    emit("LDA","imm",1)
    emit("STA","absx",0x0615)
    emit("JMP","abs",0xFD59)  # separately pinned window_rotate continuation
    image.label("fire_callback_bridge")
    emit("LDY","abs",0x061B)
    emit("TXA")
    emit("LDX","abs",0x061A)
    emit("JMP","ind",0x0208)
    end=image.pc
    # Existing emitter requires vectors to resolve symbolic branches/calls.
    # These tool-only roots are discarded and NEVER returned as an image.
    image.vectors(nmi="bottom_fire",reset="bottom_fire",irq="top_fire")
    data,report=image.finish()
    fragment=data[:end-0xF800]
    return fragment,dict(schema=1,purpose="nonrunnable-callback-bridge-refactor-proposal",
                         runtime_abi=None,capabilities=[],execution_verified=False,
                         provider_approved=False,synthetic_origin=0xF800,
                         fragment_size=len(fragment),sha256=hashlib.sha256(fragment).hexdigest(),
                         offsets={name:value-0xF800 for name,value in report["symbols"].items()},
                         cumulative_parent_source="fce294b7448a7c5a1a35e6c5e5ed5611ee36473f",
                         cumulative_allocation_approved=False,
                         projected_routing_bridge_bytes=3,
                         projected_cumulative_written=1746+len(fragment)+3,
                         accepted_fire_source="a2a7455627a9ea3905464c295562debee2efec7d",
                         accepted_fragment_size=153,
                         code_bytes_saved=153-len(fragment),
                         additional_bridge_stack_bytes=0,
                         argument_setup_nominal_cycles=10,
                         setup_plus_call_bridge_nominal_cycles=21,
                         refactor_review_accepted=False,
                         projected_extra_above_timer=1746+len(fragment)+3-1504,
                         current_extra_ceiling=400,
                         fits_current_extra_ceiling=1746+len(fragment)+3-1504<=400,
                         window_parent_nonmargin_free=52,
                         accepted_cumulative_written=1902,
                         accepted_nonmargin_free=56,
                         projected_nonmargin_free=2048-(1746+len(fragment)+3)-90,
                         fits_window_parent_nonmargin_space=len(fragment)+3<=52,
                         proposed_code_block_bytes=160,
                         proposed_margin_remaining=90)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",required=True,type=Path)
    args=parser.parse_args()
    data,report=refactor_fragment()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/"callback-refactor.bin").write_bytes(data)
    (args.output_dir/"callback-refactor.json").write_text(report_json(report))


if __name__=="__main__":main()
