# Build tools and runtime boundary

## Current deliverable

RUNTIME-001 is an original Python emitter and an image-layout fixture. It has no
CPU execution engine, Atari software ABI, runtime services or emulator dependency.
Its output is tagged `purpose=emitter-layout-test-only`, `runtime_abi=null` and
`capabilities=[]`. It is not the proposed sb5200-runtime-image provider.

The explicit 29-entry instruction/address-mode subset is in tools/emitter.py.
It emits only the requested mode: no inference, relaxation, undocumented opcode
or CMOS extension. Implied, immediate, zero-page, absolute and relative modes
have explicit operand rules. Relative displacement is measured from the byte
after the operand and must fit -128..127. Absolute operands are little endian.
Generic CPU encodings do not settle Atari cartridge/reset/service conventions.

Image allocations must cover exactly F800–FFFF, with nonoverlapping named
code/asset/reserved/vector ranges. Writes cannot overlap or cross an allocation;
reserved allowance cannot be written. Symbolic JMP/JSR/branch and vector targets
must identify emitted instruction starts. Symbolic data operands must identify
written bytes. Unknown labels, missing vectors, branch overflow and unsupported
instructions fail; values never truncate or wrap silently. Failed emission does
not write a partial instruction; finish resolves into a fresh buffer.

## Fixture allocation (tool-test policy)

| Range | Allowance | Written | Purpose |
| --- | ---: | ---: | --- |
| F800–F83F | 64 | 4 | Original self-loop and RTI encoding fixture |
| F840–FFF9 | 1978 | 0 | Reserved, not a claim that services will fit |
| FFFA–FFFF | 6 | 6 | Generic CPU NMI/reset/IRQ vector encoding |
| Total | 2048 | 10 | 2038 unused bytes |

The two handlers are deliberately just tool fixtures: no cart handoff, hardware
initialization, RAM allocation, stack initialization, software dispatch or font.
No Atari default/register/keypad/vector-table values are embedded. No emulator
should select this fixture as a runtime. Fill FF is our padding policy and has
no evidentiary meaning about manufacturer ROM contents.

The map JSON has stable schema version 1, image hash/size/origin/fill,
used/remaining totals, sorted symbols and per-region allocation/usage. No time,
absolute checkout path or host-specific identity affects output. The fixture's
schema is a tool report, not a stable runtime descriptor ABI or release manifest.

## Required runtime contract

A supported runtime still needs an approved numeric software ABI/evidence matrix
for startup/cart entry, reset variants, RAM/shadows/vectors, NMI/VBI/DLI, IRQ/BRK,
clocks, input scanning, POKEY interactions and original font encoding. For every
claimed row: permitted source or probe ID, exact postcondition, independent
fixture, confidence and unsupported cases. [Startup evidence](startup-evidence.md)
now records primary documentary cartridge-area/reservation facts, revision history
and remaining gaps. These are not measured retail ABI or implementation approval.

The actual code/font/vector/free-space budget must follow those requirements,
with all RAM/stack ownership declared. Generic CPU stack addressing is not a
license to choose an Atari reset stack policy. Overflow stops for review rather
than truncating, stealing RAM or assuming extra banking. All claimed services
and assets must ultimately fit together; the tool fixture proves no such fit.

Planned integration keeps ordinary CPU/reset/interrupt/chip execution in the
emulator. The app explicitly selects an available original provider; it never
fabricates a BIOS pak or falls back silently. CPU reads, debugger peeks and ANTIC
DMA must agree. Replacement states bind immutable profile/version/image identity
and refuse mismatches before mutation; raw replacement stacks are unsupported.
These interfaces and save layouts are proposals for future integration review.

## Diagnostic tooling

[ENTRY-01 protocol](entry-observation-protocol.md) specifies an original 26-byte
capture fragment and bounded scalar-record validator. `fixed_instruction` shares
the emitter's fixed numerical-operand encodings; symbols remain the image
emitter's responsibility. Four entries added: absolute STX/STY, implied PHP/TSX.
The fragment is not a complete cartridge, runtime image or execution approval.
Its configurable result area and stack use require review; no metadata encoder
or MMIO defaults are invented. Synthetic tests establish byte layout, identity,
normalization, format rejection and inconclusive handling, not CPU execution.
