# Runtime handoff

## Current slice and authorization

Apollo Retro maintains this public GPL-3.0-or-later project under explicit owner
authorization to complete it, commit and push; no community contribution dependency.
Acquire repo:atari-5200-runtime lease before writes and release after push.
Mars req_6f74 remains incomplete: do not ack/reopen or poll. Authoring approval
msg_aa05 /7c290c4 accepts cold-start-digits-v1, with chip/reset/observer corrections
now in docs/startup-brief.md revision2. It does not approve provider/execution,
reference runs, pins, release or retail compatibility.

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
  existing ten-byte layout fixture remains separate. No sb5200-runtime-image.
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

Deliver image/map/fit and prose execution packet to Mars on req_6f74. Independent
chip/CPU execution, stall-inclusive timing, read/peek/DMA/pixel behavior and
provider/reset/status/state acceptance are outstanding owner work. Ask for precise
observer/provider sequencing; no extra historical-default research is needed for
this approved authored scope. Do not expand ongoing services until their numeric
behavior/allocation/independent fixtures are separately reviewed. Keep both repos'
roadmaps/handoffs current, push coherent passing work and release lease.
