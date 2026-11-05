<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Eight-axis analog shadow service proposal

RUNTIME-004 next service, original proposal1. Not implemented or approved.
Display/DLI bounded independent execution accepted per msg_8f2c; their pins
and false export labels stay unchanged. This analog policy still needs review.
Target all eight standard-controller axes across four ports under the existing
NTSC development profile. No keypad/fire scan, reset-key handling or retail claim.

## Integration facts and source boundary

Mars msg_2864 answers the original hardware-interface question in prose. Only
that interface contract was read, not chip implementation/tests or Atari firmware.
This is emulator integration evidence, not measured hardware/BIOS behavior.
Existing CONSUMER-01/02 declarations supply shadow/register address candidates.

Read POT0..7 at E800..E807, ALLPOT at E808. Write POTGO at E80B (data ignored),
SKCTL at E80F; writes at E800..E807 are audio and E808 is AUDCTL, so read/write
aliases must stay explicit. A pending ALLPOT bit is1; pending POT reads are running
counts, not completed values. POTGO samples eight axes/power and restarts all
conversions, clearing counts and setting ALLPOT FF. Do not restart until consuming
the completed result. Cold ALLPOT00/POTsFF does NOT establish a completed sample:
explicit priming is required before any completion-based service.

SKCTL00 cannot advance slow conversion;03 supports slow conversion and debounced
keyboard scan. CONSOL C01F bit2 controls analog power globally; bits0..1 select
keypad/top fire. POTGO samples all four ports independently of that selector,
and later power/select changes do not rewrite already sampled conversion targets.
Real hardware timing/equivalence and keypad semantics remain separately unproved.

## Proposed original policy for review

After existing cold shadow/vector initialization, before metadata validation:
write SKCTL03, CONSOL04, then POTGO04 (ignored data). This primes a real conversion
once, without extra persistent RAM. Preserve IRQEN00/NMIEN00 and actual CPU/chip
execution; no host-computed POT bytes. Startup's earlier SKCTL00 reset remains.
New cold writes deliberately enable conversion/analog power; keyboard scanning
can run with IRQEN disabled but no keypad/fire service is claimed.

On eligible VBI after clock/CRITIC check and BEFORE display transfer:

1. CRITIC nonzero skips analog copy/restart as well as display/deferred callback.
2. Read ALLPOT once. Any pending bit skips BOTH copy and restart, retaining the
   previous eight shadow bytes. Continue existing display/deferred work.
3. If ALLPOT zero, read POT0..7 ascending and write PADDL shadows0011..0018 in
   the same order, preserving each raw unsigned byte. No clamping or conversion
   to normalized host axes. Write POTGO00 once AFTER all eight reads/stores.
4. Continue display then deferred callback. Restart samples the next conversion;
   no spin, waiting loop, extra IRQ, hidden first-sample flag or scratch RAM.

Before the first completed conversion, cold shadows remain zero (existing ABI
initialization), explicitly unavailable startup samples, not centered readings.
If the first VBI arrives before conversion completes, leave shadows zero and
allow the already primed conversion to continue. CRITIC may postpone consumption
for multiple frames; resume copies the completed old sample then starts a fresh
one. This latency is explicit; no fresh-every-video-frame guarantee. Disconnected
channels retain actual completed timeout bytes. Mars clarification specifies
unpowered standard/disconnected target228; unpowered approximate Trak-Ball
axis0 targets114, independently of keypad port selection. Standard or Trak-Ball acquisition
still follows real POTGO/core post-run input cadence, not direct host shadow writes.

Cart must preserve priming lifecycle: external POTGO/SKCTL/power manipulation or
host/hotplug topology changes require a separately synchronized restart contract.
No assumption that ALLPOT00 establishes validity after arbitrary reset/config
changes. No warm reset, partial-channel restart or runtime-selected fast mode.
DLI callback must not change acquisition controls in the supported fixture.

## Estimated fit and fixtures

Potential startup sequence13 bytes (LDA03/STA E80F, LDA04/STA C01F/STA E80B)
fits remaining14 startup bytes: startup127/128, handoff movesFC7C. This is near
capacity; any further startup growth needs explicit allocation/refactoring review.
Proposed input body FD40: LDA E808/BNE local exit, eight unrolled LDA abs/STA zp,
LDA00/STA E80B, local exit JMP display_transfer.53/176 input bytes. Clock replaces
its absolute display JMP with input JMP (same size). Estimated cumulative1384
written/664 free incl250 untouched margin; zero extra RAM/stack. These are
estimates, not emitted allocation or approval. Existing exports stay reproducible.

Independent original fixture must verify cold prime ordering, first early-VBI
pending case/no restart, all eight axes/port isolation, endpoints/center/timeout,
changing sample latched at POTGO, mid-conversion pending, zero/FF CRITIC and long
skips/resume, exact RAM/MMIO write order, no audio-register writes, register/stack/
clock/display/DLI coexistence and safe-point/same/fresh/process replay including
pending conversions. Strict new image/config identity and R65 host-vector-before-
import order apply. Release/sanitizer/default-OFF/old-provider checks remain.
No CPU loop or firmware input service is implemented by this proposal. Obtain
integration review before authoring or claiming the chosen startup/cadence policy.
