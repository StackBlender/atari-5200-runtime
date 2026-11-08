# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Export the compat3 generation under a NEW complete identity."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from emitter import AssemblyError, report_json
from export_candidate import source_revision
from export_compat2_candidate import candidate as parent_candidate, verify_checkout as verify_parent
from compat3_image import compat3_image

ROOT = Path(__file__).resolve().parents[1]
EXTRA_INPUTS = ('tools/compat3_image.py', 'tools/export_compat3_candidate.py', 'cmake/compat3-candidate.cmake')
PARENT_REVISION = '9ecf093f50f139bbcc1be08cb98a5cb11e252081'


def revision(value):
    value = source_revision(value)
    if value in (PARENT_REVISION, '214e1e4a3caabc3c17693bd5271d2e9ce0761428', 'c1aaf9b2f3f3663f1263492dc4edabb8eb2c32df', 'e8f296d5a8fa693f13b5dd46259eafcb5567e88f'):
        raise AssemblyError('compat3 requires a new distinct source revision')
    return value


def candidate(value):
    value = revision(value)
    data, mapping = compat3_image(); mapping['source_revision'] = value
    encoded = report_json(mapping)
    _, _, old = parent_candidate(PARENT_REVISION); manifest = json.loads(old)
    manifest.update(
        source_revision=value,
        version=manifest['version'].replace('.compat-v2.candidate1', '.compat-v3.candidate1'),
        authored_capabilities=mapping['authored_capabilities'],
        image=dict(origin=0xf800, size=2048, sha256=mapping['sha256']),
        map_sha256=hashlib.sha256(encoded.encode()).hexdigest(), symbols=mapping['symbols'],
        compat=manifest.get('compat'), compat3=mapping['compat3'])
    manifest['timing']['base_cycles_max'] = mapping['nominal_startup']['numeric_boundary_cycles']
    manifest['timing']['diagnostic_second_ff_base_cycles_max'] = mapping['nominal_startup']['ff_boundary_cycles']
    manifest['provenance'].update(parent_image_sha256=mapping['parent_image_sha256'],
        parent_exporter_sha256=manifest['provenance']['exporter_sha256'],
        startup_source_sha256=mapping['source_sha256'],
        exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return data, encoded, report_json(manifest)


def verify_checkout(root, value):
    value = revision(value)
    try:
        for relative in EXTRA_INPUTS:
            pinned = subprocess.run(['git', '-C', str(root), 'show', value + ':' + relative],
                capture_output=True, check=True, timeout=10).stdout
            if (root / relative).read_bytes() != pinned:
                raise AssemblyError('export input differs from pinned source: ' + relative)
    except (OSError, subprocess.SubprocessError) as error:
        raise AssemblyError('cannot verify compat3 checkout') from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-revision', required=True)
    parser.add_argument('--output-dir', required=True, type=Path); args = parser.parse_args()
    try:
        verify_parent(ROOT, PARENT_REVISION)
        verify_checkout(ROOT, args.source_revision)
        data, mapping, manifest = candidate(args.source_revision)
    except AssemblyError as error:
        parser.error(str(error))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, value in [('startup.bin', data), ('startup-map.json', mapping.encode()), ('startup-manifest.json', manifest.encode())]:
        path = args.output_dir / name
        if not path.exists() or path.read_bytes() != value:
            temp = path.with_suffix(path.suffix + '.tmp'); temp.write_bytes(value); temp.replace(path)


if __name__ == '__main__':
    main()
