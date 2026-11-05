# Atari 5200 Runtime roadmap

StackBlender will complete and freely share this original runtime. Initial scope
is NTSC four-port, followed by evidenced differences and broader compatibility.
The first image fixture is a build-tool test, not an implementation milestone
for cartridge startup.

## Next

Current slice: RUNTIME-004 bounded startup brief and complete original diagnostic
candidate. [docs/startup-brief.md](docs/startup-brief.md) proposal1 specifies
`cold-start-digits-v1` under the accepted `sb52-dev-cc65-v1` development interface:
explicit original MMIO/order, RAM/vector/SP/flags, failure loops, digit assets,
reset limits, cycle/stack targets and independent acceptance. It is pending Mars
scope/chip/reset/mapper review on req_6f74; no runtime service code is authorized
by the proposal itself. Historical final/retail VBI remains unknown/unselected.

Original digit metadata encoder and complete unapproved 32 KiB diagnostic layout
are implemented with eight independent tests (43 total). They do not execute a
CPU, select a mapper, provide a runtime or approve reference/owner execution.
Concrete next action: obtain Mars corrections/approval of this exact brief,
then implement the bounded image, report actual fit/stack/cycles, and request
Mars execution of the original diagnostic and provider integration. Continue
independent tooling only while scope review is pending; do not poll Odin.

1. **RUNTIME-002: approved startup and service evidence.** Build a per-service
   numeric ABI/evidence matrix from screened primary behavioral documentation
   and lawful original-system observations. Start with cartridge metadata/entry,
   cold reset, RAM/stack ownership and required initial vectors/registers.
   Preserve unknowns; do not implement a guessed jump-to-cart or software defaults.
   Primary PAM documentation now supplies cartridge-area/entry and RAM reservation
   rows with revision history. Next obtain exact software vector/shadow declarations,
   metadata encoding and entry/reset postconditions. Integration review accepts
   dated documentary facts; reconcile October/January VBI rules before selecting
   final/retail behavior. March's back-reference does not settle that policy.
   Selected NMOS capture semantics are now sourced independently. Public cc65
   declarations supply candidate vector/shadow offsets with a separate
   consumer-interface-unmeasured label, accepted for limited development scope; these
   do not establish Atari reset defaults or resolve final/retail VBI policy.
2. **RUNTIME-003: approve and pilot the original probe protocol.** The 26-byte
   capture fragment, scalar record contract and offline validator are implemented
   with 35 passing tests. Next review result ownership, metadata/mapper layout,
   interrupt window, readout, correction rules and named observer/reviewer roles.
   Identify actual reference access; none is available yet. The primary service
   manual distinguishes original/universal four-port boards; record exact board
   and firmware identities separately. No ROM/font/whole
   RAM or stack dumps, instruction traces or captured boot artwork.
3. **RUNTIME-004: real allocation and first supported startup.** Review original
   asset encoding/placement, code/vector/free margin and every RAM/stack use
   against the approved ABI. docs/allocation-plan.md/json now proposes a full
   2 KiB budget: 1024 asset + 768 code + 250 margin + 6 vectors; zero additional
   persistent RAM, a separately unproven stack allowance. Planning review accepted;
   proposal1 is now in docs/startup-brief.md for scope review. Implement the
   reviewed bounded startup scope, report actual
   image fit and remaining allowances, then execute original diagnostics through
   an integration owner. Stop on overflow for scope/architecture review.
4. Add the supported runtime service classes: NMI/VBI/DLI, IRQ/BRK dispatch,
   clocks/timers, display shadows, analog/keypad/fire scanning and character data.
   Each needs evidence, independently expected fixtures and explicit unsupported
   cases; all services/assets must fit together at acceptance.
5. Deliver reproducible image/map/manifest and generated read-only C++ provider
   through sb5200-runtime-image. Coordinate explicit provider selection, read/peek/
   DMA, reset reporting and strictly identity-bound synchronized saves with Mars.
6. Full service and authorized-cartridge validation, deterministic replay and
   lifecycle checks, followed by complete-app performance and device energy.
   Resolve discrepancies through completion; publish only supported claims.

## Landed

- RUNTIME-004 proposal1 defines concrete original startup policy and diagnostic
  acceptance without relabeling unknown retail behavior. No startup implementation
  or scope approval yet. Public cc65 chip-register declarations are separately
  recorded as consumer-interface-unmeasured; hardware effects await Mars review.
- Original digit metadata encoder and full unapproved diagnostic cartridge
  candidate: twenty title digits +two year digits, little-endian mapped entry,
  32 KiB layout with the original capture fragment and zero-fill holes. Eight
  tests cover independent bytes/layout, strict ASCII/types, bounds/overlap,
  fresh-process reproducibility and fail-before-output CLI. Total43 pass.

- Mars 1f411e5 accepts the public-interface boundary and digit-only convention
  for proposed sb52-dev-cc65-v1, plus the complete estimated allocation. No extra
  historical provenance needed merely to target the declarations. Services,
  defaults, actual fit/stack, complete cart and execution remain separate gates.

- RUNTIME-002 consumer-interface packet: pinned permissive cc65 declarations and
  documentation, exact vector/shadow candidates and exposure/hash ledger. Keeps
  consumer expectations separate from original Atari or measured facts; identifies
  cc65 conio storage and the 021C–021F reservation discrepancy. Metadata digit
  conventions are documentary candidates, not an approved bypass or full encoder.
- RUNTIME-004 allocation proposal: complete ROM ranges and future-service
  allowances, RAM ownership, original asset plan, margin/overflow stop rule and
  first implementation gates. No measured fit or stack-depth claim.

- RUNTIME-003 tooling: original 26-byte A/X/Y/status/SP capture fragment,
  deterministic source/encoder/fragment descriptor, draft role/operator protocol
  and strict bounded scalar-record validator. Rejects malformed/dump-shaped data
  and stale probe identities; preserves synthetic labels and inconclusive results.
  Thirty-five offline tests and CMake/CTest pass. Four factual opcode entries
  added after selected manufacturer CPU semantics review. No complete cartridge,
  metadata encoder, original execution or service implementation is implied.

- RUNTIME-002 integration review: dated documentary rows accepted; separate
  October partial, January VBI revision and March final-memo evidence profiles.
  Final/retail VBI policy remains null. Metadata uses CPU mapping, software saves
  retain the hardware interrupt frame, and boot prose does not authorize an MMIO
  sweep. ENTRY-01 still requires protocol review before execution.

- RUNTIME-002 documentary research: located and screened original Atari PAM
  memoranda. startup-evidence.md/json records factual rows, provenance/hash,
  October/January/March revisions, unresolved cells and an original ENTRY-01
  measurement plan. No BIOS source/assets, firmware execution or numeric guesses.
  Per-symbol vectors/shadows, metadata encoding and entry/reset defaults remain
  open; the research slice is not a completed runtime ABI.

- RUNTIME-001: original bounded emitter, explicit instruction/address-mode
  subset, symbolic absolute/relative fixups, mandatory CPU vectors, allocation
  and executable-label validation. Offline CMake/CTest and fresh-process
  reproducibility checks; no emulator, external assembler or downloaded code.
- Layout fixture emits four original instruction bytes and six vector bytes,
  with 2038 bytes unused in a 2048-byte image. This proves the tool's small
  fixture fits only; runtime services/fonts and their fit remain unimplemented.
- README/LICENSE public bootstrap. GPL-3.0-or-later, copyright StackBlender LLC.
  No community contribution is needed. Original source and evidence work remain ours.

## Decisions and limitations

- Original 6502 execution in F800–FFFF; no host HLE, direct-PC bypass, hidden
  RAM allocation or invented bank hardware. Initial NTSC four-port target is
  a development profile, not measured board compatibility.
- Current maintainer acts from Apollo Retro with an Odin repo lease. No separate
  runtime owner/queue is registered. Mars owns its emulator integration.
- Primary documentary ABI facts now exist; no original-system measurements,
  runtime services, font, cart boot, usable provider or game compatibility yet.
- Default external-BIOS behavior in consumers remains untouched. There is no
  replacement state/release or cross-version compatibility claim.
