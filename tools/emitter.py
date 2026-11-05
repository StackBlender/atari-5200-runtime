# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Original bounded 6502 emitter. No emulator or Atari software ABI knowledge."""
from dataclasses import dataclass
import hashlib
import json


class AssemblyError(ValueError):
    pass


# Explicit subset of documented NMOS-compatible encodings. No mode inference,
# undocumented opcodes, timing model, text parser or branch relaxation.
OPCODES = {
    ("SEI", "impl"): 0x78, ("CLD", "impl"): 0xD8,
    ("TXS", "impl"): 0x9A, ("NOP", "impl"): 0xEA,
    ("RTI", "impl"): 0x40, ("RTS", "impl"): 0x60,
    ("INX", "impl"): 0xE8, ("DEX", "impl"): 0xCA,
    ("PHA", "impl"): 0x48, ("PLA", "impl"): 0x68,
    ("PHP", "impl"): 0x08, ("TSX", "impl"): 0xBA,
    ("STX", "abs"): 0x8E, ("STY", "abs"): 0x8C,
    ("LDA", "imm"): 0xA9, ("LDX", "imm"): 0xA2,
    ("LDY", "imm"): 0xA0,
    ("LDA", "zp"): 0xA5, ("STA", "zp"): 0x85,
    ("LDA", "abs"): 0xAD, ("STA", "abs"): 0x8D,
    ("JMP", "abs"): 0x4C, ("JSR", "abs"): 0x20,
    ("BNE", "rel"): 0xD0, ("BEQ", "rel"): 0xF0,
    ("BPL", "rel"): 0x10, ("BMI", "rel"): 0x30,
    ("BCC", "rel"): 0x90, ("BCS", "rel"): 0xB0,
}


def integer(value, low, high, description):
    if type(value) is not int or not low <= value <= high:
        raise AssemblyError(f"{description} must be an integer in {low}..{high}")
    return value


def fixed_instruction(mnemonic, mode="impl", operand=None):
    """Encode one fixed-address instruction; no symbols or relative guesses."""
    key = (mnemonic, mode)
    if key not in OPCODES or mode == "rel":
        raise AssemblyError("unsupported fixed instruction/address mode")
    if mode == "impl":
        if operand is not None:
            raise AssemblyError("implied instruction takes no operand")
        return bytes([OPCODES[key]])
    value = integer(operand, 0, 65535 if mode == "abs" else 255, "operand")
    if mode == "abs":
        return bytes([OPCODES[key], value & 255, value >> 8])
    return bytes([OPCODES[key], value])


@dataclass(frozen=True)
class Region:
    name: str
    start: int
    end: int  # exclusive
    kind: str  # code, asset, reserved or vectors


class Image:
    ORIGIN = 0xF800
    END = 0x10000

    def __init__(self, regions, fill=0xFF):
        self.fill = integer(fill, 0, 255, "fill")
        self.regions = tuple(regions)
        names = set()
        for region in self.regions:
            if not region.name or region.name in names:
                raise AssemblyError("empty or duplicate region name")
            names.add(region.name)
            integer(region.start, self.ORIGIN, self.END - 1, "region start")
            integer(region.end, region.start + 1, self.END, "region end")
            if region.kind not in {"code", "asset", "reserved", "vectors"}:
                raise AssemblyError("unknown region kind")
            if any(region.start < other.end and other.start < region.end
                   for other in self.regions if other is not region):
                raise AssemblyError("overlapping regions")
        # Require every byte to have an allocation, including unused allowance.
        if sum(r.end - r.start for r in self.regions) != self.END - self.ORIGIN:
            raise AssemblyError("allocation must cover the complete 2 KiB window")
        self.data = bytearray([self.fill] * (self.END - self.ORIGIN))
        self.written = set()
        self.pc = self.ORIGIN
        self.labels = {}
        self.fixups = []
        self.vector_targets = None
        self.instructions = set()

    def region_at(self, address):
        integer(address, self.ORIGIN, self.END - 1, "address")
        return next(r for r in self.regions if r.start <= address < r.end)

    def org(self, address):
        self.region_at(address)
        self.pc = address

    def label(self, name):
        if not isinstance(name, str) or not name or name in self.labels:
            raise AssemblyError("empty or duplicate label")
        self.region_at(self.pc)
        self.labels[name] = self.pc

    def _write(self, values, allowed):
        values = tuple(values)
        for value in values:
            integer(value, 0, 255, "byte")
        if not values:
            return
        region = self.region_at(self.pc)
        if region.kind not in allowed or self.pc + len(values) > region.end:
            raise AssemblyError("write exceeds its allocation or has wrong region kind")
        addresses = set(range(self.pc, self.pc + len(values)))
        if addresses & self.written:
            raise AssemblyError("overlapping writes")
        start = self.pc - self.ORIGIN
        self.data[start:start + len(values)] = bytes(values)
        self.written.update(addresses)
        self.pc += len(values)

    def bytes(self, *values):
        self._write(values, {"code", "asset"})

    def instruction(self, mnemonic, mode="impl", operand=None):
        key = (mnemonic, mode)
        if key not in OPCODES:
            raise AssemblyError("unsupported instruction/address mode")
        if mode == "rel":
            if not isinstance(operand, str) or not operand:
                raise AssemblyError("relative branch requires a label")
            encoded = bytes([OPCODES[key], 0])
        elif mode == "abs" and isinstance(operand, str) and operand:
            encoded = fixed_instruction(mnemonic, mode, 0)
        else:
            encoded = fixed_instruction(mnemonic, mode, operand)
        start = self.pc
        self._write(encoded, {"code"})
        self.instructions.add(start)
        if mode in {"abs", "rel"} and isinstance(operand, str):
            self.fixups.append((start + 1, mode, operand, mnemonic in {"JMP", "JSR"} or mode == "rel"))

    def vectors(self, *, nmi, reset, irq):
        if self.vector_targets is not None:
            raise AssemblyError("vectors already emitted")
        targets = (nmi, reset, irq)
        if any(not isinstance(name, str) or not name for name in targets):
            raise AssemblyError("vector targets must be labels")
        saved_pc = self.pc
        self.pc = 0xFFFA
        try:
            self._write([0] * 6, {"vectors"})
        except AssemblyError:
            self.pc = saved_pc
            raise
        self.pc = saved_pc
        self.vector_targets = targets
        for offset, name in enumerate(targets):
            self.fixups.append((0xFFFA + 2 * offset, "abs", name, True))

    def finish(self):
        if self.vector_targets is None:
            raise AssemblyError("missing CPU vectors")
        # Resolve into a fresh buffer so repeated output is deterministic and a
        # failed resolution cannot partially patch the source image.
        data = bytearray(self.data)
        for address, mode, label, executable in self.fixups:
            if label not in self.labels:
                raise AssemblyError(f"unresolved label: {label}")
            target = self.labels[label]
            if target not in self.written:
                raise AssemblyError("target points at unwritten allowance")
            if executable and target not in self.instructions:
                raise AssemblyError("control-flow target is not an emitted instruction")
            offset = address - self.ORIGIN
            if mode == "rel":
                delta = target - (address + 1)
                if not -128 <= delta <= 127:
                    raise AssemblyError("relative branch out of range")
                data[offset] = delta & 255
            else:
                data[offset:offset + 2] = target.to_bytes(2, "little")
        allocations = []
        for region in sorted(self.regions, key=lambda r: r.start):
            used = sum(region.start <= address < region.end for address in self.written)
            allocations.append(dict(name=region.name, kind=region.kind,
                                    start=region.start, end=region.end,
                                    used=used, remaining=region.end - region.start - used))
        report = dict(schema=1, purpose="emitter-layout-test-only", runtime_abi=None,
                      capabilities=[], origin=self.ORIGIN, size=len(data), fill=self.fill,
                      sha256=hashlib.sha256(data).hexdigest(),
                      used=len(self.written), remaining=len(data) - len(self.written),
                      symbols=dict(sorted(self.labels.items())), allocations=allocations)
        return bytes(data), report


def report_json(report):
    return json.dumps(report, indent=2, sort_keys=True) + "\n"
