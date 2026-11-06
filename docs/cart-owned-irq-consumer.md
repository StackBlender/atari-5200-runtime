# Application-owned IRQ consumer and ordinary-layout review

This is a concrete original software consumer of the released timer ancestor,
not an implementation of a historical BIOS keyboard routine. It narrows the
missing B requirements without assigning semantics to names such as vkeybd/vkeypd.
The executable remains an explicit diagnostic. No ordinary profile is admitted.

## Evidence and distinction

The official cc65 platform document, reviewed2026-11-06, sections3/4.2/5.3/6.1,
describes application RAM021C..3FFF, public hardware access, a standard joystick
driver and console display. It does not specify a keyboard IRQ callback ABI:
source ownership, raw-code delivery, ACK/rearm and return convention are absent.
This is a limit of the reviewed document, not proof that no existing game needs
those services. No compiler driver/startup/kernel/macro implementation was read.
[Primary consumer prose](https://cc65.github.io/doc/atari5200.html).

An ORIGINAL consumer now supplies its own complete IRQ contract below. It runs
on unchanged timer sourceac9b47e50c213b08022e78bdef64662569cd3d29/image
eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550, released MR43.
Only the public genericIRQ0200 layout/return contract and screened Mars keyboard
interface prose are used. No runtime/private input data at0600..061F is required.
This shows what THIS actual cartridge needs; it does not establish existing
stock cc65 or historical BIOS compatibility by declaration.

## Actual required contract

|Requirement|Original consumer behavior|
|---|---|
|Board/entry|Explicit original Linear32K; digit metadata and entry8000; cold reset only|
|RAM|Runtime existing public shadows0000..18/vectors0200..21B; shared CPU stack0100..1FF; application owns0019..FF/021C..3FFF, proposed cession021C..21F is separate review|
|Private application fields|3000..301F only; not a runtime reservation and not0600..061F|
|Dispatch|CPU installs0200=8400 while IRQ/NMI disabled; generic runtime classifier reaches cart handler with hardware frame only, temporary A/X already removed|
|Sources|Cart enables keyboard40 only; timers/Break/serial remain disabled. BRK is not invoked in this consumer|
|Entry/exit|Cart handler preserves its own A/X/Y, uses no ZP scratch, balances saves, RTI. It does NOT JMP FCB0, which expects the runtime's saved-register frame|
|Source validation|Cart reads IRQST E80E, inverts/ANDs its coherent POKMSK00, requires40 plus application phase2 and no prior valid capture; canceled entry returns normally|
|Read/normalize|First accepted handler reads raw KBCODE E809 into private RAM, derives(code&1E)>>1.1..15 are valid;0 is flagged invalid. RawFF is not treated as a no-contact sentinel|
|Publish/ACK|Raw/code then valid, increment application capture count; clear POKMSK/IRQEN coherently. No second capture overwrites this armed latch|
|Rearm|CPU mailbox first SEI/mask-off+ACK, select CONSOL04|port, phase1/clear valid/code; two ordinary runs settle. Separate command sets phase2/mask40/IRQEN40, then CLI|
|Scanner|Cart chooses continuousSKCTL06 AFTER startup; no per-window reset. This is consumer policy, not a provider default or a slow03 compatibility claim|
|VBI|Default VBI enabled40, CRITIC00/01 exercised. Default VBI must not modify this cart's selector/mask/phase; arbitrary custom NMI mutation/nesting is outside scope|
|Host/state|Host contacts staged before native import; next host interval after import. Retain ordinary frame returns/polls, real serialized caches/stacks, no forced quiescence|
|Release|Latched capture remains after release; a freshly rearmed empty window records no IRQ capture. No automatic release event, chord/repeat/FIFO/short-tap or universal physical-release claim|

This uses hardware IRQ delivery plus a cart-owned dispatcher. It does not call
0208/020A or require the runtime to interpret them. Native keyboard40 reaches
the installed0200 handler; the old timer default unsupported40 branch is never
selected in this consumer. No change to that default or its fail-fast policy.
Three cart register saves are additional to the hardware frame; default VBI
can preempt it, but arbitrary arrival positions/allSP/reentrancy are not claimed.

## Completed native consumer coverage

Retro-owned tests atari5200_cart_irq.hpp and check_5200_cart_irq_process.py author all code/
expectations without reading native implementation; this is the same maintaining actor, not an independent reference-role split. Public standard Controller
button names match #/0/*/Reset/9/8/7/Pause/6/5/4/Start/3/2/1 in normalized order1..15.
All60port/contact cases have different canary seeds; CRITIC alternates across
cases (30each), not120fully crossed cases. Other three ports hold a different
contact, checking selected-port isolation. An empty selected window, first press,
held latch after release, fresh empty window and repress are checked explicitly.
Marker3005 changed to5A after entry must remain5A; input must not rerun startup.

16043guard bytes cover0019..FF and021C..3FFF except3000..301F; initialize after
accepted cold whileStarting/instructions0 before startup, including conio and
0600..061F.60same-root+60fresh-root continuations and60writer-exits/reader process
continuations require full native byte equality. Before EVERY valid import all
protected target bytes are inverted, then checked immediately after import before
frames. No physical-store observer is supplied by this consumer; the separate
Mars350b508 exact-parent bounded store audit remains separately attributed.

Process reader480refusals cover wrong original-ROM unused byte, fourth-port
Trak-Ball, checksum/short/extended states and unsupported reset3. Each preserves
full native state AND the next two ordinary-frame continuation. These are topology
refusals, not Trak-Ball gameplay. AR52KI01 diagnostic framing has8byte magic,
LE32 count60,40ASCII source/64ASCII image, record port/key/seed/CRITIC/4host codes,
then two LE32-length-prefixed native blobs; max8MiB archive/1MiB state. Entire
archive identity/provider/case/host/length/trailing preflight before native load.
Independent Python checks60records,16archive and1CLI refusals. No native layout
is decoded;17598byte snapshots are observations of four standard Controllers.
Temporary archives removed automatically; no third-party game bytes committed.

Timer selector now registers15checks, including cart IRQ native/process tests
alongside previous timer/BRK/process and2600 regressions. Full Release15/15 and adapterASan/UBSan15/15 PASS; final configuration recorded
in handoff. Native Mars
remains Release uninstrumented even when adapter/header code uses ASan/UBSan.
No original hardware, historical encoding/boot, game, device or online claim.

## B0 proposal for review, not an emitted profile

Review a separately named ordinary-layout DEVELOPMENT profile for consumers that
own0200 dispatch as above, on exact qualified timer parent. Explicitly cede
021C..021F to application and leave0600..061F unreserved; maintain public shadow/
vector/shared-stack boundaries. No mandatory cooperating input-v2/v3 tag should
pretend this application reserves hidden input RAM. Require explicit board and
actual supported software contract, not size alone or a blanket cc65/game claim.

This consumer requires no BIOS key callback, release/repeat algorithm or extra
runtime state. The existing generic classifier and default VBI/analog services
suffice for it; application owns scanner/IRQ programming. Other software may
require different services and remains unresolved. A descriptor/profile/source/
version-bound identity must separate this future target from old conservative
profiles, even if its ROM bytes remain identical. Preserve all13old exports,
old reservations/identities, flags/capabilities/defaultOFF, native schema and
strict pre-mutation refusal+ordinary continuation. Timer parent is1504written
with250reserved margin; do not apply fire-v3's90byte reserve figure to it.

Review questions: is this implemented consumer sufficient for bounded B0
profile authoring, with broader legacy/cc65/game compatibility still open? If a
previously existing software consumer is mandatory instead, identify that as the
remaining gate rather than treating an undocumented BIOS callback as known.
No profile/descriptor/image was emitted under this proposal.

## B1 real-homebrew startup requirement, separate review

The locally authorized author-published homebrew corpus was screened only for
packaged length/hash and metadata eligibility; no game implementation/disassembly,
font or BIOS was inspected. One5200image requests the second-year-byteFF
diagnostic flag and a valid existing entry range; numeric metadata admission
fails. Its identifying hash/source/results stay under ignored tests/local.
No cartridge was run, patched or falsely declared cooperating. Opaque-title and
font qualification do not authorize FF handling. Source-specific details are
available locally for reproducing admission, not in this tracked aggregate.

Official consumer prose7.2 says that flag bypasses splash and most initialization,
but supplies no complete preserved/initialized-state contract. A separate lawful
original diagnostic cold policy could intentionally retain the existing reviewed
cold initialization and allow that flag/opaque title before normal CPU entry;
that would NOT reproduce or silently claim the documented BIOS bypass semantics.
It requires explicit policy/numeric-path/fit/state review before emission and
actual unchanged-game validation afterward. It must never become a host PC jump
or concealed metadata mutation. Review whether to author this explicitly named
experimental cold policy or first obtain a fuller diagnostic-entry requirement.
Either choice keeps historical/ordinary-game compatibility unproved until tested.

Retro final keypad Release regression13/13 PASS; same existing third root
restored Release/keypad-irq with sanitizer flags empty. Earlier keypadASan13/13
retained, not rerun for timer-only additions. No extra roots/devices/Fable.
