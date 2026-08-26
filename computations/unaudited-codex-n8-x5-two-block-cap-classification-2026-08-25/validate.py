#!/usr/bin/env python3
"""Fail-closed validator for the 34-support active-cap classification."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-single-offfamily-block-2026-08-25/MANIFEST.sha256"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-single-offfamily-block-2026-08-25/results_single_offfamily_block.json"
PARENT_SHA256 = "73a0b8e1e9e3934ce74f77506b85748c8f147219fecb53992ca122b44fb7a3bb"
PARENT_RESULT_SHA256 = "fe69a5e1854bf5aafdccd8c7a369c7da103fc220fed1c7a332500b990fbea2a2"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
    assert result["status"] == "PASS_ALL_34_TWO_BLOCK_SUPPORTS_HAVE_COEFFICIENT_INDEPENDENT_ACTIVE_CAP"
    assert evidence["status"] == "ALL_34_SUPPORTS_HAVE_COEFFICIENT_INDEPENDENT_ACTIVE_CLEAN_CAP"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    assert result["parent_result_sha256"] == evidence["parent_result_sha256"] == PARENT_RESULT_SHA256
    symmetry = result["exact_guard_symmetry"]
    assert symmetry["order"] == 2
    assert symmetry["generator"] == "(1 2)(6 7)"
    assert symmetry["support_orbits"] == 18
    assert symmetry["singleton_orbits"] == 2 and symmetry["doubleton_orbits"] == 16
    orbits = result["orbit_classification"]
    assert len(orbits) == 18
    assert [record["orbit_id"] for record in orbits] == list(range(18))
    members = [tuple(member) for record in orbits for member in record["members"]]
    assert len(members) == len(set(members)) == 34
    assert sum(record["orbit_size"] for record in orbits) == 34
    assert all(record["six_residual_formula"].startswith("P_a*Q_b + ") for record in orbits)
    assert all(record["new_matchings"] for record in orbits)
    for record in orbits:
        cap = record["cap_certificate"]
        assert cap["forbidden_response_matrix_rank"] == 0
        assert cap["kernel_dimension"] == 9
        assert cap["K"] == "I3"
        assert cap["kappa"] == [1, 1, 1]
        assert cap["s_pairing"] == 3
        assert record["common_zero_implication"].startswith("active clean cap")
    supports = result["all_34_support_cap_certificates"]
    assert len(supports) == 34
    assert all(cap["forbidden_response_matrix_rank"] == 0 and cap["s_pairing"] == 3
               for cap in supports.values())
    theorem = result["theorem"]
    assert theorem["common_zero_of_six_residuals_required"] is False
    assert theorem["common_zero_implication"] is True
    assert theorem["coefficient_field"] == "characteristic zero"
    direct = result["direct_A01_A23"]
    assert direct["residual_formula"] == "R_ab=P_a*Q_b+A01[a,b]*A23[b,a]*V[b,b]"
    assert direct["universal_active_cap"] == {
        "cap": "16", "triangle": "027", "possible_response_edges": ["07", "27"],
        "forbidden_response_matrix_rank": 0, "kernel_dimension": 9,
        "K": "I3", "kappa": [1, 1, 1], "s_pairing": 3,
    }
    replay = result["literal_replay"]
    assert replay["orbit_representatives"] == 18
    assert replay["residual_colour_cases"] == 108
    assert replay["all_cap_certificates_replayed"] is True
    assert result["scope"]["all_34_two_block_supports"] is True
    assert result["scope"]["smallest_surviving_inactive_common_zero_family"] is None
    assert result["scope"]["three_or_more_added_blocks_classified"] is False
    assert result["scope"]["full_support_dichotomy"] is False
    assert result["scope"]["full_conjecture_claim"] is False
    assert evidence["scope"]["inactive_common_zero_family_in_two_block_layer"] is False
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
    result = json.loads((HERE / "results_two_block_cap_classification.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r, e: r["exact_guard_symmetry"].update(order=1),
        lambda r, e: r["exact_guard_symmetry"].update(support_orbits=17),
        lambda r, e: r["orbit_classification"].pop(),
        lambda r, e: r["orbit_classification"][0].update(six_residual_formula="0"),
        lambda r, e: r["orbit_classification"][0]["cap_certificate"].update(forbidden_response_matrix_rank=1),
        lambda r, e: r["orbit_classification"][0]["cap_certificate"].update(s_pairing=0),
        lambda r, e: r["all_34_support_cap_certificates"].pop(next(iter(r["all_34_support_cap_certificates"]))),
        lambda r, e: r["theorem"].update(common_zero_implication=False),
        lambda r, e: r["direct_A01_A23"]["universal_active_cap"].update(triangle="026"),
        lambda r, e: r["literal_replay"].update(residual_colour_cases=107),
        lambda r, e: r["scope"].update(three_or_more_added_blocks_classified=True),
        lambda r, e: e["scope"].update(full_support_dichotomy=True),
        lambda r, e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_TWO_BLOCK_CAP_CLASSIFICATION_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "all 34 source-changing two-block supports in 18 exact guard orbits",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
