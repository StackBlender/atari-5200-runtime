# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Export separately identified experimental original64 character bank."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from emitter import AssemblyError, report_json
from export_candidate import source_revision
from export_opaque_title_candidate import candidate as parent_candidate, verify_opaque_title_checkout
from character_bank_image import character_bank_image, PARENT_REVISION

EXTRA_INPUTS=('tools/character_bank_image.py','tools/export_character_bank_candidate.py',
              'cmake/character-bank-candidate.cmake','assets/printable-geometry.json')


def candidate(revision):
    revision=source_revision(revision)
    data,mapping=character_bank_image();mapping['source_revision']=revision
    encoded=report_json(mapping)
    _,_,parent=parent_candidate(revision);manifest=json.loads(parent)
    manifest.update(version=manifest['version'].replace('.candidate1','.original64-v1.candidate1'),
        authored_capabilities=mapping['authored_capabilities'],
        image=dict(origin=0xf800,size=2048,sha256=mapping['sha256']),
        map_sha256=hashlib.sha256(encoded.encode()).hexdigest(),symbols=mapping['symbols'],
        character_mapping=mapping['character_mapping'],font_geometry=mapping['font_geometry'])
    manifest['provenance'].update(parent_source_revision=PARENT_REVISION,
        parent_image_sha256=mapping['parent_image_sha256'],
        parent_source_sha256=mapping['parent_source_sha256'],
        parent_exporter_sha256=manifest['provenance']['exporter_sha256'],
        startup_source_sha256=mapping['source_sha256'],
        geometry_source_data_sha256=mapping['font_geometry']['source_data_sha256'],
        exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return data,encoded,report_json(manifest)


def verify_character_bank_checkout(root,revision):
    verify_opaque_title_checkout(root,PARENT_REVISION)
    verify_opaque_title_checkout(root,revision)
    try:
        for relative in EXTRA_INPUTS:
            pinned=subprocess.run(['git','-C',str(root),'show',revision+':'+relative],
                capture_output=True,check=True,timeout=10).stdout
            if (root/relative).read_bytes()!=pinned:
                raise AssemblyError('export input differs from pinned source: '+relative)
    except (OSError,subprocess.SubprocessError) as error:
        raise AssemblyError('cannot verify pinned character-bank checkout') from error


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-revision',required=True)
    parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args()
    try:
        verify_character_bank_checkout(Path(__file__).resolve().parents[1],args.source_revision)
        data,mapping,manifest=candidate(args.source_revision)
    except AssemblyError as error:parser.error(str(error))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,value in [('startup.bin',data),('startup-map.json',mapping.encode()),('startup-manifest.json',manifest.encode())]:
        path=args.output_dir/name
        if not path.exists() or path.read_bytes()!=value:
            temporary=path.with_suffix(path.suffix+'.tmp');temporary.write_bytes(value);temporary.replace(path)


if __name__=='__main__':main()
