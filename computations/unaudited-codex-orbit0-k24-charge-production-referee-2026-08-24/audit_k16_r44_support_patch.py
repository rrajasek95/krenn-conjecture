#!/usr/bin/env python3
"""Fail closed unless the R4-4 support repair preserves the bounded scalar fold."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_k16_r44_prefix262144.json"
NEW = HERE / "control_k16_r44_distributed262144_support_v4.json"
CANDIDATES = HERE / "k24_k16_r44_support_candidates.tsv"
CENSUS = HERE / "results_k24_k16_r44_support_census.json"
SOURCE = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/run_k24_charge_k16_r44.rs"
BINARY = HERE / "run_k24_charge_k16_r44_support_v4"
OUTPUT = HERE / "results_k16_r44_support_patch_audit.json"

OLD_SOURCE_SHA256 = "1ed9ef5a9b4450f55f2259a11a88a2f370259a6373af6b4b735361f928cdf1e1"
OLD_BINARY_SHA256 = "3a1b5e716ff4f781a5e523e990d8f209975b34231faf55cce8e8dd72e4f88ef9"
NEW_SOURCE_SHA256 = "64c0a6946e5233b8f7d8066ca09fe0670739bdbf60fdca6d5339eabf21f50691"
NEW_BINARY_SHA256 = "6f61d41122a2c1107b97b53cafd94b722118770357bbd6ba2f9bbb292bc333a6"
CANDIDATE_SHA256 = "57b7f0cfa15b436b6b821922c426f19d15496eb7a1cd64e7e632acaa003d5fbf"

SCALAR_FIELDS = [
    "status", "group_id", "degree", "scale_U", "ids", "covered_ids",
    "individual_id_charges", "record_interval", "records_declared",
    "distributed_prefix", "source_rows", "signed_source_coefficient",
    "l1_source_coefficient", "pivotable_K16_rows", "p1_uses",
    "first_children", "pivotable_intermediate_children", "p2_uses",
    "K24_terminal_occurrences", "full_occurrences", "irreducible_occurrences",
    "full_charge_scaled_U", "irreducible_charge_scaled_U", "m1_m2_hist",
    "terminal_cache", "packet_grouping_guard", "sign_rule", "terminality", "scope",
]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--old", type=Path, default=OLD)
    parser.add_argument("--new", type=Path, default=NEW)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    old = json.loads(args.old.read_text())
    new = json.loads(args.new.read_text())
    require(set(SCALAR_FIELDS) <= old.keys() and set(SCALAR_FIELDS) <= new.keys(), "missing scalar/control field")
    mismatches = {key: [old[key], new[key]] for key in SCALAR_FIELDS if old[key] != new[key]}
    require(not mismatches, f"sample repair changed bounded scalar fold: {mismatches}")
    require(sha256(SOURCE) == NEW_SOURCE_SHA256, "new source pin mismatch")
    require(sha256(BINARY) == NEW_BINARY_SHA256, "new binary pin mismatch")
    require(sha256(CANDIDATES) == CANDIDATE_SHA256, "candidate ledger pin mismatch")
    census = json.loads(CENSUS.read_text())
    require(census["status"] == "PASS_K24_K16_R44_READ_ONLY_SUPPORT_CENSUS", "bad census")
    require(census["candidate_count"] == 257 and census["realized_support_bins"] == list(range(37)), "bad support census")
    require(census["scalar_charge_accumulated"] is False, "census is not sample-only")
    require(new["nonzero_support_bins"] == list(range(37)), "bounded support set is not exactly bins 0..36")
    require(new["nonzero_support_records_outside_bins_0_36"] == 0, "positive support outside bins 0..36")
    require(set(map(int, new["nonzero_support_record_hist"])) == set(range(37)), "support histogram key set")
    require(all(int(value) > 0 for value in new["nonzero_support_record_hist"].values()), "support histogram has nonpositive count")
    report = {
        "status": "PASS_K24_K16_R44_SAMPLE_ONLY_PATCH_AUDIT",
        "old_source_sha256": OLD_SOURCE_SHA256,
        "old_binary_sha256": OLD_BINARY_SHA256,
        "new_source_sha256": NEW_SOURCE_SHA256,
        "new_binary_sha256": NEW_BINARY_SHA256,
        "old_control_sha256": sha256(args.old),
        "new_control_sha256": sha256(args.new),
        "candidate_ledger_sha256": CANDIDATE_SHA256,
        "scalar_fields_compared": SCALAR_FIELDS,
        "scalar_field_mismatches": mismatches,
        "bounded_records": new["source_rows"],
        "old_charge_scaled_U": old["full_charge_scaled_U"],
        "new_charge_scaled_U": new["full_charge_scaled_U"],
        "old_runtime_seconds": old["elapsed_seconds"],
        "new_runtime_seconds": new["elapsed_seconds"],
        "new_projected_full_seconds": new["projected_full_seconds"],
        "static_patch_scope": "candidate-ledger loading, witness routing, and support metadata only; Q arithmetic fields and recurrence are unchanged",
        "proof_scope": "exact bounded old/new execution equality plus source review; no failed full scalar is recovered or accepted",
        "production_launched": False,
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "scalar_fields": len(SCALAR_FIELDS)}))


if __name__ == "__main__":
    main()
