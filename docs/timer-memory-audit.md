# Conditional timer ancestor memory audit

Mars1afec85/f20996c review permits B audit only, not a new ordinary-software
profile or keyIRQ implementation. This tool inventories our exact qualified
original timer image, sourceac9b47e50c213b08022e78bdef64662569cd3d29,
SHAeae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550.
No old generation source/image/profile or runtime behavior is changed.

## Static method and conditional result

`tools/timer_memory_audit.py` uses an independently written narrow factual opcode
length/address decoder, not the emitter's opcode table. It traverses both branch
arms, calls/fallthroughs, hardware vectors and startup-installed default software
handler routes.220instructions cover all474emitted code bytes; every remaining
FC00..FEFF byte must beFF padding. Font/vector/padding are not decoded as code.
Unknown opcodes, out-of-range flow, overlapping instruction/operand targets,
unreviewed calls/pointers and indexed accesses without an exact guard fail.

No registers, flags, memory, chips or cycles are executed or simulated. Exact
startup loop patterns supply manual finite-index proofs: zero-page X24..0,
vector evenX0..26/oddX1..27, metadataX0..21; stack index is an8-bit value. The
service initializer bytes are also guarded, establishing default software routes.
The public CLI requires the complete qualified image hash; the internal analyzer
is exposed to synthetic corruptions only by tests. These are conditional facts
of this immutable original program, not a general static data-flow theorem.

|CPU operand/implicit stack area|Conditional footprint|
|---|---|
|RAM writes|0000..0018,0100..021B|
|RAM reads|0000..0003,0005..0010,0100..0207,020E..020F,0216..021B|
|Application021C..3FFF|No explicit runtime CPU operand reads/writes|
|cc65 conio0019..001C|No explicit runtime CPU operand reads/writes|
|Stack|NMOS0100..01FF; hardware interrupt/JSR/PHA and return/pull effects included conservatively|
|External pointer frontiers|0200/0202/0204/0206/020E/0216/0218/021A/BFFE|

Writes above RAM are only declared startup/display/analog/timer/NMI MMIO aliases;
all addresses are enumerated in JSON. INC clock RMW affects only0001/0002,
including its old-value write. No application RAM is borrowed for hidden state.
The write range0100..021B joins hardware stack and adjacent public vector bytes;
it does not authorize data outside either area or prove callback stack depth.

Consumer callbacks/cart code, their stack balance, direct jumps into routines,
core cold-power/randomization and chip DMA/bus dummy cycles are explicit external
boundaries. Only legitimate reviewed entries/returns and protected-loop invariants
are assumed. This is not an all-software/bus/power preservation or execution proof.

## Independent startup/VBI consumer evidence

Retro's original timer diagnostic now seeds15837canaries AFTER accepted core
cold power/randomization while public runtimeInfo isStarting with zero observed
instructions, BEFORE startup executes. The range is021C..3FFF excluding its
seven cart result/counter bytes3000..3006;0600..061F is included. Checkpoints
confirm all canaries survive actual startup, then live CPU-enabled VBI and
same/fresh-root continuations. Host input remains staged before native import.
No input-v2 assertion or new native profile is used. Release12/12 and adapter
ASan/UBSan12/12 pass; native Mars remains Release/uninstrumented in those runs.
This expands the earlier post-entry-only canary evidence. It is not preservation
of RAM across power-on itself, all native IRQ/DLI/fault paths or an actual game.

## Reproduce and remaining gates

Generate the OWN original program, then analyze it; never supply manufacturer
firmware or an unrelated program:

```sh
python3 tools/timer_dispatch_image.py --output-dir build/timer-audit
python3 tools/timer_memory_audit.py build/timer-audit/timer-dispatch.bin
```

Six tests cover220instruction/474byte coverage and exact footprints, altered
loop/default-vector guards, forbidden app RAM store/read, unknown opcode/branch/
call/pointer, exact image admission and fresh CLI reproducibility/refusal.
188offline methods/CTest1/1 PASS, retaining all eleven old export/CMake and
opaque-title candidate artifact checks. No CPU emulator or foreign test/code.

A separate proposed consumer-interface profile still must EXPLICITLY cede
021C..021F; older profiles' conservative reservation is unchanged. Audit/qualify
all native startup/IRQ/VBI/fault paths and consumer-owned display/stack cases.
Supply the actual required keyIRQ source/mask/ACK/rearm/rawcode/vector/entry/
return/clobber/nesting/RAM/state contract from screened prose or authorized
consumer observations. Direct hardware input and optional BIOS callbacks are
different requirements. Do not relabel unrelated cartridges as cooperating,
claim ordinary-game compatibility or infer an approved profile from this report.
