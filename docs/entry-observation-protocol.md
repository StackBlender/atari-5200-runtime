# ENTRY-01 scalar observation protocol (draft v1)

RUNTIME-003 provides original diagnostic tooling for review. No operator, original
execution, complete cartridge, result-area approval or measured baseline exists.
This protocol is not permission to run a reference system. The record validator
checks format and internal consistency; it cannot authenticate approval receipts,
hardware identity, operator conduct or an original-system claim.

## Roles and release boundary

| Role | Allowed input/output | Current assignment |
| --- | --- | --- |
| Documentary researcher | Screened behavioral prose; dated fact packets and unknowns | apollo_retro_owner |
| Original-system operator | Approved original diagnostic, lawful system, stimulus; six scalar outputs only | Unassigned |
| Evidence reviewer | Scalar record, source/probe identities, ownership/instrumentation/role receipts; approved fact packet | Unassigned |
| Runtime implementer | Approved fact packet and original diagnostic expectations; no firmware/source/asset dumps | Project maintainer; measured handoff not established |

Before execution, record named role assignments and permitted exposure in a
reviewed handoff. A token in JSON refers to that handoff; it is not an approval.
Do not fill missing roles with the current author and call it independent review.
The operator must establish lawful access and the actual console/firmware revision
without copying firmware content into this project. An unknown revision can be
logged but cannot select a retail policy.

Review these items before issuing a runnable diagnostic: metadata encoding and
mapper layout, result-area ownership and DMA exclusions, permitted stack use,
interrupt window, readout method, reset apparatus, role exposure and repeated-run
procedure. No original BIOS, vendor glyph or manufacturer instruction trace is an
input/output of this protocol. A cartridge generator is deliberately absent.

## Authored capture fragment

`tools/entry_probe.py` emits 26 original bytes plus a deterministic descriptor.
It is a fragment, not a valid cartridge or runtime provider. Addresses are explicit
parameters: entry must fit within the proposed CPU cartridge window 4000–BFE7;
six result bytes must fit in candidate 0220–3FFF. These tool bounds do not prove
that an address is writable, free of display DMA or owned by a cartridge.
The example addresses 8000/3000 are synthetic layout choices, not approved defaults.

| Offset in result area | Field | Capture |
| --- | --- | --- |
| 0 | a | STA before changing A |
| 1 | x | STX before changing X |
| 2 | y | STY before changing Y |
| 3 | p_pushed | PHP then PLA, saved before TSX |
| 4 | sp | TSX after the balanced push/pull |
| 5 | complete | Authored A5 marker written after all captures |

Ordered source plan, with `R` and `E` supplied only after review:

```asm
STA R+0
STX R+1
STY R+2
PHP
PLA
STA R+3
TSX
STX R+4
LDA #$A5
STA R+5
idle: JMP idle  ; E+23
```

The fragment has one temporary stack byte and no net stack-pointer change before
SP capture. It overwrites that one stack slot but never reads the prior value.
The operator must review this use, including wrap and pending interrupts. This
probe is observational, not transparent: A/X and flags are changed after their
capture; no register restoration or return to a manufacturer continuation occurs.
No arbitrary stack, return address, ROM, MMIO or font is copied into the results.

Correction rules: keep raw `p_pushed`, derive only `p_known = p_pushed & CF` with
`p_known_mask = CF` (N,V,D,I,Z,C). Do not assign original values to B/expansion
bits. PLA and TSX change flags after the saved status. SP needs no arithmetic
correction after a balanced push/pull, subject to the interrupt-window review.
Do not insert SEI, CLD, loads, stack setup or a subroutine call before capture.
Those would change the boundary being measured. No expected Atari register value
is supplied by these rules.

A5 already present in RAM is insufficient: the operator must observe the final
write event for this execution, then read the six whitelisted scalars. Record how
the readout was established without a firmware trace or broad memory dump. No
unreviewed debugger or emulator/original-firmware runner is implicitly authorized.
For repeated/reset runs, distinguish a fresh write from retained prior results.
If completion cannot be observed, raw values are inconclusive. If an interrupt is
observed or its effect cannot be bounded, the capture is inconclusive; do not
invent a correction or assume that a handler preserved registers.

## Record contract

`tools/observations.py RECORD.json` accepts one UTF-8 JSON object up to 65536
bytes, at most eight nested levels, 64 trials and 32 steps per trial. Unknown or
missing fields, duplicate keys, non-finite constants and invalid types are rejected.
Booleans are not numeric bytes. No extension field or arbitrary byte array exists.

| Object | Required fields and constraints |
| --- | --- |
| Root | `schema:1`, `probe:ENTRY-01`, `kind:synthetic` or `original-reference`, `observation_id`, `observer`, `recorded_at`, `machine`, `approval_refs`, `artifact`, `trials` |
| Identifiers | ASCII `[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}`; use role/receipt IDs rather than personal information |
| recorded_at | Valid UTC timestamp `YYYY-MM-DDTHH:MM:SSZ`; records observation time, not a build timestamp |
| machine | `model:ntsc-four-port`, `board_revision`, `firmware_revision`; revision values are identifiers, not extracted data |
| approval_refs | `access`, `operator`, `roles`, `result_area`, `protocol`; each an identifier; null allowed only in synthetic records |
| artifact | `entry_address`, `result_start`, `source_sha256`, `encoder_sha256`, `fragment_sha256`, `cartridge_sha256` |
| trial | Unique integer `trial_id` 0–65535, `reset_kind`, `steps`, `held_inputs`, `raw`, `completion_write_observed`, `interruption` |
| step | `action` from the list below and integer `duration_ms` 0–3600000; duration is the operator's recorded action duration, not invented CPU timing |
| raw | Exactly the six named result fields, each integer 0–255; null if no scalar result was collected |

Hashes are 64 lowercase hex digits. Source/encoder/fragment hashes must match the
current checked-out diagnostic and its parameters. To validate a historical
capture, use its reviewed source revision; do not rewrite old hashes to match a
new tool. `cartridge_sha256` is recorded but unchecked unless the operator provides
`--original-diagnostic PATH`, which checks exactly 32768 bytes and the full hash.
That option hashes a locally authored diagnostic only; it does not validate title
encoding, certify the mapper/entry layout or authorize use of the image.

Reset kinds: `cold-power`, `cpu-reset`, `controller-reset`. Cold sequences require
power-off followed by power-on; other kinds require their corresponding action.
They remain separate stimuli: controller Reset does not imply CPU reset or a new
cartridge handoff. No completion can be a useful observation; it is not an entry
register baseline. Do not report unsupported reset apparatus as an executed test.

Step actions: `power-off`, `power-on`, `install-original-cartridge`, `wait`,
`cpu-reset`, `controller-reset`, `set-inputs`, `observe-completion-write`,
`read-six-scalars`. Completion observation must follow the reset trigger and
precede scalar readout. Record one trial per reset; repeating resets belongs in
separate trials.

`held_inputs` contains unique semantic labels: fire-1/fire-2, start/pause/reset,
stick-left/right/up/down, key-0 through key-9, key-star/key-hash. Empty means no
held input. These are proposed stimulus labels, not hardware key codes or proven
analog endpoints. v1 describes a fixed held combination per trial, not an analog
waveform or input changes during capture; use a later reviewed protocol for those.
`interruption` is `none-observed`, `observed` or `unknown`. A reviewed apparatus
must justify that classification; the validator cannot inspect the machine.

## Results and review

A well-formed inconclusive record exits successfully so it can be retained.
Each trial reports reasons and `usable_for_protocol_review`; missing completion,
a non-A5 marker, absent raw scalars or an uncertain/observed interrupt window
prevent that flag. Invalid input exits 2 without a partial success report.

Every report preserves `kind`; synthetic never becomes reference evidence.
`evidence_approved`, `original_measurement_claim`, `approval_refs_verified` and
`runtime_policy_selected` remain false. Byte/hash consistency and syntactic
receipt IDs do not establish provenance or accuracy. The cartridge hash flag
means only that the supplied local file matched the recorded size/hash.

After an independent pilot, the reviewer checks source exposure, actual roles,
identities, timing/units, apparatus, repetitions, correction rules and uncertainty.
Only then create a separately approved behavioral fact packet. Compare repeated
trials within the same profile/reset/input case; preserve disagreement rather
than averaging register bytes or imposing thresholds from our replacement.
No record produced in this repository currently represents such a pilot.
