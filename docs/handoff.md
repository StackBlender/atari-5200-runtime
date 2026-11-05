# Runtime handoff

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
