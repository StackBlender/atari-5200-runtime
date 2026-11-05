<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Display-shadow candidate: static proof and integration packet

Original implementation of docs/display-shadow-brief.md revision1. Scope review
and independent execution remain pending. This is not a release or game result.

## Emitted image

2048 bytes, SHA256
1992e64b05d096e479c9532b14a77839bad182428b459a3ca8862ede51acb364.
1307 written,741 unwritten. Display uses63/96 bytes at FE50..FE8E;
input176 and reserved margin250 remain entirely FF. Startup114, interrupt40,
clock16, shared44, font1024 and CPU vectors6 unchanged in size.

Only image byte differences from the ba90c85 VBI candidate are the3-byte clock
routing at FDFA..FDFC and the new63-byte display body. All prior labels, startup,
faults, font, metadata helper and CPU vectors are identical. Final handoff FC6F.
Clock routes CRITIC-zero via JMP FE50, while nonzero still JMP FCB0. Twelve
unrolled LDA zp/STA abs pairs implement the brief's exact pointer/colors/DMA order;
last instruction JMP (0204). No JSR or persistent write outside existing clock,
real stack and the named hardware registers. Register-save/restore ABI unchanged.
No new instruction encodings or global opcode table mutation.

## Static timing and stack

Twelve load/store pairs cost12*(3+4)=84 base cycles/24 instructions. The new
absolute routing JMP costs3 cycles, followed by the existing indirect JMP5 at
body exit. Compared with the former immediate indirect JMP5, the delta is87
cycles/25 instructions. Eligible default VBI therefore168..173 cycles/50..51
instructions, including RTI but excluding hardware entry and refresh/RDY.
CRITIC-nonzero path unchanged. All branches remain within a page; no new indexed
load/page-crossing cost. Existing startup1108/1115 base cycles and411/414
instructions unchanged. Maximum default stack depth6 including hardware frame;
seven stack writes including the temporary classifier push. No extra RAM.

Full default512-cycle target and active DMA/render behavior require actual Mars
execution. Indefinitely held RDY, arbitrary callbacks and nested interrupts are
not bounded. Cold shadows zero can disable/clear display on the first eligible
VBI; initialize safe shadows before enabling NMI. Transfer order is original
policy, not an atomic active-display transaction or measured retail behavior.

## Export interface

After committing generation inputs, choose the full source revision explicitly:

```sh
python3 tools/export_display_candidate.py --source-revision <full-commit> --output-dir build/display-candidate
```

Parent integration adds this repository as before, sets
SB5200_DISPLAY_SOURCE_REVISION to that full lowercase commit, then includes
cmake/display-shadow-candidate.cmake. Depend on sb5200-display-shadow-image before
conversion. Same four target properties: absolute SB5200_IMAGE_FILE,
SB5200_MANIFEST_FILE, SB5200_MAP_FILE and full SB5200_SOURCE_REVISION.
Separate display-candidate output directory prevents old-target collisions.

Every baseline input plus tools/display_shadow_image.py,
tools/export_display_candidate.py and cmake/display-shadow-candidate.cmake must
match the pinned commit byte for byte before outputs are created. No dirty mode.
Manifest version cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.candidate1;
schema1/ABI1/profile/reset/mapper/startup-interrupt observer requirements remain.
Source/image/map/provenance hashes and display_transfer symbol are exported.
All accepted-capability lists remain empty, approval/execution/retail/full-cycle
flags false. Independent receipts belong in prose; do not silently change the
converter's candidate-label contract. Strict identity and R65 state-version work
must be coordinated by Mars; no legacy state migration promised.

## Local verification

Seven new test methods bring the suite to73: independent exact display bytes,
clock routing/only-intended differences and both prior image hashes; all region
budgets/reserves; manifest identity/false flags/timing/revision rejection;
every generation-input mismatch; fresh-process reproducibility; actual old-pin
CLI rejection before output. Direct unittest plus existing CMake/CTest pass.
These checks do not execute a CPU or implement a second emulator. Independent
Mars fixtures are specified in the brief and must verify actual bus order,
CRITIC/immediate/deferred semantics, real DMA/render, save/process replay,
converter negatives, lifecycle, sanitizers and both earlier provider regressions.
