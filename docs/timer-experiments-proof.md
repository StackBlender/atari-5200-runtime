# Separate ordinary RAM and original diagnostic cold experiments

## Exact separate B0/B1 export receipt

Both source/export pins: becb92e01e97e89568cac58ab051e23b803ae53a.

|Artifact|B0 ordinary RAM|B1 diagnostic full cold|
|---|---|---|
|Image SHA256|eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550|9da1ddefb339dc2ef3f93643d33b45021099d3fd3256ce1f9754f32787e6b69f|
|Map raw SHA256|620f145e981826e9a31c059b605fd234c72cb75f44b6da56465aa4d810d85981|11c2cf69a819d46aa32d3cca0d7901d9cd3414ff82995c09d9e09e847aa99b07|
|Map semantic SHA256|ef3a00eacea84816536e749fda0412097f3f654e89ccec86a7e6f164e4c4b4e6|97289c8e7000bada80b66b9b11d9b10f3801c7bf325b28957b3cbb44d0f8a51b|
|Manifest raw SHA256|b80652692fcf601c8b5239f1fd40b3c4405efa590cd96250f9c9b7b90ab3f37d|3c993b60a7a57a1acddcb21a63e77a30f4e4e28a4e85785d708adfdcc5165929|
|Manifest semantic SHA256|86c68580f163ea829f89cb163ad64ebafe3170b7ec80a6b25c48489021668b4b|ea3d40791f74f3eec669bf57a780e954d969fef1988de3c37ec51f9a5544078f|

Semantic hashes: sorted-key compactJSON comma/colon UTF8/no trailing newline.
Eight new methods bring205offline +build/CTest1/1 PASS, including both exact
committed CLI/CMake consumers:4absolute properties/fullsource/dependency ordering/
triple byte equality. Separate temporary parents removed; existing build only.
All13previous qualified exports still checked. Neither candidate is added to the
qualified catalog until independent native admission; same-image B0 identity
MUST be checked independently of its byte equality. No game/pin/default/flag move.

New exact-policy corpus eligibility check: the authorized image also has a
NONNUMERIC FIRSTyear, so approved B1 does NOT admit it despite allowed secondFF.
Image unchanged/unrun; identifying data and boolean classification stay ignored.
No relaxation to B1 was made. Any separate B2 proposal allowing opaque firstyear
ONLY when secondFF requires explicit review/new identity/qualification; do not
silently change the approved firstnumeric invariant or infer historical bypass.

Mars81025cfddd64502c276e0a8895cdc96f9b0249fc/msg_993d (req_6f74) approves
BOUNDED AUTHORING, not native/provider admission or a game trial. Read only owner
prose a52-cart-owned-profile-review.md. No native implementation/tests, BIOS,
foreign kernel/font or third-party game code read. Both separate experiments
require exact timer parent ac9b47e50c213b08022e78bdef64662569cd3d29/image
eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550.
All13older exporters/input pins/images/identities/reservations remain immutable.

## B0 ordinary RAM: identical executable, new explicit identity

ordinary_ram_image.py returns BYTE-IDENTICAL2048timer bytes:1504written,
544unwritten incl250RESERVED. No instruction/data/allocation/symbol/vector change.
New profile ntsc-four-port-cart-owned-irq-development; same declared public
layout ABI sb52-dev-cc65-v1, new ordinary-ram-v1 version/source/map/manifest.
It MUST be a separately explicitly selected identity, never auto-selected from
cart size, lack of a cooperating assertion or presumed compiler origin.

Normative docs/ordinary-ram-profile.json publishes EACH public shadow/vector
name/address/initial value, not just intervals. All25shadows0000..18 cold0;
rtclok low1/high2, paddl zeros unscanned not centered, no attract service.
Fourteen little-endian vectors0200..21B initiallyFC86, then0200=FE00 timer,
0202=FCA0 systemVBI,0204=FCB0 exit; remaining11stayFC86. See startup/timer briefs
for exact initialization write order. Values are at successful cold handoff,
not a promise that application changes or later enabled services leave them zero.

Ownership explicitly cedes021C..021F: application0019..FF/021C..3FFF, runtime
shadows0000..18/vectors0200..21B, shared real CPU stack0100..1FF. No runtime
600..61F reservation, extra persistent RAM or mandatory input-v2/v3 assertion.
This is original development ownership, not a historical reconciliation. No
power-on RAM-content preservation guarantee across core randomization itself.
No guessed0208/020A BIOS keyboard callback. Cart can install0200dispatcher,
own raw source/capture/ACK/rearm/AXY saves and RTI. Default timer dispatcher still
supports07 and faults enabled unsupportedF8 BEFORE ACK, including40 if the cart
fails to replace its generic vector. Default VBI/analog must not mutate the cart's
selector/mask/phase. Actual original consumer is the earlier60case Retro fixture;
no stockcc65/legacy/game compatibility inferred from it.

B0 nominal timing remains1148/1155cycles,422/425instructions. Parent native
1235/1242cycle observations are retained parent evidence, NOT new selection
measurements. Byte equality does not qualify new profile identity: native states
of old timer and B0 MUST mutually refuse before mutation despite identical
image hash, preserving next two ordinary frames. Schema/native fields unchanged;
complete profile/source/version/descriptor must participate in strict binding.

## B1 original full-cold admission: separate executable/profile

Profile ntsc-four-port-diagnostic-cold-development, diagnostic-cold-v1 version,
SAME conservative parent ownership THROUGH021F, NOT B0 cession. No implicit
B0+B1/font/bridge/fire combination; no new glyphs or0600input contract. Title
BFE8..BFFB20bytes opaque and never read by active metadata validation. FIRST
BFFC year ALWAYS50..59; SECOND BFFD50..59 orFF ONLY. A firstFF remains invalid
even when secondFF. Other invalid year values/pointers still faultFC86.

FF changes ADMISSION ONLY: all existing full-cold instructions/MMIO/shadow/vector
initialization execute in their existing order. No initialization bypass, splash,
cart byte mutation, hostPC change or hidden state. Entry4000..BFE7, AX/Y0,
SPFF/P&CF06/cold-only/error/reset policy and4096watchdog retained. It is NOT a
historical diagnostic bypass implementation or evidence the authorized game
expects/tolerates full initialization. No game run before exact admission,
lawful-source validation and explicit board/mapping/ownership decision.

New52byte validator occupies previously FF/unwritten inputFD80..FDB3. Original
metadataFEB0..FEDB stays byte-identical but is no longer the active startup call.
Only startup JSR operand bytesFC61/62 change B0FE ->80FD; opcode atFC60 stays20,
actual pushed returnFC62/resumeFC63/handoffFC6B unchanged. Map validate_metadata
nowFD80 with legacy_validate_metadataFEB0; independent diagnostic entry/valid/
invalid labels supplied. All other old services, original1024font, vectors,
padding andFF00..FFF9250reserve byte-identical. No new RAM/stack depth/helper call.

Actual image SHA2569da1ddefb339dc2ef3f93643d33b45021099d3fd3256ce1f9754f32787e6b69f.
Used1556/unwritten492; input105/176 (53old+52new). Parent1504 +52, not fire-v3
allocation; all250reserve untouched. Synthetic assembler vector roots only resolve
our fragment branches and are discarded; actual six hardware vector bytes are
unchanged. No CPU/register/chip execution model is supplied by these tools.

Independent nominal worksheet: old22iteration prefix LDX2+22*19-1=419cycles.
First valid year4+2+2+2+2=12; numeric second4+2+2+2+2+2+2=16, FF second4+2+3=9.
New prefixes28numeric/21FF save391/398nominal cycles. Existing entry check and
JSR counts unchanged, all branches withinFDpage, absolute metadata reads no
indexed crossing. Nominal numeric normal757/boundary764, FF750/757. Instructions
numeric257/260, FF253/256; oldprefix177instructions vs12numeric/8FF. Full native
refresh/RDY/timing remains unmeasured for B1, all full-cycle flagsfalse. Descriptor
base_cycles_max764, FF max757; full watchdog4096 unchanged, not a new global bound.

## Separate artifact boundary and tooling checks

New shared timer_experiment.py checks strict parent hash/1504fit/250reserve.
Separate export_ordinary_ram_candidate.py and export_diagnostic_cold_candidate.py
verify ALL inherited inputs at BOTH exact parent and requested full source, plus
new common/own generator/exporter/CMake and B0public contract data. Any dirty/
missing/old input refuses before outputs. No old exporter/CMakeLists modified.

Include cmake/ordinary-ram-candidate.cmake or diagnostic-cold-candidate.cmake
AFTER baseline add_subdirectory. Targets sb5200-ordinary-ram-image and
sb5200-diagnostic-cold-image with full40lowercase SB5200_ORDINARY_RAM_SOURCE_REVISION
or SB5200_DIAGNOSTIC_COLD_SOURCE_REVISION. Same4absolute artifact/source properties,
separate output directories. Building both targets in one tooling parent does
NOT create a combined runtime selection or ownership/metadata policy.

New map/manifest profile/version/source/provenance/contract SHA explicit. Public
layout ABI unchanged; accepted capabilities empty and all execution/provider/
retail/full-cycle flagsfalse. Seven methods put full offline suite at204: B0all
bytes/individual initialization/ownership, B1exact52encoding/branch/allowedchange/
fit/reserve/symbols, independent timing worksheet, disjoint identity/policies,
parent/contract drift, every inherited/new source pin corruption, old-pin refusal
and fresh-process reproduction. All13qualified prior CLI/CMake checks retained.
Exact committed new CLI/CMake consumer checks follow after obtaining source pin.

## Required independent native admission

B0 Releaseunity/full-native nonunityASan:120FULLY CROSSED port/contact xCRITIC
cases, not earlier60alternated. Original cart-owned IRQ/physical target-store
observer/pre-startupcanaries/explicit cart windows/poisoned immediate imports,
empty/held/release/repress/isolation/source/ACK/rearm/defaults/bounded NMI
preemption/fault/refusal, real ordinary/in-handler same/fresh/process continuation.
All inherited service/allSP/state/lifecycle/R65/OFF/firmware and converter negatives.
Old same-image timer/B0 mutual refusal must preserve state AND ordinary continuation.

B1 independently5120single-title positives+mixed/allFF, EACH year4F/50/59/5A/FF
and invalid pairs/firstFF+secondFF refusal, both numeric/secondFF entry boundaries.
Observe actual metadata CPU reads/no title reads/full cold write order/bus/RAM/
stack/finalflags/registers/handoff/refresh/RDY/counts/4096watchdog; early/pending/
helperNMI/IRQ/BRK/synchronization/recovery. Inherited services/allSP/frame/cache/
process/R65/poisoned valid imports and foreign/malformed state refusal with
ordinary continuation, old13exports/defaultOFF/firmware/converter exact tuples.
No game/profile admission from offline checks; fullR62 remains open/noACK,
MR43latest/app pins/defaults unchanged. A future combined B0+B1 needs explicit
exact identity/ownership and separate qualification, never automatic composition.
