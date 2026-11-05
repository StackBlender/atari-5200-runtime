<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# VBI and clock development service proposal

RUNTIME-004 next service, revision1, 2026-11-05. **Proposal for scope review,
not authoring approval, emitted implementation or measured retail behavior.**
The existing source711a2e986f7906f45aebd310e6330fd7ffc338bf and its exported
candidate labels remain unchanged. This proposal requires a distinct image,
manifest version and explicitly reviewed integration allowlist before execution.

## Supported scope and evidence

Proposed capability `vbi-clock-v1` extends `cold-start-digits-v1` under the same
`sb52-dev-cc65-v1` public field layout, NTSC four-port, Linear32K/cold-only
profile. It supplies actual CPU NMI dispatch, immediate/deferred VBI vector
handoff, a little-endian16-bit modulo frame counter and register-restoring RTI.
No input scan, DLI dispatch, IRQ/BRK service, attract algorithm, countdown timers,
display-shadow transfer, warm reset or broader game support follows.

PAM NMI-01 and the dated January VBI-01 prose motivate the interface and
clock-before-CRITIC order. We deliberately select a new original development
policy with no processor-I-bit exclusion; this does not reconcile October/
January for any retail firmware. CONSUMER-01 supplies addresses only.
CONSUMER-02 supplies ANTIC aliases and mask declarations: D40E NMIEN,
D40F read NMIST/write NMIRES; DLI80, VBI40, Reset20. The pinned public ANTIC
header was reread and its existing SHA verified; no emulator/kernel/test code
was read. All dispatch, stack, acknowledgment, clock endian/wrap, callback and
unsupported-case decisions below are original policy, subject to owner review.

## Entry and acknowledgment

Startup retains DMA/POKEY interrupts/NMI disabled and the existing initial
register/flag/stack and RAM boundaries. The cartridge explicitly writes NMIEN40
only after startup handoff and stable valid callbacks. No automatic NMI enable
or implicit display service. The ordinary hardware VBI source is required;
forcing a host PC or invoking callbacks in C++ is not service execution.

The new CPU NMI vector points to an authored classifier in the interrupt region.
It temporarily saves A (PHA), reads NMIST once, and accepts exactly the supported
source bits: VBI set, DLI/Reset clear. Lower non-source bits are ignored. It writes
NMIRES once to acknowledge the source latch, restores A (PLA), then CPU-indirect
JMPs through vvblki0202. No hardware stack frame is removed by classification.
X/Y are untouched. Live condition flags are unspecified; interrupted P/PC remain
on the real CPU stack. I is set by hardware NMI; D may still be set. No decimal
arithmetic is used by runtime clock work.

DLI-only, Reset-source, simultaneous VBI+DLI/Reset and a spurious NMI without VBI
reach nmi_faultFC80 before clock/callback work. Do not acknowledge an unsupported
source as a serviced VBI. This deliberately refuses mixed-source work rather
than dropping one event while reporting both serviced. DLI enable remains outside
the contract. Repeated/nested NMI during classification or callbacks is unsupported;
no unbounded-stack safety claim. Default handler duration must complete before
another supported VBI edge. Persistent NMIEN0 does not clear a CPU-latched NMI.

## Vectors and callback stacks

| Slot | Cold default | Callback contract |
| --- | --- | --- |
| vvblki0202 | exported system_vbi | Original A/X/Y, hardware frame only; JMP system_vbi to continue, or RTI to replace the entire service. No RTS. |
| vvblkd0204 | exported vbi_exit | A/X/Y/live flags scratch; hardware frame plus three saved registers; finish with JMP vbi_exit. No RTS or direct RTI. |
| Other twelve slots0200/0206..021A | startup_faultFC86 | Still unsupported, not silently successful. |

The immediate callback must preserve A/X/Y itself if it changes them before
chaining; system_vbi preserves the values it receives. It must leave SP and the
hardware frame unchanged when chaining. No hidden JSR return address is supplied.
A standalone immediate RTI intentionally skips clock, CRITIC and deferred work.
Deferred handlers may clobber A/X/Y but must balance their own stack use. Callback
code/targets and vector updates are cartridge-owned; arbitrary, torn, invalid or
recursive vector targets are unsupported. Update only with NMI disabled and a
quiescent CPU-pending interrupt state established by the owner-approved fixture.

system_vbi pushes A, X, Y in that order (transfers through A as needed). It
increments rtclok0001 low byte; on wrap increments0002 high byte. Result is
(old+1) modulo65536, exactly once per invocation, independent of interrupted
I/D flags. Then read CRITIC0003. Nonzero jumps directly to vbi_exit; zero jumps
indirectly through vvblkd0204. Thus CRITIC suppresses only deferred work here;
clock and immediate dispatch already occurred. No input/display side effects
are implied by the term system VBI.

vbi_exit pops Y, X, A in reverse order and executes RTI. Default complete path
restores A/X/Y/SP, hardware-restored P (compare meaningful bits), and PC. It does
not alter CRITIC, vectors, other shadows or the cartridge's pending IRQ cause.
IRQ/BRK CPU vector continues to irq_faultFC83; arbitrary enabled IRQ is outside
this capability. Callback vector symbols and entry/exit contracts must be exported
in the future map, not hardcoded by consumers from this planning document.

## Allocation and measurable bounds

Keep fontF800..FBFF, fault loopsFC80/83/86, shared metadataFEB0..FEFF and250-byte
FF00..FFF9 margin unchanged. Proposed classifier starts atFC89; all classifier,
register prologue/exit and vector routing must fit inside the remaining183 bytes
of FC80..FD3F. Clock/CRITIC body fits its existing96-byte FDF0..FE4F allowance.
No input/display allowance is consumed. These are ceilings, not emitted sizes.

Existing startup94 bytes leave34 within FC00..FC7F. The two default vector
replacements need at most20 proposed bytes with immediate-byte absolute stores;
report exact byte usage and updated startup full-cycle bound after authoring.
Do not assume the current FC5B handoff address or1091-base-cycle total survives.
Hardware vectors and image/manifest/map hashes necessarily change. Overflow
requires allocation/scope review before using margin or other service ranges.

Only persistent writes: clock0001/0002 per service; cold startup may additionally
initialize the same previously declared zero page/vector fields. No extra RAM,
conio0019..001C, padding021C..021F, hidden host state or cartridge scratch.
Classifier has one temporary A byte after the three-byte hardware frame.
It pops that byte before dispatch. system_vbi has three saved register bytes,
so the default maximum is six additional bytes from interrupted SP, with no
JSR. Callback extra depth is separate and must be bounded by each fixture.
The32-byte planning estimate does not prove arbitrary callback/nesting safety.

Proposed normal default-handler target: at most512 full CPU cycles from first
classifier opcode through RTI, including ordinary refresh/RDY steals, excluding
hardware entry latency and caller callbacks. This is a target for owner review,
not a measured bound under indefinitely held RDY. Count entry latency separately;
owner instrumentation must distinguish complete/default versus callback paths.
Startup still targets4096 full cycles but must be independently remeasured.

## Independent acceptance packet

Use independently authored cartridge source and expectations; do not import this
project's implementation/tests or use an emitted self-result as the oracle.
A diagnostic result area is cartridge-owned, separately approved by the owner.
Use scalar results/write observations, never manufacturer code/assets/traces.

1. Repeat all existing startup/metadata/entry/register/RAM/fresh-write/asset tests
   against the new explicitly pinned image; verify defaults for0202/0204 and all
   other vectors, and update the exact ordered startup write whitelist.
2. Generate actual ANTIC VBIs after handoff with NMIEN40. Verify one tick per
   serviced VBI, read-before-NMIRES ordering, no early callback or host service,
   PC after RTI and no endless retrigger. Compare1,2 and120 completed VBIs.
3. Seed clock pairs0000,00FE,00FF,01FF,FFFE,FFFF. Expected next values0001,00FF,
   0100,0200,FFFF,0000. Observe low-byte write every tick and high-byte write only
   on low wrap. Verify default path with all four interrupted I/D combinations.
4. With CRITIC00/01/80/FF, require clock to advance in every case; only00 invokes
   the original deferred marker callback. Immediate marker precedes clock, and
   deferred marker follows it. Use independent markers outside runtime RAM.
5. Immediate custom chaining preserves A/X/Y and hardware frame; standalone RTI
   skips clock/deferred. Deferred custom clobbers A/X/Y then JMPs exported exit;
   default register/flag/SP/PC restoration still holds. Vary SP80/FF and A/X/Y
   00/55/AA/FF; exact stack maximum six for default, callback budget separate.
6. Unsupported DLI/Reset/mixed/spurious sources must fail visibly, without clock
   advance/deferred marker or successful service. Early/startup NMI, pending NMI,
   repeated/nested interrupts need explicit owner failure/status expectations;
   do not promote an interrupted startup to Ready. Never simulate service by
   editing PC or clearing CPU pending state from the host.
7. Sentinels prove no writes outside clock/real stack/approved cart markers after
   entry. Verify no display/input/IRQ/timer writes and no conio/padding changes.
8. Synchronized capture during NMI, before/after clock carry, at each callback
   boundary and after RTI must replay byte-identically in same/fresh instances
   and separate processes. Bind new full image/manifest/pin identity. Old and new
   candidate states reject each other before mutation; raw remains refused.
   Confirm whether the current ready-state serializer already captures all CPU/
   chip/stack fields; avoid a new state version unless the schema actually changes.
9. Repeat cold/reset failures/unload/new-instance/live-exit, default-OFF and
   missing-provider gates, Release and nonunity ASan; run old bounded provider
   and a26 regressions. Keep any existing accepted711a2e9 path reproducible.

## Decisions requested from integration owner

Review the source masks/latch acknowledgment and mixed/spurious failure policy;
startup/pending NMI visibility before Ready without hidden service logic; callback
stack/return and vector-update preconditions; clock/CRITIC ordering;512-cycle target
and independent fixture ownership. Confirm candidate version/allowlist extension
and state rejection strategy for a new module alongside the existing bounded pin.
Approval is needed for this concrete service scope before emitting its image.
No original-system access, retail behavior selection or product enablement is
requested. The full runtime commitment remains unchanged.
