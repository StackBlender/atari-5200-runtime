# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Export a separately versioned cumulative both-fire candidate for explicit adapter review."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from emitter import AssemblyError, report_json
from export_candidate import candidate as baseline_candidate, source_revision, verify_checkout
from fire_bridge_image import fire_bridge_image

EXTRA_INPUTS = ("tools/fire_bridge_image.py", "tools/export_fire_bridge_candidate.py",
                "cmake/fire-bridge-candidate.cmake", "docs/fire-profile.json", "docs/fire-allocation.json")


def candidate(revision):
    revision = source_revision(revision)
    image, mapping = fire_bridge_image()
    mapping["source_revision"] = revision
    map_text = report_json(mapping)
    # Shared reset/mapper policy stays identical, without editing baseline inputs.
    _, _, baseline_text = baseline_candidate(revision)
    manifest = json.loads(baseline_text)
    manifest.update(version="cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.dli-dispatch-v1.analog-shadow-v1.irq-brk-dispatch-v1.timer-dispatch-v1.keypad-irq-latch-v1.keypad-windows-v1.both-fire-v1.bridge-refactor-v1.candidate1",
                    authored_capabilities=mapping["authored_capabilities"],
                    image=dict(origin=0xF800, size=2048, sha256=mapping["sha256"]),
                    map_sha256=hashlib.sha256(map_text.encode("utf-8")).hexdigest(),
                    symbols=mapping["symbols"],
                    fault_symbols={key: mapping["symbols"][key]
                                   for key in ("nmi_fault", "irq_fault", "startup_fault")},
                    runtime_abi="sb52-dev-input-fire-v3",
                    profile="ntsc-four-port-cooperating-input-fire-development",
                    cooperating_cart=json.loads((Path(__file__).resolve().parents[1]/
                        "docs/fire-profile.json").read_text()),
                    timing=dict(base_cycles_max=1478, full_cycle_target=4096,
                                full_cycles_verified=False,
                                irq_dispatch_full_cycle_target=512,
                                irq_dispatch_full_cycles_verified=False,
                                timer_full_cycles_verified=False,
                                default_vbi_full_cycles_verified=False,
                                default_vbi_full_cycle_target=4096,
                                analog_complete_base_cycles=136,
                                conditions="cooperating-cart activation, each key/fire callback<=128 nominal cycles, at most6 sequential callbacks; no arbitrary RDY or callback guarantee"),
                    startup_interrupt_acceptance_observation_required=True,
                    provenance=dict(encoder_sha256=mapping["encoder_sha256"],
                                    startup_source_sha256=mapping["source_sha256"],
                                    baseline_startup_source_sha256=mapping["baseline_startup_sha256"],
                                    allocation_sha256=mapping["allocation_sha256"],
                                    exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                    baseline_exporter_sha256=manifest["provenance"]["exporter_sha256"]))
    return image, map_text, report_json(manifest)


def verify_fire_bridge_checkout(root, revision):
    verify_checkout(root, revision)
    try:
        for relative in EXTRA_INPUTS:
            pinned = subprocess.run(["git", "-C", str(root), "show", revision+":"+relative],
                                    capture_output=True, check=True, timeout=10).stdout
            if (root/relative).read_bytes() != pinned:
                raise AssemblyError("export input differs from pinned source: "+relative)
    except (OSError, subprocess.SubprocessError) as error:
        raise AssemblyError("cannot verify pinned fire bridge export checkout") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        verify_fire_bridge_checkout(Path(__file__).resolve().parents[1], args.source_revision)
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
