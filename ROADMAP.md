# Atari 5200 Runtime roadmap

StackBlender will complete and freely share this original GPL-3.0-or-later
runtime. NTSC four-port first; full software compatibility remains unfinished.

## Next

C source/data packet ready: character-bank-proposal.md screens selected1982
manufacturer ANTIC prose via OCR, with errors/visual limits explicit. Proposes
64ASCII-labelled first-bank cells (54original ASCII drawings plus10retained
seven-segment digits), preserves old high512bytes/legacy50digits/all code/reserve.
No authoring approval or bank emission.95cannot fit64; no inferred ATASCII ABI.
Standalone189method suite now exposes95declarative8x8 oracle cells,760glyphbytes
unchanged and all bank/encoding/ABI null. Need owner review before binding.

B audit advanced under Marsf20996c/msg_7827, no profile approval: standalone
strict timer_memory_audit.py inventories220instructions/all474emitted code bytes,
all default-handler/frontier control flow, guarded finite startup loops, explicit
RAM/MMIO/stack operands. Conditional RAM writes0000..18/0100..21B; no app021C..3FFF
or conio0019..1C operand access.188offline/CTest1/1 PASS, corruption boundaries
fail. Retro now seeds15837canaries after cold randomization before first observed
runtime instruction; startup+VBI/same-fresh-root replay pass timerRelease12/12
and adapterASan12/12. Need actual keyIRQ consumer contract and explicit separate
021C..21F cession/all-native-path qualification before ordinary profile emission.
See timer-memory-audit.md; no profile/game/native-completion inference.

Opaque-title sourceed01354/image8d6ef38c is now independently qualified by
Marsd5c709f/msg_d972 in Release/full-native ASan,5120title cases plus inherited/
R65/state/refusal/OFF/firmware. Full cold1167/1177cycles,360/363instructions;
measured savings414/411 versus static380. Pooled/unreleased; MR43 and app pins
unchanged. Persistent verifier now covers12qualified exports and latest opaque
CMake consumer;189methods retained. See independent-execution.md. B ordinary
profile/keyIRQ contract and C bank authoring review remain pending, not A.

Completed export-regression automation: tools/verify_accepted_exports.py
reproduces all eleven real pinned CLI exports and optionally the real parent
CMake dependency/fourproperties/triple equality. Two added methods put the real
CLI/CMake check and invalid artifact/binding/approval cases in the ordinary suite:
175unittest/CTest1/1 PASS. See docs/accepted-generations.md; no native rerun,
provider selection, old input or approval change. No disposable harness needed.

1. Opaque-title generation authored under Mars1afec85/msg_0ea1: sole FEB1=14,
   SHA8d6ef38c1b487fa95742e62e9a5c0b1a928ddb446977264739a263fa0bc070c4;
   unchanged1895written/ABI/90reserve.182offline methods +real pinned CLI/CMake PASS. Source/export
   ed013540ac2996d76fab149f6fb8dea9fcead584 pushed. Recomputed nominal
   startup1091/1098; independently qualified Marsd5c709f/msg_d972 as recorded above.
   No native admission/release/default/false-flag change. See opaque-title-proof.
2. Resolve an ordinary-software RAM profile: cc65 documents021C..3FFF; current
   cooperating input ABI reserves0600..061F. Do not relabel arbitrary homebrew
   as cooperating. Reconcile021C..021F and actual consumer key IRQ requirements.
3. Bind original printable glyphs only after a supported consumer/ANTIC2/6/7
   address/color/inverse/encoding contract. Current standalone asset is unbound;
   all eleven prior generations and old digit font remain unchanged.
4. Close remaining reset, finalVBI, attract, Break/serial, broader board/cart and
   service requirements with screened evidence, explicit policy, fit and independent
   probes. Never invent numeric warm services or spend the90-byte reserve.
5. Authorized real-game compatibility and product controls/audio/local-online/
   device acceptance. Bounded diagnostics do not establish those gates.

## Latest accepted development generation

Opaque-title ed013540ac2996d76fab149f6fb8dea9fcead584, image
8d6ef38c1b487fa95742e62e9a5c0b1a928ddb446977264739a263fa0bc070c4.
Marsd5c709f/msg_d972 independent Release/full-native ASan qualification above;
full attributed matrix/timing/limits in [execution receipt](docs/independent-execution.md).
Same fire-v3/frozen declaration/32RAM,1895written/fire146/90reserve/nativefields/
schema/false approval flags. Pooled UNRELEASED; MR43 remains latest and Retro
pins stay unchanged. FullR62 req_6f74 remains open/noACK. Preserve real ordinary
frame returns, post-return polls/stale caches and host-before-import ordering.
B ordinary profile/keyIRQ and C numeric binding review remain open.

## Standalone asset batch

95original printable ASCII drawings/760bytes, explicit geometry, six independent
checks; total173offline methods. No Atari mapping/bank/provider/ABI/approval.
See [glyph contract](docs/printable-glyphs.md). Existing images/profiles/allocation/
false approval flags remain immutable. Font binding and title policy review are
separate gates, not implied by artwork or seven saved bytes.

## Evidence and completion rules

Source ledger: [sources](docs/sources.md). Remaining contracts:
[service inventory](docs/remaining-services-review.md). Earlier proposals/receipts
are preserved with dates; latest explicit receipt supersedes pending notes.
No firmware/disassembly/extracted assets/foreign implementation, reference oracle
or original-hardware observation corpus. Development policy and independent
emulator results must not be relabeled historical firmware equivalence.

## History

The former append-only roadmap is preserved verbatim in
[history](docs/history/roadmap-before-glyph-batch.md). It records earlier pins,
reviews and qualification transitions; use the current Next list for priority.

Batch verification:173unittest methods, build/CTest1/1 PASS. Real pinned bridge
CLI plus temporary parentCMake/fourproperties/dependency order/artifact equality
PASS; all ten earlier pinned exporters reproduce unchanged hashes. Temporary
parent removed. Standalone asset SHA256
674bd8776ac83d517654b3d6ca2720e5b6d69f5e084c2bd35052c19c074f547a.
Original-only raster preview visually inspected under ignored
build/printable-glyphs/preview.png. git diff --check PASS. No runtime generation
or approval fields changed. Repo lease to be released after push.
