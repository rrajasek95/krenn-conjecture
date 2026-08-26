#!/usr/bin/env python3
"""Fail-closed validator for the canonical triangle-inactive guard witness."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25/MANIFEST.sha256"
REFEREE = HERE.parent / "unaudited-codex-n8-x5-support-induction-boundary-referee-2026-08-25/FINAL_MANIFEST.sha256"
PARENT_SHA256 = "13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85"
REFEREE_SHA256 = "583bea191a1be0adb8d197270c22f9dd7b7ba0494b9d1f95b963213a19f23f61"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert sha256(REFEREE) == REFEREE_SHA256
    assert result["status"] == "PASS_TRIANGLE_INACTIVE_GUARD_WITNESS_STAR_ROUTE_SURVIVES_AND_FULL_X5_FAILS"
    assert evidence["status"] == "EXACT_TRIANGLE_INACTIVE_GUARD_POINT_WITH_TWO_ACTIVE_STARS"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    assert result["referee_manifest_sha256"] == evidence["referee_manifest_sha256"] == REFEREE_SHA256
    support = result["support"]
    assert support["added"] == ["06", "13", "17", "24", "26", "56", "57"]
    assert support["nonzero_variable_blocks"] == ["04", "12", "35", "67"]
    assert support["fixed_identity_blocks"] == ["03", "16", "27", "45"]
    assert support["all_15_blocks_nonzero"] is True
    assert len(result["source"]["matrix_units"]) == 11
    assert all(item["coefficient"] in (-1, 1) for item in result["source"]["matrix_units"].values())
    guard = result["formal_guard"]
    assert guard["cap"] == "67" and guard["triangle"] == "012" and guard["K"] == "I3"
    assert guard["outside_equations"] == len(guard["outside_response_equations"]) == 12
    assert guard["nontrivial_direct_switched_cancellations"] == 2
    assert guard["all_zero"] is True
    assert all(all(value == "0" for row in record["sum"] for value in row)
               for record in guard["outside_response_equations"])
    activity = result["activity_census"]
    assert activity["triangle_carriers"] == 560
    assert activity["active_triangle_carriers"] == 0
    assert sum(activity["triangle_response_rank_census"].values()) == 560
    assert activity["triangle_response_rank_census"] == {
        "2": 25, "3": 21, "4": 24, "5": 55,
        "6": 8, "7": 29, "8": 10, "9": 388,
    }
    assert activity["star_carriers_supplementary"] == 168
    assert activity["active_star_carriers"] == 2
    assert sum(activity["star_response_rank_census"].values()) == 168
    assert [(record["cap"], record["defining_sites"], record["response_rank"], record["kernel_dimension"])
            for record in activity["active_star_records"]] == [
        ("16", [2], 2, 7), ("45", [2], 1, 8)
    ]
    assert all(all(record["activity_live"].values()) for record in activity["active_star_records"])
    assert activity["exact_rational_rank_and_activity_replay"] is True
    full = result["full_X5_test"]
    assert full["pure_amplitudes"] == [1, 1, 1]
    assert full["pure_normalization_pass"] is True
    assert [record["amplitude"] for record in full["six_residuals"]] == [1, 1, 1, 1, 1, 2]
    assert full["six_residual_common_zero"] is False
    assert full["first_false_equation"]["word"] == "01100011"
    assert full["first_false_equation"]["amplitude"] == 1
    assert full["nonzero_mixed_amplitudes"] == 114
    assert full["is_full_X5_point"] is False
    theorem = result["theorem_verdict"]
    assert theorem["guard_plus_pure_forces_block_zero_or_active_triangle"] is False
    assert theorem["guard_plus_pure_forces_block_zero_or_active_triangle_or_star"].startswith("NOT_REFUTED")
    assert theorem["guard_plus_full_X5_forces_block_zero_or_active_cap"].startswith("OPEN")
    assert theorem["referee_complete_switched_rectangle_lemma"].startswith("NOT_REFUTED")
    scope = result["scope"]
    assert scope["exact_canonical_stuck_support"] is True
    assert scope["all_560_triangle_carriers"] is True
    assert scope["all_168_star_carriers_supplementary"] is True
    assert scope["formal_guard"] is True
    assert scope["pure_normalization"] is True
    assert scope["full_X5"] is False
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
    result = json.loads((HERE / "results_inactive_guard_witness.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r, e: r["support"].update(added=["06"]),
        lambda r, e: r["support"].update(all_15_blocks_nonzero=False),
        lambda r, e: r["source"]["matrix_units"]["04"].update(coefficient=0),
        lambda r, e: r["formal_guard"].update(outside_equations=11),
        lambda r, e: r["formal_guard"].update(nontrivial_direct_switched_cancellations=1),
        lambda r, e: r["formal_guard"].update(all_zero=False),
        lambda r, e: r["activity_census"].update(triangle_carriers=559),
        lambda r, e: r["activity_census"].update(active_triangle_carriers=1),
        lambda r, e: r["activity_census"].update(star_carriers_supplementary=167),
        lambda r, e: r["activity_census"].update(active_star_carriers=0),
        lambda r, e: r["activity_census"]["active_star_records"][0].update(response_rank=9),
        lambda r, e: r["full_X5_test"].update(pure_amplitudes=[1, 1, 0]),
        lambda r, e: r["full_X5_test"].update(six_residual_common_zero=True),
        lambda r, e: r["full_X5_test"].update(nonzero_mixed_amplitudes=0),
        lambda r, e: r["theorem_verdict"].update(guard_plus_pure_forces_block_zero_or_active_triangle=True),
        lambda r, e: r["scope"].update(full_X5=True),
        lambda r, e: e["scope"].update(full_conjecture_claim=True),
        lambda r, e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_SEVEN_BLOCK_TRIANGLE_INACTIVE_GUARD_WITNESS_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "exact canonical guard+pure point; 560 triangles inactive, two stars active, not X5",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
