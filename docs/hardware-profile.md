# Reference machine identification

RUNTIME-003 documentary hardware identity, 2026-11-05. Atari's CX5200 Field
Service Manual, section 1, printed pages 1-1 and 1-4 (PDF 9 and 12), distinguishes:

| Board | Documentary description |
| --- | --- |
| CA018087 | Original four-port board |
| CA020108 | Four-port universal board |
| CA021374 | Two-port board |

The manual says its default references concern CA018087 unless noted otherwise.
Therefore `ntsc-four-port` identifies a target family, not a unique board, firmware
revision or measured reset policy. Record the actual board separately in an
ENTRY-01 observation; do not equate board identity with firmware identity.
Unknown identities remain unknown until the operator supplies reviewed evidence.

Source: [Atari field-service manual scan](https://www.atarimania.com/documents/Atari_5200_Field_Service_Manual.pdf),
187 PDF pages, SHA-256
`481b7e5ddedb79c7a099709339ccd5af3f8b6fce82b21e3397a855de773875e0`.
The selected page 1-1 carries the June 21 1983 ECN 0036 revision mark. This dates
that page, not every page in the compiled manual or a retail firmware revision.

Screening: cover/title, contents and low-resolution theory-page index; visually
reviewed PDF 9, 12 and 16 (printed 1-1, 1-4 and 1-8). Those pages describe board
identity, the processor and controller components. No diagnostic cartridge test,
firmware listing, manufacturer boot artwork, wiring procedure or implementation
was used here. The source/render files remain temporary and outside Git.

This evidence does not establish an available operator, approved hardware
procedure, mapped RAM ownership, a CPU-reset apparatus or numerical MMIO defaults.
It improves identification requirements only. Actual controller Reset and physical
CPU reset remain separate protocol stimuli; nothing here authorizes hardware
modification or assumes it makes a new cartridge entry.
