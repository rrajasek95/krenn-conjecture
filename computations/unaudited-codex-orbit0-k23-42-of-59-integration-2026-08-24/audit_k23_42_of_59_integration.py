#!/usr/bin/env python3
"""Independent fail-closed referee for the strict K23 42/59 partial integration."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
U = 400_591_699_200
MANIFEST = HERE / "k23_manifest_direct23_k16_hidden_42_of_59.json"
PARTIAL = HERE / "results_k23_direct23_k16_hidden_42_of_59_partial.json"
DAG = ROOT / "computations/unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23/results_recurrence_dag.json"
SCHEDULE = ROOT / "computations/unaudited-codex-orbit0-k23-availability-schedule-2026-08-24"
ASSEMBLER = SCHEDULE / "assemble_k23_59_exact.py"
CONTRACT = SCHEDULE / "k23_expected_scalar_groups.json"
DIRECT = ROOT / "computations/unaudited-codex-orbit0-k23-direct23-independent-integration-2026-08-24"
K16 = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k16-18-charge-2026-08-24"
HIDDEN = ROOT / "computations/unaudited-codex-orbit0-k23-hidden-collected-k18-2026-08-24"

PINS = {
    DAG: "469639f662682d3e39b5b9f2d1055e113826a93bd416dbdcb788881e9ffe44fa",
    ASSEMBLER: "b189ddf195af4e5e896aee495bf7adbc074af0108a4f026ae852fbbabaacbaaf",
    CONTRACT: "6d59f1a24771e3a5e595ab79d8d0309881edea085da62c34b8e70cf93757c9ab",
    DIRECT / "k23_manifest_direct23_23_of_59.json": "acfe5a4e005495eb42ea0fa04b9423e73bde1308cb997f8344dabcd58993d23d",
    DIRECT / "results_k23_direct23_independent_integration_audit.json": "f4aa0bbf83e966feab4ceeff9d4b20ac488bf9fec42015c1f16a9d62004004ba",
    K16 / "k23_direct_k16_18_fragment_manifest.json": "9c37703f0c4e5c32f8993caf486eca18b8ed9d2bf46dab8a0192abc5af1397a1",
    K16 / "results_k23_direct_k16_18.json": "ba05ebd7bdd28528b6ff6ed78df60b776e43a7b0fcc19597d8023bad5ca403f0",
    K16 / "results_k23_direct_k16_18_literal_referee.json": "56ed7ef4b831b22c43fc5218646114490dcca14a34c1c5d162afcf2401bfcd98",
    HIDDEN / "k23_hidden_collected_singleton_fragment_manifest.json": "ac797c5f1e529de2fd2dc12d5a761fd55d6216bf3213da45f7701c8dfe9cb06d",
    HIDDEN / "results_k23_hidden_collected_complete_package_audit.json": "28a89ac4448ff9e9c776fc464fc0eba37355c6dc7e1cb98cfe7de9fe96565c00",
    ROOT / "computations/unaudited-codex-orbit0-k23-direct23-source-fold-2026-08-24/results_k23_direct23.json": "e84a39d027e07ad56d1c4d67dd9cab733ef25575aa324c892157deb80272767f",
    K16 / "results_k23_direct_k16_223.json": "ac15faad3d2d249ee57787ac28d2d7f48d6f6dbdb388b4d7c95279e2067eb6da",
    K16 / "results_k23_direct_k16_34.json": "371463f3feaf52183238af0d54b0c7f61773761e509bd0c075442225b1ad08ec",
    K16 / "results_k23_direct_k16_43.json": "d75a8afd74e6fa2990aebec237d01319ee365fc202786bd0d24ee1639205a4db",
    HIDDEN / "results_k23_hidden_collected_k18.json": "265498ca2af6aa43bb9099af532988571d647ef1f08698a262fe87320479a08e",
}

EXPECTED_GROUPS = [
    "source_D14_R2_2_2_3",
    "source_D16_R2_2_3",
    "source_D16_R3_4",
    "source_D16_R4_3",
    "source_D17_R2_4",
    "source_D17_R3_3",
    "source_D18_R2_3",
    "source_D19_R4",
]
EXPECTED_MISSING_GROUPS = [
    "source_D14_R2_3_4",
    "source_D14_R2_4_3",
    "source_D14_R3_2_4",
    "source_D14_R3_3_3",
    "source_D14_R4_2_3",
    "source_D15_R2_2_4",
    "source_D15_R2_3_3",
    "source_D15_R3_2_3",
    "source_D15_R4_4",
]
EXPECTED_MISSING_IDS = [
    "D14:222|R:2-3-4",
    "D14:222|R:2-4-3",
    "D14:222|R:3-2-4",
    "D14:222|R:3-3-3",
    "D14:222|R:4-2-3",
    "D15:223|R:2-2-4",
    "D15:223|R:2-3-3",
    "D15:223|R:3-2-3",
    "D15:223|R:4-4",
    "D15:232|R:2-2-4",
    "D15:232|R:2-3-3",
    "D15:232|R:3-2-3",
    "D15:232|R:4-4",
    "D15:322|R:2-2-4",
    "D15:322|R:2-3-3",
    "D15:322|R:3-2-3",
    "D15:322|R:4-4",
]
EXPECTED_SUBTOTAL = -4_222_958_701_661_124_231_168


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def source_shape(entry: dict) -> dict:
    return {key: entry[key] for key in (
        "ids", "full_scaled_U", "irreducible_scaled_U", "full", "irreducible",
        "evidence_path", "evidence_sha256",
    )}


def reject(module, manifest: dict, needle: str) -> None:
    try:
        module.assemble(manifest, allow_partial=True)
    except ValueError as error:
        assert needle in str(error), (needle, str(error))
    else:
        raise AssertionError(f"hostile manifest accepted: {needle}")


def main() -> None:
    for path, digest in PINS.items():
        assert sha(path) == digest, f"source hash mismatch: {path}"

    manifest = load(MANIFEST)
    partial = load(PARTIAL)
    dag = load(DAG)
    contract = load(CONTRACT)
    assert (manifest["degree"], manifest["scale_U"]) == (23, U)
    assert (contract["required_ids"], contract["scale_U"], len(contract["groups"])) == (59, U, 17)
    contract_by_id = {entry["group_id"]: entry["ids"] for entry in contract["groups"]}
    assert list(contract_by_id) == list(EXPECTED_GROUPS[:1]) + EXPECTED_MISSING_GROUPS[:5] + EXPECTED_MISSING_GROUPS[5:] + EXPECTED_GROUPS[1:]

    source_pins = {entry["path"]: entry["sha256"] for entry in manifest["sources"]}
    assert len(source_pins) == len(manifest["sources"]) == 10
    for relative, digest in source_pins.items():
        path = ROOT / relative
        assert path in PINS and PINS[path] == digest and sha(path) == digest

    groups = manifest["groups"]
    assert [entry["group_id"] for entry in groups] == EXPECTED_GROUPS
    assert all(entry["ids"] == contract_by_id[entry["group_id"]] for entry in groups)
    flat = [lineage for entry in groups for lineage in entry["ids"]]
    required = dag["required_reachable_lineage_ids_by_degree"]["23"]
    assert len(required) == len(set(required)) == 59
    assert len(flat) == len(set(flat)) == 42 and set(flat) <= set(required)
    assert [lineage for lineage in required if lineage not in set(flat)] == EXPECTED_MISSING_IDS

    hidden_source = load(HIDDEN / "k23_hidden_collected_singleton_fragment_manifest.json")["groups"]
    assert len(hidden_source) == 1
    assert groups[0] == hidden_source[0]

    k16_manifest = load(K16 / "k23_direct_k16_18_fragment_manifest.json")["groups"]
    k16_result = load(K16 / "results_k23_direct_k16_18.json")["groups"]
    normalized_k16 = {}
    for result_group in k16_result:
        matches = [entry for entry in k16_manifest if entry["ids"] == result_group["ids"]]
        assert len(matches) == 1
        normalized_k16[result_group["group_id"]] = source_shape(matches[0])
    assert set(normalized_k16) == set(EXPECTED_GROUPS[1:4])
    for entry in groups[1:4]:
        assert source_shape(entry) == normalized_k16[entry["group_id"]]

    direct_groups = load(DIRECT / "k23_manifest_direct23_23_of_59.json")["groups"]
    assert groups[4:] == direct_groups

    spec = importlib.util.spec_from_file_location("strict_k23_assembler", ASSEMBLER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    replay = module.assemble(manifest, allow_partial=True)
    assert replay == partial
    assert partial["status"] == "REJECT_INCOMPLETE_K23_59_ID_GATE"
    assert not partial["complete_K23_claim"]
    assert (partial["covered_paths"], partial["scalar_groups"], partial["required_paths"], partial["required_scalar_groups"]) == (42, 8, 59, 17)
    assert partial["missing_scalar_groups"] == EXPECTED_MISSING_GROUPS
    assert partial["missing_paths"] == EXPECTED_MISSING_IDS
    assert partial["duplicate_paths"] == partial["extra_paths"] == []

    group_once = sum(int(entry["full_scaled_U"]) for entry in groups)
    hostile_per_id = sum(int(entry["full_scaled_U"]) * len(entry["ids"]) for entry in groups)
    assert group_once == EXPECTED_SUBTOTAL and hostile_per_id != group_once
    assert int(partial["full_scaled_U"]) == int(partial["irreducible_scaled_U"]) == group_once
    exact = Fraction(group_once, U)
    assert Fraction(partial["full"]["text"]) == Fraction(partial["irreducible"]["text"]) == exact
    assert partial["full_equals_irreducible"]

    hostile = copy.deepcopy(manifest)
    hostile["groups"].append(copy.deepcopy(hostile["groups"][-1]))
    reject(module, hostile, "duplicate_group")
    hostile = copy.deepcopy(manifest)
    hostile["groups"][1]["ids"][0] = hostile["groups"][0]["ids"][0]
    reject(module, hostile, "partition/order")
    hostile = copy.deepcopy(manifest)
    hostile["groups"][0]["group_id"] = "hostile_extra"
    reject(module, hostile, "unknown_group")
    hostile = copy.deepcopy(manifest)
    hostile["groups"][0]["full"] = "0"
    reject(module, hostile, "scaled/rational")
    hostile = copy.deepcopy(manifest)
    hostile["groups"][0]["evidence_sha256"] = "0" * 64
    reject(module, hostile, "hash mismatch")

    payload = {
        "status": "PASS_INDEPENDENT_K23_42_OF_59_PARTIAL_INTEGRATION_REFEREE",
        "degree": 23,
        "coverage": {
            "required_ids": 59,
            "covered_ids": 42,
            "missing_ids": 17,
            "covered_scalar_groups": 8,
            "missing_scalar_groups": 9,
            "exact_gap_ids": EXPECTED_MISSING_IDS,
            "exact_gap_groups": EXPECTED_MISSING_GROUPS,
            "duplicates": [],
            "extras": [],
        },
        "arithmetic": {
            "scale_U": U,
            "subtotal_scaled_U": str(group_once),
            "subtotal": str(exact),
            "full_equals_irreducible": True,
            "group_scalar_once": True,
            "hostile_per_id_multiplication_rejected": True,
        },
        "source_referee": {
            "all_source_hashes_replayed": True,
            "source_pin_count": len(PINS),
            "manifest_source_pin_count": len(source_pins),
            "hidden_fragment_exact": True,
            "direct23_fragment_exact": True,
            "direct_k16_label_normalization": "group_id recovered uniquely from sealed results_k23_direct_k16_18.json by exact IDs; all other fields byte-for-byte equal to the unlabeled sealed fragment entry",
        },
        "strict_assembler": {
            "path": str(ASSEMBLER.relative_to(ROOT)),
            "sha256": sha(ASSEMBLER),
            "partial_replay_exact": True,
            "hostile_duplicate_regroup_extra_rational_hash_rejected": True,
        },
        "artifacts": {
            "manifest_path": str(MANIFEST.relative_to(ROOT)),
            "manifest_sha256": sha(MANIFEST),
            "partial_path": str(PARTIAL.relative_to(ROOT)),
            "partial_sha256": sha(PARTIAL),
            "dag_sha256": sha(DAG),
            "dag_logical_sha256": dag["logical_sha256"],
        },
        "scope": "read-only integration/referee of three sealed K23 fragments; no recurrence charge computation, no new K23 IDs, no K24, and no complete K23 claim",
    }
    logical = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    payload["logical_sha256"] = logical
    output = HERE / "results_k23_42_of_59_integration_audit.json"
    temporary = Path(str(output) + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps({"status": payload["status"], "subtotal": str(exact), "logical_sha256": logical}, indent=2))


if __name__ == "__main__":
    main()
