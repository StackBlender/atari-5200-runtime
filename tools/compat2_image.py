# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Compatibility generation 2 over compat-v1. No native admission inferred.

Two further consumer-observed behaviours (software expectations seen through bounded
local observation, not manufacturer bytes):
 1. Software sets countdown bytes at $021C..$021F and waits for them to reach zero; the
    default vertical-blank service now decrements each non-zero byte once per frame
    (before the CRITIC test, so a critical section does not stall timers).
 2. Software leaves the immediate ($0202) or deferred ($0204) vector high byte at $FF
    to mean "use the default". The immediate path now falls back to system_vbi and the
    deferred path to the register-restoring exit at $FCB2 instead of jumping to $FFxx.
 No other behaviour changes; the new code sits in previously erased space."""
import argparse
import hashlib
from pathlib import Path
from emitter import AssemblyError, report_json
from compat_image import compat_image
from callable_reset_image import ORIGIN

PARENT_SHA256 = None   # parent identity is verified by structure (reviewed byte patterns) below
IMMEDIATE_JMP = 0xFCD9    # JMP ($0202) in the classifier VBI path
VBI_JSR_OPERAND = 0xFCA6  # system_vbi: JMP clock_body operand
DEFERRED_JMP = 0xFE8C     # JMP ($0204) after the shadow updates
IMMEDIATE_HELPER = 0xFCE0
TIMER_CLOCK = 0xFDC0
DEFERRED_HELPER = 0xFDE0
IMMEDIATE_CODE = bytes.fromhex('48ad0302c9fff00468' '6c0202' '68' '4ca0fc')
TIMER_CODE = bytes.fromhex('e602d002e601' 'a203' 'bd1c02' 'f003' 'de1c02' 'ca10f5' 'a503d003' '4c40fd' '4cb0fc')
DEFERRED_CODE = bytes.fromhex('ad0502c9ffd003' '4cb2fc' '6c0402')


def _off(address):
    return address - ORIGIN


def _put(image, address, expect, new):
    o = _off(address)
    if bytes(image[o:o + len(expect)]) != expect:
        raise AssemblyError('compat2 region differs from the reviewed bytes at %04X' % address)
    image[o:o + len(new)] = new


def compat2_image():
    parent, mapping = compat_image()
    image = bytearray(parent)
    _put(image, IMMEDIATE_JMP, bytes.fromhex('6c0202'), bytes.fromhex('4ce0fc'))
    _put(image, VBI_JSR_OPERAND, bytes.fromhex('f0fd'), bytes.fromhex('c0fd'))
    _put(image, DEFERRED_JMP, bytes.fromhex('6c0402'), bytes.fromhex('4ce0fd'))
    _put(image, IMMEDIATE_HELPER, b'\xff' * len(IMMEDIATE_CODE), IMMEDIATE_CODE)
    _put(image, TIMER_CLOCK, b'\xff' * len(TIMER_CODE), TIMER_CODE)
    _put(image, DEFERRED_HELPER, b'\xff' * len(DEFERRED_CODE), DEFERRED_CODE)
    data = bytes(image)
    added = len(IMMEDIATE_CODE) + len(TIMER_CODE) + len(DEFERRED_CODE)
    mapping = dict(mapping)
    symbols = dict(mapping['symbols'])
    symbols.update(vbi_immediate_default=IMMEDIATE_HELPER, vbi_timer_clock=TIMER_CLOCK, vbi_deferred_default=DEFERRED_HELPER)
    mapping.update(purpose='authored-compat2-awaiting-native-admission',
        sha256=hashlib.sha256(data).hexdigest(), symbols=symbols,
        used=mapping['used'] + added, remaining=mapping['remaining'] - added,
        parent_image_sha256=hashlib.sha256(parent).hexdigest(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        compat2=dict(timer_bytes='$021C..$021F decremented per frame when non-zero',
            ff_vector_policy='high byte $FF at $0203 -> system_vbi; at $0205 -> exit at $FCB2',
            source='consumer-observed software behaviour, not manufacturer firmware'))
    mapping['authored_capabilities'] = [*mapping['authored_capabilities'], 'compat-v2']
    return data, mapping


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    try:
        data, mapping = compat2_image()
    except AssemblyError as error:
        parser.error(str(error))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'compat2.bin').write_bytes(data)
    (args.output_dir / 'compat2-map.json').write_text(report_json(mapping))


if __name__ == '__main__':
    main()
