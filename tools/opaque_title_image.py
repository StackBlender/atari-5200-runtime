# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Approved original opaque-title policy; no native execution qualification."""
import argparse
import hashlib
from pathlib import Path
from emitter import AssemblyError, report_json
from fire_bridge_image import fire_bridge_image

PARENT_REVISION='e25a466d15c574f3ec364bfc2f44bc7ef2f51117'
PARENT_SHA256='c5fd8df1564c28e5ed4c5aad9f8eabdc64a62e32de28e8dcce6bfae7ea533d24'


def opaque_title_image():
    parent,mapping=fire_bridge_image()
    if hashlib.sha256(parent).hexdigest()!=PARENT_SHA256:
        raise AssemblyError('opaque title requires the exact qualified bridge parent')
    if mapping['symbols']['validate_metadata']!=0xfeb0 or parent[0x6b0:0x6b5]!=bytes.fromhex('a200bde8bf'):
        raise AssemblyError('metadata entry differs from reviewed LDX00/LDA BFE8,X')
    if mapping['used']!=1895 or parent[0x7a0:0x7fa]!=b'\xff'*90:
        raise AssemblyError('reviewed cumulative fit/reserve differs')
    # Static composition of OUR original program, not a runtime patch, HLE or
    # manufacturer binary. LDX20 starts the unchanged loop at BFFC (two years).
    image=bytearray(parent);image[0x6b1]=20;data=bytes(image)
    mapping.update(purpose='authored-opaque-title-awaiting-execution',
        sha256=hashlib.sha256(data).hexdigest(),
        parent_source_revision=PARENT_REVISION,parent_image_sha256=PARENT_SHA256,
        parent_source_sha256=mapping['source_sha256'],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        metadata_policy=dict(title_bytes=20,title='opaque',year_bytes=2,
                             year_min=0x50,year_max=0x59,diagnostic_bypass=False),
        nominal_startup=dict(normal_cycles=1091,boundary_cycles=1098,
                             skipped_title_iterations=20,cycles_saved=380,
                             helper_cycles=39,instructions_saved=160))
    mapping['authored_capabilities']=[*mapping['authored_capabilities'],'opaque-title-v1']
    return data,mapping


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args()
    try:
        data,mapping=opaque_title_image()
    except AssemblyError as error:
        parser.error(str(error))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'opaque-title.bin').write_bytes(data)
    (args.output_dir/'opaque-title-map.json').write_text(report_json(mapping))


if __name__=='__main__':main()
