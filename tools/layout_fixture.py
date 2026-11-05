# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Generate an ORIGINAL tool fixture, not a usable Atari runtime/provider."""
import argparse
from pathlib import Path
from emitter import Image, Region, report_json


def fixture():
    # Tool-test policy only. This does not fix future BIOS service/font addresses.
    image = Image([
        Region("tool_code", 0xF800, 0xF840, "code"),
        Region("future_allowance", 0xF840, 0xFFFA, "reserved"),
        Region("cpu_vectors", 0xFFFA, 0x10000, "vectors"),
    ])
    image.label("loop")
    image.instruction("JMP", "abs", "loop")
    image.label("interrupt_return")
    image.instruction("RTI")
    image.vectors(nmi="interrupt_return", reset="loop", irq="interrupt_return")
    return image.finish()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    data, report = fixture()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "layout-test.bin").write_bytes(data)
    (args.output_dir / "layout-test.json").write_text(report_json(report), encoding="utf-8")


if __name__ == "__main__":
    main()
