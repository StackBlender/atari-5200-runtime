# Qualified development generations and regression checks

These thirteen original generations have separately attributed bounded independent
native receipts. This catalog does NOT select a provider, approve arbitrary
software, declare a product release or promote candidate flags. Latest native
receipt is the character-bank variant (Mars938d829/msg_d02f); older native qualifications are retained, not
rerun by the offline tool. See independent-execution.md for actual evidence.

|Variant|Full source generation|Image SHA256|
|---|---|---|
|startup|`711a2e986f7906f45aebd310e6330fd7ffc338bf`|`b2d8ebb8d0070f2aee1bd79d7adfee85b88797702cb96035ab3a18e9bd37f68d`|
|vbi|`ba90c8550c1be1c85b5aa7d6810e1ee6c6031656`|`62df6162ac3accdfa19769c8f2dcd450c510e385fa71f98ec7912f61d449fa54`|
|display|`9d7071f837ec513905b4a2f9718e269c7662b90c`|`1992e64b05d096e479c9532b14a77839bad182428b459a3ca8862ede51acb364`|
|dli|`258bc0cc764a0614ec8443a89d242a8f1fe8cb5e`|`374465be3cfce3d15c10c7899f4fedbd8cf854b23ee1734b9302c7049e55e05c`|
|analog|`a6c406e4cee090b8044eea3b9b6c7a5b6391b3ab`|`32343a567399b3b4f9c142bde446fe89397267267d51a89393553fdab9471290`|
|irq|`42762a73a0caa72b7753bd5aa4380cf9a63c573f`|`2b257c582044af2308699c6a0f327dca674ed79bd95eed2da7cea2537ead0675`|
|timer|`ac9b47e50c213b08022e78bdef64662569cd3d29`|`eae07d3610237c96d3cdf11959680eb25ed59dd6083c0de59d4c999188057550`|
|keypad-irq|`b2e2b40d8c11326f1684635e35832fcc50f9f2d6`|`2fa0cbdbace0d70bab06953fef5bf08e065c6c6247a8a67692718307e75d6ef8`|
|keypad-window|`fce294b7448a7c5a1a35e6c5e5ed5611ee36473f`|`3c1b419b9af94645ea537126d21e464f90f05013689ef7132656680d62d4207a`|
|fire|`a2a7455627a9ea3905464c295562debee2efec7d`|`e937064b0d1fe33d0f75cfe4dba89bcbec953adc215f83ed51ce4fee8705f815`|
|fire-bridge|`e25a466d15c574f3ec364bfc2f44bc7ef2f51117`|`c5fd8df1564c28e5ed4c5aad9f8eabdc64a62e32de28e8dcce6bfae7ea533d24`|
|opaque-title|`ed013540ac2996d76fab149f6fb8dea9fcead584`|`8d6ef38c1b487fa95742e62e9a5c0b1a928ddb446977264739a263fa0bc070c4`|
|character-bank|`46b485ddff275af0f66b29b5a2388f8668cc9e11`|`c7caa810132d16ae55b75077e6d5138b5ad388a0094cedaee1eee091cb4a6598`|

`tools/verify_accepted_exports.py` executes each real pinned exporter, whose own
checkout preflight verifies every declared generation input against local Git.
It compares retained image digests, exact2048-byte descriptors, full source pins,
map digest/symbol bindings, empty accepted capabilities and false execution/
provider/retail/timing flags. No old input is edited or grandfathered by size.
All source pins must exist in this repository's local history. No network,
firmware, emulator, CPU/device run, cache override or automatic fetch is supplied.

```sh
python3 tools/verify_accepted_exports.py
python3 tools/verify_accepted_exports.py --cmake
```

The second command also creates a temporary parent CMake project for the exact
character-bank target, verifies the dependency is built before a real downstream consumer,
checks all four absolute artifact/full-source properties and compares image/map/
manifest bytes with the CLI export. Temporary sources/build/artifacts are removed.
Requires CMake3.20+ and Ninja in addition to Python/Git; no compiler needed.

The normal unittest/CTest suite now includes the real thirteen-export/CMake check,
plus independently constructed invalid source/descriptor/map/symbol/capability/
flag/image cases.197methods total. This replaces earlier disposable per-slice
harnesses. Add future reviewed generations explicitly without rewriting old pins,
hashes or approval labels. New native identities still require owner qualification;
a passing export check cannot provide it.
