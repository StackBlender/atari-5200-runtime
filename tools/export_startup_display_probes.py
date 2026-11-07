# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Export twelve ORIGINAL cartridge diagnostics from one immutable source pin."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from startup_display_probe import startup_display_probe

ROOT=Path(__file__).resolve().parents[1]
INPUTS=('tools/startup_display_probe.py','tools/export_startup_display_probes.py',
        'tools/emitter.py','tools/entry_probe.py','tools/cartridge_candidate.py',
        'docs/startup-display-probe-contract.md')


def export(revision,destination):
    if not re.fullmatch('[0-9a-f]{40}',revision):
        raise ValueError('full immutable source revision required')
    hashes={}
    for path in INPUTS:
        committed=subprocess.run(['git','-C',str(ROOT),'show',revision+':'+path],
                                 capture_output=True,check=True,timeout=10).stdout
        data=(ROOT/path).read_bytes()
        if committed!=data:
            raise ValueError('diagnostic frozen input differs: '+path)
        hashes[path]=hashlib.sha256(data).hexdigest()
    # Verify ALL source inputs before creating any output. No runtime provider,
    # manifest converter target or existing catalog entry is replaced.
    destination.mkdir(parents=True,exist_ok=True)
    cases=[]
    for board,entries in (('Linear32K',(0x8000,)),('Linear8K',(0x8000,0xa000))):
        for entry in entries:
            for control in ('direct','shadow'):
                for second_ff in (False,True):
                    data,report=startup_display_probe(board,entry,control,second_ff)
                    name=f"{board}-{entry:04x}-{control}-{'second-ff' if second_ff else 'numeric'}"
                    report.update(source_revision=revision,source_inputs=hashes)
                    image=destination/(name+'.bin');descriptor=destination/(name+'.json')
                    image.write_bytes(data)
                    descriptor.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
                    cases.append(dict(name=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                                      report_sha256=hashlib.sha256(descriptor.read_bytes()).hexdigest()))
    index=dict(schema=1,purpose='original-startup-display-diagnostics-only',
               source_revision=revision,source_inputs=hashes,cases=cases,
               native_execution_verified=False,private_input_used=False,runtime_provider=False)
    (destination/'index.json').write_text(json.dumps(index,sort_keys=True,indent=2)+'\n')
    return index


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-revision',required=True)
    parser.add_argument('--output-dir',required=True,type=Path)
    args=parser.parse_args()
    try:export(args.source_revision,args.output_dir)
    except (ValueError,subprocess.SubprocessError) as error:parser.error(str(error))


if __name__=='__main__':main()
