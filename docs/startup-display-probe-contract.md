<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Original Cold-to-progress and geometric bitmap diagnostic

Authoring scope: Mars60cb46a/msg_32af/req_6f74. This is an ORIGINAL cartridge
requirement, not a private application's expected behavior, a BIOS observation,
a runtime repair or native execution acceptance. No font, text or external asset.
This contract is a frozen export input; receipts belong in a separate proof file.

## Independent input specification

Generate twelve explicitly identified cases: Linear32K/exact32768/entry8000,
and Linear8K/exact8192/entry8000 or A000; each crosses direct/shadow with numeric
year26 or secondFF year00,FF. Both years require full Cold. Canonical final24
bytes:20original zero-title digits50, numeric52,56 or00,FF, then little-endian
entry. No file detection, payload padding/duplication or alternate wiring trial.
The8KiB alias is an explicit entry choice in an independently generated8192-byte
cartridge, not a32KiB image truncated or mirrored by the consumer. Native8KiB
execution remains barred until its separate guard/qualification is delivered.

Use qualified combined32KiB native138fad8/modulee8 and guarded8KiB source2e8fd51
ONLY after actual native qualification. Their common2048runtime image remains
5936e46d; no runtime source/input/ABI/provider/capability change is needed here.

After fresh full Cold, observe the first actual application opcode at the
canonical entry:8D0030 (STA3000). Application code stores incoming A/X/Y/P/SP
and completionA5 in3000..3005, using PHP/PLA for one temporary shared-stack byte.
This records handoff but does NOT replace independent observation of first fetch.
Native guard/handoff/NMI refusal semantics remain mandatory. Capture expectations
come from the qualified full-Cold handoff contract, not generator output.

CPU setup disables NMI(D40E00), IRQ(E80E00), DMA(D40000), players/missiles(GRACTL
C01D00), GTIA special modes(PRIOR C01B00) and scroll(D404/500). It initializes
3006..3008 to0,3009 to1direct/2shadow; copies its32-byte display list into0800..081F
and its240-byte bitmap into1000..10EF. No fixture suspension, host RAM write,
forced event, canary seed, reset replay, save import or PC change is permitted.
All application-owned writes:0800..0820,1000..10F0,3000..300A, half-open. Public
shadow writes in the shadow control are explicitly the existing ABI interface,
not private application ownership of0000..0018. No vectors or CRITIC are patched;
full Cold's default CRITIC0/default VBI and exit vectors remain in force.

ROM tables are entry+0400(list32) and entry+0500(bitmap240). Linear32K physical
code offset4000/tables4400,4500; Linear8K physical0/tables0400,0500 with selected
8000/A000 CPU alias references. All other cartridge bytes are original zero-fill
except canonical metadata. Code may not overlap the first table; no executable
instruction is fetched from metadata, open bus or any unspecified helper.

Display list at0800, independently expected literal bytes:70,70,70 (24 blank
scanlines),48,00,10 (mode8 with LMS1000),23 bytes08, then41,00,08 (JVB0800).
It stays within one1KiB display-list page; bitmap stays within one4KiB scan page.
Logical display:40columns by24rows, two-bit selectors packed MSB-first (four per
byte), ten bytes per mode line; each selector covers4color clocks by8scanlines.
Thus active pattern is320high-resolution horizontal samples by192scanlines.

Original geometric selector function, in logical(x,y),0<=x<40,0<=y<24:

1. Top half(y<12):1onleft(x<20),2onright; bottom half:2onleft,1onright.
2. Replace central rectangle18<=x<22,10<=y<14 with0.
3. Set marker(4,4),(5,4),(4,5), and entire outer border to3.

Selector0 uses COLBK=00;1 uses COLPF0=06;2 uses COLPF1=0A;3 uses COLPF2=0E. These are four original
prescribed grayscale register values, not measured television RGB values. Both
controls MUST produce exactly this geometry and selector/color relationship.
No font/glyph reconstruction, fitted crop/scale/translation or weakened pattern.
The native integration owner must independently declare viewport origin and
canonical RGBA conversion BEFORE execution from its public renderer contract;
these are UNKNOWN here, not values fitted after observing a screenshot. The
field-local pixel oracle is fully specified independently of callback margins.

## Controls and expected trace order

Direct control leaves NMI disabled throughout and performs these twelve actual
CPU MMIO stores in order after data initialization: D402=00,D403=08,
C012..C015=00, C016=06,C017=0A,C018=0E,C019=00,C01A=00,D400=22 LAST.
No public display-shadow stores, no runtime VBI or shadow-transfer acceptance is
inferred from this control. The common initialD40000 write is separate.

Shadow control performs NO application display-register stores after common
setup. It writes public shadows5=00,6=08,8..B=00,C=06,D=0A,E=0E,F=00,10=00,
then7=22 LAST; only after the complete list/bitmap/shadow initialization does it
write NMIEND40E40. Ordinary VBI must increment clock01/carry02 and then issue
exactly the same ordered twelve display MMIO values above, DMA last, from the
qualified runtime's actual instruction PCs, before default deferred exit. Observe
real read/write buses, not register readback aliases. Read source shadow immediately
before destination write as specified by the existing display service. Startup
zero writes are separate from active eligible-service transfers. Matching pixels
ALONE cannot establish this path; require real NMI/service and ordered-source/PC
attribution, plus application progress while the display is active. No extra
NMI/IRQ source, custom callback or assumed mid-frame atomicity is introduced.

Both controls set3008=5A after arming their path, then repeatedly INC3006,
INC3007 only on low wrap, JMP to the loop. It is a16-bit application-owned
progress counter, initialized by CPU. Each complete iteration increments once.
Record low/high physical writes and carry order; a frame return may fall between
low and high stores, so an isolated torn sample is not proof of regression.
No exact per-return instruction/cycle count is assumed under DMA/RDY or VBI.

## Eight ordinary-return acceptance

Integration owner independently composes the expected geometry and bus oracle
from this prose. Producer report/instruction inventory and generated bytes are
inputs to identify what runs, not an independent expected-result generator.

Fresh full Cold, neutral original HOST controls, ordinary run calls ONLY; at most
eight returns and external10seconds per case. Record first application fetch,
entry capture, all CPU result/data initialization, ready marker, progressing
counter trace at return boundaries, actual display-list instruction/operand DMA,
and bitmap fetch1000..10EF in ten-byte mode-line sequences. Repeated scanlines
reuse ANTIC's line data; refresh reads are not bitmap/list DMA. Require at least
one fully settled complete specified pattern within eight returns and agreement
of the final two complete sampled patterns. Missing callback/display is failure,
not permission for extra frames, manual events, host state changes or a new image.

Report actual callback count/dimensions/byte pitch/format/row order and native
viewport pixels; preserve original raw identity and PNG/canonical RGBA digests
if capturing images. Direct and shadow final geometry/colors must agree, while
trace provenance must distinguish application MMIO from ordinary VBI shadow
service. Declare exact failure/first unmet condition BEFORE suggesting a runtime
change. No retail equivalence, fullR62 ACK, reference-role, release, device or
product adoption follows. No private payload replay/repair is authorized.

## Documentary scope

Shared ANTIC facts only: Atari Inc.1982 *400/800 Hardware Manual*, II.7..12,
[manufacturer transcription](https://manualzz.com/doc/9258442/atari-400-800-home-computer-system-hardware-manual): display-list/LMS/JVB layout,
1KiB/4KiB counter boundaries, mode8 geometry and two-bit selector order. Read
selected prose/table; OCR/scan limitations retained, not a hardware measurement.
Existing screened public5200 ANTIC/GTIA register declarations supply C000/D400
aliases; home-computer OS shadows/address defaults are NOT5200 facts. Existing
original display-shadow-brief.md supplies the software shadow map/service order.
Pattern, colors, ROM/RAM layout, counter and stop conditions are original policy.
