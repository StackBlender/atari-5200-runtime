# Runtime handoff

## Active batch / resume

Owner authorized a large RUNTIME-002/003/004 batch on 2026-11-05. First slice:
original ENTRY-01 tooling, protocol and selected primary NMOS semantics. New
files: tools/entry_probe.py, tools/observations.py, tests/test_entry_probe.py,
tests/test_observations.py, docs/entry-observation-protocol.md. emitter.py adds
fixed_instruction and four encodings (29 total); its original layout output is
unchanged. README, contract, sources, startup evidence, testing and roadmap updated.

Validation: direct unittest discovery passes all 35 methods; CMake configure,
build and CTest pass. A first run exposed missing JSON depth enforcement, now
bounded explicitly; invalid UTF-8, duplicate/non-finite keys, stale identities,
unknown fields/dump attempts and reset/readout order covered. Synthetic inputs
only. No CPU, complete cartridge, original firmware or service executed. Probe
stack/result ownership and metadata/operator/role review remain open.

First slice pushed as b699dff. Second slice adds consumer-interface.md/json and
allocation-plan.md/json. cc65 revision 77b6484615427746e55fda2755c9cbc320a1fb51
public headers/docs/license only: candidate exact vector/shadow addresses,
consumer-owned conio fields and the cc65 021C versus PAM 0220 free-RAM discrepancy.
No startup/kernel/driver/assembler implementation read. Facts remain
consumer-interface-unmeasured, not approved Atari runtime policy. Primary startup
unknowns and final/retail VBI selection remain explicit. The full 2 KiB proposal
reserves 1024 font, 768 service code, 250 margin and 6 CPU vectors; no additional
persistent RAM or proven stack depth. Continue: send the completed evidence,
protocol and allocation proposal to Mars for specific scope/provenance review. No runtime policy is selected or
provider enabled. Acquire the runtime lease for edits; push each passing slice.

## Current slice

RUNTIME-002 documentary startup research is committed/pushed with this handoff.
Retro owns/maintains the repo under its Odin lease. No separate runtime owner
needs assignment. No observer/implementer role split or original execution is
claimed by a documentary review.

New docs/startup-evidence.md/json: original Atari PAM Package behavioral memo
facts, source SHA-256, page/revision provenance, unknown numeric fields, and
ENTRY-01 scalar observation plan. Updated sources, contract, README, AGENTS and
roadmap. No source code, dependency, artifact generator or consumer pin changed.
Documentation validation: JSON parsed, field layout/ranges checked, local links
and staged diff whitespace checked. Existing emitter acceptance remains 17 tests.
No firmware, copied manual text/scans, assets, manufacturer source or games in Git.

## Integration review receipt

Mars accepted the dated primary rows in msg_7eb0 / req_6f74, review commit
739cc71932e6bda4987ee14b08eeba49223a5975. No integration conflict found;
this is not provider approval. Separate documentary revision profiles now appear
in startup-evidence.md/json; final_retail_vbi_policy remains null because March's
back-reference does not reconcile October and January. VBI-01 is January-only.
Metadata must use CPU cart mapping; software dispatch saves do not replace the
hardware frame; boot prose requires writable-register/order/alias/default review.
ENTRY-01 execution remains gated on operator, safe result area, correction rules
and role protocol. No runtime code, generated artifact or consumer pin changed.
Validation for this receipt: JSON structure/profile-selection assertions, local
Markdown links and diff whitespace. Existing 17-test emitter result is unchanged;
no CPU/firmware execution or new measurements claimed.

## Research receipt

Primary archive URL:
https://atarimuseum.ctrl-alt-rees.com/ahs_archives/archives/pdf/videogames/5200/pam_package.pdf
25 scanned pages. Read prose pages 2–8 and 17–25; low-resolution layout index
only for 9–16, whose examples/flowchart were not read/transcribed as implementation.
Selected October 30 1981 partial description, January 18 1982 VBI revision and
March 18 1982 final memo support documentary rows; exact source provenance and
limitations are docs/sources.md. No source-listing references were followed.

Facts: cartridge communication BFE8–BFFF, entry pointer BFFE–BFFF; final
zero-page reservation 0000–0018; stack page 0100–01FF and documentary vector
reservation 0200–021F. January drops I-bit participation in the VBI critical
check. No numeric vector-symbol/shadow offsets, cartridge flag/metadata encoding,
initial A/X/Y/P/SP or exact boot register values established. Do not guess.
These facts are documentary and retail-unmeasured; no firmware equivalence claim.

## Resume

Continue RUNTIME-002: obtain screened primary software-interface declarations
for exact per-symbol vector/shadow addresses and metadata encoding, and define
cold/warm/key reset separately. Reconcile VBI revision applicability with further
primary/approved observational evidence before selecting a final/retail policy;
Mars has accepted the dated facts only, not a complete implementation scope.
ENTRY-01 needs lawful operator/access and reviewed
cart-owned result area, instrumentation semantics, and observer/implementer
handoff. No hardware/oracle is established; do not manufacture expected results.

Temporary renderer pypdfium2/Pillow was installed in /tmp/retro-pdf-tools only for
scanned-source screening, not as a project dependency or configure fetch. Source
PDF and render outputs were temporary research material, not repo artifacts.
The build remains offline Python/CMake with no compiler/emulator/firmware needed.
RUNTIME-001 tool fixture still has zero capabilities, 10 written/2038 unused bytes;
no real service/font fit, provider target or boot implemented. Mars integration
remains req_6f74; report only reviewed facts, no private source transfer.
