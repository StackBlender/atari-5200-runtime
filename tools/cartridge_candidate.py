# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Author an unapproved diagnostic layout, not a runtime or execution permission."""
import argparse
import hashlib
import json
from pathlib import Path
from emitter import AssemblyError, integer
from entry_probe import capture_fragment

ORIGIN = 0x4000
END = 0xC000
METADATA = 0xBFE8
PROFILE = "sb52-dev-cc65-v1"


def digit_bytes(value, count, description):
    if type(value) is not str or len(value) != count or any(c not in "0123456789" for c in value):
        raise AssemblyError(f"{description} must contain exactly {count} ASCII digits")
    return bytes(ord(c) + 32 for c in value)


def communication_area(title, year, entry_address):
    """Our accepted digit-only convention; address is a CPU-mapped contract."""
    title_data = digit_bytes(title, 20, "title")
    year_data = digit_bytes(year, 2, "year")
    integer(entry_address, ORIGIN, METADATA - 1, "entry address")
    return title_data + year_data + entry_address.to_bytes(2, "little")


def diagnostic_candidate(title, year, entry_address=0x8000, result_start=0x3000):
    metadata = communication_area(title, year, entry_address)
    fragment, capture = capture_fragment(entry_address, result_start)
    image = bytearray(END - ORIGIN)  # Original fill policy; no imported data.
    start = entry_address - ORIGIN
    image[start:start + len(fragment)] = fragment
    image[METADATA - ORIGIN:] = metadata
    data = bytes(image)
    report = dict(schema=1, purpose="unapproved-diagnostic-cartridge-candidate",
                  proposed_interface=PROFILE, runtime_provider=False,
                  execution_approved=False, mapper_review_approved=False,
                  reference_execution_approved=False, original_measurement_claim=False,
                  proposed_mapping="unbanked-32k-4000-bfff", origin=ORIGIN,
                  size=len(data), fill=0, metadata_address=METADATA,
                  metadata_size=len(metadata), title=title, year_digits=year,
                  cartridge_sha256=hashlib.sha256(data).hexdigest(), capture=capture,
                  layout_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return data, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--year-digits", required=True)
    parser.add_argument("--entry-address", type=lambda v: int(v, 0), default=0x8000)
    parser.add_argument("--result-start", type=lambda v: int(v, 0), default=0x3000)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        image, report = diagnostic_candidate(args.title, args.year_digits,
                                             args.entry_address, args.result_start)
    except AssemblyError as error:
        parser.error(str(error))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "entry-candidate.bin").write_bytes(image)
    (args.output_dir / "entry-candidate.json").write_text(
        json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
