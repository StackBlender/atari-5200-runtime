# Runtime handoff

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


## Analog priming clarification

Mars msg_2864 clarifies analog acquisition: ALLPOT00 at cold reset is NOT proof
of any conversion; explicit prime after SKCTL/analog power setup is required.
New docs/analog-shadow-brief.md proposes original cold priming + complete-eight-
axis copy/restart after CRITIC and before display, preserving pending conversion
and zero startup shadows, no extra RAM. Proposal only, not implementation or
hardware/BIOS evidence. Startup estimate127/128 leaves1 byte: further growth
requires explicit fit/refactoring review. Next obtain Mars policy review before
authoring; existing display/DLI execution gates and candidate pins unchanged.

## Committed DLI export receipt

Source/export258bc0cc764a0614ec8443a89d242a8f1fe8cb5e pushed; CLI and real
temporary parent CMake target pass four properties, absolute artifacts/dependency
ordering, source/image/map identity/false flags and exact CLI-byte equality.
All three previous pinned candidates reproduce unchanged image hashes; temporary
consumer removed. Ignored artifacts in existing build/dli-candidate. Full packet
sent Mars req_6f74 for independent scope/tuple/CPU/raster/state acceptance; no
local CPU run. Pending display9d7071f acceptance remains distinct. Requested
prose-only POT/ALLPOT/POTGO/SKCTL/power/select clarification for next original
four-controller analog service; no historical scan or extra RAM invented.
No consumer pin/provider flag/release/default change. Lease released after push.

## Current DLI dispatch continuation

Original dli-dispatch-v1 atop pending display-shadow-v1, separate source/export/
target; scope sent Mars req_6f74/msg_d7c0. No display acceptance assumed. See
docs/dli-dispatch-{brief,proof}.md. Image SHA256
374465be3cfce3d15c10c7899f4fedbd8cf854b23ee1734b9302c7049e55e05c,
1318/2048 used,730 free incl250 untouched margin. ClassifierFCC0 accepts40→0202
and80→0206; old rangeFC89 becomesFF, startup/other labels unchanged. No extra
RAM; DLI callback hardware frame only/own register saves/RTI, default0206 faults.
80 offline methods/CTest pass; no actual CPU/raster/state run. Source export
requires committed full pin; real CLI/parent verification follows next receipt.
Exact changed paths: tools/dli_dispatch_image.py, tools/export_dli_candidate.py,
cmake/dli-dispatch-candidate.cmake, tests/test_dli_dispatch_image.py,
docs/dli-dispatch-brief.md and proof, README/ROADMAP/testing/sources/handoff.
Next send full pinned packet, resolve Mars contract review and independent DLI+
display acceptance; then specify four-controller input service. Current consumer
pins/defaults/false labels unchanged. Runtime write lease held until final push.

## Committed display export receipt

Source/export pin9d7071f837ec513905b4a2f9718e269c7662b90c is pushed. Real
CLI and temporary parent CMake consumer passed all four target properties,
absolute artifacts, dependency-before-converter order, source/image/map hashes,
false approvals and CLI-byte equality. Original711a2e9 and ba90c85 pinned
exports reproduce their unchanged hashes. Temporary consumer source/build removed;
final candidate artifacts remain ignored in build/display-candidate. No CPU run.
Full delivery sent to Mars on req_6f74; independent scope/execution reply pending.
Next review owner response, resolve any contract discrepancy, then obtain real
bus/render/state acceptance before following controller/DLI/IRQ service work.

## Display-shadow batch (current)

RUNTIME-004 adds separate tools/display_shadow_image.py, export_display_candidate.py,
cmake/display-shadow-candidate.cmake, tests/test_display_shadow_image.py and
docs/display-shadow-{brief,proof}.md. Scope sent to Mars on req_6f74/msg_65cc;
review/execution pending. Earlier candidate source inputs untouched. Image2048,
SHA1992e64b05d096e479c9532b14a77839bad182428b459a3ca8862ede51acb364,
1307 written/741 free,63 display bytes atFE50; no new RAM/stack/margin.
Direct73 methods plus existing build/CTest pass. Static eligible VBI168..173
cycles/50..51 instructions (includes extra3-cycle routing JMP), full512 target
unmeasured; startup unchanged. Pinned export requires committed source, so
real CLI/parent validation and exact pushed pin follow in a receipt.
Next Mars independently tests the brief before any enablement; then define
four-controller analog/keypad/fire and DLI/IRQ services. No retail/game result.


## Latest independent VBI acceptance

Owner msg_9ae4 accepts the exact ba90c8550c1be1c85b5aa7d6810e1ee6c6031656
candidate in committed development integration, pending separate release.
See docs/independent-execution.md for owner-reported288 combinations/120VBIs,
actual interrupt-selection/pending-NMI failure, RMW/stack/callback/RAM and twelve
safe-point/fresh/process state replay results. Startup1197/1204 full cycles,
default handler95 inclRTI, custom119, hardware entry7 separately. Release unity/
nonunity Debug ASan and baseline/default-OFF/a26/converter/firmware checks pass.
No local CPU run or foreign implementation/test exposure. No observer schema
change; sb52rt-dev1 old/new state refusal passes. False labels and both source
pins unchanged. This supersedes pending-independent-execution notes below.
Next specify display-shadow transfer with reviewed MMIO/cadence/CRITIC/order,
allocation and independent acceptance before authoring. No full service/game/
product or new release authorization; main integration request remains open.


## Current VBI clock authoring slice

Mars msg_1e39 /3c6a4ce approves bounded vbi-clock-v1 with qualifications now
incorporated in docs/vbi-clock-brief.md revision2. tools/vbi_clock_image.py emits
an original separate2048-byte image:1244 written/804 remaining, margin250 intact.
SHA62df6162ac3accdfa19769c8f2dcd450c510e385fa71f98ec7912f61d449fa54.
ClassifierFC89, system_vbiFCA0, exitFCB0, clockFDF0, changed handoffFC6F.
No new CPU engine; six local NMOS encodings preserve baseline emitter/table.
Separate export_vbi_candidate.py and opt-in cmake/vbi-clock-candidate.cmake
verify all pinned inputs before producing image/map/manifest with false flags.
Nine new test methods (66 total) pass; docs/vbi-clock-proof.md owns byte/stack/
base-cycle/fit/static expectations. Startup1115 worst base cycles/414 instructions;
default VBI81..86 base cycles/25..26 instructions, max stack6 including hardware.
These are static results, not CPU/ANTIC execution or a new accepted provider.
Original711a2e9 generation inputs/hash unchanged. Committed source/export pin is ba90c8550c1be1c85b5aa7d6810e1ee6c6031656.
Real CLI/parent CMake consumer properties/artifacts/hash/false labels/ordering and
byte equality pass; original711a2e9 CLI reproduces unchanged image. Existing
build/ CTest passes66 methods; temporary consumer source/build removed.
Delivery packet on req_6f74 uses that source pin, unchanged by this docs receipt.
Mars must extend Starting interrupt/pending-NMI observation and tuple allowlist,
then independently exercise real VBI/callback/clock/RMW writes/stack/state/replay.
Mixed/Reset sources synthetic; state captures actual synchronization safe points.
No retail VBI reconciliation, module release or app enablement approval.

## Current slice and authorization

Apollo Retro maintains this public GPL-3.0-or-later project under explicit owner
authorization to complete it, commit and push; no community contribution dependency.
Acquire repo:atari-5200-runtime lease before writes and release after push.
Mars req_6f74 remains incomplete: do not ack/reopen or poll. Authoring approval
msg_aa05 /7c290c4 accepts cold-start-digits-v1, with chip/reset/observer corrections
now in docs/startup-brief.md revision2. It does not approve provider/execution,
reference runs, pins, release or retail compatibility.

## Independent bounded execution receipt

Integration-owner report now supersedes earlier pending bounded CPU/provider/
state notes below; see docs/independent-execution.md. Normal1166 full cycles/403
instructions, worst valid1175/406 including stalls, write/entry/RAM/negative/glyph
DMA/render/state/replay/lifecycle acceptance pass per owner. No local rerun,
reference measurement or emulator implementation/test exposure. Source pin711a2e9
and all generation flags/capabilities remain unchanged; candidate-label validation
is intentional. Full ongoing services and product/module acceptance remain open.

## Candidate export slice

Mars msg_1678 /c50e58a independently checked generated image/diagnostic hashes,
1177/871 allocation and refreshed encoder identity. No CPU run or GPL source read.
Requested artifact target now implemented: sb5200-runtime-image, properties
SB5200_IMAGE_FILE / SB5200_MANIFEST_FILE / SB5200_MAP_FILE absolute paths and
SB5200_SOURCE_REVISION full commit. tools/export_candidate.py produces schema1/
ABI1 manifest with image/map/source identities, cold-only/Linear32K and fault map;
all57 offline tests pass. Candidate flags remain false; source export must not
require the execution approval it enables. Image bytes unchanged. docs/candidate-
export.md is the exact interface/build/provenance packet. Pinned generation inputs
must be committed before CLI/target emission. Export implementation commit
711a2e986f7906f45aebd310e6330fd7ffc338bf passed the real CMake target and57-test
CTest suite. A temporary parent add_subdirectory harness verified all4 properties,
absolute existing artifacts, manifest/map/image hashes/full revision and consumer
dependency ordering; fresh CLI exports were byte-identical and real prior-pin
export refusal created no output. Temporary harness removed. No CPU acceptance.
Mars owns read-only C++ conversion, not a GPL implementation header import.

## First authored module

- tools/startup_image.py: approved bounded original startup atFC00, ordered14
  MMIO stores, zero0000..0018, fourteenFC86 vectors0200..021B, digit/entry checking
  helperFEB0, explicit A=X=Y=0,P&CF=06,SPFF and CPU JMP(BFFE). Three failure loops
  FC80/FC83/FC86; no ongoing VBI/DLI/IRQ/input/timer/shadow service.
- Original1024-byte font: independently composed digits50..59 atFA80..FACF,
  other glyphs blank. No bitmap reference used.
- tools/emitter.py: eight new factual common-NMOS encodings,37 entries total;
  strict zpx/absx/ind numeric operand widths. No CPU engine or HLE.
- CMake authored_startup target emits ignored generated/startup.bin and map;
  existing ten-byte layout fixture remains separate. Candidate export is separate.
- Actual image SHA b2d8ebb8d0070f2aee1bd79d7adfee85b88797702cb96035ab3a18e9bd37f68d;
 2048 bytes,1177 written:1024font+94startup+9faults+44helper+6vectors.871 unused,
 including all250margin. Future service allowances untouched. Full future fit unknown.
- tests/test_startup_image.py adds seven independent encoding/pixel/fit/reserve/
  opcode-boundary/reproducibility tests. Total50 direct unittest and CMake/CTest
  pass. docs/startup-proof.md records exact expected bytes/boundaries/fixtures,
  static stack and CPU-cycle analysis, not measured CPU behavior.

## Static argument and remaining execution gate

Valid normal paths:1084 base cycles/403 instructions for4000..BEFF entries;
1091/406 forBF00..BFE7. All branches remain within a page; digit reads no page
cross. Ordinary one helper uses two balanced stack bytes. One interrupt after
TXS can add three before first fault; repeatedNMI/pre-TXS unbounded/not supported.
Full4096 deadline INCLUDING refresh/RDY remains unproved. Frame-return-only
observation is insufficient; request Mars instruction-boundary observer and
independent execution, no traps/direct-PC/service shortcuts.

Use explicit Linear32K,32768-byte board/profile load success before power. Future
structured operation maps Node power(false) to cold; true refuses before mutation
with visible runtime status. System::power(true) is not CPU-only reset. Physical
controller-key input is separate from semantic reset. External-BIOS unchanged.
NMIRES does not clear CPU-pending NMI; DMACTL0 still has refresh steals; SKCTL0
resets key/serial/error/clock state; AUDC0 does not reset all timers; PRIOR/CHBASE
pipeline remains normal. These are Mars integration facts, not retail defaults.

## Diagnostic/tooling and evidence already pushed

8cb2c6d: strict20-title+2-year ASCII digit metadata, LE entry, full unapproved32KiB
original diagnostic around26-byte ENTRY-01 capture; eight tests. Candidate uses
entry8000/results3000..3005, title01234567890123456789/year26; image SHA remains
c7ae62b374ccecde52448d39596421924e749cac9175838198f4b427d0fe83f7.
Regenerate descriptors after emitter change: encoder hash changed, cart bytes did
not. The result area is accepted for DMA-off Mars diagnostic only, not original
hardware. Require freshA5 store, expectedA/X/Y00,P&CF06,SPFF. Baseline caller RAM
AFTER core cold randomization; see startup-proof.md negative cases.

Earlier b699dff/ca643f9/62f45c6/7209d6a: original capture/strict scalar validator and
protocol, public cc65 declaration layout/digit convention, full budget and primary
board identities. Source hashes/exposure in docs/sources.md. CONSUMER-02 chip
headers are public declarative source only. No startup/kernel/driver/emulator code
read. Historical final/retail VBI stays null; dated PAM profiles separate. The
Buchholz disassembly-derived article remains quarantined. No original-system
operator/apparatus/role split/reference result; never relabel development policy
measured retail. Generated binaries/reports remain ignored in existing build/.

## Resume

Both baseline and VBI-clock independent execution are accepted as bounded
development evidence. Next specify display-shadow transfer under the existing
allocation and vector/CRITIC conventions, with exact MMIO order and independent
fixtures, then request scope review. Wait for separately authorized integration
release and consumer checks before any app adoption. Preserve false labels,
source pins and state boundaries. Keep roadmap/handoff current and release lease.
