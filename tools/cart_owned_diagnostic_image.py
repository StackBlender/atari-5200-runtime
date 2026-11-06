# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Explicit combined contract, byte-identical B2; no native admission inferred."""
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError
from diagnostic_conditional_image import diagnostic_conditional_image

ROOT=Path(__file__).resolve().parents[1]
IMAGE_PARENT_REVISION='89af2dcc1d889585d6c9dde2fa12a3db30ce3045'
IMAGE_PARENT_SHA256='5936e46d08c7991231a52dfb6c1a404a7a0d1ab505a51b2c5e09a569d7ad20e4'
OWNERSHIP_PARENT_REVISION='becb92e01e97e89568cac58ab051e23b803ae53a'
OWNERSHIP_PARENT_SHA256='250834f404aedde32eab4fe752f0ac0b1a5ef13fac89ba9303a177e7da787ff1'
PROFILE='ntsc-four-port-cart-owned-diagnostic-conditional-development'


def cart_owned_diagnostic_image():
    data,mapping=diagnostic_conditional_image()
    if (len(data)!=2048 or hashlib.sha256(data).hexdigest()!=IMAGE_PARENT_SHA256 or
        mapping['used']!=1556 or mapping['remaining']!=492 or
        data[0x700:0x7fa]!=b'\xff'*250 or
        mapping['target']!='ntsc-four-port-diagnostic-conditional-development' or
        mapping['ownership_policy']!='unchanged-conservative-timer-parent-through021F-no-B0-cession' or
        'public_contract' in mapping):
        raise AssemblyError('combined profile requires exact conservative B2 parent')
    try:
        old=(ROOT/'docs/ordinary-ram-profile.json').read_bytes()
        source=(ROOT/'docs/cart-owned-diagnostic-profile.json').read_bytes()
        if hashlib.sha256(old).hexdigest()!=OWNERSHIP_PARENT_SHA256:
            raise AssemblyError('immutable B0 ownership source differs')
        expected=json.loads(old);expected.update(profile=PROFILE,purpose='original-cart-owned-conditional-cold-development')
        contract=json.loads(source)
        if json.dumps(contract,sort_keys=True)!=json.dumps(expected,sort_keys=True):
            raise AssemblyError('rebound combined ownership/initialization differs')
    except (OSError,ValueError,TypeError) as error:
        raise AssemblyError('cannot read explicit combined ownership contract') from error
    current_hash=hashlib.sha256(source).hexdigest()
    if current_hash==OWNERSHIP_PARENT_SHA256:
        raise AssemblyError('combined contract must have its own identity')
    mapping.update(purpose='authored-cart-owned-diagnostic-awaiting-native-admission',
        target=PROFILE,public_contract=contract,public_contract_sha256=current_hash,
        ownership_policy='explicit-cart-owned-application021C-3FFF-no0600reservation-v1',
        parent_source_revision=IMAGE_PARENT_REVISION,parent_image_sha256=IMAGE_PARENT_SHA256,
        parent_source_sha256=mapping['source_sha256'],
        ownership_parent_source_revision=OWNERSHIP_PARENT_REVISION,
        ownership_parent_contract_sha256=OWNERSHIP_PARENT_SHA256,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    mapping['authored_capabilities']=[*mapping['authored_capabilities'],'cart-owned-diagnostic-contract-v1']
    return data,mapping
