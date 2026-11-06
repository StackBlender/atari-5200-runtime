# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Original window-to-event planning model; no CPU/chip/MMIO execution.

Inputs are already acquired contact observations. This cannot establish that
hardware can supply those observations; see docs/keypad-fire-brief.md.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    port: int = 0
    collecting: bool = False
    keys: tuple = (None, None, None, None)
    fires: tuple = (0, 0, 0, 0)
    bottom_ready: bool = False
    top_ready: int = 0


@dataclass(frozen=True)
class Event:
    kind: str
    port: int
    old: object
    new: object


def _integer(value, low, high):
    return type(value) is int and low <= value <= high


def advance(state, *, key=None, top=False, bottoms=(False,)*4, window_valid=True):
    """One eligible VBI boundary: four bottom samples and selected window close.

    key=None means NO NEW CAPTURE during an entire collection window, never a
    stale KBCODE or instantaneous down flag. Caller performs hardware acquisition. Invalid/busy windows defer protected work without release.
    During settling, key/top are ignored. Changed contacts emit one old->new
    transition; repeated captures of a held contact emit nothing. No autorepeat.
    """
    if (type(state) is not State or not _integer(state.port, 0, 3)
            or type(state.collecting) is not bool
            or type(state.keys) is not tuple or len(state.keys) != 4
            or any(k is not None and not _integer(k, 1, 15) for k in state.keys)
            or type(state.fires) is not tuple or len(state.fires) != 4
            or any(not _integer(f, 0, 3) for f in state.fires)
            or type(state.bottom_ready) is not bool
            or not _integer(state.top_ready, 0, 15)):
        raise ValueError("invalid policy state")
    if (type(window_valid) is not bool
            or key is not None and not _integer(key, 1, 15)
            or type(top) is not bool or type(bottoms) is not tuple
            or len(bottoms) != 4 or any(type(b) is not bool for b in bottoms)):
        raise ValueError("invalid acquired observation")
    keys, fires, events = list(state.keys), list(state.fires), []
    for port, bottom in enumerate(bottoms):
        old = fires[port]
        fires[port] = (old & 2) | int(bottom)
        if state.bottom_ready and old != fires[port]:
            events.append(Event("fire", port, old, fires[port]))
    ready = state.top_ready
    if not window_valid:
        return State(state.port, state.collecting, tuple(keys), tuple(fires),
                     True, ready), tuple(events)
    if state.collecting:
        port = state.port
        old = keys[port]
        keys[port] = key
        if old != key:
            events.append(Event("key", port, old, key))
        old = fires[port]
        fires[port] = (old & 1) | (int(top) << 1)
        if ready & (1 << port) and old != fires[port]:
            events.append(Event("fire", port, old, fires[port]))
        ready |= 1 << port
    return State((state.port + int(state.collecting)) & 3,
                 not state.collecting, tuple(keys), tuple(fires), True, ready), tuple(events)
