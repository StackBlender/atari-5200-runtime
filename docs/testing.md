# Testing

The current foundation requires Python 3.10+; CMake 3.20+ and Ninja provide the
build entry point. There is no compiler, SDK, external assembler, emulator,
network fetch, game or firmware dependency. Python 3.12.3 and CMake 3.28.3/Ninja
are the initial host tools; no cross-version tool equivalence claim yet.

```sh
cmake -S . -B build -G Ninja
cmake --build build
ctest --test-dir build --output-on-failure
```

Or run the emitter suite directly:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The baseline CTest entry originally ran57 Python test methods (17 image-emitter, four capture
fragment, 14 scalar-record, eight cartridge-candidate, seven startup-image and
seven candidate-export tests). Independent expected instruction
bytes cover symbolic forward/backward resolution, little-endian addresses,
branch limits -128/127 and rejection at -129/128. Negative cases cover overlap,
allocation bounds, writes to reserved space, operand overflow, duplicate/undefined/
unwritten/non-executable targets, missing/repeated vectors and unsupported modes.
Fresh subprocesses emit identical image/report files in separate temporary paths.

`build/generated/layout-test.bin` is exactly 2048 bytes with ten written bytes;
`layout-test.json` reports its hash, symbols and budget. This is a build-tool
fixture with no runtime capabilities, not a usable BIOS replacement. Test reports
establish encoding/layout/reproducibility only. No CPU execution, hardware
service acceptance, original-BIOS compatibility or game result is covered.

All generated files stay in ignored build directories or temporary test directories.
The tests use original source and independent constants; no manufacturer program
is downloaded or used as an expected binary. New service claims require separate
permitted documentary or original-system evidence and independently expected probes.

## ENTRY-01 tooling

Generate a **non-runnable fragment** in the existing build tree using synthetic
example addresses (neither address is an approved result-area allocation):

```sh
python3 tools/entry_probe.py --entry-address 0x8000 --result-start 0x3000 --output-dir build/entry-probe
python3 tools/observations.py tests/local/entry-record.json
```

The second command needs an explicitly authored record following
[the protocol](entry-observation-protocol.md); there is no collected reference
record shipped in this repo. It prints a format report, not firmware approval.
Do not run the fragment as a cartridge. No CMake target installs/selects it.

Tests independently assert all 26 fragment bytes, result offsets, relocation and
address boundaries, stable fresh-process descriptor/image output and the one-byte
stack allowance. Record tests exercise bytes/types, missing/extra fields, dump
attempts, duplicate JSON keys, size/depth/non-finite rejection, artifact identities,
synthetic/reference separation, receipt requirements, unique trials, reset/input
semantics, observation order, status-bit masking and inconclusive results. CLI
rejection is exit 2 with no partial success report; local diagnostic size/hash
checking is tested with synthetic data. No test runs a CPU or original firmware.

## Original metadata and diagnostic candidate

```sh
python3 tools/cartridge_candidate.py --title 01234567890123456789 --year-digits 26 --output-dir build/entry-candidate
```

This creates `entry-candidate.bin` (32768 bytes) and `entry-candidate.json` in
that ignored directory. It is a complete proposed unbanked cartridge layout,
**not execution approval**. No default CMake target installs or runs it. Do not
supply it to a reference machine; the original-system protocol gates remain.
Its embedded capture descriptor still describes the fragment, not full-cart
approval. Source/encoder/fragment hashes remain the existing ENTRY-01 identity;
additional full-image/layout-source hashes identify the enclosing candidate.

Eight new tests independently check all 24 metadata bytes, every digit mapping,
strict ASCII versus Unicode lookalikes, types/lengths, little-endian entry limits,
all zero-fill holes, all capture bytes, the last nonoverlapping placement,
cart-owned result bounds, negative CLI no-output and fresh-process determinism.
No metadata decoding or machine execution is tested; scope/MMIO/mapper review
and CPU/ANTIC observations belong to later owner acceptance. See
[startup-brief.md](startup-brief.md) for exact proposed expectations and limits.

## Authored bounded startup image

Default offline build now also emits `build/generated/startup.bin` and
`startup-map.json` via authored_startup, independently of the layout fixture.
For an explicit standalone generation in the same build tree:

```sh
python3 tools/startup_image.py --output-dir build/startup
```

Seven new tests compare all94 reset and44 helper bytes against independent NMOS
constants, branch offsets/labels, three fault loops and CPU vectors, all80 original
digit bytes and every blank glyph, exact allocation/FF future reserves/margin,
eight new opcode encodings/bounds and fresh-process image/map reproducibility.
The image's accepted capability list remains empty pending independent execution;
authored_capabilities distinguishes implemented source scope. See
[startup-proof.md](startup-proof.md) for static stack/base-cycle derivation and
Mars instruction-boundary/full-cycle acceptance requirements. No own CPU engine
or host service emulation was introduced to make the tests pass.

## Pinned candidate export

After committing generation inputs, configure the same build tree and run
`cmake --build build --target sb5200-runtime-image`. See
[candidate-export.md](candidate-export.md) for exact properties, pinned source
verification, manifest flags and parent dependency ordering. Seven new tests
exercise manifest identity/false approvals/revision format/determinism and pinned-
input rejection. Export is not CPU/provider execution acceptance.


## VBI clock candidate

Nine additional methods bring the suite to66, covering the separately authored
VBI image, strict local encodings, exact reset/interrupt/clock/exit bytes, fit,
unchanged baseline, versioned manifest, all pinned-input failures and fresh-process
output. See [static packet](vbi-clock-proof.md) and [approved scope](vbi-clock-brief.md).
Generate unexported image/map with tools/vbi_clock_image.py --output-dir build/vbi-clock.
Pinned integration export is tools/export_vbi_candidate.py; it requires committed
inputs. Separate opt-in CMake target is documented in the static packet. No
offline test runs a CPU or establishes actual clock/interrupt service acceptance.


## Display-shadow candidate

Seven additional methods bring the offline suite to73. See
[static proof/export](display-shadow-proof.md) and [service brief](display-shadow-brief.md).
Generate unexported image/map with tools/display_shadow_image.py --output-dir
build/display-shadow; export committed source with tools/export_display_candidate.py.
Separate opt-in CMake target sb5200-display-shadow-image preserves prior pins.
Exact bytes/fit/reproducibility/export refusal are offline checks only; hardware
write order, rendering and synchronized state replay require integration execution.


## DLI dispatch candidate

Seven additional methods bring total80. Generate unexported image/map using
tools/dli_dispatch_image.py --output-dir build/dli-dispatch. Separate pinned
export tools/export_dli_candidate.py and opt-in target sb5200-dli-dispatch-image
are documented in dli-dispatch-proof.md. Byte/branch/vector/fit/provenance and
fail-before-output checks do not execute NMI or establish raster/state acceptance.


## Analog shadow candidate

Seven new tests bring total87. tools/analog_shadow_image.py emits ignored
image/map; tools/export_analog_candidate.py requires committed source. Separate
opt-in sb5200-analog-shadow-image target documented in analog-shadow-proof.md.
Offline prime/pending/copy/restart bytes/fit/provenance tests do not prove real
POKEY acquisition, initial validity, callback/state execution or game support.


## IRQ/BRK dispatch candidate

Eight methods bring total95. tools/irq_brk_image.py emits ignored image/map;
tools/export_irq_candidate.py requires committed source. Opt-in target
sb5200-irq-brk-image and SB5200_IRQ_SOURCE_REVISION are documented in
irq-brk-proof.md. Static stack arithmetic covers all256 positions, not CPU
execution; actual IRQ/BRK/status/RTI/replay acceptance belongs to Mars.


## Timer dispatch candidate

Nine methods bring total104. tools/timer_dispatch_image.py emits ignored
image/map; pinned export tools/export_timer_candidate.py and opt-in target
sb5200-timer-dispatch-image documented in timer-dispatch-proof.md. Exact byte/
branch/mask-write/fit/helper/static checks do not run CPU timers or prove IRQ
source handling, callback RTI, priority or synchronized process replay.


## Keypad/fire policy planning model

Seven new methods bring total111. Run the existing unittest/CTest commands.
tools/keypad_policy.py reduces already acquired window observations; tests cover
all old/new contact values/ports, holds/releases, scheduling, fire ordering and
policy replay/strict inputs. See keypad-fire-brief.md for unresolved hardware,
IRQ/NMI race, RAM/profile and fit gates. No CPU/chip model, MMIO/image change,
acquisition validation or native state acceptance is supplied by these tests.


Keypad/fire revision2 adds invalid/busy-window preservation (112 total methods)
and restricts contacts1..15. The existing8-boundary scheduling assertion is a
reducer property only; actual first-handler acquisition can approach9 intervals
before deferrals. No native IRQ/NMI frontier or hardware latency proof follows.


## Keypad IRQ latch candidate

Nine additional methods bring121 total. Exact original IRQ/latch/source/timer/
RAM-clear bytes and budgets, new opcode strictness, profile/provenance/refusal/
fresh-process tests cover authored encoding only. See keypad-irq-proof.md for
commands, four-property pinned exporter and native CPU/frontier/state acceptance
packet. No automatic window/fire/input event service exists in this candidate.


## Automatic keypad window candidate

Nine new methods bring130 total: independently expected analog-loop/rotation/
window/guard/pending-before-ack/callback/arm bytes, strict new local encodings,
full unchanged-range/fit checks and profile/provenance/fresh-process/refusal. See
keypad-window-proof.md for actual CPU/stack/window/latency/state acceptance still
required. All earlier emitters/profiles remain byte-exact; fire remains unfinished.


## Both-fire nonrunnable fit fragment

Six methods bring136total; tools/fire_service_fragment.py emits153raw bytes
only, no runtime image/provider. Exact independent encodings/order/baselines/
branches, budget failure/projection, strict local opcodes/parent preservation and
fresh-process output checks. See fire-allocation-review.md: allocation/profile
review is required before cumulative emission; no CPU/fire/game acceptance.


## Static fire-fragment boundary audit

Six mutation and CLI methods bring142 total. Run the normal unittest/CTest suite.
After fragment generation, `python3 tools/fire_fragment_audit.py
build/fire-fragment/fire-service-fragment.bin` prints the deterministic audit.
The audit independently decodes only the permitted small instruction subset and
checks access operands, internal branch destinations and fixed callback/exits.
Negative tests redirect real store operands to protected addresses, attempt
write-only readback/indexed-base changes, branch escapes and callback/control
changes; CLI failure exits2 with empty stdout. No CPU execution or dataflow proof:
indexed footprints assume X0..3 at those operations and callbacks obey contract.
The report is not an allocation/native acceptance or worst-case timing result.


## Cartridge-side input callback recorder

Five new methods bring147 total. Use the existing unittest/CTest commands.
`python3 tools/input_callback_probe.py --output-dir build/input-callback` emits
only a nonrunnable80-byte fragment/descriptor. See input-callback-probe.md for
independent encoding/cycle/bounds/freshprocess checks, synthetic snapshot decoder,
required cart RAM/control invariants and remaining native cartridge execution.
No runtime generation/allocation/provider changed; no real callback was executed.


## Cumulative both-fire fire-v3 candidate

Eight methods bring155 total; existing unittest/CTest. See fire-proof.md for
new separate allocation/profile/export/CMake and exact ROM/routing/falseflag/
provenance/failure/freshprocess checks. fire_image.py --output-dir build/fire
emits only ignored unexported image/map. Committed source required for
export_fire_candidate.py and sb5200-fire-image. Native both-source behavior,
actual cache/latency/stack/full-VBI/state/converter qualification remains pending.


## Standalone callback-bridge fit proposal

Five new methods bring160 total. Existing unittest/CTest; see
remaining-services-review.md for the original146-byte alternate fragment,
independently expected encodings/branches/cycle arithmetic, preserved accepted
image/fragment, false approval flags and fresh-process checks. Not a cumulative
image or native equivalence proof; no accepted generation/allocation changed.


## Separate cumulative callback-bridge refactor

Seven methods bring167 total. Existing unittest/CTest; fire-bridge-proof.md
records exact relocated146bytes/callreturnPCs/bridgeargsetup/reload,1895fit/
90reserve,oldparentpreservation,budgetstop/profile/identity/falseflags/pinned
failures andfreshprocess. Newsource/export/CMake require explicitnewpin and
native tuple admission; oldten generations unchanged. No nativeequivalence yet.

## Standalone printable glyph authoring

The full offline suite now has173methods including six printable-glyph checks.
Use the existing unittest/CTest commands. tools/printable_glyphs.py outputs only
760unbound asset bytes and JSON; no runtime image/target/approval. See
printable-glyphs.md. Full pinned eleven-generation export reproduction remains
required when changing generation inputs; this slice adds none to old exports.

## Persistent all-generation regression

Current suite175methods includes tests/test_accepted_exports.py: real eleven
pinned CLI exporters and temporary parentCMake dependency/fourproperty/artifact
byte equality, plus negative binding/descriptor/map/image/capability/approval
fixtures. tools/verify_accepted_exports.py --cmake is the standalone command;
see accepted-generations.md. Local own source history/CMake/Ninja required,
no network/emulator/firmware. Older native qualifications are not rebuilt here.

## Approved opaque-title policy

Six new methods bring181total. Exact sole FEB1index byte, unchanged1895fit/90reserve/
all prior symbols/bytes, independently recomputed1091/1098nominal startup,
identity/profile/false labels/provenance, every old/new pinned input and fresh
CLI reproducibility. All eleven qualified export/CMake checks still run. See
opaque-title-proof.md; native5120title/year/entry/inherited/state/R65qualification
is separate and pending. No runtime CPU execution is performed by tool tests.

Pinned opaque-title CLI/CMake consumer verification adds a seventh method:
182total PASS, including exacted01354artifacts/fourproperties/dependency/equality
and all eleven older pinned exports. Native qualification remains pending.

## Conditional timer memory inventory

Six static-audit methods bring188total.220instructions/474code bytes, exact
loop/default-target guards, RAM/conio/MMIO/stack footprints and deliberate
operand/control-flow/identity failures. CLI tools/timer_memory_audit.py admits
only our exact qualified timer image. No CPU simulation/native execution.
See timer-memory-audit.md for assumptions, external boundaries and consumer
startup/VBI canaries. All earlier export/candidate artifact checks remain included.

## Declarative original geometry

A seventh glyph test puts the full suite at189methods. Independent binary parsing
of95explicit8x8 JSON cells reproduces the frozen760byte asset. No glyph changes,
Atari encoding/bank/ABI remain null. This supports separate native pixel oracles;
character-bank-proposal.md is documentary policy only, not authoring/admission.

## Twelve qualified exports

Marsd5c709f/msg_d972 independently qualified opaque-title ed01354. The persistent
verifier catalog adds its immutable source/image tuple and uses its CMake target
for the latest parent dependency/fourproperty/triple equality check. All11older
CLI exports remain checked; the dedicated opaque-title artifact method also stays.
189methods total, no added CPU execution/provider approval or generation input edit.
See independent-execution.md for native evidence and its product limitations.

## Original first64-cell bank authoring

Seven tests/test_character_bank_image.py methods bring196total; run standard
unittest/build/CTest. Independent all95geometry repacking/hash/all64boundcells,
retained fixed80digit bytes, parent-high/code/fit/reserve/symbol preservation,
manifest identity/provenance/false flags, malformed source geometry/content and
pin/fit/parent corruption, old-pin refusal before output and fresh process checks.
Prior12CLI exports/latest opaque CMake regressions retained; new candidate
qualification remains native-owner work, not these tests. See character-bank-proof.md.
