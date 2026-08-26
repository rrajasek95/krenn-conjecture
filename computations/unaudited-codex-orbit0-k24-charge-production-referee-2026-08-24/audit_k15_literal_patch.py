#!/usr/bin/env python3
"""Prove bounded scalar equality for the source-backed K15 sample patch."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_direct_k15_prefix8.json"
NEW = HERE / "control_k15_literals_v2_prefix8.json"
OUTPUT = HERE / "results_k15_literal_patch_audit.json"
SOURCE = ROOT / "computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/run_k24_charge_direct_k15.rs"
BINARY = HERE / "run_k24_charge_direct_k15_literals_v2"
SOURCE_SHA = "594701a258a9b9be9b6ec4516ba683eb758b3c4c026ce66b982899d17b2596c9"
BINARY_SHA = "230918d02643e1cdc87c6de3e2f0d4a89ac37099a8449d42d8a3e6b063639b57"
OLD_SOURCE_SHA = "600159d7a51bbd655d0392d52d45e09c4434bf4417cc3438e34123422e1a53ec"
OLD_BINARY_SHA = "802ed7b56bcda0ee0071cc24817d5bacda42ff6f901fcd9f27e9dfbf7b44cd48"

TOP_FIELDS = ["status", "scale_U", "slice_interval", "source_slices", "source_heads_per_slice", "workers", "degree", "covered_ids", "scalar_groups", "packet_grouping_guard", "sign_rule", "terminality", "scope"]
SINK_FIELDS = ["ids", "individual_id_charges", "degrees", "source_heads", "source_mass", "source_l1", "stage_pivot_uses", "stage_tail_candidates", "stage_pivotable_children", "terminal_response_keys_evaluated", "terminal_K24_occurrences", "full_occurrences", "irreducible_occurrences", "full_charge_scaled_U", "irreducible_charge_scaled_U", "denominator_product_hist"]


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    old = json.loads(OLD.read_text()); new = json.loads(NEW.read_text())
    top_mismatch = {key: [old.get(key), new.get(key)] for key in TOP_FIELDS if old.get(key) != new.get(key)}
    require(not top_mismatch, f"K15 top-level scalar mismatch: {top_mismatch}")
    require(set(old["sinks"]) == set(new["sinks"]), "K15 sink set changed")
    sink_mismatch = {}
    for sink in old["sinks"]:
        changed = {key: [old["sinks"][sink].get(key), new["sinks"][sink].get(key)] for key in SINK_FIELDS if old["sinks"][sink].get(key) != new["sinks"][sink].get(key)}
        if changed:
            sink_mismatch[sink] = changed
    require(not sink_mismatch, f"K15 sink scalar mismatch: {sink_mismatch}")
    require(sha256(SOURCE) == SOURCE_SHA and sha256(BINARY) == BINARY_SHA, "K15 v2 source/binary pin")
    report = {
        "status": "PASS_K24_K15_SOURCE_BACKED_SAMPLE_ONLY_PATCH_AUDIT",
        "old_source_sha256": OLD_SOURCE_SHA, "old_binary_sha256": OLD_BINARY_SHA,
        "new_source_sha256": SOURCE_SHA, "new_binary_sha256": BINARY_SHA,
        "old_control_sha256": sha256(OLD), "new_control_sha256": sha256(NEW),
        "top_scalar_fields_compared": TOP_FIELDS, "per_sink_scalar_fields_compared": SINK_FIELDS,
        "top_mismatches": top_mismatch, "sink_mismatches": sink_mismatch,
        "bounded_slices": 8, "new_elapsed_seconds": new["elapsed_seconds"],
        "new_projected_full_seconds": new["projected_full_seconds"],
        "new_sample_schema": new["sample_schema"],
        "sample_patch_scope": "source head ordinal/row, first nonzero literal route per slice and sink, ledger serialization, metadata only",
        "production_launched": False,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"], "sink_fields": len(SINK_FIELDS)}))


if __name__ == "__main__":
    main()
