# Runtime handoff

## Next service scope

User2026-11-05: continue5200. Prepared docs/vbi-clock-brief.md revision1 under
RUNTIME-004: named original vbi-clock-v1, actual NMI classifier, immediate/deferred
vector stack contracts, little-endian clock-before-CRITIC, exact persistent-write
boundaries, unchanged ROM ceilings and independent acceptance matrix. No service
implementation approved/emitted yet; current source711a2e9/generation flags stay
unchanged. CONSUMER-02 pinned ANTIC declaration reread/hash verified for aliases/
masks only; no emulator/kernel/tests viewed. Send pushed full source revision to
Mars on req_6f74 for concrete authoring/observer/state boundary review, then
implement after acceptance. Existing bounded MR-42 receipt is development-only.

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

Candidate export and independent bounded execution are reported complete.
Next review docs/vbi-clock-brief.md with Mars on req_6f74, resolve its concrete
open integration decisions, then author the accepted service and verify exact
fit/encoding/stack/static cycles before requesting independent execution. Keep
current711a2e9 export reproducible and unchanged until explicit adapter review.
Do not expand services using assumed retail defaults or reuse old Ready states.
Keep roadmap/handoff current, commit/push passing slices and release the lease.
