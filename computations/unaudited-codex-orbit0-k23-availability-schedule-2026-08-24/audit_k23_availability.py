#!/usr/bin/env python3
"""Exact availability and bounded physical schedule audit for all 59 K23 IDs.

This is metadata/schema work only.  Large inputs are checked by size/header
against upstream SHA-256 pins; no K23 response or charge is evaluated.
"""

from __future__ import annotations

import hashlib
import json
import os
import struct
from collections import Counter
from pathlib import Path

from assemble_k23_59_exact import EXPECTED_GROUPS, U


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
        "role": "78 frozen pivots and 12 K2 / 32 K3 tails per pivot",
    },
    "response_k4": {
        "path": "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin",
        "bytes": 18_727,
        "sha256": "4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3",
        "magic": "K18K4A1",
        "role": "60 frozen K4 tails per pivot",
    },
    "cycle_aux": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin",
        "bytes": 2_637,
        "sha256": "8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7",
        "magic": "K17CYC1\0",
        "role": "frozen literal 77-cycle charge table",
    },
    "direct_k15_rows": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k15.bin",
        "bytes": 169_958_768,
        "records": 5_311_211,
        "record_bytes": 32,
        "header_bytes": 16,
        "sha256": "e79b752f94ad3b16ce4cf7d3f044e8887bda54bba5c6298ab31338bb121fa20f",
        "magic": "K15CHK1\0",
        "role": "alternative exact signed-collected direct-K15 row source; selected schedule uses source-linear R8 replay",
    },
    "direct_k16_rows": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin",
        "bytes": 771_107_056,
        "records": 24_097_095,
        "record_bytes": 32,
        "header_bytes": 16,
        "sha256": "93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3",
        "magic": "K16DIR1\0",
        "role": "literal grouped direct-K16 canonical rows",
    },
    "hidden_decorated_k16_pair_orbits": {
        "path": "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin",
        "bytes": 5_381_923_399,
        "records": 101_545_723,
        "record_bytes": 53,
        "header_bytes": 80,
        "sha256": "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8",
        "magic": "H16ORM1\0",
        "role": "exact decorated (K16 row, selected pivot) H-orbits repairing hidden D14 R2 descendants",
    },
    "hidden_k18_22_pivotable_rows": {
        "path": "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin",
        "bytes": 12_675_197_280,
        "records": 158_439_965,
        "record_bytes": 80,
        "header_bytes": 80,
        "sha256": "442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8",
        "magic": "H18PIV2\0",
        "role": "literal collected pivotable D14 R2-2 K18 parent rows repairing the deep hidden descendant",
    },
}


REUSABLE_ENGINES = [
    {"path": "computations/unaudited-codex-orbit0-k22-hidden-collected-k18-2026-08-24/run_k22_hidden_collected_k18.rs", "sha256": "d54f6f2c861b3b7bd40a47ec1282cf392903bf1348826fbbd2207156ba9012fb", "reuse": "H18PIV2 source-linear deep continuation; replace only final K2 sink by K3"},
    {"path": "computations/unaudited-codex-orbit0-k22-hidden-pair-fold-2026-08-24/run_k22_hidden_pair_fold.rs", "sha256": "a472f2f79c1144d4f58a347c73ef6710089c631b77b31c6d6da024f25df09945", "reuse": "decorated hidden pair reader and two strictly separate source-linear sinks"},
    {"path": "computations/unaudited-codex-orbit0-k22-d14-source-three-fold-2026-08-24/run_k22_d14_source_three.rs", "sha256": "52881a540068ea6b21b0b3d4d7ad6f2b63c576d17f93ceb5889a2b882dc5c547", "reuse": "K14 R8 source fold; change terminal tail family only"},
    {"path": "computations/unaudited-codex-orbit0-k22-direct-k15-four-sink-2026-08-24/run_k22_direct_k15_four_sink.rs", "sha256": "9a5599da22dbac007e80da8b3d38062257aad6084e9dbe8bfa14c0b62c0b6f3b", "reuse": "source-linear 485-slice grouped K15 four-sink engine"},
    {"path": "computations/unaudited-codex-orbit0-k22-direct23-source-fold-2026-08-24/run_k22_direct23_source_fold.rs", "sha256": "ccfd1af09fced6d05f0aeb40cf3ee482f8d8a26565f2448cbc30fb5c0952241b", "reuse": "combined D17/D18/D19 R8 source sectors"},
]

NONINTERFACE_EVIDENCE = [
    {"path": "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_k19_charge.json", "sha256": "8af5f43965fa6ab53d857dfea6b2b0241634783e744c100d85c24b3403f96e5a", "scope": "charge-only; no K19 rows or K20 tails"},
    {"path": "computations/unaudited-codex-orbit0-k22-availability-schedule-2026-08-24/results_k22_availability_schedule.json", "sha256": "7c31a27b3896038ed87e53f462a7491362219ea10ae7e501f7156af21666e694", "scope": "earlier availability/multiplex design, not evidence that multiplexing ran"},
]


GROUP_METADATA = {
    "source_D14_R2_2_2_3": ("hidden_collected_k18", ["hidden_k18_22_pivotable_rows"], 20, 3),
    "source_D14_R2_3_4": ("hidden_decorated_k16_pair", ["hidden_decorated_k16_pair_orbits"], 19, 4),
    "source_D14_R2_4_3": ("hidden_decorated_k16_pair", ["hidden_decorated_k16_pair_orbits"], 20, 3),
    "source_D14_R3_2_4": ("k14_source_formula", ["orbit0_structure"], 19, 4),
    "source_D14_R3_3_3": ("k14_source_formula", ["orbit0_structure"], 20, 3),
    "source_D14_R4_2_3": ("k14_source_formula", ["orbit0_structure"], 20, 3),
    "source_D15_R2_2_4": ("grouped_direct_k15_source", ["orbit0_structure", "direct_k15_rows"], 19, 4),
    "source_D15_R2_3_3": ("grouped_direct_k15_source", ["orbit0_structure", "direct_k15_rows"], 20, 3),
    "source_D15_R3_2_3": ("grouped_direct_k15_source", ["orbit0_structure", "direct_k15_rows"], 20, 3),
    "source_D15_R4_4": ("grouped_direct_k15_source", ["orbit0_structure", "direct_k15_rows"], 19, 4),
    "source_D16_R2_2_3": ("grouped_direct_k16_rows", ["direct_k16_rows"], 20, 3),
    "source_D16_R3_4": ("grouped_direct_k16_rows", ["direct_k16_rows"], 19, 4),
    "source_D16_R4_3": ("grouped_direct_k16_rows", ["direct_k16_rows"], 20, 3),
    "source_D17_R2_4": ("direct_D17_D18_D19_formula", ["orbit0_structure"], 19, 4),
    "source_D17_R3_3": ("direct_D17_D18_D19_formula", ["orbit0_structure"], 20, 3),
    "source_D18_R2_3": ("direct_D17_D18_D19_formula", ["orbit0_structure"], 20, 3),
    "source_D19_R4": ("direct_D17_D18_D19_formula", ["orbit0_structure"], 19, 4),
}


def intervals(total: int, parts: int) -> list[list[int]]:
    boundaries = [total * i // parts for i in range(parts + 1)]
    return [[boundaries[i], boundaries[i + 1]] for i in range(parts)]


EXECUTION_FAMILIES = [
    {
        "family_id": "hidden_collected_k18", "group_ids": ["source_D14_R2_2_2_3"],
        "input_artifact": "hidden_k18_22_pivotable_rows", "source_units": 158_439_965,
        "prefix_units": [1, 4096, 1_000_000], "planned_intervals": intervals(158_439_965, 3),
        "conservative_projected_max_shard_seconds": 345,
        "historical_basis": "same H18PIV2 source completed two K22 sinks in 387.878229 s; three intervals absorb the K3/K2 tail ratio",
        "contract": "K18 row -> K2 pivotable K20 -> every selected pivot -> 32 terminal K3 tails",
    },
    {
        "family_id": "hidden_decorated_k16_pair", "group_ids": ["source_D14_R2_3_4", "source_D14_R2_4_3"],
        "input_artifact": "hidden_decorated_k16_pair_orbits", "source_units": 101_545_723,
        "prefix_units": [4096, 1_000_000], "planned_intervals": intervals(101_545_723, 3),
        "conservative_projected_max_shard_seconds": 497,
        "historical_basis": "identical K22 intervals completed in 186.19/47.34/53.09 s; worst terminal tail ratio <=8/3 gives <497 s from the measured maximum",
        "contract": "decorated K16/pivot -> K3 pivotable K19 -> K4, and K4 pivotable K20 -> K3; separate sinks",
    },
    {
        "family_id": "k14_source_formula", "group_ids": ["source_D14_R3_2_4", "source_D14_R3_3_3", "source_D14_R4_2_3"],
        "input_artifact": "orbit0_structure", "source_units": 485,
        "prefix_units": [1, 8, 32, 64], "planned_intervals": intervals(485, 4),
        "conservative_projected_max_shard_seconds": 300,
        "historical_basis": "K22 64-slice gate 56.566792 s; four intervals and worst 8/3 tail factor target <300 s each",
        "contract": "source-linear K14 factor replay through every intermediate pivot, then terminal K4/K3 tails",
    },
    {
        "family_id": "grouped_direct_k15_source", "group_ids": ["source_D15_R2_2_4", "source_D15_R2_3_3", "source_D15_R3_2_3", "source_D15_R4_4"],
        "input_artifact": "orbit0_structure", "source_units": 485,
        "prefix_units": [1, 8, 32], "planned_intervals": intervals(485, 8),
        "conservative_projected_max_shard_seconds": 451,
        "historical_basis": "K22 122-slice maximum 337.592894 s; halved intervals and worst 8/3 tail factor target about 450 s",
        "contract": "source-linear reconstruction of 13,824 grouped K15 heads per R8 slice; four strict sinks",
    },
    {
        "family_id": "grouped_direct_k16_rows", "group_ids": ["source_D16_R2_2_3", "source_D16_R3_4", "source_D16_R4_3"],
        "input_artifact": "direct_k16_rows", "source_units": 24_097_095,
        "prefix_units": [1000, 10_000, 800_000], "planned_intervals": intervals(24_097_095, 8),
        "conservative_projected_max_shard_seconds": 240,
        "historical_basis": "800k K22 gates 7.75/14.28/5.43 s; tail-ratio conservative combined projection is <240 s per eighth",
        "contract": "one K16 checkpoint scan with three separately named recurrence sinks",
    },
    {
        "family_id": "direct_D17_D18_D19_formula", "group_ids": ["source_D17_R2_4", "source_D17_R3_3", "source_D18_R2_3", "source_D19_R4"],
        "input_artifact": "orbit0_structure", "source_units": 485,
        "prefix_units": [1, 8, 32], "planned_intervals": intervals(485, 3),
        "conservative_projected_max_shard_seconds": 366,
        "historical_basis": "same combined K22 sectors completed in 410.380572 s at 5.04 GiB; three intervals and worst 8/3 tail ratio target <366 s",
        "contract": "one R8 sector scan with D17/D18/D19 degree/response-separated sinks",
    },
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def check_artifact(name: str, spec: dict) -> dict:
    path = ROOT / spec["path"]
    if not path.is_file() or path.stat().st_size != spec["bytes"]:
        raise AssertionError(f"missing/size mismatch {name}")
    with path.open("rb") as stream:
        header = stream.read(max(32, len(spec.get("magic", ""))))
    if "magic" in spec and not header.startswith(spec["magic"].encode("latin1")):
        raise AssertionError(f"magic mismatch {name}")
    if "records" in spec and "record_bytes" in spec:
        expected = spec.get("header_bytes", 16) + spec["records"] * spec["record_bytes"]
        if expected != spec["bytes"]:
            raise AssertionError(f"record geometry mismatch {name}")
    if name == "orbit0_structure":
        if struct.unpack_from("<IIII", header, 11) != (384, 485, 78, 12):
            raise AssertionError("orbit0 structure count header changed")
    if name == "response_aux":
        scale, cover, pivots = struct.unpack_from("<QII", header, 8)
        if (scale, cover, pivots) != (281_801_520, 25, 78):
            raise AssertionError("response aux header changed")
    checked = {"exists": True, "size_checked": True, "header_schema_checked": "magic" in spec, "upstream_sha256_pin": spec["sha256"]}
    if spec["bytes"] < 1_000_000:
        if sha(path) != spec["sha256"]:
            raise AssertionError(f"hash mismatch {name}")
        checked["full_hash_checked_here"] = True
    else:
        checked["full_hash_reused_from_upstream_sealed_pin"] = True
    return checked


def write_atomic(path: Path, payload) -> None:
    temporary = Path(str(path) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def main() -> None:
    if sha(DAG_PATH) != DAG_SHA256:
        raise AssertionError("DAG file hash mismatch")
    dag = json.loads(DAG_PATH.read_text())
    if dag["logical_sha256"] != DAG_LOGICAL_SHA256:
        raise AssertionError("DAG logical hash mismatch")
    required = dag["required_reachable_lineage_ids_by_degree"]["23"]
    if len(required) != len(set(required)) or len(required) != 59:
        raise AssertionError("frozen K23 set changed")
    node_map = {node["id"]: node for node in dag["nodes"]}
    edge_map = {edge["child"]: edge for edge in dag["edges"]}

    groups = []
    flat = []
    family_counts = Counter()
    terminal_proofs = []
    lineage_ledger = []
    for group_id, group_ids in EXPECTED_GROUPS.items():
        family, artifacts, parent_degree, final_shift = GROUP_METADATA[group_id]
        for lineage in group_ids:
            node = node_map[lineage]
            edge = edge_map[lineage]
            responses = node["response_shifts"]
            if not node["reachable"] or node["degree"] != 23 or responses[-1] != final_shift:
                raise AssertionError(f"bad frozen node {lineage}")
            if node["direct_packet"]["degree"] + sum(responses) != 23:
                raise AssertionError(f"degree sum mismatch {lineage}")
            if 23 - final_shift != parent_degree or edge["shift"] != final_shift:
                raise AssertionError(f"parent/final edge mismatch {lineage}")
            if edge["tail_terms_per_pivot"] != (60 if final_shift == 4 else 32):
                raise AssertionError(f"tail count mismatch {lineage}")
            if edge["coefficient_rule"] != "child coefficient = -parent coefficient / pivot_count":
                raise AssertionError(f"coefficient rule mismatch {lineage}")
            parent_anchor_sum = 24 - parent_degree
            child_anchor_sum = parent_anchor_sum - 4 + (4 - final_shift)
            if child_anchor_sum != 1 or child_anchor_sum >= 4:
                raise AssertionError(f"terminality mismatch {lineage}")
            expected_sign = -1 if len(responses) % 2 == 0 else 1
            if node["sign_relative_to_unsigned_R8prime"] != expected_sign:
                raise AssertionError(f"sign mismatch {lineage}")
            if not node["denominator_product_class"]["global_scale_divides"]:
                raise AssertionError(f"U divisor class mismatch {lineage}")
            terminal_proofs.append({"id": lineage, "parent_degree": parent_degree, "final_shift": final_shift, "child_anchor_sum": child_anchor_sum})
            lineage_ledger.append({
                "id": lineage,
                "group_id": group_id,
                "availability": "SOURCE_REPLAY_REQUIRED",
                "source_family": family,
                "immediate_parent_id": edge["parent"],
                "immediate_parent_degree": parent_degree,
                "final_shift": final_shift,
                "terminal_tail_terms_per_selected_pivot": edge["tail_terms_per_pivot"],
                "child_anchor_sum": child_anchor_sum,
                "terminal": True,
                "frozen_dag_provenance_state": node["current_provenance"]["state"],
                "post_DAG_source_repair": (
                    "hidden retained source now present and pinned"
                    if node["current_provenance"]["state"] == "MISSING_DISCARDED_K14_K2_PIVOTABLE_PARENT"
                    else None
                ),
            })
        groups.append({
            "group_id": group_id,
            "ids": group_ids,
            "count": len(group_ids),
            "availability": "SOURCE_REPLAY_REQUIRED",
            "retained_terminal_profile_interface": False,
            "source_family": family,
            "artifacts": artifacts,
            "terminal_parent_degree": parent_degree,
            "final_shift": final_shift,
            "terminal_tail_terms_per_selected_pivot": 60 if final_shift == 4 else 32,
            "all_inputs_present": all((ROOT / ARTIFACTS[a]["path"]).is_file() for a in artifacts),
        })
        flat.extend(group_ids)
        family_counts[family] += len(group_ids)

    counts = Counter(flat)
    missing = [x for x in required if x not in counts]
    duplicate = sorted(x for x, count in counts.items() if count != 1)
    extra = sorted(set(flat) - set(required))
    if missing or duplicate or extra or set(flat) != set(required):
        raise AssertionError(f"partition failure missing={missing} duplicate={duplicate} extra={extra}")
    if Counter(g["final_shift"] for g in terminal_proofs) != Counter({3: 35, 4: 24}):
        raise AssertionError("final response split changed")
    if Counter(g["parent_degree"] for g in terminal_proofs) != Counter({19: 24, 20: 35}):
        raise AssertionError("parent degree split changed")

    artifact_checks = {name: check_artifact(name, spec) for name, spec in ARTIFACTS.items()}
    for engine in REUSABLE_ENGINES:
        if sha(ROOT / engine["path"]) != engine["sha256"]:
            raise AssertionError(f"engine pin mismatch {engine['path']}")
    for evidence in NONINTERFACE_EVIDENCE:
        if sha(ROOT / evidence["path"]) != evidence["sha256"]:
            raise AssertionError(f"noninterface evidence pin mismatch {evidence['path']}")
    for family in EXECUTION_FAMILIES:
        ivals = family["planned_intervals"]
        if ivals[0][0] != 0 or ivals[-1][1] != family["source_units"] or any(ivals[i][1] != ivals[i + 1][0] for i in range(len(ivals) - 1)):
            raise AssertionError(f"interval gap/overlap {family['family_id']}")
        if any(b <= a for a, b in ivals):
            raise AssertionError(f"empty interval {family['family_id']}")
        if family["conservative_projected_max_shard_seconds"] > 540:
            raise AssertionError(f"initial shard projection exceeds launch ceiling {family['family_id']}")
    scheduled_groups = [g for family in EXECUTION_FAMILIES for g in family["group_ids"]]
    if Counter(scheduled_groups) != Counter(EXPECTED_GROUPS.keys()):
        raise AssertionError("physical schedule does not cover 17 groups exactly once")

    expected_contract = {
        "status": "K23_EXPECTED_17_SCALAR_GROUP_CONTRACT_NO_VALUES",
        "degree": 23,
        "scale_U": U,
        "required_ids": 59,
        "groups": [{"group_id": group_id, "ids": group_ids, "required_manifest_fields": ["full_scaled_U", "irreducible_scaled_U", "full", "irreducible", "evidence_path", "evidence_sha256"]} for group_id, group_ids in EXPECTED_GROUPS.items()],
        "warning": "No scalar value is supplied or inferred. K22 scalar outputs are terminal and are not K23 inputs.",
    }
    availability_manifest = {"degree": 23, "scale_U": U, "groups": [], "scope": "availability-only zero-scalar manifest; intentionally incomplete"}
    write_atomic(HERE / "k23_expected_scalar_groups.json", expected_contract)
    write_atomic(HERE / "k23_manifest_availability_only.json", availability_manifest)

    result = {
        "status": "PASS_EXACT_K23_59_ID_AVAILABILITY_AND_BOUNDED_SCHEDULE",
        "scope": "availability, terminality, and execution schedule only; no K23 charge, residual, membership, or conjecture claim",
        "scale_U": U,
        "dag": {"path": str(DAG_PATH.relative_to(ROOT)), "sha256": DAG_SHA256, "logical_sha256": DAG_LOGICAL_SHA256, "required_K23_ids": 59, "required_ordered_ids": required, "partition_equal": True, "missing": [], "duplicate": [], "extra": []},
        "availability_counts": {"RETAINED_TERMINAL_PROFILE_INTERFACE": 0, "SOURCE_REPLAY_REQUIRED": 59, "GENUINELY_MISSING_PROVENANCE": 0},
        "final_response_counts": {"3": 35, "4": 24},
        "terminal_parent_degree_counts": {"19": 24, "20": 35},
        "terminality": {"universal": True, "child_anchor_sum": 1, "pivot_anchor_mass": 4, "proof": "for p=23-s: (24-p)-4+(4-s)=24-(p+s)=1<4"},
        "artifacts": ARTIFACTS,
        "artifact_checks": artifact_checks,
        "reusable_engine_pins": REUSABLE_ENGINES,
        "explicit_non_interfaces": [
            "K22 charges are terminal scalars at anchor mass 2; K23 parents are instead K19/K20 rows, so no K22 scalar can be prolonged.",
            "The frozen K19 charge artifacts retain incoming-response 43-byte terminal charge profiles/scalars, not literal K19 rows or outgoing selected-pivot profiles.",
            "K20/K21/K22 scalar results, response caches, and sample ledgers contain no prolongable immediate K19/K20 parent interface.",
            "Existing enriched terminal profiles have immediate parent degree K18 and suffice only for their already-named K22 K4 sinks, not K23.",
        ],
        "pinned_noninterface_evidence": NONINTERFACE_EVIDENCE,
        "groups": groups,
        "lineages": lineage_ledger,
        "source_family_id_counts": dict(sorted(family_counts.items())),
        "physical_folds": EXECUTION_FAMILIES,
        "bounded_gate": {
            "workers": 8,
            "launch_projection_seconds_max": 540,
            "hard_shard_wall_seconds": 600,
            "hard_single_family_cache_GiB": 8,
            "hard_aggregate_live_RSS_GiB": 16,
            "concurrency": "one physical fold shard at a time",
            "adaptive_rule": "after the largest named prefix, launch an interval only if conservative projected wall <=540 s; otherwise bisect it and rerun the prefix; watchdog discards any non-atomic attempt at 570 s",
            "projection_qualification": "listed projections are conservative planning values from measured K22 engines and terminal tail ratios, not launch authority; the new K23 measured prefix is mandatory",
            "merge": "exact source interval coverage, no gap/overlap, distinct named sinks, sum scaled integers before division by U, atomic output, no parent rows",
            "literal_referee": "257 deterministic distributed nonzero continuations per scalar group where realized; replay source, pivots, divisors, sign, terminal tails, and charge independently",
        },
        "planned_shards": sum(len(f["planned_intervals"]) for f in EXECUTION_FAMILIES),
        "K22_nonprolongation_guard": "No K22 scalar or terminal child is an input to this schedule; each K23 sink is recomputed from its K19/K20 parent via the pinned source family.",
        "assembler": {"program": str((HERE / "assemble_k23_59_exact.py").relative_to(ROOT)), "expected_group_contract": str((HERE / "k23_expected_scalar_groups.json").relative_to(ROOT)), "availability_manifest": str((HERE / "k23_manifest_availability_only.json").relative_to(ROOT)), "required_scalar_groups": 17},
    }
    logical_basis = json.loads(json.dumps(result))
    result["logical_sha256"] = hashlib.sha256(json.dumps(logical_basis, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    write_atomic(HERE / "results_k23_availability_schedule.json", result)
    print(json.dumps({"status": result["status"], "required_ids": 59, "source_replay_ids": 59, "retained_terminal_profile_ids": 0, "physical_folds": 6, "planned_shards": result["planned_shards"], "logical_sha256": result["logical_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
