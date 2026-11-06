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

The default-route graph assumes initialized default software vectors. It does
not prove early/hijacked startup interrupt safety or torn/uninitialized vector
routing; those depend on the integration startup observer and native tests.
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

### Proposed ownership reconciliation (not a selected profile)

For the separate ordinary-consumer target, propose the following explicit policy:

|Area|Proposed owner|
|---|---|
|0000..0018|Existing declared runtime shadows only|
|0019..00FF|Consumer, including cc65 conio0019..001C|
|0100..01FF|Shared hardware/call/interrupt stack under the eventual callback ABI|
|0200..021B|Existing declared public vector table only|
|021C..021F|Explicitly CEDED to the consumer in this separate proposal|
|0220..3FFF|Consumer code/data/heap/display;0600..061F is NOT reserved|

This deliberately reconciles the compiler layout by changing the reservation for
that future target, rather than claiming the old conservative PAM profile already
cedes the four bytes. The static own-code inventory supports the proposed cession;
it does not establish historical ownership or approve its implementation. No new
profile identifier/provider/manifest/selection or executable policy is created.
Its actual keyIRQ consumer requirements remain unfilled; no hidden state or
callback/repeat semantics may be invented to complete the table.

A separate proposed consumer-interface profile still must EXPLICITLY cede
021C..021F; older profiles' conservative reservation is unchanged. Audit/qualify
all native startup/IRQ/VBI/fault paths and consumer-owned display/stack cases.
Supply the actual required keyIRQ source/mask/ACK/rearm/rawcode/vector/entry/
return/clobber/nesting/RAM/state contract from screened prose or authorized
consumer observations. Direct hardware input and optional BIOS callbacks are
different requirements. Do not relabel unrelated cartridges as cooperating,
claim ordinary-game compatibility or infer an approved profile from this report.

## Next independent B boundary audit

Request native-owner Release/full-nativeASan evidence on the exact unchanged timer
ancestor ac9b47e50c213b08022e78bdef64662569cd3d29/image
eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550.
Audit-only, no new ordinary profile or keyIRQ implementation: seed consumer RAM
021C..3FFF including600..61F after cold power randomization and before startup;
exercise valid startup/entry, metadata and entry refusals, initialized default
VBI/DLI/analog/IRQ/BRK/timer and supported bounded callbacks/fault paths. Declare
all cart-owned code/display/result writes separately; inspect unexpected physical
CPU stores rather than inferring preservation from final bytes alone. Cover
ordinary frame/mid-service safe and separate-process continuations with genuine
poisoned target RAM before native import and pre-mutation refusal continuation.

Report exact tested vector initialization/observer/stack/callback assumptions,
unsupported early/torn/custom routing and uncovered boundaries; a failure or
unprovable boundary is evidence, not permission to repair/emulate/invent services.
No claim of RAM preservation through power randomization itself, arbitrary
callbacks, BIOS equivalence or ordinary-game acceptance. Existing timer profile
ownership and unsupported keyIRQ behavior stay unchanged. This independent B
coverage can proceed while actual consumer keyIRQ requirements remain unresolved;
all profile/provider authoring still requires the separate explicit contract.

## Retro-owned timer/BRK consumer receipt, 2026-11-06

Retro source8e590a6 completes a consumer test extension on RELEASED MR43 timer
sourceac9b47e50c213b08022e78bdef64662569cd3d29/image
eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550.
This is reported first-party consumer evidence by the same runtime maintainer,
not a separate observer role, original-system measurement or the requested Mars
all-native-boundary/physical-store audit. No runtime generation input changed.

Ten original cases cross timer masks00/01/02/04/07 andCRITIC0/1; real CPU installs
bounded callbacks, programs rates/STIMER/coherentPOKMSK+IRQEN, enables VBI and BRK.
Cart-owned mailbox masks/acks then restarts timers; active sources count, masked
sources stop after ordinary settling, while CPU/BRK/VBI continue. No host MMIO/
PC/source injection, input declaration, new service/profile or timer rate claim.

16043canaries cover0019..FF/021C..3FFF except cart results3000..301F, including
conio0019..1C/600..61F. Seed after cold randomization Starting/instructions0,
before startup. Thirty repeated same-root/ten fresh-root plus ten separate writer-
exits/reader process continuations compare full synchronized native state; every
successful import inverts target canaries first and checks immediate restoration
BEFORE frames. Saved HOST contacts before import, new contacts after; real ordinary
returns/polls/stacks/caches retained, no forced instruction/interrupt quiescence.

Process reader100refusals: different unused-ROM byte, fourth-portTrak-Ball,
signature/version/checksum/short/extended native state and unsupported reset3.
Each preserves complete native state AND next two ordinary-frame continuation.
Independent AR52TM01 framing checks ten cases/exact source+image and14badarchive/
2CLI refusals, whole-file preflight before machine load. State17598bytes observed
for four standard Controllers, not a universal layout. Temp archives removed.

Timer Release13/13 +adapterASan/UBSan13/13 PASS; keypad regression Release13/13
+adapterASan/UBSan13/13 PASS. Native Mars stays Release UNINSTRUMENTED, so not
full-nativeASan. Existing third consumer root restored Release/keypad-irq,
sanitizer flags empty; no new build root/device/Fable/thirdpartycartridge/firmware.
The older15837-byte startup/VBI baseline remains separate and included.

Final-canary/replay checks cannot expose every transient CPU store. Early/torn/
custom-vector/startup-observer/allSP/DLI/fault/physical-store coverage remains
Mars-owned audit work; no power-on-content, arbitrarycallback, ordinary profile/
keyIRQ/historicalABI/game/device/multiplayer claim. Explicit future021C..21F
cession and actual consumer keyIRQ requirements still gates; old conservative
profiles unchanged. FullR62req_6f74 OPEN/noACK, MR43latest/app pins/defaults/false
flags unchanged. Runtime offline197/13export evidence unchanged (not rerun for
this documentation-only receipt). Next B native audit already requestedmsg_4005.
