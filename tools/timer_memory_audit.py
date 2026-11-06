# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Conditional static operand/control-flow audit of OUR exact timer program.

No registers, RAM, flags, chips, timing or instructions are executed/simulated.
Consumer callbacks and core power randomization are explicit external boundaries.
"""
import argparse
import hashlib
import json
from pathlib import Path

TIMER_SHA256='eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550'
ORIGIN=0xf800


class AuditError(ValueError):pass


# Independent narrow factual decoder, not imported from an emitter/test/model.
# Each tuple: mnemonic, mode, length, memory/control-flow class.
OPS={
    0x78:('SEI','impl',1,None),0xd8:('CLD','impl',1,None),
    0xa2:('LDX','imm',2,None),0x9a:('TXS','impl',1,None),
    0xa9:('LDA','imm',2,None),0xa0:('LDY','imm',2,None),
    0x8d:('STA','abs',3,'write'),0x95:('STA','zpx',2,'write_x'),
    0x85:('STA','zp',2,'write'),0xca:('DEX','impl',1,None),
    0xe8:('INX','impl',1,None),0xe0:('CPX','imm',2,None),
    0x10:('BPL','rel',2,'branch'),0xd0:('BNE','rel',2,'branch'),
    0xf0:('BEQ','rel',2,'branch'),0x90:('BCC','rel',2,'branch'),
    0xb0:('BCS','rel',2,'branch'),0x20:('JSR','abs',3,'call'),
    0x18:('CLC','impl',1,None),0xb8:('CLV','impl',1,None),
    0x6c:('JMP','ind',3,'indirect'),0x4c:('JMP','abs',3,'jump'),
    0x48:('PHA','impl',1,'push'),0x68:('PLA','impl',1,'pull'),
    0x8a:('TXA','impl',1,None),0x98:('TYA','impl',1,None),
    0xa8:('TAY','impl',1,None),0xaa:('TAX','impl',1,None),
    0xba:('TSX','impl',1,None),0x40:('RTI','impl',1,'return'),
    0x60:('RTS','impl',1,'return'),0xad:('LDA','abs',3,'read'),
    0xbd:('LDA','absx',3,'read_x'),0xa5:('LDA','zp',2,'read'),
    0xe6:('INC','zp',2,'rmw'),0x25:('AND','zp',2,'read'),
    0x29:('AND','imm',2,None),0xc9:('CMP','imm',2,None),
    0x49:('EOR','imm',2,None),
    0x9d:('STA','absx',3,'write_x'),
}
DEFAULTS={0x200:0xfe00,0x202:0xfca0,0x204:0xfcb0,0x206:0xfc86,
          0x20e:0xfc86,0x216:0xfc86,0x218:0xfc86,0x21a:0xfc86}
MMIO_WRITES={0xd40e,0xd400,0xe80e,0xe80f,0xe801,0xe803,0xe805,0xe807,
    0xc01d,0xc01b,0xc01a,0xd401,0xd409,0xd40f,0xc01f,0xe80b,0xd402,0xd403,
    *range(0xc012,0xc01b)}


def require(condition,message):
    if not condition:raise AuditError(message)


def ranges(values):
    result=[]
    for value in sorted(set(values)):
        if result and value==result[-1][1]+1:result[-1][1]=value
        else:result.append([value,value])
    return result


def _analyze(data):
    require(type(data) is bytes and len(data)==2048,'expected one2048-byte original image')
    def at(address,length):return data[address-ORIGIN:address-ORIGIN+length]
    # Finite-loop proofs are conditional on these exact byte patterns. They do
    # not infer arbitrary X bounds or execute a data-flow/CPU interpreter.
    for address,encoded in (
        (0xfc37,'a2189500ca10fb'),
        (0xfc3e,'a200a9869d0002e8a9fc9d0002e8e01cd0f0'),
        (0xfeb0,'a200bde8bfc9509020c95ab01ce8e016d0f0'),
        (0xfedc,'a9a08d0202a9fc8d0302a9b08d0402a9fc8d0502a9008d0002a9fe8d010260'),
    ):
        expected=bytes.fromhex(encoded)
        require(at(address,len(expected))==expected,'startup index/default-vector proof guard changed')
    vectors=[int.from_bytes(data[offset:offset+2],'little') for offset in (2042,2044,2046)]
    require(vectors==[0xfcc0,0xfc00,0xfd00],'hardware entry vectors changed')
    pending=list(vectors);records={};occupied=set();reads=set();writes=set()
    frontiers=set();edges=[]
    while pending:
        pc=pending.pop()
        if pc in records:continue
        require(0xfc00<=pc<0xff00,'control flow leaves own emitted code')
        require(pc not in occupied,'control flow enters instruction operand')
        opcode=at(pc,1)[0]
        require(opcode in OPS,'unknown/unapproved opcode')
        mnemonic,mode,length,kind=OPS[opcode]
        require(pc+length<=0xff00,'truncated instruction')
        span=set(range(pc,pc+length))
        require(not span&occupied,'overlapping instruction decode')
        occupied.update(span)
        operand=int.from_bytes(at(pc+1,length-1),'little')
        footprint=set();next_pc=pc+length
        if kind in {'read','write','rmw'}:footprint={operand}
        elif kind in {'read_x','write_x'}:
            if pc==0xfc39 and mode=='zpx' and operand==0:
                footprint=set(range(0x19))
            elif pc in (0xfc42,0xfc48) and mode=='absx' and operand==0x200:
                start=0 if pc==0xfc42 else 1
                footprint={0x200+x for x in range(start,0x1c,2)}
            elif pc==0xfeb2 and kind=='read_x' and operand==0xbfe8:
                footprint=set(range(0xbfe8,0xbffe))
            elif pc==0xfd07 and kind=='read_x' and operand==0x100:
                footprint=set(range(0x100,0x200))
            else:raise AuditError('indexed access lacks exact bounded-loop/stack proof')
        if kind in {'read','read_x','rmw'}:reads.update(footprint)
        if kind in {'write','write_x','rmw'}:
            for address in footprint:
                require(address<0x19 or 0x200<=address<0x21c or address in MMIO_WRITES,
                        'runtime store outside declared shadows/vectors/MMIO')
            writes.update(footprint)
        successors=[]
        if kind=='branch':
            displacement=operand if operand<128 else operand-256
            successors=[next_pc,next_pc+displacement]
        elif kind=='call':
            require((pc,operand) in {(0xfc50,0xfedc),(0xfc60,0xfeb0)},'unreviewed runtime call')
            successors=[next_pc,operand]
        elif kind=='jump':successors=[operand]
        elif kind=='indirect':
            require(operand in DEFAULTS or operand==0xbffe,'unknown indirect pointer')
            reads.update((operand,operand+1));frontiers.add(operand)
            if operand in DEFAULTS:successors=[DEFAULTS[operand]]
        elif kind!='return':successors=[next_pc]
        for target in successors:edges.append([pc,target])
        pending.extend(successors)
        records[pc]=dict(pc=pc,mnemonic=mnemonic,mode=mode,operand=operand,
                        access=kind,operand_ranges=ranges(footprint))
    require(len(occupied)==474,'not all474 emitted code bytes covered')
    require(all((a in occupied or data[a-ORIGIN]==0xff)
                for a in range(0xfc00,0xff00)),'unvisited nonpadding code')
    # Hardware interrupt entry, PHA and JSR can only address the NMOS stack page.
    reads.update(range(0x100,0x200));writes.update(range(0x100,0x200))
    require(not any(0x21c<=a<0x4000 for a in reads|writes),'application RAM operand found')
    require(not any(0x19<=a<0x1d for a in reads|writes),'cc65 conio operand found')
    return dict(schema=1,purpose='conditional-static-original-timer-memory-audit',
        execution_verified=False,ordinary_profile_approved=False,
        image_sha256=hashlib.sha256(data).hexdigest(),instruction_count=len(records),
        code_bytes_covered=len(occupied),ram_read_ranges=ranges(a for a in reads if a<0x4000),
        ram_write_ranges=ranges(a for a in writes if a<0x4000),
        mmio_write_addresses=sorted(a for a in writes if a>=0x4000),
        application_operand_accesses=[],cc65_conio_operand_accesses=[],
        implicit_stack_page=[0x100,0x1ff],software_pointer_frontiers=sorted(frontiers),
        external_boundaries=['consumer callback/cart code','core cold power/randomization',
                             'chip DMA/bus dummy cycles','callback stack balance/depth'],
        conditional_loop_bounds={'zero_page':[0,24],'vector_even_x':[0,26],
            'vector_odd_x':[1,27],'metadata_x':[0,21],'stack_x':[0,255]},
        edges=sorted(edges),instructions=[records[pc] for pc in sorted(records)])


def audit(data):
    require(type(data) is bytes and hashlib.sha256(data).hexdigest()==TIMER_SHA256,
            'only the exact qualified original timer image is admitted')
    return _analyze(data)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image',type=Path)
    args=parser.parse_args()
    try:report=audit(args.image.read_bytes())
    except (OSError,AuditError) as error:parser.exit(2,str(error)+'\n')
    print(json.dumps(report,sort_keys=True,indent=2))


if __name__=='__main__':main()
