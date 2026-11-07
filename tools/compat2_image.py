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
 3. Keyboard and break interrupts. A pending break source (IRQST bit 7) or keyboard source
    (bit 6) is acknowledged (IRQEN disable, POKMSK restore) and X/Y are restored so only A is
    on the stack. Break goes to ($020C). Keyboard goes to ($0208) when software installed its
    own handler; the default value is $FC.. or $FD.. (the table value or the observed
    BIOS-internal default), which selects a default routine (FF20) that pushes X/Y, converts
    KBCODE bits 4..1 to a key value in A (digits 0..9, $0A '*', $0B '#', $0C Start, $0D
    Pause, $0E Reset; layout observed, numbering consumer-inferred) and calls ($020A) with the
    full frame, or exits at $FCB2 when $020A is unset (high byte $00 or $FF). Other sources fault.
 4. Software restores the IRQ vector to $FC03 as a default value; $FC03 now is JMP $FE00.
    Reset entry becomes JMP $FC74 (SEI CLD LDX #$FF TXS, JMP $FC06) so the first 15 bytes no
    longer need to be executed in order; the callable-reset boundary at +$0F is unchanged.
 5. Software copies its default vectors from a table in BIOS space ($FE95, six vectors:
    IRQ $FC03, immediate VBI $FCB8, deferred VBI $FCB2 exit, DLI $FCDD RTI, keyboard
    $FC8D default check, keyboard deferred $FCB2 exit); the table now exists.
 Known gap: a $FFFF key/break vector set explicitly by software is still jumped to.
 No other behaviour changes; new code sits in previously erased space and the head of the former reserve."""
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
KEY_ENTRY_AT = 0xFC8D     # default-or-custom check for the keyboard immediate vector
KEY_ENTRY = bytes.fromhex('ad090209' '01c9fdd0034c20ff' '6c0802')
KEY_CODE_AT = 0xFF20      # default keyboard routine: key value in A, full frame, JMP ($020A) unless unset
KEY_CODE = bytes.fromhex('8a489848' 'ad09e84a290faa' 'bd3cff' 'ae0b02f008e8f005' '6c0a02' '4cb2fc')
KEY_TABLE_AT = 0xFF3C
KEY_TABLE = bytes.fromhex('0f0b000a0e090807' '0d0605040c030201')
OLD_CLOCK_AT = 0xFDF0
OLD_CLOCK = bytes.fromhex('e602d002e601a503d0034c40fd4cb0fc')   # unreachable since system_vbi was redirected; erased
RESET_AT = 0xFC00
RESET_OLD = bytes.fromhex('78d8a2ff9aa9008d0ed48d00d4eaea')
RESET_NEW = bytes.fromhex('4c74fc' '4c00fe' 'a9008d0ed48d00d4ea')
RESET_STUB_AT = 0xFC74
RESET_STUB = bytes.fromhex('78d8a2ff9a' '4c06fc')
SOURCE_AT = 0xFF00     # first bytes of the former reserve
SOURCE_CODE = bytes.fromhex('8a29c0d0034c83fc' '8a3005' 'a9bf18' '9003' 'a97f38' '25008d0ee8a5008d0ee8' '4cf0fc')
FAULT_JUMP_AT = 0xFE4D  # the unsupported-source fault jump; redirected to the classifier
VECTOR_TABLE_AT = 0xFE95
VECTOR_TABLE = bytes.fromhex('03fc' 'b8fc' 'b2fc' 'ddfc' '8dfc' 'b2fc')
SPLIT_AT = 0xFCF0
SPLIT_CODE = bytes.fromhex('68a868aa' 'b003' '4c8dfc' '6c0c02')   # restore X/Y, break -> ($020C), key -> $FC8D


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
    _put(image, FAULT_JUMP_AT, bytes.fromhex('4c83fc'), bytes.fromhex('4c00ff'))
    _put(image, VECTOR_TABLE_AT, b'\xff' * len(VECTOR_TABLE), VECTOR_TABLE)
    _put(image, SOURCE_AT, b'\xff' * len(SOURCE_CODE), SOURCE_CODE)
    _put(image, SPLIT_AT, b'\xff' * len(SPLIT_CODE), SPLIT_CODE)
    _put(image, KEY_ENTRY_AT, b'\xff' * len(KEY_ENTRY), KEY_ENTRY)
    _put(image, KEY_CODE_AT, b'\xff' * len(KEY_CODE), KEY_CODE)
    _put(image, KEY_TABLE_AT, b'\xff' * len(KEY_TABLE), KEY_TABLE)
    _put(image, OLD_CLOCK_AT, OLD_CLOCK, b'\xff' * len(OLD_CLOCK))
    _put(image, RESET_STUB_AT, b'\xff' * len(RESET_STUB), RESET_STUB)
    _put(image, RESET_AT, RESET_OLD, RESET_NEW)
    data = bytes(image)
    added = (len(IMMEDIATE_CODE) + len(TIMER_CODE) + len(DEFERRED_CODE) + len(SOURCE_CODE)
             + len(SPLIT_CODE) + len(KEY_CODE) + len(KEY_ENTRY) + len(RESET_STUB) + len(VECTOR_TABLE)
             + len(KEY_TABLE) - len(OLD_CLOCK))
    mapping = dict(mapping)
    symbols = dict(mapping['symbols'])
    symbols.update(vbi_immediate_default=IMMEDIATE_HELPER, vbi_timer_clock=TIMER_CLOCK, vbi_deferred_default=DEFERRED_HELPER,
        irq_source_classifier=SOURCE_AT, irq_key_default=KEY_CODE_AT, irq_key_check=KEY_ENTRY_AT, key_value_table=KEY_TABLE_AT, irq_default_entry=0xFC03, default_vector_table=VECTOR_TABLE_AT)
    mapping.update(purpose='authored-compat2-awaiting-native-admission',
        sha256=hashlib.sha256(data).hexdigest(), symbols=symbols,
        used=mapping['used'] + added, remaining=mapping['remaining'] - added,
        parent_image_sha256=hashlib.sha256(parent).hexdigest(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        compat2=dict(timer_bytes='$021C..$021F decremented per frame when non-zero',
            ff_vector_policy='high byte $FF at $0203 -> system_vbi; at $0205 -> exit at $FCB2',
            key_irq='bit 6 -> ack, A=key value 0..9,$0A * ,$0B #,$0C Start,$0D Pause,$0E Reset, full frame, JMP ($020A)',
            break_irq='bit 7 -> ack, A-only frame, JMP ($020C)',
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
