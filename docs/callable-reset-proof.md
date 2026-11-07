<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Callable-reset layout (development generation, authored 2026-11-07)

Capability `callable-reset-v1` rebuilds ONLY the reset region of the exact cart-owned
diagnostic parent (image SHA256 5936e46d08c7991231a52dfb6c1a404a7a0d1ab505a51b2c5e09a569d7ad20e4)
so software that reuses the reset routine as a subroutine works. Every other byte, vector, fault
stub, allocation and the 90 reserved bytes are unchanged.

## Consumer-observed requirement

Observed from a licensed cartridge's behaviour through the independent Mars-integrated emulator
with an instruction trace (no manufacturer firmware, disassembly or foreign source consulted):
the program reads a revision byte at $FFF8, copies [reset-vector target, target+L) to RAM at
$2100, writes RTS ($60) at the end address, and calls $2100+$0F to re-initialise hardware.
L = $181 when the byte is 0, $16B when it is $32, otherwise $8A. With the previous layout $0F
fell mid-instruction and the routine ended in JMP ($BFFE) at +$6B, so the copy restarted the
program forever (about four copies per frame, display and NMI never enabled).

## Layout

| Offset | Content |
| --- | --- |
| +$00..+$0E | SEI CLD LDX#$FF TXS LDA#0, STA D40E, STA D400, NOP NOP (instruction boundary at +$0F) |
| +$0F..+$70 | unchanged initialisation body (MMIO zero, shadows, vectors, JSR $FEDC, POKEY/GTIA setup, JSR $FD80) then CLC CLV LDY#0 LDX#0 LDA#0 and an always-taken BCC to +$8A |
| +$80..+$88 | existing NMI/IRQ/startup fault stubs, skipped by the branch |
| +$8A | JMP ($BFFE), the cartridge handoff, at exactly the fall-through offset |

$FFF8 stays $FF (not 0 or $32), selecting L=$8A. No NMI is enabled by the runtime; the
target enables it itself. Static budget: used 1556 -> 1560, remaining 488; startup region 111
of 128, interrupts region 80 of 192 (three handoff bytes borrow from it); nominal startup
+3 instructions (traced natively: 257 -> 260) and +7 cycles (statically, one taken same-page
BCC and two NOPs): numeric 764/771, second-FF 745/752. Native cycle confirmation is Mars'.

## Evidence

- `tests/test_callable_reset_image.py` (5 methods; 242 offline total pass): changed-region bound,
  independent decode (boundary at +$0F, BCC lands on +$8A, no absolute transfer into the copied
  range), an independent subset interpreter that performs the consumer copy/patch/call and proves
  fall-through to the RTS with A=X=Y=0, C=V=0, identical stores and calls to the parent, real
  reset reaching the handoff, revision-byte policy, export identity/timing and pin checks.
- Native experiment (consumer side): the image exactly as generated here, supplied through the
  stock external-bios path of the debug probe (our own image, no firmware), takes a licensed 32K
  target from a restart loop to its menu with DMA/display and NMI enabled and responding to fire.
  This is NOT a Mars provider qualification; the target is not named here and its results stay
  in ignored private notes.

## Not claimed

No Mars provider admission, no retail or title compatibility, no warm/CPU reset service, no
change to any accepted generation. Mars integration needs a new variant, tuple and independent
native qualification of this exact image.
