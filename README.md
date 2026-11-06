# Atari 5200 Runtime

An original, open source replacement for the Atari 5200's startup and runtime
services, by [StackBlender](https://stackblender.com). The goal is to let emulators
run supported cartridges without requiring or distributing Atari's BIOS.

StackBlender is building this to completion and sharing it freely as a goodwill
gesture to the emulation community. The runtime is intended to be useful beyond
StackBlender's apps. No community contribution is needed to complete the work.

**First bounded startup authored:** an original 2 KiB image now implements the
approved development-only cold-start/digit-metadata scope and original digit
assets. It fits with 871 bytes unwritten, including the untouched 250-byte margin.
Fifty-seven offline tool/image/export tests pass. The integration owner now reports bounded CPU/chip execution, stall-inclusive
timing, development-provider and state/replay checks passing; see the
[independent receipt](docs/independent-execution.md). Cartridge compatibility
and supported product integration remain unverified.
A separate approved-scope VBI/clock extension is now authored and fits with804
bytes unwritten;66 offline checks pass. The integration owner reports independent interrupt/clock/state checks passing,
with startup at most1204 full cycles and default VBI handler at most95 for the
DMA-off diagnostics; see the [execution receipt](docs/independent-execution.md).
The development adapter change awaits a separately authorized release.
Input scanning, display shadows and further interrupt services remain future work.

## Intended design

Start with an original 6502 program for the 5200's 2 KiB system-ROM window at
`$F800–$FFFF`, including independently authored character graphics where needed.
The emulator executes the program through its existing CPU, memory, video,
audio and controller hardware. The initial reference profile is NTSC four-port;
other console variants require separate investigation.

The planned services include cartridge startup, reset, interrupt dispatch,
display shadows and controller/keypad processing. Primary Atari developer memoranda now document the cartridge communication
area, RAM reservations and some calling conventions; see the
[startup evidence](docs/startup-evidence.md). An explicit original development
startup policy is proposed in the
[startup brief](docs/startup-brief.md); service approval and retail validation
remain separate requirements.
Speed and efficient execution matter, with dependable play and repeatable saves;
cycle-for-cycle equivalence is not the initial goal.

The module should remain independent of any emulator or app UI. Planned integration
with StackBlender's Mars core uses explicit provider selection, ordinary reset-vector
execution and save states bound to the replacement's immutable identity. A bounded development integration is independently reported; broader supported
integration remains future work.

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
selected as a BIOS replacement. The build also emits the separately named
`build/generated/startup.bin` and `startup-map.json` for the authored bounded
scope. See [fit/execution packet](docs/startup-proof.md); bounded execution evidence is recorded separately in the
[independent receipt](docs/independent-execution.md). The separate [candidate export target](docs/candidate-export.md)
provides image/map/manifest for integration, with no provider/release approval.

[Diagnostic protocol](docs/entry-observation-protocol.md),
[testing](docs/testing.md), [contract](docs/contract.md) and
[source/evidence ledger](docs/sources.md) describe the checks and remaining work.

## License

Copyright (c) 2026 StackBlender LLC.

GNU General Public License, version 3 or (at your option) any later version
(`GPL-3.0-or-later`); see [LICENSE](LICENSE). For other terms, contact
[StackBlender](https://stackblender.com).


The separately authored [display-shadow candidate](docs/display-shadow-proof.md)
extends the bounded VBI clock with display-list/color/DMA shadow transfer. It fits
within the existing2 KiB allocation and passes offline encoding/export tests.
Independent CPU/render/state acceptance is pending; this is still not a complete
BIOS replacement or evidence of playable games.


A separate [DLI dispatch candidate](docs/dli-dispatch-proof.md) adds the original
cartridge callback route for display-list interrupts. Offline checks pass; actual
DLI/raster and replay acceptance remain pending alongside display-shadow execution.


Independent Mars execution now accepts the bounded display-shadow and DLI
candidates: actual writes/rendering, callback/interrupt handling and synchronized
process replay pass per the [receipt](docs/independent-execution.md). Input/timer/
reset completion, games and product enablement remain open. All candidate export
flags stay false; integration changes await a separately approved release.


The original [eight-axis analog candidate](docs/analog-shadow-proof.md) now
primes hardware conversion at cold startup and copies completed samples for
four controllers during eligible VBI. Offline tests pass; actual acquisition/
state acceptance is pending. Keypad/fire services and complete game support
remain unfinished.


The eight-axis analog candidate now has independent Mars execution/state replay
acceptance; see the receipt above. Keypad delivery under the selected03 scan
mode remains unresolved and is not a supported service. No complete BIOS/game
compatibility follows from the accepted analog subset.


A separate original [IRQ/BRK candidate](docs/irq-brk-proof.md) routes CPU
interrupts to cartridge callbacks with stack-wrap handling. Offline tests pass;
independent execution remains pending. Device-source acknowledgment and all
remaining keypad/fire/timer/reset services are separate unfinished work.


The original [timer-dispatch candidate](docs/timer-dispatch-proof.md) adds three
POKEY timer callbacks and moves vector initialization into a shared helper to
leave room in startup. Offline checks pass; real timer/source/RTI/state acceptance
is pending. No timer rates or interrupts are automatically enabled.


The IRQ/BRK and timer candidates now have independent Mars CPU/stack/callback/
state acceptance; see the receipt above. The complete firmware replacement still
needs reliable keypad/fire and reset/remaining-service validation. Integration
release/app adoption remains separate; all candidate export flags stay false.


An original [keypad/fire policy proposal](docs/keypad-fire-brief.md) and offline
event model now define the next review slice. Acquisition, interrupt races and
explicit RAM ownership still need review before a new executable candidate;
the planning model does not establish working keypad/fire hardware services.


A separate [keypad IRQ latch candidate](docs/keypad-irq-proof.md) now supplies
original executable capture and interrupt-ownership plumbing for cooperating
diagnostic cartridges, with an explicit new32-byte RAM/profile contract. It
fits2048 bytes with the250-byte margin intact. Automatic port rotation, input
events and both-fire services remain unfinished; native execution is pending.


The keypad IRQ latch foundation now has independent Mars CPU/interrupt/fast-
analog/state acceptance for its explicit cooperating-cart development profile;
see the execution receipt. Automatic port rotation, contact callbacks and both
fire services remain unfinished. No complete firmware or game support is implied.
