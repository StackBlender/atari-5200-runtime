# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Static allowlist audit of the nonrunnable fire fragment; no CPU execution.

Addresses are synthetic F800-based. Indexed footprints are conditional on the
reviewed X=0..3 loop/selected-port invariant; this tool does not prove that invariant.
No registers, flags, RAM, chips, callbacks or instruction timing are simulated.
"""
import argparse
import json
from pathlib import Path


class AuditError(ValueError):
    pass


# Independent narrow decoding policy, deliberately not imported from the emitter.
# opcode: (length, access, allowed operand/base)
POLICY = {
    0xAD: (3, "read", {0x600, 0x614, 0x61B, 0xE80F}),
    0xBD: (3, "read_x", {0x610, 0x615, 0xC010}),
    0xAE: (3, "read", {0x602, 0x619, 0x61A}),
    0xAC: (3, "read", {0x61B}),
    0xCD: (3, "read", {0x61B}),
    0x0D: (3, "read", {0x61B}),
    0x8D: (3, "write", {0x614, 0x61A, 0x61B}),
    0x8E: (3, "write", {0x619}),
    0x9D: (3, "write_x", {0x610, 0x615}),
    0xA2: (2, None, None), 0xA9: (2, None, None),
    0xC9: (2, None, None), 0xE0: (2, None, None),
    0x49: (2, None, None), 0x29: (2, None, None),
    0x4A: (1, None, None), 0x8A: (1, None, None),
    0xE8: (1, None, None),
    0xD0: (2, "branch", None), 0xF0: (2, "branch", None),
    0x20: (3, "call", {0xF896}),
    0x4C: (3, "exit", {0xFD1A, 0xFD59}),
    0x6C: (3, "callback", {0x208}),
}


def audit(data):
    if not isinstance(data, bytes) or len(data) != 153:
        raise AuditError("expected exactly 153 fragment bytes")
    records = []
    offset = 0
    reads, writes = set(), set()
    while offset < len(data):
        opcode = data[offset]
        if opcode not in POLICY:
            raise AuditError(f"unapproved opcode at {offset}")
        length, access, allowed = POLICY[opcode]
        if offset + length > len(data):
            raise AuditError("truncated instruction")
        operand = int.from_bytes(data[offset+1:offset+length], "little")
        if allowed is not None and operand not in allowed:
            raise AuditError(f"unapproved {access} operand at {offset}")
        if access in {"read", "read_x", "write", "write_x"}:
            footprint = range(operand, operand + (4 if access.endswith("_x") else 1))
            (writes if access.startswith("write") else reads).update(footprint)
        records.append((offset, length, access, operand))
        offset += length
    starts = {row[0] for row in records}
    branches, calls, exits, callbacks = [], [], [], []
    for offset, length, access, operand in records:
        if access == "branch":
            target = offset + length + (operand if operand < 128 else operand - 256)
            # Neither routine may branch into the other or callback trampoline.
            lo, hi = (0, 81) if offset < 81 else (81, 150)
            if target not in starts or not lo <= target < hi:
                raise AuditError("branch leaves routine or targets operand")
            branches.append([offset, target])
        elif access == "call":
            if operand - 0xF800 not in starts:
                raise AuditError("callback call does not target instruction")
            calls.append(offset)
        elif access == "exit":
            exits.append([offset, operand])
        elif access == "callback":
            callbacks.append(offset)
    if calls != [62, 136] or exits != [[78, 0xFD1A], [147, 0xFD59]] or callbacks != [150]:
        raise AuditError("unexpected call/exit/callback boundary")
    if not {0, 81, 150}.issubset(starts):
        raise AuditError("entry does not target instruction")
    return dict(schema=1, purpose="static-fire-fragment-access-audit",
                execution_verified=False, allocation_approved=False,
                indexed_x_range_assumption=[0, 3],
                instruction_count=len(records), reads=sorted(reads), writes=sorted(writes),
                branches=branches, call_offsets=calls, exits=exits,
                callback_pointer=0x208,
                maximum_bridge_stack_bytes=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fragment", type=Path)
    args = parser.parse_args()
    try:
        result = audit(args.fragment.read_bytes())
    except (OSError, AuditError) as error:
        parser.exit(2, f"audit rejected: {error}\n")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
