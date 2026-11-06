# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import itertools
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"tools"))
from keypad_policy import State, Event, advance


class KeypadPolicyTests(unittest.TestCase):
    def test_every_key_transition_and_port_isolation(self):
        for port, old, new in itertools.product(range(4), (None, *range(16)), (None, *range(16))):
            keys = [None]*4
            keys[port] = old
            state = State(port=port, collecting=True, keys=tuple(keys))
            result, events = advance(state, key=new)
            expected = () if old == new else (Event("key", port, old, new),)
            self.assertEqual(events, expected)
            self.assertEqual(result.keys[port], new)
            self.assertTrue(all(result.keys[p] is None for p in range(4) if p != port))

    def test_two_boundaries_per_port_and_settle_ignores_stale_observation(self):
        state = State()
        observed = []
        for tick in range(16):
            observed.append((state.port, state.collecting))
            state, events = advance(state, key=9 if tick % 2 == 0 else None, top=True)
            self.assertFalse(any(e.kind == "key" for e in events))
        self.assertEqual(observed, [(p, phase) for _ in range(2) for p in range(4) for phase in (False, True)])
        self.assertEqual(state.keys, (None,)*4)

    def test_held_capture_windows_release_and_repress(self):
        state = State()
        keys = []
        for sample in (5, 5, 5, None, None, 5):
            for _ in range(8):
                state, events = advance(state, key=sample)
                keys.extend(e for e in events if e.kind == "key")
        self.assertEqual(keys, [Event("key", p, None, 5) for p in range(4)]
                         + [Event("key", p, 5, None) for p in range(4)]
                         + [Event("key", p, None, 5) for p in range(4)])

    def test_all_scan_schedule_positions_reach_each_port_in_eight_boundaries(self):
        for starting_port, collecting, target in itertools.product(range(4), (False, True), range(4)):
            state = State(port=starting_port, collecting=collecting)
            delivered = []
            for boundary in range(1, 9):
                state, events = advance(state, key=3)
                delivered.extend(boundary for e in events if e.kind == "key" and e.port == target)
            self.assertEqual(len(delivered), 1)
            self.assertLessEqual(delivered[0], 8)

    def test_four_bottom_fires_each_boundary_with_independent_selected_top(self):
        state, events = advance(State(), bottoms=(True,)*4)
        self.assertEqual(events, ())  # baseline, no invented edges on activation
        state, events = advance(state, top=True, bottoms=(False,)*4)
        self.assertEqual(events, tuple(Event("fire", p, 1, 0) for p in range(4)))
        self.assertEqual(state.fires, (2, 0, 0, 0))
        for _ in range(6):
            state, _ = advance(state)
        state, _ = advance(state)
        state, events = advance(state, top=False, bottoms=(True, False, False, False))
        self.assertEqual(events, (Event("fire", 0, 2, 3), Event("fire", 0, 3, 1)))

    def test_replay_from_every_policy_boundary(self):
        sequence = [dict(key=(i//3)%16 if i%7 else None, top=bool(i%3),
                         bottoms=tuple(bool((i+p)%2) for p in range(4))) for i in range(48)]
        states, outputs, state = [], [], State()
        for sample in sequence:
            states.append(state)
            state, events = advance(state, **sample)
            outputs.append((state, events))
        for start, checkpoint in enumerate(states):
            replay = []
            for sample in sequence[start:]:
                checkpoint, events = advance(checkpoint, **sample)
                replay.append((checkpoint, events))
            self.assertEqual(replay, outputs[start:])

    def test_strict_inputs_refuse_before_state_changes(self):
        state = State()
        for kwargs in ({"key":True}, {"key":-1}, {"key":16}, {"top":1},
                       {"bottoms":[False]*4}, {"bottoms":(False,)*3}, {"bottoms":(0,)*4}):
            with self.assertRaises(ValueError): advance(state, **kwargs)
        for bad in (State(port=True), State(port=4), State(keys=(None,)*3),
                    State(fires=(0, 0, 0, 4)), State(top_ready=16), State(collecting=1)):
            with self.assertRaises(ValueError): advance(bad)
        self.assertEqual(state, State())
