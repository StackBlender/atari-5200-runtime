<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Authored VBI clock image: fit and static proof

Scope approval: Mars msg_1e39 /3c6a4ce; vbi-clock-brief.md revision2.
This is static reasoning about our original emitted program, not an emulator
run, original firmware reconstruction result or provider acceptance.

Image SHA256: `62df6162ac3accdfa19769c8f2dcd450c510e385fa71f98ec7912f61d449fa54`.
Exactly2048 bytes,1244 written/804 unwritten. Font1024, startup114, interrupt40,
clock16, shared44, vectors6. Startup has14 free bytes, interrupt152, clock80,
shared36; input176/display96/margin250 remain entirely unwritten FF. All
original region boundaries remain; full future-service fit is not established.

## Control flow, memory and stack

Reset's first80 bytes through the vector-initialization loop are unchanged.
The new20-byte block atFC50 writes four bytes0202=A0,0203=FC,0204=B0,0205=FC.
All fourteen slots were first initialized toFC86; only these two are overridden.
It does not write021C..021F or conio storage. The only JSR is nowFC64 ->FEB0,
pushing returnFC66; RTS resumesFC67. Final setup still establishes A=X=Y=0,
P&CF=06,SPFF. Handoff JMP(BFFE) is nowFC6F, not the oldFC5B. Helper/font bytes
are unchanged. Startup has71 explicit stores (14MMIO+25ZP+28vector+4override),
plus the actual two JSR stack writes. Independent acceptance must update these
expectations rather than treating the new image as the old allowlisted tuple.

CPU NMI vector isFC89; resetFC00 and IRQ/BRKFC83. Fault loopsFC80/FC83/FC86
remain unchanged. ClassifierFC89..FC99 is17 bytes: PHA, real NMIST read, AND E0,
CMP40, BNEFC80, NMIRES write, PLA, JMP(0202). The failure branch is same-page
and occurs before acknowledgment/clock/callback. Only accepted current status
reaches dispatch. A temporary software byte is popped before immediate dispatch;
its peak is four bytes including hardware entry. Fault path retains that byte
until owner observation freezes failure; repeated/nested NMI is unsupported.

system_vbiFCA0..FCA7: PHA/TXA/PHA/TYA/PHA/JMP FDF0. The default clock body at
FDF0..FDFF increments low0001, conditionally high0002, reads CRITIC0003 and
jumps through0204 when zero; otherwise JMPFCB0. Both branches stay on FD page.
No JSR is used during interrupt service. INC writes the old value followed by
new value on the real NMOS bus: two clock writes without carry, four with carry.
The service does not use decimal ADC/SBC or write CRITIC/other shadows.

vbi_exitFCB0..FCB5: PLA/TAY/PLA/TAX/PLA/RTI, reversing the Y/X/A save order.
Default maximum additional stack is six (three hardware +three software), not
seven: classifier's temporary was already popped. Total default stack writes
are seven including hardware (classifier1+prologue3+hardware3), despite maximum
simultaneous depth six. Callback depth and nested interrupts are separate and
unsupported unless individually bounded. RTI restores the real hardware P/PC;
an enabled pending IRQ can consequently fire if restored I=0.

## Static normal cycle paths

All values below are documented NMOS base cycles, excluding stalls. These are
manual control-flow counts, not a new CPU implementation or execution result.
Startup adds four LDA#2/STAabs4 pairs:24 cycles and eight instructions. Valid
entries belowBF00 therefore use1108/411; BF00..BFE7 use1115/414. Remeasure all
full cycles against4096 through the new exported handoff symbol. Startup/pending
NMI must be rejected by Mars' revised actual-acceptance observer before Ready;
this module has no hidden startup-phase RAM variable or host-cleared pending bit.

| Default handler block | Base cycles | Instructions |
| --- | ---: | ---: |
| Classifier, supported status | 26 | 8 |
| Register prologue and jump | 16 | 6 |
| Clock/no carry, CRITIC zero, indirect deferred jump | 18 | 5 |
| Default exit including RTI | 22 | 6 |

No-carry CRITIC0 total82/25. Carry adds4 cycles/one instruction. Nonzero CRITIC
replaces a not-taken BNE2+indirect JMP5 with taken BNE3+absolute JMP3, reducing
one cycle without changing instruction count. Four default paths:82/25,86/26,
81/25,85/26. Hardware entry latency is excluded and must be reported separately.
Accepted target512 includes ordinary refresh/RDY with DMA off and RTI; no custom
callback, indefinitely held RDY, active-DMA or WSYNC bound is invented.

## Export and independent execution

Original711a2e9 generation inputs remain byte-identical; baseline target/artifacts
continue to reproduce. The new tools/vbi_clock_image.py has a local six-opcode
extension without mutating the original emitter table. New export is separate:

```sh
python3 tools/export_vbi_candidate.py --source-revision ba90c8550c1be1c85b5aa7d6810e1ee6c6031656 --output-dir build/vbi-candidate
```

A parent may add the baseline module, set SB5200_VBI_SOURCE_REVISION to that full
commit and include cmake/vbi-clock-candidate.cmake. Target sb5200-vbi-clock-image
has the same four SB5200_IMAGE_FILE/MANIFEST_FILE/MAP_FILE/SOURCE_REVISION
properties, with distinct vbi-candidate paths. Parent consumers must depend on
the target and artifact paths before their own validation/conversion. New version
is cold-start-digits-v1.vbi-clock-v1.candidate1; all acceptance/execution/provider
flags stay false. The new map exports classifier/system/clock/exit/handoff symbols.
Every old and new generation input is checked against the supplied commit before
writing output; no network/source import/circular execution gate is introduced.

Nine additional offline methods independently assert all114 startup bytes,
classifier/prologue/clock/exit bytes, relative targets and vectors, strict local
encoding operands, unchanged baseline font/helper/hash, full fit/reserves,
manifest identity/false flags, each pinned-input rejection, stale-pin CLI
no-output and fresh-process reproducibility. Total66 pass. These checks establish
encoding/fit/export, not actual VBI execution or timing.

Mars next extends actual startup interrupt-acceptance/pending-NMI refusal and
allowlists the complete new tuple, then authors independent CPU/ANTIC/clock/
callback/stack/mid-service-safe-point/state/replay/lifecycle fixtures from
vbi-clock-brief.md. Mixed/Reset status cases are synthetic; actual scheduling
must exercise real VBI/DLI and near-handoff/vector-hijack cases. Capture actual
synchronized safe points, not arbitrary mid-instruction states. Old/new image
state refusal must hold both directions; schema-version changes follow actual
persistent observer changes, not guessed necessity. No product/release pin or
commercial-cartridge compatibility approval follows from this packet.


## Committed export verification receipt

Source pin ba90c8550c1be1c85b5aa7d6810e1ee6c6031656 was emitted through the
real pinned CLI and a temporary parent CMake consumer. All four properties,
absolute existing artifacts, image/map hashes, full source revision, false labels
and dependent-target ordering passed. CLI and CMake artifacts were byte-identical.
The original711a2e9 export reproduced its unchanged b2d8ebb8... image at the same
time. Existing build/ CTest passed all66 methods. Temporary parent source/build
were removed; ignored build/vbi-candidate retains the new integration artifacts.
No CPU/chip execution or new-provider acceptance occurred locally.


## Subsequent independent acceptance

Integration-owner msg_9ae4 now reports the bounded execution/timing/state matrix
passing; see [independent receipt](independent-execution.md). This supersedes
pending owner-execution steps above, without converting static analysis into a
local execution result or changing the generated flags/pin. Further service,
release and product acceptance remain separate.
