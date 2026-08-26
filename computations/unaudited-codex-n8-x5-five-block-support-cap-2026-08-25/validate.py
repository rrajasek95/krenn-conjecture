#!/usr/bin/env python3
"""Fail-closed validator for the exact five-block support theorem."""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-four-block-guard-collapse-2026-08-25/MANIFEST.sha256"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-four-block-guard-collapse-2026-08-25/results_four_block_guard_collapse.json"
PARENT_SHA256 = "a9ffc82d1b3bda811dfeffc33c61c1a0b277bea48a2265a583fd01ed714070c8"
PARENT_RESULT_SHA256 = "2ea44d104e37ec6e44793ebddb441af4df880d1335a4a9d52c49e07b50aa8cb6"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
    assert result["status"] == "PASS_ALL_15504_FIVE_BLOCK_SUPPORTS_CLOSED_UNDER_FORMAL_GUARD"
    assert evidence["status"] == "ALL_FIVE_BLOCK_SUPPORTS_HAVE_ACTIVE_CAP_OR_GUARD_REDUCE_LOWER"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    assert result["parent_result_sha256"] == evidence["parent_result_sha256"] == PARENT_RESULT_SHA256
    enumeration = result["enumeration"]
    assert enumeration["five_block_supports"] == 15504 == len(tuple(itertools.combinations(range(20), 5)))
    assert enumeration["fixed_identity_triangle_or_star_closed"] == 14976
    assert enumeration["fixed_identity_evaders"] == 528
    assert enumeration["guard_reduced_size_census"] == {"2": 60, "3": 287, "4": 170, "5": 11}
    assert enumeration["guard_reduced_to_parent_at_most_four"] == 517
    assert enumeration["stable_five_block_supports"] == 11
    assert enumeration["stable_guard_symmetry_orbits"] == 6
    records = enumeration["stable_orbit_records"]
    assert len(records) == 6
    assert sorted(len(record["members"]) for record in records) == [1, 2, 2, 2, 2, 2]
    members = [tuple(member) for record in records for member in record["members"]]
    assert len(members) == len(set(members)) == 11
    expected_representatives = [
        ["06", "07", "13", "14", "25"],
        ["06", "07", "13", "15", "24"],
        ["06", "07", "14", "25", "34"],
        ["06", "07", "15", "25", "34"],
        ["06", "14", "17", "23", "25"],
        ["06", "15", "17", "23", "24"],
    ]
    assert [record["representative"] for record in records] == expected_representatives
    for record in records:
        assert record["cap67_response_edges"] == ["01", "02", "12"]
        nonzero = record["cap67_nonzero_stratum"]
        assert nonzero["forbidden_response_rank"] == 0
        assert nonzero["kernel_dimension"] == 9
        assert nonzero["hyperplanes_proper_when_A67_nonzero"] is True
        assert nonzero["active_clean_cap"] is True
        assert nonzero["activity_hyperplanes"] == [
            "K00=0", "K11=0", "K22=0", "<K,A67>=0"
        ]
        zero = record["cap67_zero_stratum"]
        assert zero["cap"] == "16"
        assert zero["carrier"] in ("triangle", "star")
        assert zero["forbidden_response_rank"] == 0
        assert zero["kernel_dimension"] == 9
        assert zero["kappa"] == [1, 1, 1]
        assert zero["s_pairing"] == 3
    lemma = result["guard_reduction_lemma"]
    assert lemma["outside_blocks"] == ["36", "37", "46", "47", "56", "57"]
    assert lemma["coordinate_rank"] == 9
    assert lemma["unit_minor_determinant_abs"] == 1
    assert lemma["iterative_reduction_exact"] is True
    theorem = result["five_load_theorem"]
    assert theorem["coefficient_dependent_minors_required"] is False
    assert theorem["pure_rows_used"] is False
    assert theorem["six_residual_common_zero_used"] is False
    assert theorem["source_equations_used"] is False
    replay = result["literal_replay"]
    assert replay["samples"] == 257
    assert replay["all_11_stable_supports_distributed"] is True
    assert replay["nonzero_A67_active_K_constructed"] is True
    assert replay["zero_A67_fixed_cap_replayed"] is True
    scope = result["scope"]
    assert scope["all_five_block_supports"] is True
    assert scope["all_zero_through_five_block_layers_closed"] is True
    assert scope["six_or_more_added_blocks"] is False
    assert scope["full_support_dichotomy"] is False
    assert scope["full_conjecture_claim"] is False
    assert scope["broad_cegar"] is False
    assert scope["degree_twelve_read"] is False
    assert evidence["scope"] == scope
    return True


def must_reject(mutator, result, evidence):
    candidate_result = copy.deepcopy(result)
    candidate_evidence = copy.deepcopy(evidence)
    mutator(candidate_result, candidate_evidence)
    try:
        check(candidate_result, candidate_evidence)
    except (AssertionError, KeyError, TypeError):
        return True
    raise AssertionError("hostile mutation accepted")


def main():
    result = json.loads((HERE / "results_five_block_support_cap.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r, e: r["enumeration"].update(five_block_supports=15503),
        lambda r, e: r["enumeration"].update(fixed_identity_evaders=527),
        lambda r, e: r["enumeration"].update(guard_reduced_size_census={"2": 60, "3": 287, "4": 171, "5": 10}),
        lambda r, e: r["enumeration"].update(stable_five_block_supports=10),
        lambda r, e: r["enumeration"].update(stable_guard_symmetry_orbits=5),
        lambda r, e: r["enumeration"]["stable_orbit_records"][0].update(cap67_response_edges=["01", "02", "12", "34"]),
        lambda r, e: r["enumeration"]["stable_orbit_records"][0]["cap67_nonzero_stratum"].update(kernel_dimension=8),
        lambda r, e: r["enumeration"]["stable_orbit_records"][0]["cap67_zero_stratum"].update(s_pairing=0),
        lambda r, e: r["guard_reduction_lemma"].update(coordinate_rank=8),
        lambda r, e: r["five_load_theorem"].update(coefficient_dependent_minors_required=True),
        lambda r, e: r["literal_replay"].update(samples=256),
        lambda r, e: r["scope"].update(six_or_more_added_blocks=True),
        lambda r, e: e["scope"].update(full_support_dichotomy=True),
        lambda r, e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_FIVE_BLOCK_SUPPORT_CAP_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "all 15504 five-added-block supports under the formal guard",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
