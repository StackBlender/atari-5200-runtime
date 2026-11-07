<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Compatibility generation 2 (compat-v2)

Original development generation over [compat-v1](compat-proof.md), from bounded local
observation of cartridge software expectations. Not firmware, not natively qualified,
not a product release. Which titles were observed stays out of this repository.

| # | Observed expectation | Change |
|---|---|---|
| 1 | Software stores a countdown in `$021C..$021F` and waits for zero. | The default VBI clock decrements each non-zero byte once per frame, before the CRITIC test. |
| 3 | Break and keyboard interrupts: software installs handlers at `$020C` (break / top fire), `$0208` (own keyboard handler, A-only frame) or `$020A` (deferred, full frame, key value in A) and expects the source acknowledged. | Bits 7 and 6 are acknowledged (IRQEN disable, POKMSK restore), X/Y restored, then break → `($020C)`; keyboard → `($0208)` unless it holds a default (`$FC..`/`$FD..`), in which case the default routine at `$FF20` converts KBCODE to a key value and calls `($020A)` with the full frame, or exits at `$FCB2` if `$020A` is unset. Other sources fault. |
| 4 | Software restores the IRQ vector to `$FC03` as a default. | `$FC03` is `JMP $FE00`; reset entry is `JMP $FC74` (`SEI CLD LDX #$FF TXS`, `JMP $FC06`). Callable boundary `+$0F` unchanged. |
| 6 | Software copies six default vectors from a table at `$FE95` into `$0200`. | Table present: IRQ `$FC03`, immediate VBI `$FCB8`, deferred VBI `$FCB2`, DLI `$FCDD` (bare RTI), keyboard `$FC8D` (key-value routine), keyboard deferred `$FCB2`. |
| 2 | A vector whose high byte is `$FF` means "use the default". | Immediate (`$0202`): falls back to `system_vbi`. Deferred (`$0204`): falls back to the register-restoring exit at `$FCB2`. |

New code lives in previously erased space, the head of the former reserve (`$FF00..$FF4B`) and the erased superseded clock body (`$FDF0..$FDFF`):
`$FC00..$FC0E` (reset entry), `$FC74..$FC7B`, `$FC8D..$FC9B`, `$FCE0..$FCEF`, `$FCF0..$FCFB`, `$FDC0..$FDDC`, `$FDE0..$FDEC`,
table `$FE95..$FEA0`. Redirected operands: `$FCD9`, `$FCA6`, `$FE8C`, and the unsupported-source fault jump at `$FE4D`.
Image 2048 bytes, vectors untouched, `$FF4C..$FFF9` still erased.

Export: `python3 tools/export_compat2_candidate.py --source-revision <full-commit> --output-dir <dir>`
(`cmake/compat2-candidate.cmake` is the opt-in target). Offline tests prove bytes, layout
and export identity only.

Key values come from KBCODE bits 4..1 through a 16-byte table: digits 0..9, `$0A` `*`, `$0B` `#`, `$0C` Start, `$0D` Pause, `$0E` Reset. The KBCODE layout was observed; the numbering is inferred from consumer behaviour and is not manufacturer data.

Known gap: a `$FFFF` key or break vector set explicitly by software is still jumped to.
