# Proposed first64-cell original character bank

C continuation after Mars1afec85/f20996c. **Proposal only: no numeric bank binding,
provider or image authoring is approved by this document.** Aopaque-title native
qualification and Bordinary-profile/keyIRQ requirements remain separate gates.

## Screened source and limits

Atari Inc.,1982, *Atari400/800 Home Computer System Hardware Manual*, selected
manufacturer prose: II.13,II.15,II.17 and III.4..6. [Archived123-page scan](https://www.atarimania.com/documents/atari-400-800-hardware-manual.pdf);
[manufacturer-text transcription](https://manualzz.com/doc/9258442/atari-400-800-home-computer-system-hardware-manual).
Only title/frontmatter/contents and selected prose/register descriptions were
read. Source IV sample program and font/pixel images were not consulted; adjacent
published display-list examples/diagram labels appeared in extracted context,
not copied. The scan's screenshot interface returned no usable image content;
this is OCR/transcription screening, NOT visual verification of the scan.

Documentary facts, not5200BIOS observations:40-column character modes use128
eight-byte cells/1KiB alignment;20-column modes64cells/512-byte alignment.
Mode6 uses8display rows,7repeats rows to16. Upper screen bits select playfield
colors in6/7; clear pixels use background. CHACTLbit2 reflects vertically;
bits1/0 control inverse/blank for high-bit names in2/3, together producing solid.
CHBASE drops the low1or2page bits. OCR numeric tables contain visible errors
(e.g. a512-byte entry rendered212); use unambiguous prose, not damaged table digits.

This is home-computer ANTIC documentation. Do not import its OS shadows, E000
font address, POKEY aliases, reset policy or character ROM into5200. Existing
5200 register declarations/Mars model prose corroborate the shared hardware
constraints; board/retail font equivalence remains unmeasured. No general ATASCII
mapping or glyph shape is inferred. Secondary search snippets (Xmission ANTIC,
Altirra/Wikipedia/mirrors) were seen but not opened/used as numeric authority.

## Proposed original software policy

Bind only64cells in the first512bytes of our existing1024-byte F800font region:

|Region|Proposed contents|
|---|---|
|F800..F9FF,index0..63|ASCII labels32..95 map to indexASCII-32; own geometry below|
|First-bank indices10..19 hex|Existing ORIGINAL seven-segment digits0..9, retaining their geometry|
|Other first-bank cells|The54 corresponding drawings from the standalone originalASCII asset, including space|
|FA00..FBFF,index64..127|Byte-identical parent high bank, including legacy mode2digits50..59|
|FC00..FFFF|Entire code, branches, vectors, padding and reserve byte-identical to separately approved parent|

This is a deliberately proposed development mapping, NOT evidence of historical
5200/ATASCII/cc65 alphabetic encoding. Only64of95ASCII labels are bound; lowercase
and the remaining standalone glyphs remain unbound. The ten standalone digit
drawings are not substituted for existing seven-segment digits. Do not claim a
95glyph font fits64slots. Full graphics/control/retail charset work stays open.

The existing accepted numeric metadata convention gives encoded digits50..59.
For mode6/7 their low6bits are10..19; adding the own first-bank digit aliases
therefore follows already accepted consumer digits plus hardware indexing.
Mode2legacy50..59 addressesFA80..FACF remain unchanged. First-bank digit cells
would occupyF880..F8CF. This arithmetic does not derive an alphabetic convention.
The ASCII-32 letter policy above requires its own explicit owner approval.

All first-bank cells fitF800..F9FF; no extra ROM is allocated. Existing allocation
already counts the entire1024-byte font, so total1895written/fire146of160/90reserve
would remain unchanged. No RAM/stack/native-field/IRQ/service expansion. Actual
emitted comparison and new exact source/image/map/manifest/version still required.
All prior generations/assets/identities remain immutable. Suggested cumulative
parent is opaque-titleed01354 ONLY after its native qualification and a separate
C authoring approval; do not silently change parent or emit now.

## Declarative geometry and independent oracle input

The already approved standalone ASCII asset now reports `geometry.glyphs` as
95ASCII-keyed cells, exactly8rows of8 '.'/'#' pixels, top-to-bottom/MSB-left.
Its760binary bytes remain SHA256
674bd8776ac83d517654b3d6ca2720e5b6d69f5e084c2bd35052c19c074f547a.
Runtime ABI/Atari encoding/bank address stay null, flagsfalse/capabilitiesempty.
This is ORIGINAL asset data for independent fixture authors, not generator/test/
firmware implementation. A consumer can compose pixels without reading Python.
Existing seven-segment geometry is specified separately in startup-brief.md;
recompose it independently instead of deriving an expected image from an emitter.

## Exact register/setup and qualification proposal

Use the existing5200ANTIC/GTIA aliases, static before-DMA setup, GRACTL00,PRIOR00,
no players/missiles or scrolling. Set CHBASEF8 initially; stable CHACTL02 baseline,
then exercise all0..7control combinations without mid-line changes. Set distinct
COLPF0..3/COLBK via their actual public shadows. In2 use PF2paper and PF1luminance
for ink under normal GTIA conditions; in6/7 test all upper2bit color selectors.
Absolute palette/analogTV reproduction is not claimed; independent native pixel
oracles must account for actual GTIA channel rules and converter output format.

Required CPU-bus/peek/DMA/pixel matrix: all256screen bytes in modes2/6/7, all8
CHACTL combinations, all four selector colors and CHBASEF8/F9/FA/FB. Low ignored
CHBASE bits must alias correctly; distinguish the unchanged high bank from the
new first bank. Check glyph edges, all rows, reflected rows,7's repeated rows,
mode2inverse/blank/both-solid and absence of inverse/blank interpretation in6/7.
No new artwork/reference pixels or post-return cache/quiescence shortcuts.

Require a full font-byte comparison against declared own geometry/legacy digits,
preserved high512bytes and all code/vector/reserve bytes, exact fit/provenance,
all old exports, strict new/old refusal before mutation with continuation and
real frame/cache/process snapshots. Retain inherited input/timer/interrupt/R65/
watchdog/OFF/firmware checks; no global timing/battery or ordinary-game claim.
Owner must review source screening/OCR confidence, exact mapping/register/oracle
conditions and approve bounded authoring BEFORE any bank is assembled/admitted.
