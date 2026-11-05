<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Timer dispatch static proof and separate export

Original pending-scope/execution candidate; [timer-dispatch-brief.md](timer-dispatch-brief.md)
owns callback/source policy. No keypad mode switch, device HLE or timer-rate defaults.
Image2048 SHA256
eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550.
1504 written/544 free incl250 untouched margin. Startup110/128 (18 free),
interrupt77, input53, clock96/96, display63, shared75/80, font1024, vectors6.
Further clock/shared growth requires allocation review; no extra persistent RAM.

## Exact static layout

system_timer FE00 starts saved-register prologue then single LDA IRQST/EOR FF/
AND zp00/TAX. Unsupported-enabled pending bitsF8 branch local timer_faultFE4D.
Priority tests01/02/04 route timer1 FE3E, timer2 FE2F, timer4 FE20. Displacements
3C/28/14/2D independently checked. Three15-byte paths load POKMSK, clear chosen
bit FE/FD/FB, STA IRQEN, reload POKMSK/STA IRQEN, JMP timer vector0216/18/1A.
Body77 bytes plus3-byte JMP irq_faultFC83 exactly fills FE00..FE4F. No reads of
POKEY write-only aliases, no POKMSK writes, no audio/timer rate/counter writes.
Unsupported/spurious fault precedes any IRQEN acknowledgment.

Cold helper initialize_services FEDC..FEFA31 bytes stores old VBI defaults0202/
0204 plus new vinter0200=FE00, then RTS. Startup replaces20 old override bytes
with3-byte JSR FEDC atFC50 (returnFC52/resumeFC53). Prime movesFC53 unchanged
in order/values; metadata JSRFC60 returnsFC62/resumesFC63; final handoffFC6B.
Old helper metadataFEB0..FEDB stays unchanged. New body uses31 of36 shared
free bytes. Cold stores76 plus4 writes from the two sequential nonnested JSRs;
ordinary max startup depth2. Original final AXY0/P&CF06/SPFF/metadata rules stay.

Changed ranges only startupFC50..FC7E, timerFE00..FE4F, helperFEDC..FEFA. Prior
labels unchanged except cart_handoff. IRQ classifierFD00/BRK hardware route,
NMI/VBI/DLI, analog body and display transfers are byte-identical to IRQ42762a7.
No automatic IRQEN enable; default timer vectors remainFC86 until installed.

## Nominal bounds and callback stack

Startup old+24 cycles/+6 instructions yields1148/1155 cycles422/425 instructions.
Timer body56/62/67 cycles (Timer1/2/4) ends at indirect callback JMP. Generic IRQ
classifier39 separately. Diagnostic no-op callback JMPexit3+exit22 gives complete
120/126/131 nominal cycles excluding hardware entry7/refresh/RDY. Full default
timer target256 requires independent execution with suitable source rates; no
arbitrary high-rate/held source/custom callback/nested interrupt deadline claim.

system_timer saves A/X/Y as VBI and callback must JMP vbi_exit; total stack6
including hardware frame, scratch live flags. Generic classifier's two temporary
saves are already popped, so its maximum5 does not add to6. Callback extra depth
separate. Original hardware P/PC remain; CRITIC has no effect on timer IRQ.
Source bits coalesce, not an event counter; multiple pending sources re-enter
normally after RTI. Keep software/hardware mask coherent and stable in service.

## Exact pinned export

```sh
python3 tools/export_timer_candidate.py --source-revision <full-commit> --output-dir build/timer-candidate
```

Parent adds baseline module, sets SB5200_TIMER_SOURCE_REVISION to full lowercase
commit, includes cmake/timer-dispatch-candidate.cmake and depends on
sb5200-timer-dispatch-image before conversion. Same4 target properties absolute
SB5200_IMAGE_FILE/MANIFEST_FILE/MAP_FILE and full SB5200_SOURCE_REVISION. All
baseline inputs plus tools/timer_dispatch_image.py, tools/export_timer_candidate.py
and cmake/timer-dispatch-candidate.cmake must byte-match commit before output.
No dirty bypass; previous source exports untouched.

Manifest version
cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.dli-dispatch-v1.analog-shadow-v1.irq-brk-dispatch-v1.timer-dispatch-v1.candidate1.
Schema1/ABI1/reset/mapper/profile and actual Starting interrupt observer contract
unchanged; observer must use generated FC6B handoff. All capability/approval/
execution/retail/full-cycle flags stay false. New timer nominal fields and256
full target are static/pending only. New complete image/map/descriptor/source
profile tuple needs explicit converter review; same strict sb52rt-dev2 may be
sufficient but only owner qualifies field/identity/state semantics. No legacy
state reconstruction or app/provider/release enablement.

## Local and independent checks

Nine new methods bring total104. Exact80 timer bytes/branches/priority/ack paths,
startup helper/returns/handoff, only intended diffs/labels, full allocations,
local EORimm49/ANDzp25 strict operands and no global-table mutation, manifest
hashes/false flags/timings, every pinned-input failure, fresh-process output and
actual previous-pin CLI no-output refusal pass. Direct unittest and existing
build/CTest pass. No CPU or hardware service emulation added.

Mars independently exercises actual timers/IRQ/BRK with all pending combinations,
mask/ack/retrigger/source priority/coalescing, callback stack/RTI, startup helper
and final RAM/state, actual safe points around masks/callbacks, same/fresh/process
replay, mutual state refusal, all previous providers/R65/analog/display/DLI/VBI/
defaultOFF/lifetime/Release/nonunity sanitizer/firmware checks. Hardware source
contracts and timing must be reviewed before acceptance; source-backed bit
numbers do not prove the authored runtime policy executes correctly.

## Committed timer export receipt

Source/exportac9b47e50c213b08022e78bdef64662569cd3d29 pushed; real CLI and
temporary parent CMake consumer pass all4properties/absolute artifacts/dependency
ordering/source-image-map hashes/false flags/exact CLI equality. All six earlier
pinned exports reproduce their unchanged hashes. Temporary source/build removed;
ignored output remains build/timer-candidate. Full contract/tuple/shifted startup
and source handling packet sent Mars req_6f74 for independent scope/execution.
No local CPU run, state-schema/provider acceptance or new flags/default/pin/release
change. Next actual IRQ/timer/ack/retrigger/callback/RTI/process validation, then
remaining keypad/fire/reset/software timers/contracts. Keypad req_72f0 primary
wiring review remains separate. Lease released after push.


## Incorporated authoring review

Marsd7be9b4/msg_3385 accepts bounded authoring with brief revision2
qualifications, not artifact/integration/execution. IRQEN writes also acknowledge
other disabled latch sources, while preserving other enabled pending sources.
Status/ack/re-enable races, timer enable/disabled-tail clocks and coalescing are
not a lossless/immediate-quiet transaction. Priority1 can starve2/4. Test actual
clock/bus behavior and256SP callbacks. Ordered helper stores0202=A0,0203=FC,
0204=B0,0205=FC,0200=00,0201=FE; only0200 final value changes. Uninstalled
other slots hitFC86 Metadata; timer unsupported/spurious trampolineFC83 IRQ.
Artifact sourceac9b47e and all generation inputs/flags remain unchanged.
