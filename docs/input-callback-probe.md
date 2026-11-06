# Original input callback recorder fragment

RUNTIME-004 diagnostic preparation, separate from pending runtime allocation and
native execution reviews. This is an original80-byte cartridge-side fragment,
not a complete cartridge, runtime image, approved provider or executed probe.
No BIOS/firmware data, foreign emulator/test or reference trace was used.

## Layout and use contract

`python3 tools/input_callback_probe.py --output-dir build/input-callback`
emits ignored input-callback.bin/json. Default cartridge mapping entry8000,
key callback8000/fire8008/common8010/full804A. Relocation permits4000..BF98,
before communication metadataBFE8. These are proposed diagnostic addresses,
not a retail BIOS convention. No default target selects/executes this fragment.

Default cart-owned control0700..0706 and buffer0800..087F do not overlap reserved
runtime0600..061F. Tools require both allocations >=0620 and <4000, disjoint;
application owns and must reserve them. Controls are count,cursor,port,old,new,
kind,overflow. Buffer holds32 four-byte records kind/port/old/new; kind0=key,
kind1=fire. Port0..3, keysFF(no contact) or1..15, fire bitmap0..3.

A later reviewed cooperating cartridge must initialize all7 control bytes to0
before enabling callbacks, install key entry at020A and fire entry at0208 only
for the exact selected runtime contract, and obey that profile's quiescent
SEI/NMI-off activation/disable sequence. This fragment does not activate scanning,
configure input, install vectors, reset hardware, reserve memory in an unknown
cartridge, or establish approval of the proposed fire-v3 contract. It does not
require changes to any current runtime/provider image or ROM allocation.

Each callback receives Aport/Xold/Ynew, stores scratch, then appends one tagged
record in invocation order. It advances cursor by4 and publishes count LAST,
then RTS. Once count>=32, it only flags overflow (scratch still updates), never
wraps/overwrites the buffer or increments count. AXY/flags are scratch. No extra
push/helper JSR; RTS consumes the caller's bridge return. No CLI, input/mask/
selector/audio/NMI/GTIA/POKEY write or hardware read. Runtime and timer handlers
must not share diagnostic scratch. Callbacks cannot run recursively; foreground
must not mutate the control/buffer while capture is active. Initial valid
count/cursor invariant and exclusive ownership are preconditions, not enforced
against arbitrary RAM corruption by the CPU fragment.

Independent nominal worksheet: entry9 +common24 +four record fields44 +tail20
=97 NMOS CPU cycles including RTS. Full-buffer path42, at most43 if its taken
branch crosses a page after relocation. STAabsX fixed5 cycles; no read-index
penalty. This fits the proposed <=128 nominal callback budget, but is not actual
Mars/ANTIC refresh/RDY timing, full VBI budget, battery or physical latency proof.

## Reading results and independent acceptance

Quiesce acquisition/NMI before copying7 control and128 buffer bytes. Snapshot
control+buffer coherently; a live read across writes is not an atomic protocol.
`decode_snapshot(control_bytes,buffer_bytes)` validates exact lengths/types,
count<=32, cursor=4count, overflow0/1 (only at full), kind/port/key/fire ranges,
and changed values, then returns an ordered diagnostic event list. Unused buffer
and scratch bytes are ignored. It accepts original diagnostic result RAM only,
never firmware instruction/memory traces. No reference record is shipped.

Synthetic format tests demonstrate ordering of four bottom/key/selected-top-like
records, full capacity/overflow and invalid records; these are supplied values,
not CPU execution, contact acquisition or baseline/hold/port-isolation evidence.
At overflow, recorded prefix is retained but later callbacks are lost explicitly.
Reinitialize quiescently for each bounded native scenario; do not infer event
absence from a saturated log. Decoder output retains acquisition_verified=false.

Five methods bring147 total offline tests: complete independent expected80-byte
encoding/publication/branch/RTS, nominal cycle arithmetic, relocation/adjacent and
last-byte bounds/overlap rejection, synthetic ordered/full/invalid snapshot decode,
fresh CLI determinism and no-output-on-failure. Existing9 candidate generation
inputs and both-fire fragment are unchanged. No second CPU/chip model introduced.

Next after owner reviews: integrate a complete original cooperating diagnostic
cartridge with reviewed activation and exact module tuple, execute through Mars,
and compare actual callbacks/holds/baselines/order/overflow/safe-state continuations.
Mars's independent acceptance programs remain separately authored; this helper
is not a substitute for that independent oracle or a game compatibility test.
