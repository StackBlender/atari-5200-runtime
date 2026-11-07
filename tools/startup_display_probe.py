# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Original Cold-to-progress/bitmap cartridges; no CPU execution engine."""
import argparse
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError, fixed_instruction
from cartridge_candidate import communication_area
from entry_probe import capture_fragment

LIST = 0x0800
BITMAP = 0x1000
RESULT = 0x3000
# Existing public service order; values are original diagnostic choices.
TRANSFERS = ((5,0xd402,0), (6,0xd403,8),
             (8,0xc012,0), (9,0xc013,0), (10,0xc014,0), (11,0xc015,0),
             (12,0xc016,6), (13,0xc017,10), (14,0xc018,14),
             (15,0xc019,0), (16,0xc01a,0), (7,0xd400,0x22))


def bitmap():
    # ORIGINAL geometric composition, logical 40x24 two-bit color selectors.
    result = bytearray()
    for y in range(24):
        row = []
        for x in range(40):
            color = (1 if x < 20 else 2) if y < 12 else (2 if x < 20 else 1)
            if 18 <= x < 22 and 10 <= y < 14:
                color = 0
            if (x,y) in ((4,4),(5,4),(4,5)) or x in (0,39) or y in (0,23):
                color = 3
            row.append(color)
        for x in range(0,40,4):
            result.append(sum(row[x+i] << (6-2*i) for i in range(4)))
    return bytes(result)


def startup_display_probe(board='Linear32K', entry=0x8000, control='direct', second_ff=False):
    if board not in ('Linear32K','Linear8K') or control not in ('direct','shadow'):
        raise AssemblyError('explicit board and direct/shadow control required')
    if type(entry) is not int or entry not in ((0x8000,) if board=='Linear32K' else (0x8000,0xa000)):
        raise AssemblyError('32K baseline entry8000; exact8K explicit8000/A000 alias required')
    if type(second_ff) is not bool:
        raise AssemblyError('second_ff must be bool')
    size = 32768 if board=='Linear32K' else 8192
    offset = entry-0x4000 if board=='Linear32K' else 0
    fragment,capture = capture_fragment(entry,RESULT)
    code = bytearray(fragment[:23])  # Own register capture; omit old self-loop.
    instructions = []
    def emit(mnemonic,mode='impl',operand=None):
        pc = entry+len(code)
        if mnemonic=='INC' and mode=='abs':
            encoded = bytes((0xee,operand&255,operand>>8))  # NMOS INC absolute.
        else:
            encoded = fixed_instruction(mnemonic,mode,operand)
        code.extend(encoded)
        instructions.append(dict(pc=pc,mnemonic=mnemonic,mode=mode,operand=operand))
    def store(address,value):
        emit('LDA','imm',value);emit('STA','abs',address)
    def bne(target):
        delta = target-(entry+len(code)+2)
        if not -128<=delta<=127:
            raise AssemblyError('original diagnostic branch overflow')
        instructions.append(dict(pc=entry+len(code),mnemonic='BNE',mode='rel',operand=target))
        code.extend((0xd0,delta&255))
    emit('SEI');emit('CLD')
    # Full Cold leaves no pending NMI. Disable sources during CPU-owned setup;
    # no vector changes, host events, RAM seeds or fixture suspension are used.
    for address in (0xd40e,0xe80e,0xd400,0xc01d,0xc01b,0xd404,0xd405):
        store(address,0)
    for address in (0x3006,0x3007,0x3008):
        store(address,0)
    store(0x3009,1 if control=='direct' else 2)
    # Every byte of the selected list and bitmap is initialized by actual CPU
    # instructions from original cartridge data before display is enabled.
    for table,target,count in ((entry+0x400,LIST,32),(entry+0x500,BITMAP,240)):
        emit('LDX','imm',0);loop=entry+len(code)
        emit('LDA','absx',table);emit('STA','absx',target)
        emit('INX');emit('CPX','imm',count);bne(loop)
    setup = entry+len(code)
    for shadow,register,value in TRANSFERS:
        emit('LDA','imm',value)
        emit('STA','abs' if control=='direct' else 'zp',register if control=='direct' else shadow)
    if control=='shadow':
        store(0xd40e,0x40)  # Ordinary default VBI, only AFTER all shadows/data.
    store(0x3008,0x5a)
    loop = entry+len(code)
    emit('INC','abs',0x3006)
    branch = entry+len(code)
    # Skip high-byte increment except when low byte wraps; never touch code PC.
    bne(branch+5)
    emit('INC','abs',0x3007)
    emit('JMP','abs',loop)
    if len(code)>0x400:
        raise AssemblyError('original diagnostic code overlaps ROM tables')
    display_list = bytes((0x70,0x70,0x70,0x48,0x00,0x10))+bytes((8,))*23+bytes((0x41,0x00,0x08))
    if len(display_list)!=32:
        raise AssemblyError('original display list size drift')
    image = bytearray(size)
    image[offset:offset+len(code)] = code
    image[offset+0x400:offset+0x420] = display_list
    pixels = bitmap()
    image[offset+0x500:offset+0x5f0] = pixels
    metadata = bytearray(communication_area('0'*20,'26',entry))
    if second_ff:
        metadata[20:22] = bytes((0,255))
    image[-24:] = metadata
    report = dict(schema=1,purpose='original-cold-startup-progress-geometric-bitmap-authoring',
        board=board,bytes=size,entry=entry,control=control,second_ff=second_ff,
        required_runtime=dict(
            source_revision=('e8f296d5a8fa693f13b5dd46259eafcb5567e88f' if board=='Linear32K'
                             else '2e8fd5152908e0c06d018d04bbfd9d07d1298703'),
            variant='cart-owned-diagnostic' if board=='Linear32K' else 'linear8k-guarded',
            image_sha256='5936e46d08c7991231a52dfb6c1a404a7a0d1ab505a51b2c5e09a569d7ad20e4',
            qualified_native_revision='138fad844c5c1877acd080bb7239b92d7e0bab9b' if board=='Linear32K' else None,
            new_native_guard_required=board=='Linear8K'),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        sha256=hashlib.sha256(image).hexdigest(),code_payload=[offset,offset+len(code)],
        code_cpu=[entry,entry+len(code)],first_opcode=[0x8d,0x00,0x30],
        setup_cpu=setup,progress_loop_cpu=loop,instructions_after_capture=instructions,
        capture_prefix_bytes=23,entry_capture_slots=capture['slots'],
        entry_capture_p_known_mask=capture['p_known_mask'],extra_stack_bytes=1,
        application_ram_write_windows=[[LIST,LIST+32],[BITMAP,BITMAP+240],[RESULT,RESULT+10]],
        public_shadow_writes=[] if control=='direct' else [t[0] for t in TRANSFERS],
        common_setup_mmio=[0xd40e,0xe80e,0xd400,0xc01d,0xc01b,0xd404,0xd405],
        ordered_display_writes=[dict(shadow=s,mmio=r,value=v) for s,r,v in TRANSFERS],
        counter=dict(low=0x3006,high=0x3007,initial=0,bits=16,commit='INC low; INC high iff low wraps'),
        ready=dict(address=0x3008,value=0x5a),control_marker=dict(address=0x3009,value=1 if control=='direct' else 2),
        display_list_ram=[LIST,LIST+32],display_list_rom_cpu=[entry+0x400,entry+0x420],
        bitmap_ram=[BITMAP,BITMAP+240],bitmap_rom_cpu=[entry+0x500,entry+0x5f0],
        metadata_cpu=[0xbfe8,0xc000],metadata_payload=[size-24,size],
        max_ordinary_returns=8,external_timeout_seconds=10,
        logical_pixels=[40,24],hardware_color_clock_pixel_width=4,scanlines_per_pixel=8,
        field_hires_pixels=[320,192],callback_origin=None,canonical_rgba_values=None,
        native_execution_verified=False,provider_approved=False,private_input_used=False,
        cpu_engine=False,reference_role=False,new_runtime_service=False)
    return bytes(image),report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--board',choices=('Linear32K','Linear8K'),required=True)
    parser.add_argument('--entry',type=lambda value:int(value,0),required=True)
    parser.add_argument('--control',choices=('direct','shadow'),required=True)
    parser.add_argument('--second-ff',action='store_true')
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    try:
        data,report=startup_display_probe(args.board,args.entry,args.control,args.second_ff)
    except AssemblyError as error:
        parser.error(str(error))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'original-startup-display.bin').write_bytes(data)
    (args.output_dir/'original-startup-display.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')


if __name__=='__main__':main()
