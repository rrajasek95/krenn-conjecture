#!/usr/bin/env python3
"""Fail-closed validator for the three-block fixed-cap theorem."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-two-block-cap-classification-2026-08-25/MANIFEST.sha256"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-two-block-cap-classification-2026-08-25/results_two_block_cap_classification.json"
PARENT_SHA256 = "139a5270a384a36d6a1b3312dd6e1a0efba0cafe76912a179c973039e1464297"
PARENT_RESULT_SHA256 = "87bdde155fbded9f39821b6023fe1d2939ec27a101f671d5bd9e289003e4ccb0"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
    assert result["status"] == "PASS_ALL_1140_THREE_BLOCK_SUPPORTS_HAVE_FIXED_IDENTITY_ACTIVE_CAP"
    assert evidence["status"] == "ALL_1140_THREE_BLOCK_SUPPORTS_HAVE_FIXED_IDENTITY_ACTIVE_CAP"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    assert result["parent_result_sha256"] == evidence["parent_result_sha256"] == PARENT_RESULT_SHA256
    theorem = result["graph_theorem"]
    assert theorem["fixed_identity_caps"] == ["03", "16", "27", "45"]
    assert theorem["coefficient_field"] == "characteristic zero"
    assert theorem["same_source"] is True
    three = result["three_block_classification"]
    assert three["supports"] == 1140
    assert three["exact_guard_symmetry"] == {"order": 2, "generator": "(1 2)(6 7)"}
    assert three["orbits"] == len(three["orbit_records"]) == 579
    assert three["singleton_orbits"] == 18 and three["doubleton_orbits"] == 561
    assert three["fixed_cap_triangle_evaders"] == 0
    assert sum(three["certificate_cap_census"].values()) == 1140
    members = [tuple(member) for orbit in three["orbit_records"] for member in orbit["members"]]
    assert len(members) == len(set(members)) == 1140
    assert all(orbit["representative_certificate"]["forbidden_response_rank"] == 0
               and orbit["representative_certificate"]["kernel_dimension"] == 9
               and orbit["representative_certificate"]["kappa"] == [1, 1, 1]
               and orbit["representative_certificate"]["s_pairing"] == 3
               for orbit in three["orbit_records"])
    replay = result["literal_replay"]
    assert replay["dense_rational_samples"] == 257
    assert replay["forbidden_responses_zero"] is True
    boundary = result["sharp_four_block_boundary_diagnostic"]
    assert boundary["supports"] == 4845
    assert boundary["fixed_triangle_certificate_evaders"] == 264
    assert boundary["fixed_triangle_or_star_certificate_evaders"] == 24
    assert boundary["exact_guard_orbits_of_fixed_carrier_evaders"] == len(boundary["orbit_records"]) == 12
    assert boundary["coefficient_conditions_solved"] is False
    boundary_members = [tuple(member) for orbit in boundary["orbit_records"] for member in orbit["members"]]
    assert len(boundary_members) == len(set(boundary_members)) == 24
    assert all(set(orbit["fixed_cap_response_graphs"]) == {"03", "16", "27", "45"}
               for orbit in boundary["orbit_records"])
    assert result["scope"]["all_zero_one_two_three_block_layers_closed"] is True
    assert result["scope"]["three_block_inactive_common_zero_family"] is None
    assert result["scope"]["four_block_coefficient_classification"] is False
    assert result["scope"]["full_support_dichotomy"] is False
    assert result["scope"]["full_conjecture_claim"] is False
    assert evidence["scope"]["four_block_coefficients_solved"] is False
    assert evidence["scope"]["full_support_dichotomy"] is False
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
    result = json.loads((HERE / "results_three_block_support_cap.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r, e: r["graph_theorem"].update(coefficient_field="characteristic three"),
        lambda r, e: r["three_block_classification"].update(supports=1139),
        lambda r, e: r["three_block_classification"].update(orbits=578),
        lambda r, e: r["three_block_classification"].update(fixed_cap_triangle_evaders=1),
        lambda r, e: r["three_block_classification"]["orbit_records"].pop(),
        lambda r, e: r["three_block_classification"]["orbit_records"][0]["representative_certificate"].update(s_pairing=0),
        lambda r, e: r["literal_replay"].update(dense_rational_samples=256),
        lambda r, e: r["sharp_four_block_boundary_diagnostic"].update(fixed_triangle_certificate_evaders=263),
        lambda r, e: r["sharp_four_block_boundary_diagnostic"].update(fixed_triangle_or_star_certificate_evaders=23),
        lambda r, e: r["sharp_four_block_boundary_diagnostic"].update(coefficient_conditions_solved=True),
        lambda r, e: r["scope"].update(four_block_coefficient_classification=True),
        lambda r, e: e["scope"].update(full_support_dichotomy=True),
        lambda r, e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_THREE_BLOCK_SUPPORT_CAP_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "all 1,140 three-block supports; first fixed-carrier boundary at four blocks",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
