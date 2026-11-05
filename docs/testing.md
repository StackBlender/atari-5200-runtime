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

The CTest entry runs 35 Python test methods (17 image-emitter, four capture
fragment and 14 scalar-record tests). Independent expected instruction
bytes cover symbolic forward/backward resolution, little-endian addresses,
branch limits -128/127 and rejection at -129/128. Negative cases cover overlap,
allocation bounds, writes to reserved space, operand overflow, duplicate/undefined/
unwritten/non-executable targets, missing/repeated vectors and unsupported modes.
Fresh subprocesses emit identical image/report files in separate temporary paths.

`build/generated/layout-test.bin` is exactly 2048 bytes with ten written bytes;
`layout-test.json` reports its hash, symbols and budget. This is a build-tool
fixture with no runtime capabilities, not a usable BIOS replacement. Test reports
establish encoding/layout/reproducibility only. No CPU execution, startup, hardware
service, original-BIOS compatibility or game result is covered.

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
