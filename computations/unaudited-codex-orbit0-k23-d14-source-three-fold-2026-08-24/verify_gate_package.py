#!/usr/bin/env python3
"""Strict verifier for the held K23 D14 source-three gate and shard plan."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
IDS = ["D14:222|R:3-2-4", "D14:222|R:3-3-3", "D14:222|R:4-2-3"]
DEGREES = [(3,2,4,60), (3,3,3,32), (4,2,3,32)]
LOCAL = {
    "run_k23_d14_source_three.rs": "32a23e26bced387be2ce348b1bb41de126f5f17e2f5ee2adeccc9320d69f116b",
    "merge_k23_d14_source_three_shards.py": "cd8cd10a5f39430c3bd78edd99fab75cc526e27093d2b60e334496552a39d96b",
    "results_prefix1.json": "f767be71b0eb279caa9044ab9ebd931f1c50c941761a3acb11a86e7facba46d4",
    "results_prefix1.json.samples.tsv": "3a72db1515078a1256681b3b49ed7425f28cbb52bf395edaf1b60593e867215a",
    "results_prefix8.json": "fbe61b7f1d86755d7bbe2686734e07b0d690987b43458b13391d420453e68204",
    "results_prefix8.json.samples.tsv": "ee6207519e7842e2f7b885f7882bc9d7edb088b82fd01e483d3b63775029d5de",
    "results_prefix64.json": "6f45de7c5c501d128ab1f7a1381f5493dfa1f9ed9906289881ab4d6c146ec83c",
    "results_prefix64.json.samples.tsv": "b5fa3e698af223114dca2489d77621eda456b761f348186df199b19724cb7de8",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for name, digest in LOCAL.items(): assert sha(HERE / name) == digest, name
    pins = json.loads((HERE / "input_pins.json").read_text())
    for value in pins.values(): assert sha(ROOT / value["path"]) == value["sha256"], value["path"]
    contract = json.loads((ROOT / pins["frozen_schedule_group_contract"]["path"]).read_text())
    by_id = {group["group_id"]: group["ids"] for group in contract["groups"]}
    assert by_id["source_D14_R3_2_4"] == [IDS[0]]
    assert by_id["source_D14_R3_3_3"] == [IDS[1]]
    assert by_id["source_D14_R4_2_3"] == [IDS[2]]

    gate_specs = [(1,1,[1,1,1]), (8,8,[11,11,11]), (64,8,[96,95,95])]
    for records, workers, sample_counts in gate_specs:
        doc = json.loads((HERE / f"results_prefix{records}.json").read_text())
        assert doc["status"] == "PASS_BOUNDED_D14_222_K23_SOURCE_THREE_EVALUATOR"
        assert doc["covered_lineage_ids"] == IDS and doc["scale_U"] == "400591699200"
        assert doc["distributed_record_mode"] and doc["R8_records_consumed"] == records
        assert doc["workers"] == workers and doc["source_heads"] == records * 1728
        assert doc["all_realized_cached_K23_responses_terminal"]
        assert doc["literal_sample_guard"]["records_per_sink"] == sample_counts
        assert doc["literal_sample_guard"]["records"] == sum(sample_counts)
        assert doc["terminal_cache_resource_guard"]["peak_keys_per_worker"] <= 3_000_000
        for lineage, (d1,d2,d3,tails) in zip(IDS, DEGREES, strict=True):
            sink = doc["sinks"][lineage]
            assert (sink["first_response_degree"],sink["second_response_degree"],sink["terminal_response_degree"]) == (d1,d2,d3)
            assert sink["K23_terminal_occurrences"] == tails * sink["selected_p3_uses"]
            assert sink["full_occurrences"] == sink["irreducible_occurrences"] == sink["K23_terminal_occurrences"]
            assert sink["full_charge_scaled_U"] == sink["irreducible_charge_scaled_U"]
        lines = (HERE / f"results_prefix{records}.json.samples.tsv").read_text().splitlines()
        assert len(lines) == 1 + sum(sample_counts)
        observed = {lineage: 0 for lineage in IDS}
        for line in lines[1:]:
            c = line.split("\t"); assert len(c) == 28 and c[0] in observed
            observed[c[0]] += 1
            head, r8 = int(c[2]), int(c[3])
            assert int(c[1]) == head * 257 // (485 * 1728) and r8 == head // 1728
            assert int(c[23]) == dict(zip(IDS,(4,3,3),strict=True))[c[0]]
        assert [observed[lineage] for lineage in IDS] == sample_counts

    plan = json.loads((HERE / "shard_plan.json").read_text())
    assert plan["status"] == "PASS_BOUNDED_K23_D14_SOURCE_THREE_SHARD_PLAN"
    assert plan["covered_lineage_ids"] == IDS and plan["production_shards"] == [[0,243],[243,485]]
    assert plan["production_authorization"] == "HELD_PENDING_EXPLICIT_RESOURCE_CLEARANCE"
    assert plan["merge_contract"]["exact_no_gap_intervals"] == [[0,243],[243,485]]
    assert plan["merge_contract"]["required_global_witness_bins_per_sink"] == 257
    assert plan["merge_contract"]["required_total_witnesses"] == 771
    compile((HERE / "merge_k23_d14_source_three_shards.py").read_text(), "merge", "exec")
    audit = {
        "status": "PASS_STRICT_K23_D14_SOURCE_THREE_GATE_PACKAGE",
        "covered_lineage_ids": IDS,
        "source_sha256": LOCAL["run_k23_d14_source_three.rs"],
        "gates": [1,8,64],
        "largest_gate_projected_full_seconds": 432.139892,
        "largest_gate_observed_rss_kib": 3889088,
        "peak_terminal_cache_keys_per_worker": 2933454,
        "production_shards": [[0,243],[243,485]],
        "required_literal_witnesses": 771,
        "production_held": True,
    }
    output = HERE / "gate_audit.json"; tmp = Path(f"{output}.tmp")
    tmp.write_text(json.dumps(audit, indent=2) + "\n"); os.replace(tmp, output)
    print(json.dumps(audit, indent=2))


if __name__ == "__main__": main()
