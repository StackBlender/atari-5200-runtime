# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Export the callable-reset generation under a NEW complete identity."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from emitter import AssemblyError,report_json
from export_candidate import source_revision
from export_cart_owned_diagnostic_candidate import candidate as parent_candidate,verify_checkout as verify_parent
from callable_reset_image import callable_reset_image,PARENT_SHA256

ROOT=Path(__file__).resolve().parents[1]
EXTRA_INPUTS=('tools/callable_reset_image.py','tools/export_callable_reset_candidate.py',
              'cmake/callable-reset-candidate.cmake')


def revision(value):
    value=source_revision(value)
    if value=='e8f296d5a8fa693f13b5dd46259eafcb5567e88f':
        raise AssemblyError('callable reset requires a new distinct source revision')
    return value


def candidate(value):
    value=revision(value)
    data,mapping=callable_reset_image();mapping['source_revision']=value
    encoded=report_json(mapping);_,_,old=parent_candidate(value);manifest=json.loads(old)
    manifest.update(
        version=manifest['version'].replace('.cart-owned-diagnostic-v1.candidate1','.cart-owned-diagnostic-v1.callable-reset-v1.candidate1'),
        authored_capabilities=mapping['authored_capabilities'],
        image=dict(origin=0xf800,size=2048,sha256=mapping['sha256']),
        map_sha256=hashlib.sha256(encoded.encode()).hexdigest(),symbols=mapping['symbols'],
        reset_layout=mapping['reset_layout'])
    manifest['timing']['base_cycles_max']=mapping['nominal_startup']['numeric_boundary_cycles']
    manifest['timing']['diagnostic_second_ff_base_cycles_max']=mapping['nominal_startup']['ff_boundary_cycles']
    manifest['provenance'].update(parent_image_sha256=PARENT_SHA256,
        parent_source_sha256=mapping['parent_source_sha256'],
        parent_exporter_sha256=manifest['provenance']['exporter_sha256'],
        startup_source_sha256=mapping['source_sha256'],
        exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return data,encoded,report_json(manifest)


def verify_checkout(root,value):
    value=revision(value)
    try:
        for relative in EXTRA_INPUTS:
            pinned=subprocess.run(['git','-C',str(root),'show',value+':'+relative],
                capture_output=True,check=True,timeout=10).stdout
            if (root/relative).read_bytes()!=pinned:
                raise AssemblyError('export input differs from pinned source: '+relative)
    except (OSError,subprocess.SubprocessError) as error:
        raise AssemblyError('cannot verify callable-reset checkout') from error


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-revision',required=True)
    parser.add_argument('--output-dir',required=True,type=Path);args=parser.parse_args()
    try:
        verify_parent(ROOT,args.source_revision)
        verify_checkout(ROOT,args.source_revision)
        data,mapping,manifest=candidate(args.source_revision)
    except AssemblyError as error:parser.error(str(error))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,value in [('startup.bin',data),('startup-map.json',mapping.encode()),('startup-manifest.json',manifest.encode())]:
        path=args.output_dir/name
        if not path.exists() or path.read_bytes()!=value:
            temp=path.with_suffix(path.suffix+'.tmp');temp.write_bytes(value);temp.replace(path)


if __name__=='__main__':main()
