<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Bounded POKEY timer IRQ dispatch

RUNTIME-004 original proposal1, separate candidate atop IRQ42762a7. Scope and
independent execution review pending. Keypad evidence req_72f0 remains separate.
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
POKMSK back, then JMP through0216/0218/021A. Other pending source bits remain
pending; RTI may immediately re-enter for them. Coalesced source bits are not a
lossless event counter. A new selected expiration during service can reassert.
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
VBI), A/X/Y/live flags scratch. It balances its own saves and finishes JMP
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
cold field changes except0200 FE00. Additional helper call balanced; peak ordinary
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
retrigger, masked/unmasked/I cases and documented bit coalescing. Observe single
IRQST read, exact two IRQEN writes/masks before selected callback; no timer/audio
counter writes or POKMSK mutation. Unsupported/spurious must fault before ack.
Default vectors fault, balanced custom callbacks restore AXY/P/SP/PC, CRITIC
independent; test generic BRK and all256 stack positions independently. Startup
must verify both helper return pairs/write/RAM/final state/new handoff/metadata/
early-pending observer. Capture pending/source acknowledgment/restore/callback/
RTI at actual safe points; same/fresh/process replay and strict mutual candidate
refusal before mutation. Include R65 host-input-before-import, old providers,
VBI/display/DLI/analog/reset/lifetime/defaultOFF/Release/nonunity ASan/firmware.

CONSUMER-01 supplies shadow/vector slots; pinned CONSUMER-02 POKEY declaration
hash reverified for timer bits01/02/04. CPU-02 factual EOR immediate49/2cycles and
AND zp25/3cycles reviewed in appendixB. Original source priority/ack/callback ABI
awaits integration review, not primary hardware timing or manufacturer code.
