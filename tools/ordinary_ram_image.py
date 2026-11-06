# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""B0: identical original timer bytes, separately explicit ordinary RAM contract."""
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError
from timer_experiment import ROOT,PARENT_REVISION,PARENT_SHA256,parent_image


def ordinary_ram_image():
    data,mapping=parent_image()
    source=(ROOT/'docs/ordinary-ram-profile.json').read_bytes();contract=json.loads(source)
    expected=dict(intervals='half-open',runtime_shadows=[0,25],runtime_vectors=[512,540],
        shared_stack=[256,512],consumer_zero_page=[25,256],consumer_ram=[540,16384],
        explicitly_ceded=[540,544],runtime_input_reservation=None,
        additional_runtime_ram_bytes=0,power_on_contents_preserved=False)
    if (contract['schema']!=1 or contract['profile']!='ntsc-four-port-cart-owned-irq-development' or
        contract['runtime_abi']!='sb52-dev-cc65-v1' or contract['historical_abi'] is not False or
        contract['retail_compatibility'] is not False or contract['ownership']!=expected or
        contract['irq']!=dict(default_timer_supported_mask=7,default_unsupported_fault_before_ack=True,
            cart_owns_generic_vector=True,generic_entry='hardware-frame-only-after-classifier-restores-AX',
            cart_callback_return='RTI-after-own-register-restores',required_runtime_keyboard_callback=None,
            mandatory_extra_ram_cart_declaration=False) or
        [(f['address'],f['cold']) for f in contract['initialization']['shadows']]!=[(i,0) for i in range(25)] or
        [(f['address'],f['cold']) for f in contract['initialization']['vectors']]!=
            [(512+2*i,{0:0xfe00,1:0xfca0,2:0xfcb0}.get(i,0xfc86)) for i in range(14)]):
        raise AssemblyError('ordinary RAM reviewed ownership/initialization differs')
    mapping.update(purpose='authored-ordinary-ram-profile-awaiting-native-admission',
        target=contract['profile'],public_contract=contract,
        public_contract_sha256=hashlib.sha256(source).hexdigest(),
        parent_source_revision=PARENT_REVISION,parent_image_sha256=PARENT_SHA256,
        parent_source_sha256=mapping['source_sha256'],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    mapping['authored_capabilities']=[*mapping['authored_capabilities'],'ordinary-ram-contract-v1']
    return data,mapping
