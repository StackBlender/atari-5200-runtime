# Cumulative both-fire development candidate

Authoring follows Mars2784b289ff54849cb4f7301556a79fd2d5f3bed6/msg_e667
bounded experimental review of proposal98a31b7. Native execution, complete reset/
remaining services, provider integration/release and game support are NOT accepted.
All mandatory review qualifications below override older planning shorthand.

## Actual static image and allocation

Separate tools/fire_image.py authors2048 bytes,1902 written/146 unwritten:
398 above timer1504,2 below the explicit400-extra ceiling. New separate
fire-allocation.json assignsFF00..FF9F160code, FFA0..FFF990reserved; source
rejects changed160/90 bounds and >1904written. Old allocation-plan.json and all
nine older generation inputs/250-margin exports remain immutable.

|Region|Written/allowance|
|---|---:|
|Font|1024/1024|
|Startup|120/128|
|Interrupts|167/192|
|Input|166/176|
|Clocks|96/96|
|Display|95/96|
|Shared|75/80|
|Fire|153/160|
|Margin|0/90|
|Vectors|6/6|

56 ordinary fragmented bytes remain, including7 in new fire region. These and
90reserved are not permission or a promise for complete reset/remaining services;
a further measured cumulative fit/refactor review is required. No banking,
extra RAM or font reduction. ROM SHA256:
e937064b0d1fe33d0f75cfe4dba89bcbec953adc215f83ed51ce4fee8705f815.

Exact changed hooks relative to accepted windowsfce294b:
analog_exitFD56 JMPFF00; equal-key BEQ atFCE2 targetsFC96 (displacement-78);
near top_fire_entryFC96..98 JMPFF51; changed-key tailFCF6 JMPFF51.
BottomFF00..FF50 continuesFD1A window_entry. TopFF51..FF95 continuesFD59
window_rotate. Fire callback bridgeFF96..FF98 JMPind0208. SevenFF padding bytes
FF99..FF9F and all90 FFA0..FFF9 remain unwritten. Every other parent byte, including
font, cold startup/metadata/handoff, IRQ/timers, analog copy, clock, display,
helpers and hardware vectors is preserved. All branch/call symbols resolve to
emitted instruction starts; allocations reject collisions/crossings.

## Event, storage and cooperation contract

fire-profile.json defines separately reviewed ABI sb52-dev-input-fire-v3,
profile ntsc-four-port-cooperating-input-fire-development and BEFORE-CONNECT
frozen declaration sb52-dev-input-fire-v3-ram600-61f-unlatched-v1. This is a
caller assertion of cooperation, not automatic detection of later violations.
No old-provider/old-cart declaration or state may pass new identity by size/prefix.
Native payload RAM already covers fields; no new native field is proposed.

Existing0600..060A unchanged.0610..13 four fire bitmaps bit0bottom/bit1top;
0614 all-bottom-ready;0615..18 four independently ready top flags;0619 port,
061Aold,061Bnew VBI-only scratch.060B..0F and061C..1F reserved. Same32-byte
cold zero loop covers all. Application>=0620; no added persistent RAM.

Quiescent foreground SEI/NMI-off activation, no suspended IRQ transaction:
keyboard mask/ack coherently off, install0208 fire and020A key RTS callbacks,
initialize fire state/readiness/scratch0 and key contactsFF, configure continuous06,
analog power and settled selector/phase1, explicitly maintain GRACTL bit2 clear
while retaining intended graphics bits, enableLAST. Disable mask/acks keyboard
before invalidation without fabricated releases. Reenable repeats full setup and
both source baseline sets. No competing protected/input/mask writers.

Eligible VBI analog precedes four bottom samples (ports0..3), optional key event,
then selected top after successful key close, then rotation. Bottom C010..13
cached active-low bit0 merges retained top; all first bottom samples silently
baseline,0614 set only after all4. Top independent SKSTAT E80F active-low bit3
merges retained bottom; first sample of EACH selectedport silently baselines.
Only changed later observations callback0208 Aport/Xold/Ynew bitmap0..3, committed
store first, then RTS through bridge; reload index from private RAM after scratch
AXY/flags callback. No KBCODE-derived top or keyboard acknowledgment in fire code.

Old/new bitmap sources are independently AGED committed observations, never
simultaneous physical state. Unknown is not released. Consumers consult readiness
and adopt initial baselines silently from RAM; a baseline can change a bitmap
without a callback. Retaining the other bit proves no physical stability.

Bottom may run while IRQbusy only because its writes are disjoint. Its callback
must not assume protected key/mask fields form a coherent snapshot midtransaction;
read-only does not imply coherence. No reserved/input/scratch/mask/selector/GTIA/
NMI writes, CLI, BRK, recursive interrupts, service reentry or unbounded waits.
Use only callback-owned application RAM/stack. Top/window defers whilebusy or
invalid; bottom effects MAY precede a later invalid window fault. No global
premutation service-fault guarantee. CRITIC skips VBI commits/analog/display/fire,
but independent IRQ capture can still publish during CRITIC.

## Timing and hardware limits

GTIA bottom is polled after ordinary System::run returns. Runtime register reads
and callbacks do not refresh host cache. Acceptance must use uninterrupted frame
returns and both sides of post-run poll; Event::Step instrumentation changes
poll cadence and is not sufficient end-to-end latency evidence. GRACTL bit2 is
write-only; unsupported latchedlow mode can conceal release indefinitely. Cart
assertion does not inspect/readback or detect all later invalid latch writes.

Selected KR2 can age up to7296cycles+read, independently of keypad. Full settle
required; near-close changes may wait another rotation plus scan age. Busy,
CRITIC, invalid/missing-mask/pending windows add unbounded deferrals. No general
eight-interval freshness, lossless short taps/chords or physical/mobile deadline.
Measure bottom/top host-input-to-callback separately/allports/simultaneous/aliases.

Each callback <=128nominalcycles includingRTS, up to6sequential =>768 allowance,
not a full bound. New diagnostic target4096 FULL hardware-entry-through-RTI,
including callbacks/refresh/carry/analog/window/fire/display, DMA-off ordinary
refresh. Separate cold-start4096watchdog and old2048window target unchanged.
Arbitrary DMA/RDY/custom waits excluded. No measuredfullcycleflag promoted.

IRQ6+VBI6+bridge2=14 before BOTH interrupted and new callback/helper stacks.
32 remains unproved estimate; sequential callbacks do not multiply bridge depth.
Native all256SP, classifier temporaries, timer callbacks and permitted nesting
must qualify actual depth. No arbitrary callback-depth or recursive NMI guarantee.

## Export and next independent acceptance

Unexported CLI: python3 tools/fire_image.py --output-dir build/fire.
After generation inputs are committed, tools/export_fire_candidate.py requires
--source-revision FULL40 --output-dir build/fire-candidate. Strict verification
checks every baseline and new source/allocation/profile/export/CMake byte before
output. New allocation identity is SHA256-bound in map/manifest provenance.
All execution/provider/retail/full-cycle flags stayfalse; capabilities empty.
Authoredcapabilities adds both-fire-v1, not accepted service claims.

Opt-in parent: add_subdirectory(module...), include cmake/fire-candidate.cmake,
set SB5200_FIRE_SOURCE_REVISION=FULL40; target sb5200-fire-image exports the four
absolute image/manifest/map/full-source properties. No existingdefault target is
changed. Mars still requires its own explicit new tuple integration before any
CPU run; do not pass a wrong variant to bypass the converter.

Eight additional methods bring155offline tests: all153 relocated bytes, exact
four hooks/branches/only-changed-region diff, unchanged parent identity/font/
startup/kernel/vectors, budget/reserve/stop failures, new profile/review limits/
provenance/false flags, all pinned inputs fail-closed and freshprocess equality.
No second CPU/chip model or manufacturer observation supplied.

Next independent Mars packet: exacttuple/artifacts/4props +native bothlogicalfire
channels/fourports/aliases, independent baselines/reenable/holds/releases/repress/
no repeat/simultaneous ordering, GTIA unlatched/cache/latchednegative with ordinary
framepoll, KR2 phases/settle/staleness, busy/NMI/allSP/timer/CRITIC/invalidwindows/
clobber/RTS/six128cyclecallbacks/fullVBI timing, analog/TrakBall/sharedclock/audio
write whitelist, safe repeated/fresh/process replay INCLUDINGcallbacks, full
new/old declaration/profile/state preflight/converter negatives, earlier9variants/
R65/defaultOFF/lifetime/firmware hygiene. Fullreq_6f74 remainsopen/noACK.


## Committed export receipt

Generation pin a2a7455627a9ea3905464c295562debee2efec7d, imagee937064b above.
Manifest file SHA2565480b4472a78cb1092732d73e0e6cc242a8c280327e6c8452427dc0a8182ec06;
map file SHA2561b942e04c5be03e742393b87075c694f86c26b5d6013b9ad688c068df01b3e04.
155 unittest/build/CTest1/1 pass. Actual pinnedCLI +ephemeral parentCMake
fourprops/dependency-before-consumption/artifactbyteequality PASS. All9older
real pinnedCLI exports reproduce unchanged. Temporaryparent removed; no new
persistentbuildroot. These are offline/static/export checks, not native execution.
