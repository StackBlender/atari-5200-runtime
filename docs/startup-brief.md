<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Bounded development startup brief

RUNTIME-004, proposal 1, 2026-11-05. Requested scope review on Mars req_6f74.
**Proposed original policy; not implementation approval or measured Atari behavior.**
Targets the accepted `sb52-dev-cc65-v1` consumer-interface layout, NTSC four-port
emulation and an explicitly selected original provider. Original/reference role
separation is not established; this proposal makes no measured-reconstruction or
retail-compatibility claim. Final/retail VBI policy remains unknown and unselected.

## First implementation scope and evidence

Name the bounded capability `cold-start-digits-v1`: execute CPU reset, initialize
only declared runtime-owned locations, validate digit metadata and hand off to an
original diagnostic through a CPU indirect jump. Also provide independently
authored digit assets for later explicit cart-controlled display. No title splash,
VBI/DLI/IRQ service, scanning, timers or shadow propagation is claimed. A startup
milestone is part of the full runtime plan, not completion of the BIOS replacement.

Sources: PAM-01/03 for mapped communication area and reservations; CONSUMER-01
for the accepted development slots/digit convention; CONSUMER-02 below for chip
register declarations. All numeric defaults, order, failure loops, register/SP
choices and asset pixels below are **our original policy**, not inferred retail
facts. Mars must review chip effects/reset/routing and this limited service scope
before runtime code or execution. No host shadow updates, HLE or direct-PC handoff.

## Cartridge contract

For this first diagnostic, request the owner's existing unbanked 32 KiB mapping:
physical offsets 0000–7FFF map to CPU 4000–BFFF. Mars must explicitly confirm
that mapper selection; no size-only generic mapper detector is added here.
The runtime reads metadata on the emulated bus, not physical file-tail shortcuts:

| CPU addresses | Length | Required bytes |
| --- | ---: | --- |
| BFE8–BFFB | 20 | Exactly twenty authored decimal title digits, each encoded 50–59 |
| BFFC–BFFD | 2 | Exactly two authored year digits, each encoded 50–59 |
| BFFE–BFFF | 2 | Entry address, low byte then high byte |

Entry must be 4000–BFE7 inclusive and lie in this cart's mapped executable data;
our diagnostic further constrains the whole 26-byte fragment to end by BFE7.
Runtime range checking cannot certify arbitrary cart machine code. No optional
init routine, alphabetic title encoding, FF bypass, bank switching or other cart
format is supported by this first scope. All 22 digit bytes are validated before
entry; the two pointer bytes are read/checked as an immutable cart value. Invalid
metadata or entry reaches the exported `startup_fault` loop; no successful handoff.
Absent/unsupported cart/profile/provider must be rejected by Mars before mutation.

## Cold start: exact proposed order

Only full cold power is supported. Mars resets its normal CPU/chips/mapper first;
this program begins at reset vector FC00. Nothing assumes a chip's retained MMIO
value or undocumented reset byte. Before its first controlled TXS, a pending NMI
may use the CPU's incoming stack; that exceptional path is unsupported/fail-stop.
Normal execution starts with SEI, CLD and SP=FF via X/TXS. No waiting for frames,
input, host time or title delay. Perform these writes in order, each once:

| Order | Write address/name | Value | Intended hardware effect, subject to Mars review |
| --- | --- | --- | --- |
| 1 | D40E NMIEN | 00 | Disable ANTIC interrupt enables |
| 2 | D400 DMACTL | 00 | Disable display/PM DMA fetches |
| 3 | E80E IRQEN | 00 | Disable POKEY IRQ enables |
| 4 | E80F SKCTL | 00 | Hold serial/key scanning reset; no input service |
| 5–8 | E801/E803/E805/E807 AUDC1/2/3/4 | 00 each | Silence four audio channels |
| 9 | C01D GRACTL | 00 | Disable player/missile output and trigger latch |
| 10 | C01B PRIOR | 00 | Select ordinary GTIA rendering policy |
| 11 | C01A COLBK | 00 | Black background |
| 12 | D401 CHACTL | 02 | Normal character orientation, inverse present |
| 13 | D409 CHBASE | F8 | Point at original F800 font bank |
| 14 | D40F NMIRES (write alias) | 00 | Clear latched ANTIC NMI causes |

No reads are used to infer prior write-register values. No numeric MMIO sweep;
never touch WSYNC, POTGO, STIMER, SKREST, SEROUT, CONSOL, unused registers or
read-only aliases during startup. AUDF/AUDCTL, display-list pointers, PMBASE,
scroll, other color registers and collision state receive no writes and no
postcondition. Disabled DMA/sprites and silent AUDC make those unspecified fields
irrelevant to the first blank-screen diagnostic. This is a required review
argument, not a chip-execution result. POKEY RNG/timers/serial behavior is unclaimed.

Next write exactly 0000–0018 to zero (25 bytes). Thus pokmsk, rtclok, critic,
atract, sdlst, sdmctl, pcolr, color and paddl start at zero; paddl zero means
unscanned, not physical center. rtclok is proposed little endian but does not
advance without later VBI service. Shadows are initialization values only, with
no ongoing hardware propagation. Write each of the fourteen little-endian vector
slots 0200–021B to FC86 (`startup_fault`). Preserve 021C–021F; reservation does
not authorize clearing padding. No program writes 0019–00FF, 0220–3FFF or page
0100–01FF except actual CPU stack operations. These are program-write boundaries,
not promises that Mars cold power preserves preexisting RAM.

Validate the cart through a helper in the shared allowance. On success set
A=X=Y=00; N=0,V=0,D=0,I=1,Z=1,C=0; SP=FF. Ignore pushed B/expansion bits. A
balanced helper call is allowed; set final flags explicitly after helper return.
Execute JMP indirect through BFFE, which does not cross a 6502 page boundary.
No synthetic return address remains. RTS from cart entry is unsupported. Metadata
is not copied to RAM, and no hidden mailbox/persistent work area is allocated.

## Interrupts, resets and failures

Proposed immutable CPU vectors: NMI=FC80, reset=FC00, IRQ/BRK=FC83. FC80 and FC83
are distinct self-jump failure loops; FC86 is the metadata/default-vector failure
loop. Each is three bytes in the interrupt allocation. They do not silently RTI
or acknowledge successful service. A hardware interrupt still pushes its real
three-byte CPU frame. There is no software dispatch, handler call, input-key Reset
or supported cart enabling NMI/IRQ yet. Cart-controlled direct MMIO after handoff
is outside this startup guarantee; all later services need their own reviewed ABI.

Mars should reject warm/CPU-only/controller-key Reset requests before mutation
for this capability; it must not silently label cold power a warm reset. Repeated
full cold power is allowed and repeats initialization; failure to expose that
reset distinction is an integration blocker. An interrupt during startup/capture
fails or makes the diagnostic inconclusive, never proves entry postconditions.

Proposed first ordinary-path deadline: handoff within 4096 emulated CPU cycles
from the first runtime opcode, excluding the owner's preceding chip-reset work.
Prove an exact cycle upper bound after emission, including branch/page cases and
any chip stalls; revise for review if the bound cannot be met. Export fault-loop
addresses in the map so Mars can report unsupported interrupt/invalid metadata
from PC observation; do not implement instruction traps or host-side services.
Missing handoff without an identified fault is startup timeout, not success.

## Original asset ABI

Reserve F800–FBFF, 128 glyphs of eight row bytes, bit7 leftmost. Glyph index c
begins at F800+8*c. Independently author ten seven-segment-style digit patterns at
indices 50–59 (FA80–FACF); every other
glyph is blank in this first subset. There are no historic alphabet, logo or
font-address assumptions. Define segment pixels on an 8x8 grid: top=(x2..5,y0),
middle=(x2..5,y3), bottom=(x2..5,y6), upper-left=(x1,y1..2),
upper-right=(x6,y1..2), lower-left=(x1,y4..5), lower-right=(x6,y4..5).
Row7 is blank. Digits use conventional segment selections, independently authored
from these coordinates. No font file or bitmap reference is consulted.

Consumer display contract is ANTIC mode 2, CHBASE F8, CHACTL02, PRIOR00,
COLPF1=0E/COLPF2=00/COLBK=00, DMACTL22 once a cart supplies its own safe display
list/screen memory. High-bit inverse and other modes are not claimed/tested yet.
Startup itself keeps DMA off and does not render the title. Mars must review mode,
font routing and colors before this display contract is exercised; no video
capture or glyph appearance is accepted from tool-only tests.

## Allocation, stack and independent diagnostic acceptance

Keep all planning ranges unchanged: startup FC00–FC7F (128), interrupts
FC80–FD3F (192), shared FEB0–FEFF (80); font1024, total code768, margin250,
vectors6. Unimplemented service allowances remain unwritten. First emission
reports actual per-region usage and leaves margin untouched. Stop for review on
overflow; do not hide extra code in font, margin, cartridge or RAM.

Bound first startup helper depth to one JSR (two bytes), no software pushes.
A single exceptional interrupt can add three: proposed maximum five stack bytes
after SP initialization, provided Mars stops at the first failure loop. Repeated
external NMI edges can push further frames even there; no stack bound is promised
for repeated interrupts or continued execution after the first failure. ENTRY-01 adds one balanced PHP
byte after handoff (SP=FF). These must be checked against actual control flow;
future interrupt nesting/service stack32 remains unproved and unapproved.

The original diagnostic candidate is a zero-filled 32 KiB unbanked layout, fixed
20-digit title 01234567890123456789, year26, entry8000, capture results3000–3005.
The 26-byte capture fragment records only A/X/Y/pushedP/SP/completion. Its six-byte
result area is our cart-owned choice with DMA off, not approved for original
hardware/oracle use. Tool generation is allowed; no runtime or execution approval
follows. Expected normal results: A=X=Y=00, (P & CF)=06, SP=FF, fresh complete=A5.
Require observation of a fresh A5 write after reset, not a stale RAM marker. No
reference firmware, screen artwork or whole RAM/stack readout.

Mars-owned execution acceptance must independently verify bus metadata reads,
reset-vector fetch/normal opcode execution, entry register/flag/SP scalars, exact
runtime write whitelist/order, caller-RAM sentinels, CPU read/peek/ANTIC asset
agreement and distinct fault/timeouts. Repeat cold power and fresh-instance runs.
Negative cases: each digit invalid at first/middle/last position, FF year, entry
below4000/in metadata/aboveBFFF, missing cart, unsupported mapper/provider/reset,
pending/early interrupt and malformed image. No service or game compatibility
claim until its own independent fixtures pass. Keep future strict image/profile/
version-bound state and raw-state rejection integration requirements unchanged.

## Review requested

Approve or correct this bounded scope, mapper/reset operation, MMIO semantics and
order, final CPU/RAM policy, failure reporting, asset ABI, deadline and diagnostic
result ownership. Review this prose without reading GPL implementation if Mars'
source boundary requires it. After scope approval, implement the first bounded
image, prove actual fit/cycles/stack, then request Mars diagnostic execution and
provider integration under their own review gates.
