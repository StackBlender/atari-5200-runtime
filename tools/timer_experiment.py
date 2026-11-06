# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Shared exact-parent/export plumbing for SEPARATE original B0/B1 experiments."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from emitter import AssemblyError, report_json
from export_candidate import source_revision
from export_timer_candidate import candidate as timer_candidate,verify_timer_checkout
from timer_dispatch_image import timer_dispatch_image

ROOT=Path(__file__).resolve().parents[1]
PARENT_REVISION='ac9b47e50c213b08022e78bdef64662569cd3d29'
PARENT_SHA256='eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550'


def parent_image():
    data,mapping=timer_dispatch_image()
    if (len(data)!=2048 or hashlib.sha256(data).hexdigest()!=PARENT_SHA256 or
        mapping['used']!=1504 or mapping['remaining']!=544 or
        data[0x700:0x7fa]!=b'\xff'*250):
        raise AssemblyError('experiment requires exact qualified1504-byte timer parent/reserve')
    return data,mapping


def candidate(kind,revision,exporter):
    revision=source_revision(revision)
    if kind=='ordinary-ram':
        from ordinary_ram_image import ordinary_ram_image
        data,mapping=ordinary_ram_image()
    elif kind=='diagnostic-cold':
        from diagnostic_cold_image import diagnostic_cold_image
        data,mapping=diagnostic_cold_image()
    else:raise AssemblyError('unknown separate timer experiment')
    mapping['source_revision']=revision;encoded=report_json(mapping)
    _,_,parent=timer_candidate(revision);manifest=json.loads(parent)
    manifest.update(profile=mapping['target'],version=manifest['version'].replace('.candidate1','.'+kind+'-v1.candidate1'),
        authored_capabilities=mapping['authored_capabilities'],
        image=dict(origin=0xf800,size=2048,sha256=mapping['sha256']),
        map_sha256=hashlib.sha256(encoded.encode()).hexdigest(),symbols=mapping['symbols'])
    for field in ('public_contract','metadata_policy','ownership_policy'):
        if field in mapping:manifest[field]=mapping[field]
    if 'nominal_startup' in mapping:
        manifest['timing']['base_cycles_max']=mapping['nominal_startup']['numeric_boundary_cycles']
        manifest['timing']['diagnostic_second_ff_base_cycles_max']=mapping['nominal_startup']['ff_boundary_cycles']
    manifest['provenance'].update(parent_source_revision=PARENT_REVISION,parent_image_sha256=PARENT_SHA256,
        parent_source_sha256=mapping['parent_source_sha256'],
        parent_exporter_sha256=manifest['provenance']['exporter_sha256'],
        startup_source_sha256=mapping['source_sha256'],
        exporter_sha256=hashlib.sha256(Path(exporter).read_bytes()).hexdigest(),
        experiment_export_plumbing_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    if 'public_contract_sha256' in mapping:
        manifest['provenance']['public_contract_sha256']=mapping['public_contract_sha256']
    return data,encoded,report_json(manifest)


def verify_checkout(root,revision,inputs):
    source_revision(revision)
    verify_timer_checkout(root,PARENT_REVISION);verify_timer_checkout(root,revision)
    try:
        for relative in inputs:
            pinned=subprocess.run(['git','-C',str(root),'show',revision+':'+relative],capture_output=True,check=True,timeout=10).stdout
            if (root/relative).read_bytes()!=pinned:
                raise AssemblyError('export input differs from pinned source: '+relative)
    except (OSError,subprocess.SubprocessError) as error:
        raise AssemblyError('cannot verify separate timer experiment checkout') from error


def main(kind,inputs,exporter):
    parser=argparse.ArgumentParser(description='Separate original '+kind+' experiment')
    parser.add_argument('--source-revision',required=True)
    parser.add_argument('--output-dir',required=True,type=Path);args=parser.parse_args()
    try:
        verify_checkout(ROOT,args.source_revision,inputs)
        data,mapping,manifest=candidate(kind,args.source_revision,exporter)
    except AssemblyError as error:parser.error(str(error))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,value in [('startup.bin',data),('startup-map.json',mapping.encode()),('startup-manifest.json',manifest.encode())]:
        path=args.output_dir/name
        if not path.exists() or path.read_bytes()!=value:
            temp=path.with_suffix(path.suffix+'.tmp');temp.write_bytes(value);temp.replace(path)
