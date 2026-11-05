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
