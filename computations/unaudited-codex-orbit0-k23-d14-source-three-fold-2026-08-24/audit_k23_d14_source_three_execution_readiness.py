#!/usr/bin/env python3
"""Fail-closed readiness audit for the held two-shard D14 source-three K23 production."""

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
IDS = ["D14:222|R:3-2-4", "D14:222|R:3-3-3", "D14:222|R:4-2-3"]
PINS = {
    "run_k23_d14_source_three.rs": "32a23e26bced387be2ce348b1bb41de126f5f17e2f5ee2adeccc9320d69f116b",
    "run_k23_d14_source_three": "5ecb715d1861280495d92a9d970b4c50db6cc32ba78577ecbc97a5837b66373f",
    "merge_k23_d14_source_three_shards.py": "cd8cd10a5f39430c3bd78edd99fab75cc526e27093d2b60e334496552a39d96b",
    "results_prefix1.json": "f767be71b0eb279caa9044ab9ebd931f1c50c941761a3acb11a86e7facba46d4",
    "results_prefix1.json.samples.tsv": "3a72db1515078a1256681b3b49ed7425f28cbb52bf395edaf1b60593e867215a",
    "results_prefix8.json": "fbe61b7f1d86755d7bbe2686734e07b0d690987b43458b13391d420453e68204",
    "results_prefix64.json": "6f45de7c5c501d128ab1f7a1381f5493dfa1f9ed9906289881ab4d6c146ec83c",
    "input_pins.json": "27626ec2ab686a004a00cb937d46b82c793904d70c140cb45f2e4949e210984a",
    "shard_plan.json": "deba625bd30b23c7d63b6e6dde8e5c26900a1b10c6741bdaeadcc5abcbd17295",
    "gate_audit.json": "04c86141ca29a096dcf206a957aa533e0cdd6d2603830145d79bafdfa5cda92a",
    "results_binary_revalidation1.json.samples.tsv": "3a72db1515078a1256681b3b49ed7425f28cbb52bf395edaf1b60593e867215a",
    "referee_k23_d14_source_three_literals.rs": "64bc0cd19c859f57a9fb01c6a8a66a54a4d798de6dc524e1459b5015395bd6d4",
    "referee_k23_d14_source_three_literals": "8ea90ad3caa491833ad214a2df2d5a17367addc6b78353be25b200e84eb199b6",
    "results_literal_referee_prefix64_test.json": "2a699f3502dd2d462ffdb01218b1bbf6912a8ced0898a61530262618f5b36b79",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def semantic_gate(doc: dict) -> dict:
    value = json.loads(json.dumps(doc))
    value.pop("elapsed_seconds", None)
    value.pop("projected_full_seconds_from_consumed_records", None)
    value["literal_sample_guard"].pop("ledger", None)
    return value


def main() -> None:
    for name, digest in PINS.items():
        assert sha(HERE / name) == digest, name
    pins = load(HERE / "input_pins.json")
    for entry in pins.values():
        assert sha(ROOT / entry["path"]) == entry["sha256"], entry["path"]

    original = load(HERE / "results_prefix1.json")
    revalidation = load(HERE / "results_binary_revalidation1.json")
    assert semantic_gate(revalidation) == semantic_gate(original)
    assert sha(HERE / "results_binary_revalidation1.json.samples.tsv") == sha(HERE / "results_prefix1.json.samples.tsv")

    schema = load(HERE / "k23_d14_source_three_output_schema.json")
    assert set(schema["top_level_required"]) <= set(original)
    assert original["covered_lineage_ids"] == IDS and list(original["sinks"]) == IDS
    for lineage, multiplier in schema["terminal_tail_multipliers"].items():
        sink = original["sinks"][lineage]
        assert set(schema["sink_required"]) <= set(sink)
        assert sink["K23_terminal_occurrences"] == multiplier * sink["selected_p3_uses"]
        assert sink["full_occurrences"] == sink["irreducible_occurrences"] == sink["K23_terminal_occurrences"]
        assert sink["full_charge_scaled_U"] == sink["irreducible_charge_scaled_U"]
    assert (HERE / "results_prefix1.json.samples.tsv").read_text().splitlines()[0] == schema["sample_header"]

    plan = load(HERE / "production_execution_plan.json")
    assert plan["status"] == "PASS_HELD_K23_D14_SOURCE_THREE_PRODUCTION_EXECUTION_PLAN"
    assert plan["strict_ids"] == IDS
    assert plan["producer"]["source_sha256"] == sha(HERE / "run_k23_d14_source_three.rs")
    assert plan["producer"]["binary_sha256"] == sha(HERE / "run_k23_d14_source_three")
    assert [entry["interval"] for entry in plan["shards"]] == [[0, 243], [243, 485]]
    assert plan["merge"]["exact_no_gap_intervals"] == [[0, 243], [243, 485]]
    assert plan["merge"]["required_merged_samples"] == 771
    assert plan["literal_referee"]["required_samples_per_sink"] == 257
    assert plan["literal_referee"]["source_sha256"] == sha(HERE / "referee_k23_d14_source_three_literals.rs")
    assert plan["literal_referee"]["binary_sha256"] == sha(HERE / "referee_k23_d14_source_three_literals")
    assert plan["resource_and_scope_guard"]["production_requires_explicit_clearance"] is True

    shard_plan = load(HERE / "shard_plan.json")
    assert shard_plan["production_shards"] == [[0, 243], [243, 485]]
    assert shard_plan["merge_contract"]["exact_no_gap_intervals"] == [[0, 243], [243, 485]]
    assert shard_plan["merge_contract"]["required_total_witnesses"] == 771
    merger = (HERE / "merge_k23_d14_source_three_shards.py").read_text()
    for guard in (
        "INTERVALS = [(0, 243), (243, 485)]", "assert structural == expected",
        "assert set(samples) ==", "assert peak <= 3_000_000",
        "PASS_COMPLETE_D14_222_K23_SOURCE_THREE_CHARGE",
    ):
        assert guard in merger
    compile(merger, "merge", "exec")
    compile((HERE / "finalize_k23_d14_source_three_fragment.py").read_text(), "finalizer", "exec")

    referee_test = load(HERE / "results_literal_referee_prefix64_test.json")
    assert referee_test["status"] == "PASS_INDEPENDENT_K23_D14_SOURCE_THREE_LITERAL_REFEREE"
    assert referee_test["samples_per_sink"] == [96, 95, 95]
    assert referee_test["literal_terminal_children_checked"] == 22_686_976
    assert referee_test["witness_terminal_children_checked"] == 11_840
    for field in (
        "source_heads_reconstructed_from_frozen_R8", "all_literal_path_counts_and_charges_equal",
        "all_U_divisions_exact", "all_terminal_K23_children_nonpivotable",
        "all_abstract_literal_cycle_keys_equal",
    ):
        assert referee_test[field] is True

    payload = {
        "status": "PASS_K23_D14_SOURCE_THREE_PRODUCTION_READINESS_REFEREE",
        "degree": 23,
        "strict_ids": IDS,
        "producer": {
            "source_sha256": sha(HERE / "run_k23_d14_source_three.rs"),
            "binary_sha256": sha(HERE / "run_k23_d14_source_three"),
            "sealed_gate_manifest_replay": True,
            "fresh_prefix1_semantic_revalidation": True,
            "all_input_hashes_replayed": True,
        },
        "execution": {
            "exact_intervals": [[0, 243], [243, 485]],
            "gap_free_no_overlap": True,
            "workers_per_shard": 8,
            "atomic_output": True,
            "external_alarm_seconds": 570,
            "hard_internal_wall_seconds": 600,
            "hard_RSS_bytes": 17_179_869_184,
        },
        "output_guard": {
            "schema_sha256": sha(HERE / "k23_d14_source_three_output_schema.json"),
            "schema_replayed_against_sealed_gate": True,
            "terminal_multipliers": [60, 32, 32],
            "full_equals_irreducible_required": True,
        },
        "merge": {
            "source_sha256": sha(HERE / "merge_k23_d14_source_three_shards.py"),
            "exact_structural_counts_pinned": True,
            "exact_no_gap_intervals": True,
            "complete_257_bins_per_sink_required": True,
        },
        "literal_referee": {
            "source_sha256": sha(HERE / "referee_k23_d14_source_three_literals.rs"),
            "binary_sha256": sha(HERE / "referee_k23_d14_source_three_literals"),
            "prefix64_test_sha256": sha(HERE / "results_literal_referee_prefix64_test.json"),
            "prefix64_full_literal_path_replays": 286,
            "production_required_replays": 771,
            "production_complete_257_bins_per_sink_required": True,
        },
        "fragment": {
            "finalizer_sha256": sha(HERE / "finalize_k23_d14_source_three_fragment.py"),
            "strict_singleton_group_ids": ["source_D14_R3_2_4", "source_D14_R3_3_3", "source_D14_R4_2_3"],
            "group_scalar_once": True,
        },
        "production_launched_by_this_readiness_package": False,
        "scope": "execution/referee preparation only; no heavy launch, K24, rows, membership, or conjecture claim",
    }
    logical = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    payload["logical_sha256"] = logical
    output = HERE / "results_production_readiness_audit.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps({"status": payload["status"], "logical_sha256": logical}, indent=2))


if __name__ == "__main__":
    main()
