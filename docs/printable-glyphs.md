# Original standalone printable glyphs

`tools/printable_glyphs.py` authors95 printable ASCII glyph drawings (32..126)
as5-column rows within8x8 cells. The source contains explicit original ink/paper
geometry; the tool only packs those coordinates into bytes. Letters/digits occupy
seven rows; descenders for g/j/p/q/y use the eighth. x0/x6/x7 are always paper.
The space is empty; all other characters have ink and all95 cells are distinct.

No external font, Atari bitmap/logo/table, firmware or replacement kernel was
consulted. This is newly authored artwork, not a traced or extracted font. Prior
runtime seven-segment digit assets and every accepted generation remain intact.

Output is760 bytes in ASCII order with8 bytes per character. This is NOT an
Atari screen-code table,1024-byte firmware bank, runnable image, provider target
or full character-compatibility claim. The JSON explicitly leaves runtime ABI,
Atari encoding and bank address null, with empty capabilities/false approvals.

Generate ignored assets using the existing build root:

```sh
python3 tools/printable_glyphs.py --output-dir build/printable-glyphs
```

Six independent test methods cover the exact repertoire, cell boundary bits,
distinct shapes, selected expected letter/digit/punctuation bytes, descenders,
malformed drawings/repertoire failures, source/output identity and fresh-process
reproducibility. They also freeze the accepted bridge image hash and90-byte
reserve. Geometry tests establish authored assets, not ANTIC execution.

Before any bank binding, review consumer encoding, ANTIC2/6/7 glyph addressing,
color and inverse/CHACTL behavior, placement and actual glyph repertoire needed
by ordinary software. Keep the current mode2 digits50..59 semantics distinct
from mode6's consumer encoding. Do not guess missing numeric mappings from
macro names. Require a separately identified generation, unchanged2048-byte fit,
full inherited native CPU/peek/DMA/pixel/state/refusal checks and old export
reproduction. Original shape may differ aesthetically from manufacturer artwork;
this does not waive functional character/graphics requirements.

## Declarative oracle data

The JSON now includes geometry.glyphs:95ASCII label keys, each with8explicit
8-pixel '.'/'#' rows, top-to-bottom/MSB-left. This exposes original asset DESIGN
DATA to independent native fixture authors without reading generator/test code.
No glyph byte changes: SHA256674bd8776ac83d517654b3d6ca2720e5b6d69f5e084c2bd35052c19c074f547a.
A seventh test independently packs the declared rows and confirms all760bytes.
All Atari binding/ABI/bank fields remain null, no provider/image is emitted.
See character-bank-proposal.md for the separately UNAPPROVED64cell bank plan.
