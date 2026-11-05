# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Original ENTRY-01 capture fragment. Not a cartridge, runtime or approved probe."""
import argparse
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError, fixed_instruction, integer

VERSION = 1
SIZE = 26
COMPLETE = 0xA5
P_MASK = 0xCF  # Only N,V,D,I,Z,C; no claim about pushed B/expansion bits.
SLOTS = {"a": 0, "x": 1, "y": 2, "p_pushed": 3, "sp": 4, "complete": 5}


def capture_fragment(entry_address, result_start):
    # These bounds define our proposed diagnostic layout, not proven RAM ownership.
    integer(entry_address, 0x4000, 0xBFE8 - SIZE, "entry address")
    integer(result_start, 0x0220, 0x4000 - len(SLOTS), "candidate result start")
    steps = [
        ("STA", "abs", result_start),
        ("STX", "abs", result_start + 1),
        ("STY", "abs", result_start + 2),
        ("PHP", "impl", None),
        ("PLA", "impl", None),
        ("STA", "abs", result_start + 3),
        ("TSX", "impl", None),
        ("STX", "abs", result_start + 4),
        ("LDA", "imm", COMPLETE),
        ("STA", "abs", result_start + 5),
        ("JMP", "abs", entry_address + 23),
    ]
    fragment = b"".join(fixed_instruction(*step) for step in steps)
    assert len(fragment) == SIZE
    tool_dir = Path(__file__).resolve().parent
    descriptor = dict(schema=1, probe="ENTRY-01", capture_version=VERSION,
                      purpose="unapproved-capture-fragment", executable_cartridge=False,
                      execution_approved=False, entry_address=entry_address,
                      result_start=result_start, result_size=len(SLOTS),
                      slots=SLOTS.copy(), size=SIZE, p_known_mask=P_MASK,
                      stack_extra_bytes=1, stack_net_change=0,
                      fragment_sha256=hashlib.sha256(fragment).hexdigest(),
                      source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      encoder_sha256=hashlib.sha256((tool_dir / "emitter.py").read_bytes()).hexdigest())
    return fragment, descriptor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entry-address", required=True, type=lambda x: int(x, 0))
    parser.add_argument("--result-start", required=True, type=lambda x: int(x, 0))
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        fragment, descriptor = capture_fragment(args.entry_address, args.result_start)
    except AssemblyError as exc:
        parser.error(str(exc))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "entry-capture.bin").write_bytes(fragment)
    (args.output_dir / "entry-capture.json").write_text(
        json.dumps(descriptor, sort_keys=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
