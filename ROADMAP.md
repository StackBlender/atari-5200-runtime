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

Opaque-title authoring complete: sourceed013540ac2996d76fab149f6fb8dea9fcead584,
image8d6ef38c1b487fa95742e62e9a5c0b1a928ddb446977264739a263fa0bc070c4;
sole FEB1=14, static1091/1098, fit/ABI/90reserve unchanged. Exact qualification
packetmsg_73ee/req_6f74 already delivered. Full dualnative5120title+inherited/
state/process/R65 qualification pending; no admission/release/pin/default change.
B ordinary profile and C numeric font binding remain unapproved. Do not repeat
A authoring or ask for human permission; see opaque-title-proof.md.

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
   startup1091/1098; native full timing not measured. Exacttuple msg_73ee delivered; full5120title+year/entry/inherited/state/R65 matrix pending.
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

Exact source e25a466d15c574f3ec364bfc2f44bc7ef2f51117; image
c5fd8df1564c28e5ed4c5aad9f8eabdc64a62e32de28e8dcce6bfae7ea533d24.
Bridge deduplication independently qualified by Mars5b6c5be4/msg_fd40.
1895written/2048,391above1504timer,9under1904ceiling,146/160fire,
63ordinaryfree and90reserve untouched. No new service/RAM/stack/native field.
Same fire-v3 ABI/frozen cooperating declaration. Release/ASan892fire cases,
37safe/cache/frame/moved-setup/process frontiers each plus inherited services,
R65/refusal/converter11tuples/default-OFF/firmware checks. Pooled; MR43 latest.
See [proof/receipt](docs/fire-bridge-proof.md) and
[independent execution](docs/independent-execution.md). Ordinary frame return may
occur inside VBI/callback: keep real post-return polls and serialized stale caches.

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
