#!/usr/bin/env python3
"""Independent, read-only acceptance audit for the final K16 R4-4 v4 producer."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / "computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24"
FAST = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24"
K16 = ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23"

PINS = {
    FAST / "run_k24_charge_k16_r44.rs": "64c0a6946e5233b8f7d8066ca09fe0670739bdbf60fdca6d5339eabf21f50691",
    REF / "run_k24_charge_k16_r44_support_v4": "6f61d41122a2c1107b97b53cafd94b722118770357bbd6ba2f9bbb292bc333a6",
    K16 / "checkpoint_direct_k16.bin": "93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3",
    FAST / "results_k16_r44_prefix262144.json": "237c4c132ab4f3dfef51ae4ddaad8469b9f28719b90cb13ecbe9c98326e52110",
    REF / "control_k16_r44_distributed262144_support_v4.json": "70b46e4227689be0d12d9ad2603dd9dd8d9b7b6e01198787f3f26cf9d27c0d75",
    REF / "control_k16_r44_distributed262144_support_v4.json.samples.tsv": "3e1dbdc91e17b37d8649917dd7341bc1b74e29f140c7a7317d1da737c9059161",
    REF / "k24_k16_r44_support_candidates.tsv": "57b7f0cfa15b436b6b821922c426f19d15496eb7a1cd64e7e632acaa003d5fbf",
    REF / "results_k16_r44_support_patch_audit.json": "81e58baef547bb4d305de2543ca02e774e84d1b3ad84df706864d732ec7dca12",
    REF / "results_k16_r44_support_patch_hostile_selftest.json": "7b2b59d484572a270861dff48f8fb1cf7fb2024e912f353e34cdc1214b12b10a",
    REF / "results_k24_k16_r44_support_candidates_literal_referee.json": "d0fd9bd271ba8842a1b74f27c226a7fc3b45e46eb68c265d40d1fa8045625319",
    REF / "results_control_k16_r44_support_v4_literal_referee.json": "33666166bfc55b48975fd67548aa515fe604572acc04a42508a073ec5e43adbf",
    REF / "validate_k24_charge.py": "de85f65495427ff5ec95a7d010160a6e72499e1602286a39f5061092cbda9d18",
}

SCALAR = [
    "status", "group_id", "degree", "scale_U", "ids", "covered_ids",
    "individual_id_charges", "record_interval", "records_declared",
    "distributed_prefix", "source_rows", "signed_source_coefficient",
    "l1_source_coefficient", "pivotable_K16_rows", "p1_uses",
    "first_children", "pivotable_intermediate_children", "p2_uses",
    "K24_terminal_occurrences", "full_occurrences", "irreducible_occurrences",
    "full_charge_scaled_U", "irreducible_charge_scaled_U", "m1_m2_hist",
    "terminal_cache", "packet_grouping_guard", "sign_rule", "terminality", "scope",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main() -> None:
    for path, expected in PINS.items():
        assert path.is_file() and sha(path) == expected, (path, sha(path))

    new = json.loads((REF / "control_k16_r44_distributed262144_support_v4.json").read_text())
    old = json.loads((FAST / "results_k16_r44_prefix262144.json").read_text())
    assert all(new[k] == old[k] for k in SCALAR)
    assert new["record_interval"] == [0, 262144]
    assert new["full_charge_scaled_U"] == "-5997775755852840960"
    hist = {int(k): int(v) for k, v in new["nonzero_support_record_hist"].items()}
    assert set(hist) == set(range(37)) and all(v > 0 for v in hist.values())
    assert new["nonzero_support_bins"] == list(range(37))
    assert int(new["nonzero_support_records_outside_bins_0_36"]) == 0
    assert new["candidate_quota_by_support_bin"] == {"0_through_34": 7, "35_through_36": 6}

    candidates = load_tsv(REF / "k24_k16_r44_support_candidates.tsv")
    assert len(candidates) == 257
    assert {int(r["candidate_slot"]) for r in candidates} == set(range(257))
    assert len({int(r["record_index"]) for r in candidates}) == 257
    quota = Counter()
    by_slot = {}
    for r in candidates:
        slot, index, support = int(r["candidate_slot"]), int(r["record_index"]), int(r["support_bin"])
        assert support == min(256, index * 257 // 24097095)
        assert int(r["terminal_q"]) != 0 and int(r["nonzero_contribution_scaled_U"]) != 0
        quota[support] += 1
        by_slot[slot] = r
    assert quota == Counter({**{i: 7 for i in range(35)}, 35: 6, 36: 6})

    bounded = load_tsv(REF / "control_k16_r44_distributed262144_support_v4.json.samples.tsv")
    assert len(bounded) == 7
    for r in bounded:
        c = by_slot[int(r["sample_ordinal"])]
        for field in ("record_index", "coefficient", "source_row", "intermediate_row", "p1", "t1", "p2", "m1", "m2", "terminal_q", "unit_scaled_U", "nonzero_contribution_scaled_U", "final_degree"):
            assert r[field] == c[field], (field, r[field], c[field])

    literal257 = json.loads((REF / "results_k24_k16_r44_support_candidates_literal_referee.json").read_text())
    literal7 = json.loads((REF / "results_control_k16_r44_support_v4_literal_referee.json").read_text())
    assert literal257["status"].startswith("PASS") and literal257.get("witnesses_replayed") == 257
    assert literal7["status"].startswith("PASS") and literal7.get("witnesses_replayed") == 7

    hostile = json.loads((REF / "results_k16_r44_support_patch_hostile_selftest.json").read_text())
    assert hostile["status"] == "PASS_K24_K16_R44_SUPPORT_PATCH_HOSTILE_SELFTEST"
    assert hostile["standard_optimized_isolated"] is True and len(hostile["cases"]) == 18
    for case in hostile["cases"]:
        assert (case["observed"] == 0) == (case["expected"] == "PASS"), case

    src = (FAST / "run_k24_charge_k16_r44.rs").read_text()
    guard = 'assert_eq!(q.nonzero_support_records.keys().copied().collect::<Vec<_>>(), (0u16..37).collect::<Vec<_>>());'
    samples_guard = "assert_eq!(ss.len(), 257)"
    sample_write = 'std::fs::write(&st'
    result_write = 'std::fs::write(&tmp'
    assert src.index(guard) < src.index(samples_guard) < src.index(sample_write) < src.index(result_write)
    assert "record_has_nonzero |= z.0 != 0" in src
    assert "if record_has_nonzero" in src
    assert "nonzero_support_records_outside_bins_0_36" in src

    # There must be no accepted v4 full output at audit time.
    full_candidates = list(FAST.glob("results_k16_r44_complete_v4*.json")) + list(REF.glob("results_k16_r44_complete_v4*.json"))
    assert not full_candidates, full_candidates

    result = {
        "status": "PASS_INDEPENDENT_K24_K16_R44_SUPPORT_V4_RELAUNCH_AUDIT",
        "verdict": "ACCEPT_ONE_FULL_RELAUNCH_AFTER_RESOURCE_CLEARANCE_AND_EXPLICIT_APPROVAL",
        "source_sha256": PINS[FAST / "run_k24_charge_k16_r44.rs"],
        "binary_sha256": PINS[REF / "run_k24_charge_k16_r44_support_v4"],
        "control_sha256": PINS[REF / "control_k16_r44_distributed262144_support_v4.json"],
        "checkpoint_sha256": PINS[K16 / "checkpoint_direct_k16.bin"],
        "candidate_ledger_sha256": PINS[REF / "k24_k16_r44_support_candidates.tsv"],
        "support_bins": list(range(37)),
        "positive_support_outside_bins_0_36": 0,
        "frozen_candidates": 257,
        "bounded_literal_replays": 7,
        "independent_candidate_literal_replays": 257,
        "hostile_cases": 18,
        "standard_optimized_isolated": True,
        "bounded_scalar_field_mismatches": {},
        "projected_full_seconds": new["projected_full_seconds"],
        "full_production_launched": False,
        "accepted_command": "gtimeout 600 computations/unaudited-codex-orbit0-k24-charge-production-referee-2026-08-24/run_k24_charge_k16_r44_support_v4 --mode 44 --start-record 0 --count-records 24097095 --workers 8 --output DISTINCT_ATOMIC_SUPPORT_V4_RESULT.json",
    }
    out = Path(__file__).with_name("results_independent_support_v4_audit.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
