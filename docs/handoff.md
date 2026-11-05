# Runtime handoff

## Current slice

RUNTIME-001 original emitter/build foundation follows the owner's instruction to
start work and carry the public GPL project through completion. Current acting
maintainer is apollo_retro_owner, using the runtime repo's Odin lease. A dedicated
owner/queue is unassigned; do not invent registration or wait for contributors.

Paths: AGENTS.md, ROADMAP.md, CMakeLists.txt, .gitignore, tools/emitter.py,
tools/layout_fixture.py, tests/test_emitter.py, docs/contract.md, docs/sources.md,
docs/testing.md and README.md. LICENSE remains the bootstrap's verbatim GPLv3.
No dependencies, submodules, firmware, font, cartridges or external source added.

Validation: offline configure/build, one CTest running 17 original Python tests,
and fresh-process deterministic image/map generation. The fixture writes ten
bytes in a 2048-byte window; 2038 bytes remain. It has no runtime capabilities,
ABI or provider target and cannot boot a cartridge. Only tool fit is established.
Exact commands and evidence limits are docs/testing.md. Python 3.12.3 /
CMake 3.28.3 / Ninja configured and passed the suite in build/. Fresh-process
reproducibility is a test case, not a claim that a completed runtime was emitted.
This slice is committed/pushed with this handoff; inspect git status on resume.

## Resume

RUNTIME-002: screen primary behavioral sources and fill the numeric startup/cart/
reset and RAM/stack evidence matrix in docs/sources.md. No numeric Atari software
ABI is approved yet, and no original-system oracle is established. Do not reuse
quarantined disassembly-derived constants or write convenient reset defaults.
CPU-01 supports the common opcode encoding subset, not all NMOS CPU differences.
A dedicated NMOS processor reference and permitted Atari developer documentation
are next source needs. Keep source/exposure records current.

The tool-test allocation is not a runtime code/font layout. Real placement must
follow the approved software contract and reviewed full budget. Then implement a
bounded supported startup and get execution coverage from the integration owner;
this project contains no emulator. Mars integration remains coordinated by Retro
through req_6f74; no consumer pin/provider/API/state implementation has changed.
