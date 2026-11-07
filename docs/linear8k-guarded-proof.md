# Guarded Linear8K development authoring

Technical scope approved Mars9076b17/msg_f869 underreq_6f74. Only owner review
prose docs/a52-linear8k-profile-review.md was read; no native implementation/test/
decoder, private payload, game asset/font/firmware/disassembly or reference trace.
This scope is original profile/tool/diagnostic authoring, NOT native/private-game
admission. All earlier generation inputs and14native semantics remain unchanged.

## Unchanged CPU image, new required native guard

CPU parent e8f296d5a8fa693f13b5dd46259eafcb5567e88f, image SHA256
5936e46d08c7991231a52dfb6c1a404a7a0d1ab505a51b2c5e09a569d7ad20e4.
ALL2048bytes/symbols/allocations/assets/metadata CPU code remain identical,
1556used/492unused/250reserved. No new6502validator/RAM/stack/helper/native payload
field is authored. Original CPU authored capabilities remain EXACTLY the parent's;
a required native eligibility guard is not an emulated CPU capability.

New profile ntsc-four-port-cart-owned-linear8k-guarded-development, explicit
variant linear8k-guarded, own source/version/map/manifest/current contract hash.
Mapper is Linear8K/exact8192. The normative
[contract](linear8k-guarded-profile.json) retains ALL25shadow/14vector individual
cold values/ownership/IRQ semantics and declares linear8k-immutable-entry-guard-v1.
Application0019..FF/021C..3FFF, no0600reservation; public0..18/0200..21B,
shared0100..1FF. No fake cooperating tag or historical8K BIOS/board claim.

The native requirement is NOT implemented by these producer tools:

1. Every cold/system-power/state-import route checks actual immutable loaded
   board and exact8192size, canonical little-endian entry via readonly immutable
   board peeks BEFORE power/randomization/cache/import mutation.
2. Entry must be in [8000,9FE8) or[A000,BFE8), hexadecimal half-open. Exclude
   4000..7FFF open bus and BOTH metadata aliases9FE8..9FFF/BFE8..BFFF. Canonical
   metadata BFE8..BFFF maps payload1FE8..1FFF; entry BFFE/BFFF maps1FFE/1FFF.
3. Before Ready and FIRST application opcode, ACTUAL handoff PC must equal the
   immutable entry AND be in those intervals. Pending-NMI refusal remains.
   Original overlay/cheat-hook/stale-entry probes must challenge equality even
   when the substituted PC is another otherwise allowed address. No PC repair.
4. Publish pre-power-entry refusal distinctly from the parent's CPU metadata fault
   after initialization. The contract's classification is a required observation
   stage, not a newly implemented RuntimeError enum. Native owner must document
   the actual public phase/error representation. Invalid YEAR with otherwise
   eligible immutable entry still executes original full cold then CPU refusal.

The CPU's generic4000..BFE7 validator remains a SUPERSET, not an8K-aware gate.
Valid numeric and secondFF cases retain full cold/4096watchdog; no historical FF
bypass, changed scan policy/font/service/default or metadata overlay is invented.
Byte equality alone cannot authorize8K. Native integration/qualification remains
required before this profile is usable; no app selector currently admits it.

## Complete identity and exports

New files tools/linear8k_guarded_image.py, export_linear8k_guarded_candidate.py and
cmake/linear8k-guarded-candidate.cmake verify frozen combined parent/current
contract and new source inputs. Parent source reuse refuses; every export input
must match its explicit new40hex pin before output. Typed JSON equality refuses
False-for-zero, ownership/reservation/guard/mapper drift. Four standard properties
on sb5200-linear8k-guarded-image, source variable
SB5200_LINEAR8K_GUARDED_SOURCE_REVISION. Output separate linear8k-guarded-candidate
folder; no old catalog/variant/source input is widened.

The manifest/map bind the new mapper and native requirement, ABI/version/profile,
raw contract/source/exporter hashes and exact parent lineage. Accepted capabilities
stay empty; execution/provider/retail/timing labels stay false. Inherited nominal
CPU worksheets are not new native measurements or full-cycle proof. The new
current raw contract differs from parent f287bfc766c3e13973464b2219762cdc2249180ec9c54d5bd5555e1be0be5cb9;
that old hash is parent provenance only. A source or byte-identical image alone
never selects this guarded profile, including cross32K/8K states.

## Original exact-size diagnostic, not an execution oracle

Tools/linear8k_probe.py generates ONLY an ORIGINAL8192-byte cartridge from owned
capture/emitter code, with selectable8000/A000 alias entry and numeric/secondFF
metadata. Captures AXY/P/SP before its own setup; masks IRQ/NMI, reads declared
ROM/alias/open-bus boundary addresses, copies ALL24metadata bytes through BOTH
aliases into declared private result windows, then marks5A and loops. Source
markers are our chosen35/A7/6D at payload0100/1100/1FE7. No private data is used.
Open-bus values are expressly UNKNOWN: native data-bus observation is required,
not an invented FF/zero constant. Declared result windows total69application bytes;
producer tests verify encoding/layout/reproducibility, not actual CPU behavior.
Masking interrupts for this mapping probe does NOT qualify services/input/state.

```sh
python3 tools/linear8k_probe.py --output-dir build/original-linear8k
python3 tools/linear8k_probe.py --entry 0x8000 --second-ff --output-dir build/original-linear8k-ff
```

All generated artifacts stay ignored. Native owner still needs independently
authored exact-size CPU oracles; do not use the producer's own output as an
independent execution proof. No original-system measurements/reference role.

## Remaining independent admission

Dual-native Release/fullASan actual mapping/alias/openbus/metadata/entry-boundary/
first fetch, immutable/pak drift, overlay/cheat actual-handoff and pendingNMI
negatives, fullCold/numeric/FF/RAM/IRQ/input/stack/fault/allSP/ordinary/in-handler/
process/poisoned replays. Wrong board/size/source/state and SAME-IMAGE32K/8K
mutual pre-mutation refusal plus nextTWOframes, inherited/R65/OFF/firmware/
converter/all old14tuples. Equal-length16K wiring cases are UNSUPPORTED negatives,
not selected boards or a private wiring sweep. Return a disproved guard route for
review BEFORE authoring CPU validator changes. No private-input/source-rights/
gameplay/product/reference/source-delivery/release/fullR62 acceptance follows.

## Initial producer validation

Focused8/8 and full227offline tests PASS (8.859s full), existing build PASS,
CTest1/1 PASS10.94s. Original8192fixture CLI also generated in the existing ignored
build root. New current contract raw SHA256
4749f1d32c026abd5c9c2ad769ebc314d2b60af2b3b3c0375a39ca577d45d15e;
version223characters,10CPU authored capabilities unchanged. No native run. A real
committed-source CLI/CMake four-property/order/triple-equality receipt follows
once the NEW source pin exists; synthetic test source IDs are not delivery pins.
