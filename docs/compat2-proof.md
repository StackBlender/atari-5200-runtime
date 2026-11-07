<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Compatibility generation 2 (compat-v2)

Original development generation over [compat-v1](compat-proof.md), from bounded local
observation of cartridge software expectations. Not firmware, not natively qualified,
not a product release. Which titles were observed stays out of this repository.

| # | Observed expectation | Change |
|---|---|---|
| 1 | Software stores a countdown in `$021C..$021F` and waits for zero. | The default VBI clock decrements each non-zero byte once per frame, before the CRITIC test. |
| 2 | A vector whose high byte is `$FF` means "use the default". | Immediate (`$0202`): falls back to `system_vbi`. Deferred (`$0204`): falls back to the register-restoring exit at `$FCB2`. |

All new code lives in previously erased space (`$FCE0..$FCEF`, `$FDC0..$FDDC`, `$FDE0..$FDEC`);
three jump operands are redirected (`$FCD9`, `$FCA6`, `$FE8C`). Image 2048 bytes, vectors and
reserve untouched.

Export: `python3 tools/export_compat2_candidate.py --source-revision <full-commit> --output-dir <dir>`
(`cmake/compat2-candidate.cmake` is the opt-in target). Offline tests prove bytes, layout
and export identity only.
