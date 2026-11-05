# Runtime handoff

## Resume the authorized batch

Owner authorized a large RUNTIME-002/003/004 batch on 2026-11-05. Runtime owner is
apollo_retro_owner; development/commits/pushes and public GPL-3.0-or-later are
explicitly authorized. No community contribution dependency. Acquire the Odin
repo:atari-5200-runtime lease before writes and release after push.

## Pushed work

- b699dff: tools/entry_probe.py generates an original 26-byte capture fragment and
  deterministic descriptor, not a runnable cartridge. Four fixed encodings added
  to tools/emitter.py (29 entries total); its ten-byte layout fixture is unchanged.
  tools/observations.py implements the strict bounded ENTRY-01 scalar record
  validator. docs/entry-observation-protocol.md defines roles, capture corrections,
  completion-write observation, reset/input sequences and inconclusive handling.
- ca643f9: docs/consumer-interface.md/json records permissive cc65 public ABI
  declarations at 77b6484615427746e55fda2755c9cbc320a1fb51, exact source hashes,
  shadow/vector candidates, digit metadata convention and exposure. Only headers,
  platform document and license reviewed; no startup/kernel/driver implementation.
  Facts remain consumer-interface-unmeasured, not Atari provenance or approval.
  cc65 conio0019–1C is consumer-owned; keep PAM reservation through021F despite
  cc65 app RAM from021C. Clock order/defaults remain unknown.
- Same slice: docs/allocation-plan.md/json proposes 1024 original font + 768 service
  code + 250 margin + 6 vectors =2048. No extra persistent RAM; stack32 is an
  estimate requiring analysis, not a reserved cartridge quota or proven depth.
- This handoff's slice: docs/hardware-profile.md records primary Atari board IDs:
  CA018087 original four-port, CA020108 universal four-port, CA021374 two-port.
  Exact board and firmware identities are separate, currently unmeasured.

All generated artifacts stay ignored. No firmware, copied fonts/art, commercial
games, foreign implementation, original execution or service-capable provider.
The source ledger preserves the earlier quarantined disassembly-derived article
exposure; do not backfill its constants.

## Validation

Direct unittest discovery and CMake/Ninja/CTest pass: 35 methods (17 image-emitter,
four original capture-fragment, 14 scalar-record). Exact commands in docs/testing.md.
Independent expected bytes, relocation/bounds, fresh-process reproducibility,
strict JSON size/depth/UTF-8/duplicates/types, identity, masking and inconclusive
handling covered. An initial depth rejection failure was fixed and retested.
Only synthetic records; no CPU/firmware or game execution. No reference result
exists. CMake still generates only the original ten-byte tool fixture, not a ROM.

Documentation checks: JSON parse, all 2048 allocation bytes covered once using the
existing Image/Region validator, code768/assets1024 totals, candidate vector and
ZP bounds, explicit null/unapproved policies, local Markdown links and whitespace.
The final hardware-identity slice changes documentation only.

## Coordination and concrete next action

Mars req_6f74 remains incomplete; do not ack/reopen or poll. Original integration
proposal is 3cde45c; budget sequencing b94c119, ownership/GPL e1dd041, primary
review739cc719 and correction acceptance a9a5fec4. Dated primary PAM rows are
accepted; October/January/March evidence profiles stay separate. January VBI-01
must not silently become final/retail policy; final_retail_vbi_policy remains null.

New actionable review sent as msg_d4a2 linked req_6f74: asks Mars whether public
consumer declarations/digit-only metadata can define an explicit development
scope, and reviews the full allocation proposal/protocol prerequisites. Asked
for documentary prose/tables only, excluding GPL tool/test implementation and
the protocol assembly block. Await a poke; no policy/provider/pin selected.

On response, resolve specific provenance/scope/allocation concerns. If approved,
define the exact development profile, numeric startup MMIO/default policy and
metadata encoder; build the first complete original diagnostic, then a bounded
supported runtime with actual fit. Until then continue primary evidence or
protocol review, not guessed service code. Exact reset/register defaults,
interrupt/shadow semantics, asset encoding, stack analysis and original operator/
role/access/readout/result-area approvals remain open. No hardware/oracle exists.

Source PDFs/renders were isolated in /tmp, not committed or project dependencies:
PAM package, MOS selected CPU manual, cc65 declarations and Atari service manual.
The temporary pypdfium2/Pillow renderer is not needed by the offline build. CPU
facts/provenance and precise source sections/hashes are in docs/sources.md.
