<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Compatibility generation (compat-v1)

Original development generation over [callable-reset-v1](callable-reset-proof.md). It changes
three behaviours that bounded local observation showed cartridge software relies on. It is
not firmware, not qualified natively, and not a product release. Details of which titles
were observed stay out of this repository.

| # | Observed expectation | Change |
|---|---|---|
| 1 | Vertical-blank NMI is already running at cartridge handoff; software polls the frame counter. | Reset writes `NMIEN=$40` (`LDA #$40`, `STA $D40E`) just before the handoff tail. |
| 2 | The per-frame changing counter byte is `$0002`; `$0001` is the high byte. | Default clock body increments `$0002` and carries into `$0001` (operands swapped, same length). |
| 3 | An NMI can arrive with no source flagged in NMIST. | The classifier's failure branch now lands on `PLA`, `RTI` at `$FCDC` instead of the fault loop. |

Image: 2048 bytes, 1567 used / 481 free, reserve and vectors untouched. Startup is 7
bytes larger (+6 static cycles, +2 instructions, not natively traced). Changed bytes are
limited to the reset region, `$FDF1`, `$FDF5`, `$FCCD`, `$FCDC..FCDD`; callable-reset layout
(`+$0F` boundary, `JMP ($BFFE)` at `+$8A`) is kept and re-tested.

Export: `python3 tools/export_compat_candidate.py --source-revision <full-commit> --output-dir <dir>`
(`cmake/compat-candidate.cmake` is the matching opt-in target). Native identity requires owner
qualification; the offline tests prove bytes, layout and export identity only.
