# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Original cartridge-side input recorder fragment, not a runnable cartridge."""
import argparse
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError, fixed_instruction, integer

SIZE = 80
CAPACITY = 32
CONTROL_SIZE = 7
BUFFER_SIZE = CAPACITY * 4


def recorder_fragment(entry=0x8000, control=0x700, buffer=0x800):
    integer(entry, 0x4000, 0xBFE8-SIZE, "fragment entry")
    integer(control, 0x620, 0x4000-CONTROL_SIZE, "cart control RAM")
    integer(buffer, 0x620, 0x4000-BUFFER_SIZE, "cart record RAM")
    if control < buffer+BUFFER_SIZE and buffer < control+CONTROL_SIZE:
        raise AssemblyError("control and record RAM overlap")
    out = bytearray()
    def emit(op, mode="impl", operand=None):
        if op == "LDX" and mode == "abs":
            integer(operand, 0, 65535, "LDX operand")
            out.extend(bytes((0xAE, operand & 255, operand >> 8)))
        else:
            out.extend(fixed_instruction(op, mode, operand))
    # A=port, X=old, Y=new. Two entries tag the common publication path.
    for kind in (0, 1):
        emit("STA", "abs", control+2)
        emit("LDA", "imm", kind)
        emit("JMP", "abs", entry+16)
    emit("STA", "abs", control+5)
    emit("STX", "abs", control+3)
    emit("STY", "abs", control+4)
    emit("LDX", "abs", control)
    emit("CPX", "imm", CAPACITY)
    branch = len(out)
    out.extend((0xB0, 0))  # fixed after the full-buffer entry is known
    emit("LDX", "abs", control+1)
    for slot in (5, 2, 3, 4):
        emit("LDA", "abs", control+slot)
        emit("STA", "absx", buffer)
        emit("INX")
    emit("STX", "abs", control+1)
    emit("LDX", "abs", control)
    emit("INX")
    emit("STX", "abs", control)  # publish complete count LAST
    emit("RTS")
    full = len(out)
    out[branch+1] = integer(full-branch-2, 0, 127, "full branch displacement")
    emit("LDA", "imm", 1)
    emit("STA", "abs", control+6)
    emit("RTS")
    if len(out) != SIZE:
        raise AssemblyError("recorder layout changed")
    data = bytes(out)
    return data, dict(schema=1, purpose="unapproved-input-callback-fragment",
                      executable_cartridge=False, execution_verified=False,
                      runtime_provider=False, allocation_approved=False,
                      key_entry=entry, fire_entry=entry+8, common=entry+16,
                      full_entry=entry+full, size=SIZE,
                      control_start=control, control_size=CONTROL_SIZE,
                      control_fields={"count":0, "cursor":1, "port":2,
                                      "old":3, "new":4, "kind":5, "overflow":6},
                      buffer_start=buffer, buffer_size=BUFFER_SIZE,
                      capacity=CAPACITY, record_fields=["kind", "port", "old", "new"],
                      nominal_callback_cycles=97,
                      nominal_full_cycles_max=43,
                      hardware_timing_verified=False,
                      extra_stack_bytes=0, callback_return="RTS",
                      sha256=hashlib.sha256(data).hexdigest())


def decode_snapshot(control, buffer):
    """Decode caller-supplied original diagnostic RAM, never a firmware trace.

    Snapshot must be taken quiescently. Unused buffer bytes have no meaning.
    This validates the recorder format, not chip acquisition or callback execution.
    """
    if type(control) is not bytes or len(control) != CONTROL_SIZE:
        raise AssemblyError("expected seven control bytes")
    if type(buffer) is not bytes or len(buffer) != BUFFER_SIZE:
        raise AssemblyError("expected 128 buffer bytes")
    count, cursor = control[:2]
    if count > CAPACITY or cursor != count*4 or control[6] not in (0, 1):
        raise AssemblyError("incoherent recorder control")
    if control[6] and count != CAPACITY:
        raise AssemblyError("overflow without full buffer")
    events = []
    for i in range(count):
        kind, port, old, new = buffer[i*4:i*4+4]
        valid = {0xFF, *range(1, 16)} if kind == 0 else set(range(4))
        if kind not in (0, 1) or port > 3 or old not in valid or new not in valid or old == new:
            raise AssemblyError("invalid input event record")
        events.append(dict(kind="key" if kind == 0 else "fire", port=port, old=old, new=new))
    return dict(schema=1, purpose="diagnostic-event-format-only", events=events,
                overflow=bool(control[6]), acquisition_verified=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entry", type=lambda x:int(x,0), default=0x8000)
    parser.add_argument("--control", type=lambda x:int(x,0), default=0x700)
    parser.add_argument("--buffer", type=lambda x:int(x,0), default=0x800)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        data, descriptor = recorder_fragment(args.entry, args.control, args.buffer)
    except AssemblyError as error:
        parser.error(str(error))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/"input-callback.bin").write_bytes(data)
    (args.output_dir/"input-callback.json").write_text(json.dumps(descriptor,sort_keys=True,indent=2)+"\n")


if __name__ == "__main__":
    main()
