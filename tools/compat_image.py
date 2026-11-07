# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Compatibility generation over callable-reset-v1. No native admission inferred.

Three consumer-observed behaviours (software expectations seen through bounded local
observation, not manufacturer bytes) that the earlier generations did not provide:
 1. Software assumes vertical-blank NMI is already running at cartridge handoff and
    polls the frame counter; reset now writes NMIEN=$40 just before the handoff.
 2. Software polls the LOW frame counter byte at $0002 for a per-frame change; $0001
    is the high byte. The default clock body now increments $0002 and carries into $0001.
 3. An NMI can arrive with no source flagged in NMIST; the classifier returned to the
    fault loop. It now treats that as spurious (PLA, RTI) instead of faulting.
 4. Software ends its own vertical-blank handler with JMP $FCB2 (expecting the full
    register-restoring exit to START there) and restores the immediate-VBI vector to $FCB8.
    The exit sequence now begins at $FCB2 (two NOPs keep $FCB0 valid) and $FCB8 is
    JMP system_vbi."""
import argparse
import hashlib
from pathlib import Path
from emitter import AssemblyError, report_json
from callable_reset_image import callable_reset_image, RESET, END, ORIGIN

PARENT_SHA256 = '97b1304d'  # prefix check; full parent hash is verified from the generator output
TAIL = bytes.fromhex('18b8a000a200a900')   # CLC CLV LDY#0 LDX#0 LDA#0
ENABLE_VBI = bytes.fromhex('a9408d0ed4')   # LDA #$40, STA NMIEN
CLOCK = 0xFDF0
CLASSIFIER_BNE_OPERAND = 0xFCCD
SPURIOUS = 0xFCDC
EXIT = 0xFCB0
VBI_ENTRY = 0xFCA0
VBI_ALIAS = 0xFCB8


def _off(address):
    return address - ORIGIN


def compat_image():
    parent, mapping = callable_reset_image()
    if not hashlib.sha256(parent).hexdigest().startswith(PARENT_SHA256):
        raise AssemblyError('compat requires the exact callable-reset parent')
    image = bytearray(parent)
    reset = _off(RESET)
    code = bytearray(parent[reset:reset + 0x80])
    join = code.index(bytes.fromhex('2080fd')) + 3
    if code[join:join + 8] != TAIL or code[join + 8] != 0x90:
        raise AssemblyError('callable-reset tail differs from the reviewed sequence')
    new = bytes(code[:join]) + ENABLE_VBI + TAIL
    branch_at = len(new)
    new += bytes([0x90, (END - (branch_at + 2)) & 0xFF])
    if len(new) + 0 > END:
        raise AssemblyError('NMI enable overruns the fall-through offset')
    image[reset:reset + 0x80] = new + b'\xff' * (0x80 - len(new))
    image[reset + END:reset + END + 3] = bytes.fromhex('6cfebf')
    clock = _off(CLOCK)
    if parent[clock:clock + 6] != bytes.fromhex('e601d002e602'):
        raise AssemblyError('clock body differs from the reviewed sequence')
    image[clock + 1] = 0x02
    image[clock + 5] = 0x01
    bne = _off(CLASSIFIER_BNE_OPERAND)
    if parent[bne - 1] != 0xD0 or parent[bne] != 0xB2 or parent[_off(SPURIOUS):_off(SPURIOUS) + 2] != b'\xff\xff':
        raise AssemblyError('NMI classifier differs from the reviewed sequence')
    image[bne] = SPURIOUS - (CLASSIFIER_BNE_OPERAND + 1)
    image[_off(SPURIOUS):_off(SPURIOUS) + 2] = bytes.fromhex('6840')   # PLA, RTI
    ex = _off(EXIT)
    if parent[ex:ex + 8] != bytes.fromhex('68a868aa6840ffff') or parent[_off(VBI_ALIAS):_off(VBI_ALIAS) + 3] != b'\xff' * 3:
        raise AssemblyError('vbi exit region differs from the reviewed sequence')
    image[ex:ex + 8] = bytes.fromhex('eaea68a868aa6840')          # NOP NOP, then the exit at $FCB2
    image[_off(VBI_ALIAS):_off(VBI_ALIAS) + 3] = bytes.fromhex('4ca0fc')   # JMP system_vbi
    data = bytes(image)
    startup_used = len(new)
    added = 5 + 2 + 2 + 3
    mapping = dict(mapping)
    symbols = dict(mapping['symbols']); symbols.update(nmi_spurious=SPURIOUS, vbi_exit_entry=0xFCB2, vbi_alias=VBI_ALIAS)
    allocations = [dict(a) for a in mapping['allocations']]
    for a in allocations:
        if a['name'] == 'startup':
            grown = startup_used - (a['used'])
            a.update(used=startup_used, remaining=a['end'] - a['start'] - startup_used)
        if a['name'] == 'interrupts':
            a.update(used=a['used'] + 7, remaining=a['remaining'] - 7)
    base = mapping['nominal_startup']
    mapping.update(purpose='authored-compat-awaiting-native-admission',
        sha256=hashlib.sha256(data).hexdigest(), symbols=symbols, allocations=allocations,
        used=mapping['used'] + added, remaining=mapping['remaining'] - added,
        parent_image_sha256=hashlib.sha256(parent).hexdigest(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        compat=dict(nmien_at_handoff=0x40, frame_counter_low=0x0002, frame_counter_high=0x0001,
            spurious_nmi='PLA RTI', vbi_exit_entry=0xFCB2, vbi_alias='JMP system_vbi at FCB8', source='consumer-observed software behaviour, not manufacturer firmware'),
        nominal_startup=dict(base,
            numeric_normal_cycles=base['numeric_normal_cycles'] + 6,
            numeric_boundary_cycles=base['numeric_boundary_cycles'] + 6,
            ff_normal_cycles=base['ff_normal_cycles'] + 6,
            ff_boundary_cycles=base['ff_boundary_cycles'] + 6,
            numeric_normal_instructions=base['numeric_normal_instructions'] + 2,
            numeric_boundary_instructions=base['numeric_boundary_instructions'] + 2,
            ff_normal_instructions=base['ff_normal_instructions'] + 2,
            ff_boundary_instructions=base['ff_boundary_instructions'] + 2,
            basis='callable-reset plus LDA#/STA abs before handoff; static cycles, not natively traced'))
    mapping['authored_capabilities'] = [*mapping['authored_capabilities'], 'compat-v1']
    return data, mapping


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    try:
        data, mapping = compat_image()
    except AssemblyError as error:
        parser.error(str(error))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'compat.bin').write_bytes(data)
    (args.output_dir / 'compat-map.json').write_text(report_json(mapping))


if __name__ == '__main__':
    main()
