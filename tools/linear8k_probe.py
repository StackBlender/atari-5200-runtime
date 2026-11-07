# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""ORIGINAL exact8192 CPU diagnostic layout; native admission still required."""
import argparse
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError,fixed_instruction
from entry_probe import capture_fragment
from cartridge_candidate import communication_area

READS=(0x4000,0x7fff,0x8000,0x8100,0x9100,0x9fe7,0x9fe8,0x9fff,
       0xa000,0xa100,0xb100,0xbfe7,0xbfe8,0xbfff)


def original_linear8k_probe(entry=0xa000,second_ff=False):
    if type(entry) is not int or entry not in (0x8000,0xa000) or type(second_ff) is not bool:
        raise AssemblyError('original8K probe requires explicit8000/A000 alias entry and bool year policy')
    fragment,capture=capture_fragment(entry,0x3000)
    code=bytearray(fragment[:23]) # own capture stores only; omit old self-loop
    def emit(mnemonic,mode='impl',operand=None):
        code.extend(fixed_instruction(mnemonic,mode,operand))
    emit('SEI')
    for address in (0xd40e,0xe80e,0):
        emit('LDA','imm',0);emit('STA','abs',address)
    for index,address in enumerate(READS):
        emit('LDA','abs',address);emit('STA','abs',0x3010+index)
    emit('LDX','imm',0);loop=len(code)
    for address,target in ((0x9fe8,0x3040),(0xbfe8,0x3060)):
        emit('LDA','absx',address);emit('STA','absx',target)
    emit('INX');emit('CPX','imm',24)
    delta=loop-(len(code)+2)
    if not -128<=delta<=127:raise AssemblyError('original metadata loop branch overflow')
    code.extend((0xd0,delta&255))
    emit('LDA','imm',0x5a);emit('STA','abs',0x3006)
    halt=entry+len(code);emit('JMP','abs',halt)
    if len(code)>0x100:raise AssemblyError('original8K probe overlaps first marker')
    image=bytearray(8192);image[:len(code)]=code
    image[0x100]=0x35;image[0x1100]=0xa7;image[0x1fe7]=0x6d
    metadata=bytearray(communication_area('0'*20,'26',entry))
    if second_ff:metadata[20:22]=bytes((0,255))
    image[0x1fe8:]=metadata
    data=bytes(image)
    reads=[]
    for index,address in enumerate(READS):
        offset=None if address<0x8000 else (address-0x8000)%8192
        reads.append(dict(cpu_address=address,result_address=0x3010+index,
            payload_offset=offset,expected=None if offset is None else data[offset],
            kind='native-open-bus-observation-required' if offset is None else 'declared-ROM-alias'))
    report=dict(schema=1,purpose='original-exact8192-mapping-probe-awaiting-native-admission',
        bytes=8192,sha256=hashlib.sha256(data).hexdigest(),declared_board='Linear8K',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        entry=entry,code_bytes=len(code),first_opcode=data[0],halt_cpu=halt,
        metadata_cpu=[0xbfe8,0xc000],metadata_payload=[0x1fe8,0x2000],
        metadata_alias_cpu=[0x9fe8,0xa000],metadata_expected=list(metadata),
        entry_capture_slots=capture['slots'],entry_capture_prefix_bytes=23,
        entry_capture_p_known_mask=capture['p_known_mask'],entry_capture_extra_stack=1,
        result_windows=[[0x3000,0x3007],[0x3010,0x3010+len(READS)],
                        [0x3040,0x3058],[0x3060,0x3078]],
        mapping_complete=dict(address=0x3006,value=0x5a),reads=reads,
        native_execution_verified=False,private_input_used=False,
        cpu_engine=False,open_bus_value_assumed=False,reference_role=False)
    return data,report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entry',type=lambda value:int(value,0),default=0xa000)
    parser.add_argument('--second-ff',action='store_true')
    parser.add_argument('--output-dir',required=True,type=Path);args=parser.parse_args()
    try:data,report=original_linear8k_probe(args.entry,args.second_ff)
    except AssemblyError as error:parser.error(str(error))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'original-linear8k.bin').write_bytes(data)
    (args.output_dir/'original-linear8k.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')


if __name__=='__main__':main()
