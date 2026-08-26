#!/usr/bin/env python3
"""Read-only integrity audit of the frozen grouped-K15 K24 production contract."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCHEDULE = HERE / "results_k15_two_half_schedule_audit.json"
CONTRACT = HERE / "k24_charge_referee_contract.json"
HOSTILE = HERE / "results_k15_two_half_contract_hostile_selftest.json"
OUTPUT = HERE / "results_k15_two_half_contract_integrity_audit.json"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    schedule = json.loads(SCHEDULE.read_text())
    contract = json.loads(CONTRACT.read_text())
    hostile = json.loads(HOSTILE.read_text())
    producer = schedule["producer"]
    for key, hash_key in (("source_path", "source_sha256"), ("binary_path", "binary_sha256")):
        path = ROOT / producer[key]
        require(path.is_file() and sha256(path) == producer[hash_key], f"K15 {key} pin")
    for section, path_key, hash_key in (
        ("launcher", "path", "sha256"),
        ("merger", "path", "sha256"),
        ("literal_referee", "dedicated_binary_path", "dedicated_binary_sha256"),
    ):
        pin = schedule[section]
        path = ROOT / pin[path_key]
        require(path.is_file() and sha256(path) == pin[hash_key], f"K15 {section} pin")
    fast = contract["producer_sources"]["fast_k15_charge_only"]
    require(fast["sha256"] == producer["source_sha256"] and fast["binary_sha256"] == producer["binary_sha256"], "K15 contract/producer pins")
    require(fast["production_partition"] == [[0, 242], [242, 485]], "K15 contract partition")
    require(schedule["groups"] == contract["families"]["k15"]["groups"], "K15 exact DAG groups")
    require(sum(map(len, schedule["groups"].values())) == 6 and len(schedule["groups"]) == 2, "K15 exact six-ID/two-group coverage")
    intervals = [item["slice_interval"] for item in schedule["schedule"]]
    require(intervals == [[0, 242], [242, 485]], "K15 exact half order")
    require(all(item["projected_seconds"] < 540 for item in schedule["schedule"]), "K15 half wall projection")
    require(sum(item["source_slices"] for item in schedule["schedule"]) == 485, "K15 no-gap source total")
    require([item["expected_literal_bins_per_group"] for item in schedule["schedule"]] == [128, 129], "K15 half bin partition")
    require(hostile["status"] == "PASS_K24_K15_TWO_HALF_CONTRACT_HOSTILE_SELFTEST" and hostile["case_count"] == 30, "K15 hostile suite")
    require(all(case["observed_returncode"] == 0 for case in hostile["cases"] if case["expected"] == "PASS"), "K15 hostile positive controls")
    require(all(case["observed_returncode"] != 0 for case in hostile["cases"] if case["expected"] == "REJECT"), "K15 hostile rejection controls")
    report = {
        "status": "PASS_K24_K15_TWO_HALF_CONTRACT_INTEGRITY_AUDIT",
        "schedule_sha256": sha256(SCHEDULE), "contract_sha256": sha256(CONTRACT),
        "producer_source_sha256": producer["source_sha256"],
        "producer_binary_sha256": producer["binary_sha256"],
        "launcher_sha256": schedule["launcher"]["sha256"],
        "merger_sha256": schedule["merger"]["sha256"],
        "literal_referee_binary_sha256": schedule["literal_referee"]["dedicated_binary_sha256"],
        "strict_covered_ids": 6, "strict_scalar_groups": 2,
        "intervals": intervals, "no_gap": True, "no_overlap": True,
        "projected_seconds": [item["projected_seconds"] for item in schedule["schedule"]],
        "literal_bins_per_group_after_merge": 257,
        "literal_witnesses_after_merge": 514,
        "hostile_cases": hostile["case_count"],
        "production_launched": False,
        "launch_decision": schedule["launch_decision"],
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"]}))


if __name__ == "__main__":
    main()
