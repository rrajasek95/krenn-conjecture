#!/usr/bin/env python3
"""Fail-closed validator for the exact seven-block structural boundary."""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-six-block-support-cap-2026-08-25/MANIFEST.sha256"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-six-block-support-cap-2026-08-25/results_six_block_support_cap.json"
PARENT_SHA256 = "fcfc7f972dfb0ed6c7d9cffdc6e2ce552ebad68ae1bc0af121df1455029327b7"
PARENT_RESULT_SHA256 = "fe1af0a5d935aa58a9727ba0b04c331e366b5c5c2b28979733188f175baa398d"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
    assert result["status"] == "PASS_EXACT_SEVEN_BLOCK_CLASSIFICATION_WITH_64_FIRST_STRUCTURAL_EVADER_STRATA"
    assert evidence["status"] == "SEVEN_BLOCK_CLASSIFIED_64_STRUCTURAL_STRATA_REMAIN"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    assert result["parent_result_sha256"] == evidence["parent_result_sha256"] == PARENT_RESULT_SHA256
    enumeration = result["enumeration"]
    assert enumeration["seven_block_supports"] == 77520 == len(tuple(itertools.combinations(range(20), 7)))
    assert enumeration["fixed_identity_triangle_or_star_closed"] == 56240
    assert enumeration["fixed_identity_evaders"] == 21280
    assert enumeration["guard_reduced_size_census"] == {
        "2": 54, "3": 1430, "4": 6454, "5": 8926, "6": 3926, "7": 490
    }
    assert enumeration["guard_reduced_to_parent_at_most_six"] == 20790
    assert enumeration["stable_seven_block_supports"] == 490
    assert enumeration["stable_guard_symmetry_orbits"] == 251
    assert enumeration["stable_orbit_size_census"] == {"1": 12, "2": 239}
    strata = result["exact_variable_stratum_classification"]
    assert strata["strata"] == 7840 == 490 * 16
    assert strata["census"] == {
        "fixed_identity_cap": 6895,
        "nonidentity_cap_hyperplane_avoidance": 881,
        "unresolved_response_minor_locus": 64,
    }
    assert strata["closed_strata"] == 7776
    assert strata["unresolved_structural_strata"] == 64
    assert strata["unresolved_added_supports"] == 20
    assert strata["unresolved_guard_symmetry_orbits"] == 32
    assert strata["unresolved_variable_subset_census"] == {
        "04,12,35": 20,
        "04,12,35,67": 12,
        "04,35": 20,
        "04,35,67": 12,
    }
    assert strata["full_family_nonzero_unresolved_supports"] == 12
    assert strata["full_family_nonzero_unresolved_orbits"] == 6
    orbit_records = strata["unresolved_orbit_records"]
    assert len(orbit_records) == 32
    members = [member for orbit in orbit_records for member in orbit["members"]]
    assert len(members) == 64
    member_keys = {
        (tuple(member["added"]), tuple(member["nonzero_variable_blocks"]))
        for member in members
    }
    assert len(member_keys) == 64
    assert all(member["all_supported_carriers_fail_triangle_star"] is True for member in members)
    assert all(len(member["added"]) == 7 for member in members)
    assert all(member["nonzero_variable_blocks"] in (
        ["04", "35"], ["04", "12", "35"],
        ["04", "35", "67"], ["04", "12", "35", "67"]
    ) for member in members)
    lemmas = result["general_lemmas"]
    assert "stops at seven" in lemmas["induction_verdict"]
    assert "A17 and A26" in lemmas["switched_rectangle"]
    replay = result["literal_replay"]
    assert replay["samples"] == 257
    assert replay["closed_nonidentity_strata_distributed"] is True
    assert replay["active_K_constructed"] is True
    assert replay["forbidden_responses_replayed"] is True
    scope = result["scope"]
    assert scope["all_seven_block_supports_classified"] is True
    assert scope["all_seven_block_strata_closed"] is False
    assert scope["closed_seven_block_stable_strata"] == 7776
    assert scope["unresolved_seven_block_structural_strata"] == 64
    assert scope["first_full_family_structural_evader_supports"] == 12
    assert scope["zero_through_six_layers_closed"] is True
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
    result = json.loads((HERE / "results_seven_block_support_boundary.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r, e: r["enumeration"].update(seven_block_supports=77519),
        lambda r, e: r["enumeration"].update(fixed_identity_evaders=21279),
        lambda r, e: r["enumeration"].update(guard_reduced_to_parent_at_most_six=20789),
        lambda r, e: r["enumeration"].update(stable_seven_block_supports=489),
        lambda r, e: r["enumeration"].update(stable_guard_symmetry_orbits=250),
        lambda r, e: r["exact_variable_stratum_classification"].update(strata=7839),
        lambda r, e: r["exact_variable_stratum_classification"]["census"].update(unresolved_response_minor_locus=63),
        lambda r, e: r["exact_variable_stratum_classification"].update(closed_strata=7777),
        lambda r, e: r["exact_variable_stratum_classification"].update(unresolved_added_supports=19),
        lambda r, e: r["exact_variable_stratum_classification"].update(full_family_nonzero_unresolved_supports=11),
        lambda r, e: r["exact_variable_stratum_classification"]["unresolved_orbit_records"][0]["members"][0].update(all_supported_carriers_fail_triangle_star=False),
        lambda r, e: r["general_lemmas"].update(induction_verdict="closes all seven"),
        lambda r, e: r["literal_replay"].update(samples=256),
        lambda r, e: r["scope"].update(all_seven_block_strata_closed=True),
        lambda r, e: e["scope"].update(full_support_dichotomy=True),
        lambda r, e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_SEVEN_BLOCK_SUPPORT_BOUNDARY_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "complete seven-block structural classification; 64 unresolved exact strata",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
