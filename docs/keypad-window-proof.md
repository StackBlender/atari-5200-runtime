# Automatic four-port keypad windows: authored candidate

RUNTIME-004,2026-11-06. Separately versioned cumulative keypad-windows-v1 atop
accepted IRQ foundationb2e2b40d8c11326f1684635e35832fcc50f9f2d6. This implements
original automatic keypad collection, port rotation and contact-change callbacks.
Both FIRE services remain unfinished. Offline emission is not native execution,
measured input latency, game support or complete firmware acceptance. Existing
8 source/export contracts and full250-byte margin are preserved.

## Identity and exact state

Same declared reservation0600..061F, input-v2 cooperating-cart ABI and before-
connect pak runtime-cart-contract=sb52-dev-input-v2-ram600-61f-v1. The new source,
image/map/manifest/profile tuple MUST be separately allowlisted; no old/new state
or descriptor aliasing. No native payload field is added. This cart declaration
asserts RAM cooperation only, not correct initialization or arbitrary game support.
The profile in keypad-window-profile.json adds:

|Range|Purpose|Cold|Activation|
|---|---|---|---|
|0600..0605|enabled,busy,port,phase,code,valid|all0|enabled1 LAST,port0,phase1,valid0|
|0606..0609|four committed contact values|all0|allFF (software no-contact)|
|060A|VBI-only old-key scratch|0|runtime scratch, not IRQ scratch|
|060B..061F|reserved|all0|leave reserved|

IRQ accesses0600..05 only; VBI scratch060A cannot corrupt an interrupted IRQ.
Cold still leaves acquisition disabled and callback020A at FC86 Metadata fault.
An original cooperative cart MUST install a valid RTS callback, initialize four
keysFF, select CONSOL04/port0, retain SKCTL06/analog power, establish a complete
settle interval, set phase1/valid0 and finally enabled1. Do this from quiescent
foreground with CPU I set and NMI disabled, keyboard40 coherently masked/acked;
never activate from a user callback or while an IRQ transaction is suspended.
Do not clear busy as a substitute for quiescence. Application RAM begins>=0620.
Enabling just before VBI without the initial settle requirement is unsupported.

Disable from the same quiescent context: clear40 in POKMSK/IRQEN and acknowledge
BEFORE clearing enabled/phase/valid; retain other enabled timer bits coherently.
Do not fabricate release callbacks. Reenable repeats the complete activation and
baseline initialization. No concurrent foreground/timer/custom-NMI writer of
selector/window/SKCTL/POKMSK/IRQEN/POTGO/held-key/scratch is supported while active.
Rate/timer-mask changes need this exclusive ownership boundary. No callback CLI,
recursive NMI or changing input registers during a protected transaction.

## Eligible VBI behavior

Existing clock increments regardless of CRITIC. CRITIC!=0 skips analog/display/
input and retains old window/sample. On resume it may consume an older acquired
sample; no fresh-input guarantee. Existing completed analog copy/restart runs
before windows, then window_entryFD1A:

1. Busy!=0 defers ALL window/selector/mask/contact callback work without waiting;
   disabled!=1 also skips it. Both continue display/deferred service. Default VBI
   runs with I set, so an IRQ cannot interrupt this single writer.
2. Verify selected port0..3. Phase1 settling branches to fresh arm; phase2 collects;
   another active phase faults FC83 BEFORE input mask changes.
3. At close, published valid permits commit. Otherwise require software mask40
   still enabled AND current IRQST40 deasserted BEFORE ack. Pending-without-valid
   or missing mask makes the window invalid: leave selector/phase/code/mask/held
   state coherent, defer a bounded attempt to next eligible VBI and allow IRQ
   after RTI. Never synthesize release from lost pending evidence.
4. Valid close clears40 coherently in POKMSK/IRQEN. Compare captured_contact to
   this port's committed value. Equal => no callback/repeat. Different => store
   new committed contact, invoke key callback with port and old/new values.
5. Reload port after callback (all AXY/flags scratch), increment modulo4, write
   CONSOL04|port, set phase1, continue display/deferred. No scanner reset/hidden
   host sampling, and power bit2 remains set. The next eligible VBI arms; the
   following closes, yielding one settle+one collect interval per port.

Fresh arm clears valid, sets captured_contactFF (software none), publishes
collecting phase2, writes IRQEN with40 off to acknowledge old pending, then writes
coherent POKMSK/IRQEN with40 on, preserving timer bits. A fresh hardware request
can execute after NMI return. Reuse the accepted first-handler-read IRQ latch;
no raw FF test, down-pulse read or repeated stale code becomes a contact event.
The handler stores1..15 and valid1, masks40 and preserves timers. The armedFF
becomes a release only through the valid-empty close checks above.

A masked/incomplete/stopped-clock/mutated-register window has no finite latency
promise and must not be treated as a successful empty acquisition. Code can
check software mask/pending/busy, not detect every external clock-ownership breach.
The cooperative contract must retain continuous06 and enable CPU IRQs during
collection. A physical change just after an old capture can still approach9
intervals before commit (~150ms at60Hz), plus busy/CRITIC/stalls. Actual full
input-to-callback timing is REQUIRED before product acceptance. Short taps/chords
are not losslessly observed; one keypad contact per port and independent fires
are the selected scope. Both-fire acquisition is not implemented here.

## Key callback and stack

020A callback: A=port0..3, X=old contact1..15 orFF, Y=new contact1..15 orFF.
Committed key RAM already contains new value; selector still names this port.
JSR FCF3 -> indirect bridgeFCAB -> user callback, RTS returnsFCF6 and JMPs rotate.
Callback can clobber AXY/flags; no hardware/input/mask/reserved-state mutation,
no CLI/NMI configuration or yielding arbitrary time. Maximum128 nominal cycles,
including its RTS, is an original bounded diagnostic condition, not an enforced
watchdog or DMA-inclusive guarantee. Callback may save registers on its own stack;
include every such byte in the independent stack proof. Install before enabling.
No callback on a stable hold; a changed contact emits one old->new transition.

Non-nested VBI: hardware3+savedAXY3+JSR return2=8, before callback-owned depth.
One VBI over IRQ:6+6+2=14 before callback depth; classifier transient paths also
need all256SP tests. No extra input helper frame exists. Existing timer callback
uses JMP FCB0 and DLI owns RTI; neither returns RTS to this bridge. All register
and frame/nested safe-state claims require independent actual CPU execution.

## Fit and analog-loop tradeoff

Image2048 SHA256
3c1b419b9af94645ea537126d21e464f90f05013689ef7132656680d62d4207a.
1746written/302free includes all250 reserved; only52 ordinary bytes remain.
Net133 above IRQ foundation,242 above timer parent1504. The266 extra ceiling
leaves24 bytes before review; **this is not a fit claim for future fire/reset**.
Stop for allocation/refactoring review before exceeding it or consuming margin.

|Region|Used/allowance|
|---|---|
|startup|120/128|
|interrupts|164/192|
|input|166/176|
|clocks|96/96|
|display|95/96|
|shared|75/80|
|font|1024/1024|
|vectors|6/6|
|reserved|0/250|

Analog reads/stores remain ascending POT0..7 -> PADDL11..18 and only restart
once all complete. Compact LDX0/LDA-absX/STA-zpX/INX/CPX8/BNE copy saves28 ROM
bytes, trades65 nominal completed-copy cycles: complete analog service136 versus
old71; pending path still10 before jumping to new window service. This is a
software byte/cycle estimate, not audio/analog snapshot or hardware timing proof.
No hardware alias/mode/prime/sample-validity claim changed. Independent hardware
bus order/RMW/refresh/native safe-frontier requalification is required.

Cold startup/font/helpers/IRQ/timer bytes and declared stores/handoff remain
byte-identical to foundation: FC75 handoff and32 RAM zeros;1471/1478 static cold
estimates, not measured whole-cycle timing. New actual input-enabled VBI cost is
unknown. Request2048-cycle default diagnostic VBI target including callback<=128
and ordinary refresh/DMA-off; old512 claim does not automatically cover windows.
Owner must measure per-path/actual callbacks/DMA/list/scan-settle behavior and
verify selected->arm interval covers required7296+read for later Top Fire.
Unbounded waits/callbacks/heldRDY remain outside the target.

Placement: entryFD1A..FD3D, close-checkFE3C..FE4F, mask-closeFDDF..FDEA,
commitFCDC..FCF8/arm bridgeFCF9..FCFB, fresh armFE8F..FEAE,
rotateFD59..FD6F, exitFCA8..FCAA/key bridgeFCAB..FCAD. Compact analogFD40..FD58.
All remaining IRQ/NMI/timer/reset/font/vector code unchanged. No RAM code/banking.

## Export, independent checks and next delivery

Unexported: tools/keypad_window_image.py --output-dir build/keypad-window.
Committed pinned export: tools/export_keypad_window_candidate.py --source-revision
<FULL40PIN> --output-dir build/keypad-window-candidate. Parent includes
cmake/keypad-window-candidate.cmake, target sb5200-keypad-window-image,
SB5200_KEYPAD_WINDOW_SOURCE_REVISION; four usual absolute-artifact/source props.
New profile JSON plus source/exporter/CMake and unchanged baseline inputs are
verified byte-exact against that pin BEFORE output. All approval/full-cycle labels
false, capabilities empty; authored list adds keypad-windows-v1 only.

Nine independently expected exact-byte/layout/branch/order/profile/provenance/
strict-operand/fresh-process/old-source-refusal methods bring130 offline tests.
No Python CPU/chip engine or foreign implementation/tests. The planning reducer
is a synthetic event policy, not the execution oracle for these instructions.
Run existing CMake/CTest, real committed CLI and ephemeral CMake parent, and all8
older source-pinned exports before handoff.

Ongoingreq_6f74 must independently execute exact tuple and original cartridges:
15keys x4ports x64phases, all window entry/capture/pending/valid/busy/ack/rotate
NMI frontiers and simultaneous timers, held/release/repress/change/empty/stale,
missingmask/maskedIRQ/pending-invalid deferrals, CRITIC/resume, activation/disable/
re-enable and invalid port/phase faults, key callbacksAXY/flags/RTS/all256SP and
one NMI-over-IRQ, maximum callback budget. Actual scan/host-to-event latency,
analog ascending complete/pending/boundaries/TrakBall/controller cache, clocks/
audio/register whitelist and VBI costs with/without display waits; native real
safe-frontier repeated/fresh-process replay including callbacks. New/old tuple/
profile refusal, converter negatives, all8 prior/R65/lifetime/defaultOFF/firmware
regressions. No app pin/release/fullR62 ACK or game compatibility follows.


## Committed export receipt

Sourcefce294b7448a7c5a1a35e6c5e5ed5611ee36473f:130 offline methods/build/
CTest1/1 PASS. Real source-pinned CLI and ephemeral parent CMake consumer prove
four absolute artifact/full-source properties, dependency ordering and byte-exact
image/map/manifest equality. All8 prior pins reproduce unchanged image hashes.
Temporary source/build removed; ignored artifacts stay build/keypad-window-candidate.
Native automatic window/callback/analog/state acceptance remains pending.
