# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Strict, bounded ENTRY-01 scalar record validation; never evidence approval."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
from entry_probe import COMPLETE, P_MASK, SLOTS, capture_fragment
from emitter import AssemblyError

MAX_BYTES = 65536
MAX_TRIALS = 64
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}\Z")
HASH = re.compile(r"[0-9a-f]{64}\Z")
ARTIFACT_KEYS = {"entry_address", "result_start", "source_sha256", "encoder_sha256",
                 "fragment_sha256", "cartridge_sha256"}
APPROVAL_KEYS = {"access", "operator", "roles", "result_area", "protocol"}
ACTIONS = {"power-off", "power-on", "install-original-cartridge", "wait",
           "cpu-reset", "controller-reset", "set-inputs", "observe-completion-write",
           "read-six-scalars"}
INPUTS = {"fire-1", "fire-2", "start", "pause", "reset", "stick-left",
          "stick-right", "stick-up", "stick-down", "key-star", "key-hash"}
INPUTS.update(f"key-{i}" for i in range(10))


class RecordError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise RecordError(message)


def obj(value, keys, name):
    require(type(value) is dict and set(value) == keys, f"{name}: unexpected or missing keys")


def number(value, low, high, name):
    require(type(value) is int and low <= value <= high, f"{name}: integer outside {low}..{high}")


def token(value, name):
    require(type(value) is str and TOKEN.fullmatch(value) is not None, f"{name}: invalid identifier")


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def reject_constant(_):
    raise RecordError("non-finite JSON number")


def read_record(path):
    # Read only the bounded limit, even for a very large file.
    with Path(path).open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    require(len(data) <= MAX_BYTES, "record exceeds 64 KiB")
    try:
        record = json.loads(data.decode("utf-8"), object_pairs_hook=reject_duplicates,
                            parse_constant=reject_constant)
        pending = [(record, 0)]
        while pending:
            value, depth = pending.pop()
            require(depth <= 8, "JSON nesting exceeds eight levels")
            if type(value) in (dict, list):
                children = value.values() if type(value) is dict else value
                pending.extend((child, depth + 1) for child in children)
        return record
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise RecordError("invalid JSON record") from exc


def validate_record(record):
    obj(record, {"schema", "probe", "kind", "observation_id", "observer", "recorded_at",
                 "machine", "approval_refs", "artifact", "trials"}, "record")
    require(type(record["schema"]) is int and record["schema"] == 1, "unsupported schema")
    require(record["probe"] == "ENTRY-01", "unsupported probe")
    require(record["kind"] in ("synthetic", "original-reference"), "unsupported evidence kind")
    synthetic = record["kind"] == "synthetic"
    token(record["observation_id"], "observation_id")
    token(record["observer"], "observer")
    stamp = record["recorded_at"]
    require(type(stamp) is str and re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", stamp),
            "recorded_at: UTC seconds required")
    try:
        datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise RecordError("recorded_at: invalid date") from exc
    machine = record["machine"]
    obj(machine, {"model", "board_revision", "firmware_revision"}, "machine")
    require(machine["model"] == "ntsc-four-port", "unsupported machine target")
    token(machine["board_revision"], "board_revision")
    token(machine["firmware_revision"], "firmware_revision")
    approvals = record["approval_refs"]
    obj(approvals, APPROVAL_KEYS, "approval_refs")
    for name, value in approvals.items():
        if value is None:
            require(synthetic, f"approval_refs.{name}: reference required")
        else:
            token(value, f"approval_refs.{name}")
    artifact = record["artifact"]
    obj(artifact, ARTIFACT_KEYS, "artifact")
    for name in ARTIFACT_KEYS - {"entry_address", "result_start"}:
        value = artifact[name]
        require(type(value) is str and HASH.fullmatch(value) is not None, f"{name}: invalid SHA-256")
    try:
        _, expected = capture_fragment(artifact["entry_address"], artifact["result_start"])
    except AssemblyError as exc:
        raise RecordError(str(exc)) from exc
    for name in ("source_sha256", "encoder_sha256", "fragment_sha256"):
        require(artifact[name] == expected[name], f"{name}: current probe identity mismatch")
    trials = record["trials"]
    require(type(trials) is list and 1 <= len(trials) <= MAX_TRIALS, "trials: require 1..64")
    seen = set()
    results = []
    for trial in trials:
        obj(trial, {"trial_id", "reset_kind", "steps", "held_inputs", "raw",
                    "completion_write_observed", "interruption"}, "trial")
        trial_id = trial["trial_id"]
        number(trial_id, 0, 65535, "trial_id")
        require(trial_id not in seen, "duplicate trial_id")
        seen.add(trial_id)
        reset = trial["reset_kind"]
        require(reset in ("cold-power", "cpu-reset", "controller-reset"), "invalid reset_kind")
        steps = trial["steps"]
        require(type(steps) is list and 1 <= len(steps) <= 32, "steps: require 1..32")
        actions = []
        for step in steps:
            obj(step, {"action", "duration_ms"}, "step")
            require(type(step["action"]) is str and step["action"] in ACTIONS, "invalid step action")
            number(step["duration_ms"], 0, 3600000, "step duration_ms")
            actions.append(step["action"])
        if reset == "cold-power":
            require("power-off" in actions and "power-on" in actions and
                    actions.index("power-off") < actions.index("power-on"), "cold-power sequence missing")
        else:
            require(reset in actions, "reset stimulus missing")
        held = trial["held_inputs"]
        require(type(held) is list and len(held) <= len(INPUTS), "invalid held_inputs")
        require(all(type(x) is str and x in INPUTS for x in held), "unknown held input")
        require(len(held) == len(set(held)), "duplicate held input")
        require(type(trial["completion_write_observed"]) is bool, "completion event must be boolean")
        interruption = trial["interruption"]
        require(interruption in ("none-observed", "observed", "unknown"), "invalid interruption")
        raw = trial["raw"]
        normalized = None
        reasons = []
        if raw is None:
            require(not trial["completion_write_observed"], "completion event without scalar result")
            reasons.append("no-scalar-result")
        else:
            obj(raw, set(SLOTS), "raw")
            for name, value in raw.items():
                number(value, 0, 255, f"raw.{name}")
            if raw["complete"] != COMPLETE:
                reasons.append("incomplete-marker")
            normalized = {name: raw[name] for name in ("a", "x", "y", "sp")}
            normalized.update(p_known=raw["p_pushed"] & P_MASK, p_known_mask=P_MASK)
        if not trial["completion_write_observed"]:
            reasons.append("completion-write-not-observed")
        else:
            require("observe-completion-write" in actions and "read-six-scalars" in actions and
                    actions.index("observe-completion-write") < actions.index("read-six-scalars"),
                    "completion observation/read sequence missing")
            trigger = "power-on" if reset == "cold-power" else reset
            require(actions.index(trigger) < actions.index("observe-completion-write"),
                    "completion observation precedes reset stimulus")
        if interruption != "none-observed":
            reasons.append("interrupt-window-not-established")
        results.append(dict(trial_id=trial_id, usable_for_protocol_review=not reasons,
                            reasons=reasons, normalized=normalized))
    return dict(schema=1, probe="ENTRY-01", observation_id=record["observation_id"],
                kind=record["kind"], format_valid=True, evidence_approved=False,
                original_measurement_claim=False,
                approval_refs_verified=False, cartridge_hash_verified=False,
                runtime_policy_selected=False, trials=results)


def verify_cartridge(path, expected_hash):
    # Hash only a bounded original diagnostic image; do not decode its contents.
    with Path(path).open("rb") as stream:
        data = stream.read(32769)
    require(len(data) == 32768, "original diagnostic cartridge must be 32 KiB")
    require(hashlib.sha256(data).hexdigest() == expected_hash, "cartridge SHA-256 mismatch")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--original-diagnostic", type=Path,
                        help="hash-check the operator's locally authored 32 KiB diagnostic")
    args = parser.parse_args()
    try:
        record = read_record(args.record)
        report = validate_record(record)
        if args.original_diagnostic:
            verify_cartridge(args.original_diagnostic, record["artifact"]["cartridge_sha256"])
            report["cartridge_hash_verified"] = True
    except (RecordError, OSError) as exc:
        print(f"record rejected: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
