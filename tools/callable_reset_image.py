# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Callable-reset layout over the exact cart-owned diagnostic parent. No native admission inferred.

Consumer-observed requirement (a program's behaviour, not manufacturer bytes): some
cartridge software copies [reset-vector target, target+L) to RAM at $2100, patches an RTS
over the byte at target+L, and calls target+$0F as a hardware re-initialisation
subroutine. L is chosen by the byte at $FFF8: 0 -> $181, $32 -> $16B, anything else ->
$8A. This layout provides the $8A form: an instruction boundary at +$0F, a body that
only uses relative branches and absolute ROM/hardware operands, registers/flags set
for cartridge handoff before the end, and the cartridge JMP ($BFFE) at exactly +$8A."""
import argparse
import hashlib
from pathlib import Path
from emitter import AssemblyError, report_json
from cart_owned_diagnostic_image import cart_owned_diagnostic_image

PARENT_SHA256='5936e46d08c7991231a52dfb6c1a404a7a0d1ab505a51b2c5e09a569d7ad20e4'
ORIGIN=0xF800
RESET=0xFC00
ENTRY=0x0F          # re-initialisation entry offset from the reset target
END=0x8A            # fall-through offset; the cartridge handoff JMP lives here
REVISION_BYTE=0xFFF8


def _off(address):
    return address-ORIGIN


def callable_reset_image():
    parent,mapping=cart_owned_diagnostic_image()
    old=bytes(parent[_off(RESET):_off(RESET)+0x6E])
    if (hashlib.sha256(parent).hexdigest()!=PARENT_SHA256 or mapping['used']!=1556
        or mapping['symbols']['reset']!=RESET or old[-3:]!=bytes.fromhex('6cfebf')
        or parent[_off(RESET)+0x6E:_off(RESET)+0x80]!=b'\xff'*0x12
        or parent[_off(0xFC80):_off(0xFC89)]!=bytes.fromhex('4c80fc4c83fc4c86fc')
        or parent[_off(0xFC89):_off(0xFCA0)]!=b'\xff'*0x17
        or parent[_off(REVISION_BYTE)] not in range(256) or parent[_off(REVISION_BYTE)] in (0,0x32)):
        raise AssemblyError('callable reset requires the exact cart-owned parent and free handoff tail')
    # Parent body: SEI CLD LDX#FF TXS LDA#0, STA D40E, STA D400 (13 bytes), then the rest
    # of the init (from STA E80E) through JSR FD80; then CLC CLV LDY#0 LDX#0 LDA#0 JMP ($BFFE).
    prefix=old[:13]
    body=old[13:0x63]                      # STA E80E ... JSR $FD80, all relative/absolute-safe
    if prefix!=bytes.fromhex('78d8a2ff9aa9008d0ed48d00d4') or body[-3:]!=bytes.fromhex('2080fd'):
        raise AssemblyError('parent reset body differs from the reviewed sequence')
    tail=bytes.fromhex('18b8a000a200a900')  # CLC CLV LDY#0 LDX#0 LDA#0 (C=0 keeps BCC taken)
    code=bytearray(prefix+b'\xea\xea'+body+tail)   # two NOPs align the body at +$0F
    if len(code)+2>END:
        raise AssemblyError('re-initialisation body overruns the fall-through offset')
    code+=bytes([0x90,(END-(len(code)+2))&0xFF])    # BCC always taken -> +$8A
    startup_used=len(code)
    image=bytearray(parent)
    image[_off(RESET):_off(RESET)+0x80]=bytes(code)+b'\xff'*(0x80-len(code))
    image[_off(0xFC80):_off(0xFC89)]=parent[_off(0xFC80):_off(0xFC89)]
    image[_off(RESET+END):_off(RESET+END)+3]=bytes.fromhex('6cfebf')   # JMP ($BFFE)
    image[_off(0xFC80):_off(0xFC89)]=parent[_off(0xFC80):_off(0xFC89)]
    data=bytes(image)
    if (len(data)!=2048 or data[:_off(RESET)]!=parent[:_off(RESET)]
        or data[_off(0xFC8D):]!=parent[_off(0xFC8D):] or code[ENTRY-0:ENTRY+3]!=bytes.fromhex('8d0ee8')
        or data[_off(RESET+END):_off(RESET+END)+3]!=bytes.fromhex('6cfebf')):
        raise AssemblyError('callable reset changed bytes outside the reviewed region')
    mapping=dict(mapping)
    symbols=dict(mapping['symbols'])
    symbols.update(cart_handoff=RESET+END,reset_reinit=RESET+ENTRY)
    allocations=[dict(a) for a in mapping['allocations']]
    for a in allocations:
        if a['name']=='startup':
            a.update(used=startup_used,remaining=a['end']-a['start']-startup_used)
        if a['name']=='interrupts':
            a.update(used=a['used']+3,remaining=a['remaining']-3)
    mapping.update(purpose='authored-callable-reset-awaiting-native-admission',
        sha256=hashlib.sha256(data).hexdigest(),symbols=symbols,allocations=allocations,
        used=mapping['used']+(startup_used-110)+3,remaining=mapping['remaining']-(startup_used-110)-3,
        parent_image_sha256=PARENT_SHA256,parent_source_sha256=mapping['source_sha256'],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        reset_layout=dict(reset_target=RESET,reinit_entry_offset=ENTRY,fall_through_offset=END,
            revision_byte_address=REVISION_BYTE,revision_byte_value=parent[_off(REVISION_BYTE)],
            copy_length_for_revision_byte=END,handoff='JMP ($BFFE) at reset+$8A',
            registers_before_end='CLC CLV Y=0 X=0 A=0',nmi_enabled_by_runtime=False,
            source='consumer-observed software behaviour, not manufacturer firmware'),
        nominal_startup=dict(mapping['nominal_startup'],
            numeric_normal_cycles=764,numeric_boundary_cycles=771,
            ff_normal_cycles=745,ff_boundary_cycles=752,
            numeric_normal_instructions=260,numeric_boundary_instructions=263,
            ff_normal_instructions=251,ff_boundary_instructions=254,
            basis='parent plus 2 NOP and one taken same-page BCC; instructions traced natively +3, cycles static +7'))
    mapping['authored_capabilities']=[*mapping['authored_capabilities'],'callable-reset-v1']
    return data,mapping


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args()
    try:
        data,mapping=callable_reset_image()
    except AssemblyError as error:
        parser.error(str(error))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'callable-reset.bin').write_bytes(data)
    (args.output_dir/'callable-reset-map.json').write_text(report_json(mapping))


if __name__=='__main__':main()
