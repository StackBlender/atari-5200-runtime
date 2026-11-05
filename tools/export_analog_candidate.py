# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Export a separately versioned analog-shadow candidate for explicit adapter review."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from emitter import AssemblyError, report_json
from export_candidate import candidate as baseline_candidate, source_revision, verify_checkout
from analog_shadow_image import analog_shadow_image

EXTRA_INPUTS = ("tools/analog_shadow_image.py", "tools/export_analog_candidate.py",
                "cmake/analog-shadow-candidate.cmake")


def candidate(revision):
    revision = source_revision(revision)
    image, mapping = analog_shadow_image()
    mapping["source_revision"] = revision
    map_text = report_json(mapping)
    # Shared reset/mapper policy stays identical, without editing baseline inputs.
    _, _, baseline_text = baseline_candidate(revision)
    manifest = json.loads(baseline_text)
    manifest.update(version="cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.dli-dispatch-v1.analog-shadow-v1.candidate1",
                    authored_capabilities=mapping["authored_capabilities"],
                    image=dict(origin=0xF800, size=2048, sha256=mapping["sha256"]),
                    map_sha256=hashlib.sha256(map_text.encode("utf-8")).hexdigest(),
                    symbols=mapping["symbols"],
                    fault_symbols={key: mapping["symbols"][key]
                                   for key in ("nmi_fault", "irq_fault", "startup_fault")},
                    timing=dict(base_cycles_max=1131, full_cycle_target=4096,
                                full_cycles_verified=False,
                                default_vbi_base_cycles_min=240,
                                default_vbi_base_cycles_max=245,
                                default_vbi_full_cycle_target=512,
                                default_vbi_full_cycles_verified=False,
                                analog_complete_base_cycles=71,
                                analog_pending_base_cycles=10,
                                pending_vbi_base_cycles_min=179,
                                pending_vbi_base_cycles_max=184,
                                dli_dispatch_base_cycles=30,
                                dli_dispatch_full_cycle_target=128,
                                dli_dispatch_full_cycles_verified=False,
                                default_vbi_conditions="DMA-off, ordinary refresh, no custom callbacks or held RDY"),
                    startup_interrupt_acceptance_observation_required=True,
                    provenance=dict(encoder_sha256=mapping["encoder_sha256"],
                                    startup_source_sha256=mapping["source_sha256"],
                                    baseline_startup_source_sha256=mapping["baseline_startup_sha256"],
                                    allocation_sha256=mapping["allocation_sha256"],
                                    exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                    baseline_exporter_sha256=manifest["provenance"]["exporter_sha256"]))
    return image, map_text, report_json(manifest)


def verify_analog_checkout(root, revision):
    verify_checkout(root, revision)
    try:
        for relative in EXTRA_INPUTS:
            pinned = subprocess.run(["git", "-C", str(root), "show", revision+":"+relative],
                                    capture_output=True, check=True, timeout=10).stdout
            if (root/relative).read_bytes() != pinned:
                raise AssemblyError("export input differs from pinned source: "+relative)
    except (OSError, subprocess.SubprocessError) as error:
        raise AssemblyError("cannot verify pinned analog export checkout") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        verify_analog_checkout(Path(__file__).resolve().parents[1], args.source_revision)
        image, mapping, manifest = candidate(args.source_revision)
    except AssemblyError as error:
        parser.error(str(error))
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
