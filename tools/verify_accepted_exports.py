# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Reproduce eleven independently qualified DEVELOPMENT exports, no CPU run."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
# Immutable bounded native-qualified generations, NOT a product release list.
# name, exporter, full source pin, independently retained image SHA256.
GENERATIONS=(
    ('startup','export_candidate.py','711a2e986f7906f45aebd310e6330fd7ffc338bf','b2d8ebb8d0070f2aee1bd79d7adfee85b88797702cb96035ab3a18e9bd37f68d'),
    ('vbi','export_vbi_candidate.py','ba90c8550c1be1c85b5aa7d6810e1ee6c6031656','62df6162ac3accdfa19769c8f2dcd450c510e385fa71f98ec7912f61d449fa54'),
    ('display','export_display_candidate.py','9d7071f837ec513905b4a2f9718e269c7662b90c','1992e64b05d096e479c9532b14a77839bad182428b459a3ca8862ede51acb364'),
    ('dli','export_dli_candidate.py','258bc0cc764a0614ec8443a89d242a8f1fe8cb5e','374465be3cfce3d15c10c7899f4fedbd8cf854b23ee1734b9302c7049e55e05c'),
    ('analog','export_analog_candidate.py','a6c406e4cee090b8044eea3b9b6c7a5b6391b3ab','32343a567399b3b4f9c142bde446fe89397267267d51a89393553fdab9471290'),
    ('irq','export_irq_candidate.py','42762a73a0caa72b7753bd5aa4380cf9a63c573f','2b257c582044af2308699c6a0f327dca674ed79bd95eed2da7cea2537ead0675'),
    ('timer','export_timer_candidate.py','ac9b47e50c213b08022e78bdef64662569cd3d29','eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550'),
    ('keypad-irq','export_keypad_irq_candidate.py','b2e2b40d8c11326f1684635e35832fcc50f9f2d6','2fa0cbdbace0d70bab06953fef5bf08e065c6c6247a8a67692718307e75d6ef8'),
    ('keypad-window','export_keypad_window_candidate.py','fce294b7448a7c5a1a35e6c5e5ed5611ee36473f','3c1b419b9af94645ea537126d21e464f90f05013689ef7132656680d62d4207a'),
    ('fire','export_fire_candidate.py','a2a7455627a9ea3905464c295562debee2efec7d','e937064b0d1fe33d0f75cfe4dba89bcbec953adc215f83ed51ce4fee8705f815'),
    ('fire-bridge','export_fire_bridge_candidate.py','e25a466d15c574f3ec364bfc2f44bc7ef2f51117','c5fd8df1564c28e5ed4c5aad9f8eabdc64a62e32de28e8dcce6bfae7ea533d24'),
)


def require(condition,reason):
    if not condition:
        raise ValueError(reason)


def run(arguments):
    process=subprocess.run(arguments,capture_output=True,text=True,timeout=60)
    if process.returncode:
        raise ValueError(f'{Path(arguments[0]).name} failed: '+process.stderr.strip())


def validate(directory,pin,expected):
    data=(directory/'startup.bin').read_bytes()
    map_bytes=(directory/'startup-map.json').read_bytes()
    mapping=json.loads(map_bytes)
    manifest=json.loads((directory/'startup-manifest.json').read_bytes())
    require(len(data)==2048 and hashlib.sha256(data).hexdigest()==expected,'immutable image mismatch')
    require(manifest['source_revision']==pin and mapping['source_revision']==pin,'full source pin mismatch')
    require(manifest['image']==dict(origin=0xf800,size=2048,sha256=expected),'image descriptor mismatch')
    require(mapping['sha256']==expected,'map image mismatch')
    require(manifest['map_sha256']==hashlib.sha256(map_bytes).hexdigest(),'map digest mismatch')
    require(manifest['symbols']==mapping['symbols'],'symbol manifest mismatch')
    require(manifest['capabilities']==[],'accepted capabilities must remain empty')
    for flag in ('execution_verified','provider_approved','retail_compatibility'):
        require(manifest[flag] is False,'candidate flag promoted: '+flag)
    require(manifest['timing'].get('full_cycles_verified') is False,'explicit full-cycle status missing or promoted')
    for key,value in manifest['timing'].items():
        if key.endswith('verified'):
            require(value is False,'timing approval promoted: '+key)


def cmake_consumer(root,expected_directory):
    pin=GENERATIONS[-1][2]
    source=root/'parent';source.mkdir()
    checker=source/'check.py'
    checker.write_text('''from pathlib import Path
import json,sys
values=Path(sys.argv[1]).read_text().splitlines()
assert len(values)==4
assert all(Path(value).is_absolute() and Path(value).is_file() for value in values[:3])
assert json.loads(Path(values[1]).read_text())['source_revision']==values[3]
Path(sys.argv[2]).write_text('verified')
''')
    fields=('SB5200_IMAGE_FILE','SB5200_MANIFEST_FILE','SB5200_MAP_FILE','SB5200_SOURCE_REVISION')
    properties='\\n'.join('$<TARGET_PROPERTY:sb5200-fire-bridge-image,'+field+'>' for field in fields)+'\\n'
    # These are our absolute repository/temp paths, passed as CMake quoted
    # literals. Reject delimiters rather than guessing an escaping convention.
    for path in (ROOT,source):
        require(not any(c in str(path) for c in ('"',';','\\','\n')),'unsupported CMake path character')
    (source/'CMakeLists.txt').write_text('''cmake_minimum_required(VERSION 3.20)
project(accepted_export_consumer LANGUAGES NONE)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
'''+f'add_subdirectory("{ROOT}" module)\ninclude("{ROOT}/cmake/fire-bridge-candidate.cmake")\n'
        +f'file(GENERATE OUTPUT "${{CMAKE_BINARY_DIR}}/properties" CONTENT "{properties}")\n'
        +'''add_custom_command(OUTPUT "${CMAKE_BINARY_DIR}/verified"
COMMAND "${Python3_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/check.py" "${CMAKE_BINARY_DIR}/properties" "${CMAKE_BINARY_DIR}/verified"
DEPENDS sb5200-fire-bridge-image VERBATIM)
add_custom_target(consume ALL DEPENDS "${CMAKE_BINARY_DIR}/verified")
''')
    build=source/'build'
    run(['cmake','-S',str(source),'-B',str(build),'-G','Ninja','-DSB5200_FIRE_BRIDGE_SOURCE_REVISION='+pin])
    run(['cmake','--build',str(build),'--target','consume'])
    values=(build/'properties').read_text().splitlines()
    require(len(values)==4 and values[3]==pin,'CMake property tuple mismatch')
    for path,name in zip(values[:3],('startup.bin','startup-manifest.json','startup-map.json')):
        require(Path(path).read_bytes()==(expected_directory/name).read_bytes(),'CMake/CLI bytes differ: '+name)
    require((build/'verified').is_file(),'dependent consumer ran before artifacts existed')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cmake',action='store_true',help='also check real parent consumer dependency/property/artifact equality')
    args=parser.parse_args()
    try:
        with tempfile.TemporaryDirectory(prefix='sb52-accepted-exports-') as temporary:
            root=Path(temporary)
            for name,script,pin,expected in GENERATIONS:
                directory=root/name
                run([sys.executable,str(ROOT/'tools'/script),'--source-revision',pin,'--output-dir',str(directory)])
                validate(directory,pin,expected)
            if args.cmake:
                cmake_consumer(root,root/'fire-bridge')
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as error:
        parser.exit(1,str(error)+'\n')
    print('Eleven immutable development exports PASS; candidate flags unchanged'
          +('; CMake dependency/four properties/triple byte equality PASS' if args.cmake else ''))


if __name__=='__main__':
    main()
