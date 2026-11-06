# Both-fire service: concrete allocation review proposal1

RUNTIME-004,2026-11-06. **STOP before cumulative emission.** Current approved
allocation/ceiling cannot contain the both-fire extension. The existing public
allocation-plan.json, all9 candidate inputs/provider images and250-byte margin
are unchanged. This packet requests a separately identified bounded allocation
revision; it does not authorize an image, converter, release or game claim.

## Concrete code and proposed placement

Original tools/fire_service_fragment.py emits ONLY a153-byte NONRUNNABLE fragment
and JSON at syntheticF800 for size/fixup/encoding tests. This is not a BIOS, cart,
complete2KiB image or provider. No font bytes are replaced. Generic vector roots
required internally by the shared emitter are discarded, never exported. Only
fragment code is returned. No default build/provider target selects it.
SHA2569ea001fd9af9eb2d95f19cd9f219760b6d4deb270bb30eb1ae480453c44d5cb1.
It imports our existing original assembler/code, not any foreign implementation.

Cumulative projection atop windowsfce294b7448a7c5a1a35e6c5e5ed5611ee36473f:

|Item|Bytes|
|---|---:|
|Existing written|1746|
|Both-fire routines and callback bridge|153|
|New near top-entry routing bridge|3|
|Projected total written|1902/2048|
|Current extra over timer1504|398 (old ceiling266 exceeded)|
|Current ordinary free|52 (156 additional cannot fit)|
|Proposed remaining reserved|90|
|Projected ordinary free after revised allocation|56|

Propose fire codeFF00..FF9F (160 allowance) and retain marginFFA0..FFF9 (90).
Original font1024, hardware vectors6, all existing startup/timer/input ranges and
32-byte RAM reservation remain unchanged. Exact standalone allocation proposal
is fire-allocation-proposal.json; it is not read by any runtime emitter/exporter.
Projected both-fire bottomFF00..FF50, topFF51..FF95, callback bridgeFF96..FF98;
7unused in the new160-byte block. New top-entry JMP bridgeFC96..FC98 uses3 existing
free bytes. Route analog_exit JMP to bottomFF00, which continueswindow_entryFD1A.
Equal-key branch uses nearbyFC96 thenFF51; changed-key callback's tail JMPsFF51.
Top concludeswindow_rotateFD59. Existing instruction lengths do not grow at those
hooks; actual relocated full image and branch/map/budget proof must follow review.

Request replace the old266extra ceiling only for this explicit extension with
bounded400extra (398projected,2headroom), retaining90reserved. This is NOT a
complete reset/runtime fit promise or license to spend the remaining ordinary
bytes. If cumulative emission exceeds400extra,160new code or any region, stop
for further review rather than truncate, steal font/RAM or invent banking.
Final remaining-service code will need its own measured fit/refactoring review.

## Original service behavior

The bottom routine runs after eligible analog handling and BEFORE key window
work. enabled!=1 skips it. For eachport0..3 read C010+port, invert active-low bit0,
merge with its retained top bit1, update committed bitmap BEFORE any callback.
Separate bottom_ready initially0 suppresses ALL first-pass events; set1 only after
all4baselines. Changed subsequent values call0208 with Aport/Xold/Ynew. Reload
loop port from private RAM after arbitrary scratchAXY/flags callback; loop bound4.
No stale X/index leakage after a callback and no keyboard IRQ source is used.

The selected top routine runs AFTER successful key close/optional key callback
and BEFORE rotation, never on a busy/invalid/settling window. Read SKSTAT E80F,
invert selected KR2/shift bit3, shift into bitmapbit1, merge retained bottom bit0.
Update committed bitmap first. Each port has its OWN top_ready byte; first sample
sets baseline silently even if bottom was already initialized. Later change
calls0208 with the same old/new bitmap ABI. Reload selectedport after callback,
set only that port's ready and continue normal rotation. No KBCODE modifier used.

Thus up to4bottom events precede key transition, followed by at most1selected
top event per eligible VBI. Fire callbacks are RTS via a JSR/indirect bridge,
AXY/flags scratch, same no-CLI/no input/mask/NMI-writer/no unbounded callback
conditions as key callback. First-source baselines suppress fabricated activation
edges. A bitmap's uninitialized source bit is not evidence of a physical release;
consumers consult its ready flag. Re-enable explicitly clears both sets of ready
flags and starts a new baseline, without fabricated disable-release callbacks.

A busy IRQ need not block bottom sampling: it touches only GTIA/cache/fire/VBI
scratch and calls an input-state-read-only bounded user callback. Protected
selector/window/mask/key publication still skips while busy. Top work occurs only
when window is valid and busyclear. Neither routine resets scanning, powers down
analog, touches audio registers, reads write-only registers or acks keyboard IRQ.
Nested VBI over IRQ still needs hardware+savedAXY12 plus this bridge2=14 before
callback depth, with no extra helper JSR. Recursive NMI/callback CLI unsupported.

## RAM and explicit new profile proposal

Keep existing0600..060A fields. Allocate from already reserved32-byte block:

|Range|New use|
|---|---|
|0610..0613|four committed fire bitmaps, bit0bottom/bit1top|
|0614|all-bottom first-pass-ready0/1|
|0615..0618|four independent top-ready0/1 flags|
|0619|VBI bottom loop port, reload after callback|
|061A|VBI old fire bitmap scratch|
|061B|VBI new fire bitmap scratch|
|060B..060F,061C..061F|remain reserved|

Cold32-byte zero loop already covers new fields. Cooperative activation resets
these to0, initializes key fields/callbacks/settledselector as before and enables
LAST in quiescent SEI/NMI-off context. No IRQ use of the new fire/VBI scratch.
Disable masks/acks before invalidating and emits no source releases. CRITIC skips
all eligible work and preserves old input; busy may defer top/key but not bottoms.
No hidden host storage/new native payload field is proposed.

Propose runtime ABI sb52-dev-input-fire-v3, profile
ntsc-four-port-cooperating-input-fire-development, required frozen before-connect
cart declaration sb52-dev-input-fire-v3-ram600-61f-unlatched-v1. Same32-byte
reservation/app>=0620 plus explicit GTIA latch ownership justify distinct contract.
Old/new variants/declarations/states must mutually refuse beforepower/import.
Declaration asserts cooperation, not inspection that an unknown game obeys it.

## Hardware limits and native acceptance

GTIA bottom reads are post-run cached; GRACTL bit2 MUST be0 during acquisition.
It is write-only, so the cooperating cart explicitly programs/owns unlatched mode;
no silent graphics clear/readback test. Latchedlow can conceal release indefinitely:
reject unsupported latch configuration through explicit contract/fixture limits,
not a fake physical release event. Selected KR2 updates independently once per64
ticks in current Mars, up to7296cycles+read after stable input. Continuous06 and
full selected settle interval remain required; late changes can be stale. No
KBCODE-derived top state or physical-board timing/feel/battery claim.

Keep callback<=128nominalcycles each; worstcase up to6callbacks (4bottom+key+top)
needs measured VBI/refresh cost. Proposed diagnostic DMA-off/ordinary-refresh
full VBI target4096 replaces2048 only after actual measurement; arbitrary display
waits/DMA-heldRDY/longcallbacks not covered. No lossless subwindow taps or keypad
chords; selected top follows the existing rotating-window latency and deferrals.

After allocation/profile review, author separate cumulative image/export/manifest
and prove all ranges/bridges/hooks/cold fields/false labels before actual CPU.
Owner independently executes both logical fire channels across all4ports and any exposed physical aliases, holds/releases/repress,
bottom/top simultaneous independent of keypad, separate baseline/re-enable,
GTIA latch limitation, post-run cache, selected KR2 timing/alias phases, callback
AXY/flags/clobber/RTS/all256SP/nestedNMI and pending-invalid/busy/CRITIC windows,
concurrent timers/analog/TrakBall, bus/register whitelist, measured worstcase
callbacks+VBI/event latency and safe-frontier/process state replay. Require full
new/old tuple/cart-declaration/converter refusal and prior9variants/R65/lifetime/
defaultOFF/firmware hygiene. No fullR62 ACK or app pin/release/default change.

## Current offline checks

Six new methods bring136 total. Independent expected bytes/branch destinations
cover all153fragment bytes, stores-before-callback, distinct baselines/index
reload, false nonrunnable labels/explicit budget failure, local opcodes/strict
bounds and global/parent preservation, fresh-process reproducibility. No CPU or
chip simulator was added; no runtime/game/fire execution is claimed. Use existing
unittest/CTest. Tool CLI: python3 tools/fire_service_fragment.py --output-dir
build/fire-fragment. Outputs stay ignored; no module/provider target exists.


Validation:136offline methods/existingbuild/CTest1/1 PASS. Revalidated explicit
window-source-pinned CLI/CMake and all8older pinned exports:9unchanged images.
Temporary parent removed; only ignored fragment outputs in existing build root.
Diff check clean. No cumulative allocation/provider/emulator change or CPU run.
