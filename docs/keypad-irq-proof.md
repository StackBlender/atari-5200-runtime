# Keypad IRQ latch foundation: authored candidate

RUNTIME-004,2026-11-06. Original bounded subset of the reviewed
[keypad/fire proposal2](keypad-fire-brief.md), Mars9654ecb/msg_0c5f.
**No automatic port rotation, contact events or fire acquisition is implemented
in this candidate.** It establishes executable IRQ capture/ownership plumbing
for those next services. Tools/tests do not execute a CPU or establish keypad
acquisition, native replay, cartridge compatibility or actual performance.

## New explicit profile and RAM

runtime_abi=sb52-dev-input-v2;
profile=ntsc-four-port-cooperating-input-development. The exact machine-readable
contract is [keypad-irq-profile.json](keypad-irq-profile.json). Only original
cooperating Linear32K diagnostics with explicit declaration
sb52-dev-input-v2-ram600-61f-v1 and application/data/heap/stack ownership excluding
0600..061F may be selected. Application RAM minimum0620 is a new linker contract;
old cc65 starts021C and is INCOMPATIBLE. Size alone is insufficient. Mars converter/
loader must reject missing/wrong declarations and old profile tuples BEFORE power
or RAM mutation. No current accepted converter can silently adopt this identity.
No native field/schema change is proposed; state binds complete profile/source/
image/map and cart contract, including these ordinary RAM bytes and chip state.

| Address | Field | Cold | Ownership |
| --- | --- | --- | --- |
|0600|enabled|0|cart may set exactly1 only after valid initialization|
|0601|irq_busy|0|runtime IRQ transaction; custom NMI must inspect, never modify|
|0602|selected_port|0|cart window controller0..3, matches CONSOL selector|
|0603|phase|0|0 inactive,1 settling,2 collecting; cart window controller|
|0604|captured_contact|0|runtime writes normalized1..15 on fresh accepted IRQ|
|0605|capture_valid|0|runtime publishes1 AFTER code; cart clears only while disarmed|
|0606..061F|reserved|0|untouched after cold; no hidden cart or runtime scratch|

Cold zeros all32 bytes once before selecting continuousSKCTL06 and the explicit
CONSOL04/POTGO04 prime. This changes the old slow03 analog policy only in this
new source/profile. Both03/06 already clock shared polynomials/prescaler;06
changes debounce/fast pot stepping. Fast pots, startup chip/audio interactions,
Trak-Ball cache and actual rendering need new independent execution acceptance.

The original diagnostic cart controls windows until automatic VBI service exists:
configure selector under keyboard-mask-off/ack; retain analog power; allow a full
settle interval; clear valid; set active+collecting then coherently enable40 in
POKMSK and IRQEN. A custom VBI MUST defer all selector/phase/window/mask work while
irq_busy!=0, without spinning. At close inspect pending40 BEFORE ack: pending
without published sample invalidates/defer, never release. A valid empty window
is not inferred from stale KBCODE/down flags. Missing clocks, masked/incomplete
windows, CRITIC and disable/reset must not fabricate releases. Mask/ack40 BEFORE
invalidating/clearing a window. Exact no-op/capture boundaries need native tests.
The current default VBI does not rotate/select/ack or call input callbacks, so it
does not itself close windows or alter the protected mask transaction.

## Authored IRQ behavior

Default0200 points to system_input_irqFC89. Existing wrap-safe classifierFD00
removes its temporary A/X before the new entry saves exactly AXY once. Busy is
set before reading IRQST/POKMSK, held through source/phase/capture and ALL timer
IRQEN writes, cleared after final coherent publication/mask and before callbacks.
No chaining into the parent's saved-frame prologue.

Effective pending=(~IRQST)&POKMSK. Any unsupported enabledB8 faults FC83 BEFORE
ack; supported47 is keyboard40 plus timer1/2/4 bits07. Keyboard is first priority,
then timer1/2/4. A canceled/spurious entry with no current effective source clears
busy and restores the saved frame through FCB0, rather than inheriting the old
variant's spurious fault. Fault paths deliberately retain busy while halted.

Keyboard pending while active==1 and phase==2 and valid==0 verifies port<4,
reads KBCODE, projects bits1..4 via AND1E/LSR and refuses contact0 before ack.
It stores contact0604 THEN publishes valid0605=1. This is the first accepted
handler's register READ, not necessarily the first chip capture: KBCODE continues
updating even masked. Already valid/inactive/noncollecting entries do not
publish. Every keyboard handled/canceled path clears POKMSK40 and writes that
coherent mask to IRQEN, leaving other enabled timers intact. Then busy0 and RTI
via saved-AXY exit. No user callback or stale-code polling, no host input shortcut.
A second accepted capture in the same valid window cannot overwrite the latch.

Timer acknowledgment has the parent's selected-disable/full-mask writes with
busy held throughout. Only AFTER both writes does it clear busy and JMP the
corresponding0216/18/1A callback. One saved frame, scratch AXY/flags, finish by
JMP FCB0, notRTI/RTS. Other disabled latch sources may clear; pending/races,
coalescing, source reassertion and priority starvation limits remain. In an active
window keyboard takes precedence over a simultaneous timer; after40 is disabled,
the enabled timer remains pending for a later IRQ. No fairness/FIFO claim.

## Exact image, allocation and static limits

Image2048 SHA256
2fa0cbdbace0d70bab06953fef5bf08e065c6c6247a8a67692718307e75d6ef8.
Written1613; unwritten435 includes250 RESERVED margin, leaving185 ordinary bytes.
Net109 more written than timer parent1504;266 cumulative extra ceiling therefore
leaves157 before that ceiling, not a complete input-service fit guarantee.
Font, hardware vectors, conio/padding and all old emitters remain untouched.

|Region|Used/allowance|
|---|---|
|startup|120/128|
|interrupts|90/192|
|input|159/176|
|clocks|76/96|
|display|63/96|
|shared|75/80|
|font|1024/1024|
|CPU vectors|6/6|
|reserved margin|0/250|

New prologueFC89..FC95, source/latch/bridgesFD75..FDDE, timer transactions
FE00..FE3B; unchanged old timer bytesFE3C..FE4F become FF allowance. Metadata
helperFEDC six vector stores now sets0200/01=89/FC. Startup RAM loopFC57,
handoffFC75,32 extra direct RAM stores:108 cold direct stores total plus four
real JSR stack writes. Metadata JSR nowFC6A, pushesFC6C/resumesFC6D; service
helper JSRFC50 pushesFC52/resumesFC53. Final AXY0/SPFF/flags match parent policy.
Zero32 loop adds323 nominal cycles/98 instructions: static startup1471 normal,
1478 worst metadata path. This is not stall-inclusive CPU measurement.

Non-nested IRQ has3 hardware+3 savedAXY=6 stack bytes. Classifier's2 temporary
saves are already removed. One NMI over IRQ default system VBI can require12
including both hardware+AXY frames; classifier temporary placements must be
checked at all SP positions too. Future input JSR/bridge adds2 each; proposal2
requires14 before helper/callback extras. No recursive NMI or callback CLI/
reentrant mask mutation. Do not promote static stack math to safe-frontier proof.

## Export and offline validation

Unexported: python3 tools/keypad_irq_image.py --output-dir build/keypad-irq.
Committed export: python3 tools/export_keypad_irq_candidate.py --source-revision
<FULL40PIN> --output-dir build/keypad-irq-candidate. Parent CMake includes
cmake/keypad-irq-candidate.cmake after adding the baseline module, uses target
sb5200-keypad-irq-image and SB5200_KEYPAD_IRQ_SOURCE_REVISION. Four properties
remain absolute image/map/manifest plus full source revision. New profile JSON is
pinned alongside emitter/exporter/CMake and all unchanged baseline inputs.
False execution/provider/retail/full-cycle flags and empty capabilities remain;
authored_capabilities adds only keypad-irq-latch-v1. No release/default change.

Nine new independent methods bring121 total: exact startup/source/normalization/
ack/timer/branch/frame bytes, operand/global-table isolation, declared32-byte
RAM/new identity/false labels, real prior full-pin refusal before output, each
pinned input mismatch, fresh-process generation and only allowed image changes.
No CPU emulator or foreign implementation/test used. Existing build/CTest and
real pinned CLI/temporary CMake consumer must pass before final handoff.

## Integration execution request and next slice

Use ongoing req_6f74, NOT full-request ACK. Require actual original cooperative
cart/CPU: all15keys/fourports/all64phases, stale code, first accepted read versus
overwrite, inactive/settling/duplicate/canceled IRQ, reserved0 and invalid-port
fault before ack, simultaneous07/40/unsupportedB8 and precise mask bus whitelist.
One NMI over IRQ at every source/capture/valid/ack/busy frontier; original custom
window close observes busy and pending-before-ack. Verify one saved frame/AXY/
status/BRK+2/all256SP and timer callbacks. Actual startup/fastanalog/source counts
and safe-frontier same/repeated/fresh-process state replay, strict new cart/profile
refusal and all seven prior variants/R65/lifetime/defaultOFF/firmware hygiene.
No top/bottom fire service or conditional150ms automatic event latency is yet
implemented or qualified. Next cumulative window/rotation/key callbacks and both
fires must fit with this kernel, then full runtime/reset/compatibility/product.


## Committed export validation receipt

Sourceb2e2b40d8c11326f1684635e35832fcc50f9f2d6:121 offline methods and existing
build/CTest1/1 pass. Real strict CLI and temporary CMake parent validate four
properties, absolute outputs, dependency ordering and identical image/map/manifest
bytes. All seven older pinned exports reproduce their recorded image hashes.
Temporary source/build removed. Artifacts remain ignored build/keypad-irq-candidate.
No CPU, converter/cart preflight acceptance, native safe-state or product claim.
