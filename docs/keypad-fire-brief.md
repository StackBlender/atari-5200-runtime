# Original keypad/fire policy proposal 2

RUNTIME-004 continuation, 2026-11-06. **Bounded experimental authoring scope accepted with corrections:** Mars
9654ecb239d87abfe3ddf518ab74150c50004b40 /msg_0c5f. No new image,
MMIO implementation, provider or accepted historical ABI. Revision2 incorporates that prose review. Parent is timer source
ac9b47e50c213b08022e78bdef64662569cd3d29. Preserve all seven old exports exactly.
The event model tools/keypad_policy.py consumes acquired observations; it does
not model POKEY or establish that the acquisition proposal below works.

## Selected original direction

Use an explicitly opt-in four-port development profile with SKCTL06 continuous
forced-compare scanning. This is a new policy proposal, not an approved workaround
or a modification of accepted analog03. It changes the POT stepping/debounce and
keyboard/audio interactions; both03/06 already enable the shared prescaler and
polynomial clock, so no new divider/reset is claimed. These effects require independent execution checks.
Never toggle SKCTL00/06 on each port/window: repeated resets could disturb sound
and acquisition. Initialize once, prime POTGO explicitly, and retain power bit2
on every CONSOL selector write. Read all eight completed pots before restarting,
as in the parent. Fast conversion values/timing and audio consequences must be
qualified anew; previous slow analog acceptance does not cover this profile.

Round-robin ports0,1,2,3, one full eligible VBI interval settling and one full
interval collecting per port. At each collecting window's end, consume either
one **code read by the first accepted handler after a fresh request** or no capture. A held key may produce repeated
chip captures but only changes in committed per-port contact emit events.
No autorepeat; one old->new transition represents a changed contact. None after
a whole valid collection window means release, never merely an instantaneous
SKSTAT pulse or unchanged/stale KBCODE. No FF sentinel applied to raw KBCODE.
KBCODE can update even after IRQ40 is disabled, so the latch is not guaranteed
to contain the first chip capture. Normalize contact bits1..4 only after proving capture provenance; do not treat
modifier/alias phase bits as distinct keys. Current Mars interface contact IDs are1 #,2 0,3 *,4 Reset,5 9,6 8,7 7,
8 Pause,9 6,10 5,11 4,12 Start,13 3,14 2,15 1. Contact0 is reserved/refused.
This is an interface mapping, not measured physical legend/retail ABI parity.

This proposal supports one keypad contact per port plus independent fire inputs.
Multiple keypad contacts/chords and sub-window taps are not qualified. All15
physical keys including Start/Pause/Reset must be exercised separately. An
unsupported multiple-contact selection must not be advertised as a chord service.
For first-handler latching, a change just after an old sample in B1..B2 can
miss B2 and wait until B10: the conditional change-to-commit bound approaches
**nine intervals (~150ms at60Hz)**, not eight, even before busy/CRITIC/IRQ
mask deferrals. The reducer's8-boundary scheduling test supplies ready observations
and does not prove acquisition latency. Measure installed host-input to CPU callback
latency, including post-run caches, before accepting casual multiplayer behavior.
Multiple contacts, sub-window changes and invalid/masked windows have no lossless
or finite latency promise. Shorten/restructure acquisition if measurements fail
product needs; do not alter chip semantics to force this policy to pass.

## Proposed acquisition and interrupt ownership

1. Enter a settling interval with keyboard IRQ40 disabled/acknowledged and no
   valid sample. Select CONSOL04|port without resetting the scanner.
2. At the next eligible boundary, discard stale pending/code, clear the capture
   latch, set POKMSK bit40 and write the coherent mask to IRQEN. Collect for the
   following full interval. Other enabled timer sources remain enabled.
3. Extend the new variant's default IRQ dispatcher to recognize keyboard40
   before timers. On its first request, read KBCODE after validating current pending/phase/window, copy it into the
   selected port/window latch, clear POKMSK40 and write IRQEN to stop further
   keyboard IRQ entries for that window. Preserve all other enabled bits and
   existing timer/BRK behavior; disabled latch sources may also be cleared by the
   IRQEN write, as already documented. Break80 remains disabled/unsupported.
4. At the next eligible boundary, close the window with a bounded atomic section:
   inspect pending40 and capture-valid BEFORE ack. Pending without a published
   sample makes this an INVALID window: keep selector/collection coherent, defer
   to a later bounded attempt and allow IRQ after NMI; do not synthesize release
   or spin. For a valid window, mask/ack40, snapshot capture-valid/code, commit key transition, sample selected
   top-fire, then select the next port and start settling. Establish exact ordering
   for a request arriving on the boundary; no event FIFO or lossless pulse claim.

Proposed interlock for review: set a dedicated IRQ-busy byte BEFORE reading
IRQST/KBCODE or selected-window state; clear it only after the final coherent source/mask/publication transaction,
including timer acknowledgment. At VBI entry, busy!=0 defers ALL keyboard/top-fire/selector
window work to the next eligible boundary, while unrelated clock/bottom-fire/
analog/display work may proceed. Never spin in NMI waiting for interrupted IRQ.
A VBI before busy is set can close/ack the old window; the subsequent IRQ may
therefore observe no source. The NEW dispatcher must treat this canceled/spurious
entry as a bounded no-op, not inherit the parent's unconditional spurious fault.
Other unsupported enabled sources must still fault before acknowledgment. If a
window is settling, an obsolete keyboard entry must not publish a key. Keep busy across ALL IRQEN read/modify/write transactions, including timer-only
acknowledgment. In particular old mask41 read -> VBI closes to01 -> resumed timer
write40 would violate settling; the inverse can acknowledge a new window. Clear
busy only AFTER final coherent mask/publication and before USER callbacks.
Refactor timer dispatch into the same single saved-AXY frame; do not chain a
second prologue into the old timer body. Partition IRQ/VBI scratch. Publish a capture only for the still-active collection.
Prove this ordering at every actual CPU instruction frontier, including NMI
before busy-set, between status/code/publication/ack and after busy-clear. This
is an explicit new policy, not retroactive acceptance of the parent. Callback
code may not mutate the interlock or acquisition state. No recursively nested
NMI contract is proposed.

Cart callbacks may not touch selector, SKCTL, POKMSK/IRQEN, POTGO or acquisition
RAM while active. CRITIC must suspend window advancement coherently: retain the
selected port/capture while paused; resume may consume an older contact sample
and must not promise fresh input. Define disable as mask/ack40 before invalidating
state, with no fabricated releases. Review timer concurrency and pause fixtures.

The first-capture latch caps software keyboard IRQ work at one accepted request
per collection window; reassertion/disabled-tail timing still needs actual CPU
checks. CPU I must normally permit IRQ during collection. No polling spin loop,
host timer, direct input injection or emulator functional mode is proposed.
Missing capture with a masked CPU cannot silently count as a valid release;
activation preconditions/invalid-window behavior must be resolved in review.

Bottom Fire: sample all four GTIA trigger inputs every eligible VBI. Top Fire:
sample the selected port only after settling; proposed SKSTAT shift/KR2 route
is confirmed by Mars prose to observe selected KR2 independently of keypad
capture, once per64 ticks: stable selection up to7296 machine cycles plus read
frontier in current Mars; late changes can remain stale. Do not infer fresh top-fire state
from latched KBCODE modifiers. Require unlatched GTIA triggers (GRACTL bit2 clear) through explicit cooperating
cart ownership: latched low can persist forever through release. GRACTL is write-
only, so no readback validation or silent graphics/latch clear is allowed. Bottom
reads use the existing post-run input cache; measure that delay. First valid fire sample establishes
a baseline without invented activation edges. Subsequent changes emit old/new
bitmaps, bit0 bottom and bit1 top. Bottom and top updates can emit two ordered
transitions at the same boundary. Four bottom events precede selected key event,
then selected top event. IRQ capture itself must not call user code.

## RAM, callbacks and ROM stop rules

Persistent state cannot fit in already committed ZP00..18 or vector padding.
Propose **32 explicit cart-cooperating bytes at0600..061F**, with linker/data
start at least0620 for original diagnostic cartridges. This is NOT spare OS RAM:
cc65 applications currently start021C, so it conflicts without a changed linker
contract. This reservation is accepted for bounded authoring. A separately named opt-in
profile (tentative sb52-dev-input-v2) must
reserve it and bind the new identity; do not claim old cc65/retail compatibility.
Bind cart cooperation, reservation and activation in descriptor/converter preflight;
Linear32K size alone is insufficient. Nothing changes consumer-interface.json/
allocation-plan.json at proposal time.
Exact reservation/profile preflight must be implemented before execution acceptance.

Proposed working ledger: selector1, phase1, captured code1, valid/window flags1,
committed keys4, fire bitmaps4, baseline/enable/interlock/epoch/scratch up to12,
remaining8 reserved for reviewed race handling. Exact byte offsets, epoch wrap,
critical section and reset defaults are an authoring acceptance item, not assigned
facts. All mutable state must be ordinary serialized machine RAM/chips; no host
shadow state. A disabled/invalid window cannot fabricate a release.

Proposed callbacks:020A key transition,0208 fire transition, A=port0..3,
X=old, Y=new; key FF is a SOFTWARE no-contact value after normalization,
fire values0..3. Called from saved-AXY VBI via a JSR-to-indirect-JMP bridge;
callback returns RTS and may clobber AXY/flags, runtime must restore its own loop
state. This differs from timer's JMP-vbi_exit and DLI's RTI. Both callbacks must
be installed before activation; disabled cold defaults remain FC86 Metadata
fault. No callbacks during IRQ capture. One NMI preempting IRQ is a NEW contract requiring proof: IRQ hardware3+savedAXY3
plus VBI hardware3+savedAXY3 plus bridge2 is14 bytes before helpers/callbacks.
An input helper JSR adds2 more. Include classifier temporaries and timer/DLI
paths; prohibit recursive NMI/CLI-in-callback and unqualified reentrancy.
The old32-byte estimate is not approval.

Parent usage1504/2048, total unwritten544 includes250 RESERVED margin; only294
bytes are available without an allocation change: startup18, interrupts115,
input123, display33, shared5; clocks0. Propose cumulative additional code ceiling
**266**: input123, interrupts105, startup14, display20, shared4, leaving28 regular
bytes and all250 margin. These are allowance ceilings, not compiled sizes or a
fit proof. Interrupt/input helpers may use their remaining contiguous subranges;
clocks are full. If code cannot fit, stop for explicit allocation/font/scope review.
No stealing font, vectors, conio, padding or margin; no new bank or RAM code.

## Independent acceptance packet after review

- Finalize exact RAM offsets/reset/disable/activation/clock continuity and
  implement reviewed interlock/invalid windows/single frame; validate corrected
  fire/contact/latency/profile assumptions and actual byte budget.
- Author separate cumulative candidate/export with new identity, old pins intact;
  strict manifest/converter/state/profile refusal and all approval flags false.
- Actual CPU15keys x4ports across all scan phases; hold/release/repress/change,
  stale code, no capture, masked CPU, selector-boundary arrivals, aliases, overrun,
  repeated requests, CRITIC/pause, concurrent timers and NMI preemption points.
- Both fires all4ports independent of keypad, simultaneous holds and baselines;
  four-pad and mixed Trak-Ball topology, analog endpoints/prime/pending/restarts,
  shared clock/audio configuration interactions and no repeated SKCTL reset.
- Validate callbacks AXY/frame/RTS and no wrong-port events, measured CPU/IRQ
  counts and max operation latency with DMA on/off. ~150ms is not accepted until
  measured and judged adequate. No game/device/energy claim from cycle fixtures.
- Same/repeated/fresh-process state replay at real native safe frontiers across
  settle, armed, captured, commit and selector transitions; prior seven variants
  and R65/default-off/lifetime/firmware hygiene regressions. Strict full identity
  refusal before mutation. No new emulator serialized fields proposed.

## Offline policy checks and limits

Eight tests cover1024 old/new contact transitions across4ports, repeat suppression,
release/repress, four-port isolation, all32 scheduler start/target combinations,
settle contamination refusal, both-fire ordering/baselines, strict scalar inputs, invalid-window preservation
and deterministic policy replay from48 boundaries. This is a planning-level
reducer, not an emulator/test oracle or binary/runtime acceptance. Hardware
acquisition and race coverage must be authored independently by the integration
owner. No firmware, primary scan, foreign implementation/test or new external
source was read. Reuses permitted interface prose and original event choices.
