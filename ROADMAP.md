# Atari 5200 Runtime roadmap

StackBlender will complete and freely share this original runtime. Initial scope
is NTSC four-port, followed by evidenced differences and broader compatibility.
The first image fixture is a build-tool test, not an implementation milestone
for cartridge startup.

## Next


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
