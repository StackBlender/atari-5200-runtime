<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Bounded IRQ and BRK dispatch

Independent bounded execution accepted Mars msg_30c1/f32595cb; see
independent-execution.md. Earlier execution-pending text below is historical.
Export pins/false flags/defaults stay unchanged; pooled release still pending.

RUNTIME-004 scope revision2. Bounded scope accepted Mars msg_c9ef /f3b991a;
independent artifact/CPU execution pending. Separate candidate atop accepted
analoga6c406e4. Keypad evidence req_72f0 completed without chip changes. This service dispatches actual CPU interrupts, not device scanning,
IRQ source polling/acknowledgment, timers or historic firmware compatibility.

## Original development callback ABI

Hardware IRQ/BRK vector points to irq_classifier FD00. Preserve A and X using
PHA/TXA/PHA, TSX, three INX, then LDA0100,X to inspect the stacked status byte.
INX wraps in eight bits, so the load stays within page0100 even when the hardware
frame/saves cross01FF/0100. Do NOT substitute LDA0103,X with an absolute-indexed
page crossing. AND10 selects the hardware-stacked B bit:0 IRQ,1 BRK. Restore X
and A from the two saves before JMP indirect0200 (vinter IRQ) or020E (vbreak BRK).
Y is untouched. Callback receives original A/X/Y and only the real hardware frame;
live flags scratch, I hardware-set, D retained. Own register saves must balance,
and callback finishes RTI, not RTS or JMP vbi_exit. RTI restores meaningful P bits
and hardware PC. Ordinary IRQ resumes normal interrupted PC; BRK resumes opcode
address+2, not+1. Runtime never edits saved P/PC or skips a BRK padding byte itself.

The two software slots retain existing cold FC86 startup_fault defaults.
Mars reports that destination as Metadata, while FC83 irq_fault is IRQ;
uninstalled-slot diagnostics must distinguish it from older unconditional faults. Cart
must install valid handlers before CLI/BRK, with interrupt sources disabled and
quiescent CPU-pending NMI/IRQ state as the fixture requires. No extra startup
writes, IRQEN enable or POKMSK shadow propagation. Runtime IRQ dispatcher reads
no device status, masks no source and writes no device acknowledgment; handler
owns explicit source handling/ack before RTI or the real CPU may retrigger. No
priority, implicit IRQST read-to-ack or keyboard repeat/held validity assumption.
Other source-specific vectors remain unsupported until their own contracts exist.

Cold I remains set. Masked queued hardware IRQ may remain pending normally while
Ready, unlike an unaccepted CPU-pending NMI at handoff; don't discard it or force
an IRQ failure merely because I prevents entry. BRK can execute with I set and
must still route BRK. NMI can hijack interrupt selection in real CPU execution;
classify only the stacked B bit on an actual IRQ-vector path, not immutable
source provenance. Nested/overlapping IRQ/NMI, recursive vectors, corrupt stack,
callback-modified hardware frames and arbitrary held sources are unsupported.

## Allocation and static targets

FD00..FD19 classifier26 bytes fits remaining FC80..FD3F interrupt allowance;
prior51 becomes77. Total1410/2048,638 free including250 untouched margin; input53,
startup127 and all previous services unchanged. Hardware IRQ vector changes to
FD00; old irq_fault FC83 stays an explicit exported fault destination. No extra
RAM or persistent state. Maximum dispatch stack5 including3 hardware bytes and
2 saves; callback entry3, total5 stack writes, arbitrary callback/nesting separate.

IRQ dispatch39 base cycles/14 instructions; BRK route40/14. All branches same
page and load base0100 cannot page-cross. Hardware entry7 and callback/RTI
excluded. Proposed full dispatch target128 under DMA-off ordinary refresh, not
held RDY. No previous startup/VBI/DLI static costs change. Actual fixture timing,
stack/state/source/callback execution needs independent Mars acceptance.

## Independent acceptance

- Install distinct original IRQ/BRK callbacks; real timer/allowed IRQ source and
  original CPU BRK00 with distinguishable padding and continuation markers.
  Verify each routes its slot, original A/X/Y, real stacked B/PC/P, balanced saves,
  RTI return, no extra clock/analog/display/device work. Cold untouched slots fault.
- Test all256 interrupted stack positions independently (runtime uses only its
  two saves), rotating A/X/Y and I/D/meaningful status combinations; SP00..05 and
  FC..FF explicitly cover hardware/software stack wrap. Callbacks use only cart
  scratch plus their declared saves and source acknowledgment. Compare real bus
  stack writes and software-vector reads, no host PC or callback substitution.
- IRQ masked/unmasked/pending and explicit ack/retrigger; BRK with I0/I1; no
  guessed device status acknowledgment by runtime. Keep NMI disabled for bounded
  classification fixtures, then separately nonoverlapping VBI/DLI coexistence.
  Early/hijacked/nested placements labeled synthetic/unsupported; existing
  Starting interrupt/handoff observer must retain actual no-false-Ready rules.
- Synchronize at actual safe points around saves, status read, restore/dispatch,
  callback and RTI; same/fresh/process replay and strict mutual analog/new-state
  identity refusal. Host input/residual before native import remains required.
- Repeat analog8axis, VBI/display/DLI, metadata/startup/reset/lifetime/defaultOFF,
  R65 controller and converter negatives, Release/nonunity ASan and firmware
  regressions. No keypad/fire/timer service or full game/reference claim.

## Evidence boundary

CONSUMER-01 supplies0200/020E field declarations only. CPU-02 manufacturer manual
section9.7 supplies stacked B/BRK+2/IRQ distinction; existing opcode facts reused.
Synertek1976 transcription reviewed selected chapter9 prose and nearby example
visible; example not copied. Our wrapping stack-index calculation, dispatch ABI,
source-handling separation and fixtures were designed before that review. No
Atari BIOS/disassembly/kernel/foreign emulator/test or instruction trace read.
