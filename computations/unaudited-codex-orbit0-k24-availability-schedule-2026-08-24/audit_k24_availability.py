#!/usr/bin/env python3
"""Audit the exact 35-ID K24 availability and bounded source-fold schedule.

This is metadata/schema work only.  No K24 response, charge, residual, or
terminal-span computation is performed.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from assemble_k24_35_exact import EXPECTED_GROUPS, U


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DAG_PATH = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
DAG_SHA256 = "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa"
DAG_LOGICAL_SHA256 = "ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66"


ARTIFACTS = {
    "orbit0_structure": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin",
        "bytes": 115_275,
        "sha256": "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
        "magic": "K16DIRECT1\0",
        "role": "485 frozen R8prime records plus exact direct-factor source formula",
    },
    "response_aux": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin",
        "bytes": 14_364,
        "sha256": "f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab",
        "magic": "K17AUX1\0",
        "role": "78 frozen pivots and K2/K3 response tails",
    },
    "response_k4": {
        "path": "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin",
        "bytes": 18_727,
        "sha256": "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
        "magic": "K18K4A1",
        "role": "60 literal K4 tails for each of 78 pivots",
    },
    "cycle_aux": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin",
        "bytes": 2_637,
        "sha256": "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
        "magic": "K17CYC1\0",
        "role": "frozen literal 77-cycle charge table; charge mode only",
    },
    "direct_k15_rows": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k15.bin",
        "bytes": 169_958_768,
        "records": 5_311_211,
        "record_bytes": 32,
        "header_bytes": 16,
        "sha256": "e79b752f94ad3b16ce4cf7d3f044e8887bda54bba5c6298ab31338bb121fa20f",
        "magic": "K15CHK1\0",
        "role": "available exact direct-K15 row checkpoint; alternative only, not selected by this K24 schedule",
        "selected_for_K24": False,
    },
    "direct_k16_rows": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin",
        "bytes": 771_107_056,
        "records": 24_097_095,
        "record_bytes": 32,
        "header_bytes": 16,
        "sha256": "93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3",
        "magic": "K16DIR1\0",
        "role": "exact signed-collected grouped direct-K16 canonical rows",
    },
    "hidden_decorated_k16_pair_orbits": {
        "path": "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin",
        "bytes": 5_381_923_399,
        "records": 101_545_723,
        "record_bytes": 53,
        "header_bytes": 80,
        "sha256": "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8",
        "magic": "H16ORM1\0",
        "role": "decorated (K16 row, selected pivot) H-orbits repairing hidden D14 R2 descendants",
    },
    "hidden_k18_22_pivotable_rows": {
        "path": "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin",
        "bytes": 12_675_197_280,
        "records": 158_439_965,
        "record_bytes": 80,
        "header_bytes": 80,
        "sha256": "442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8",
        "magic": "H18PIV2\0",
        "role": "literal collected pivotable D14 R2-2 K18 rows repairing the deep hidden descendant",
    },
}


ENGINE_REFS = [
    {"path": "computations/unaudited-codex-orbit0-k22-hidden-collected-k18-2026-08-24/run_k22_hidden_collected_k18.rs", "sha256": "d54f6f2c861b3b7bd40a47ec1282cf392903bf1348826fbbd2207156ba9012fb", "reuse": "H18PIV2 reader/source-linear continuation; add K4 row-orbit sink"},
    {"path": "computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/run_k22_hidden_pair_fold.rs", "sha256": "a472f2f79c1144d4f58a347c73ef6710089c631b77b31c6d6da024f25df09945", "reuse": "decorated hidden pair reader; retain only R2-4-4 K24 sink"},
    {"path": "computations/unaudited-codex-orbit0-k22-d14-source-three-fold-2026-08-24/run_k22_d14_source_three.rs", "sha256": "52881a540068ea6b21b0b3d4d7ad6f2b63c576d17f93ceb5889a2b882dc5c547", "reuse": "K14 485-slice source-linear fold"},
    {"path": "computations/unaudited-codex-orbit0-k22-direct-k15-four-sink-2026-08-24/run_k22_direct_k15_four_sink.rs", "sha256": "9a5599da22dbac007e80da8b3d38062257aad6084e9dbe8bfa14c0b62c0b6f3b", "reuse": "grouped K15 485-slice source-linear fold"},
    {"path": "computations/unaudited-codex-orbit0-k22-direct23-source-fold-2026-08-24/run_k22_direct23_source_fold.rs", "sha256": "ccfd1af09fced6d05f0aeb40cf3ee482f8d8a26565f2448cbc30fb5c0952241b", "reuse": "combined D17/D18 source sectors"},
]


SPAN_REFS = [
    {"path": "computations/unaudited-codex-orbit0-k24-factorized-gram-2026-08-23/k24_factorized_gram_provider.py", "sha256": "29075c59bdc72237c9e88cd8df360dfcb5184968c4824556032b437f8fb8112d", "role": "multiplier-aware literal-column/H-row-orbit span provider"},
    {"path": "computations/unaudited-codex-orbit0-k24-factorized-gram-2026-08-23/results_k24_factorized_gram.json", "sha256": "dc7adf3399d0e704e5f358422523f2f8aecb8fdba52b8db0d8f8c8625c8186a1", "role": "exact Gram interface and 1,757-decoration correction"},
    {"path": "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/filtered_k24_reducer.py", "sha256": "6c265a1e655d9d5c5d6759a02823bb59f8590e7ce287108f2fdb7eab050f18fd", "role": "restartable exact H-orbit-mass run/merge reference"},
    {"path": "computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/results_filtered_k24_reducer_design.json", "sha256": "dc3a164b8e7eee33cc9046d0b0fd4d97de7d63b80633e984b88ed37558503c37", "role": "later-pivot policy and row-run interface pin"},
]


GROUP_METADATA = {
    "source_D14_R2_2_2_4": ("hidden_collected_k18", ["hidden_k18_22_pivotable_rows"]),
    "source_D14_R2_4_4": ("hidden_decorated_k16_pair", ["hidden_decorated_k16_pair_orbits"]),
    "source_D14_R3_3_4": ("k14_source_formula", ["orbit0_structure"]),
    "source_D14_R4_2_4": ("k14_source_formula", ["orbit0_structure"]),
    "source_D15_R2_3_4": ("grouped_direct_k15_source", ["orbit0_structure"]),
    "source_D15_R3_2_4": ("grouped_direct_k15_source", ["orbit0_structure"]),
    "source_D16_R2_2_4": ("grouped_direct_k16_rows", ["direct_k16_rows"]),
    "source_D16_R4_4": ("grouped_direct_k16_rows", ["direct_k16_rows"]),
    "source_D17_R3_4": ("direct_D17_D18_formula", ["orbit0_structure"]),
    "source_D18_R2_4": ("direct_D17_D18_formula", ["orbit0_structure"]),
}


def intervals(total: int, parts: int) -> list[list[int]]:
    boundaries = [total * index // parts for index in range(parts + 1)]
    return [[boundaries[index], boundaries[index + 1]] for index in range(parts)]


EXECUTION_FAMILIES = [
    {
        "family_id": "hidden_collected_k18", "group_ids": ["source_D14_R2_2_2_4"],
        "input_artifact": "hidden_k18_22_pivotable_rows", "source_units": 158_439_965,
        "prefix_units": [1, 4096, 1_000_000], "planned_intervals": intervals(158_439_965, 6),
        "conservative_projected_max_shard_seconds": 390,
    },
    {
        "family_id": "hidden_decorated_k16_pair", "group_ids": ["source_D14_R2_4_4"],
        "input_artifact": "hidden_decorated_k16_pair_orbits", "source_units": 101_545_723,
        "prefix_units": [1, 4096, 1_000_000], "planned_intervals": intervals(101_545_723, 6),
        "conservative_projected_max_shard_seconds": 465,
    },
    {
        "family_id": "k14_source_formula", "group_ids": ["source_D14_R3_3_4", "source_D14_R4_2_4"],
        "input_artifact": "orbit0_structure", "source_units": 485,
        "prefix_units": [1, 8, 64], "planned_intervals": intervals(485, 8),
        "conservative_projected_max_shard_seconds": 300,
    },
    {
        "family_id": "grouped_direct_k15_source", "group_ids": ["source_D15_R2_3_4", "source_D15_R3_2_4"],
        "input_artifact": "orbit0_structure", "source_units": 485,
        "prefix_units": [1, 8, 31], "planned_intervals": intervals(485, 16),
        "conservative_projected_max_shard_seconds": 430,
    },
    {
        "family_id": "grouped_direct_k16_rows", "group_ids": ["source_D16_R2_2_4", "source_D16_R4_4"],
        "input_artifact": "direct_k16_rows", "source_units": 24_097_095,
        "prefix_units": [1, 4096, 262_144], "planned_intervals": intervals(24_097_095, 6),
        "conservative_projected_max_shard_seconds": 380,
    },
    {
        "family_id": "direct_D17_D18_formula", "group_ids": ["source_D17_R3_4", "source_D18_R2_4"],
        "input_artifact": "orbit0_structure", "source_units": 485,
        "prefix_units": [1, 8, 61], "planned_intervals": intervals(485, 8),
        "conservative_projected_max_shard_seconds": 385,
    },
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_artifact(name: str, item: dict) -> dict:
    path = ROOT / item["path"]
    if not path.is_file() or path.stat().st_size != item["bytes"]:
        raise RuntimeError(f"missing/size mismatch: {name}")
    with path.open("rb") as stream:
        header = stream.read(max(16, len(item["magic"])))
    if not header.startswith(item["magic"].encode("latin1")):
        raise RuntimeError(f"magic mismatch: {name}")
    if "records" in item and item["header_bytes"] + item["records"] * item["record_bytes"] != item["bytes"]:
        raise RuntimeError(f"geometry mismatch: {name}")
    hash_mode = "rehash" if item["bytes"] <= 1_000_000 else "upstream_sealed_full_hash_pin"
    if hash_mode == "rehash" and digest(path) != item["sha256"]:
        raise RuntimeError(f"hash mismatch: {name}")
    return {**item, "present": True, "geometry_and_magic_checked": True, "hash_check_mode": hash_mode}


def main() -> None:
    if digest(DAG_PATH) != DAG_SHA256:
        raise RuntimeError("DAG file hash mismatch")
    dag = json.loads(DAG_PATH.read_text())
    if dag["logical_sha256"] != DAG_LOGICAL_SHA256:
        raise RuntimeError("DAG logical hash mismatch")
    required = dag["required_reachable_lineage_ids_by_degree"]["24"]
    flat = [item for group in EXPECTED_GROUPS.values() for item in group]
    if len(required) != 35 or len(set(required)) != 35 or Counter(flat) != Counter(required):
        raise RuntimeError("strict K24 partition mismatch")

    artifacts = {name: check_artifact(name, item) for name, item in ARTIFACTS.items()}
    for reference in ENGINE_REFS + SPAN_REFS:
        path = ROOT / reference["path"]
        if digest(path) != reference["sha256"]:
            raise RuntimeError(f"reference hash mismatch: {reference['path']}")

    nodes = {node["id"]: node for node in dag["nodes"]}
    edges_by_child = {}
    for edge in dag["edges"]:
        edges_by_child.setdefault(edge["child"], []).append(edge)
    group_for = {item: group for group, items in EXPECTED_GROUPS.items() for item in items}
    lineages = []
    for lineage_id in required:
        node = nodes[lineage_id]
        edges = edges_by_child[lineage_id]
        if len(edges) != 1:
            raise RuntimeError(f"non-unique parent edge: {lineage_id}")
        edge = edges[0]
        parent = nodes[edge["parent"]]
        if edge["shift"] != 4 or edge["tail_terms_per_pivot"] != 60:
            raise RuntimeError(f"K24 non-K4 terminal edge: {lineage_id}")
        if edge["pivot_policy"] != "all_literal_dividing_pivots" or edge["coefficient_rule"] != "child coefficient = -parent coefficient / pivot_count":
            raise RuntimeError(f"recurrence policy mismatch: {lineage_id}")
        if parent["degree"] != 20 or node["sign_relative_to_unsigned_R8prime"] != -parent["sign_relative_to_unsigned_R8prime"]:
            raise RuntimeError(f"parent/sign mismatch: {lineage_id}")
        denominator = node["denominator_product_class"]
        if not denominator["global_scale_divides"] or U % denominator["product_lcm"]:
            raise RuntimeError(f"U divisor failure: {lineage_id}")
        group = group_for[lineage_id]
        family, artifact_names = GROUP_METADATA[group]
        state = node["current_provenance"]["state"]
        repaired = state == "MISSING_DISCARDED_K14_K2_PIVOTABLE_PARENT"
        lineages.append({
            "id": lineage_id,
            "group_id": group,
            "source_family": family,
            "artifacts": artifact_names,
            "availability": "SOURCE_REPLAY_REQUIRED",
            "retained_immediate_K20_profile": False,
            "immediate_parent_id": edge["parent"],
            "immediate_parent_degree": 20,
            "final_shift": 4,
            "tail_terms_per_selected_pivot": 60,
            "sign_relative_to_unsigned_R8prime": node["sign_relative_to_unsigned_R8prime"],
            "denominator_product_lcm": denominator["product_lcm"],
            "global_scale_U_divides": True,
            "frozen_dag_provenance_state": state,
            "post_DAG_source_repair": "hidden retained source now present and pinned" if repaired else None,
            "parent_anchor_mass": 4,
            "child_anchor_mass": 0,
            "terminal": True,
        })

    groups = []
    for group_id, group_ids in EXPECTED_GROUPS.items():
        family, artifact_names = GROUP_METADATA[group_id]
        groups.append({
            "group_id": group_id,
            "ids": group_ids,
            "count": len(group_ids),
            "source_family": family,
            "artifacts": artifact_names,
            "availability": "SOURCE_REPLAY_REQUIRED",
            "retained_immediate_K20_profile_interface": False,
            "terminal_parent_degree": 20,
            "final_shift": 4,
            "terminal_tail_terms_per_selected_pivot": 60,
            "child_anchor_mass": 0,
            "separate_named_sink_required": True,
        })

    for family in EXECUTION_FAMILIES:
        planned = family["planned_intervals"]
        if planned[0][0] != 0 or planned[-1][1] != family["source_units"] or any(left[1] != right[0] for left, right in zip(planned, planned[1:])):
            raise RuntimeError(f"interval gap/overlap: {family['family_id']}")
        if family["conservative_projected_max_shard_seconds"] > 540:
            raise RuntimeError(f"projection gate failure: {family['family_id']}")
        family.update({
            "planned_shards": len(planned),
            "response_mode": "60 literal K4 tails per selected K20 pivot",
            "launch_gate": "prefix-measured projection <=540s and RSS <=8GiB; otherwise bisect",
            "watchdog_seconds": 570,
            "hard_wall_seconds": 600,
            "family_RSS_limit_GiB": 8,
            "aggregate_RSS_limit_GiB": 16,
            "atomic_output": True,
            "merge_requires_gap_free_no_overlap": True,
        })

    schema_path = HERE / "literal_k24_residual_interface.schema.json"
    schema = json.loads(schema_path.read_text())
    if schema.get("$id") != "literal-k24-h-row-orbit-residual-v1":
        raise RuntimeError("literal residual schema identity mismatch")
    residual_contract = {
        "schema": str(schema_path.relative_to(ROOT)),
        "schema_sha256": digest(schema_path),
        "canonical_policy": "H-canonical sorted 24-cell row; all literal dividing mixed-K0 pivots averaged occurrencewise",
        "target_coordinate": "total exact rational mass on each H-row orbit",
        "required_row_record": ["canonical_row_hex", "orbit_size", "orbit_mass_numerator", "orbit_mass_denominator"],
        "required_shard_provenance": ["family_id", "source_interval", "group_id", "input_sha256", "engine_sha256", "recurrence_policy", "canonicalization_policy", "scale_U", "run_count", "row_count", "exact_zero_cancellations", "content_sha256"],
        "required_literal_sample_provenance": ["source_cursor", "lineage_id", "ordered_pivot_indices", "ordered_tail_ordinals", "literal_K24_row_hex", "H_canonical_row_hex", "H_action_or_witness", "exact_signed_fraction"],
        "merge_rule": "retain group/shard runs until exact external merge; sum exact orbit masses by canonical row and delete only proven exact zeros",
        "span_seed_rule": "seed multiplier-aware Gram provider with every literal column incident to every nonzero residual row orbit",
        "not_sufficient": ["charge scalar", "support-only rows", "anchor signature", "1,757 decorated-matching orbit index", "K22 scalar", "K23 scalar"],
        "complete_component_required": True,
    }

    result = {
        "status": "PASS_EXACT_K24_35_ID_AVAILABILITY_SCHEDULE_NO_CHARGE",
        "scope": "availability, recurrence, physical scheduling, and residual interface only",
        "charge_run": False,
        "residual_run": False,
        "terminal_span_run": False,
        "degree": 24,
        "scale_U": U,
        "dag": {"path": str(DAG_PATH.relative_to(ROOT)), "sha256": DAG_SHA256, "logical_sha256": DAG_LOGICAL_SHA256},
        "required_ids": 35,
        "covered_by_prolongable_sources": 35,
        "retained_immediate_K20_terminal_profile_ids": 0,
        "source_replay_ids": 35,
        "genuine_provenance_gaps": 0,
        "scalar_groups": 10,
        "physical_source_folds": 6,
        "planned_initial_shards": sum(len(item["planned_intervals"]) for item in EXECUTION_FAMILIES),
        "exact_group_partition": groups,
        "lineages": lineages,
        "artifacts": artifacts,
        "reusable_engine_references": ENGINE_REFS,
        "terminal_span_references": SPAN_REFS,
        "physical_schedule": EXECUTION_FAMILIES,
        "terminality_proof": {
            "parent_degree": 20,
            "parent_anchor_mass": 4,
            "removed_pivot_anchor_mass": 4,
            "K4_tail_anchor_mass": 0,
            "child_anchor_mass": 0,
            "formula": "4 - 4 + 0 = 0",
            "pivot_requires_anchor_mass": 4,
            "conclusion": "all 35 K24 outputs are terminal; full charge equals irreducible charge",
        },
        "nonprolongable_guard": {
            "K22_or_K23_charge_scalars_used": False,
            "reason": "terminal scalar outputs retain neither literal K20 parent rows nor outgoing selected-pivot occurrence data",
            "actual_inputs_are_literal_or_factor_sources": True,
        },
        "residual_contract": residual_contract,
        "runtime_policy": {
            "charge_mode": "integer/source-linear scalar fold; no parent-row output",
            "residual_mode": "same gap-free source shards but exact canonical H-row-orbit runs; re-gate wall, RSS, unique rows, bytes/row, and disk independently",
            "residual_disk_guard": "do not launch a projected >=1 TiB materialization without explicit capacity approval; bisect/flush compressed sorted runs and preserve exact-zero merge semantics",
            "sequential_shards": True,
            "sample_requirement": "257 distributed nonzero literal continuations per physical family/mode",
        },
    }
    logical = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    output = HERE / "results_k24_availability_schedule.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps({
        "status": result["status"],
        "required_ids": 35,
        "source_replay_ids": 35,
        "gaps": 0,
        "physical_folds": 6,
        "planned_initial_shards": result["planned_initial_shards"],
        "logical_sha256": logical,
    }, indent=2))


if __name__ == "__main__":
    main()
