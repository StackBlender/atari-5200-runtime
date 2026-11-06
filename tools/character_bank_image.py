# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Original64-cell development mapping; native qualification remains separate."""
import argparse
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError, report_json
from opaque_title_image import opaque_title_image

ROOT=Path(__file__).resolve().parents[1]
PARENT_REVISION='ed013540ac2996d76fab149f6fb8dea9fcead584'
PARENT_SHA256='8d6ef38c1b487fa95742e62e9a5c0b1a928ddb446977264739a263fa0bc070c4'
ASSET_REVISION='316a91f630f47aa0cdbefa93e39546459778ab67'
ASSET_SHA256='674bd8776ac83d517654b3d6ca2720e5b6d69f5e084c2bd35052c19c074f547a'


def pack_geometry(document):
    """Validate and pack our normative ORIGINAL geometry data, not a ROM oracle."""
    if (not isinstance(document,dict) or document.get('schema')!=1 or
        document.get('purpose')!='original-asset-data-not-atari-encoding' or
        document.get('source_revision')!=ASSET_REVISION or
        document.get('license')!='GPL-3.0-or-later' or
        document.get('copyright')!='2026 StackBlender LLC' or
        document.get('sha256')!=ASSET_SHA256):
        raise AssemblyError('original geometry provenance mismatch')
    geometry=document.get('geometry')
    if not isinstance(geometry,dict) or any(geometry.get(k)!=v for k,v in
        dict(schema=1,paper='.',ink='#',row_order='top-to-bottom',bit_order='MSB-left').items()):
        raise AssemblyError('geometry convention mismatch')
    cells=geometry.get('glyphs')
    if not isinstance(cells,dict) or set(cells)!={str(n) for n in range(32,127)}:
        raise AssemblyError('exact95original ASCII labels required')
    data=bytearray()
    for label in range(32,127):
        rows=cells[str(label)]
        if not isinstance(rows,list) or len(rows)!=8:
            raise AssemblyError('geometry requires eight rows')
        for row in rows:
            if not isinstance(row,str) or len(row)!=8 or set(row)-{'.','#'}:
                raise AssemblyError('geometry requires eight binary pixels per row')
            value=0
            for pixel in row:
                value=(value<<1)|(pixel=='#')
            data.append(value)
    if hashlib.sha256(data).hexdigest()!=ASSET_SHA256:
        raise AssemblyError('original760-byte geometry identity mismatch')
    return bytes(data)


def digit_cells():
    # Recompose our original startup-brief segment coordinates, never read the
    # parent image as the source of expected glyph geometry.
    selections=('abcdef','bc','abdeg','abcdg','bcfg','acdfg','acdefg','abc','abcdefg','abcdfg')
    points=dict(a=[(x,0) for x in range(2,6)],g=[(x,3) for x in range(2,6)],
                d=[(x,6) for x in range(2,6)],f=[(1,y) for y in (1,2)],
                b=[(6,y) for y in (1,2)],e=[(1,y) for y in (4,5)],
                c=[(6,y) for y in (4,5)])
    result=bytearray()
    for selected in selections:
        rows=bytearray(8)
        for segment in selected:
            for x,y in points[segment]:rows[y]|=128>>x
        result.extend(rows)
    return bytes(result)


def character_bank_image():
    parent,mapping=opaque_title_image()
    if len(parent)!=2048 or hashlib.sha256(parent).hexdigest()!=PARENT_SHA256:
        raise AssemblyError('character bank requires exact qualified opaque-title parent')
    if (mapping['used']!=1895 or mapping['remaining']!=153 or
        parent[0x7a0:0x7fa]!=b'\xff'*90):
        raise AssemblyError('reviewed cumulative fit/reserve differs')
    try:
        source=(ROOT/'assets/printable-geometry.json').read_bytes()
        original=pack_geometry(json.loads(source))
    except (OSError,ValueError,TypeError) as error:
        raise AssemblyError('cannot read original geometry data') from error
    bank=bytearray(original[:512]);bank[0x80:0xd0]=digit_cells()
    data=bytes(bank)+parent[512:]
    mapping.update(purpose='authored-original64-bank-awaiting-execution',
        sha256=hashlib.sha256(data).hexdigest(),
        parent_source_revision=PARENT_REVISION,parent_image_sha256=PARENT_SHA256,
        parent_source_sha256=mapping['source_sha256'],
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        character_mapping=dict(policy='original-ascii20-5f-first64-v1',
            historical_encoding=False,label_first=32,label_last=95,index_bias=-32,
            bank_address=0xf800,bank_bytes=512,glyph_count=64,bytes_per_glyph=8,
            retained_digit_indices=[16,25],legacy_digit_indices=[80,89],
            remaining_ascii_unbound=True),
        font_geometry=dict(source_revision=ASSET_REVISION,sha256=ASSET_SHA256,
            source_data_sha256=hashlib.sha256(source).hexdigest(),
            source_data='assets/printable-geometry.json',
            composed_bank_sha256=hashlib.sha256(bank).hexdigest()))
    mapping['authored_capabilities']=[*mapping['authored_capabilities'],'original64-font-v1']
    return data,mapping


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args()
    try:data,mapping=character_bank_image()
    except AssemblyError as error:parser.error(str(error))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'character-bank.bin').write_bytes(data)
    (args.output_dir/'character-bank-map.json').write_text(report_json(mapping))


if __name__=='__main__':main()
