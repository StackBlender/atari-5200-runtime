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
silently applied to ordinary software using that RAM. The qualified opaque-title
variant accepts arbitrary20title bytes with digit-only years;
full text/ordinary-RAM/remaining reset and service compatibility are current work.
Warm/CPU-only/host ControllerKey reset requests refuse; physical controller Reset
is a separate input. Speed and battery efficiency take priority over fine timing
accuracy, with dependable behavior and repeatable saves.

A separate [original printable glyph asset](docs/printable-glyphs.md) contains
95new drawings. It has no Atari encoding, runtime-bank binding or provider target.
Accepted runtime fonts and all thirteen pinned generation inputs remain unchanged.

## Build and test

Requires Python3.10+, CMake3.20+, Ninja and Git; no compiler, emulator, firmware,
game download or network dependency is needed for offline authoring checks.

```sh
cmake -S . -B build -G Ninja
cmake --build build
ctest --test-dir build --output-on-failure
```

Or run all237offline methods directly:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The ordinary suite includes real reproduction of all thirteen pinned development
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

A [callable-reset generation](docs/callable-reset-proof.md) rebuilds only the reset region of
the cart-owned diagnostic parent: an instruction boundary at +$0F, fall-through to the cartridge
handoff at +$8A, so software that copies the reset routine to RAM and calls it as a subroutine
works. Offline tests pass (242); a licensed target reaches its menu through the stock external-bios
debug path. Not Mars-qualified or admitted.

## License

Copyright (c)2026 StackBlender LLC.

GNU General Public License, version3 or (at your option) any later version
(`GPL-3.0-or-later`); see [LICENSE](LICENSE). For other terms, contact
[StackBlender](https://stackblender.com).

A separately [authored opaque-title generation](docs/opaque-title-proof.md) removes
only the digit restriction on20title bytes. Numeric years and entry validation
remain. Mars d5c709f independently qualified it in both native builds; it remains
unreleased;
old generations/ABI/allocation/defaults remain unchanged.

A [conditional timer memory audit](docs/timer-memory-audit.md) inventories every
original runtime code path/default-handler frontier without executing a CPU. It
supports ordinary-RAM planning, not an approved profile or game-compatibility claim.

The separately [authored original64 bank](docs/character-bank-proof.md) binds
64original development labels, preserving legacy digits/high bank/code. It is
independently qualified by Mars938d829 in both native builds; no historical charset or ordinary
software compatibility is claimed. Normative own geometry is available as source
asset DATA in assets/printable-geometry.json for independent pixel oracles.

Separate B0ordinary-RAM identity and B1original diagnostic full-cold experiments
are authored under Mars81025cf, NOT admitted. See docs/timer-experiments-proof.md
(or timer-experiments-proof.md from docs).205offline methods include eight new
contract/encoding/timing/pin/failure checks. Old13exports/flags/defaults preserved;
no combined profile or unchanged-game run.

B2's separate [conditional-year experiment](docs/diagnostic-conditional-proof.md)
permits any first year only with secondFF, retaining full cold initialization.
It does not amend B1 or combine ordinary RAM, and requires independent admission.
212offline checks including exact committed CLI/CMake consumer; no game trial.

The explicitly [combined cart-owned diagnostic profile](docs/cart-owned-diagnostic-proof.md)
now rebinds B0ownership onto byte-identical B2code under its own identity. It is
independently qualified for its bounded development contract; see the
[native receipt](docs/cart-owned-diagnostic-native-receipt.md). Game mapping and
consumer trial decisions remain separate. All prior profiles/defaults stay unchanged.

A separately [guarded Linear8K development identity](docs/linear8k-guarded-proof.md)
keeps all2048combined ROM bytes unchanged and declares REQUIRED native immutable
board/length/entry/handoff guards. Its exact pinned exporter/CMake and ORIGINAL
8192-byte diagnostic layout pass offline checks. Native integration/qualification
is pending; this is not8KiB game admission or a new implemented6502validator.


An [original startup/display diagnostic](docs/startup-display-probe-proof.md) now
exports twelve self-initializing cartridge controls (32KiB baseline/exact8KiB,
direct MMIO versus VBI shadows, numeric/secondFF Cold). Counter and geometric
bitmap expectations are independently specified. Offline authoring is qualified;
native execution,8KiB guard and all product/compatibility gates remain separate.


The four32KiB startup/display controls now [independently pass native Release and
full-native ASan](docs/startup-display-native-receipt.md), including first fetch,
CPU progress, actual display DMA, VBI shadow provenance and every geometric pixel.
The eight8KiB controls await native guard qualification. This baseline result
does not establish general game compatibility or a complete BIOS replacement.
