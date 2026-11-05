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

Current direct unittest discovery and CMake/Ninja/CTest pass: 43 methods (17 image-emitter,
four original capture-fragment, 14 scalar-record, eight cartridge-candidate). Exact commands in docs/testing.md.
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

Review msg_d4a2 answered by Mars msg_001a / 1f411e5: accepts public declarations
for an explicit development interface, proposed sb52-dev-cc65-v1, with the same
consumer-interface-unmeasured label. No additional historical provenance needed
merely to target them. Accepts digits0–9 =>50–59 as OUR original convention,
20 title digits +two normal year digits, noFF bypass; metadata and little-endian
entry must be CPU mapped. Requires original glyph/mode/color mapping. Planning
budget accepted with no routing/alignment conflict; actual fit and32 stack bound
unproved. Protocol prose gaps addressed; no assembly/GPL implementation reviewed.

Concrete startup proposal1 is now docs/startup-brief.md: original limited
cold-start-digits-v1, explicit reset/MMIO write list and order, A/X/Y/flags/SP,
ZP/vector writes, no hidden RAM, fail-stop interrupts/invalid metadata, cold-only
reset, original digit assets and per-scope independent diagnostic expectations.
It leaves historical final/retail VBI unknown; ongoing services remain later work.
New public chip-header exposure/hashes are recorded as CONSUMER-02 in sources.md.
Scope/chip/reset/mapper review must precede runtime implementation/execution.

New tools/cartridge_candidate.py implements strict 20+2 ASCII-digit metadata and
little-endian entry encoding, plus complete unapproved 32 KiB original diagnostic
layout around the existing26-byte capture. tests/test_cartridge_candidate.py adds
eight independent tests; total43 methods pass directly and through CTest. No CPU
execution, runtime service code, image provider, reference approval or pin change.
Generate ignored build/entry-candidate artifacts per docs/testing.md; no default
build target selects them. Nested capture descriptor keeps its fragment-only
scope; enclosing candidate carries its own whole-image/layout-source identity.

Concrete resume: obtain Mars review/corrections on req_6f74 for startup-brief.md
proposal1 (prose only if implementation exposure is unwanted), then implement the
approved bounded image, prove actual allocation/cycles/stack and request original
diagnostic execution/integration through Mars. No reference-system execution:
operator/apparatus/result ownership and role receipts remain absent. Do not poll,
ack or reopen the incomplete main request. No need for more generic historical
research merely to target the already accepted development declarations.

Source PDFs/renders were isolated in /tmp, not committed or project dependencies:
PAM package, MOS selected CPU manual, cc65 declarations and Atari service manual.
The temporary pypdfium2/Pillow renderer is not needed by the offline build. CPU
facts/provenance and precise source sections/hashes are in docs/sources.md.
