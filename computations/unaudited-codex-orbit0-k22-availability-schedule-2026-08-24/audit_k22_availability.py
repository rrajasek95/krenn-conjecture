#!/usr/bin/env python3
"""Exact availability/schedule audit for the 76 reachable K22 lineages.

This program is deliberately read-only with respect to the large retained
checkpoints.  It proves the lineage partition from the frozen recurrence DAG,
checks the local artifact schemas/sizes used by the schedule, and writes no
K22 charge or row data.
"""

from collections import Counter
from pathlib import Path
import hashlib
import json
import os
import struct


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DAG_PATH = ROOT / (
    "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/"
    "results_recurrence_dag.json"
)
U = 400_591_699_200


def qpath(value):
    return ROOT / value


ARTIFACTS = {
    "orbit0_structure": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin",
        "bytes": 115_275,
        "sha256": "55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b",
        "role": "frozen R8prime records and direct-factor source formula",
    },
    "direct_k15_rows": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k15.bin",
        "bytes": 169_958_768,
        "records": 5_311_211,
        "sha256": "e79b752f94ad3b16ce4cf7d3f044e8887bda54bba5c6298ab31338bb121fa20f",
        "role": "literal grouped direct-K15 canonical rows",
    },
    "direct_k16_rows": {
        "path": "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin",
        "bytes": 771_107_056,
        "records": 24_097_095,
        "sha256": "93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3",
        "role": "literal grouped direct-K16 canonical rows",
    },
    "hidden_decorated_k16_pair_orbits": {
        "path": "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/hidden_k16_decorated_pair_orbits_full.bin",
        "bytes": 5_381_923_399,
        "records": 101_545_723,
        "record_bytes": 53,
        "magic": "H16ORM1\x00",
        "sha256": "22f91fc887caecb628df495b6a19e319c0ada39b6940b1ca4f795ae09d6c21c8",
        "role": "exact decorated (K16 row, selected pivot) H-orbits for the hidden D14 R2 subtree",
    },
    "hidden_k18_22_pivotable_rows": {
        "path": "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin",
        "bytes": 12_675_197_280,
        "records": 158_439_965,
        "record_bytes": 80,
        "magic": "H18PIV2\x00",
        "sha256": "442f4220e7f224b9961c8236fff918c6274337e672b5cf5e62c87614b53044c8",
        "role": "literal collected pivotable D14 R2-2 K18 parent rows",
    },
    "direct_k18_profiles": {
        "path": "computations/unaudited-codex-orbit0-direct-k18-profile-census-2026-08-23/direct_k18_enriched_profiles.bin",
        "bytes": 70_494_808,
        "records": 979_091,
        "sha256": "d77f2a84f220aad9f52fe81547ab730a6b834005b27e6f47172bb80cf5850da2",
        "role": "terminal-only (profile, signature, pivot, weight, witness) K18 interface",
    },
    "k14_r4_k18_profiles": {
        "path": "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/k14_k4_enriched_profiles.bin",
        "bytes": 1_894_591_760,
        "records": 18_217_226,
        "sha256": "5cc8c15b2333937ddfaefac1ec056b2f2fd899f5b89ea5b0276d374b05d92d7f",
        "role": "terminal-only K18 interface for D14 R4",
    },
    "k15_r3_k18_profiles": {
        "path": "computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/checkpoint_k15_k3_profiles_merged.bin",
        "bytes": 2_658_696_792,
        "records": 25_564_391,
        "record_bytes": 104,
        "magic": "K15MRG1\x00",
        "sha256": "8b05f3fb8edcda062111d20089309abb85d4ccd8675d289947178b437139c1db",
        "role": "terminal-only grouped K18 interface for D15 R3",
    },
    "k16_r2_k18_profiles": {
        "path": "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/checkpoint_k16_k2_profiles_merged.bin",
        "bytes": 715_131_168,
        "records": 6_876_260,
        "record_bytes": 104,
        "magic": "K16MRG1\x00",
        "sha256": "d23271184b8258634cbf6f0942c4b1068e04c505e206b08fd3638e1c9b03be03",
        "role": "terminal-only grouped K18 interface for D16 R2",
    },
}


BASES = {
    14: ["222"],
    15: ["223", "232", "322"],
    16: ["224", "233", "242", "323", "332", "422"],
    17: ["234", "243", "324", "333", "342", "423", "432"],
    18: ["244", "334", "343", "424", "433", "442"],
    19: ["344", "434", "443"],
}


def lineage_ids(degree, response):
    return [f"D{degree}:{digits}|R:{response}" for digits in BASES[degree]]


GROUPS = [
    # Immediate K18 terminal interfaces: one selected pivot/profile record and 60 K4 tails.
    dict(group_id="profile_D18_R4", ids=lineage_ids(18, "4"), availability="TERMINAL_READY_PROFILE_INTERFACE", artifacts=["direct_k18_profiles"], terminal_parent_degree=18, final_shift=4, profile_records=979_091, exact_terminal_tail_evaluations=58_745_460),
    dict(group_id="profile_D14_R4_4", ids=lineage_ids(14, "4-4"), availability="TERMINAL_READY_PROFILE_INTERFACE", artifacts=["k14_r4_k18_profiles"], terminal_parent_degree=18, final_shift=4, profile_records=18_217_226, exact_terminal_tail_evaluations=1_093_033_560),
    dict(group_id="profile_D15_R3_4", ids=lineage_ids(15, "3-4"), availability="TERMINAL_READY_PROFILE_INTERFACE", artifacts=["k15_r3_k18_profiles"], terminal_parent_degree=18, final_shift=4, profile_records=25_564_391, exact_terminal_tail_evaluations=1_533_863_460),
    dict(group_id="profile_D16_R2_4", ids=lineage_ids(16, "2-4"), availability="TERMINAL_READY_PROFILE_INTERFACE", artifacts=["k16_r2_k18_profiles"], terminal_parent_degree=18, final_shift=4, profile_records=6_876_260, exact_terminal_tail_evaluations=412_575_600),
    # One immediate literal K18 checkpoint.
    dict(group_id="literal_D14_R2_2_4", ids=lineage_ids(14, "2-2-4"), availability="RETAINED_LITERAL_PARENT_CHECKPOINT", artifacts=["hidden_k18_22_pivotable_rows"], terminal_parent_degree=18, final_shift=4, input_records=158_439_965, selected_parent_pivots=399_275_484, exact_terminal_tail_evaluations=23_956_529_040),
    # K19 parent reconstructions, followed by one final K3 response.
    dict(group_id="source_D19_R3", ids=lineage_ids(19, "3"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["orbit0_structure"], terminal_parent_degree=19, final_shift=3, known_selected_terminal_pivots=111_744_000, exact_terminal_tail_evaluations=3_575_808_000),
    dict(group_id="source_D15_R4_3", ids=lineage_ids(15, "4-3"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["direct_k15_rows"], terminal_parent_degree=19, final_shift=3, source_records=5_311_211, known_selected_terminal_pivots=1_549_305_840, exact_terminal_tail_evaluations=49_577_786_880),
    dict(group_id="source_D16_R3_3", ids=lineage_ids(16, "3-3"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["direct_k16_rows"], terminal_parent_degree=19, final_shift=3, source_records=24_097_095, known_selected_terminal_pivots=2_041_782_688, exact_terminal_tail_evaluations=65_337_046_016),
    dict(group_id="source_D17_R2_3", ids=lineage_ids(17, "2-3"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["orbit0_structure"], terminal_parent_degree=19, final_shift=3, known_selected_terminal_pivots=1_448_947_200, exact_terminal_tail_evaluations=46_366_310_400),
    dict(group_id="source_D14_R2_3_3", ids=lineage_ids(14, "2-3-3"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["hidden_decorated_k16_pair_orbits"], terminal_parent_degree=19, final_shift=3, source_records=101_545_723, representative_K19_children=3_249_463_136, known_selected_terminal_pivots=1_774_721_368, exact_terminal_tail_evaluations=56_791_083_776),
    dict(group_id="source_D14_R3_2_3", ids=lineage_ids(14, "3-2-3"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["orbit0_structure"], terminal_parent_degree=19, final_shift=3, known_selected_terminal_pivots=5_075_412_480, exact_terminal_tail_evaluations=162_413_199_360),
    dict(group_id="source_D15_R2_2_3", ids=lineage_ids(15, "2-2-3"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["direct_k15_rows"], terminal_parent_degree=19, final_shift=3, source_records=5_311_211, known_selected_terminal_pivots=None, exact_terminal_tail_evaluations=None),
    # K20 parent reconstructions, followed by one final K2 response.
    dict(group_id="source_D16_R4_2", ids=lineage_ids(16, "4-2"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["direct_k16_rows"], terminal_parent_degree=20, final_shift=2, source_records=24_097_095),
    dict(group_id="source_D17_R3_2", ids=lineage_ids(17, "3-2"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["orbit0_structure"], terminal_parent_degree=20, final_shift=2),
    dict(group_id="source_D18_R2_2", ids=lineage_ids(18, "2-2"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["orbit0_structure"], terminal_parent_degree=20, final_shift=2),
    dict(group_id="source_D14_R2_2_2_2", ids=lineage_ids(14, "2-2-2-2"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["hidden_k18_22_pivotable_rows"], terminal_parent_degree=20, final_shift=2, source_records=158_439_965, known_K20_children=4_791_305_808, known_pivotable_K20_children=570_281_318),
    dict(group_id="source_D14_R2_4_2", ids=lineage_ids(14, "2-4-2"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["hidden_decorated_k16_pair_orbits"], terminal_parent_degree=20, final_shift=2, source_records=101_545_723),
    dict(group_id="source_D14_R3_3_2", ids=lineage_ids(14, "3-3-2"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["orbit0_structure"], terminal_parent_degree=20, final_shift=2),
    dict(group_id="source_D14_R4_2_2", ids=lineage_ids(14, "4-2-2"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["orbit0_structure"], terminal_parent_degree=20, final_shift=2),
    dict(group_id="source_D15_R2_3_2", ids=lineage_ids(15, "2-3-2"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["direct_k15_rows"], terminal_parent_degree=20, final_shift=2, source_records=5_311_211),
    dict(group_id="source_D15_R3_2_2", ids=lineage_ids(15, "3-2-2"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["direct_k15_rows"], terminal_parent_degree=20, final_shift=2, source_records=5_311_211),
    dict(group_id="source_D16_R2_2_2", ids=lineage_ids(16, "2-2-2"), availability="SOURCE_REPLAY_REQUIRED", artifacts=["direct_k16_rows"], terminal_parent_degree=20, final_shift=2, source_records=24_097_095),
]


EXECUTION_FAMILIES = [
    {
        "family_id": "terminal_k18_profiles",
        "group_ids": ["profile_D18_R4", "profile_D14_R4_4", "profile_D15_R3_4", "profile_D16_R2_4"],
        "input_scans": 4,
        "contract": "profile_terminal_fold(profile,signature,pivot,weight,K4)->degree_separated_Q_sink",
        "gate": "self-test; 2^16-record prefix; full only if projected wall <=600 s and RSS <=16 GiB",
    },
    {
        "family_id": "hidden_collected_k18",
        "group_ids": ["literal_D14_R2_2_4", "source_D14_R2_2_2_2"],
        "input_scans": 1,
        "contract": "literal_parent_fold(K18 row,scaled weight): fan K4 directly and K2->pivotable K20->K2",
        "gate": "1-record and 4096-record guards; 1,000,000-record measured interval; shard before full unless <=600 s/16 GiB; no child rows",
    },
    {
        "family_id": "hidden_decorated_k16_pair",
        "group_ids": ["source_D14_R2_3_3", "source_D14_R2_4_2"],
        "input_scans": 1,
        "contract": "decorated_pair_fold(K16,pivot,weight,m2): fan K3->K19->K3 and K4->K20->K2",
        "gate": "4096 then 1,000,000 pair-orbit prefix; interval shards; cache hard guard <=8 GiB; no K19/K20 rows",
    },
    {
        "family_id": "k14_source_formula",
        "group_ids": ["source_D14_R3_2_3", "source_D14_R3_3_2", "source_D14_R4_2_2"],
        "input_scans": 1,
        "contract": "factor_source_fold(R8,K14 packet): retain literal row only through each remaining pivot; separate response-sequence sinks",
        "gate": "8 then 32 of 485 R8-record prefix; shard if projected wall >600 s or RSS >16 GiB",
    },
    {
        "family_id": "grouped_direct_k15_rows",
        "group_ids": ["source_D15_R4_3", "source_D15_R2_2_3", "source_D15_R2_3_2", "source_D15_R3_2_2"],
        "input_scans": 1,
        "contract": "literal_source_fold(K15 row,coefficient): fan first response shifts and keep four grouped recurrence sinks",
        "gate": "4096, 131072, then <=1% measured record interval; run restartable shards only",
    },
    {
        "family_id": "grouped_direct_k16_rows",
        "group_ids": ["source_D16_R3_3", "source_D16_R4_2", "source_D16_R2_2_2"],
        "input_scans": 1,
        "contract": "literal_source_fold(K16 row,coefficient): fan first response shifts and keep three grouped recurrence sinks",
        "gate": "10000 then 800000 record prefix; full only as bounded intervals; aggregate RSS <=16 GiB",
    },
    {
        "family_id": "direct_D17_D18_D19_formula",
        "group_ids": ["source_D17_R2_3", "source_D17_R3_2", "source_D18_R2_2", "source_D19_R3"],
        "input_scans": 1,
        "contract": "factor_source_fold(R8,direct sectors D17..D19): degree/response-separated exact sinks",
        "gate": "8 then 32 of 485 R8-record prefix; sector-shard if any sink projects above 600 s",
    },
]


REUSABLE_ENGINES = [
    {"path": "computations/unaudited-codex-orbit0-k21-hidden-232-charge-2026-08-24/run_k21_hidden_232_charge.rs", "sha256": "4228a7ca6380329bae6c1351e32605bfad2cf04b0c7c5261c877e913cff0fe5c", "reuse": "decorated-pair reader, exact next-pivot division, bounded response cache"},
    {"path": "computations/unaudited-codex-orbit0-k21-d15-r4-2-charge-2026-08-24/run_k21_d15_r4_2_charge.rs", "sha256": "e63cdfe040fb12a7ab093e69c7bac7834dea51c5cd704cb76686dc36b61af98c", "reuse": "interval K15 literal source fold and atomic shard result"},
    {"path": "computations/unaudited-codex-orbit0-k21-direct-k16-32-2026-08-24/run_k21_direct_k16_32.rs", "sha256": "b4f0c4ae64d2d29d1febb2bd6beb4b2e745f944701404620c41cd591d781f73a", "reuse": "grouped K16 checkpoint source fold"},
    {"path": "computations/unaudited-codex-orbit0-k21-direct-k17-22-2026-08-24/run_k21_direct_k17_22.rs", "sha256": "7999b1797e3103f254977b17f60ff42088f4eee6726ba4e7006b86f08cff05b7", "reuse": "factorized direct-sector fold and per-sector accounting"},
    {"path": "computations/unaudited-codex-orbit0-k21-d14-322-charge-2026-08-24/run_k21_d14_322_charge.rs", "sha256": "9667311ff4c870eee1f6a8e7f881bb9082f01f1b6bceee7947404901a8003e72", "reuse": "deep K14 source recursion with exact U divisions"},
    {"path": "computations/unaudited-codex-orbit0-k20-222-consumer-design-2026-08-23/consume_k18_222_to_k20.rs", "sha256": "1df3172a5169c692e07acbc3c1eadf1d83a508ed1c19ac0737460fc7b2b8bb3c", "reuse": "H18PIV2 literal checkpoint reader and next-pivot enumeration"},
]


def check_artifact(name, spec):
    path = qpath(spec["path"])
    if not path.is_file():
        raise AssertionError(f"missing artifact {name}: {path}")
    actual_size = path.stat().st_size
    if actual_size != spec["bytes"]:
        raise AssertionError(f"size mismatch {name}: {actual_size}")
    checked = {"exists": True, "size_checked": True, "full_hash_reused_from_upstream_pin": True}
    # Cheap local schema guards.  The multi-GB full hashes are upstream-pinned.
    if "magic" in spec:
        with path.open("rb") as stream:
            magic = stream.read(8)
            header = magic + stream.read(72)
        if magic != spec["magic"].encode("latin1"):
            raise AssertionError(f"magic mismatch {name}: {magic!r}")
        if name == "hidden_decorated_k16_pair_orbits":
            if struct.unpack_from("<Q", header, 48)[0] != spec["records"]:
                raise AssertionError("decorated-pair count mismatch")
            if actual_size != 80 + spec["record_bytes"] * spec["records"]:
                raise AssertionError("decorated-pair geometry mismatch")
        if name == "hidden_k18_22_pivotable_rows":
            if struct.unpack_from("<Q", header, 48)[0] != spec["records"]:
                raise AssertionError("H18PIV2 count mismatch")
            if actual_size != 80 + spec["record_bytes"] * spec["records"]:
                raise AssertionError("H18PIV2 geometry mismatch")
        if name in ("k15_r3_k18_profiles", "k16_r2_k18_profiles"):
            if struct.unpack_from("<Q", header, 56)[0] != spec["records"]:
                raise AssertionError(f"profile count mismatch {name}")
            if actual_size != 128 + spec["record_bytes"] * spec["records"]:
                raise AssertionError(f"profile geometry mismatch {name}")
        checked["header_schema_checked"] = True
    if actual_size <= 1_000_000:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != spec["sha256"]:
            raise AssertionError(f"digest mismatch {name}")
        checked["full_hash_checked_here"] = True
    return checked


def terminality_proof(parent_degree, shift):
    # In the frozen anchor signature, degree d has anchor sum 24-d.  A pivot
    # removes four anchor incidences; a K_shift tail restores 4-shift.
    before = 24 - parent_degree
    after = before - 4 + (4 - shift)
    return {
        "parent_degree": parent_degree,
        "response_shift": shift,
        "parent_anchor_sum": before,
        "pivot_removes": 4,
        "tail_restores": 4 - shift,
        "child_anchor_sum": after,
        "available_four_anchor_pivot_impossible": after < 4,
    }


def main():
    dag = json.loads(DAG_PATH.read_text())
    if dag["logical_sha256"] != "ad59639716fe2a2cc04fca83a189d74ff8c1f5bbe6d7257676dd458f4c768a66":
        raise AssertionError("frozen DAG logical digest changed")
    required = dag["required_reachable_lineage_ids_by_degree"]["22"]
    if len(required) != len(set(required)) or len(required) != 76:
        raise AssertionError("K22 interface is not exactly 76 unique IDs")

    edges = {edge["child"]: edge for edge in dag["edges"]}
    nodes = {node["id"]: node for node in dag["nodes"]}
    flat = [item for group in GROUPS for item in group["ids"]]
    duplicates = sorted(item for item, count in Counter(flat).items() if count != 1)
    missing = [item for item in required if item not in set(flat)]
    extra = sorted(set(flat) - set(required))
    if duplicates or missing or extra:
        raise AssertionError(f"partition mismatch duplicate={duplicates} missing={missing} extra={extra}")

    artifact_checks = {name: check_artifact(name, spec) for name, spec in ARTIFACTS.items()}
    engine_checks = []
    for engine in REUSABLE_ENGINES:
        path = qpath(engine["path"])
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != engine["sha256"]:
            raise AssertionError(f"engine pin mismatch {path}")
        engine_checks.append({**engine, "full_hash_checked_here": True})

    lineages = []
    for group in GROUPS:
        for item in group["ids"]:
            edge = edges[item]
            node = nodes[item]
            if not edge["child_reachable"] or not node["reachable"] or node["degree"] != 22:
                raise AssertionError(f"bad reachable K22 node {item}")
            if edge["shift"] != group["final_shift"]:
                raise AssertionError(f"final shift mismatch {item}")
            parent = nodes[edge["parent"]]
            if parent["degree"] != group["terminal_parent_degree"]:
                raise AssertionError(f"parent degree mismatch {item}")
            proof = terminality_proof(parent["degree"], edge["shift"])
            if proof["child_anchor_sum"] != 2 or not proof["available_four_anchor_pivot_impossible"]:
                raise AssertionError(f"terminality failed {item}")
            lineages.append({
                "id": item,
                "group_id": group["group_id"],
                "availability": group["availability"],
                "parent_id": edge["parent"],
                "parent_degree": parent["degree"],
                "final_response_shift": edge["shift"],
                "tail_terms_per_selected_pivot": edge["tail_terms_per_pivot"],
                "sign_relative_to_unsigned_R8prime": node["sign_relative_to_unsigned_R8prime"],
                "terminal_anchor_sum": proof["child_anchor_sum"],
            })

    counts = Counter(item["availability"] for item in lineages)
    if counts != Counter({
        "TERMINAL_READY_PROFILE_INTERFACE": 16,
        "RETAINED_LITERAL_PARENT_CHECKPOINT": 1,
        "SOURCE_REPLAY_REQUIRED": 59,
    }):
        raise AssertionError(f"availability counts changed: {counts}")
    shift_counts = Counter(item["final_response_shift"] for item in lineages)
    if shift_counts != Counter({2: 35, 3: 24, 4: 17}):
        raise AssertionError(f"shift counts changed: {shift_counts}")

    direct_k20 = nodes["D20:444|R:direct"]
    fake_child = nodes["D20:444|R:2"]
    if not direct_k20["reachable"] or fake_child["reachable"] or fake_child["reachable_anchor_signatures"] != 0:
        raise AssertionError("direct-K20 empty outgoing-signature guard changed")

    groups = []
    for group in GROUPS:
        groups.append({**group, "count": len(group["ids"]), "all_inputs_present": all(artifact_checks[key]["exists"] for key in group["artifacts"])})

    result = {
        "status": "PASS_EXACT_K22_76_ID_AVAILABILITY_AND_BOUNDED_SCHEDULE_AUDIT",
        "scope": "availability, terminality, scheduling, and assembler integration only; no K22 charge run and no K22 rows",
        "scale_U": U,
        "dag": {
            "path": str(DAG_PATH.relative_to(ROOT)),
            "sha256": "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
            "logical_sha256": dag["logical_sha256"],
            "required_K22_ids": 76,
            "partition_equal": True,
            "missing": [], "duplicate": [], "extra": [],
        },
        "availability_counts": dict(sorted(counts.items())),
        "genuinely_missing_provenance": {"count": 0, "ids": [], "qualification": "No immediate K19/K20 parent checkpoint survives for 59 IDs, but every one has a complete retained literal or factorized source replay route."},
        "final_response_counts": {str(key): value for key, value in sorted(shift_counts.items())},
        "terminality": {
            "universal_K22_proof": "For parent degree p=22-s and response shift s, anchor sum is (24-p)-4+(4-s)=24-(p+s)=2<4; hence no four-anchor K0 pivot exists.",
            "full_equals_irreducible": True,
            "stronger_K21_to_K24_statement": "Every degree d>=21 has anchor sum 24-d in {3,2,1,0}, so every realized K21,K22,K23,K24 response child is terminal.",
            "checked_all_76_edges": True,
        },
        "direct_K20_nonbranch_guard": {
            "parent": "D20:444|R:direct",
            "candidate": "D20:444|R:2",
            "candidate_reachable": False,
            "reachable_anchor_signatures": 0,
            "consequence": "No 77th K22 lineage exists.",
        },
        "artifacts": ARTIFACTS,
        "artifact_checks": artifact_checks,
        "groups": groups,
        "lineages": sorted(lineages, key=lambda item: required.index(item["id"])),
        "execution_families": EXECUTION_FAMILIES,
        "reusable_engines": engine_checks,
        "source_faithful_kernel": {
            "literal_state": "(canonical row, signed scaled coefficient, exact response-prefix provenance)",
            "pivot_step": "enumerate every literal dividing pivot, m=len(pivots), assert coefficient % m == 0, then apply w_child=-w_parent/m to every requested K2/K3/K4 tail",
            "folding_theorem": "Occurrencewise scalar folding is exact because pivot count and 77-charge are row functions invariant under H; identical canonical rows have the same divisor, so signed collection commutes with the linear response operator.",
            "compression_guard": "Profile compression is allowed only at the final response. No terminal-only K19/K20 charge/profile or exact-zero-omitting profile is prolonged.",
            "output_guard": "Atomic scalar/count/sample JSON only; never write K19, K20, or K22 row streams.",
        },
        "bounded_gate": {
            "required_prefixes": ["one-source or tiny self-test", "4096 source units", "representative >=1% or named historical prefix"],
            "full_launch_condition": "projected wall <=600 seconds per shard, aggregate live RSS <=16 GiB, exact-U division and universal terminality assertions enabled",
            "cache_condition": "bounded chunk cache, hard abort before 8 GiB for a single worker family",
            "samples": "257 deterministic distributed nonzero continuations per scalar group where available; replay literal pivots, division, tail, sign, and 77-charge independently",
            "merge": "exact interval coverage with no gaps/overlaps; sum scaled integers before one final U reduction; atomic rename; no row output",
        },
        "multiplex": {
            "principle": "After a literal K19 or K20 parent and its pivot are reconstructed, fan K2/K3/K4 terminal tails in the same pass into degree-separated sinks.",
            "K19_parent_sinks": ["K21 via K2", "K22 via K3", "K23 via K4"],
            "K20_parent_sinks": ["K22 via K2", "K23 via K3", "K24 via K4"],
            "guard": "Never combine degree ledgers or scalar sinks; each output fragment names exactly its frozen DAG IDs and is assembled only at its own degree.",
            "benefit": "The seven source families need not be rescanned separately for K22, K23, and K24 once their preterminal literal parent is realized.",
        },
        "explicit_non_interfaces": [
            "K19/K20 scalar charge results contain no prolongable parent rows.",
            "weights_k17_* and enriched K18 profile files omit exact-zero aggregates and are terminal-only; only the four named final-K4 K22 groups may use profiles.",
            "K21 charge result caches and sample ledgers are referees, not K19/K20 checkpoints.",
            "The complete K20 direct D20:444 scalar has no outgoing pivot and contributes no K22 lineage.",
        ],
        "assembler": {
            "program": str((HERE / "assemble_k22_76_exact.py").relative_to(ROOT)),
            "availability_manifest": str((HERE / "k22_manifest_availability_only.json").relative_to(ROOT)),
            "expected_group_contract": str((HERE / "k22_expected_scalar_groups.json").relative_to(ROOT)),
            "current_covered_ids": 0,
            "current_missing_ids": 76,
        },
    }
    contract = {
        "status": "K22_EXPECTED_SCALAR_GROUP_CONTRACT_NO_VALUES",
        "degree": 22,
        "scale_U": U,
        "required_ids": 76,
        "expected_scalar_groups": [
            {
                "group_id": group["group_id"],
                "ids": group["ids"],
                "availability": group["availability"],
                "artifacts": group["artifacts"],
                "terminal_parent_degree": group["terminal_parent_degree"],
                "final_shift": group["final_shift"],
                "future_manifest_fields": [
                    "full_scaled_U", "irreducible_scaled_U", "full", "irreducible",
                    "evidence_path", "evidence_sha256",
                ],
            }
            for group in GROUPS
        ],
        "coverage_equal": True,
        "guard": "This file carries no charge values and is not an assembler manifest. A producer must emit one exact scalar fragment per listed group, although independently refined subgroups are allowed if the strict 76-ID union remains exact.",
    }
    contract["logical_sha256"] = hashlib.sha256(json.dumps(contract, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    contract_output = HERE / "k22_expected_scalar_groups.json"
    contract_temporary = Path(str(contract_output) + ".tmp")
    contract_temporary.write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n")
    contract_temporary.replace(contract_output)
    logical = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    output = HERE / "results_k22_availability_schedule.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps({"status": result["status"], "counts": result["availability_counts"], "logical_sha256": logical}, sort_keys=True))


if __name__ == "__main__":
    main()
