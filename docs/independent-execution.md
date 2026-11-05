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
