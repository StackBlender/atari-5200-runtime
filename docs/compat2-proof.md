<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Compatibility generation 2 (compat-v2)

Original development generation over [compat-v1](compat-proof.md), from bounded local
observation of cartridge software expectations. Not firmware, not natively qualified,
not a product release. Which titles were observed stays out of this repository.

| # | Observed expectation | Change |
|---|---|---|
| 1 | Software stores a countdown in `$021C..$021F` and waits for zero. | The default VBI clock decrements each non-zero byte once per frame, before the CRITIC test. |
| 3 | Software installs handlers at `$020A` (keyboard) and `$020C` (break / top fire), leaves `$0208` alone, and expects the interrupt already acknowledged. | IRQ source bit 7: acknowledge (IRQEN disable, POKMSK restore), restore X/Y, `JMP ($020C)` with only A on the stack. Bit 6: acknowledge, `A` = key value, full A/X/Y frame left on the stack, `JMP ($020A)`. Other sources still fault. |
| 4 | Software restores the IRQ vector to `$FC03` as a default. | `$FC03` is `JMP $FE00`; reset entry is `JMP $FC74` (`SEI CLD LDX #$FF TXS`, `JMP $FC06`). Callable boundary `+$0F` unchanged. |
| 5 | Software may install its own keyboard handler at `$0208`. | `$0208` high byte other than `$FC` is called directly; the default goes through the key-value path to `$020A`. |
| 6 | Software copies six default vectors from a table at `$FE95` into `$0200`. | Table present: IRQ `$FC03`, immediate VBI `$FCB8`, deferred VBI `$FCB2`, DLI `$FCDD` (bare RTI), keyboard `$FC8D` (key-value routine), keyboard deferred `$FCB2`. |
| 2 | A vector whose high byte is `$FF` means "use the default". | Immediate (`$0202`): falls back to `system_vbi`. Deferred (`$0204`): falls back to the register-restoring exit at `$FCB2`. |

All new code lives in previously erased space (`$FCE0..$FCEF`, `$FDC0..$FDDC`, `$FDE0..$FDEC`, `$FF00..$FF1F` (first bytes of the former reserve), `$FE4D`, table `$FE95..$FEA0`, `$FCF0..$FCFB`, `$FD33..$FD3F`, key table `$FDF0..$FDFF` (reuses the superseded clock body), `$FC00..$FC0E`, `$FC74..$FC7B`, `$FC8D..$FC99`);
three jump operands and two branch operands (`$FE10`, `$FE1F`) are redirected (`$FCD9`, `$FCA6`, `$FE8C`). Image 2048 bytes, vectors and
reserve untouched.

Export: `python3 tools/export_compat2_candidate.py --source-revision <full-commit> --output-dir <dir>`
(`cmake/compat2-candidate.cmake` is the opt-in target). Offline tests prove bytes, layout
and export identity only.

Key values come from KBCODE bits 4..1 through a 16-byte table: digits 0..9, `$0A` `*`, `$0B` `#`, `$0C` Start, `$0D` Pause, `$0E` Reset. The KBCODE layout was observed; the numbering is inferred from consumer behaviour and is not manufacturer data.

Known gap: a `$FFFF` key or break vector set explicitly by software is still jumped to.
