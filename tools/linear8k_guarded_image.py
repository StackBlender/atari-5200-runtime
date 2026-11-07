# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Byte-identical combined CPU image; NEW required native Linear8K guard."""
import copy
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError
from cart_owned_diagnostic_image import cart_owned_diagnostic_image

ROOT=Path(__file__).resolve().parents[1]
PARENT_REVISION='e8f296d5a8fa693f13b5dd46259eafcb5567e88f'
PARENT_IMAGE='5936e46d08c7991231a52dfb6c1a404a7a0d1ab505a51b2c5e09a569d7ad20e4'
PARENT_CONTRACT='f287bfc766c3e13973464b2219762cdc2249180ec9c54d5bd5555e1be0be5cb9'
PROFILE='ntsc-four-port-cart-owned-linear8k-guarded-development'
MAPPER=dict(board='Linear8K',program_size=8192,successful_load_required=True)
GUARD={
 'schema':1,'id':'linear8k-immutable-entry-guard-v1',
 'immutable_loaded_board':'Linear8K','exact_program_size':8192,
 'canonical_metadata_cpu':[0xbfe8,0xc000],'canonical_metadata_payload':[0x1fe8,0x2000],
 'canonical_entry_cpu':[0xbffe,0xc000],'canonical_entry_payload':[0x1ffe,0x2000],
 'entry_endian':'little','entry_read_source':'immutable-readonly-board-peeks',
 'allowed_entry_cpu':[[0x8000,0x9fe8],[0xa000,0xbfe8]],
 'open_bus_cpu':[[0x4000,0x8000]],'metadata_alias_cpu':[[0x9fe8,0xa000],[0xbfe8,0xc000]],
 'intervals':'half-open','pre_mutation_routes':['cold','system-power','state-import'],
 'validate_actual_loaded_board_and_length':True,
 'entry_rejection_stage':'before-power-randomization-cache-or-import-mutation',
 'entry_rejection_classification':'pre-power-entry',
 'handoff_guard_stage':'before-ready-and-first-application-opcode',
 'actual_handoff_equals_immutable_entry':True,'actual_handoff_in_allowed_entry':True,
 'pending_nmi_refusal_retained':True,'cpu_cheat_hook_overlay_negative_required':True,
 'cheats_overlays_live_configuration_supported':False,'failure_action':'refuse-or-fault-never-patch-pc',
 'cpu_full_cold_and_year_validator_retained':True,
 'additional_emulated_ram_bytes':0,'additional_stack_bytes':0,
 'additional_helper_calls':0,'additional_native_payload_fields':0}


def linear8k_guarded_image():
    data,mapping=cart_owned_diagnostic_image()
    if (len(data)!=2048 or hashlib.sha256(data).hexdigest()!=PARENT_IMAGE or
        mapping['used']!=1556 or mapping['remaining']!=492 or data[0x700:0x7fa]!=b'\xff'*250 or
        mapping['target']!='ntsc-four-port-cart-owned-diagnostic-conditional-development'):
        raise AssemblyError('Linear8K requires exact unchanged combined parent')
    try:
        old=(ROOT/'docs/cart-owned-diagnostic-profile.json').read_bytes()
        source=(ROOT/'docs/linear8k-guarded-profile.json').read_bytes()
        if hashlib.sha256(old).hexdigest()!=PARENT_CONTRACT:
            raise AssemblyError('immutable combined contract differs')
        expected=json.loads(old)
        expected.update(profile=PROFILE,purpose='original-cart-owned-linear8k-native-guard-required-development',
                        mapper=MAPPER,native_guard_requirement=GUARD)
        contract=json.loads(source)
        if json.dumps(contract,sort_keys=True)!=json.dumps(expected,sort_keys=True):
            raise AssemblyError('Linear8K native guard/typed ownership contract differs')
    except (OSError,ValueError,TypeError) as error:
        raise AssemblyError('cannot read guarded Linear8K contract') from error
    parent_source=mapping['source_sha256']
    mapping.update(purpose='authored-linear8k-guarded-requires-native-admission',target=PROFILE,
        public_contract=contract,public_contract_sha256=hashlib.sha256(source).hexdigest(),
        parent_source_revision=PARENT_REVISION,parent_image_sha256=PARENT_IMAGE,
        parent_public_contract_sha256=PARENT_CONTRACT,parent_source_sha256=parent_source,
        mapper=copy.deepcopy(MAPPER),native_guard_requirement=copy.deepcopy(GUARD),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    # A required HOST guard is not a new authored CPU capability.
    return data,mapping
