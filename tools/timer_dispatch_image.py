# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Original timer dispatch candidate; integration review/execution pending."""
import argparse
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError, Image, Region, integer, report_json
from startup_image import original_font, ZERO_MMIO

# Documented NMOS additions local to this image. Never mutate the baseline
# emitter's global table or change the reproducible711a2e9 export inputs.
SERVICE_OPCODES = {("EOR", "imm"): 0x49, ("AND", "zp"): 0x25, ("AND", "imm"): 0x29, ("INC", "zp"): 0xE6,
                   ("TXA", "impl"): 0x8A, ("TYA", "impl"): 0x98,
                   ("TAX", "impl"): 0xAA, ("TAY", "impl"): 0xA8}


class ServiceImage(Image):
    def instruction(self, mnemonic, mode="impl", operand=None):
        key = (mnemonic, mode)
        if key not in SERVICE_OPCODES:
            return super().instruction(mnemonic, mode, operand)
        if mode == "impl":
            if operand is not None:
                raise AssemblyError("implied instruction takes no operand")
            encoded = [SERVICE_OPCODES[key]]
        else:
            encoded = [SERVICE_OPCODES[key], integer(operand, 0, 255, "operand")]
        start = self.pc
        self._write(encoded, {"code"})
        self.instructions.add(start)


def timer_dispatch_image():
    root = Path(__file__).resolve().parents[1]
    allocation = json.loads((root/"docs/allocation-plan.json").read_text())
    image = ServiceImage([Region(r["name"], r["start"], r["end"], r["kind"])
                          for r in allocation["regions"]])
    emit = image.instruction
    image.org(0xF800)
    image.label("original_font")
    image.bytes(*original_font())
    image.org(0xFC00)
    image.label("reset")
    for mnemonic in ["SEI", "CLD"]:
        emit(mnemonic)
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
    emit("JSR", "abs", "initialize_services")
    # Explicit prime: cold ALLPOT=0 does not imply any acquired sample.
    emit("LDA", "imm", 3)
    emit("STA", "abs", 0xE80F)
    emit("LDA", "imm", 4)
    emit("STA", "abs", 0xC01F)
    emit("STA", "abs", 0xE80B)
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
    image.org(0xFCA0)
    image.label("system_vbi")
    for mnemonic in ["PHA", "TXA", "PHA", "TYA", "PHA"]:
        emit(mnemonic)
    emit("JMP", "abs", "clock_tick")
    image.org(0xFCB0)
    image.label("vbi_exit")
    for mnemonic in ["PLA", "TAY", "PLA", "TAX", "PLA", "RTI"]:
        emit(mnemonic)
    image.org(0xFCC0)
    image.label("nmi_classifier")
    emit("PHA")
    emit("LDA", "abs", 0xD40F)
    emit("AND", "imm", 0xE0)
    emit("CMP", "imm", 0x40)
    emit("BEQ", "rel", "vbi_source")
    emit("CMP", "imm", 0x80)
    emit("BNE", "rel", "nmi_fault")
    emit("STA", "abs", 0xD40F)
    emit("PLA")
    emit("JMP", "ind", 0x0206)
    image.label("vbi_source")
    emit("STA", "abs", 0xD40F)
    emit("PLA")
    emit("JMP", "ind", 0x0202)
    image.org(0xFD00)
    image.label("irq_classifier")
    for mnemonic in ["PHA", "TXA", "PHA", "TSX", "INX", "INX", "INX"]:
        emit(mnemonic)
    # Increment the byte index, not the absolute base: stacked P wraps in 0100.
    emit("LDA", "absx", 0x0100)
    emit("AND", "imm", 0x10)
    emit("BNE", "rel", "brk_dispatch")
    image.label("irq_dispatch")
    for mnemonic in ["PLA", "TAX", "PLA"]:
        emit(mnemonic)
    emit("JMP", "ind", 0x0200)
    image.label("brk_dispatch")
    for mnemonic in ["PLA", "TAX", "PLA"]:
        emit(mnemonic)
    emit("JMP", "ind", 0x020E)
    image.org(0xFD40)
    image.label("analog_transfer")
    emit("LDA", "abs", 0xE808)
    emit("BNE", "rel", "analog_exit")
    for register, shadow in [(0xE800, 0x11), (0xE801, 0x12),
                             (0xE802, 0x13), (0xE803, 0x14),
                             (0xE804, 0x15), (0xE805, 0x16),
                             (0xE806, 0x17), (0xE807, 0x18)]:
        emit("LDA", "abs", register)
        emit("STA", "zp", shadow)
    emit("LDA", "imm", 0)
    emit("STA", "abs", 0xE80B)
    image.label("analog_exit")
    emit("JMP", "abs", "display_transfer")
    image.org(0xFDF0)
    image.label("clock_tick")
    emit("INC", "zp", 1)
    emit("BNE", "rel", "check_critic")
    emit("INC", "zp", 2)
    image.label("check_critic")
    emit("LDA", "zp", 3)
    emit("BNE", "rel", "critical_exit")
    emit("JMP", "abs", "analog_transfer")
    image.label("critical_exit")
    emit("JMP", "abs", "vbi_exit")
    image.org(0xFE00)
    image.label("system_timer")
    for mnemonic in ["PHA", "TXA", "PHA", "TYA", "PHA"]:
        emit(mnemonic)
    emit("LDA", "abs", 0xE80E)
    emit("EOR", "imm", 0xFF)
    emit("AND", "zp", 0)
    emit("TAX")
    emit("AND", "imm", 0xF8)
    emit("BNE", "rel", "timer_fault")
    emit("TXA")
    emit("AND", "imm", 1)
    emit("BNE", "rel", "timer1")
    emit("TXA")
    emit("AND", "imm", 2)
    emit("BNE", "rel", "timer2")
    emit("TXA")
    emit("AND", "imm", 4)
    emit("BEQ", "rel", "timer_fault")
    for name, clear_mask, vector in [("timer4", 0xFB, 0x021A),
                                     ("timer2", 0xFD, 0x0218),
                                     ("timer1", 0xFE, 0x0216)]:
        image.label(name)
        emit("LDA", "zp", 0)
        emit("AND", "imm", clear_mask)
        emit("STA", "abs", 0xE80E)
        emit("LDA", "zp", 0)
        emit("STA", "abs", 0xE80E)
        emit("JMP", "ind", vector)
    image.label("timer_fault")
    emit("JMP", "abs", "irq_fault")
    image.org(0xFE50)
    image.label("display_transfer")
    # Original policy: pointer, nine colors, DMA enable last. Hardware masks
    # and delayed effects belong to the chips; no hidden host interpretation.
    for shadow, register in [(0x05, 0xD402), (0x06, 0xD403),
                             (0x08, 0xC012), (0x09, 0xC013),
                             (0x0A, 0xC014), (0x0B, 0xC015),
                             (0x0C, 0xC016), (0x0D, 0xC017),
                             (0x0E, 0xC018), (0x0F, 0xC019),
                             (0x10, 0xC01A), (0x07, 0xD400)]:
        emit("LDA", "zp", shadow)
        emit("STA", "abs", register)
    emit("JMP", "ind", 0x0204)
    # Same original metadata validation algorithm; no new cartridge semantics.
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
    image.org(0xFEDC)
    image.label("initialize_services")
    for address, value in [(0x0202, 0xA0), (0x0203, 0xFC),
                           (0x0204, 0xB0), (0x0205, 0xFC),
                           (0x0200, 0x00), (0x0201, 0xFE)]:
        emit("LDA", "imm", value)
        emit("STA", "abs", address)
    emit("RTS")
    image.vectors(nmi="nmi_classifier", reset="reset", irq="irq_classifier")
    data, report = image.finish()
    report.update(purpose="authored-timer-dispatch-awaiting-execution",
                  runtime_abi="sb52-dev-cc65-v1",
                  authored_capabilities=["cold-start-digits-v1", "vbi-clock-v1", "display-shadow-v1", "dli-dispatch-v1", "analog-shadow-v1", "irq-brk-dispatch-v1", "timer-dispatch-v1"],
                  execution_verified=False, provider_approved=False,
                  retail_compatibility=False, target="ntsc-four-port-development",
                  mapper="Linear32K", reset_kind="cold-only",
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  encoder_sha256=hashlib.sha256((root/"tools/emitter.py").read_bytes()).hexdigest(),
                  baseline_startup_sha256=hashlib.sha256((root/"tools/startup_image.py").read_bytes()).hexdigest(),
                  allocation_sha256=hashlib.sha256((root/"docs/allocation-plan.json").read_bytes()).hexdigest())
    return data, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    data, report = timer_dispatch_image()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/"timer-dispatch.bin").write_bytes(data)
    (args.output_dir/"timer-dispatch-map.json").write_text(report_json(report), encoding="utf-8")


if __name__ == "__main__":
    main()
