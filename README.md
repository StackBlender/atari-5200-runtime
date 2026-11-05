# Atari 5200 Runtime

An original, open source replacement for the Atari 5200's startup and runtime
services, by [StackBlender](https://stackblender.com). The goal is to let emulators
run supported cartridges without requiring or distributing Atari's BIOS.

StackBlender is building this to completion and sharing it freely as a goodwill
gesture to the emulation community. The runtime is intended to be useful beyond
StackBlender's apps. No community contribution is needed to complete the work.

**Planning stage:** this repository currently contains documentation and a license.
There is no runtime implementation, generated image, build or compatibility claim.

## Intended design

Start with an original 6502 program for the 5200's 2 KiB system-ROM window at
`$F800–$FFFF`, including independently authored character graphics where needed.
The emulator executes the program through its existing CPU, memory, video,
audio and controller hardware. The initial reference profile is NTSC four-port;
other console variants require separate investigation.

The planned services include cartridge startup, reset, interrupt dispatch,
display shadows and controller/keypad processing. Their software addresses,
calling conventions and defaults must be established before implementation.
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

- Assign the runtime maintainer and establish the supported service/evidence contract.
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

There are no build or test commands yet. No Atari firmware is included. Implementation and integration acceptance remain
separate from this repository bootstrap.

## License

Copyright (c) 2026 StackBlender LLC.

GNU General Public License, version 3 or (at your option) any later version
(`GPL-3.0-or-later`); see [LICENSE](LICENSE). For other terms, contact
[StackBlender](https://stackblender.com).
