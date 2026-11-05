# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""All records here are invented test inputs, never original-system observations."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from entry_probe import capture_fragment
from observations import RecordError, read_record, validate_record, verify_cartridge


def synthetic_record():
    _, manifest = capture_fragment(0x8000, 0x3000)
    artifact = {name: manifest[name] for name in
                ("entry_address", "result_start", "source_sha256", "encoder_sha256", "fragment_sha256")}
    artifact["cartridge_sha256"] = "0" * 64  # No actual cartridge/reference result.
    return dict(schema=1, probe="ENTRY-01", kind="synthetic", observation_id="test-only",
                observer="synthetic-test", recorded_at="2026-11-05T00:00:00Z",
                machine=dict(model="ntsc-four-port", board_revision="unmeasured",
                             firmware_revision="unmeasured"),
                approval_refs=dict(access=None, operator=None, roles=None, result_area=None, protocol=None),
                artifact=artifact, trials=[dict(trial_id=1, reset_kind="cold-power", held_inputs=[],
                    steps=[dict(action=action, duration_ms=0) for action in
                           ("power-off", "power-on", "observe-completion-write", "read-six-scalars")],
                    raw=dict(a=0x12, x=0x34, y=0x56, p_pushed=0xFF, sp=0x80, complete=0xA5),
                    completion_write_observed=True, interruption="none-observed")])


class ObservationTests(unittest.TestCase):
    def assertRejected(self, record):
        with self.assertRaises(RecordError):
            validate_record(record)

    def test_synthetic_normalization_without_evidence_claim(self):
        record = synthetic_record()
        original = copy.deepcopy(record)
        result = validate_record(record)
        self.assertEqual(record, original)
        self.assertEqual(result["kind"], "synthetic")
        for field in ("evidence_approved", "original_measurement_claim", "approval_refs_verified",
                      "cartridge_hash_verified", "runtime_policy_selected"):
            self.assertFalse(result[field])
        self.assertEqual(result["trials"][0]["normalized"],
                         dict(a=0x12, x=0x34, y=0x56, sp=0x80, p_known=0xCF, p_known_mask=0xCF))
        self.assertTrue(result["trials"][0]["usable_for_protocol_review"])

    def test_pushed_nonobservable_bits_never_promoted(self):
        for value in (0, 0x10, 0x20, 0x30):
            record = synthetic_record()
            record["trials"][0]["raw"]["p_pushed"] = value
            self.assertEqual(validate_record(record)["trials"][0]["normalized"]["p_known"], 0)

    def test_raw_bytes_strict_and_bounded(self):
        for field in ("a", "x", "y", "p_pushed", "sp", "complete"):
            for value in (-1, 256, True, 0.0, "255", [0], None):
                record = synthetic_record()
                record["trials"][0]["raw"][field] = value
                with self.subTest(field=field, value=value):
                    self.assertRejected(record)

    def test_unknown_fields_and_dump_attempts(self):
        for path in ((), ("machine",), ("artifact",), ("approval_refs",),
                     ("trials", 0), ("trials", 0, "raw"), ("trials", 0, "steps", 0)):
            record = synthetic_record()
            target = record
            for key in path:
                target = target[key]
            target["firmware_bytes"] = [0] * 16
            with self.subTest(path=path):
                self.assertRejected(record)
        record = synthetic_record()
        record["trials"][0]["raw"] = [0] * 6
        self.assertRejected(record)

    def test_missing_keys_types_and_versions(self):
        for field in synthetic_record():
            record = synthetic_record()
            del record[field]
            self.assertRejected(record)
        for field, value in (("schema", True), ("schema", 2), ("probe", "ROM-DUMP"),
                             ("kind", "verified"), ("kind", []), ("observer", "a b"),
                             ("observation_id", "x" * 65), ("recorded_at", "2026-02-30T00:00:00Z"),
                             ("recorded_at", "2026-11-05")):
            record = synthetic_record()
            record[field] = value
            self.assertRejected(record)

    def test_reference_receipts_are_required_but_not_authenticated(self):
        record = synthetic_record()
        record["kind"] = "original-reference"
        self.assertRejected(record)
        record["approval_refs"] = {name: "test-receipt" for name in record["approval_refs"]}
        report = validate_record(record)
        self.assertFalse(report["approval_refs_verified"])
        self.assertFalse(report["evidence_approved"])
        self.assertFalse(report["original_measurement_claim"])

    def test_artifact_identity_mismatch(self):
        for field in ("source_sha256", "encoder_sha256", "fragment_sha256"):
            record = synthetic_record()
            record["artifact"][field] = "0" * 64
            with self.subTest(field=field):
                self.assertRejected(record)
        for value in ("abc", "A" * 64, True, []):
            record = synthetic_record()
            record["artifact"]["cartridge_sha256"] = value
            self.assertRejected(record)
        for field, value in (("entry_address", 0xBFCF), ("result_start", 0x21F)):
            record = synthetic_record()
            record["artifact"][field] = value
            self.assertRejected(record)

    def test_trial_limits_and_identity(self):
        for trials in ([], [synthetic_record()["trials"][0]] * 65, {}, None):
            record = synthetic_record()
            record["trials"] = trials
            self.assertRejected(record)
        record = synthetic_record()
        record["trials"] *= 2
        self.assertRejected(record)
        record = synthetic_record()
        record["trials"][0]["trial_id"] = True
        self.assertRejected(record)

    def test_reset_and_input_validation(self):
        for field, value in (("reset_kind", "warm-guess"), ("held_inputs", ["unknown"]),
                             ("held_inputs", ["fire-1", "fire-1"]), ("held_inputs", [[]]),
                             ("completion_write_observed", 1), ("interruption", "certain")):
            record = synthetic_record()
            record["trials"][0][field] = value
            self.assertRejected(record)
        for reset in ("cpu-reset", "controller-reset"):
            record = synthetic_record()
            record["trials"][0]["reset_kind"] = reset
            self.assertRejected(record)
            record["trials"][0]["steps"][1]["action"] = reset
            self.assertTrue(validate_record(record)["format_valid"])

    def test_steps_and_observation_order(self):
        for steps in ([], [{}], [dict(action="dump-rom", duration_ms=0)],
                      [dict(action="wait", duration_ms=True)]):
            record = synthetic_record()
            record["trials"][0]["steps"] = steps
            self.assertRejected(record)
        for indices in ((1, 0, 2, 3), (0, 1, 3, 2)):
            record = synthetic_record()
            trial = record["trials"][0]
            trial["steps"] = [trial["steps"][i] for i in indices]
            self.assertRejected(record)

    def test_inconclusive_is_not_silently_usable(self):
        for field, value, reason in (("completion_write_observed", False, "completion-write-not-observed"),
                                     ("interruption", "unknown", "interrupt-window-not-established"),
                                     ("interruption", "observed", "interrupt-window-not-established")):
            record = synthetic_record()
            record["trials"][0][field] = value
            trial = validate_record(record)["trials"][0]
            self.assertFalse(trial["usable_for_protocol_review"])
            self.assertIn(reason, trial["reasons"])
        record = synthetic_record()
        record["trials"][0]["raw"]["complete"] = 0
        self.assertIn("incomplete-marker", validate_record(record)["trials"][0]["reasons"])
        record["trials"][0].update(raw=None, completion_write_observed=False)
        self.assertIsNone(validate_record(record)["trials"][0]["normalized"])
        record["trials"][0]["completion_write_observed"] = True
        self.assertRejected(record)

    def test_bounded_json_duplicate_nonfinite_and_depth_rejection(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            for data in (b'{"schema":1,"schema":1}', b'{"x":NaN}', b'{"x":Infinity}',
                         b'\xff', '{}'.encode('utf-16'), b' ' * 65537, b'[' * 1500 + b']' * 1500):
                path.write_bytes(data)
                with self.subTest(size=len(data)), self.assertRaises(RecordError):
                    read_record(path)
            path.write_text(json.dumps(synthetic_record()))
            self.assertTrue(validate_record(read_record(path))["format_valid"])

    def test_cartridge_size_and_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "original-diagnostic.bin"
            for size in (0, 2048, 32767, 32769):
                path.write_bytes(bytes(size))
                with self.assertRaises(RecordError):
                    verify_cartridge(path, hashlib.sha256(bytes(size)).hexdigest())
            data = bytes(32768)  # Synthetic size/hash fixture, not a runnable cartridge.
            path.write_bytes(data)
            verify_cartridge(path, hashlib.sha256(data).hexdigest())
            with self.assertRaises(RecordError):
                verify_cartridge(path, "0" * 64)

    def test_cli_reports_synthetic_and_rejects_bad_record(self):
        script = Path(__file__).resolve().parents[1] / "tools/observations.py"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.json"
            path.write_text(json.dumps(synthetic_record()))
            result = subprocess.run([sys.executable, str(script), str(path)],
                                    capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["kind"], "synthetic")
            path.write_text('{"schema":1,"schema":1}')
            result = subprocess.run([sys.executable, str(script), str(path)],
                                    capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b"")
            self.assertIn(b"record rejected", result.stderr)
