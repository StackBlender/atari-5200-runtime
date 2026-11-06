# Atari 5200 Runtime roadmap

StackBlender will complete and freely share this original runtime. Initial scope
is NTSC four-port, followed by evidenced differences and broader compatibility.
The first image fixture is a build-tool test, not an implementation milestone
for cartridge startup.



## Next

## Reviewed bridge refactor authored; native qualification next

Mars2ffaa687/msg_b2c1 approves boundedbridge deduplication alone andpreserves
coldreset/refusal/input-vs-game distinctions; no numericreset evidence supplied.
New fire_bridge_image.py/export_fire_bridge_candidate.py +optin CMake
fire-bridge-candidate.cmake/sb5200-fire-bridge-image/SB5200_FIRE_BRIDGE_SOURCE_REVISION.
Actual1895written/391extra/9under1904,146/160fire,63ordinaryfree/90reserve untouched.
SHA c5fd8df1564c28e5ed4c5aad9f8eabdc64a62e32de28e8dcce6bfae7ea533d24.
New topFF4A/bridgeFF88..91, JSRFF37/FF7A returnPCFF39/FF7C ->reloadFF3A/FF7D.
OnlyFC96/keytail/newfireblock change; old10inputs andsamefire-v3allocation/profile
immutable. No addedstack/RAM/field/service, allflagsfalse/OFFdefault unchanged.
Sevennew exactbytes/budget/profile/identity/refusal/freshprocess methods bring167.
See fire-bridge-proof.md. Next committedpin CLI/CMake+10olderexports, exactnative
handoff/requalification inclordinary midVBI/frame/cache/movedsetup snapshots.


## Next reset/service contract and measured bridge refactor review

Current accepted fire-v3 remainsunchanged. remaining-services-review.md now
inventories reset/unusedBreak-serial/attract/metadata/fullfont/retailprofile/
consumer gaps with explicit closure requirements, not completion by exclusion.
Coldreset vsController Reset4/Pause8/Start12 input vs warm/CPU-only unknown
contracts are separated; requestowner permitted evidence/behavior review before
newresetcode. New NONRUNNABLE fire_callback_refactor.py measures common argument
setup in existing bridge:146vs153bytes,7saved, noextraJSR/stack/RAM,21nominal
callback setup-call-bridge sum unchanged. Projected1895/391extra/9ceilingheadroom/
63ordinaryfree,90reserve untouched; NO cumulativeemission orpermission fornew
services. Five exactbyte/projection/noapproval/preservation/freshprocess methods
bring160offline tests. Validation160unittest/build/CTest1/1 PASS.
Existingaccepted10generationinputs unchanged. Next owner
review ofresetcontract evidence andboundedrefactor, then newpinnedcumulative
image/proof/native identity/cache/frame/NMI/SP/process qualification ifapproved.


## Both-fire native qualification received; next reset/service review

Mars4e6a3a55412b9aaf7a1f5452344489aac8f43292/msg_0343 independently
qualifies a2a7455/imagee937064b for bounded development. Releaseunity/nonunityASan
892firecases/26same-freshroot-processfrontiers, all16controller topologies,
256KR2phases, all256SP14/20byte nested programs, six128cycle callbacks andactive/
pendinganalog pass. Inheritedwindow/keypad/IRQ/timer/analog/display/DLI/R65,
32converternegatives/10tuples/defaultOFF/firmware pass; old9native variants not
allrebuilt. See independent-execution.md for exact attribution/limits.
CRITICAL: ordinary frame return can occur MID-VBI/callback. Preserve ordinary
post-run controller poll; do not forcequiescence/EventStep. Serialize actualcache/
stacks and restore hostinputs before native import; stalehost/cache andmidVBI
frame-boundary replay pass in owner's probes. No frame=VBIcompletion assumption.
Sampled fullentry1835<4096; bottom28827..58853/top<=239036machinecycles, notphysical/
mobiledeadline.1902/1904written,153/160newblock,90reserveduntouched,56ordinaryfree.
Old9allocations/falseflags/OFFdefaults unchanged. Pooled/no newrelease; MR43latest,
consumeradoption separate. FullR62 open/noACK; reset/remainingservices/game/app/
multiplayer incomplete. Next enumerate reset/remainingservice contracts andtheir
actual cumulative fit/refactor proposal BEFORE emission;2ceilingheadroom isnot
permission tospend remaininggaps/reserve orclaim completefit.


## Both-fire cumulative candidate authored under explicit review

Mars2784b289/msg_e667 authorizes boundedexperimental fire-v3 withmandatory
aged/readiness/busy/cache/latch/CRITIC/latency/stack/timing corrections; see
fire-proof.md and separate fire-profile/allocation JSON. Original cumulative
fire_image.py now emits1902/2048written,398above timer,2under400ceiling,
153/160newblock and90reserved untouched,56ordinaryfree. Exact hooksFC96/FCE2/
FCF6/FD56 and153relocated bytes tested, cold/kernel/font/vectors preserved;
all9oldgenerationinputs unchanged. NewABI sb52-dev-input-fire-v3/frozen unlatched
contract/32RAM unchanged. Standalone export_fire_candidate.py +optin CMake
fire-candidate.cmake fourprops; allapproval/fullcycle flagsfalse. Eightnewmethods
bring155offline tests. Full nativefit/behavior/provider integration notaccepted.
Further remainingservice fitreview stillrequired; no extra margin or arbitrarygame claim.

Pinned source/export a2a7455627a9ea3905464c295562debee2efec7d pushed.
Validation155 unittest methods/build/CTest1/1 PASS. Real committedCLI and
explicitpin temporaryparentCMake dependency-before-consumption/fourproperties/
image-map-manifest byteequality PASS; all9older realpinnedexports unchanged.
Temporaryparent removed, generatedartifacts ignored in existingbuild. Exact
nativepacket sent Mars under req_6f74; fullrequest remainsopen/noACK. NoCPU/native
fire/state/provideracceptance or apppin/default/release change. Next independent
newtuple integration +full nativepacket, then remainingreset/service fitreview.


## Automatic keypad windows independently accepted

Mars64f2485d67a4f8cff71c89719ee6796a29251249 /msg_b0cb independently
accepts fce294b/image3c1b419b for bounded development. Releaseunity/nonunityASan
4534cases(3840natural+694supplemental),18same/fresh/process windowfrontiers,
57key+93combinedkey/timer syntheticNMI instructionfrontiers/all256ordinary+nested
SP/128cycleRTScallback/pending-mask/busy/lifecycle and inheritedsuites PASS.
CRITIC defers VBI commits but IRQcapture canpublish; no globalinputfreezeclaim.
Final502focusedcases: postvector624 +hardwareentrypeak8 =>conservative632<2048
for sampled diagnosticpaths. Changeaftercapture267156cycles(~149ms emulatedNTSC),
selected->armminimum26848; no physical/mobile latency or fullinputdeadline.
R65/defaultOFF/24converternegatives/mutualfoundationrefusal/9tuples/budget/
firmwarehygiene pass; old8nativevariants notallrebuilt. Pooled/no newrelease,
MR43 remainslatest. Old generationinputs/falseflags/OFFdefaults unchanged;
fullR62 staysopen/noACK. Read only owner prose a52-keypad-window-development.md,
not producerimplementation/tests. Next BOTH-FIRE explicitallocation/profile
review (98a31b docs/fire-allocation-review.md+JSON, prior msg_d13f) before any
cumulativeauthoring:1902projected needs398extra/160reserved-byte reallocation,
90retainedmargin; old52ordinary/24ceilingheadroom cannotfit. No approval inferred.


## Original cartridge callback recorder prepared

RUNTIME-004: tools/input_callback_probe.py supplies an80-byte NONRUNNABLE
cartridge-side key/fire callback fragment, separate from pending runtime ROM
allocation. Two RTS entries, ordered32-record log(kind/port/old/new), complete
count publishedlast, fullflag withoutoverwrite; cartRAM0700..06/0800..7F defaults,
strictrelocation/disjointbounds>=0620. Host snapshotdecoder validates coherent
counts/cursor/overflow/ranges/changes, no acquisitionclaim. Five original byte/
cycle/bounds/syntheticformat/freshCLI tests bring147offline methods.
Validation:147 unittest methods/build/CTest1/1 PASS; diff check clean. Nominal97
cycles inclRTS, full<=43 (notstall-inclusive/native proof), noextra push/helper,
no MMIO/input/mask writes. See docs/input-callback-probe.md for owner/initialization/
quiescentread conditions and exact native TODO. No completecart/CPU/image/provider
or acceptedallocation/profile/physicalevent claim; all generationinputs unchanged.
Next owner allocation/profile msg_d13f +automaticwindow msg_d22f, cumulativefire
candidate/native validation, then complete diagnosticcart under exactcontract.

## Static fire-fragment boundary audit

RUNTIME-004 next: retain allocation/profile stop pending Mars msg_d13f; window
execution msg_d22f also pending. Added independent static fragment access/control
allowlist (tools/fire_fragment_audit.py): rejects forbidden hardware/key/mask/
selector writes, write-only readback, indexed base changes, branch escapes or
operand targets, altered callback/exits and unsupported control opcodes. Six
mutation/CLI tests bring142 offline methods. Conditional indexed footprint
0610..061B requires reviewed X0..3 invariant; no register/flag/memory/chip/CPU
simulation, timing bound, reachability or callback behavior proof. No generation
input changed; fragment and all9 prior image identities unchanged. New audit
does not approve allocation, native fire execution, provider or game support.
Next accept/correct owner review, then cumulative candidate and native packet.

Validation:142 unittest methods, existing build and CTest1/1 PASS.


## Both-fire code measured; cumulative allocation review required

Original NONRUNNABLE fire_service_fragment.py emits153-byte code,6new exact-byte/
budget/provenance methods (136total). Both-fire routines plus3-byte routing bridge
project1902total/398above timer: exceeds current266ceiling and52ordinaryfree.
NO cumulative emission/reserved consumption: fullfont/9oldproviders unchanged.
Concrete review docs/fire-allocation-review.md +fire-allocation-proposal.json
propose160codeFF00..FF9F,90marginFFA0..FFF9, bounded400extra for this extension,
0610..1B fire/baseline/VBI scratch within existing32RAM, new input-fire-v3 frozen
unlatched-cart contract. Native tests/profile/actual fit remain unapproved.
Validation:136 offline unittest methods/build/CTest1/1 PASS; currentwindow
explicit-pin CLI/CMake and all8older exports reproduce unchanged (9total).
No current generation input changed. Next obtain Mars allocation/profile/behavior
review on ongoingR62, THEN separately
emit/export cumulative bothfire image and independently test CPU/input/state.

## Current RUNTIME-004 both-fire fit review

Author a NONRUNNABLE original bottom/top fire fragment to establish exact size
and state/callback ownership before changing cumulative allocation. Current
windows1746 leaves52 regular bytes and only24 before266extra ceiling. No actual
reserved margin/font/vector/old provider is changed. Bottoms4per eligibleVBI,
selectedTop afterkeycommit/before rotation, independent first-source baselines,
0208 RTS callback old/newbitmaps, unlatchedGTIA/postrun/selectedKR2 qualifications.
If it exceeds budget, stop at concrete code/size/state review with Mars on R62;
no cumulative fire candidate or margin consumption until allocation review.

## Committed automatic keypad export receipt

Immutable source/exportfce294b7448a7c5a1a35e6c5e5ed5611ee36473f. Real pinned CLI
and ephemeral parent CMake consumer PASS: four absolute-artifact/full-source
properties, generation-before-consumption, profile/falseflags/map+image hashes
and byte-exact CLI/CMake outputs. All8 earlier pinned CLI exports reproduce
unchanged hashes.130 offline unittest methods and existing build/CTest1/1 PASS;
diffcheck clean. Temporary parent source/build removed; ignored outputs remain
build/keypad-window-candidate. No nativeCPU/latency/state/profile/game acceptance.
Next independent automatic-window/keycallback/IRQ-NMI/timer/analog-loop/state
execution via fullopenreq_6f74, then bothfires with cumulative budget review:
1746written,52nonmargin free,242above timer leaves24 before266extra ceiling.
No margin use/old9profile aliasing/falseflag/default/app pin/fullR62 change.

## Authored automatic keypad windows (native execution pending)

Separate keypad_window_image.py/export_keypad_window_candidate.py/profile/CMake
implements eligibleVBI four-port settle/collect rotation, pending-before-ack and
busy deferrals, per-port held keys/RTS callback020A, coherent arm/mask ownership.
Explicit quiescent activation setskeysFF/settledport0/phase1/callback before enable;
disable masks before invalidating, emits no release. Cold remains disabled.
Analog ascending loop saves28ROM at65nominal completed-copy cycle cost; must
requalify actual bus/analog/timing/state. Image1746/2048,52 ordinary free plus250
reserved, net242 above timer:24 left before266extra ceiling. Fire remains NEXT
and needs actual cumulative fit/refactor/allocation review. Nine new offline
methods bring130 PASS; no CPU/native/event latency/profile/product acceptance.
Exact proof docs/keypad-window-proof.md. Next committed CLI/CMake/8old exports,
then native window/callback/frontier/analog/state acceptance via ongoingreq_6f74.

## Current RUNTIME-004 automatic keypad windows

Author separate keypad-windows-v1 atop accepted IRQb2e2b40: eligible VBI rotates
four ports, one full settle+collect interval, busy/pending-before-ack invalid
windows defer without release, per-port held contacts and RTS key callback020A.
Cart activation explicitly initializes keysFF/selector/phase under NMI-off/SEI;
disable coherently masks before invalidation; cold stays disabled. Fire remains
next. Compact ascending analog loop trades28 ROM bytes for65 nominal complete
cycles; actual timing/acquisition must be requalified. Preserve all8old inputs.
Acceptance: independent bytes/fit/profile/old-export invariants, real source-pinned
CLI/CMake, then actual CPU windows/NMI/timer/callback/state execution via R62.

## MR-43 released; runtime completion still open

Mars msg_108d releases annotatedMR43 ed99d3fc4c8c453665fbfd144fed28e5626ded77,
localtag verified. This supersedes pooled/unreleased notes for the eight bounded
R62 variants and R65 snapshot/lifecycle work. Consumer adoption is separate;
OFF-default/development-only/false candidate labels remain. Fullreq_6f74 staysopen,
noACK. Keypad input-v2 requires frozen preconnect cooperating-cart declaration.
Next automatic windows/four-port rotation/contact callbacks/bothfires and exact
reset/disable/stack/fit; then remaining service/retail ABI/authorized-game evidence
and complete-app/device/local-online qualification. MR43 release is not full BIOS
or game support. Preserve archives/old executable when old synchronized states
refuse on consumer adoption under already accepted policy.

## Independent keypad IRQ foundation acceptance

Mars003e782458dfe82ca3baeb96e97a179844a1b917 /msg_4f5f independently accepts
exact keypad-irq sourceb2e2b40d8c11326f1684635e35832fcc50f9f2d6 and image2fa0cbdb
as a bounded development foundation only. Releaseunity/nonunity DebugASan both
pass4465 native cases plus explicitly synthetic raw-code0 negative,93 source-
qualified synthetic nested-NMI instruction frontiers,14keypad+14timer native safe-
frontier same/repeated/fresh-process replay,1302 inherited IRQ/BRK/timer cases,
53 fastanalog and priorVBI/display/DLI/R65 controller/wire/process/lifetime checks.
24 converter negatives and mutual old/new state refusal pass; all8 tuples/font/
vectors/250margin and defaultOFF/43-image firmware/tree/history/3build hygiene pass
per owner. No local CPU rerun, physical timing, arbitrary midinstruction/nested
reentrancy/game/device qualification or full input-service acceptance.

Before cartridge connect set pak runtime-cart-contract=
sb52-dev-input-v2-ram600-61f-v1. Declaration frozen at connect, bound in sb52rt-dev2
provider identity, required before power/import. Mutable-pak edits cannot repair
missing/wrong/oldcc65/size-only declaration; disconnect/reconnect required.
Old variants reject newly declared carts too. No new native payload field.
This asserts cooperation, not proof arbitrary cartridges reserve0600..061F.

Actual cold1581normal/1588boundary machine cycles,520/523 instructions; static
1471/1478 is NOT measured full timing. Phase-matrix input install to IRQ return
max4004cycles excludes automatic-window waiting, no event deadline. Maximum
tested timer callback+RTI183 excludes hardware entry. Fastanalog timeout229/
prime/pending/CRITIC/TrakBall/sharedclock state replay passes, not hardware audio
or host/battery proof. Native serialization uses existing safe boundaries only.

Next automatic settled windows/rotation/contact callbacks and both-fire services
under9654ecb corrected policy, exact reset/disable/CRITIC/stack/fit and native
validation. FullR62 req_6f74 remains open; doNOTack full request. Integration is
pooled/unreleased; old8exports/false flags/OFF defaults/app pins unchanged.
Read only owner prose a52-keypad-irq-development.md, no producer implementation/
tests/firmware or primary reference exposure.

## Committed keypad IRQ export receipt

Immutable source/exportb2e2b40d8c11326f1684635e35832fcc50f9f2d6. Real pinned CLI
and ephemeral parent CMake consumer PASS: four absolute artifact/full-source
properties, dependency-before-consumption, profile/RAM/false flags/hash binding
and byte-identical CLI/CMake artifacts. All seven earlier pinned CLI exports
reproduce unchanged hashes.121 offline unittest methods/build/CTest1/1 PASS,
diff check clean. Temporary parent source/build removed; ignored artifacts in
build/keypad-irq-candidate only. No native/CPU execution claimed. Next send exact
source/profile/contract/proof to ongoingreq_6f74 for independent converter/cart
preflight/IRQ-NMI-timer/fastanalog/state acceptance; complete VBI/contact/fire next.
No new default/app pin/approval flag/fullR62 completion. Public runtime lease
released only after push. RAM/profile contract is explicit cooperating-cart,
not backward-compatible with legacycc65/retail software.

## Authored keypad IRQ latch foundation (execution pending)

Separate tools/keypad_irq_image.py/export_keypad_irq_candidate.py and
cmake/keypad-irq-candidate.cmake implement the first executable subset of reviewed
keypad/fire policy: one saved IRQ frame, busy across keyboard/timer transactions,
normalized first-handler-read latch, canceled-entry return, cold32-byte RAM and
new explicit sb52-dev-input-v2 cooperating-cart contract. docs/keypad-irq-profile.json
and docs/keypad-irq-proof.md bind exact RAM/selector/phase/window ownership and
before-power cart declaration. Automatic VBI rotation/events/fire remain NEXT,
not implemented. Image1613/2048,435 unwritten incl250 margin; net109 above parent.
Nine new static/export tests (121 total) pass. No CPU/native/profile/game proof.
Next committed CLI/parent CMake receipt and independent kernel/frontier/fastanalog/
state execution on ongoingreq_6f74, then remaining cumulative input services.
Earlier seven exports/03/profile/flags/defaults/app pins unchanged.

## Current RUNTIME-004 executable IRQ acquisition foundation

Implement a separate keypad-irq-latch-v1 cumulative candidate first: cold32-byte
cooperating-cart RAM/new ABI, continuous06 prime, one saved-AXY IRQ frame, busy
through all timer/key mask transactions, source/phase validation, normalized
first-handler-read latch and bounded canceled-entry return. Diagnostic cartridge
explicitly arms/closes windows under reviewed ownership. This slice deliberately
does not claim automatic VBI rotation/contact events/fire services; those follow
within the cumulative budget. No callback IRQ path. Acceptance: exact bytes,
range/old-profile refusal, startup/helper/stack/static paths, pinned export/CMake
and independent CPU/window/timer/NMI frontier execution via ongoingreq_6f74.
All seven earlier exports/policies remain immutable. No default/provider enablement.

## Keypad/fire revision2 authoring scope accepted with corrections

Mars9654ecb239d87abfe3ddf518ab74150c50004b40 /msg_0c5f reviews proposal1.
Revision2 incorporates busy across TIMER mask transactions, pending-before-ack
invalid-window deferral, first-handler-read (not first chip capture), one NMI-over-
IRQ peak14+helper/callback bytes and single saved frame, top-fire independent
KR2 latency7296+read, unlatched GTIA/post-run cache ownership, IDs1..15 only,
and corrected conditional near9-interval/~150ms latency (8 was wrong). Both03/06
already enable shared polynomial/prescaler; requalify fast pots/audio separately.
32 cart-cooperating bytes/new profile allowed for bounded authoring, not oldABI.
Planning reducer now refuses0 and supports invalid/busy windows without releases
or selector advance. Next exact RAM/reset/preflight and separate cumulative byte
candidate within266-byte ceiling, then independent real CPU/frontier/analog/fire/
state tests. No new image, actual fit, execution/profile/product acceptance or
fullR62 completion. Existing seven exports/flags/defaults/pins preserved.
Validation:112 offline unittest methods PASS, CTest1/1 PASS, diff check clean.
Review incorporated; next byte authoring needs no further human permission.

## Current RUNTIME-004 keypad/fire planning slice

Original proposal1 in docs/keypad-fire-brief.md and tools/keypad_policy.py/tests
specifies two-interval four-port windows, fresh-capture provenance and no-repeat
contact events, independent bottom/top fire, explicit opt-in06 analog/audio
change, tentative32-byte cart-cooperating RAM/profile and266-byte code ceiling.
This is a review packet, NOT emitted/approved runtime. IRQ/NMI atomicity,
masked-window validity, independent top-fire read and storage/fit must resolve
before byte authoring. No silent03 switch, old ABI/RAM theft or chip correction.
Validation:111 unittest methods PASS (seven new planning methods), existing
build/CTest1/1 PASS and git diff --check clean. No image generation input changed.
FullR62 req_6f74 stays open; next integration-owner review of the committed
packet, then separate candidate only within accepted scope. Current seven exports/provider flags/app pins/defaults remain unchanged.

## Independent IRQ/BRK and timer execution acceptance

Mars msg_30c1 /f32595cb7c67a20395006adf413b6ba310a45b30 independently accepts
IRQ source42762a73a0caa72b7753bd5aa4380cf9a63c573f and timer source
ac9b47e50c213b08022e78bdef64662569cd3d29 as explicit bounded development
variants. Exact original artifacts/semantic manifests/maps/source profiles bind
sb52rt-dev2; no serialized field/chip algorithm/raw behavior change. Source
exports/false approval flags and two OFF-default gates remain unchanged. Prior
five variants preserved. No local CPU rerun or original hardware/game proof.

Release unity/nonunity Debug ASan(-g -O1) owner receipt:514 IRQ/BRK and1303
cumulative timer cases per build, including two explicitly synthetic NMI-vector
placements. All256SP/rotated registers/meaningful flags, actual CPU BRK+2 and
hardware Timer1/2/4, all pending sets, coalescing, exact ack bus whitelist,
selected reassertion and rapid Timer1 starvation pass. Unsupported/spurious
fault before ack; cold timer callback slots acknowledge then FC86 Metadata fault,
while FC83 IRQ meanings remain distinct. Nonnesting/source races remain bounded
contract limits, no lossless/fair/always-quiet or arbitrary callback guarantee.

Generated FC6B handoff, six-store helper order,76 direct cold stores+4 real JSR
writes, returnFC52/FC62 and original final state independently verified. Timer
startup1235 full cycles/422 instructions, worst1242; IRQ startup1212/416,
worst1219. Tested callback+RTI operation max100 generic,159 timer, excluding
hardware entry. These are fixture operation counts, not mobile performance or
unbounded source-rate deadlines. Custom delayed active-display4901 still lies
outside default512 VBI target.

Five IRQ/twelve timer requested native reconstructible safe frontiers pass
same/repeated/fresh-process full-state replay. Valid intermediate BRK capture
must respect those real native safe boundaries; no arbitrary half-instruction
state guarantee. New/old mutual provider refusal and20 converter negatives per
variant pass, plus inherited288 VBI/404 display/128 DLI/59 analog matrices and
process replay. Seven converter tuples, changed-range/budget and250 margin
checks pass. R65 timerRelease/IRQ-ASan standard/mixed four-controller/wire/
process/live-exit and defaultOFF a26 exact/fast/lifecycle/missingBIOS pass.
43-image firmware self-test/tree/history/three build roots clean per owner.

Integration is pooled/unreleased; no app pin/provider default/product/physical
reference enablement. FullR62 remains open for reliable runtime keypad/fire,
reset/remaining services/reference/product acceptance. R70 evidence conclusion
unchanged: no chip correction; next separately reviewed original acquisition/
contact-event/analog policy. Runtime author read only integration prose; no
foreign emulator/kernel implementation/tests or firmware reference exposure.


## Reviewed keypad evidence complete; IRQ/timer execution next

Mars f3b991a4637726b5b8122bcfb0357e9ced6f0fa6 /msg_dc77 completes revised
keypad evidence req_72f0, accepted/acked after prose review. Owner visually
verified manufacturer four-port FSM figs2-2A/C and errata: unused scan phases
alias contacts, consistent with documented03 qualification cancellation. Existing
chip/mapping and06 forced-compare behavior remain; no supported chip correction
or opt-in functional mode.120 CPU cases plus7680 phase checks pass Release/
nonunity ASan per owner; not a keypad service or physical reference measurement.
Runtime author read only prose, no schematics/producer code/tests/firmware.
Next original runtime acquisition/event/analog policy needs its own review.

IRQ/BRK scope accepted f3b991a /msg_c9ef; all256SP arithmetic, saved flags,
BRK+2 and static39/40 agree. Important existing error classification: uninstalled
0200/020E callbacks hit FC86=Metadata, while old unconditional FC83=IRQ. New
fixtures must distinguish these without changing earlier images. Actual tuple/
CPU/IRQ/BRK/stack/state execution not yet accepted for42762a7.

Timer bounded authoring accepted with qualifications d7be9b4ab9f732918ba8880faf4099324fb270ca
/msg_3385; incorporated in brief revision2/proof. Each IRQEN write also clears
OTHER disabled latch sources, preserves other enabled pending bits; serial bit3
has distinct nonlatching semantics. Read/ack/re-enable races and enable/disabled
tail timing mean no lossless/immediately-quiet guarantee. Priority1/2/4 may starve
lower sources; callback AXY/flags scratch, full saved frame6 restored via exit.
Six cold vector stores/shifted helper/handoff and all256SP need actual validation.
Full emitted packet already exists at sourceac9b47e; this receipt changes docs,
not generation inputs/image/flags. Next independent real timer/IRQ acceptance,
then separately reviewed keypad/fire policy, remaining timer/reset/runtime work.
No dependency pin/default/schema/release/app enablement; fullR62 remains open.



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


## Current timer dispatch authored slice

Separate original timer-dispatch-v1 atop pending IRQ42762a7, scope Mars
req_6f74/msg_0296. tools/timer_dispatch_image.py/export_timer_candidate.py,
cmake/timer-dispatch-candidate.cmake, tests/test_timer_dispatch_image.py,
docs/timer-dispatch-{brief,proof}.md. Image SHA
eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550,
1504/2048used,544free incl250margin. system_timerFE00..FE4F80bytes, single
IRQST snapshot+POKMSK, priority1/2/4, two maskwrites thenvectorcallbackJMPexit.
Startup helperFEDC31bytes sets0200FE00 plusoldVBIdefaults; startup110/128
(18free), JSRhelperFC50/returnFC52 andmetadataFC60/returnFC62, handoffFC6B.
No extra RAM or autointerruptenable; nominal startup1148/1155 andtimerbody
56/62/67cycles, no hardware timing acceptance.104 offline methods/CTestpass.
Pinned export/realparent check follows commit; independent Mars scope/CPU/
sourceack/RTI/replaypending. Keep keypadreq72f0 separate and acceptedanalog03
source/defaults/pins/flags unchanged. Next independent packet then source-specific
keypad/fire/reset and remaining software timer/runtime compatibility contracts.

Current authorized RUNTIME-004 continuation: original timer-dispatch-v1 plus
startup vector-helper refactor, docs/timer-dispatch-brief.md. Keep keypad
req_72f0 separate, accepted analog03 unchanged. Source masks/ack/callback policy
sent Mars req_6f74/msg_0296 for review. Author separate candidate, independent
exact-byte/budget/negative fixtures and pinned export, then real CPU timer/state
acceptance. No release/default/pin or false-label change.


Keypad source review publication repaired (Mars msg_6570): pushed
9349e920d2f3af1302fe68acc4c7533e00f234da, docs/a52-keyboard-source-review.md.
This supersedes earlier push-pending notes. Existing evidence-path decision
msg_69bb was sent before this crossed receipt and reiterated; no outstanding
user/scope choice. Proceed primary5200 wiring review, retain documented06,
withdraw unsupported one-event-per-hold06 chip acceptance. Runtime event policy
remains separate; no chip/schema/image/default/pin/release changes.

## Keypad evidence correction and selected next action

Mars msg_8edd/R70 source screening supersedes the earlier defect attribution,
not the120-case diagnostic observations. Reviewed ONLY local prose
Mars docs/a52-keyboard-source-review.md; its GitHub push repair is pending, so
no pushed source-review commit is claimed. No runtime image/schema changed.

Owner's screened Atari POKEY CHIP Rev3 sheet10 keyboard prose describes compare
qualification, with compare forced true when debounce is disabled. Therefore06
repeated captures/down pulses alone do NOT establish a hardware defect; our prior
one-event-per-held-key CHIP acceptance for06 is withdrawn.03 still needs primary
5200 external scan wiring/timing evidence to decide chip vs mapping behavior.
Neither mode currently supplies an accepted runtime press/hold/release service.

Decision sent on req_72f0: pursue the preferred primary5200 wiring evidence path,
retain documented06 behavior, reassess03 against documented qualification. A
reliable original runtime event policy remains module-owned and must be explicit;
no named opt-in chip functional deviation is selected. If evidence unavailable,
record the precise remaining fact before choosing a different reviewed policy.
No silent06 workaround or claim of measured hardware correctness. User's speed/
battery priority remains, without treating raw scanner pulses as application events.

An incidental disassembly-derived historical magazine lead and foreign emulator
materials were excluded by the owner. Runtime author read no implementation,
firmware, derived constants or source scan; this is attributed prose-only evidence.
Accepted analog03 source/defaults/flags and IRQ/POT/KR2 semantics unchanged.
Full R62 and req_72f0 remain open; next primary wiring/03 review, then original
keypad/fire service contract. Existing IRQ/BRK candidate execution is independent.



## Committed IRQ/BRK export receipt

Source/export42762a73a0caa72b7753bd5aa4380cf9a63c573f is pushed. Real CLI
and temporary parent CMake consumer pass all4properties, absolute artifacts,
dependency ordering, full image/map/source identity/false flags and CLI equality.
All five earlier pinned candidate exports reproduce unchanged image hashes.
Temporary parent source/build removed; ignored output in build/irq-candidate.
Exact tuple/stack/IRQBRK/callback/source-ack/timing packet sent Mars req_6f74;
independent scope/CPU/RTI/state acceptance pending. No local CPU run, provider
flag/pin/release/app/default change. Next independent acceptance and remaining
source-specific IRQ/timer/reset/fire service contracts; keypadreq72f0 separate.
Runtime lease released after push.


## IRQ/BRK authored continuation

RUNTIME-004 adds original irq-brk-dispatch-v1 atop accepted analog; scope sent
Mars req_6f74/msg_5559. New tools/irq_brk_image.py/export_irq_candidate.py,
cmake/irq-brk-candidate.cmake, tests/test_irq_brk_image.py and docs/irq-brk-
{brief,proof}.md. Image SHA256
2b257c582044af2308699c6a0f327dca674ed79bd95eed2da7cea2537ead0675,
1410/2048 used,638 free incl250margin. FD00 classifier26bytes, IRQ/BRK hardware
vectorFD00, slots0200/020E defaultFC86 until cart installs. All earlier bytes/
labels/startup127/128 unchanged. Wrapping TSX+INX3 reads real stackedP, restores
AX, Yuntouched, JMPcallback hardwareframeonly;39/40 basecycles14instructions,
no device-source ack or persistentRAM.95 offline methods/CTest pass; new actual
CPU/RTI/state acceptance pending. Real committed CLI/parent export checks follow.
Next deliver full pinned tuple toMars, obtain independent IRQ/BRK/stack/replay
acceptance; keypadreq72f0 evidence/correction separate. No pin/default/flagchange.

Current RUNTIME-004 independent slice: irq-brk-dispatch-v1 atop analog. Specify
and author bounded CPU-stacked B-bit dispatch to0200/020E with wrap-safe index,
no device-source guess/ack, extra RAM or startup growth. Exact scope/independent
fixtures in docs/irq-brk-brief.md; Mars req_6f74/msg_5559 receives review. Keypad
req_72f0 remains separate; preserve accepted analog/source exports/false labels.

## Next keypad service: hardware-interface dependency

Mars msg_7fe6 /19b9eb69a4b8e6efaafe4a3eff2faeea5805e1a8 supplies prose-only
assessment. Independent original CPU/Node probes reproduce120 cases (15 keys x4
ports x03/06), plus reset/selector/IRQ/KR2/hold/release behavior, in Release and
nonunity ASan. Passing diagnostics means the limitations reproduce, not that
keypad delivery is accepted. No chip implementation/tests read here.

03 fails stable-contact capture after correct reset/selection and16-frame hold;
not an IRQ acknowledgment/read/extra-wait prerequisite.06 captures but held
input alternates down/released and rescans request IRQ/overrun without a new
physical press.06 is NOT an approved workaround. Leave accepted analog image03
and all source pins/defaults/false flags unchanged.

KBCODE retains old code/modifiers after release/port changes; neither FF nor
nonFF alone proves fresh validity. Reads of KBCODE/SKSTAT/IRQST do not ack.
Clearing keyboard bit40 in IRQEN acknowledges/disables; repeating enabled40 does
not. SKREST clears errors separately, not pending IRQ/code. KR2 selected Top Fire
and Bottom Fire remain distinct. CPU I masks entry, not acquisition. Probe settle
29184 machine cycles per transition and06 observed3590-cycle capture maximum
are diagnostic budgets/measurements, not hardware timing specifications.03 has
no demonstrated finite remedy. Retain this distinction for future service ABI.

Formal Mars req_72f0 owns one concrete dependency: permitted primary debounce/
phase/timing evidence and contact stabilization+held/release qualification across
03/06, with replay/compatibility and all previous runtime/controller regressions.
Evidence gaps must remain explicit; no firmware-derived constants, silent fast
mode workaround or guessed hardware-accuracy claim. Full R62 req_6f74 remains
open for runtime keypad/fire/IRQ/timers/reset and product/reference completion.
Next receive the reviewed behavioral correction contract before keypad authoring;
no new runtime code or emission changes in this receipt.


## Independent analog acceptance and keypad limitation

Mars msg_1cd6 /33967abf09dfef07d163f3a14d43502f699ec9cc accepts exact source/
exporta6c406e4cee090b8044eea3b9b6c7a5b6391b3ab as a separate bounded development
tuple. Release unity/nonunity Debug ASan(-g -O1) independently pass startup1212
full cycles/416 instructions, boundary1219; prime order, FC73 helper return,
final state, metadata and early/pending/hijack/reset failures. Existing288 VBI
cases+120 services,404 display and128 DLI suites and safe/process replay pass.
No local CPU rerun or original hardware/BIOS evidence.

Analog59 cases cover eight axes/endpoints,16 connectivity masks, eight one-pending
masks (no partial copy/restart), POTGO-frozen host vectors, cold mixed Trak-Ball,
immediate/long CRITIC and early/mid/late completion. Ten pending/complete safe
points replay same/fresh; pending and mid-copy separate-process final bytes
match.20 converter negatives and mutual DLI/analog identity refusal pass. Existing
R65 sb52rt-dev2 schema/observer unchanged; no CPU/chip algorithm/host service added.

Default VBI max268 full cycles, marker282/broader marker293; entry7 separately.
DLI dispatch37/callbackRTI86. Custom VCOUNT-delayed active-list service4901
(transfer body140) is explicitly OUTSIDE default512 target; no general DMA/RDY/
nesting/callback bound. Old-provider/default-OFF/a26 and Release/ASan standard/
mixed four-controller/wire/process/lifetime regressions pass per owner.43-image
firmware tree/history/three-build checks clean. All source pins/export false
flags/default gates unchanged; pooled unreleased, no app/retail enablement.

IMPORTANT next keypad scope: under current SKCTL03 a held standard key1 leaves
KBCODE FF in the owner's fixture. RANDOM evolves256 values, KR2 SKSTAT F7 with
IRQ masked. This is a separate delivery/debounce debt, not hardware evidence or
an accepted keypad service. R65 direct hardware keypad tests use06 and do not
qualify03 runtime delivery. Investigate through permitted behavioral review
before keypad/fire/IRQ claims; do not silently change the accepted analog image.
Full R62 keypad/fire/timer/reset/reference/product scope remains open.



## Committed analog export receipt

Source/exporta6c406e4cee090b8044eea3b9b6c7a5b6391b3ab is pushed. Real CLI
and temporary parent CMake consumer pass four properties/absolute artifacts/
dependency ordering/full source/image/map identities/false flags and exact CLI
byte equality. All four earlier pinned exports reproduce unchanged image hashes.
Temporary parent source/build removed; ignored artifacts in build/analog-candidate.
Exact artifact/fit/shifted handoff/priming packet sent Mars req_6f74. Independent
execution still pending; do not ack fullR62 or claim acquired first sample from
Ready. Consumer pins/defaults/buildgates/exportflags unchanged. Next independent
POKEY/8axis/pending/midcopy/CRITIC/state-process/lifecycle acceptance, then
specify keypad/fire/IRQ/timers/reset services. Lease released after push.


## Analog shadow authored slice

Approved Mars msg_092a/83a8a400 qualifications incorporated in brief revision2.
Separate tools/analog_shadow_image.py/export_analog_candidate.py and
cmake/analog-shadow-candidate.cmake, tests/test_analog_shadow_image.py,
docs/analog-shadow-proof.md. Image SHA
32343a567399b3b4f9c142bde446fe89397267267d51a89393553fdab9471290,
1384 written/664 free, startup127/128, input53/176, margin250 untouched.
Explicit SKCTL03/CONSOL04/POTGO prime; one ALLPOT read, pending skips copy and
restart, complete copies8 raw bytes to0011..18 then restarts, before display.
HandoffFC7C, metadata JSRFC71/returnFC73/resumeFC74; startup1124/1131 nominal
cycles, default completed VBI240..245, pending179..184. No new RAM/stack.
87 offline methods/CTest pass; real pinned export/parent check follows commit.
No CPU/conversion/provider/product acceptance. Next Mars independently executes
exact tuple; remaining keypad/fire/IRQ/timers/reset need separate contracts.

Current RUNTIME-004: implement approved analog-shadow-v1 revision2. Mars
msg_092a/83a8a400 approves bounded authoring with SKCTL side effects, no validity
flag, frozen input before prime, startup fit/postconditions and real conversion/
state-safe-point qualifications. Add distinct image/export and independent offline
fixtures; then request independent Mars execution. Preserve earlier exports and
false labels. Core R118 local routing update is not runtime/app acceptance.

## Independent display and DLI acceptance

Mars msg_8f2c /4daa27f5be981b0d1a1b5a923bf40e24e97f3f4a accepts separate
explicit development tuples for display source9d7071f837ec513905b4a2f9718e269c7662b90c
and DLI source258bc0cc764a0614ec8443a89d242a8f1fe8cb5e. Prose contract/receipt
and emitted artifacts reviewed independently, not our GPL implementation/tests.
No local CPU rerun or original-system measurement. Earlier pending-review notes
below are historical; this receipt supersedes their execution-pending status.

Owner Release unity and nonunity Debug ASan(-g -O1) pass startup,288 VBI cases
plus120 services/12 safe points,404 display pattern/CRITIC/callback cases with7
safe points,128 DLI status/stack/register/CRITIC cases with9 safe points. Actual
twelve raw source/MMIO writes, callback ordering, list/color/DMA off/on rendering,
DLI hardware-frame/RTI/mode2 palette and isolated/combined twelve-event cadence
pass. Same/fresh/process replay,20 converter negatives and mutual candidate
state refusal pass; strict schema remains R65 sb52rt-dev2. DLI provider also
passes standard/mixed four-controller hardware matrix and powered live exit.

Startup1197/411, valid-boundary max1204. DMA-off ordinary-refresh default VBI
max187 for display,190 for DLI, excluding hardware entry7; custom-marker max212.
Active blank-list DLI dispatch38, complete callback/RTI86. Deliberately VCOUNT-
delayed custom active-list transfer body144, complete service4785 cycles; this
exceeds512 because of the cart callback and is OUTSIDE the default-handler
contract. No general active-DMA/RDY/WSYNC/nesting/callback deadline claim.

Prior startup/VBI/default-OFF/a26/process/lifetime and43-image firmware tree/
history/three-build checks pass per owner. Startup711 remains default; all build
gates OFF and module capability/approval/execution flags remain FALSE by design.
No observer/chip execution/state-schema change. Pending pooled release with
R65/R66; do not adopt Mars main or enable app before an approved MR announcement.
Full R62 ongoing input/timer/reset/reference/product acceptance remains open.

Next author analog service only after its original policy review: explicit
priming and complete-eight-axis copy/restart, docs/analog-shadow-brief.md. Mars
prose now confirms unpowered standard/disconnected target228, approximate Trak-
Ball unpowered target114; these emulator semantics are not board measurements.


Mars msg_2864 clarifies analog acquisition: ALLPOT00 at cold reset is NOT proof
of any conversion; explicit prime after SKCTL/analog power setup is required.
New docs/analog-shadow-brief.md proposes original cold priming + complete-eight-
axis copy/restart after CRITIC and before display, preserving pending conversion
and zero startup shadows, no extra RAM. Proposal only, not implementation or
hardware/BIOS evidence. Startup estimate127/128 leaves1 byte: further growth
requires explicit fit/refactoring review. Next obtain Mars policy review before
authoring; existing display/DLI execution gates and candidate pins unchanged.

Current RUNTIME-004 continuation: authored a separately labeled
DLI-dispatch candidate atop the pending display candidate, without claiming its
acceptance. docs/dli-dispatch-brief.md defines current-latch exact40/80 routing,
cartridge-owned RTI callback0206, unchanged VBI service and no extra RAM. Preserve
all earlier source exports and false labels. New1318-byte usage leaves730 free;
80 offline tests/CTest pass. Full export source258bc0cc764a0614ec8443a89d242a8f1fe8cb5e
passes real CLI/parent consumer and all3older pinned exports reproduce. Mars req_6f74/msg_d7c0 receives
scope for independent review; both display and DLI need separate real execution
acceptance before app enablement. Next specify four-controller input scan.

Current RUNTIME-004 batch: display-shadow-v1 implemented as a separate candidate.
See docs/display-shadow-brief.md and docs/display-shadow-proof.md: twelve ordered
transfers after clock/CRITIC and before deferred callback;1307 written/741 free,
zero extra RAM, margin250 intact.73 offline tests and CTest pass; no CPU execution.
Committed export pin9d7071f837ec513905b4a2f9718e269c7662b90c passes real
CLI/parent target properties/dependency/hash/byte-equality checks; both previous
pinned exports reproduce. Next obtain Mars scope/tuple review and independent real bus/render/callback/
state-process acceptance. Existing711a2e9/ba90c85 exports stay unchanged. After
this bounded acceptance, specify four-controller analog/keypad/fire scanning and
DLI/IRQ services with separate contracts before authoring; no game claim yet.

Mars msg_aa05 /7c290c4 approves bounded `cold-start-digits-v1` authoring with
corrections, incorporated in startup-brief.md revision2. First authored module,
original glyphs and actual allocation are now implemented;57 offline tests pass.
Image2048, written1177 (147code+1024assets+6vectors),871 unwritten, margin250
untouched. This proves bounded fit only, not future-service fit or execution.

Mars c50e58a /msg_1678 accepts the first artifact/fit receipt and requests the
candidate export boundary now implemented in docs/candidate-export.md:
sb5200-runtime-image with absolute image/manifest/map properties and full source
revision, all artifacts produced before dependent Mars conversion. No generated
GPL implementation header; execution/provider false flags retained.

Independent bounded execution is now reported by the integration owner:
[receipt](docs/independent-execution.md). Normal1166 full CPU cycles/403
instructions, worst valid1175/406 including refresh/RDY; startup writes/entry/RAM,
negative cases, actual glyph DMA/render, strict synchronized states and process
replay/lifecycle pass per owner. No local rerun or original-system observation.
Candidate export pin711a2e986f7906f45aebd310e6330fd7ffc338bf and false flags remain
unchanged; the adapter requires those labels.

Mars msg_1e39 /3c6a4ce approves vbi-clock-v1 bounded authoring with corrections
incorporated in docs/vbi-clock-brief.md revision2. Separate authored module now
fits1244/2048 bytes with804 remaining, margin250 untouched.66 offline tests pass;
see docs/vbi-clock-proof.md. Startup handoff movesFC6F; new exact tuple/observer
and independent execution are now accepted as development evidence below. Original711a2e9 inputs
and false flags remain unchanged; separate opt-in export avoids silent adoption.

Integration-owner receipt msg_9ae4 independently accepts the exact VBI candidate:
startup1197 normal/1204 boundary full cycles; default VBI max95 including RTI,
hardware entry7 separately.288 two-VBI combinations plus120 default VBIs,
interrupt/state-safe-point/process-replay/lifecycle and Release/nonunity ASan
checks pass per owner. See docs/independent-execution.md. No local rerun;
provider change is committed but pending separately authorized release.

Display-shadow contract and authored candidate now supplied above; next obtain
independent integration acceptance; separate DLI candidate authoring above does
not promote the pending display candidate to accepted. Do not assume that clock/vector acceptance
already supplies display/input/DLI/IRQ. Preserve both accepted candidate pins,
false export flags and image-bound state identities. No retail VBI policy or
product enablement; release and full consumer acceptance remain separate.

1. **RUNTIME-002: approved startup and service evidence.** Build a per-service
   numeric ABI/evidence matrix from screened primary behavioral documentation
   and lawful original-system observations. Start with cartridge metadata/entry,
   cold reset, RAM/stack ownership and required initial vectors/registers.
   Preserve unknowns; do not implement a guessed jump-to-cart or software defaults.
   Primary PAM documentation now supplies cartridge-area/entry and RAM reservation
   rows with revision history. Next obtain exact software vector/shadow declarations,
   metadata encoding and entry/reset postconditions. Integration review accepts
   dated documentary facts; reconcile October/January VBI rules before selecting
   final/retail behavior. March's back-reference does not settle that policy.
   Selected NMOS capture semantics are now sourced independently. Public cc65
   declarations supply candidate vector/shadow offsets with a separate
   consumer-interface-unmeasured label, accepted for limited development scope; these
   do not establish Atari reset defaults or resolve final/retail VBI policy.
2. **RUNTIME-003: approve and pilot the original probe protocol.** The 26-byte
   capture fragment, scalar record contract and offline validator are implemented
   with 35 passing tests. Next review result ownership, metadata/mapper layout,
   interrupt window, readout, correction rules and named observer/reviewer roles.
   Identify actual reference access; none is available yet. The primary service
   manual distinguishes original/universal four-port boards; record exact board
   and firmware identities separately. No ROM/font/whole
   RAM or stack dumps, instruction traces or captured boot artwork.
3. **RUNTIME-004: real allocation and first supported startup.** Review original
   asset encoding/placement, code/vector/free margin and every RAM/stack use
   against the approved ABI. docs/allocation-plan.md/json now proposes a full
   2 KiB budget: 1024 asset + 768 code + 250 margin + 6 vectors; zero additional
   persistent RAM, a separately unproven stack allowance. Planning review accepted;
   corrected authoring scope is accepted and the first bounded image fits.
   docs/startup-proof.md reports actual usage, static control flow/stack/base
   cycles and independent fixture expectations. Owner now reports bounded refresh/RDY and provider/reset/status/state
   acceptance in docs/independent-execution.md; future services need new checks. Stop on overflow
   for scope/architecture review before any later service expansion.
4. Add the supported runtime service classes: NMI/VBI/DLI, IRQ/BRK dispatch,
   clocks/timers, display shadows, analog/keypad/fire scanning and character data.
   Each needs evidence, independently expected fixtures and explicit unsupported
   cases; all services/assets must fit together at acceptance.
5. Deliver reproducible image/map/manifest and generated read-only C++ provider
   through sb5200-runtime-image. Coordinate explicit provider selection, read/peek/
   DMA, reset reporting and strictly identity-bound synchronized saves with Mars.
6. Full service and authorized-cartridge validation, deterministic replay and
   lifecycle checks, followed by complete-app performance and device energy.
   Resolve discrepancies through completion; publish only supported claims.

## Landed

- Candidate artifact target sb5200-runtime-image and deterministic schema1/ABI1
  manifest/map/full-pin identity, with byte-exact pinned-input verification and
  seven new tests (57 total). No runtime image-byte change or execution gate loop.

- Mars authoring approval7c290c4 and corrections: Linear32K explicit load,
  structured cold-only outcomes, physical input versus semantic reset, refresh
  steals, CPU-pending NMI and normal chip pipelines retained. No provider approval.
- RUNTIME-004 first authored image:94 startup +9 fault +44 helper bytes,1024
  original glyph bytes and6 vectors. All budget ranges enforced, future-service
  allowances/margin untouched. Seven new independent exact-byte/pixel/fit/opcode/
  reproducibility tests bring total to50. Static reasoning is not CPU execution.

- RUNTIME-004 proposal1 defines concrete original startup policy and diagnostic
  acceptance without relabeling unknown retail behavior. No startup implementation
  at that stage. Authoring approval7c290c4 and the first emitted image above
  supersede that pending scope review. Public declarations retain their
  consumer-interface-unmeasured label.
- Original digit metadata encoder and full unapproved diagnostic cartridge
  candidate: twenty title digits +two year digits, little-endian mapped entry,
  32 KiB layout with the original capture fragment and zero-fill holes. Eight
  tests cover independent bytes/layout, strict ASCII/types, bounds/overlap,
  fresh-process reproducibility and fail-before-output CLI. Total43 pass.

- Mars 1f411e5 accepts the public-interface boundary and digit-only convention
  for proposed sb52-dev-cc65-v1, plus the complete estimated allocation. No extra
  historical provenance needed merely to target the declarations. Services,
  defaults, actual fit/stack, complete cart and execution remain separate gates.

- RUNTIME-002 consumer-interface packet: pinned permissive cc65 declarations and
  documentation, exact vector/shadow candidates and exposure/hash ledger. Keeps
  consumer expectations separate from original Atari or measured facts; identifies
  cc65 conio storage and the 021C–021F reservation discrepancy. Metadata digit
  conventions are documentary candidates, not an approved bypass or full encoder.
- RUNTIME-004 allocation proposal: complete ROM ranges and future-service
  allowances, RAM ownership, original asset plan, margin/overflow stop rule and
  first implementation gates. No measured fit or stack-depth claim.

- RUNTIME-003 tooling: original 26-byte A/X/Y/status/SP capture fragment,
  deterministic source/encoder/fragment descriptor, draft role/operator protocol
  and strict bounded scalar-record validator. Rejects malformed/dump-shaped data
  and stale probe identities; preserves synthetic labels and inconclusive results.
  Thirty-five offline tests and CMake/CTest pass. Four factual opcode entries
  added after selected manufacturer CPU semantics review. No complete cartridge,
  metadata encoder, original execution or service implementation is implied.

- RUNTIME-002 integration review: dated documentary rows accepted; separate
  October partial, January VBI revision and March final-memo evidence profiles.
  Final/retail VBI policy remains null. Metadata uses CPU mapping, software saves
  retain the hardware interrupt frame, and boot prose does not authorize an MMIO
  sweep. ENTRY-01 still requires protocol review before execution.

- RUNTIME-002 documentary research: located and screened original Atari PAM
  memoranda. startup-evidence.md/json records factual rows, provenance/hash,
  October/January/March revisions, unresolved cells and an original ENTRY-01
  measurement plan. No BIOS source/assets, firmware execution or numeric guesses.
  Per-symbol vectors/shadows, metadata encoding and entry/reset defaults remain
  open; the research slice is not a completed runtime ABI.

- RUNTIME-001: original bounded emitter, explicit instruction/address-mode
  subset, symbolic absolute/relative fixups, mandatory CPU vectors, allocation
  and executable-label validation. Offline CMake/CTest and fresh-process
  reproducibility checks; no emulator, external assembler or downloaded code.
- Layout fixture emits four original instruction bytes and six vector bytes,
  with 2038 bytes unused in a 2048-byte image. This proves the tool's small
  fixture fits only; runtime services/fonts and their fit remain unimplemented.
- README/LICENSE public bootstrap. GPL-3.0-or-later, copyright StackBlender LLC.
  No community contribution is needed. Original source and evidence work remain ours.

## Decisions and limitations

- Original 6502 execution in F800–FFFF; no host HLE, direct-PC bypass, hidden
  RAM allocation or invented bank hardware. Initial NTSC four-port target is
  a development profile, not measured board compatibility.
- Current maintainer acts from Apollo Retro with an Odin repo lease. No separate
  runtime owner/queue is registered. Mars owns its emulator integration.
- Primary documentary facts and bounded original startup/font/VBI services now
  have integration-owner execution evidence. No original-system measurements,
  full runtime, usable game provider or game compatibility yet.
- Default external-BIOS behavior in consumers remains untouched. There is no
  replacement state/release or cross-version compatibility claim.
