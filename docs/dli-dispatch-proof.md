<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# DLI dispatch static proof and export

Original separate candidate, scope/execution review pending. Contract and
independent fixtures: [dli-dispatch-brief.md](dli-dispatch-brief.md). Display
candidate acceptance is also still pending; no cumulative execution claim.

2048-byte image SHA256
374465be3cfce3d15c10c7899f4fedbd8cf854b23ee1734b9302c7049e55e05c.
1318 written/730 free; interrupt51, display63, startup114, clock16, helper44,
font1024, vectors6. Input176 and margin250 untouched. Old FC89..FC99 classifier
becomes FF, new FCC0..FCDB28-byte classifier; NMI vector FCC0. Other image
bytes and all other previous labels identical to source9d7071f display candidate.

NMOS sequence saves A, reads D40F once, AND E0, CMP40/BEQ vbi_sourceFCD5;
otherwise CMP80/BNE nmi_faultFC80. Accepted DLI STA D40F/PLA/JMP(0206);
accepted VBI STA D40F/PLA/JMP(0202). Branch operands0B andB2 independently
checked to destinationFCD5/FC80. No extra JSR/stack/RAM, unchanged startup
vector0206 points to FC86 until cartridge installs its handler. Cold setup
and final handoffFC6F unchanged. Caller hardware P/PC stay on the actual stack.

Static DLI30 cycles/10 instructions through indirect JMP; hardware entry7 and
callback/RTI separate. VBI adds1 base cycle (taken BEQ rather than untaken BNE),
169..174 default eligible base cycles/50..51 instructions. Same startup1108/1115
base cycles411/414 instructions. DLI dispatch maximum stack4 bytes incl hardware,
callback entry3; VBI max6 as before. All branches samepage, no indexed access.
Full targets128 DLI-dispatch and512 default-VBI require Mars measurement under
stated DMA-off/ordinary refresh conditions. No nested/overlap/held-RDY bound.

## Separate export

```sh
python3 tools/export_dli_candidate.py --source-revision <full-commit> --output-dir build/dli-candidate
```

Parent adds baseline module, sets SB5200_DLI_SOURCE_REVISION to the full committed
source, includes cmake/dli-dispatch-candidate.cmake and depends on
sb5200-dli-dispatch-image before conversion. Four same target properties:
SB5200_IMAGE_FILE / SB5200_MANIFEST_FILE / SB5200_MAP_FILE absolute paths,
SB5200_SOURCE_REVISION full40-hex commit. Separate dli-candidate output.
Verify every baseline input plus tools/dli_dispatch_image.py,
tools/export_dli_candidate.py and cmake/dli-dispatch-candidate.cmake against the
specified commit before output. No dirty bypass. No dependency on changing old
candidate emitters; own cumulative original source preserves prior exports.

Manifest version
cold-start-digits-v1.vbi-clock-v1.display-shadow-v1.dli-dispatch-v1.candidate1;
schema1/ABI1 and same reset/mapper/profile/Starting interrupt observer contract.
All accepted capabilities and approval/execution/full-cycle flags stay false;
new dli_dispatch_base_cycles30 / full_cycle_target128 / full_cycles_verifiedfalse
only describe target/static information. New full image/map/source identity and
classifier/vbi_source symbols require explicit converter allowlist review and
strict sb52rt-dev2 mutual old/new identity refusal. No default enablement.

## Checks and limits

Seven new test methods bring total80: exact28 classifier bytes/branches/vectors,
only intended image differences and unchanged startup/register ABI, full fit and
reserves, manifest/provenance/hash/false approvals/version/timing, every pinned
input mismatch refusal, fresh-process bytes/maps and prior-pin CLI no-output
rejection. Direct unittest and existing build/CTest pass. No CPU engine added.
Offline tests cannot prove real ANTIC DLI/VBI events, raster position/response,
stack/RTI execution, converter acceptance or synchronized replay. Mars independently
owns the brief's actual device/callback/clock/display/state/lifecycle tests.
