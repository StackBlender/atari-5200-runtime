# Atari 5200 Runtime working guide

StackBlender owns this public GPL-3.0-or-later project and intends to complete it
as a goodwill gesture. The human authorized development, commits and pushes.
Current repository owner/maintainer: apollo_retro_owner; coordinate writes through
Odin's repo:atari-5200-runtime lease. Separate observer/implementer roles must be
recorded before measured reconstruction; ownership does not establish a role split.
Do not wait for community contributions to do the work.

Read README.md, ROADMAP.md, docs/contract.md, docs/sources.md, docs/testing.md and
docs/handoff.md before work. Start from a roadmap item; update roadmap/handoff
with every slice, including scope, exact checks, evidence limits and next action.
Inspect git status and preserve others' changes. Keep commits coherent and push
passing work; explicit staged paths, StackBlender <noreply@stackblender.invalid>,
no AI attribution, force push or published-history rewrite.

## Original implementation

- Implement original 6502 runtime services, tools, assets and diagnostics. No
  second emulator or app UI. Emulator owners integrate and test their own cores.
- Never read/import Atari BIOS bytes, disassembly, extracted fonts/logos/tables,
  firmware instruction traces or firmware-bearing histories. No cartridge dumps.
- No reading or transplanting other emulator/kernel implementation code for this
  reconstruction. GPL licensing our own work does not relax independent authorship.
- Public behavioral descriptions need provenance screening. Quarantine
  disassembly-derived articles; do not promote their constants to facts by repetition.
- Maintain docs/sources.md with exposure, exact source sections, permitted role,
  confidence, unresolved behavior and original-probe expectations. Record unknowns.
- Documented hardware behavior, proposed software policy and measured original
  behavior are distinct. Tool tests and self-consistency do not prove BIOS equivalence.
- No oracle is available yet. Do not invent measurements or expected firmware
  responses, download firmware, buy hardware or use an unauthorized reference runner.
- Original source and independently authored assets may be committed. Generated
  images, map reports and private inputs/results remain ignored build/local files.
- Add SPDX-License-Identifier: GPL-3.0-or-later and StackBlender LLC copyright to
  new source. Preserve LICENSE verbatim and the README's version-3-or-later grant.

## Delivery and validation

Use docs/testing.md. Build offline; no downloads or network dependencies at
configure/runtime. No GitHub Actions or Fable. Keep at most two or three build
trees. Test independently expected encodings, allocation/failure boundaries and
fresh-process reproducibility; do not use the emitter's output as its own oracle.
Add CPU/device execution through the integration owner only after the service
contract is supported. No code in another owner's repo without explicit scope.

The tool fixture has zero runtime capabilities and must never be presented as a
usable BIOS replacement. No image provider target/release until real supported
services and an evidence-backed reset/cart handoff exist. Keep the ROM limit,
all RAM/stack ownership, original asset budget and overflow stop criteria explicit.
