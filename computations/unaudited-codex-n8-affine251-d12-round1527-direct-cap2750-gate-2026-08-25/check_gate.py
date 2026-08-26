#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTROL = ROOT / "control_cap2500"
CANDIDATE = ROOT / "candidate_cap2750"


def require(condition, message):
    if not condition:
        raise SystemExit("FAIL: " + message)


def load(path):
    with path.open("rb") as handle:
        return json.load(handle)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(8 << 20)
            if not block:
                return h.hexdigest()
            h.update(block)


def normalized_result(value):
    value = json.loads(json.dumps(value))
    for key in (
        "column_cap", "checkpoint", "vector_cache", "dual", "elapsed_seconds",
        "restore_seconds", "vector_cache_write_seconds", "peak_rss_kib",
    ):
        value.pop(key, None)
    for row in value.get("rounds", []):
        for key in ("incident_seconds", "materialize_seconds", "solve_seconds"):
            row.pop(key, None)
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-only", action="store_true")
    parser.add_argument("--expected-control-cap", type=int, default=2_500_000)
    parser.add_argument("--expected-candidate-cap", type=int, default=2_750_000)
    args = parser.parse_args()

    control = load(CONTROL / "result.json")
    candidate = load(CANDIDATE / "result.json")
    control_watchdog = load(CONTROL / "watchdog.json")
    candidate_watchdog = load(CANDIDATE / "watchdog.json")

    for name, result, watchdog, cap in (
        ("control", control, control_watchdog, args.expected_control_cap),
        ("candidate", candidate, candidate_watchdog, args.expected_candidate_cap),
    ):
        require(result.get("status") == "INCOMPLETE_SEARCH_CAP", name + " result status")
        require(result.get("incomplete_reason") == "ROUND_CAP", name + " reason")
        require(result.get("rounds_completed") == 1527, name + " round")
        require(result.get("column_cap") == cap, name + " cap")
        require(result.get("strategy") == "cold", name + " strategy")
        require(result.get("pivot_mode") == "rare", name + " pivot")
        require(result.get("elimination_kernel") == "hierarchical", name + " kernel")
        require(result.get("workers") == 16, name + " workers")
        require(result.get("incremental_basis") is False, name + " incremental flag")
        require(watchdog.get("status") == "PASS", name + " watchdog status")
        require(watchdog.get("returncode") == 0, name + " return code")
        require(watchdog.get("breach") is None, name + " watchdog breach")
        require(watchdog.get("atomic_outputs_clean") is True, name + " atomic outputs")
        require(watchdog.get("peak_rss_kib", 1 << 60) < 36 * (1 << 20), name + " RSS")
        require(watchdog.get("source_sha256") == "3139689fb546aa1233a366e2dfa1dc007ea2f13399b89c951181d28636f43f59", name + " source pin")
        require(watchdog.get("binary_sha256") == "79410bc8f73f2e486c97749a446c1ee7cf6e96982cd2c6fbe54619b60f675048", name + " binary pin")
        require(watchdog.get("watchdog_sha256") == "48fe528b15c31b8ed6446eb10628b0bcb598191efaac64dd59021881b80b1522", name + " watchdog pin")

    require(control["column_orbits_exposed"] == candidate["column_orbits_exposed"] == 2_400_337, "column equality")
    require(control["dual_support"] == candidate["dual_support"] == 3_389, "support equality")
    require(normalized_result(control) == normalized_result(candidate), "normalized semantic equality")

    output = {
        "status": "PASS_METADATA" if args.metadata_only else "PASS_EXACT_BYTE_EQUIVALENCE",
        "round": 1527,
        "columns": 2_400_337,
        "dual_support": 3_389,
        "control_cap": args.expected_control_cap,
        "candidate_cap": args.expected_candidate_cap,
        "normalized_semantics_equal": True,
    }
    if not args.metadata_only:
        control_checkpoint = digest(CONTROL / "checkpoint.bin")
        candidate_checkpoint = digest(CANDIDATE / "checkpoint.bin")
        control_cache = digest(CONTROL / "vectors.bin")
        candidate_cache = digest(CANDIDATE / "vectors.bin")
        require(control_checkpoint == candidate_checkpoint, "checkpoint byte equality")
        require(control_cache == candidate_cache, "cache byte equality")
        output.update({
            "checkpoint_sha256": control_checkpoint,
            "vector_cache_sha256": control_cache,
            "checkpoint_byte_equal": True,
            "vector_cache_byte_equal": True,
        })
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
