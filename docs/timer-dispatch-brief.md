<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Bounded POKEY timer IRQ dispatch

Independent bounded execution accepted Mars msg_30c1/f32595cb; see
independent-execution.md. Earlier execution-pending text below is historical.
Export pins/false flags/defaults stay unchanged; pooled release still pending.

RUNTIME-004 original revision2, separate candidate atop IRQ42762a7. Bounded
authoring accepted with qualifications Mars msg_3385/d7be9b4; artifact/execution
acceptance pending. Keypad evidence req_72f0 completed without chip changes.
No timer-rate initialization, software countdown timers or historical ABI claim.

## Contract and source ownership

Cold vinter0200 defaults to system_timer FE00. Existing generic IRQ classifier
FD00 dispatches through it after preserving/restoring A/X and leaving only the
hardware frame; BRK020E unchanged. system_timer saves A/X/Y exactly as system_vbi
(PHA/TXA/PHA/TYA/PHA). It reads IRQST E80E once, EOR FF, AND software POKMSK00,
then copies that pending snapshot into X. Bits01/02/04 mean Timer1/2/4. Any
pending enabled bitsF8, or no recognized pending timer, faults via irq_faultFC83
before device acknowledgment. A is scratch; saved hardware P/PC are untouched.

Priority is Timer1 then2 then4; service exactly one captured source per entry.
For selected source write IRQEN E80E with POKMSK & ~source, then write full
POKMSK back, then JMP through0216/0218/021A. Other ENABLED pending source bits remain
pending. Both writes also acknowledge OTHER DISABLED latch sources; serial
bit3 has distinct nonlatching status semantics. RTI may re-enter for enabled
sources, but not necessarily immediately: enable qualification and disabled-tail
clock timing and events between read/ack/re-enable must be measured. Coalesced source bits are not a
lossless event counter. A new selected expiration during service can reassert, coalesce or race with
acknowledgment; no no-loss or immediately-quiet guarantee. Continuous Timer1
can starve Timer2/4; no fairness or lower-priority latency bound.
Do not synthesize time, alter chip counters, STIMER or audio registers.

Cartridge must configure timer rate/clock/STIMER, install a valid timer callback,
set POKMSK and actual IRQEN consistently, and CLI explicitly. Runtime never
automatically enables a timer IRQ. Mask/vector updates require sources disabled
and no overlapping callback/NMI. POKMSK must remain unchanged through service;
otherwise restoring the mask cannot have a well-defined transaction. Unsupported
serial/keyboard/Break sources are not silently consumed even if a timer is also
pending. Other enabled-but-not-pending bits alone do not fault. External/mismatched
mask sources yielding no recognized snapshot fault rather than reporting success.

Timer callback sees hardware frame plus saved A/X/Y (same6-byte total depth as
VBI), A/X/Y/live flags scratch, I remains set and D is retained. It balances its own saves and finishes JMP
vbi_exit FCB0, NOT RTI or RTS. This restores original registers and hardware P/PC.
No additional JSR or persistent RAM. Cold timer vectors still FC86 until installed;
selected-source acknowledgment precedes callback dispatch, including an uninstalled
callback fault. CRITIC does not suppress IRQ timer delivery. DLI/IRQ/VBI nesting,
arbitrary held source/callback deadline and torn vectors unsupported. Hardware
IRQ with I set remains pending normally; no hidden host polling or PC replacement.

## Startup refactor and allocation

Move the old four VBI default-vector stores from FC50 to initialize_services
FEDC. Add two stores0200=00/0201=FE and RTS. Helper31 fits36 free shared bytes;
replace20 startup bytes by JSR FEDC3. Startup110/128 now has18 bytes free,
metadata JSR FC60 pushesFC62 and resumesFC63, final handoffFC6B. No previous
cold field changes except0200 FE00. Six override stores in order:0202=A0,0203=FC,0204=B0,0205=FC,0200=00,0201=FE.
Only0200 final value differs from previous cold vectors. Additional helper call balanced; peak ordinary
startup stack still2, four total stack writes across the two nonnested JSRs.
New direct cold stores76 plus4 stack writes. Prime order/final AXY/P/SP unchanged.

system_timer77 plus local3-byte fault trampoline FE4D..FE4F fills remaining80
clock bytes FE00..FE4F. Clock region96/96; shared75/80, interrupts77, startup110,
input53/display63/font1024/vectors6. Estimated1504/2048 written,544 free incl250
untouched margin; no extra RAM. Any further clock/shared overflow needs review.
No prior generation inputs changed. Exact new image/map/pin/profile required.

Nominal startup1148/1155 cycles,422/425 instructions (+24/+6). Timer body through
indirect vector56 cycles Timer1,62 Timer2,67 Timer4. Generic IRQ39 is separate;
no-op callback JMPexit3+exit22 yields complete120/126/131 cycles excluding7-cycle
hardware entry and refresh/RDY. Proposed complete default timer target256 incl
normal refresh, no custom callback/held RDY. Existing VBI/DLI nominal unchanged.
These are estimates until exact encoding and independent execution acceptance.

## Independent acceptance

Real original CPU timer fixtures must use real rates/STIMER/masks, all seven
nonempty pending combinations, isolated01/02/04, simultaneous order and remainder
retrigger and priority starvation, masked/unmasked/I cases and documented bit coalescing. Observe single
IRQST read, exact two IRQEN writes/masks before selected callback; no timer/audio
counter writes or POKMSK mutation. Unsupported/spurious must fault before ack.
Default vectors fault, balanced custom callbacks restore AXY/P/SP/PC, CRITIC
independent; test generic BRK and all256 stack positions independently, including saved-frame wrap and source
arrivals between status read, mask-off, mask-on and callback/RTI. Startup
must verify both helper return pairs/write/RAM/final state/new handoff/metadata/
early-pending observer. Capture pending/source acknowledgment/restore/callback/
RTI at actual safe points; same/fresh/process replay and strict mutual candidate
refusal before mutation. Include R65 host-input-before-import, old providers,
VBI/display/DLI/analog/reset/lifetime/defaultOFF/Release/nonunity ASan/firmware.

CONSUMER-01 supplies shadow/vector slots; pinned CONSUMER-02 POKEY declaration
hash reverified for timer bits01/02/04. CPU-02 factual EOR immediate49/2cycles and
AND zp25/3cycles reviewed in appendixB. Original source priority/ack/callback ABI
awaits integration review, not primary hardware timing or manufacturer code.
