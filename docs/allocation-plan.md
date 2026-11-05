# Original allocation proposal

RUNTIME-004 planning input, 2026-11-05. This is an estimated budget for review,
not an emitted runtime, approved service policy or proof that complete services
fit. Mars review 1f411e5 accepts it as an estimated planning budget, with no
CPU/ANTIC routing or alignment conflict identified; actual asset fetches, per-service
fit and stack depth remain unproved. The machine target is NTSC four-port. A documentary development profile and
its original policies must be named separately from any final/retail firmware
revision; no such policy is selected by this proposal.

## Full-image allowances

| Range inclusive | Bytes | Proposed allowance | Basis / unresolved work |
| --- | ---: | --- | --- |
| F800–FBFF | 1024 | Independently authored 128 × 8-byte glyphs | Original dimensions/encoding proposal; no vendor bitmap. Confirm consumer character-window/ANTIC contract before assets. |
| FC00–FC7F | 128 | Startup / mapped cartridge handoff | Primary CART-01; metadata, reset values and explicit initialization order still need review. |
| FC80–FD3F | 192 | NMI/VBI/DLI, IRQ/BRK dispatch | Dated PAM conventions plus candidate public vector declarations; resolve profile, CPU frame and handler contracts. |
| FD40–FDEF | 176 | Port, analog, keypad and fire processing | Allowance only; scan algorithm/cadence/postconditions not approved. |
| FDF0–FE4F | 96 | Clock, attract and timer work | Clock ordering/profile, units and overflow cases remain open. |
| FE50–FEAF | 96 | Display/shadow transfer | Candidate declarations do not establish writable effects, order or cadence. |
| FEB0–FEFF | 80 | Shared routines and authored constants | No hidden external table or copied asset allowance. |
| FF00–FFF9 | 250 | Explicit unassigned margin | Must remain reported; using margin requires a reviewed allocation update. |
| FFFA–FFFF | 6 | CPU vectors | Generic CPU locations; targets must be authored executable handlers. |
| Total | 2048 | 1024 assets + 768 code + 250 margin + 6 vectors | Complete allowance, not demonstrated implementation fit. |

The font begins on a 1 KiB boundary and does not overlap CPU vectors. Alignment
is proposed here; it does not establish the missing Atari encoding or CHBASE
policy. A smaller first prototype must retain the complete future allowance in
its map. It cannot claim service completion from a padded image or count another
service's unused bytes twice. The current four-byte tool loop has no relevance
to these service estimates.

## RAM and stack ownership

| Area | Planned ownership | Evidence / restriction |
| --- | --- | --- |
| 0000–0018 (25 bytes) | Existing documentary OS reservation | March PAM; candidate field addresses in consumer-interface.json. Per-field operations/defaults remain unapproved. |
| 0019 upward | Cartridge/consumer; no new runtime allocation | Do not consume cc65's conio fields or assume application RAM is spare runtime scratch. |
| 0100–01FF (256 bytes) | Shared CPU stack page | October PAM. Proposed runtime transient allowance at most 32 bytes, including hardware frames/prologues/calls; analysis and startup SP remain unresolved. This is not 32 permanently reserved bytes or a cartridge free-space guarantee. |
| 0200–021F (32 bytes) | Conservative software-vector reservation | October PAM; candidate cc65 vectors end at 021B. Do not reclaim 021C–021F from that difference alone. |
| Other persistent RAM | Zero additional bytes proposed | Any need for scratch, display storage or RAM-resident code reopens ownership review. |
| Diagnostic six-byte result area | Separate original diagnostic cartridge | Candidate address is a parameter; not a runtime allocation or approved hardware readout. |

Mutable emulated state must live in declared RAM/chip state, never hidden host
storage. Original assets remain immutable image data. Review every stack path,
interrupt nesting and routine clobber set; if the 32-byte transient estimate is
not supported, revise the budget and explicitly assess cartridge impact before
execution. Do not infer an original stack-pointer value from this allowance.

## First bounded implementation gate

Before service code, obtain agreement on:

1. A named documentary/consumer development profile with explicit unsupported
   cases; any author-selected defaults must be identified as original policy.
2. Which candidate public ABI declarations are accepted, and what primary or
   approved observations are still required for each claimed service.
3. A concrete metadata encoder and CPU-bus cartridge mapping; no diagnostic
   bypass, physical-file-tail shortcut or host PC jump.
4. Per-register startup writes/aliases/order, numeric values or approved original
   policy, software vectors, interrupt hardware/software frames and RAM ownership.
5. Original asset encoding/placement and the full code/font/vector/margin budget.

Then emit the smallest supported startup, produce an actual image/map and execute
original diagnostics through the integration owner. Authoring a complete probe
cartridge is a separate step after its encoding/profile review; original-system
execution additionally requires the operator/role/protocol prerequisites.
If any service overflows its allowance, stop and review rather than silently
using margin, moving font data, stealing RAM or inventing banking. As services
expand, all claimed code/assets must fit and pass together. Raw byte counts and
self-consistency are never substitutes for compatibility observations.
