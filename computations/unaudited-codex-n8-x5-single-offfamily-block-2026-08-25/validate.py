#!/usr/bin/env python3
"""Fail-closed validator for the single off-family block classification."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-cycle-polynomial-ideal-2026-08-25/MANIFEST.sha256"
CORE = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25/audit_two_cell_dichotomy.py"
PARENT_SHA256 = "8ab337cde3b98f68909c642b655ceeb386abed3a81d692d53bec294547ecd107"
CORE_SHA256 = "f8305d4b514ac6dc0a2b28b359dbca62929667248596beee48804eb43109e876"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert sha256(CORE) == CORE_SHA256
    assert result["status"] == "PASS_ALL_SINGLE_BLOCK_ESCAPES_SOURCE_EQUIVALENT_OR_GUARD_ZERO"
    assert evidence["status"] == "ALL_SINGLE_BLOCK_ESCAPES_SOURCE_EQUIVALENT_OR_GUARD_ZERO"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    support = result["support_graph"]
    assert support["off_family_edges"] == len(support["single_block_records"]) == 20
    assert len({record["edge"] for record in support["single_block_records"]}) == 20
    assert all(record["perfect_matchings_using_new_block"] == 0 for record in support["single_block_records"])
    assert all(record["all_amplitude_polynomials_unchanged"] is True for record in support["single_block_records"])
    assert sum(record["support_type"] == "square_chord" for record in support["single_block_records"]) == 4
    assert sum(record["support_type"] == "cross_square_bridge" for record in support["single_block_records"]) == 16
    cap = result["cap_67_response_classification"]
    assert len(cap["records"]) == 10
    forced = [record for record in cap["records"] if record["guard_verdict"].startswith("forced_zero")]
    allowed = [record for record in cap["records"] if record["guard_verdict"].startswith("allowed")]
    assert len(forced) == cap["outside_cap_adjacent_blocks_forced_zero"] == 6
    assert len(allowed) == cap["inside_cap_adjacent_blocks_allowed_but_matching_null"] == 4
    assert all(record["fixed_K_I_block_to_forbidden_response_rank"] == 9 for record in forced)
    assert all(record["cap_covector_to_forbidden_response_rank_for_block_ranks_0_1_2_3"] == [0, 3, 6, 9]
               for record in forced)
    assert all(record["fixed_K_I_block_to_forbidden_response_rank"] == 0 for record in allowed)
    layer = result["first_support_changing_layer"]
    assert layer["minimum_additional_site_blocks"] == 2
    assert layer["support_pairs"] == len(layer["records"]) == 34
    assert layer["two_chord_pairs"] == 2 and layer["two_bridge_pairs"] == 32
    assert sum(len(record["new_matchings"]) for record in layer["records"]) == 36
    assert layer["guard_and_coefficient_equations_classified"] is False
    direct = layer["smallest_residual_common_zero_boundary"]
    assert direct["new_blocks"] == ["B=A01", "C=A23"]
    assert direct["six_residuals"] == {key: 0 for key in ("R01", "R02", "R10", "R12", "R20", "R21")}
    assert direct["pure_rows"] == [1, 1, 1]
    assert direct["named_cap_67_guard_preserved"] is True
    assert direct["named_K_I_activity_s_trace_A67"] == 0
    assert direct["mixed_violations"] == 366
    assert direct["global_active_clean_cap_census_for_this_rational_witness"] == 44
    assert direct["explicit_active_clean_cap"] == {
        "cap": "01", "triangle": "236", "K": "all-ones 3x3 matrix",
        "forbidden_responses": 0, "kappa": [1, 1, 1], "s_pairing_with_A01": 6,
    }
    replay = result["literal_replay"]
    assert replay["samples"] == 257
    assert replay["all_twenty_edges_distributed"] is True
    assert replay["six_residuals_unique_M0"] is True
    assert result["scope"]["all_single_additional_site_blocks_classified"] is True
    assert result["scope"]["two_block_coefficient_families_classified"] is False
    assert result["scope"]["full_guard_support_classification"] is False
    assert result["scope"]["full_conjecture_claim"] is False
    assert evidence["scope"]["global_support_dichotomy"] is False
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
    result = json.loads((HERE / "results_single_offfamily_block.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r, e: r["support_graph"].update(off_family_edges=19),
        lambda r, e: r["support_graph"]["single_block_records"][0].update(perfect_matchings_using_new_block=1),
        lambda r, e: r["cap_67_response_classification"].update(outside_cap_adjacent_blocks_forced_zero=5),
        lambda r, e: r["cap_67_response_classification"]["records"][4].update(fixed_K_I_block_to_forbidden_response_rank=8),
        lambda r, e: r["first_support_changing_layer"].update(minimum_additional_site_blocks=1),
        lambda r, e: r["first_support_changing_layer"].update(support_pairs=33),
        lambda r, e: r["first_support_changing_layer"]["smallest_residual_common_zero_boundary"]["six_residuals"].update(R01=1),
        lambda r, e: r["first_support_changing_layer"]["smallest_residual_common_zero_boundary"]["explicit_active_clean_cap"].update(forbidden_responses=1),
        lambda r, e: r["literal_replay"].update(samples=256),
        lambda r, e: r["scope"].update(two_block_coefficient_families_classified=True),
        lambda r, e: e["scope"].update(global_support_dichotomy=True),
        lambda r, e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_SINGLE_OFFFAMILY_BLOCK_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "all twenty one-block extensions; exact first two-block support boundary",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
