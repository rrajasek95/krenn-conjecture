#!/usr/bin/env python3
"""Fail-closed validator for the four-block formal-guard collapse."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-three-block-support-cap-2026-08-25/MANIFEST.sha256"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-three-block-support-cap-2026-08-25/results_three_block_support_cap.json"
PARENT_SHA256 = "34511eaf230805dec2c75a7babc3d6a3ff4c42b63e178adec298417a3e8f998e"
PARENT_RESULT_SHA256 = "1eefe005739b12321e1d5871c5c11c2fa16b21b6555e426e71b031e04734b193"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
    assert result["status"] == "PASS_ALL_24_STRUCTURAL_EVADERS_FORCED_TO_CLOSED_LOWER_SUPPORT"
    assert evidence["status"] == "ALL_24_STRUCTURAL_EVADERS_COLLAPSE_TO_CLOSED_LOWER_SUPPORT"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    assert result["parent_result_sha256"] == evidence["parent_result_sha256"] == PARENT_RESULT_SHA256
    assert result["formal_guard"] == {
        "cap": "67", "triangle": "012", "K": "I3",
        "forbidden_pairs": ["03", "04", "05", "13", "14", "15", "23", "24", "25", "34", "35", "45"],
    }
    lemma = result["guard_injection_lemma"]
    assert lemma["outside_cap_adjacent_blocks"] == ["36", "37", "46", "47", "56", "57"]
    assert lemma["coordinate_rank"] == 9
    assert lemma["unit_minor_determinant_abs"] == 1
    classification = result["orbit_classification"]
    assert classification["orbits"] == len(classification["records"]) == 12
    assert classification["supports"] == len(classification["support_records"]) == 24
    assert classification["representative_reduced_size_census"] == {"2": 6, "3": 6}
    assert classification["four_block_nonzero_guard_strata"] == 0
    members = [tuple(member) for record in classification["records"] for member in record["members"]]
    assert len(members) == len(set(members)) == 24
    for record in classification["records"]:
        assert len(record["forced_zero_blocks"]) in (1, 2)
        assert len(record["guard_injections"]) == len(record["forced_zero_blocks"])
        assert all(item["coordinate_map_rank"] == 9 and item["unit_minor_determinant_abs"] == 1
                   and len(item["basis_mapping"]) == 9 for item in record["guard_injections"])
        assert len(record["reduced_support"]) in (2, 3)
        assert record["inherited_active_cap"]["forbidden_response_rank"] == 0
        assert record["inherited_active_cap"]["kappa"] == [1, 1, 1]
        assert record["inherited_active_cap"]["s_pairing"] == 3
        assert record["formal_guard_stratum_nonempty_with_all_four_blocks_nonzero"] is False
    assert sum(record["reduced_size"] == 2 for record in classification["support_records"]) == 12
    assert sum(record["reduced_size"] == 3 for record in classification["support_records"]) == 12
    theorem = result["theorem"]
    assert theorem["pure_rows_used"] is False
    assert theorem["six_residual_common_zero_used"] is False
    assert theorem["source_equations_used"] is False
    assert theorem["inactive_parameter_locus"].startswith("empty")
    replay = result["literal_replay"]
    assert replay["samples"] == 257
    assert replay["all_24_supports_distributed"] is True
    assert replay["injection_before_guard"] is True
    assert replay["all_outside_cap67_responses_zero_after_guard"] is True
    assert replay["inherited_active_caps_replayed"] is True
    assert result["scope"]["all_24_first_four_block_structural_evaders"] is True
    assert result["scope"]["all_four_block_supports_closed"] is True
    assert result["scope"]["five_or_more_added_blocks"] is False
    assert result["scope"]["full_support_dichotomy"] is False
    assert result["scope"]["full_conjecture_claim"] is False
    assert evidence["scope"]["five_or_more_added_blocks"] is False
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
    result = json.loads((HERE / "results_four_block_guard_collapse.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r, e: r["formal_guard"].update(K="E00"),
        lambda r, e: r["guard_injection_lemma"].update(coordinate_rank=8),
        lambda r, e: r["guard_injection_lemma"].update(unit_minor_determinant_abs=0),
        lambda r, e: r["orbit_classification"].update(orbits=11),
        lambda r, e: r["orbit_classification"].update(supports=23),
        lambda r, e: r["orbit_classification"].update(four_block_nonzero_guard_strata=1),
        lambda r, e: r["orbit_classification"]["records"][0]["guard_injections"][0].update(coordinate_map_rank=8),
        lambda r, e: r["orbit_classification"]["records"][0]["inherited_active_cap"].update(s_pairing=0),
        lambda r, e: r["theorem"].update(pure_rows_used=True),
        lambda r, e: r["literal_replay"].update(samples=256),
        lambda r, e: r["scope"].update(five_or_more_added_blocks=True),
        lambda r, e: e["scope"].update(full_support_dichotomy=True),
        lambda r, e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_FOUR_BLOCK_GUARD_COLLAPSE_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "all 24 four-block fixed-carrier evaders and hence all four-block supports",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
