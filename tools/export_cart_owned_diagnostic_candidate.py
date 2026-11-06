# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Export explicit combined B2 bytes/B0 ownership under a NEW complete identity."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from emitter import AssemblyError,report_json
from export_candidate import source_revision
from export_diagnostic_conditional_candidate import candidate as parent_candidate,verify_checkout as verify_image_parent
from export_ordinary_ram_candidate import verify_checkout as verify_ownership_parent
from cart_owned_diagnostic_image import (cart_owned_diagnostic_image,IMAGE_PARENT_REVISION,
    OWNERSHIP_PARENT_REVISION)

ROOT=Path(__file__).resolve().parents[1]
EXTRA_INPUTS=('tools/cart_owned_diagnostic_image.py','tools/export_cart_owned_diagnostic_candidate.py',
              'cmake/cart-owned-diagnostic-candidate.cmake','docs/cart-owned-diagnostic-profile.json')


def revision(value):
    value=source_revision(value)
    if value in (IMAGE_PARENT_REVISION,OWNERSHIP_PARENT_REVISION):
        raise AssemblyError('combined delivery requires a new distinct source revision')
    return value


def candidate(value):
    value=revision(value)
    data,mapping=cart_owned_diagnostic_image();mapping['source_revision']=value
    encoded=report_json(mapping);_,_,old=parent_candidate(value);manifest=json.loads(old)
    manifest.update(profile=mapping['target'],
        version=manifest['version'].replace('.candidate1','.cart-owned-diagnostic-v1.candidate1'),
        authored_capabilities=mapping['authored_capabilities'],public_contract=mapping['public_contract'],
        ownership_policy=mapping['ownership_policy'],
        image=dict(origin=0xf800,size=2048,sha256=mapping['sha256']),
        map_sha256=hashlib.sha256(encoded.encode()).hexdigest(),symbols=mapping['symbols'])
    manifest['provenance'].update(parent_source_revision=IMAGE_PARENT_REVISION,
        parent_image_sha256=mapping['parent_image_sha256'],
        parent_source_sha256=mapping['parent_source_sha256'],
        parent_exporter_sha256=manifest['provenance']['exporter_sha256'],
        ownership_parent_source_revision=OWNERSHIP_PARENT_REVISION,
        ownership_parent_contract_sha256=mapping['ownership_parent_contract_sha256'],
        public_contract_sha256=mapping['public_contract_sha256'],
        startup_source_sha256=mapping['source_sha256'],
        exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return data,encoded,report_json(manifest)


def verify_checkout(root,value):
    value=revision(value)
    verify_image_parent(root,IMAGE_PARENT_REVISION);verify_image_parent(root,value)
    verify_ownership_parent(root,OWNERSHIP_PARENT_REVISION);verify_ownership_parent(root,value)
    try:
        for relative in EXTRA_INPUTS:
            pinned=subprocess.run(['git','-C',str(root),'show',value+':'+relative],capture_output=True,check=True,timeout=10).stdout
            if (root/relative).read_bytes()!=pinned:
                raise AssemblyError('export input differs from pinned source: '+relative)
    except (OSError,subprocess.SubprocessError) as error:
        raise AssemblyError('cannot verify explicit combined checkout') from error


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-revision',required=True)
    parser.add_argument('--output-dir',required=True,type=Path);args=parser.parse_args()
    try:
        verify_checkout(ROOT,args.source_revision)
        data,mapping,manifest=candidate(args.source_revision)
    except AssemblyError as error:parser.error(str(error))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,value in [('startup.bin',data),('startup-map.json',mapping.encode()),('startup-manifest.json',manifest.encode())]:
        path=args.output_dir/name
        if not path.exists() or path.read_bytes()!=value:
            temp=path.with_suffix(path.suffix+'.tmp');temp.write_bytes(value);temp.replace(path)


if __name__=='__main__':main()
