<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Analog shadow static proof and export

Independent bounded analog execution now accepted by Mars msg_1cd6 /33967abf;
see independent-execution.md. Pending-execution wording below is historical.
Keypad delivery under03 remains a separate debt; flags/pins stay unchanged.

Bounded authoring approved Mars msg_092a/83a8a400 with qualifications in
[analog-shadow-brief.md](analog-shadow-brief.md) revision2. Independent CPU/
conversion/state/provider acceptance pending; not a retail or game claim.

Image2048 SHA256
32343a567399b3b4f9c142bde446fe89397267267d51a89393553fdab9471290.
1384 written/664 free. Startup127/128, interrupts51, input53/176, clocks16,
display63, shared44, font1024, vectors6; margin250 untouched. Any further
startup growth requires scope/allocation/refactoring review; only1 byte remains.
No extra persistent RAM/stack, no emulator or host-computed analog service.

## Exact changes and static control flow

Startup prefix through FC63 unchanged from DLI258bc0c. At FC64 add13 bytes:
LDA03/STA E80F, LDA04/STA C01F/STA E80B. Then old metadata/finalization tail.
Metadata JSR now FC71 pushes returnFC73 and resumesFC74. Final JMP(BFFE) FC7C;
endsFC7E, FC7F remainsFF. Final A/X/Y0, SPFF, P&CF06 and normal digit/entry
validation remain required by independent execution. Cold stores now74 plus
2 helper stack writes (previous71 plus3 additional MMIO writes). Earlier
SKCTL00 reset and IRQEN00/NMIEN00 writes still precede the new explicit prime.

Input analog_transfer FD40: LDA E808, BNE analog_exit FD72 (operand2D),
eight LDA abs/STA zp ascending register E800..07 to0011..18, LDA00/STA E80B,
analog_exit JMP display_transfer FE50. Any pending ALLPOT bit bypasses all eight
copies AND POTGO; only display/deferred proceed. Clock's FDFA JMP now FD40;
CRITIC nonzero still jumps vbi_exit, so analog is also skipped. Default DLI path
unchanged. Exclusive acquisition ensures no reset/external POTGO during copying;
no atomicity or sample validity is invented outside that supported contract.

Only changed byte ranges from prior candidate: FC64..FC7E startup tail,
FD40..FD74 input body, FDFA..FDFC clock route. Other bytes and labels unchanged
except cart_handoff. New analog_transfer/analog_exit symbols identify body/exit.

Extra startup16 nominal cycles/5 instructions: new1124/1131 base cycles,
416/419 instructions. New complete input body71 nominal cycles/21 instructions;
pending body10/3. Eligible complete default VBI240..245 base cycles/71..72
instructions; pending179..184/53..54. CRITIC-nonzero VBI unchanged. Hardware
entry7, refresh/RDY, callbacks and device execution stalls remain separate.
Full startup4096/defaultVBI512 and DLI dispatch128 targets remain unmeasured
for this exact tuple. No spin or busy-wait; one ALLPOT read even if completion
occurs immediately afterward. Existing saved-register stack maximum6 including
hardware entry unchanged; DLI temporary maximum4. No extra JSR.

SKCTL03 starts keyboard/prescaler/polynomial activity: audio/RANDOM/keyboard
phase differs from prior candidates even with IRQEN00. Do not require byte-equal
old/new chip state or imply first-sample validity from Ready/shadow0. Initial
host vector before POTGO and R65 host-vector-before-import are required. Cold
Trak-Ball cached velocity0 may center first acquisition until post-run polling.

## Export

```sh
python3 tools/export_analog_candidate.py --source-revision <full-commit> --output-dir build/analog-candidate
```

Parent adds baseline module, sets SB5200_ANALOG_SOURCE_REVISION to full committed
pin, includes cmake/analog-shadow-candidate.cmake and depends on
sb5200-analog-shadow-image. Same4 target properties: absolute SB5200_IMAGE_FILE,
SB5200_MANIFEST_FILE, SB5200_MAP_FILE and full SB5200_SOURCE_REVISION. Separate
analog-candidate output. Baseline inputs plus tools/analog_shadow_image.py,
tools/export_analog_candidate.py and cmake/analog-shadow-candidate.cmake must
match named commit byte-for-byte before output, no dirty bypass. Earlier four
pinned exports remain unchanged; no mutable prior service emitter dependency.

Manifest version
cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.dli-dispatch-v1.analog-shadow-v1.candidate1.
Schema1/ABI1/reset/mapper/profile/Starting interrupt observer unchanged. All
accepted capabilities/execution/provider/retail/full-cycle flags remain false.
Analog pending/complete nominal timings are static fields only; no acceptance
flag promotion. Explicit new image/manifest/map/pin/profile tuple review required
in Mars. Existing strict sb52rt-dev2 must reject cross-image imports before
mutation. Actual safe-point, pending conversion and mid-copy process replay
must be qualified independently; don't invent arbitrary instruction captures.

## Offline coverage and independent gate

Seven new methods bring total87: exact prime/startup tail/handoff, exact complete/
pending input bytes and CRITIC route, only intended diffs and all allocations,
manifest identity/false flags/static timing, every input mismatch, fresh-process
reproducibility and real prior-pin CLI refusal before output. Direct unittest
and existing build/CTest pass. No CPU or hardware service execution here.
Independent owner must execute approved brief's early-VBI/late-completion/long
CRITIC/power/conversion/axis isolation/register/MMIO/display/DLI/callback/state/
process/lifecycle/Release-ASan and old-provider/defaultOFF regressions.

## Committed analog export receipt

Source/exporta6c406e4cee090b8044eea3b9b6c7a5b6391b3ab is pushed. Real CLI
and temporary parent CMake consumer pass four properties/absolute artifacts/
dependency ordering/full source/image/map identities/false flags and exact CLI
byte equality. All four earlier pinned exports reproduce unchanged image hashes.
Temporary parent source/build removed; ignored artifacts in build/analog-candidate.
Exact artifact/fit/shifted handoff/priming packet sent Mars req_6f74. Independent
execution still pending; do not ack fullR62 or claim acquired first sample from
Ready. Consumer pins/defaults/buildgates/exportflags unchanged. Next independent
POKEY/8axis/pending/midcopy/CRITIC/state-process/lifecycle acceptance, then
specify keypad/fire/IRQ/timers/reset services. Lease released after push.
