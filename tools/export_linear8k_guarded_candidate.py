# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Strict export of a new guard-requiring identity; no new6502 ROM code."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from emitter import AssemblyError,report_json
from export_candidate import source_revision
from export_cart_owned_diagnostic_candidate import candidate as parent_candidate,verify_checkout as verify_parent
from linear8k_guarded_image import linear8k_guarded_image,PARENT_REVISION

ROOT=Path(__file__).resolve().parents[1]
EXTRA_INPUTS=('tools/linear8k_guarded_image.py','tools/export_linear8k_guarded_candidate.py',
              'cmake/linear8k-guarded-candidate.cmake','docs/linear8k-guarded-profile.json')


def revision(value):
    value=source_revision(value)
    if value in (PARENT_REVISION,'89af2dcc1d889585d6c9dde2fa12a3db30ce3045',
                  'becb92e01e97e89568cac58ab051e23b803ae53a'):
        raise AssemblyError('guarded Linear8K needs a NEW distinct source pin')
    return value


def candidate(value):
    value=revision(value)
    data,mapping=linear8k_guarded_image();mapping['source_revision']=value
    encoded=report_json(mapping);_,_,before=parent_candidate(value);manifest=json.loads(before)
    parent_exporter=manifest['provenance']['exporter_sha256']
    manifest.update(profile=mapping['target'],
        version=manifest['version'].replace('.candidate1','.linear8k-guarded-v1.candidate1'),
        mapper=mapping['mapper'],public_contract=mapping['public_contract'],
        native_guard_requirement=mapping['native_guard_requirement'],
        map_sha256=hashlib.sha256(encoded.encode()).hexdigest())
    manifest['provenance'].update(parent_source_revision=PARENT_REVISION,
        parent_image_sha256=mapping['parent_image_sha256'],
        parent_public_contract_sha256=mapping['parent_public_contract_sha256'],
        parent_source_sha256=mapping['parent_source_sha256'],parent_exporter_sha256=parent_exporter,
        public_contract_sha256=mapping['public_contract_sha256'],
        startup_source_sha256=mapping['source_sha256'],
        exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return data,encoded,report_json(manifest)


def verify_checkout(root,value):
    value=revision(value)
    verify_parent(root,PARENT_REVISION);verify_parent(root,value)
    try:
        for relative in EXTRA_INPUTS:
            pinned=subprocess.run(['git','-C',str(root),'show',value+':'+relative],
                                   capture_output=True,check=True,timeout=10).stdout
            if (root/relative).read_bytes()!=pinned:
                raise AssemblyError('export input differs from pinned source: '+relative)
    except (OSError,subprocess.SubprocessError) as error:
        raise AssemblyError('cannot verify guarded Linear8K source') from error


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-revision',required=True)
    parser.add_argument('--output-dir',required=True,type=Path);args=parser.parse_args()
    try:
        verify_checkout(ROOT,args.source_revision)
        data,mapping,manifest=candidate(args.source_revision)
    except AssemblyError as error:parser.error(str(error))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,value in [('startup.bin',data),('startup-map.json',mapping.encode()),
                       ('startup-manifest.json',manifest.encode())]:
        path=args.output_dir/name
        if not path.exists() or path.read_bytes()!=value:
            temp=path.with_suffix(path.suffix+'.tmp');temp.write_bytes(value);temp.replace(path)


if __name__=='__main__':main()
