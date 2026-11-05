# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Export original candidate artifacts, with no execution/provider approval gate."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from startup_image import startup_image
from emitter import AssemblyError, report_json

INPUTS = ("CMakeLists.txt", "tools/emitter.py", "tools/startup_image.py",
          "tools/export_candidate.py", "docs/allocation-plan.json")


def source_revision(value):
    if type(value) is not str or not re.fullmatch(r"[0-9a-f]{40}", value):
        raise AssemblyError("source revision must be a full lowercase 40-hex commit")
    return value


def candidate(revision):
    revision = source_revision(revision)
    image, mapping = startup_image()
    mapping["source_revision"] = revision
    map_text = report_json(mapping)
    manifest = dict(schema=1, abi=1, runtime_abi="sb52-dev-cc65-v1",
                    version="cold-start-digits-v1.candidate1",
                    profile="ntsc-four-port-development", source_revision=revision,
                    purpose="candidate-for-independent-integration",
                    authored_capabilities=["cold-start-digits-v1"], capabilities=[],
                    execution_verified=False, provider_approved=False,
                    retail_compatibility=False,
                    image=dict(origin=0xF800, size=2048, sha256=hashlib.sha256(image).hexdigest()),
                    map_sha256=hashlib.sha256(map_text.encode("utf-8")).hexdigest(),
                    reset_policy=dict(supported=["cold"],
                                      unsupported=["warm", "cpu-only", "controller-reset"],
                                      reject_unsupported_before_mutation=True),
                    mapper=dict(board="Linear32K", program_size=32768,
                                successful_load_required=True),
                    symbols=mapping["symbols"],
                    fault_symbols={key: mapping["symbols"][key]
                                   for key in ("nmi_fault", "irq_fault", "startup_fault")},
                    timing=dict(base_cycles_max=1091, full_cycle_target=4096,
                                full_cycles_verified=False),
                    provenance=dict(encoder_sha256=mapping["encoder_sha256"],
                                    startup_source_sha256=mapping["source_sha256"],
                                    allocation_sha256=mapping["allocation_sha256"],
                                    exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    return image, map_text, report_json(manifest)


def verify_checkout(root, revision):
    """Each emitted input must be byte-identical to the explicitly named commit."""
    source_revision(revision)
    try:
        for relative in INPUTS:
            pinned = subprocess.run(["git", "-C", str(root), "show", revision+":"+relative],
                                    capture_output=True, check=True, timeout=10).stdout
            if (root/relative).read_bytes() != pinned:
                raise AssemblyError("export input differs from pinned source: "+relative)
    except (OSError, subprocess.SubprocessError) as error:
        raise AssemblyError("cannot verify pinned export checkout") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        verify_checkout(Path(__file__).resolve().parents[1], args.source_revision)
        image, mapping, manifest = candidate(args.source_revision)
    except AssemblyError as error:
        parser.error(str(error))
    # Validate all content before creating any output. No wall clock/host paths.
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, data in [("startup.bin", image), ("startup-map.json", mapping.encode("utf-8")),
                       ("startup-manifest.json", manifest.encode("utf-8"))]:
        path = args.output_dir/name
        if not path.exists() or path.read_bytes() != data:
            temporary = path.with_suffix(path.suffix+".tmp")
            temporary.write_bytes(data)
            temporary.replace(path)


if __name__ == "__main__":
    main()
