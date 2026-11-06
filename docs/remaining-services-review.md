# Reset, remaining services and next fit review

RUNTIME-004 continuation after independent both-fire qualification4e6a3a5.
The accepted development program is a2a7455/imagee937064b, not a complete retail
BIOS replacement. This inventory separates demonstrated original policy from
unresolved compatibility requirements; it does not infer missing routines from
unexplored ROM contents. No manufacturer firmware, disassembly or producer
implementation/tests were read. Existing documentary/consumer ledgers are inputs.

## Current service inventory and closure work

|Area|Current exact behavior|Remaining closure artifact|
|---|---|---|
|Cold power|Reviewed reset-vector startup, declared writes/32-byte reservation, metadata/handoff, fail-stop and watchdog; independently qualified|Actual product cold-reset UX/state lifecycle, broader cart and device acceptance|
|Warm/CPU-only reset|Explicit pre-mutation refusal in development provider|Permitted behavioral/reset-entry/preservation requirements before implementation; never silently map to cold or direct-PC jump|
|Controller Reset/Pause/Start|Contacts4/8/12 respectively in the reviewed normalized keypad mapping; change callbacks and source limitations|Cart owns semantic actions in current ABI. Explicit diagnostic and software-consumer expectations for held/release/repress; no automatic CPU reset/pause/restart claim|
|IRQ/BRK/timers|0200/020E dispatch and three timer callbacks with reviewed return/mask policy|Additional documented consumers/edge cases; rates and hardware programming remain cart-owned|
|Break/serial sources|Default supported IRQ mask47; unsupported B8 faults before source ACK; unused020C/0210/0212/0214 slots remain fault defaults|Document which Break/serial services software needs; exact source/ack/vector/return policy, emitted fit and independent probes before adding them|
|NMI/VBI/DLI/shadows|Clock before CRITIC; existing declared callbacks/display/analog/fire/window policy qualified|Final/retail VBI ABI is not established by interim PAM memo; compatibility evidence and real-cart validation|
|Input|Four-port analog/keypad/both fires for explicit cooperating input-fire-v3; bounded aged observations and silent baselines|Actual consumer/touch/device/multiplayer acceptance, short-tap/chord limits and authorized game tests|
|Attract state|0004 is initialized; no attract update/color transformation implemented|Permitted behavioral requirement plus explicit visual/game policy; avoid inventing a rate/threshold|
|Cartridge entry/metadata|Explicit Linear32K,22 decimal digits50..59, BFFE entry4000..BFE7, no optional init/FF bypass|Screen lawful software-consumer/primary encoding/layout evidence, supported board and real source mapping; do not accept arbitrary games by size|
|Character assets|Original128x8 bank atF800; only ten digit glyphs50..59 drawn, other glyphs blank|Original broader glyph repertoire and independently supported encoding/ANTIC/inverse behavior, no extracted font or logo|
|Sound|Ordinary POKEY is cart-controlled; reviewed startup volumes and owned IRQ writes; no independent music service|Actual cartridge audio/listening/game compatibility. A music-isolation feature is not proved by BIOS/native sound|
|Memory/stack|Public shadows/vectors plus0600..061F cooperating reservation; tested bounded14/20-byte nested programs|Noncooperating/oldcc65 RAM compatibility, explicit callback depth and any new state/version contract|
|States/frame boundaries|Safe repeated/fresh/process native replay including stale cache and mid-VBI ordinary frame return qualified|Actual frontend host-input/cache/conversion ordering and online snapshots; never forcequiescence at a frame boundary|
|Hardware/profile|NTSC four-port development/cooperating profile|Other boards/ports/region policy and documented compatibility differences; board identity is not a measured firmware revision|

This is not permission to discard unknown requirements and declare completion.
Every remaining compatibility row needs screened evidence, an explicit chosen
contract, independently authored acceptance and actual fit. A supported subset
must keep an honest name; full completion requires resolving the intended game/
software requirements, not only passing our cooperating diagnostic.

## Next reset evidence/contract request

Ask integration owner to review these reset distinctions before new reset code:

1. Keep repeated full cold power as the existing supported restart operation,
   with ordinary reset-vector execution and no hidden warm-to-cold conversion.
2. Keep physical Controller Reset contact4 as input, including held/release/
   repress and independent port ownership. Our current ABI leaves its semantic
   response to the cooperating cartridge. This is NOT a claim about historical
   firmware/controller reset behavior or that no further service is needed.
3. Identify a permitted software-consumer/primary behavioral contract for any
   additional warm/CPU-only/Break reset entry: trigger, real hardware path,
   preserved versus reinitialized RAM/chips/stack/handlers/cart identity, audio/
   scan/IRQ interactions, error outcomes and synchronized state implications.
   No new numeric entry or reset-default constants should be guessed.
4. Independently exercise held Reset/Pause/Start across cold/reopen/ordinary
   frame return and snapshots. Reset refusal is not an input-event receipt;
   existing all-contact native matrices are distinct from game semantics.

The reset/API assessment should identify missing evidence or a concrete next
contract, rather than introducing a host firmware service. Additional named
services will be sequenced from the table with the same source/fit discipline.

## Measured standalone refactor proposal

Accepted fire-v3 uses1902/2048,398 above timer1504. Its1904 ceiling leaves2,
153/160 fire code,90 reserved and56 ordinary fragmented free. None is permission
to emit a reset/remaining-service extension. Existing ten generation inputs,
allocations/profiles and export identities must remain immutable.

Original tools/fire_callback_refactor.py emits only a146-byte NONRUNNABLE
alternate fragment plus JSON at syntheticF800, compared with accepted153.
It moves the duplicated LDY061B/TXA/LDX061A argument setup into the existing
fire_callback_bridge immediately before JMPind0208. Each caller now uses a
single JSR to that bridge. It adds no helper JSR, push or persistent RAM.

|Measure|Accepted/proposal|
|---|---:|
|Two caller setups/calls plus bridge|23 ->16 bytes|
|Standalone fragment|153 ->146 bytes|
|Argument setup cycles|4+2+4=10, unchanged nominal total|
|JSR/setup/JMPind per callback|21 nominal cycles, unchanged sum|
|Additional stack beyond existing bridge|0|
|Projected cumulative written|1902 ->1895 (not emitted)|
|Projected extra above1504|398 ->391|
|Arithmetic headroom under1904|9, not permission for a new service|
|Projected ordinary fragmented free|63; reserve90 unchanged|

Synthetic offsets bottom0, top74, bridge136; proposed FF00 placement would be
bottomFF00, topFF4A and argument/indirect bridgeFF88..FF91. Near FC96 and changed
key tail must route to the new topFF4A; bottom continuesFD1A, topFD59. No actual
cumulative relocation/map/provider has been emitted. Fragment SHA256
3ed9e71084486c4ad3448f834f2ba82dac37a7ba2346b374d096a9b72bc3c484.

Moving setup inside the existing bridge preserves the intended Aport/Xold/Ynew
entry convention: X is still the loop/selected port until TXA; JSR itself does
not clobber it, and LDY does not change X. Old/new bitmap stores/baselines and
post-callback index reload remain. Final callback N/Z still follow LDXold.
Callbacks may scratch flags; original IRQ/VBI return frame rules remain.

This is a static proposal, not proved machine equivalence or a global cycle
claim. Branch placement/page-cross costs, JSR return addresses, live frame-boundary
positions inside the bridge and serialized stack differ. Preserve ordinary
System::run post-return polls, permit actual mid-VBI capture, and requalify all
native cache/phase/NMI/allSP14/20byte/callback/timer/analog/process/converter paths
before accepting a refactored image. No Event::Step-forced quiescence.

Request bounded review of THIS refactor only, preserving the160/90 allocation and
1904 ceiling. New full generation/profile/tuple and exact old/new state refusal
are required if authoring is approved. No new ABI or native field is assumed;
the complete new image/descriptor/source identity must separate states. Additional
reset/services need their own numeric contract and measured cumulative proposal;
this seven-byte saving does not establish their fit. Do not spend any reserve.

## Offline verification

Five methods bring160 total: independently expected all146bytes/branches and
bridge argument preparation, arithmetic/zero-extra-stack claim, no approval
inference, fresh-process outputs, unchanged accepted153-byte fragment/image and
90-byte reserve. No CPU or chip execution engine was added. CLI:
`python3 tools/fire_callback_refactor.py --output-dir build/callback-refactor`.
Only two ignored fragment files are emitted; there is no full provider target.
