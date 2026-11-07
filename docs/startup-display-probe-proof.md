<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# Original startup/display diagnostic export receipt

Authoring decision Mars60cb46a/msg_32af under req_6f74. Frozen original source pin
`30968a02ff474a21abcdb19faa8eac12c260c107`. Diagnostic export only: no runtime
image/profile/ABI/provider/CMake/catalog/admission/default/flag change, CPU engine
or private input. Six declared inputs are immutable; later tests/receipts are
noninputs. [Normative oracle contract](startup-display-probe-contract.md) supplies
original geometry and independently declared native expectations.

```sh
python3 -B tools/export_startup_display_probes.py --source-revision 30968a02ff474a21abcdb19faa8eac12c260c107 --output-dir build/startup-display-probes
```

The directory contains twelve binary/descriptor pairs plus index.json, all ignored.
Index raw SHA256 `e9b92f05502a24e317c0926439089e6f22f62b5fb9ed9a489853f80f7f67e74f`.
Full report hashes and source-input identities are in that reproducible index.
Each binary hash is below; regeneration never needs a game, emulator or firmware.

|Case|Bytes|SHA256|
|---|---:|---|
|Linear32K-8000-direct-numeric|32768|`afdecf1b7c24a48b382fb8c0a618b8b8c94a013cc9c84e4bb70c18b7a7fdc7e1`|
|Linear32K-8000-direct-second-ff|32768|`1a5ea8b503704a6c9dbcb45f854824188308d2d9a48b6aad7450c0013f8c68b3`|
|Linear32K-8000-shadow-numeric|32768|`465eda23c8ff3c0f3efc0c7f6863f8447fbe64062fcdaa13aa5f7bc3eaec10dc`|
|Linear32K-8000-shadow-second-ff|32768|`9be664bb038b4e180059755f39f5f92c11545069be17c1f22e593201c560aba4`|
|Linear8K-8000-direct-numeric|8192|`c372a4b2c72207b6f664f16176aae831f7f84432669aa1435ec0be757db880c4`|
|Linear8K-8000-direct-second-ff|8192|`f49eb103f20249ba1c98fab0e1c81ca09bbbbf0a0649f58b491bfdeb91fe5777`|
|Linear8K-8000-shadow-numeric|8192|`aa09fee4acd429bb82114e41cb2db8ad2d05503ecabf6665cd50118ae1d43202`|
|Linear8K-8000-shadow-second-ff|8192|`4f4191488b5dcc44ceb3275143957375d94b17a65955ce77f2c357b42c09f78f`|
|Linear8K-a000-direct-numeric|8192|`87837e1f0fdb12966227069faac6a04a01155eaa7fa50bacc161cbe4ebee946e`|
|Linear8K-a000-direct-second-ff|8192|`a6ca51dd8759f64cefcf26d97bd0552399bdb0be5515d853ae294987f1cb29c1`|
|Linear8K-a000-shadow-numeric|8192|`6f083d7d75cdc6f6cd77b9067e3fc5d57649047ed83deb7a4c698e05bd9d3dab`|
|Linear8K-a000-shadow-second-ff|8192|`e8d51a3931d36943c9ef0c482b87ebc929f1ca652de8bb224a4a2f572487150f`|

## Source inputs and validation

- `docs/startup-display-probe-contract.md`: `0f4bdbad8385e4b8aeaed05ae31646b38712140c3f3cd35571d53d3b82a39444`
- `tools/cartridge_candidate.py`: `68004d44663a62a091adc665cb2de9100f6656e6e903275c4246fa5e29fbbe40`
- `tools/emitter.py`: `7f3f3ff9918a879095c858923692bba49ba106a13e1219997c429835621f39b4`
- `tools/entry_probe.py`: `0d0610f2d34e23722ccad05901b486281e6943131c124b16aa55ceb1ecc60fda`
- `tools/export_startup_display_probes.py`: `eabd0ed0a29de49eed61e53429580ce321fbb6edaf04c4dad691b801fc913a89`
- `tools/startup_display_probe.py`: `bf42fa0d2cdc3aef9ec60abf8636c2663a81f28224bedd2ebbbaf4f08b428997`


Initial8focused tests PASS; after pin, ninth method uses real exporter processes:
all25files equal across two fresh processes,12unique cart hashes/exact sizes,
all descriptor/index/source/runtime bindings, and full prior-source refusal BEFORE
output.9/9 PASS0.247s. Full237offline PASS10.604s; existing build PASS;
CTest1/1 PASS10.63s. Independent literal tests cover all240bitmap bytes, capture/
carry loop/control register ordering, every exact layout/metadata/zero hole,
unsupported boards/aliases/types, no-execution flags and fresh-process outputs.
Six source inputs byte-identical to pin after receipt edits; prior runtime and
Linear8K frozen inputs remain untouched. Tests are encoding/layout evidence,
not native CPU, display, VBI, timing, original hardware or private-game acceptance.

Direct code182bytes, shadow175bytes at8000 or A000; table offsets0400/0500.
Result RAM3000..3009; CPU-initialized list0800..081F and bitmap1000..10EF.
Progress loop80AB/A0ABdirect or80A4/A0A4shadow. First opcodeSTA3000, ready3008=5A,
16-bit counter3006/7. No vector/CRITIC patch, host writes/forced events/fixture
suspension. Direct leaves NMI off and writes display MMIO; shadow initializes
existing ABI shadows then enables ordinary VBI. Require independent trace/source/
clock/PC/MMIO order as well as geometry, not only matching pixels. Runtime common
image remains5936e46d; qualified baseline138fad8/e8. Exact8KiB execution waits
actual new immutable-entry native guard/qualification for source2e8fd51.

Native per-case bound8ordinary returns/external10seconds. Counter/first fetch,
list/bitmap DMA and field-local geometry expectations are declared before any
run. Actual callback viewport origin/canonical RGBA conversion remain UNKNOWN
here; native owner must independently predeclare them, not fit crop/translation
from results. Report exact first unmet condition before any runtime change.
Native execution, source/reference roles, fullR62/product/release remain open.
Both prior private-target permissions stay consumed; no third attempt or repair.


## Subsequent independent32KiB native result

Mars027b703/msg_e942 independently qualifies all FOUR32KiB controls in Release/
unity and full-native Debug/ASan/nonunity. Actual first fetch/progress/data/DMA,
source/clock/MMIO attribution and predeclared raw+converted geometric pixels pass
within exactly8ordinary returns/external10seconds. See [native receipt](startup-display-native-receipt.md).
Original source/contract/report bytes remain frozen; baseline-only observed
viewport/palette facts belong to that separate receipt. Eight exact8KiB cases
remain unrun pending nativeguard/qualification. No failing baseline requirement
or private gameplay proof supports runtime/font/service repair. No release/flags.
