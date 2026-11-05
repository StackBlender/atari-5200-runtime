<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# First authored startup: fit and execution packet

Approved scope: Mars msg_aa05 / 7c290c4; contract startup-brief.md revision2.
Source tools/startup_image.py and independent expected bytes/pixels in
tests/test_startup_image.py. This packet is static reasoning over OUR program,
not firmware disassembly, an emulator, CPU execution or an original-system result.

## Actual emitted allocation

Image SHA256 `b2d8ebb8d0070f2aee1bd79d7adfee85b88797702cb96035ab3a18e9bd37f68d`,
exactly2048 bytes. The generated JSON includes source/encoder/allocation hashes.

| Allocation | Written | Allowance left |
| --- | ---: | ---: |
| F800–FBFF original glyph bank | 1024 | 0 |
| FC00–FC7F startup | 94 | 34 |
| FC80–FD3F unsupported-interrupt/fault loops | 9 | 183 |
| FD40–FDEF future inputs | 0 | 176 |
| FDF0–FE4F future clocks | 0 | 96 |
| FE50–FEAF future display | 0 | 96 |
| FEB0–FEFF metadata helper | 44 | 36 |
| FF00–FFF9 margin | 0 | 250 |
| FFFA–FFFF CPU vectors | 6 | 0 |
| Total | 1177 | 871 |

147 code bytes +1024 assets +6 vectors. All future allowances and margin retain
FF fill, enforced by independent tests. Only this bounded scope fits; no proof
that the complete future runtime fits. No sb5200-runtime-image provider target.
The map keeps accepted/executed capabilities empty; authored_capabilities names
cold-start-digits-v1, execution_verified and provider_approved remain false.

## Control flow and stack argument

Reset FC00 masks IRQ, clears decimal and sets SPFF before initialization.
Fourteen MMIO stores match the ordered contract. The ZP loop at FC39 uses X=18
through00, stores zero exactly25 times, and exits after DEX makes X=FF. It never
stores with X=FF. Vector loop FC40 starts X00, writes low86/highFC to successive
slots, advances X twice per iteration and exits at1C after fourteen iterations.
It writes exactly0200–021B; no padding or conio writes.

The only JSR is FC50 ->FEB0. It pushes return address FC52 at01FF/01FE; the
only successful RTS atFED8 consumes it and resumesFC53, restoring SPFF. No nested
calls/software pushes. Digit loop FEB2 checks22 bytes BFE8–BFFD against inclusive
50..59. All invalid branches reachFED9 ->FC86. High-entry checks accept40..BF;
BF additionally requires low<E8. For valid entry, CLC/CLV then LDY00/LDX00/LDA00
force A=X=Y=0 and P&CF=06; SEI/CLD survive the helper. JMP(BFFE) atFC5B performs
the handoff. No return frame is fabricated, and no other indirect target exists.

Ordinary maximum extra stack is two bytes, balanced before handoff. One hardware
interrupt after TXS can add three, for at most five before stopping at the first
fault PC. Before TXS or with repeated NMI edges this bound does not apply. Each
fault is an immediate self-loop with no software pushes, RTI or success return.
Diagnostic PHP adds one transient balanced byte after handoff. CPU execution must
independently verify these arguments; static bytes do not discharge that gate.

## CPU-cycle derivation and remaining full-cycle gate

Use documented NMOS timing (CPU-02 manufacturer reference): implied/immediate
2; STAabsolute4; STAzero-page-X4; STAabsolute-X5; LDAabsolute/X4 without crossing;
JSR/RTS6; JMPindirect5. A branch is2 not taken,3 taken on the same page. Every
branch source/fallthrough/target lies on the same FC or FE page. Digit addresses
BFE8+00..15 never cross a page. Stores include their fixed indexed dummy-read
cycles. No implied page penalties have been omitted from this base count.

| Block | NMOS base cycles |
| --- | ---: |
| Initial flags/SP/A and fourteen MMIO stores | 72 |
| ZP: LDX +25*(STA4+DEX2) +24*branch3 +last branch2 | 226 |
| Vectors: LDX +14*body20 +13*branch3 +last branch2 | 323 |
| JSR | 6 |
| Helper: LDX +22*body16 +21*branch3 +last branch2 | 419 |
| Valid entry below BF00: pointer checks/branch/RTS | 23 |
| Valid BF00–BFE7: pointer checks/branch/RTS | 30 |
| Final flag/register setup and indirect JMP | 15 |

Totals:1084 cycles for valid4000–BEFF;1091 for BF00–BFE7. Corresponding instruction
counts are403/406. The default diagnostic entry8000 uses1084/403. This excludes
chip reset overhead, interrupts and ANTIC refresh/RDY stalls. **It does not prove
the4096 full-cycle deadline.** The worst valid base path leaves3005 cycles for
stalls; no refresh-stall budget is invented here. Mars must implement instruction-
boundary observation and measure/count all intervening stalls before acceptance.
Unexpected stalls/interrupts, failed handoff or a frame-only observer cannot be
relabeled a pass. If4096 cannot be established, stop for reviewed bound revision.

## Independent Mars fixture requirements

Use image identity above, explicit Linear32K board/32768-byte load success, and
the original diagnostic candidate (whole-image hash remains
c7ae62b374ccecde52448d39596421924e749cac9175838198f4b427d0fe83f7).
The candidate source/encoder descriptor must be regenerated after emitter changes;
its image bytes are unchanged. Do not read/run GPL implementation to satisfy
this fixture if that violates the owner's source boundary; use these interface
expectations and authored artifact through the reviewed integration path.

Observe reset-vector fetch and first FC00 instruction, then exact instruction
boundaries through mapped entry8000; no host jump or traps. Report actual emulated
cycles including stalls, instruction count, failure PCs and fresh A5 store. Check
A=X=Y=00, P&CF=06, SPFF at entry. Runtime writes: fourteen MMIO +25ZP +28 vector
stores =67 explicit stores, plus the two real JSR stack writes; read/dummy cycles
are not stores. Cart capture subsequently writes six result bytes and one PHP
stack byte. Baseline caller sentinels AFTER core cold-power randomization, outside
these authorized writes. Check repeat cold power and fresh instances.

Negative metadata for every digit position:4F/5A/FF; boundary entries3FFF/4000/
BEFF/BF00/BFE7/BFE8/BFFF/C000/FFFF. Use independent original test entry stubs or
stop at the observed handoff for accepted boundary addresses; changing metadata
alone does not put executable code at every accepted address. Expect metadata
failureFC86 for invalid cases and no cart handoff. Inject at most one early NMI and expect FC80. A pending hardware IRQ while I=1
must remain masked; use an independently authored cart BRK stub after handoff
to exercise the IRQ/BRK vector and expect FC83, rather than forcing a masked IRQ
to behave as delivered. Test unsupported reset
kinds fail before mutation through the future structured operation, missing/wrong
provider and mapper failures, and normal external-BIOS missing-image rejection.

Read CPU/peek/DMA at original font addresses; digit0 bytes3C42420042423C00,
digit8 bytes3C42423C42423C00, all non-digit glyphs blank. Later own cart display
checks require safe display list/screen and settled pipelines before DMA22. No
boot artwork/reference footage is needed. No game, original firmware, device,
battery, raw-state portability or complete-service compatibility claim follows.
