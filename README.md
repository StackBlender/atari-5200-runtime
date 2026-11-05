# Atari 5200 Runtime

An original, open source replacement for the Atari 5200's startup and runtime
services, by [StackBlender](https://stackblender.com). The goal is to let emulators
run supported cartridges without requiring or distributing Atari's BIOS.

StackBlender is building this to completion and sharing it freely as a goodwill
gesture to the emulation community. The runtime is intended to be useful beyond
StackBlender's apps. No community contribution is needed to complete the work.

**Development started:** the repository contains an original bounded 6502 emitter,
an offline build, an original register-capture fragment and 35 tool-contract
tests. The generated layout fixture has
zero runtime capabilities. Cartridge startup and runtime services are not yet
implemented; no compatibility is claimed.

## Intended design

Start with an original 6502 program for the 5200's 2 KiB system-ROM window at
`$F800–$FFFF`, including independently authored character graphics where needed.
The emulator executes the program through its existing CPU, memory, video,
audio and controller hardware. The initial reference profile is NTSC four-port;
other console variants require separate investigation.

The planned services include cartridge startup, reset, interrupt dispatch,
display shadows and controller/keypad processing. Primary Atari developer memoranda now document the cartridge communication
area, RAM reservations and some calling conventions; see the
[startup evidence](docs/startup-evidence.md). Missing addresses, defaults and
retail validation remain explicit before implementation.
Speed and efficient execution matter, with dependable play and repeatable saves;
cycle-for-cycle equivalence is not the initial goal.

The module should remain independent of any emulator or app UI. Planned integration
with StackBlender's Mars core uses explicit provider selection, ordinary reset-vector
execution and save states bound to the replacement's immutable identity. These are
proposed interfaces, not currently available features.

## Evidence and original work

Use documented behavior with recorded provenance and independent black-box
observations of original systems. Separate documented, measured, proposed and
unknown behavior. No original-system reference operator or measurement corpus is
established yet.

Do not include Atari BIOS bytes or disassembly, extracted fonts, logos, tables,
third-party games or copied emulator implementations. Author the code, diagnostic
programs and assets independently. Disassembly-derived descriptions are not approved
implementation specifications without independently permitted evidence. Keep a source
and exposure ledger; do not label unmeasured behavior as verified compatibility.

## Work to completion

- Establish the supported service/evidence contract. StackBlender is maintaining
  the project; current work and recovery details are in [ROADMAP.md](ROADMAP.md)
  and [docs/handoff.md](docs/handoff.md).
- Define startup/reset semantics, original asset encoding and a reviewed allocation
  budget covering code, assets, vectors, free space and all RAM/stack ownership.
- Establish reference access or an explicitly scoped documentary baseline.
- Build a bounded original prototype and report its actual image/map fit. A partial
  prototype proves only its own scope fits; all supported services must fit together.
  Overflow requires a reviewed scope or architecture change.
- Add an offline reproducible build, original diagnostics and independent expected
  results, followed by emulator integration and cartridge testing.
- Complete the startup and ongoing runtime service inventory, including reset,
  interrupts, display, input, timers and character access. Resolve evidence gaps
  and compatibility failures through the full implementation and validation effort.
  The initial prototype and NTSC profile are milestones toward completion.

## Build and test the foundation

Requires Python 3.10+, CMake 3.20+ and Ninja. No firmware, game, external assembler
or network download is needed.

```sh
cmake -S . -B build -G Ninja
cmake --build build
ctest --test-dir build --output-on-failure
```

The build generates an original 2 KiB **tool fixture**, `build/generated/layout-test.bin`,
and its JSON allocation/hash report. Four instruction bytes and six vector bytes
are written; 2038 bytes remain unused. This demonstrates emitter layout only,
with no claim that the eventual runtime and font fit or work. It must not be
selected as a BIOS replacement.

[Diagnostic protocol](docs/entry-observation-protocol.md),
[testing](docs/testing.md), [contract](docs/contract.md) and
[source/evidence ledger](docs/sources.md) describe the checks and remaining work.

## License

Copyright (c) 2026 StackBlender LLC.

GNU General Public License, version 3 or (at your option) any later version
(`GPL-3.0-or-later`); see [LICENSE](LICENSE). For other terms, contact
[StackBlender](https://stackblender.com).
