# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""B1: original full-cold policy; first year ALWAYS numeric, second may beFF."""
import hashlib
from pathlib import Path
from emitter import AssemblyError,Image,Region
from timer_experiment import PARENT_REVISION,PARENT_SHA256,parent_image


def metadata_fragment():
    # Use OUR assembler, discard its tool-only vector roots. Not a CPU model.
    image=Image([Region('prefix',0xf800,0xfd80,'reserved'),
        Region('metadata',0xfd80,0xfdc0,'code'),Region('suffix',0xfdc0,0xfffa,'reserved'),
        Region('tool-vectors',0xfffa,0x10000,'vectors')])
    image.org(0xfd80);image.label('diagnostic_metadata');emit=image.instruction
    emit('LDA','abs',0xbffc);emit('CMP','imm',0x50);emit('BCC','rel','diagnostic_invalid')
    emit('CMP','imm',0x5a);emit('BCS','rel','diagnostic_invalid')
    emit('LDA','abs',0xbffd);emit('CMP','imm',0xff);emit('BEQ','rel','diagnostic_entry_check')
    emit('CMP','imm',0x50);emit('BCC','rel','diagnostic_invalid')
    emit('CMP','imm',0x5a);emit('BCS','rel','diagnostic_invalid')
    image.label('diagnostic_entry_check')
    emit('LDA','abs',0xbfff);emit('CMP','imm',0x40);emit('BCC','rel','diagnostic_invalid')
    emit('CMP','imm',0xc0);emit('BCS','rel','diagnostic_invalid')
    emit('CMP','imm',0xbf);emit('BNE','rel','diagnostic_valid')
    emit('LDA','abs',0xbffe);emit('CMP','imm',0xe8);emit('BCS','rel','diagnostic_invalid')
    image.label('diagnostic_valid');emit('RTS')
    image.label('diagnostic_invalid');emit('JMP','abs',0xfc86)
    end=image.pc;image.vectors(nmi='diagnostic_metadata',reset='diagnostic_metadata',irq='diagnostic_metadata')
    data,report=image.finish();return data[0x580:end-0xf800],report['symbols']


def diagnostic_cold_image():
    parent,mapping=parent_image();fragment,symbols=metadata_fragment()
    if (len(fragment)!=52 or parent[0x460:0x463]!=bytes.fromhex('20b0fe') or
        mapping['symbols']['cart_handoff']!=0xfc6b or parent[0x580:0x5b4]!=b'\xff'*52):
        raise AssemblyError('reviewed free input block/metadata JSR/handoff differs')
    data=bytearray(parent);data[0x461:0x463]=bytes.fromhex('80fd');data[0x580:0x5b4]=fragment
    mapping['symbols']['legacy_validate_metadata']=mapping['symbols']['validate_metadata']
    mapping['symbols']['validate_metadata']=0xfd80;mapping['symbols'].update(symbols)
    for region in mapping['allocations']:
        if region['name']=='input':region['used']+=52;region['remaining']-=52
    mapping.update(purpose='authored-diagnostic-full-cold-awaiting-execution',
        target='ntsc-four-port-diagnostic-cold-development',
        sha256=hashlib.sha256(data).hexdigest(),used=1556,remaining=492,
        parent_source_revision=PARENT_REVISION,parent_image_sha256=PARENT_SHA256,
        parent_source_sha256=mapping['source_sha256'],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        ownership_policy='unchanged-conservative-timer-parent-through021F-no-B0-cession',
        metadata_policy=dict(title_bytes=20,title='opaque',first_year_min=80,first_year_max=89,
            second_year_min=80,second_year_max=89,second_year_alternative=255,
            ff_changes='admission-only-full-cold-initialization-retained',historical_bypass=False,
            entry_min=0x4000,entry_max=0xbfe7),
        nominal_startup=dict(numeric_normal_cycles=757,numeric_boundary_cycles=764,
            ff_normal_cycles=750,ff_boundary_cycles=757,
            numeric_normal_instructions=257,numeric_boundary_instructions=260,
            ff_normal_instructions=253,ff_boundary_instructions=256,
            numeric_metadata_prefix_cycles=28,ff_metadata_prefix_cycles=21,
            parent_metadata_prefix_cycles=419))
    mapping['authored_capabilities']=[*mapping['authored_capabilities'],'diagnostic-full-cold-v1']
    return bytes(data),mapping
