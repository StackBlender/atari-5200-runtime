# Independent bounded execution receipt

Integration-owner report received 2026-11-05 for source revision
`711a2e986f7906f45aebd310e6330fd7ffc338bf`, image SHA-256
`b2d8ebb8d0070f2aee1bd79d7adfee85b88797702cb96035ab3a18e9bd37f68d`.
This records independently authored emulator fixtures, not original Atari
hardware/firmware observations or a local rerun of the owner's suite.

The owner reports real reset-vector/opcode/bus/chip execution with no host
service substitution, direct entry jump or fabricated BIOS input. Normal startup
measures1166 full CPU cycles/403 instructions; valid boundary cases reach at most
1175/406 including refresh/RDY, within the4096 target. This supplements the
static1084/1091 base-cycle argument; emulated counts are not host speed or battery
measurements.

Reported acceptance covers all67 startup stores plus two helper stack writes,
entry registers/flags/SP, preserved caller RAM and fresh completion write;
all22 digit positions with4F/5A/FF, entry limits, masked IRQ/actual BRK,
early/helper NMI (five transient stack bytes), sustained RDY timeout at4097 and
cold recovery, wrong/missing carts, repeated cold starts and new instances.
Actual ANTIC fetches all80 authored digit bytes; independently composed80x8
rendered expectations match, with CPU reads/debugger peeks/DMA agreeing.

The development provider requires two explicit opt-ins (both default OFF), an
explicit Linear32K loaded cartridge and cold reset. Unsupported reset operations
refuse before machine mutation; physical Reset remains a separate input.
Only Ready synchronized states are supported, bound to image/full manifest/pin/
profile/cart/controller identity and exact schema/checksum. Raw, starting,
failed, legacy, wrong-config and damaged/extended states refuse. Same/fresh-instance
and separate-process replay, synchronization faults and lifecycle checks pass
per owner. Release unity and nonunity Debug ASan suites (leaks disabled),14
converter negatives and default-OFF/missing-provider gates also pass.

No emulator implementation or foreign test code was read/copied into this
project. Only the owner's behavioral report/integration prose was reviewed.
**Export flags and accepted capabilities stay unchanged**, including
execution_verified=false and provider_approved=false. The current adapter
intentionally requires these candidate labels; the independent receipt is
separate evidence, not permission to alter the pinned manifest.

This completes bounded development execution evidence only. Ongoing VBI/DLI/IRQ,
input scanning, clocks/timers, display shadows, broader assets/reset/layouts and
full service fit still require reviewed contracts and independent fixtures.
No game compatibility, original-system equivalence, supported module release,
consumer acceptance, app enablement, device result or production approval follows.


## VBI clock independent execution receipt

Integration-owner report received2026-11-05 for source pin
ba90c8550c1be1c85b5aa7d6810e1ee6c6031656, image
62df6162ac3accdfa19769c8f2dcd450c510e385fa71f98ec7912f61d449fa54.
The exact new image/manifest/map/full-pin/version/symbol tuple is independently
allowlisted in the development adapter. This is owner-reported execution,
not a local rerun or original-system measurement. The integration is committed,
pending a separately authorized release; the previous released baseline remains.

Actual NMI selection while Starting, including interrupt-vector hijack, and
pending-NMI handoff refusal prevent false Ready without host service execution,
PC replacement or pending-state clearing. No persistent observer/schema change:
image-bound sb52rt-dev1 rejects old/new states in both directions before mutation.

Independent fixtures report288 clock-seed/I-D/CRITIC/callback combinations with
two real ANTIC VBIs each, plus120 default VBIs; real DLI refusal and explicitly
synthetic status/pending/vector-hijack/early/helper/near-handoff/ANTIC-phase cases.
Exact old/new RMW writes, marker order, RTI/register/stack/caller RAM pass. Twelve
actual instruction safe points replay in same/fresh instances; separate-process
mid-service checkpoint byte replay passes. These are synchronized safe points,
not arbitrary mid-instruction or half-written-RMW snapshots.

Startup1197 full cycles/411 instructions, valid boundary maximum1204/414.
DMA-off/ordinary-refresh default handler maximum95 full cycles including RTI;
custom-marker path119; hardware-entry latency7 separately. The4096 startup and
512 default-handler targets pass for those diagnostics. No arbitrary callback,
active-DMA/WSYNC/held-RDY/nesting bound, original hardware or mobile result follows.

Full Release unity and nonunity Debug ASan suites (leaks disabled),20 converter
negatives, all prior startup/metadata/RAM/DMA/pixels/reset/fault/replay/lifecycle
checks, old-provider/default-OFF/a26 regressions and firmware scans pass per owner.
No foreign implementation/test code was read/copied here. Export pin, false labels
and accepted capabilities remain unchanged. This is bounded development service
acceptance only; product enablement, further ongoing services, supported runtime
release, consumer validation and full integration request completion remain open.


## Independent display and DLI acceptance

Mars msg_8f2c /4daa27f5be981b0d1a1b5a923bf40e24e97f3f4a accepts separate
explicit development tuples for display source9d7071f837ec513905b4a2f9718e269c7662b90c
and DLI source258bc0cc764a0614ec8443a89d242a8f1fe8cb5e. Prose contract/receipt
and emitted artifacts reviewed independently, not our GPL implementation/tests.
No local CPU rerun or original-system measurement. Earlier pending-review notes
below are historical; this receipt supersedes their execution-pending status.

Owner Release unity and nonunity Debug ASan(-g -O1) pass startup,288 VBI cases
plus120 services/12 safe points,404 display pattern/CRITIC/callback cases with7
safe points,128 DLI status/stack/register/CRITIC cases with9 safe points. Actual
twelve raw source/MMIO writes, callback ordering, list/color/DMA off/on rendering,
DLI hardware-frame/RTI/mode2 palette and isolated/combined twelve-event cadence
pass. Same/fresh/process replay,20 converter negatives and mutual candidate
state refusal pass; strict schema remains R65 sb52rt-dev2. DLI provider also
passes standard/mixed four-controller hardware matrix and powered live exit.

Startup1197/411, valid-boundary max1204. DMA-off ordinary-refresh default VBI
max187 for display,190 for DLI, excluding hardware entry7; custom-marker max212.
Active blank-list DLI dispatch38, complete callback/RTI86. Deliberately VCOUNT-
delayed custom active-list transfer body144, complete service4785 cycles; this
exceeds512 because of the cart callback and is OUTSIDE the default-handler
contract. No general active-DMA/RDY/WSYNC/nesting/callback deadline claim.

Prior startup/VBI/default-OFF/a26/process/lifetime and43-image firmware tree/
history/three-build checks pass per owner. Startup711 remains default; all build
gates OFF and module capability/approval/execution flags remain FALSE by design.
No observer/chip execution/state-schema change. Pending pooled release with
R65/R66; do not adopt Mars main or enable app before an approved MR announcement.
Full R62 ongoing input/timer/reset/reference/product acceptance remains open.

Next author analog service only after its original policy review: explicit
priming and complete-eight-axis copy/restart, docs/analog-shadow-brief.md. Mars
prose now confirms unpowered standard/disconnected target228, approximate Trak-
Ball unpowered target114; these emulator semantics are not board measurements.


## Independent analog acceptance and keypad limitation

Mars msg_1cd6 /33967abf09dfef07d163f3a14d43502f699ec9cc accepts exact source/
exporta6c406e4cee090b8044eea3b9b6c7a5b6391b3ab as a separate bounded development
tuple. Release unity/nonunity Debug ASan(-g -O1) independently pass startup1212
full cycles/416 instructions, boundary1219; prime order, FC73 helper return,
final state, metadata and early/pending/hijack/reset failures. Existing288 VBI
cases+120 services,404 display and128 DLI suites and safe/process replay pass.
No local CPU rerun or original hardware/BIOS evidence.

Analog59 cases cover eight axes/endpoints,16 connectivity masks, eight one-pending
masks (no partial copy/restart), POTGO-frozen host vectors, cold mixed Trak-Ball,
immediate/long CRITIC and early/mid/late completion. Ten pending/complete safe
points replay same/fresh; pending and mid-copy separate-process final bytes
match.20 converter negatives and mutual DLI/analog identity refusal pass. Existing
R65 sb52rt-dev2 schema/observer unchanged; no CPU/chip algorithm/host service added.

Default VBI max268 full cycles, marker282/broader marker293; entry7 separately.
DLI dispatch37/callbackRTI86. Custom VCOUNT-delayed active-list service4901
(transfer body140) is explicitly OUTSIDE default512 target; no general DMA/RDY/
nesting/callback bound. Old-provider/default-OFF/a26 and Release/ASan standard/
mixed four-controller/wire/process/lifetime regressions pass per owner.43-image
firmware tree/history/three-build checks clean. All source pins/export false
flags/default gates unchanged; pooled unreleased, no app/retail enablement.

IMPORTANT next keypad scope: under current SKCTL03 a held standard key1 leaves
KBCODE FF in the owner's fixture. RANDOM evolves256 values, KR2 SKSTAT F7 with
IRQ masked. This is a separate delivery/debounce debt, not hardware evidence or
an accepted keypad service. R65 direct hardware keypad tests use06 and do not
qualify03 runtime delivery. Investigate through permitted behavioral review
before keypad/fire/IRQ claims; do not silently change the accepted analog image.
Full R62 keypad/fire/timer/reset/reference/product scope remains open.
