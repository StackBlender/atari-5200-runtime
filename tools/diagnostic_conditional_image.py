# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""B2: secondFF admits any first year; otherwise both numeric, full cold retained."""
import hashlib
from pathlib import Path
from emitter import AssemblyError,Image,Region
from diagnostic_cold_image import diagnostic_cold_image

PARENT_REVISION='becb92e01e97e89568cac58ab051e23b803ae53a'
PARENT_SHA256='9da1ddefb339dc2ef3f93643d33b45021099d3fd3256ce1f9754f32787e6b69f'


def metadata_fragment():
    image=Image([Region('prefix',0xf800,0xfd80,'reserved'),
        Region('metadata',0xfd80,0xfdc0,'code'),Region('suffix',0xfdc0,0xfffa,'reserved'),
        Region('tool-vectors',0xfffa,0x10000,'vectors')])
    image.org(0xfd80);image.label('conditional_metadata');emit=image.instruction
    # Test SECOND first: FF is the only route bypassing FIRST numeric checks.
    emit('LDA','abs',0xbffd);emit('CMP','imm',0xff);emit('BEQ','rel','conditional_entry_check')
    emit('CMP','imm',0x50);emit('BCC','rel','conditional_invalid')
    emit('CMP','imm',0x5a);emit('BCS','rel','conditional_invalid')
    emit('LDA','abs',0xbffc);emit('CMP','imm',0x50);emit('BCC','rel','conditional_invalid')
    emit('CMP','imm',0x5a);emit('BCS','rel','conditional_invalid')
    image.label('conditional_entry_check')
    emit('LDA','abs',0xbfff);emit('CMP','imm',0x40);emit('BCC','rel','conditional_invalid')
    emit('CMP','imm',0xc0);emit('BCS','rel','conditional_invalid')
    emit('CMP','imm',0xbf);emit('BNE','rel','conditional_valid')
    emit('LDA','abs',0xbffe);emit('CMP','imm',0xe8);emit('BCS','rel','conditional_invalid')
    image.label('conditional_valid');emit('RTS')
    image.label('conditional_invalid');emit('JMP','abs',0xfc86)
    end=image.pc;image.vectors(nmi='conditional_metadata',reset='conditional_metadata',irq='conditional_metadata')
    data,report=image.finish();return data[0x580:end-0xf800],report['symbols']


def diagnostic_conditional_image():
    parent,mapping=diagnostic_cold_image();fragment,symbols=metadata_fragment()
    if (len(parent)!=2048 or hashlib.sha256(parent).hexdigest()!=PARENT_SHA256 or
        mapping['used']!=1556 or mapping['remaining']!=492 or
        mapping['symbols']['validate_metadata']!=0xfd80 or
        parent[0x460:0x463]!=bytes.fromhex('2080fd') or
        parent[0x700:0x7fa]!=b'\xff'*250 or len(fragment)!=52 or
        fragment[26:]!=parent[0x59a:0x5b4]):
        raise AssemblyError('B2 requires exact52byte B1 validator/fit/entry/reserve')
    data=bytearray(parent);data[0x580:0x5b4]=fragment
    mapping['symbols'].update(symbols)
    mapping.update(purpose='authored-conditional-year-full-cold-awaiting-execution',
        target='ntsc-four-port-diagnostic-conditional-development',
        sha256=hashlib.sha256(data).hexdigest(),
        parent_source_revision=PARENT_REVISION,parent_image_sha256=PARENT_SHA256,
        parent_source_sha256=mapping['source_sha256'],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        metadata_policy=dict(title_bytes=20,title='opaque',
            numeric_year_min=80,numeric_year_max=89,second_year_alternative=255,
            first_year_rule='any-byte-if-and-only-if-second-FF-otherwise-numeric',
            ff_changes='admission-only-full-cold-initialization-retained',historical_bypass=False,
            entry_min=0x4000,entry_max=0xbfe7),
        nominal_startup=dict(numeric_normal_cycles=757,numeric_boundary_cycles=764,
            ff_normal_cycles=738,ff_boundary_cycles=745,
            numeric_normal_instructions=257,numeric_boundary_instructions=260,
            ff_normal_instructions=248,ff_boundary_instructions=251,
            numeric_metadata_prefix_cycles=28,ff_metadata_prefix_cycles=9,
            timer_metadata_prefix_cycles=419))
    mapping['authored_capabilities']=[*mapping['authored_capabilities'],'diagnostic-conditional-year-v1']
    return bytes(data),mapping
