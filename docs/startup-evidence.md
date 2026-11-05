# Startup evidence and probe plan

RUNTIME-002, reviewed 2026-11-05 by apollo_retro_owner as documentary observer.
No original-system execution took place. These facts support a documentary
profile; they do not establish measured retail compatibility or approve missing
numeric values by implication. No service implementation is added in this slice.

## Primary source

Atari, Rob Zdybel, *PAM Package*, [archived manufacturer memoranda](https://atarimuseum.ctrl-alt-rees.com/ahs_archives/archives/pdf/videogames/5200/pam_package.pdf).
PDF pages below are one-based, including the cover. The archive catalogue
identifies the package as Atari technical documents. Author/title/date are
visible on the scanned memoranda. The selected pages contain behavioral prose,
not a BIOS source listing. Store factual requirements, not scanned pages, here.

### Documentary facts

| ID | Contract fact | PDF page / revision |
| --- | --- | --- |
| CART-01 | Communication area BFE8–BFFF: name 20 bytes, decade/year one byte each, entry pointer BFFE–BFFF; handoff indirect through that pointer. | 5, October 30 1981 |
| RAM-01 | OS zero-page reservation 0000–0018 inclusive; 0019 upward available. | 24, March 18 1982 final revision |
| RAM-02 | Stack page 0100–01FF; software-vector reservation 0200–021F. | 4, October 30; final memo references this description |
| NMI-01 | Immediate VBI/DLI dispatch saves no A/X/Y; system VBI preserves registers. | 3–4, October 30 |
| IRQ-01 | Immediate IRQ neither saves A/X/Y nor clears its cause. Deferred dispatch saves A; BRK also saves X. | 3, October 30 |
| VBI-01 | Clock advances before CRITIC check; nonzero CRITIC stops remaining system VBI work. Processor I-bit no longer participates. | 17, January 18 1982 revision |
| BOOT-01 | Monitor clears zero-page and hardware; SDMCTL, PRIOR, CHBASE, SKCTL, NMIEN receive unspecified nonzero values. | 4, October 30 |

The October description identifies itself as interim. January revises VBI policy;
March's final memo refers back to the partial description and narrows the
zero-page range. That back-reference does not resolve whether October or January
VBI policy applies to a final/retail revision. Keep the dated evidence separate;
no combined final/retail interrupt policy is selected. No RAM,
register, vector or timing row here has original-system measurements.

## Dated documentary profiles and integration review

These are evidence groupings, not selectable runtime providers:

| Evidence profile | VBI policy scope | Final/retail selection |
| --- | --- | --- |
| pam-1981-10-30-partial | October interim I-bit participation only | Unselected |
| pam-1982-01-18-vbi-revision | VBI-01 applies to this dated revision only | Unselected |
| pam-1982-03-18-final-memo | Smaller ZP reservation documented; VBI reconciliation unresolved | Unselected |

The machine target remains NTSC four-port; that target does not identify a shipped
firmware revision. Further primary evidence or approved original observations
must reconcile the VBI policies before choosing a final/retail behavior.

Integration review on 2026-11-05 accepts the dated documentary rows, with these
qualifications:

- CART-01 addresses are CPU-mapped cartridge addresses. Read metadata through
  the emulated bus; do not infer arbitrary physical-file tail offsets or jump
  the host CPU directly to cartridge entry.
- NMI-01/IRQ-01 describe software saves. The CPU's automatic interrupt frame
  remains required; absence of A/X/Y saves does not remove that frame.
- BOOT-01 is broad prose, not a numeric MMIO initialization sequence. Writable
  effects, order, aliases and unresolved shadow/default values need review.
- ENTRY-01 is suitable for further protocol review, not execution approval.
  Operator, result-area ownership, measurement corrections and role separation
  remain prerequisites. Full asset/allocation/provider evidence remains open.

## Unresolved startup contract

| Gap | What implementation must not assume | Next independent observation/specification |
| --- | --- | --- |
| Cartridge flags/alternate entry | No diagnostic flag address, flag value, PAL policy or init callback inferred from a later article | Primary interface declaration or original flags/entry probe after source review |
| Metadata encoding | The memo names a display encoding but does not fully specify our encoder | Document character/digit semantics; keep author-created probe metadata distinct from copied glyphs |
| Entry registers/flags/SP | No magic accumulator/index/status/stack value or JSR return frame invented | Cart-owned scalar capture at first instruction, with instruction side effects accounted for |
| Public vector addresses | The reserved vector range is not a per-symbol address map | Primary software-interface declarations or an approved observer's scalar specification |
| Shadow addresses | Names in the memo do not determine their byte offsets | Obtain documentary offsets with provenance before writing shadow code |
| Boot register values/order | Nonzero is not a numeric default or permission to choose one | Independent post-handoff MMIO observations; distinguish readable from write-only registers |
| Reset distinctions | Key RESET is not evidence of a physical CPU reset | Specify power, software reset and cartridge/game reset independently |
| Original assets | No bitmap or logo extracted to fill CHBASE dependencies | Author original glyphs after encoding/address evidence; neutral original display only |
| Runtime cost/fit | Ten tool-fixture bytes do not budget all services | Full code/font/vector margin and RAM/stack ownership review |

## First probe: ENTRY-01

Purpose: establish the earliest cartridge-visible boundary, not manufacturer
instruction internals. Write original 32 KiB diagnostic source with its own
communication area and a fixed authored entry, using CART-01 only after metadata
encoding and the selected profile are reviewed. No BIOS included or overridden.
Do not run or claim this probe before a lawful reference operator is established.

The observer must whitelist a small cart-owned result area only after RAM
ownership review. Capture initial A/X/Y before instructions that change them;
account for instructions used to observe status and SP, and for any temporary
pushes. Keep an annotated measurement sequence and derived correction rules.
No complete stack/RAM capture, manufacturer return-address/code bytes, ROM reads,
glyph dumps, instruction trace or copied boot artwork is permitted.

Stimulus cases: cold power, repeated cold power, supported reset operation, held
and released controller inputs. Record board/revision and reset apparatus;
cartridge source/hash and image hash; operator/date; step sequence; repetition
count; exact scalar result and uncertainty. A test log is not a specification
until reviewed for provenance, data exposure and reproducibility.

A/X/Y/P/SP observations must not be guessed from the emitter fixture or another
replacement. No expected numeric baseline exists yet. ENTRY-01 initially records
measurements and rejects malformed records; comparison thresholds come after an
independent pilot, not from our own eventual runtime.

## Roles and implementation handoff

Current role: Retro performs documentary research and owns this repository.
No original-system observer/operator is available and no separate measured-
behavior implementation handoff has occurred. Before reference work, record who
may run probes, what material each role can see, and which reviewed fact packet
reaches the implementer. Do not relabel a single author's assumptions as an
independent measurement or imply the future role split has already happened.

Send the CART/RAM/interrupt documentary rows and their gaps to the integration
owner for review. A future service-capable provider needs the supported ABI,
reset contract, original asset/allocation map and noncircular execution fixtures.
This research document alone does not enable the 5200 or change the core pin.

The original capture fragment and bounded record format are now specified in
[ENTRY-01 protocol](entry-observation-protocol.md). This advances protocol tooling
only; result-area/operator/role/metadata/interrupt-window review still precedes
a complete cartridge and any reference execution.
