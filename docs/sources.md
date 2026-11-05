# Source and exposure ledger

This ledger separates tool facts, integration assumptions, software evidence and
unknown behavior. Original source is authored here by StackBlender, without
reading other assembler, emulator, BIOS or replacement-kernel implementations.
GPL licensing this project does not turn copied implementation into original work.

## Sources used

| ID | Source / revision | Exact role | Confidence / limits |
| --- | --- | --- | --- |
| CPU-01 | Western Design Center W65C02S datasheet, April 8 2022, section 4, table 3-1 (page 12) and table 5-2 (page 22), [official PDF](https://www.westerndesigncenter.com/wdc/documentation/w65c02s.pdf), reviewed 2026-11-05 | Published common instruction/address encoding and CPU-vector locations for the tool fixture; no CMOS additions emitted | Documentary CPU encoding, not NMOS timing or Atari software behavior. Validate expanded NMOS semantics with a dedicated processor source before runtime execution claims. |
| INT-01 | StackBlender Mars owner integration proposal, reviewed 2026-11-04 | Original program in F800–FFFF, 2 KiB limit, explicit provider and strict identity-bound saves | Integration proposal, not firmware behavior or an original-system measurement. No Mars source copied into this repo. |
| PAM-01/02/03 | Atari / Rob Zdybel, PAM Package: October 30 1981 partial description (PDF 3–5), January 18 1982 revision (17), March 18 1982 final (24); [primary scans](https://atarimuseum.ctrl-alt-rees.com/ahs_archives/archives/pdf/videogames/5200/pam_package.pdf), reviewed 2026-11-05 | Documentary cartridge-area, reservation and interrupt/VBI contracts; chronology matters | Documentary and retail-unmeasured, not a firmware listing; exact rows/gaps in [startup-evidence.md](startup-evidence.md), numeric records in [startup-evidence.json](startup-evidence.json). |
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
