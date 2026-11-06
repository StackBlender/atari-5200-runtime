# Atari 5200 Runtime

An original, open source replacement for Atari5200 startup/runtime services by
[StackBlender](https://stackblender.com). The goal is to run supported cartridges
without requiring or distributing Atari's BIOS. StackBlender is completing this
as a goodwill gesture to the community; no community contribution is required.

**Development software: not yet a complete BIOS replacement or general game runner.**

## What exists

An original6502 program executes in the2KiB F800..FFFF window through ordinary
CPU, bus, video, audio and input hardware emulation. Qualified development services
include cold startup, VBI clock/display shadows, DLI, analog scanning, IRQ/BRK/
timers, keypad windows and both fire sources for explicitly cooperating carts.
The latest callback-bridge refactor uses1895of2048bytes with90reserved bytes
untouched. Independent integration-owner Release/ASan diagnostics include input,
interrupt nesting, frame/cache/state/process replay and refusal checks; see the
[attributed execution receipts](docs/independent-execution.md).

These are limited development contracts, not original-hardware measurements or
broad game compatibility. Current input services reserve0600..061F and cannot be
silently applied to ordinary software using that RAM. Metadata is still digit-only;
full text/ordinary-RAM/remaining reset and service compatibility are current work.
Warm/CPU-only/host ControllerKey reset requests refuse; physical controller Reset
is a separate input. Speed and battery efficiency take priority over fine timing
accuracy, with dependable behavior and repeatable saves.

A separate [original printable glyph asset](docs/printable-glyphs.md) contains
95new drawings. It has no Atari encoding, runtime-bank binding or provider target.
Accepted runtime fonts and all eleven pinned generation inputs remain unchanged.

## Build and test

Requires Python3.10+, CMake3.20+, Ninja and Git; no compiler, emulator, firmware,
game download or network dependency is needed for offline authoring checks.

```sh
cmake -S . -B build -G Ninja
cmake --build build
ctest --test-dir build --output-on-failure
```

Or run all181offline methods directly:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The ordinary suite includes real reproduction of all eleven pinned development
exports and the CMake artifact consumer, plus rejection of altered bindings and
approval flags. Run it separately with `python3 tools/verify_accepted_exports.py
--cmake`; see the [catalog](docs/accepted-generations.md). Local source history is
required; the tool does not fetch it.

Generated images/maps/manifests/assets stay in ignored build directories.
Candidate opt-in artifact targets bind full source revision and exact outputs;
normal integration gates remain OFF. Export approval flags/capabilities remain
unchanged even after independent native receipts. There is no supported firmware
release, automatic BIOS fallback or bundled third-party cartridge.

## Evidence and next work

No Atari BIOS bytes/disassembly, extracted font/logo/table, foreign replacement
kernel/emulator implementation or firmware trace is used for reconstruction.
Documentary facts, consumer requirements, proposed original policy and independent
emulator observations are recorded separately. No original-system oracle or
measurement corpus is available. Licensing alone does not establish authorship.

[Roadmap](ROADMAP.md), [handoff](docs/handoff.md),
[source ledger](docs/sources.md), [testing](docs/testing.md),
[remaining services](docs/remaining-services-review.md) and
[contract](docs/contract.md) preserve scope, provenance and open compatibility gaps.
NTSC four-port is the initial target; other boards require explicit evidence.

## License

Copyright (c)2026 StackBlender LLC.

GNU General Public License, version3 or (at your option) any later version
(`GPL-3.0-or-later`); see [LICENSE](LICENSE). For other terms, contact
[StackBlender](https://stackblender.com).

A separately [authored opaque-title generation](docs/opaque-title-proof.md) removes
only the digit restriction on20title bytes. Numeric years and entry validation
remain. It requires independent native qualification before provider admission;
old generations/ABI/allocation/defaults remain unchanged.
