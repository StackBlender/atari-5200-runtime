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

The one CTest entry runs 17 Python test methods. Independent expected instruction
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
