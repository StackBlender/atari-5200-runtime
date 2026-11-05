<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Bounded DLI dispatch development service

Independent bounded execution now accepted by Mars msg_8f2c /4daa27f; see
[independent receipt](independent-execution.md). Pending-execution wording below
is historical; source exports/false flags remain unchanged, no product release.

RUNTIME-004 original proposal1,2026-11-05. Separate candidate extends startup,
VBI-clock and display-shadow-v1 with dli-dispatch-v1. Scope and actual execution
review pending, not a retail firmware claim. Existing three export source inputs
remain unchanged; pending display execution is not assumed accepted.

## Original contract

CPU NMI classifier at FCC0 temporarily PHA; read NMIST D40F once; AND E0.
Exactly40 accepts VBI: STA NMIRES D40F, PLA, JMP (0202), as before. Exactly80
accepts DLI: STA NMIRES, PLA, JMP (0206). Each accepted path acknowledges once
with its masked source value. Lower five bits ignored; unsupported spurious,
Reset20 or mixed60/A0/C0/E0 goes to nmi_fault FC80 without acknowledgment,
clock, display or callbacks. NMIST is the current latch, not immutable event
provenance; normal ANTIC cycle/status/CPU-pending behavior remains. No host PC
substitution, pending-NMI clearing or chip scheduling modifications.

DLI vector0206 remains startup_fault FC86 on cold start. Cartridge installs a
valid little-endian callback before enabling DLI (NMIEN80 orC0 with VBI). A
DLI with untouched vector must visibly fault, never silently claim service.
Update vectors with NMI disabled AND a quiescent CPU-pending interrupt state
established by the fixture; disabling NMI alone does not drain CPU pending.

Callback receives original A/X/Y, original hardware interrupt frame and SP three
bytes below interrupted SP; classifier temporary A already popped. Live flags
are scratch, D remains as interrupted and I is hardware-set. Callback preserves
any A/X/Y it changes, balances its own stack and finishes RTI. No RTS, no hidden
JSR frame, no VBI saved-register frame, no JMP vbi_exit. Default runtime touches
neither X nor Y on DLI and restores A before dispatch. Callback is responsible
for the final A/X/Y values; RTI restores hardware P/PC. No extra runtime DLI
exit thunk or automatic register prologue. Arbitrary/torn/recursive targets,
stack overflow, nested/overlapping NMIs and invalid display lists unsupported.

DLI does not change clock, CRITIC, shadows, input, IRQ mask or user RAM. CRITIC
has no effect on DLI dispatch; it only controls VBI display/deferred as already
specified. Ordinary NMIEN C0 allows nonoverlapping real DLI and VBI events, with
original chip timings and pipeline delays. Callback may write selected display
registers to implement a bounded raster fixture, through real CPU instructions.
VBI's next eligible shadow transfer can overwrite those registers. Current-latch
classification cannot prove original source if a later event replaces NMIST
before it is read; acknowledge this limit, do not invent immutable provenance.

## Allocation, static timing and compatibility

Classifier28 bytes at FCC0..FCDB replaces17 bytes at FC89..FC99; old range now
FF. NMI hardware vector changes from FC89 to FCC0. All other labels/startup/
font/helper/clock/display bytes remain identical to display source9d7071f.
Interrupt region51 bytes; total1318/2048 written,730 unwritten including250
untouched margin. No new RAM or stack allocation; dispatch maximum4 bytes below
interrupted SP including hardware frame and temporary A, callback entry3.

Accepted VBI takes BEQ rather than BNE, adding one base cycle and no instruction:
default eligible VBI169..174 cycles/50..51 instructions including RTI, excluding
hardware entry/stalls/callbacks. CRITIC-nonzero VBI also adds one base cycle.
DLI dispatch30 base cycles/10 instructions, first PHA through indirect JMP,
excluding7-cycle hardware entry and callback/RTI. All classifier branches stay
within page FC; full DLI dispatch target128 cycles under DMA-off ordinary refresh
without held RDY. Active-list/WSYNC callback time must be independently measured.
Startup base1108/1115 cycles and411/414 instructions unchanged. Targets not
measurements. Maximum stack/latch behavior at nested events is not bounded.

Separate target/export, schema1/ABI1, new image/map/pin/version identity; all
capabilities[] and approval/execution/full-cycle flags remain false. Explicit
converter allowlist review required. Strict synchronized sb52rt-dev2 identity
must reject different candidate states before mutation; no legacy dev1 import.
Nothing selects this candidate by default or authorizes a release/app enablement.

## Independent Mars acceptance

Author fixtures/expectations independently from this contract, not our GPL source
or test files. No manufacturer program/firmware, reference trace or extracted art.

1. Repeat startup/VBI/display coverage, source masks, callback stacks, clock wrap,
   CRITIC, register/P/SP/PC restoration and exact MMIO/RAM write boundaries.
2. Build an original safe mode2 display list using existing authored digits and
   enable actual DLI on an explicit line. Verify real CPU NMI acknowledgment and
   callback at selected raster line, no VBI/clock/shadow activity for DLI. Default
   uninstalled0206 visibly faults; installed balanced callback preserves registers
   and RTIs to interrupted CPU instruction stream. No host callback substitution.
3. Exercise all four I/D combinations, SP80/FF, A/X/Y00/55/AA/FF and CRITIC00/01/
   80/FF. DLI callback receives original A/X/Y+hardware frame; temporary push is
   balanced. Callback save/clobber/restore and visible palette marker use only
   cart-owned scratch and explicit hardware writes. RTI meaningful P bits/PC hold.
4. Actual separate DLI and VBI with NMIENC0: each DLI callback once per marked
   line, each VBI clock once, shadow order/deferred after CRITIC unchanged. Test
   DLI-only80 and VBI-only40 enables separately; current-latch source semantics
   remain, do not call synthetic forced mixed status a natural event sequence.
5. Real DLI before/while startup plus near-handoff pending interrupt must not
   report Ready. Unsupported Reset/mixed/spurious synthetic cases fail before
   acknowledgment/callback. Deliberate nesting is outside supported contract;
   report observed status without claiming detection/safety not implemented.
6. Actual synchronized captures around classification/ack/dispatch, in callback
   and after RTI: same/fresh/separate-process byte replay. Vary topology/caches
   under R65; wrong image/state/version refuses before mutation. No arbitrary
   instruction-boundary capture assumption; test actual safe points.
7. Default-OFF/missing-BIOS/unavailable-provider/reset/unload/reload/live-exit,
   strict converter negatives, Release/nonunity sanitizer and earlier providers/
   a26 regressions. No device/full-game/retail compatibility claim.

## Sources

Existing CONSUMER-01 vector0206 and CONSUMER-02 masks/aliases are reused. CPU-02
PHA/PLA/LDA/AND/CMP/BEQ/BNE/JMP/RTI facts already recorded. Dispatch/callback/
unsupported policy and numeric bounds are original. No new source exposure.
