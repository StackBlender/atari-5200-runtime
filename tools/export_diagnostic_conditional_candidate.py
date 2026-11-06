# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Export separately identified B2; never alter pinned B0/B1 plumbing/inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from emitter import AssemblyError,report_json
from export_candidate import source_revision
from export_diagnostic_cold_candidate import candidate as parent_candidate,verify_checkout as verify_parent
from diagnostic_conditional_image import diagnostic_conditional_image,PARENT_REVISION

ROOT=Path(__file__).resolve().parents[1]
EXTRA_INPUTS=('tools/diagnostic_conditional_image.py','tools/export_diagnostic_conditional_candidate.py',
              'cmake/diagnostic-conditional-candidate.cmake')


def candidate(revision):
    revision=source_revision(revision)
    data,mapping=diagnostic_conditional_image();mapping['source_revision']=revision
    encoded=report_json(mapping);_,_,old=parent_candidate(revision);manifest=json.loads(old)
    manifest.update(profile=mapping['target'],
        version=manifest['version'].replace('.candidate1','.diagnostic-conditional-v1.candidate1'),
        authored_capabilities=mapping['authored_capabilities'],metadata_policy=mapping['metadata_policy'],
        image=dict(origin=0xf800,size=2048,sha256=mapping['sha256']),
        map_sha256=hashlib.sha256(encoded.encode()).hexdigest(),symbols=mapping['symbols'])
    manifest['timing']['diagnostic_second_ff_base_cycles_max']=745
    manifest['provenance'].update(parent_source_revision=PARENT_REVISION,
        parent_image_sha256=mapping['parent_image_sha256'],
        parent_source_sha256=mapping['parent_source_sha256'],
        parent_exporter_sha256=manifest['provenance']['exporter_sha256'],
        startup_source_sha256=mapping['source_sha256'],
        exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return data,encoded,report_json(manifest)


def verify_checkout(root,revision):
    source_revision(revision)
    verify_parent(root,PARENT_REVISION);verify_parent(root,revision)
    try:
        for relative in EXTRA_INPUTS:
            pinned=subprocess.run(['git','-C',str(root),'show',revision+':'+relative],capture_output=True,check=True,timeout=10).stdout
            if (root/relative).read_bytes()!=pinned:
                raise AssemblyError('export input differs from pinned source: '+relative)
    except (OSError,subprocess.SubprocessError) as error:
        raise AssemblyError('cannot verify pinned B2 checkout') from error


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
