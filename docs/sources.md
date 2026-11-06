# Source and exposure ledger

This ledger separates tool facts, integration assumptions, software evidence and
unknown behavior. Original source is authored here by StackBlender, without
reading other assembler, emulator, BIOS or replacement-kernel implementations.
GPL licensing this project does not turn copied implementation into original work.

## Sources used

| ID | Source / revision | Exact role | Confidence / limits |
| --- | --- | --- | --- |
| CPU-01 | Western Design Center W65C02S datasheet, April 8 2022, section 4, table 3-1 (page 12) and table 5-2 (page 22), [official PDF](https://www.westerndesigncenter.com/wdc/documentation/w65c02s.pdf), reviewed 2026-11-05 | Published common instruction/address encoding and CPU-vector locations for the tool fixture; no CMOS additions emitted | Documentary CPU encoding, not NMOS timing or Atari software behavior. Validate expanded NMOS semantics with a dedicated processor source before runtime execution claims. |
| CPU-02 | MOS Technology MCS6500 Programming Manual, January 1976 second edition (6500-50A), sections 7.2/7.3 (printed 97, PDF 111), 8.5/8.6 (117/118, PDF 132/133), 8.9/8.11 (122, PDF 137); [primary scan mirror](https://ftpmirror.your.org/pub/misc/bitsavers/pdf/mosTechnology/6500-50A_MCS6500pgmManJan76.pdf), SHA-256 `a7b2ffce0ed8c876f36b78a9cabae951dc6183224d2d44d82de510ed313b6a1a` | Selected NMOS store, stack and transfer semantics for original ENTRY-01 capture plan; original instruction composition, not manual examples | Visually reviewed primary pages; no Atari reset constants or measured execution. Synertek August 1976 [transcription](https://syncopate.us/books/Synertek6502ProgrammingManual.html), sections 7.2/7.3, 8.9/8.11 and appendix B-20/21/26/29, also consulted for the four added encodings; do not rely on its unrelated TXS table typo. |
| INT-01 | StackBlender Mars owner integration proposal, reviewed 2026-11-04 | Original program in F800–FFFF, 2 KiB limit, explicit provider and strict identity-bound saves | Integration proposal, not firmware behavior or an original-system measurement. No Mars source copied into this repo. |
| PAM-01/02/03 | Atari / Rob Zdybel, PAM Package: October 30 1981 partial description (PDF 3–5), January 18 1982 revision (17), March 18 1982 final (24); [primary scans](https://atarimuseum.ctrl-alt-rees.com/ahs_archives/archives/pdf/videogames/5200/pam_package.pdf), reviewed 2026-11-05 | Documentary cartridge-area, reservation and interrupt/VBI contracts; chronology matters | Documentary and retail-unmeasured, not a firmware listing; exact rows/gaps in [startup-evidence.md](startup-evidence.md), numeric records in [startup-evidence.json](startup-evidence.json). |
| CONSUMER-01 | cc65 public declarative headers and platform document, revision `77b6484615427746e55fda2755c9cbc320a1fb51`; [review packet](consumer-interface.md) has exact paths, hashes, license and exposure | Candidate consumer-facing vector/shadow layout and digit-metadata convention, no implementation copied | Consumer-interface-unmeasured; not original Atari provenance, runtime implementation approval or retail behavior. Review separately before adopting scope. |
| HW-01 | Atari CX5200 Field Service Manual, selected PDF 9/12/16 (printed 1-1/1-4/1-8); [source and hash](hardware-profile.md) | Board identification for future scalar records, not reset values or hardware procedure | Primary documentary identity only; original/universal four-port boards must remain distinct. No original execution or diagnostic firmware read. |
| OWN-01 | StackBlender's author-selected fixture | Tool layout, loop/return fixture, FF padding, JSON format | Proposed tool-test policy, not Atari software behavior. |
| METH-01 | StackBlender SNES DSP1 README and docs/checking.md | Prior independently authored project's black-box questions/answers and replay methodology | Method descriptions only; no implementation, tests or generated images copied. |

CPU opcode metadata is a small factual encoding subset transcribed from the
manufacturer reference. No manual text, diagrams or example program was copied.
The emitted fixture and test expectations are original compositions.

## Exposure and quarantined leads

The acting maintainer previously read Claus Buchholz's public Atari 5200 porting
article (ANALOG #15/#16). Its author reports using ROM disassembly. It is
quarantined, supplies no numeric software ABI values to this implementation and
is not independent black-box evidence. Preserve this exposure record rather
than claiming nobody has encountered disassembly-derived descriptions.

Other leads located: Atari's CX5200 field service manual and Avery Lee's official
hardware-reference index/manual. Selected runtime-relevant sections have not
been approved. No third-party emulator/kernel/test archive, original firmware,
font bitmap or firmware disassembly was read/imported to implement these tools.
The prior official Altirra landing-page review was a documentation/license lead,
not a source-code or behavioral oracle.

## Required per-service evidence rows

| Area | Numeric software ABI approved? | Independent original-system observations? | Next evidence |
| --- | --- | --- | --- |
| Cartridge metadata/entry/init | Documentary area and entry pointer only | None | Encoding/flags and entry CPU postconditions still require evidence |
| Cold/warm/key reset and RAM/stack | Documentary reservations only | None | Initial SP/register defaults and reset distinctions need evidence |
| NMI/VBI/DLI and software vectors | Documentary conventions; numeric symbols missing | None | Exact per-symbol vector/shadow addresses and return-stack observations |
| IRQ/BRK and clocks/timers | No | None | Source priority, register preservation, pending events and wrap cases |
| Display shadows | No | None | Address/direction/cadence and exclusion rules |
| Analog/keypad/fire/ports | No | None | Scan cadence, code semantics, endpoints, repeat and port isolation |
| Character data/ROM access | No | None | Encoding/placement semantics, independently authored glyphs |

Record exact source sections/probe IDs, revision, author/exposure, permissions,
expected postconditions and uncertainty before promoting a row to documented or
measured. No operator or lawful execution oracle is established. Original probes
may log whitelisted scalar cart-owned results, not BIOS/font/whole RAM/stack
contents or instruction traces. Gate video capture on original probe artwork.
Another replacement's output is a cross-check, not original-system ground truth.

## RUNTIME-002 screening receipt

Read the PAM package cover and prose on PDF pages 2–8 and 17–25. A low-resolution
page index was used to screen remaining pages. Pages 9–16 (flowchart/controller
examples, including program snippets) were not read at implementation resolution
or transcribed. No manufacturer implementation/font/source file was retrieved.
The memo's references to source listings were not followed. This packet is
primary developer documentation, independently sourced from the quarantined
Buchholz article; do not backfill missing constants from that article.

The March final memo changes zero-page reservation from the October interim
range. The January revision changes the VBI critical-section rule. Preserve both
source dates; March's back-reference does not reconcile the competing VBI rules.
Keep final/retail policy unresolved pending primary or approved observational
evidence. The final memo is documentary evidence, not proof of every shipped
board/firmware revision. The trackball memo's printed year is 1981 amid 1982
material; it is not used for startup constants. No original-system observation
or actor-role separation is claimed. Reference PDFs/screenshots stay outside Git.

## RUNTIME-003 research receipt

The separate Atari 5200 memo packet,
https://atarimuseum.ctrl-alt-rees.com/ahs_archives/archives/pdf/videogames/5200/5200_memos.pdf,
was screened as a low-resolution 15-page layout index. It appears to concern
product/market planning, not the missing software-interface declarations. No
constants were adopted or implementation pages read from it. Broad search also
returned a mirror of the quarantined porting article; search snippets were seen
but not used for ABI values. Primary ABI gaps remain explicit.

The CPU manual scan was temporarily rendered at selected pages only; adjacent
manufacturer CPU examples visible there were not copied into the probe. The
probe sequence, six-slot layout, A5 marker and CF status mask are original
diagnostic policy. No original-system execution, hardware ownership approval,
Atari firmware or external implementation was used for its tests.

## RUNTIME-004 proposal1 source and exposure receipt

CONSUMER-02 extends CONSUMER-01 only to public chip register declarations at the
same cc65 revision `77b6484615427746e55fda2755c9cbc320a1fb51`. Each carries the
same permissive notice; no third-party source is vendored or transplanted:

- [include/_antic.h](https://github.com/cc65/cc65/blob/77b6484615427746e55fda2755c9cbc320a1fb51/include/_antic.h),
  SHA256 `318208d0edfe3c65471170067e1ff7360db738cddeac2be9cf6f53febb95fd95`.
- [include/_pokey.h](https://github.com/cc65/cc65/blob/77b6484615427746e55fda2755c9cbc320a1fb51/include/_pokey.h),
  SHA256 `0184ffb009fa3619b68a39495c03605d671e5e40e10c5d7c8470b5337e29eb93`.
- [include/_gtia.h](https://github.com/cc65/cc65/blob/77b6484615427746e55fda2755c9cbc320a1fb51/include/_gtia.h),
  SHA256 `6c44bbfa9180260209b04fe459a7869103785468612b968e2bfb5338531b62cd`.

Complete header text was retrieved, including explanatory comments and small
register/display-list/color/key macros. Exposure includes the ANTIC header's
attributed Wikipedia introduction. Only factual public register offsets, read/
write aliases and bit declarations inform the proposal; comments naming generic
initial defaults do not establish Atari 5200 firmware defaults. Our choices and
their intended chip effects are proposed-policy / consumer-interface-unmeasured,
subject to Mars review. No startup/kernel/driver/emulator implementation or
foreign tests were read. The atari5200.h top-level header was reread; its hash
still matches CONSUMER-01. Metadata digit convention remains the previously
accepted original subset, not a copied encoder or alphabetic ABI.

A fresh broad hardware-document search again surfaced quarantined porting-article
snippets/mirrors and secondary technical descriptions. These were not opened or
used as software facts. Search also located an Atari home-computer technical
reference scan, not read or used for this proposal. Failed web raw-header fetches
were followed by direct read-only retrieval of the pinned declarations above.
No new original-system observation exists; observer/implementer role gates remain.

OWN-02: startup-brief.md proposal1, byte-layout/metadata code and independent
expected cartridge constants are authored here. Zero-fill candidate, title digits,
year26, entry8000/result3000, register/default/stop policy and seven-segment pixel
coordinates are our design, not measurements. No font bitmap was consulted.
The per-service evidence table above remains historical-gap tracking; accepted
scoped declarations and proposed startup policy do not fill retail/measured cells.

## First bounded module source receipt

Mars approval msg_aa05 /7c290c4 supplies integration-specific qualifications in
startup-brief.md revision2, not retail observations. The original startup program,
seven-segment glyph coordinate composition and independent expected bytes are
authored here. No new foreign implementation or firmware was read.

CPU-02 extension: selected Synertek1976 manufacturer-manual transcription,
chapter3.6.1 CLV, chapter6.1/6.2 indexed addressing, chapter8.8 TXS, appendixB
CLC/CLV/CMP/CPX/JMP/JSR/LDA/RTS/STA entries and appendixC timing table were
consulted for the eight added encodings and static CPU-cycle argument. Other
nearby manufacturer examples were visible, not copied. Preserve known transcription
defects (TXS encoding/flags row, CLV operation summary, shifted CPX summary row);
use the explicit instruction section/encoding table and prior primary CPU scan,
not a mistaken summary. This is NMOS CPU evidence, not chip-stall timing.
The added CLC18/CLVB8/CMPimmC9/CPXimmE0/STAzpX95/STAabsX9D/LDAabsXBD/JMPind6C
are factual encodings, independently asserted in tests. No new opcode timing
engine or third-party test corpus was imported. Refresh/RDY acceptance is owned
by Mars; the1091-cycle worst valid base path excludes stalls explicitly.

## Candidate export receipt

Mars msg_1678 /c50e58a independently verified prior image/diagnostic hashes and
fit receipt without reading GPL implementation or executing CPU code. Requested
artifact target/properties are an integration contract, not firmware evidence.
Original tools/export_candidate.py packages our unchanged image/map with pinned
source identity and false approval flags. No external code, C++ header, service,
new firmware input or new reference result is introduced.


## VBI clock proposal source receipt

CONSUMER-02 public _antic.h at the same pinned revision was reread for NMIEN/
NMIST/NMIRES declarations only; SHA256 remains318208d0edfe3c65471170067e1ff7360db738cddeac2be9cf6f53febb95fd95.
Declarations provide DLI80/VBI40/Reset20 masks and shared read/write status/reset
alias, including a comment that NMIRES clears all sources together. No producer
implementation was read. docs/vbi-clock-brief.md uses these factual declarations
and the existing PAM/consumer packet, with all new policy explicitly original.
No new Atari firmware/reference result or retail VBI reconciliation. Network web
fetch failed, then a direct pinned read/hash verification succeeded; no file cached.


## Approved VBI authoring receipt

Mars msg_1e39 /3c6a4ce approves original development scope with status-latch,
startup-interrupt observer, real RMW bus writes and synchronized-safe-point
qualifications. Integration prose only; no emulator implementation or foreign
tests read. CPU-02 manufacturer transcription consulted for AND immediate,
INC zero-page, TAX/TAY/TXA/TYA encodings/timing, sections7.11..7.14,10.6/10.7,
appendixB entries and RTI timing. Nearby manufacturer examples were visible,
not copied. Six factual encodings live only in the new service emitter subclass.
Original runtime callbacks/clock/layout/tests are authored here. Old-value RMW
write expectations are explicitly confirmed by the integration owner. No new
original-system measurement or firmware access.


## Original display-shadow service exposure

CONSUMER-01/02 addresses reused for display-shadow-v1. Reread the two pinned
public ANTIC/GTIA declarative headers, verified SHA256 values above unchanged.
Web raw retrieval failed; direct read-only retrieval succeeded. Exposure remains
header declarations/comments/macros only, no producer implementation or tests.
Original transfer order, CRITIC policy, byte-preserving behavior and independent
fixtures are authored here; not historical facts. No new opcode facts, Atari
firmware, original-system observations, extracted artwork or reference traces.


## Original DLI dispatch service exposure

No new external source was consulted. Reuse CONSUMER-01 vector0206 and existing
CONSUMER-02 NMIST/NMIRES masks/aliases, CPU-02 factual opcode/timing subset.
Current-latch dispatch, callback-own-register RTI ABI, exact-source failure and
budget/fixtures are original development policy. No Atari firmware/kernel/source/
trace, foreign implementation/test or manufacturer program access. Display/DLI
execution are pending independent integration; no original-system measurements.


## Analog scan integration clarification

Mars msg_2864 (prose only) supplies access-specific POT/ALLPOT/POTGO/SKCTL and
CONSOL acquisition semantics for original analog-shadow-brief.md. No producer
implementation/test read. Cold ALLPOT00 requires explicit prime; selected original
policy remains proposed, not Atari hardware/reference behavior. Timing observations
of this emulator are not promoted to measured original-board facts. No new
external source exposure, firmware image or instruction trace.


## Approved analog authoring qualification

Mars msg_092a /83a8a400 reviews original proposal with explicit SKCTL keyboard/
prescaler/polynomial side effects, no first-sample flag, frozen input before prime,
Trak-Ball cached startup behavior, pending/CRITIC ordering and fit/state tests.
Only prose review read; no implementation/test exposure. Existing factual opcode
subset reused without additions. New original runtime bytes/fixtures/manifest
are authored here; no firmware/reference or historical scan behavior claimed.


## Keypad contract diagnostic boundary

Read only Mars docs/a52-keyboard-contract-review.md at assessment19b9eb69,
not its chip implementation or tests. This independently authored CPU/Node
behavioral assessment reproduces contact-stabilization/held-event faults under
03/06. It supplies no permitted primary hardware debounce timing or historical
BIOS behavior; formal req_72f0 owns that evidence/correction review. No firmware,
foreign kernel/emulator/test or instruction-trace exposure; analog03 unchanged.


## Original IRQ/BRK dispatch evidence

CPU-02 Synertek1976 manufacturer transcription chapter9, selected IRQ stack and
section9.7 BRK prose, supplies stacked B-bit0/1 and BRK returnPC+2. Nearby example
visible but not copied; our original wrap-index/save/dispatch design and scope
message preceded retrieval. No new encodings or global opcode changes. Callback
slots0200/020E come from CONSUMER-01 declarations; our ABI/policy is original, not
Atari firmware behavior. No manufacturer example, Atari BIOS/disassembly/kernel,
foreign emulator implementation/test or instruction trace imported/read here.


## R70 keypad interpretation correction

Mars msg_8edd source-screen prose (local docs/a52-keyboard-source-review.md,
push repair pending) reports Atari POKEY CHIP Rev3 sheet10 scan/compare and
forced-compare behavior. It supersedes our earlier06 defect interpretation;
diagnostic observations remain. Runtime author read only that prose, not the
primary PDF, chip code/tests, foreign emulator sources or quarantined article.
Primary5200 wiring remains unverified; selected evidence path recorded in roadmap.
No chip correction/functional policy/firmware event service approved by this note.


## Timer dispatch and startup helper

Pinned CONSUMER-02 _pokey.h reread for access-specific aliases and timer IRQ
bits01/02/04; SHA0184ffb009fa3619b68a39495c03605d671e5e40e10c5d7c8470b5337e29eb93
reverified unchanged. CPU-02 selected appendixB EOR immediate49/2cycles and AND
zero-page25/3cycles factual entries reviewed. No example code copied. New local
opcodes preserve old emitters/global table. Priority/ack/callback/mask coherence,
source fault policy and compact startup helper are original authored choices
awaiting Mars hardware-interface/execution review; no Atari firmware/historical
implementation, extracted assets, foreign emulator/kernel/test or trace read.


## Revised keypad evidence completed and dispatch authoring review

Read only Mars prose a52-keyboard-source-review.md at f3b991a: owner's visual
primary four-port FSM wiring review supports existing scan alias behavior, no
chip correction.120CPU/7680phase checks are owner emulator evidence, no physical
reference. req_72f0 accepted revised evidence scope; event policy module-owned.
Read only a52-irq-brk-review.md and a52-timer-dispatch-review.md at f3b991a/
d7be9b4; accepted bounded arithmetic/ABI/authoring qualifications, no execution.
Primary POKEY sheet23 source semantics attributed to owner, not newly read here.
No primary source scan, producer/test/firmware implementation exposure introduced.


## Original keypad/fire planning model

Read only existing Mars a52-keyboard-{source,contract}-review.md prose (R70/R62),
not producer chip code/tests or primary scans. Original two-interval schedule,
window event reducer, tentative storage/profile/budget/callbacks are proposed
software policy; model observations are synthetic inputs, not measured captures.
No new external source, reference/firmware trace, extracted asset or foreign
emulator/kernel implementation exposure. Acquisition/atomicity/top-fire remain
explicit review questions before authoring a separately identified image.


## Keypad/fire authoring review revision2

Read only Mars docs/a52-keypad-fire-review.md at9654ecb (msg_0c5f), no chip
implementation/tests/primary scan/firmware. Current-interface top-fire latency,
GTIA write-only latch/cache, contact1..15 and shared-clock facts are owner prose;
not original-board measurements. Mandatory transaction/stack/window/latency
corrections incorporated in original proposal2/model. No new foreign code/source.


## Keypad IRQ latch foundation exposure

Reuses existing permitted Mars keypad/fire review prose9654ecb, declared CPU-02
encodings and original image policies. CPU-02 Synertek1976 appendixB-18 LSR
accumulator selected factual entry (https://syncopate.us/books/Synertek6502ProgrammingManual.html)
reviewed for4A, one byte/two cycles and zero-fill right shift. Adjacent factual
table rows visible; no example/firmware program or foreign emulator/test copied.
New RAM/profile/interrupt composition is original. No Atari firmware/trace,
extracted assets, primary board scan or new reference measurement exposure.


## Independent keypad IRQ execution receipt

Read only owner prose a52-keypad-irq-development.md at003e782/msg_4f5f.
This supplies attributed independent CPU/chip/state/converter results, including
explicitly synthetic raw-code0/NMI frontier qualifications; not original-board
measurements. No producer implementation/test, firmware, reference trace or new
external source was read. Original candidate/generation inputs remain unchanged.


## Automatic keypad window authoring

No producer implementation/test, firmware/reference trace or board scan read.
Original service composes reviewed acquisition policy9654ecb atop accepted IRQ
foundation003e782. CPU-02 manufacturer transcription appendixB selected factual
CMPabsX DD/LDXabs AE entries and already visible ORAimm09 row reviewed at
https://syncopate.us/books/Synertek6502ProgrammingManual.html; no example copied.
Local opcode table only; global/old emitters untouched. New callbacks, window
state, activation and compact analog loop are original software choices requiring
independent native execution, not measured historical firmware behavior.


## Both-fire fragment and allocation proposal

Original routines reuse permitted review9654ecb SKSTAT/KR2/GTIA/cache/latch facts
and CPU-02 selected opcode facts already visible in manufacturer tables: ORAabs0D,
CMPabsCD,LDYabsAC. No new firmware/trace, producer implementation/tests, board
scan or external source exposure. Fragment originF800 is synthetic; it supplies
no authority to replace font or spend reserved ROM. Proposal remains unapproved.


## Static fire-fragment audit

No new source exposure. Independently authored allowlist uses already recorded
NMOS encodings and permitted interface facts. It decodes bytes for static access
and branch checks only; no instruction execution, chip model or foreign code.
Conditional X0..3 footprint is an explicit precondition, not measured behavior.


## Original cartridge input callback recorder

No new external source exposure. Reuses previously permitted NMOS encodings
(LDXabsAE) and proposed0208/020A Aport/Xold/Ynew RTS ABI. Cartridge RAM layout,
bounded record format and host decoder are original diagnostic policy, not
manufacturer firmware behavior. Cycle worksheet is static nominal arithmetic;
synthetic format records are not observations or measured execution. No foreign
implementation/tests, firmware/trace, assets or physical reference was read.


## Independent automatic-window receipt

Read only Mars docs/a52-keypad-window-development.md at64f2485/msg_b0cb.
Owner-reported actual CPU/chip/state/converter checks are attributed independent
emulator evidence, not physical timing, firmware observations or a local rerun.
No producer implementation/test, firmware/trace, primary scan or foreign source
exposure. All original generation inputs remain unchanged.


## Both-fire cumulative authoring approval

Read only Mars docs/a52-fire-allocation-review.md at2784b289/msg_e667.
Numeric allocation/profile/aged source/event/busy/cache/latch/stack/timing limits
are permitted owner prose, not physical reference or native fit approval. No
producer implementation/tests, firmware/trace, primaryscan or new external source.
New original cumulative emitter uses already recorded NMOS encodings and own
window/fragment policies; old9generations unchanged. Native acceptance separate.


## Independent both-fire receipt

Read only Mars docs/a52-fire-development.md at4e6a3a5/msg_0343. Qualified CPU/
chip/cache/ordinaryframe/safeprocess/NMI/stack/converter results are attributed
owneremulator evidence, not physical/firmware observations or a localrerun.
No producerimplementation/test, firmware/reference trace, primaryscan or foreign
source exposure. No generationinput/falseapprovalflag change.


## Remaining-service inventory and bridge refactor

No new external source exposure. Inventory uses existing own consumer-interface/
startup evidence and permitted Mars4e6a3a5 prose; unresolved requirements remain
unknown. Original callback-argument factoring uses previously reviewed NMOS
LDY/TXA/LDX/JSR/indirect-JMP facts, not foreign routines. Static alternate fragment
and nominal arithmetic are not measured execution or native equivalence. No
firmware/trace, extracted assets, producer implementation/test or new primaryscan.


## Callback bridge cumulative authoring review

Read only Mars docs/a52-fire-refactor-review.md at2ffaa687/msg_b2c1; approved
bounded codefactoring and reset evidence requirements, not a native execution
receipt. Original code reuses own existing encodings/policies. No new external
source, firmware/trace/assets or producerimplementation/tests exposed.
