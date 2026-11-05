<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Display-shadow development service

Independent bounded execution now accepted by Mars msg_8f2c /4daa27f; see
[independent receipt](independent-execution.md). Pending-execution wording below
is historical; source exports/false flags remain unchanged, no product release.

RUNTIME-004, revision1, 2026-11-05. Original proposed development policy, not
measured Atari BIOS behavior. Integration review/execution pending. Extends
cold-start-digits-v1 + vbi-clock-v1 as a distinct display-shadow-v1 candidate.
Both previously accepted source exports and generation inputs stay unchanged.

## Contract

Retain startup, font, callback stack ABI, NMI classification/acknowledgment,
clock-before-CRITIC order and unsupported-source fault behavior. After clock,
CRITIC nonzero skips BOTH display transfer and deferred callback. CRITIC zero
jumps to display_transfer, which performs these twelve ordered byte transfers:

| Source shadow | Hardware destination | Order |
| --- | --- | --- |
| 0005 SDLST low | D402 DLISTL | 1 |
| 0006 SDLST high | D403 DLISTH | 2 |
| 0008..000B PCOLR0..3 | C012..C015 COLPM0..3 | 3..6 ascending |
| 000C..0010 COLOR0..4 | C016..C01A COLPF0..3/COLBK | 7..11 ascending |
| 0007 SDMCTL | D400 DMACTL | 12, last |

Each source is read immediately before its destination write. All eight bits
pass unchanged to the real hardware write path; chip masks/delay remain chip
behavior. No MMIO reads, shadow writes, pointer dereference, RAM validation,
extra scratch RAM, table, JSR or extra stack use. Then JMP (0204) to deferred
callback. The callback therefore sees completed transfers and may override
registers; its shadow changes take effect at the next eligible VBI. Immediate
callback shadow/CRITIC changes apply to this invocation. Standalone immediate
RTI skips clock/display/deferred. System prologue and exit preserve A/X/Y as
before; live flags remain scratch and hardware P/PC are restored by RTI.

Cold shadows remain zero. Thus first CRITIC-zero service can write a zero
pointer/colors/DMACTL; consumers MUST initialize safe shadows before NMIEN40.
No implicit DMA enable or title display. Cart-owned screen/list/assets must be
valid before requesting DMA. Write low/high before DMACTL, but existing DMA is
not temporarily disabled: this is NOT an atomic active-display update. Normal
ANTIC/GTIA scheduling, pipeline delays, refresh and RDY remain unmodified.
No PMBASE/GRACTL/PRIOR/CHBASE/scroll/collision, input, attract or timer work.

Cart must update vectors/shadows with NMI disabled and no CPU-pending NMI, or
otherwise provide a fixture-specific safe synchronization protocol. No NMI
nesting, arbitrary callbacks, invalid lists or held-RDY completion guarantee.
Hardware IRQ/BRK and unsupported DLI/mixed/reset source behavior unchanged.

## Fit and static limits

Place display_transfer at FE50..FE8E: twelve unrolled LDA zp / STA abs pairs
(60 bytes), JMP indirect0204 (3). Uses63/96 display allowance;33 remain there.
Clock replaces its final deferred indirect JMP with absolute JMP display_transfer
(same3-byte length). Other bytes/labels unchanged. Expected image1307 written,
741 unused,250 reserved margin untouched; zero extra RAM/stack.
Each pair3+4=7 nominal CPU cycles, so add87 to eligible default VBI:168..173
base cycles,50..51 instructions. CRITIC-nonzero unchanged; startup unchanged.
Proposed full default target remains512 incl ordinary refresh but excludes
hardware entry/custom callbacks/held RDY. Active display independently measured,
not covered by the DMA-off timing estimate.

## Independent acceptance

Integration owner independently authors cartridges/expectations, without GPL
implementation/test inspection. Use exported symbols and full image identity.

- Repeat startup, metadata negatives, NMI source/early/pending/hijack, actual
  callbacks/stack/P/PC/clock-carry and default-OFF/old-provider regressions.
- Distinct twelve shadow bytes, zeros/FF, per-field walking bits and changing
  pointer/colors/DMA: exactly twelve ordered real writes per eligible VBI,
  after clock before deferred marker. CRITIC01/80/FF: no display writes/deferred,
  clock advances; immediate callback/standalone RTI follow the contract above.
- Observe no forbidden reads or persistent writes, conio/padding/other shadows
  unchanged. DMA register read aliases are not an oracle for write values;
  instrument real bus writes plus settled chip/render observations.
- Safe original mode2 list/screen using existing original digits: change pointer
  A/B, palette A/B and DMA off/on via shadows only, verify actual ANTIC fetch and
  next visible frame after pipelines settle. DLI remains disabled; no host PC or
  chip-state shortcuts. Measure full eligible service cycles with DMA-off, then
  supported active-list conditions separately; no unbounded DMA/RDY claim.
- Capture at actual synchronized safe points around pointer/color/DMA writes,
  deferred callback and RTI; same/fresh/process replay exact. New candidate
  identity must refuse old states and vice versa before mutation. Coordinate
  R65 strict-state version/cache work; no cross-version migration assumption.
- Release/nonunity sanitizer, reset/unload/reload/lifecycle and negative converter
  tuple tests. No retail equivalence, game compatibility, release or app enablement.

## Provenance

CONSUMER-01 supplies shadow addresses; CONSUMER-02 supplies ANTIC and GTIA
public register offsets. Both pinned chip headers reread/hash verified at
77b6484615427746e55fda2755c9cbc320a1fb51; no implementation source consulted.
Order, CRITIC policy, raw byte transfer and fixtures are original decisions.
All instructions already exist in this project's approved factual opcode subset.
