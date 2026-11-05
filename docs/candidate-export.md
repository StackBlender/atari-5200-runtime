<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Candidate artifact export for Mars

Mars msg_1678 /c50e58a requests this boundary after accepting the first bounded
artifact/fit receipt. It enables independent execution; it does not depend on
execution having passed. Image bytes remain unchanged at SHA256
b2d8ebb8d0070f2aee1bd79d7adfee85b88797702cb96035ab3a18e9bd37f68d.

## Build

Use Python3.10+, CMake3.20+, Ninja and Git with a pinned committed checkout.
No network, external assembler, compiler, header import or runtime dependency:

```sh
cmake -S . -B build -G Ninja
cmake --build build --target sb5200-runtime-image
ctest --test-dir build --output-on-failure
```

By default configure resolves the checkout's full HEAD. A consumer may pass
`-DSB5200_SOURCE_REVISION=<full-lowercase-40-hex-commit>` explicitly. Export checks
that every generation input matches that commit byte-for-byte before creating
outputs: CMakeLists.txt, tools/emitter.py, tools/startup_image.py,
tools/export_candidate.py and docs/allocation-plan.json. Commit authored changes
before building the export; modified inputs fail instead of mislabeling their
revision. Unrelated documentation edits do not affect the image. Reconfigure
when changing the selected pin. A source archive without the pinned Git objects
is not currently supported.

## Target contract

`sb5200-runtime-image` is an offline artifact target, usable through
add_subdirectory with a separate binary directory. Its four properties are:

| Property | Meaning |
| --- | --- |
| SB5200_IMAGE_FILE | Absolute generated path to candidate/startup.bin |
| SB5200_MANIFEST_FILE | Absolute generated path to candidate/startup-manifest.json |
| SB5200_MAP_FILE | Absolute generated path to candidate/startup-map.json |
| SB5200_SOURCE_REVISION | Full pinned source commit, never a branch/tag/short SHA |

The target produces all three files before dependent Mars generation. Mars must
add_dependencies on sb5200-runtime-image, obtain the properties and depend on
these artifact paths for its conversion command. BYPRODUCTS makes the generating
relationship explicit to Ninja. The target verifies inputs on every invocation;
unchanged files are not rewritten. No generated C++ header or implementation is
imported from this GPL module. Mars owns artifact validation and conversion to
its own read-only byte provider. Default external-BIOS selection remains unchanged.

## Descriptor

Manifest schema1/ABI1 names sb52-dev-cc65-v1, candidate version, NTSC four-port
development profile, full source revision,2048-byte image origin/hash, full map
hash, source/encoder/allocation/exporter hashes, Linear32K/32768 successful-load
requirement, cold-only reset policy and exact symbol/fault map. It carries the
1091 base-cycle maximum and4096 full-cycle target with full_cycles_verified=false.
The map adds the same source_revision to its existing allocations/symbols/hash.
No timestamps, absolute checkout paths or generated output paths enter artifacts.
The full pin and map hash change with a revision even when image bytes do not.

`authored_capabilities=[cold-start-digits-v1]` distinguishes authored scope from
`capabilities=[]`, `execution_verified=false` and `provider_approved=false`.
These false values must not prevent exporting or staging the candidate whose
execution is to be reviewed. They must not be promoted to true by file generation.
No release, accepted state ABI, reference execution or retail compatibility follows.

## Verification and next owner action

Seven new tests check exact image identity, full revision formatting, complete
manifest/map identity and independent fault addresses, false approval flags,
revision-bound deterministic output, modified-input rejection, checking every
export input and invalid CLI no-output behavior. Total57 offline tests pass.
A parent CMake harness additionally must build the target, read all four
properties and verify three existing absolute artifacts, hashes/full revision,
unchanged image and dependency ordering. Record that build receipt in the handoff.

Next Mars stages opt-in provider, structured reset/status and instruction-boundary
observer, independently executes the original positive/negative/write/asset
fixtures, counts refresh/RDY cycles, then validates identity-bound synchronized
states/raw rejection and lifecycle. Consumer/release adoption comes afterward.
See startup-proof.md for the exact open execution gates; no repeat scope/fit
review is needed for the unchanged image.
