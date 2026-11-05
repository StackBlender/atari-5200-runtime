# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""First authored cold-start image. Execution/provider acceptance remains pending."""
import argparse
import hashlib
import json
from pathlib import Path
from emitter import Image, Region, report_json

# Original pixels, authored from the segment coordinates in startup-brief.md.
DIGIT_SEGMENTS = ("abcdef", "bc", "abdeg", "abcdg", "bcfg",
                  "acdfg", "acdefg", "abc", "abcdefg", "abcdfg")
SEGMENTS = {
    "a": [(x, 0) for x in range(2, 6)],
    "g": [(x, 3) for x in range(2, 6)],
    "d": [(x, 6) for x in range(2, 6)],
    "f": [(1, y) for y in (1, 2)], "b": [(6, y) for y in (1, 2)],
    "e": [(1, y) for y in (4, 5)], "c": [(6, y) for y in (4, 5)],
}
ZERO_MMIO = (0xD40E, 0xD400, 0xE80E, 0xE80F, 0xE801, 0xE803,
             0xE805, 0xE807, 0xC01D, 0xC01B, 0xC01A)


def original_font():
    data = bytearray(1024)
    for digit, segments in enumerate(DIGIT_SEGMENTS):
        for segment in segments:
            for x, y in SEGMENTS[segment]:
                data[8 * (0x50 + digit) + y] |= 1 << (7 - x)
    return bytes(data)


def startup_image():
    root = Path(__file__).resolve().parents[1]
    allocation = json.loads((root / "docs/allocation-plan.json").read_text())
    image = Image([Region(row["name"], row["start"], row["end"], row["kind"])
                   for row in allocation["regions"]])
    emit = image.instruction
    image.org(0xF800)
    image.label("original_font")
    image.bytes(*original_font())
    image.org(0xFC00)
    image.label("reset")
    emit("SEI")
    emit("CLD")
    emit("LDX", "imm", 0xFF)
    emit("TXS")
    emit("LDA", "imm", 0)
    for address in ZERO_MMIO:
        emit("STA", "abs", address)
    for address, value in [(0xD401, 2), (0xD409, 0xF8), (0xD40F, 0)]:
        emit("LDA", "imm", value)
        emit("STA", "abs", address)
    emit("LDX", "imm", 0x18)
    image.label("zero_shadows")
    emit("STA", "zpx", 0)
    emit("DEX")
    emit("BPL", "rel", "zero_shadows")
    emit("LDX", "imm", 0)
    image.label("initialize_vectors")
    emit("LDA", "imm", 0x86)
    emit("STA", "absx", 0x0200)
    emit("INX")
    emit("LDA", "imm", 0xFC)
    emit("STA", "absx", 0x0200)
    emit("INX")
    emit("CPX", "imm", 0x1C)
    emit("BNE", "rel", "initialize_vectors")
    emit("JSR", "abs", "validate_metadata")
    emit("CLC")
    emit("CLV")
    emit("LDY", "imm", 0)
    emit("LDX", "imm", 0)
    emit("LDA", "imm", 0)
    image.label("cart_handoff")
    emit("JMP", "ind", 0xBFFE)
    for name, address in [("nmi_fault", 0xFC80), ("irq_fault", 0xFC83),
                          ("startup_fault", 0xFC86)]:
        image.org(address)
        image.label(name)
        emit("JMP", "abs", name)
    image.org(0xFEB0)
    image.label("validate_metadata")
    emit("LDX", "imm", 0)
    image.label("validate_digit")
    emit("LDA", "absx", 0xBFE8)
    emit("CMP", "imm", 0x50)
    emit("BCC", "rel", "invalid_metadata")
    emit("CMP", "imm", 0x5A)
    emit("BCS", "rel", "invalid_metadata")
    emit("INX")
    emit("CPX", "imm", 22)
    emit("BNE", "rel", "validate_digit")
    emit("LDA", "abs", 0xBFFF)
    emit("CMP", "imm", 0x40)
    emit("BCC", "rel", "invalid_metadata")
    emit("CMP", "imm", 0xC0)
    emit("BCS", "rel", "invalid_metadata")
    emit("CMP", "imm", 0xBF)
    emit("BNE", "rel", "valid_metadata")
    emit("LDA", "abs", 0xBFFE)
    emit("CMP", "imm", 0xE8)
    emit("BCS", "rel", "invalid_metadata")
    image.label("valid_metadata")
    emit("RTS")
    image.label("invalid_metadata")
    emit("JMP", "abs", "startup_fault")
    image.vectors(nmi="nmi_fault", reset="reset", irq="irq_fault")
    data, report = image.finish()
    report.update(purpose="authored-startup-awaiting-execution",
                  runtime_abi="sb52-dev-cc65-v1", authored_capabilities=["cold-start-digits-v1"],
                  execution_verified=False, provider_approved=False,
                  retail_compatibility=False, target="ntsc-four-port-development",
                  mapper="Linear32K", reset_kind="cold-only",
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  encoder_sha256=hashlib.sha256((root/"tools/emitter.py").read_bytes()).hexdigest(),
                  allocation_sha256=hashlib.sha256((root/"docs/allocation-plan.json").read_bytes()).hexdigest())
    # capabilities remains empty until independent execution acceptance.
    return data, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    data, report = startup_image()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "startup.bin").write_bytes(data)
    (args.output_dir / "startup-map.json").write_text(report_json(report), encoding="utf-8")


if __name__ == "__main__":
    main()
