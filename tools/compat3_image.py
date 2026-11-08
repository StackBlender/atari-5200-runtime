# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Compatibility generation 3 over compat-v2. No native admission inferred.

Two robustness behaviours (software expectations, not manufacturer bytes):
 1. A keyboard ($0208) or break ($020C) vector whose high byte is $FF means "no handler":
    the interrupt is acknowledged (already done by the classifier) and returned from
    instead of jumping into the unmapped $FFxx range.
 2. An interrupt source the runtime does not service (serial and any other pending enabled
    source that is not a timer, break or keyboard) is acknowledged and dropped instead of
    parking in the fault loop: IRQEN is cleared and POKMSK written back, registers restored,
    RTI. Faults remain for non-IRQ failures. Timer services (compat-v2 lineage) are unchanged.
New code sits in previously erased reserve space."""
import argparse
import hashlib
from pathlib import Path
from emitter import AssemblyError, report_json
from compat2_image import compat2_image
from callable_reset_image import ORIGIN

KEY_STUB_AT = 0xFC8D      # old default-or-custom check; now jumps to the new check
OLD_KEY_ENTRY = bytes.fromhex('ad090209' '01c9fdd0034c20ff' '6c0802')
KEYV_AT = 0xFF4C
KEYV = bytes.fromhex('ad0902' 'c9ff' 'f00c' '0901' 'c9fd' 'd003' '4c20ff' '6c0802' '6840')
BRKV_AT = 0xFF61
BRKV = bytes.fromhex('ad0d02' 'c9ff' 'd002' '6840' '6c0c02')
DROP_AT = 0xFF6D
DROP = bytes.fromhex('a9008d0ee8' 'a5008d0ee8' '68a868aa6840')
SPLIT_BREAK_AT = 0xFCF9   # last instruction of the split code: JMP ($020C)
CLASSIFIER_FAULT_AT = 0xFF05   # JMP $FC83 (fault) when no break/key source
CLASSIFIER_OLD_FAULT = bytes.fromhex('4c83fc')


def _off(address):
    return address - ORIGIN


def _put(image, address, expect, new):
    o = _off(address)
    if bytes(image[o:o + len(expect)]) != expect:
        raise AssemblyError('compat3 region differs from the reviewed bytes at %04X' % address)
    image[o:o + len(new)] = new


def compat3_image():
    parent, mapping = compat2_image()
    image = bytearray(parent)
    _put(image, KEYV_AT, b'\xff' * (len(KEYV) + len(BRKV) + len(DROP)), KEYV + BRKV + DROP)
    _put(image, KEY_STUB_AT, OLD_KEY_ENTRY, bytes.fromhex('4c4cff') + b'\xff' * (len(OLD_KEY_ENTRY) - 3))
    _put(image, SPLIT_BREAK_AT, bytes.fromhex('6c0c02'), bytes.fromhex('4c61ff'))
    _put(image, CLASSIFIER_FAULT_AT, CLASSIFIER_OLD_FAULT, bytes.fromhex('4c6dff'))
    data = bytes(image)
    added = len(KEYV) + len(BRKV) + len(DROP) - (len(OLD_KEY_ENTRY) - 3)
    mapping = dict(mapping)
    symbols = dict(mapping['symbols'])
    symbols.update(irq_key_vector_check=KEYV_AT, irq_break_vector_check=BRKV_AT, irq_drop_unsupported=DROP_AT)
    mapping.update(purpose='authored-compat3-awaiting-native-admission',
        sha256=hashlib.sha256(data).hexdigest(), symbols=symbols,
        used=mapping['used'] + added, remaining=mapping['remaining'] - added,
        parent_image_sha256=hashlib.sha256(parent).hexdigest(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        compat3=dict(ff_key_break_vectors='high byte $FF at $0209/$020D -> acknowledge and return',
            unsupported_irq_sources='acknowledged and dropped (IRQEN 0 then POKMSK), registers restored, RTI',
            source='consumer-observed software behaviour, not manufacturer firmware'))
    mapping['authored_capabilities'] = [*mapping['authored_capabilities'], 'compat-v3']
    return data, mapping


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    try:
        data, mapping = compat3_image()
    except AssemblyError as error:
        parser.error(str(error))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'compat3.bin').write_bytes(data)
    (args.output_dir / 'compat3-map.json').write_text(report_json(mapping))


if __name__ == '__main__':
    main()
