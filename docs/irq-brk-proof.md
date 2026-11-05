<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# IRQ/BRK static proof and separate export

Original authored candidate, scope/execution acceptance pending; see
[irq-brk-brief.md](irq-brk-brief.md). No keypad workaround or acquisition change.
Image2048 SHA256
2b257c582044af2308699c6a0f327dca674ed79bd95eed2da7cea2537ead0675.
1410 written/638 free, interrupt77/192 (new26), startup127/128, input53,
clock16, display63, shared44, font1024, vectors6; margin250 entirely untouched.

## Static instruction/stack argument

New irq_classifierFD00..FD19. PHA/TXA/PHA saves A and X; TSX/INX/INX/INX,
LDA0100,X/AND10/BNE brk_dispatchFD14, restoring PLA/TAX/PLA then JMP(0200)
or JMP(020E). irq_dispatchFD0E, branch displacement06. CPU IRQ/BRK vectorFD00;
old irq_faultFC83 remains exported, unchanged. All prior image bytes/labels are
identical except IRQ hardware vector and the newly occupied26-byte body.

Let interrupted stack byte S. Hardware stores P at0100+((S-2) mod256), then
leaves SP=(S-3) mod256. Two saves leave SP=(S-5) mod256. TSX+three INX gives
X=(S-2) mod256; LDA0100,X accesses exactly stacked P for all256 S without page
crossing. Five distinct stack slots used, including wrap. Pop X/A leaves original
hardware frame untouched; Y unchanged. The classifier reads stacked status only,
never edits saved P/PC or checks a device source. Both callbacks own source
handling and their register/stack discipline; no hidden JSR/VBI save frame.

IRQ39 base cycles/14 instructions, BRK40/14 (taken branch costs one more),
hardware entry7 and callback RTI6 separate. All branches within pageFD; base0100
indexed load cannot cross a page. Full dispatch128-cycle target is unmeasured
until independent execution. No startup/VBI/analog/display/DLI costs change;
max startup1131, complete VBI240..245 nominal. Max dispatch stack5 incl hardware,
callback entry3; no nesting/arbitrary callback/held source deadline guarantee.

Cold0200/020E still point to FC86: install callbacks before CLI or BRK. Masked
pending IRQ is normal, source remains chip-owned; callback must acknowledge
its selected real source or retrigger can occur. BRK with I set still dispatches;
return uses hardware PC+2. NMI hijack/source provenance limitations remain.

## Reproducible explicit export

```sh
python3 tools/export_irq_candidate.py --source-revision <full-commit> --output-dir build/irq-candidate
```

Parent adds baseline module, sets SB5200_IRQ_SOURCE_REVISION to full committed
pin, includes cmake/irq-brk-candidate.cmake and depends on sb5200-irq-brk-image
before conversion. Same four properties SB5200_IMAGE_FILE, SB5200_MANIFEST_FILE,
SB5200_MAP_FILE absolute paths and SB5200_SOURCE_REVISION full40-hex commit.
Separate irq-candidate directory. Baseline inputs plus tools/irq_brk_image.py,
tools/export_irq_candidate.py and cmake/irq-brk-candidate.cmake byte-match named
commit before any output. No dirty bypass or changed prior export dependencies.

Manifest version
cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.dli-dispatch-v1.analog-shadow-v1.irq-brk-dispatch-v1.candidate1.
Schema1/ABI1/reset/mapper/profile/Starting observer unchanged. All capabilities[]
and provider/execution/retail/full-cycle flags remain false. New IRQ/BRK nominal
fields describe static39/40, full dispatch target128 and false verification only.
Explicit exact new image/source/map/manifest/profile allowlist and sb52rt-dev2
cross-candidate refusal require Mars review. Existing irq_fault fault-symbol
metadata is retained, not silently replaced by the live irq_classifier target.

## Verification and remaining gates

Eight new methods bring total95: independent exact26 bytes/branch/CPU vectors,
all256-position stack-index arithmetic and wrong-base wrap counterexamples,
only intended image differences/preserved labels/startup, allocations/reserves,
manifest identity/timing/false flags, every source mismatch, fresh-process image/
map and real previous-pin CLI refusal before output. Direct unittest and existing
CMake/CTest pass. Static stack arithmetic is not a CPU interpreter or execution.

Independent original Mars fixtures must exercise actual IRQ and CPU BRK sources,
original A/X/Y/P/SP/PC+2, all stack positions, callback acknowledgments/retrigger,
masked IRQ versus BRK, source-vector/hijack/startup limits, real safe points and
same/fresh/process replay, mutual candidate refusal, default-OFF/old-provider/
analog/input/VBI/display/DLI/lifecycle/Release/nonunity sanitizer regressions.
No timer/keypad/fire runtime, firmware equivalence or game claim follows.

## Committed IRQ/BRK export receipt

Source/export42762a73a0caa72b7753bd5aa4380cf9a63c573f is pushed. Real CLI
and temporary parent CMake consumer pass all4properties, absolute artifacts,
dependency ordering, full image/map/source identity/false flags and CLI equality.
All five earlier pinned candidate exports reproduce unchanged image hashes.
Temporary parent source/build removed; ignored output in build/irq-candidate.
Exact tuple/stack/IRQBRK/callback/source-ack/timing packet sent Mars req_6f74;
independent scope/CPU/RTI/state acceptance pending. No local CPU run, provider
flag/pin/release/app/default change. Next independent acceptance and remaining
source-specific IRQ/timer/reset/fire service contracts; keypadreq72f0 separate.
Runtime lease released after push.
