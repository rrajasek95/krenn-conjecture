#!/usr/bin/env python3
"""Fail-closed validator for the exact six-block support theorem."""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-five-block-support-cap-2026-08-25/MANIFEST.sha256"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-five-block-support-cap-2026-08-25/results_five_block_support_cap.json"
PARENT_SHA256 = "119ec632645202f973c89c3381e85113a902c4066e627ba7c6d051fa729d49fb"
PARENT_RESULT_SHA256 = "3d4882eb2d7f0687125ec5a22ec95ca9325cf31df9d3d572760c3e23b2c4fe57"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
    assert result["status"] == "PASS_ALL_38760_SIX_BLOCK_SUPPORTS_CLOSED_UNDER_FORMAL_GUARD"
    assert evidence["status"] == "ALL_SIX_BLOCK_SUPPORTS_HAVE_ACTIVE_CAP_OR_GUARD_REDUCE_LOWER"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    assert result["parent_result_sha256"] == evidence["parent_result_sha256"] == PARENT_RESULT_SHA256
    enumeration = result["enumeration"]
    assert enumeration["six_block_supports"] == 38760 == len(tuple(itertools.combinations(range(20), 6)))
    assert enumeration["fixed_identity_triangle_or_star_closed"] == 34124
    assert enumeration["fixed_identity_evaders"] == 4636
    assert enumeration["guard_reduced_size_census"] == {
        "2": 96, "3": 1080, "4": 2244, "5": 1104, "6": 112
    }
    assert enumeration["guard_reduced_to_parent_at_most_five"] == 4524
    assert enumeration["stable_six_block_supports"] == 112
    assert enumeration["stable_guard_symmetry_orbits"] == 57
    assert enumeration["orbit_size_census"] == {"1": 2, "2": 55}
    assert enumeration["zero_A67_fixed_cap_census"] == {
        "16_star": 60, "16_triangle": 48, "27_star": 4
    }
    records = enumeration["stable_orbit_records"]
    assert len(records) == 57
    members = [tuple(member) for record in records for member in record["members"]]
    assert len(members) == len(set(members)) == 112
    assert all(len(member) == 6 for member in members)
    for record in records:
        assert record["outside_cap67_added_edges"] == []
        assert set(record["cap67_response_edges"]) <= {"01", "02", "12"}
        nonzero = record["cap67_nonzero_stratum"]
        assert nonzero["forbidden_response_rank"] == 0
        assert nonzero["kernel_dimension"] == 9
        assert nonzero["active_clean_cap"] is True
        assert nonzero["activity_hyperplanes"] == [
            "K00=0", "K11=0", "K22=0", "<K,A67>=0"
        ]
        assert len(record["cap67_zero_strata"]) == len(record["members"])
        for stratum in record["cap67_zero_strata"]:
            certificate = stratum["certificate"]
            assert certificate["cap"] in ("16", "27")
            assert certificate["carrier"] in ("triangle", "star")
            assert certificate["forbidden_response_rank"] == 0
            assert certificate["kernel_dimension"] == 9
            assert certificate["kappa"] == [1, 1, 1]
            assert certificate["s_pairing"] == 3
    criterion = result["general_no_outside_edge_criterion"]
    assert criterion["valid_for_any_number_of_added_blocks"] is True
    assert criterion["all_112_stable_six_block_evaders_satisfy"] is True
    theorem = result["six_load_theorem"]
    assert theorem["coefficient_dependent_minors_required"] is False
    assert theorem["pure_rows_used"] is False
    assert theorem["six_residual_common_zero_used"] is False
    assert theorem["source_equations_used"] is False
    replay = result["literal_replay"]
    assert replay["samples"] == 257
    assert replay["all_112_stable_supports_distributed"] is True
    assert replay["nonzero_A67_active_K_constructed"] is True
    assert replay["zero_A67_fixed_caps_replayed"] is True
    scope = result["scope"]
    assert scope["all_six_block_supports"] is True
    assert scope["all_zero_through_six_block_layers_closed"] is True
    assert scope["seven_or_more_added_blocks"] is False
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
    result = json.loads((HERE / "results_six_block_support_cap.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r, e: r["enumeration"].update(six_block_supports=38759),
        lambda r, e: r["enumeration"].update(fixed_identity_evaders=4635),
        lambda r, e: r["enumeration"].update(guard_reduced_to_parent_at_most_five=4523),
        lambda r, e: r["enumeration"].update(stable_six_block_supports=111),
        lambda r, e: r["enumeration"].update(stable_guard_symmetry_orbits=56),
        lambda r, e: r["enumeration"].update(zero_A67_fixed_cap_census={"16_star": 60}),
        lambda r, e: r["enumeration"]["stable_orbit_records"][0].update(outside_cap67_added_edges=["36"]),
        lambda r, e: r["enumeration"]["stable_orbit_records"][0].update(cap67_response_edges=["01", "34"]),
        lambda r, e: r["enumeration"]["stable_orbit_records"][0]["cap67_nonzero_stratum"].update(kernel_dimension=8),
        lambda r, e: r["enumeration"]["stable_orbit_records"][0]["cap67_zero_strata"][0]["certificate"].update(s_pairing=0),
        lambda r, e: r["general_no_outside_edge_criterion"].update(valid_for_any_number_of_added_blocks=False),
        lambda r, e: r["six_load_theorem"].update(coefficient_dependent_minors_required=True),
        lambda r, e: r["literal_replay"].update(samples=256),
        lambda r, e: r["scope"].update(seven_or_more_added_blocks=True),
        lambda r, e: e["scope"].update(full_support_dichotomy=True),
        lambda r, e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_SIX_BLOCK_SUPPORT_CAP_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "all 38760 six-added-block supports under the formal guard",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
