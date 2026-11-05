# Public consumer-interface evidence

RUNTIME-002 follow-up, 2026-11-05. These are interface declarations made by the
cc65 compiler project, not original Atari measurements or proof of how the
original authors established each address. The declarations are candidates for a
scoped compatibility target. They do not resolve the dated PAM VBI-policy issue,
boot defaults, interrupt timing or the original-system observer/implementer split.

## Source boundary

Reviewed cc65 revision `77b6484615427746e55fda2755c9cbc320a1fb51`:

- [Public Atari target header](https://github.com/cc65/cc65/blob/77b6484615427746e55fda2755c9cbc320a1fb51/include/atari5200.h), SHA-256 `f3e10e04776fcf0e998aa7357bcca9086c714242e491dfe5e338ec6fe0f7632d`.
- [OS data-structure declaration](https://github.com/cc65/cc65/blob/77b6484615427746e55fda2755c9cbc320a1fb51/include/_atari5200os.h), SHA-256 `53494a3052d955eeaede9233f71c4f0fb21b4d06ac742eb24317057b922ef600`.
- [Platform documentation](https://github.com/cc65/cc65/blob/77b6484615427746e55fda2755c9cbc320a1fb51/doc/atari5200.sgml), sections Memory layout, Platform specific header files, Changing the splash screen, SHA-256 `508c0c4f17f5073849784d647002ca0a1a7ee32945369b03a6156b986cb3e77e`.
- [Permissive license](https://github.com/cc65/cc65/blob/77b6484615427746e55fda2755c9cbc320a1fb51/LICENSE), SHA-256 `8e87ae93bbc45dbe3def75c8b20ba2905b052ddf766fe61d55b8e16a807d57f3`; the two headers also carry the permissive notice.

Only declarative headers, the platform document and license were consulted. No
startup routine, kernel, driver, linker implementation, assembler macro, emulator
or foreign test was read or copied. The public platform page displays short
example snippets; they were seen but not transplanted. This records exposure
rather than claiming an entirely Atari-only evidence set. Factual addresses below
are restated; no header implementation or third-party source is vendored.

## Declared address map

`OS` has declared base 0000. Addresses come from explicit declaration annotations,
not host C `sizeof` or alignment. All values remain consumer-interface-unmeasured.
Machine-readable facts and null runtime approval are in
[consumer-interface.json](consumer-interface.json).

| Field / group | Start | Size |
| --- | --- | ---: |
| pokmsk | 0000 | 1 |
| rtclok | 0001 | 2 |
| critic | 0003 | 1 |
| atract | 0004 | 1 |
| sdlst / sdlstl / sdlsth | 0005 | 2 |
| sdmctl | 0007 | 1 |
| pcolr0–pcolr3 | 0008 | 4 |
| color0–color4 | 000C | 5 |
| paddl0–paddl7 | 0011 | 8 |
| vinter | 0200 | 2 |
| vvblki | 0202 | 2 |
| vvblkd | 0204 | 2 |
| vdslst | 0206 | 2 |
| vkeybd | 0208 | 2 |
| vkeypd | 020A | 2 |
| vbrkky | 020C | 2 |
| vbreak | 020E | 2 |
| vserin | 0210 | 2 |
| vseror | 0212 | 2 |
| vseroc | 0214 | 2 |
| vtimr1 | 0216 | 2 |
| vtimr2 | 0218 | 2 |
| vtimr4 | 021A | 2 |

Important scope distinctions:

- The header also declares cc65-owned conio fields at 0019–001C. They are consumer
  storage, not permission for this runtime to enlarge Atari's documented ZP area.
- cc65 documents application RAM beginning at 021C; October PAM reserves through
  021F. Preserve the conservative PAM reservation until this difference is
  reconciled. The probe tool's lower candidate bound remains 0220.
- The `rtclok` array declaration alone does not specify byte order, frequency,
  rollover, interrupt cadence or initialization. Vector names do not supply the
  target addresses, save/restore sequence or startup handlers.
- `sdlst` aliases two bytes; it is not an extra allocation. Shadows do not specify
  which hardware writes are safe or when each must be transferred.

The public target header declares GTIA at C000, POKEY at E800, ANTIC at D400.
These are address aliases only. Register-specific effects, read/write aliases,
ordering and numerical reset values remain outside this evidence packet.

## Metadata and diagnostic direction

The platform documentation describes a 20-byte title and two year bytes; its
examples express displayed digits using ASCII digit plus 32. It describes a
second-year-byte FF diagnostic bypass. These establish what this public consumer
document says, not an approved Atari initialization path. Do not use that bypass
to evade runtime startup or to claim normal game compatibility.

A future original diagnostic can use a deliberately authored digits-only title,
normal year bytes and the primary PAM CPU-mapped entry pointer. This avoids
copying artwork or a manufacturer's title. Review that narrowly defined encoder
and profile before assembling the complete cartridge; alphabetic encoding and
full runtime font placement still need separate evidence. No runnable diagnostic
cartridge or runtime service is added by this packet.

## Review decision and next contract

Mars review `1f411e5` (msg_001a / req_6f74) accepts the pinned declarations as an
explicit development interface, proposed name `sb52-dev-cc65-v1`, with authority
consumer-interface-unmeasured. Further historical provenance is not required
merely to target those declarations. This accepts field/vector slot layout for
that limited scope, not handlers, defaults, retail compatibility or a completed
clean-room claim. No runtime policy, shipping profile or provider is selected.

The digits-only convention is accepted as our explicit original policy:
`encode(d) = ASCII(d) + 32`, digits 0–9 map to 50–59 hex. Use exactly 20 authored
title digits and two normal year digits; no FF diagnostic bypass. The complete
cartridge brief must specify CPU-mapped metadata and little-endian entry encoding,
original glyph/mode/color mapping and result ownership. No alphabetic or historic
font-address inference follows. The conservative vector reservation and conio
exclusion remain; stock cc65 binaries are not promised unrestricted compatibility.

Next supply a bounded startup brief with exact named reset/MMIO writes and order,
entry/SP/interrupt/vector/RAM policy, original assets, and negative/unsupported
cases. Unspecified retail defaults can be replaced by explicitly approved original
policy for this development scope. Each future service still needs its own
supported contract and independent fixtures; original-system access/role/protocol
requirements remain for measured reference work.
