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
