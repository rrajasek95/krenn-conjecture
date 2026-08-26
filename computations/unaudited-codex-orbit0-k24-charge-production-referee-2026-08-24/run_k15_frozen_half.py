#!/usr/bin/env python3
"""Frozen, non-overwriting launcher for exactly one grouped-K15 K24 half."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/run_k24_charge_direct_k15.rs"
BINARY = HERE / "run_k24_charge_direct_k15_literals_v2"
VALIDATOR = HERE / "validate_merge_k15_fast.py"
REFEREE = HERE / "referee_k24_k15_contract_v1"
SOURCE_SHA = "594701a258a9b9be9b6ec4516ba683eb758b3c4c026ce66b982899d17b2596c9"
BINARY_SHA = "230918d02643e1cdc87c6de3e2f0d4a89ac37099a8449d42d8a3e6b063639b57"
VALIDATOR_SHA = "cbbb292381afe64f68ee12814d8632f486a0d49a7df094dfa95d4f573afe7747"
REFEREE_SHA = "e9a79c20293bfaee79b1b421de95444e896ec5be93e8d0719856c5d1d7539b96"
HALVES = {0: (0, 242), 1: (242, 485)}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_atomic(path: Path, payload: dict) -> None:
    temp = Path(str(path) + ".tmp")
    temp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temp.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", type=int, choices=(0, 1), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--literal-report", type=Path, required=True)
    parser.add_argument("--provenance", type=Path, required=True)
    args = parser.parse_args()
    samples = Path(str(args.output) + ".samples.tsv")
    targets = [args.output, samples, args.validation, args.literal_report, args.provenance]
    require(len(set(map(str, targets))) == len(targets), "K15 launch outputs must be distinct")
    require(all(not target.exists() for target in targets), "K15 launcher refuses to overwrite an output")
    pins = {SOURCE: SOURCE_SHA, BINARY: BINARY_SHA, VALIDATOR: VALIDATOR_SHA, REFEREE: REFEREE_SHA}
    for path, expected in pins.items():
        require(path.is_file() and sha256(path) == expected, f"frozen K15 pin mismatch: {path}")
    start, end = HALVES[args.shard]
    command = [
        str(BINARY), "--start-slice", str(start), "--count-slices", str(end - start),
        "--workers", "8", "--output", str(args.output),
    ]
    begun_utc = datetime.now(timezone.utc).isoformat()
    begun = time.monotonic()
    producer = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elapsed = time.monotonic() - begun
    require(producer.returncode == 0, f"K15 frozen producer failed: {producer.stderr}")
    require(args.output.is_file() and samples.is_file(), "K15 producer did not publish both atomic outputs")
    validation_command = [
        sys.executable, str(VALIDATOR), "shard", "--result", str(args.output),
        "--samples", str(samples), "--start", str(start), "--end", str(end),
        "--output", str(args.validation),
    ]
    validated = subprocess.run(validation_command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(validated.returncode == 0, f"K15 shard structural validation failed: {validated.stderr}")
    replay_command = [
        str(REFEREE), "--family", "k15", "--samples", str(samples),
        "--output", str(args.literal_report),
    ]
    replayed = subprocess.run(replay_command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(replayed.returncode == 0, f"K15 shard literal replay failed: {replayed.stderr}")
    validation = json.loads(args.validation.read_text())
    literal = json.loads(args.literal_report.read_text())
    expected_bins = 128 if args.shard == 0 else 129
    require(validation.get("status") == "PASS_K24_K15_FROZEN_HALF_STRUCTURE", "K15 validation report status")
    require(literal.get("status") == "PASS_INDEPENDENT_K24_LITERAL_REPLAY" and literal.get("family") == "k15", "K15 literal report status")
    require(int(literal.get("witnesses_replayed")) == 2 * expected_bins and int(literal.get("distinct_group_bins")) == 2 * expected_bins, "K15 shard literal replay coverage")
    provenance = {
        "status": "PASS_FROZEN_K24_K15_HALF_PRODUCTION_AND_INDEPENDENT_REPLAY",
        "shard": args.shard, "slice_interval": [start, end], "source_slices": end - start,
        "workers": 8, "external_alarm_required_seconds": 540,
        "source_path": str(SOURCE.relative_to(ROOT)), "source_sha256": SOURCE_SHA,
        "binary_path": str(BINARY.relative_to(ROOT)), "binary_sha256": BINARY_SHA,
        "validator_path": str(VALIDATOR.relative_to(ROOT)), "validator_sha256": VALIDATOR_SHA,
        "literal_referee_path": str(REFEREE.relative_to(ROOT)), "literal_referee_sha256": REFEREE_SHA,
        "producer_argv": command, "producer_stdout_sha256": hashlib.sha256(producer.stdout.encode()).hexdigest(),
        "producer_stderr": producer.stderr, "producer_elapsed_seconds": elapsed,
        "started_utc": begun_utc, "finished_utc": datetime.now(timezone.utc).isoformat(),
        "result_sha256": sha256(args.output), "samples_sha256": sha256(samples),
        "validation_sha256": sha256(args.validation), "literal_report_sha256": sha256(args.literal_report),
        "literal_witnesses_replayed": int(literal["witnesses_replayed"]),
        "grouped_scalar_once": True, "covered_ids": 6, "scalar_groups": 2,
        "complete_k24_claim": False,
    }
    write_atomic(args.provenance, provenance)
    print(json.dumps({"status": provenance["status"], "shard": args.shard, "elapsed_seconds": elapsed}))


if __name__ == "__main__":
    main()
