#!/usr/bin/env python3
"""Fail-closed validation of the minimal two-cell X5 escape package."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-reciprocity-pure-row-guard-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "0c6c164e7c1e6a37a369dfe509ec4145ae8d610a80a17d8b6ff0bb0a98a6d65b"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert result["status"] == "PASS_ALL_MINIMAL_TWO_CELL_ESCAPES_FORCE_SECOND_X5_VIOLATION"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    classification = result["minimality_and_classification"]
    assert classification["all_two_new_cell_matchings"] == 15
    assert classification["diagonal_patterns_rejected_by_pure_normalization"] == 7
    assert classification["pure_preserving_two_cell_patterns"] == 8
    assert classification["source_class_counts"] == {
        "cap_star_four_cycle": 4,
        "direct_edge_six_cycle": 2,
        "residual_four_cycle": 2,
    }
    assert classification["formal_guard_preserving_patterns"] == 4
    assert len(classification["patterns"]) == 8
    assert all(item["forced_next_word"] == "00002200" for item in classification["patterns"])
    assert all(item["forced_next_amplitude"] == 1 for item in classification["patterns"])
    cap = [item for item in classification["patterns"] if item["source_class"] == "cap_star_four_cycle"]
    assert len(cap) == 4 and all(not item["formal_triangle_guard_preserved"] for item in cap)
    assert all(item["outside_response_count_for_K_I"] == 1 for item in cap)
    direct = [item for item in classification["patterns"] if item["source_class"] == "direct_edge_six_cycle"]
    assert len(direct) == 2 and all(item["remaining_mixed_violations"] == 81 for item in direct)
    boundary = result["boundary_69_violation_census"]
    assert boundary["cancelled_word_count"] == 9
    assert boundary["nonzero_mixed_count"] == 69
    assert boundary["profile_census"] == {"4+2+2": 31, "4+4": 16, "6+2": 22}
    assert boundary["word_symmetry_orbits"] == 45
    next_boundary = result["next_minimal_surviving_pattern"]
    assert next_boundary["minimal_new_cell_count_to_cancel_both_colour_words"] == 4
    assert next_boundary["remaining_mixed_violations"] == 78
    assert next_boundary["first_remaining"] == "00001200"
    assert next_boundary["normalized_X5"] is False
    assert result["scope"]["minimal_two_cell_dichotomy_proved"] is True
    assert result["scope"]["general_off_support_dichotomy_proved"] is False
    assert result["scope"]["full_conjecture_claim"] is False
    assert evidence["proved_lemma"]["identity"] == "Phi(00002200)=+1 from unique matching 03|16|27|45"
    assert evidence["scope"]["active_clean_cap_proved"] is False
    return True


def must_reject(mutator, result, evidence):
    hostile_result = copy.deepcopy(result)
    hostile_evidence = copy.deepcopy(evidence)
    mutator(hostile_result, hostile_evidence)
    try:
        check(hostile_result, hostile_evidence)
    except (AssertionError, KeyError, TypeError):
        return True
    raise AssertionError("hostile mutation was accepted")


def main():
    result = json.loads((HERE / "results_two_cell_dichotomy.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r, e: r["minimality_and_classification"].update(pure_preserving_two_cell_patterns=7),
        lambda r, e: r["minimality_and_classification"]["patterns"][0].update(forced_next_amplitude=0),
        lambda r, e: r["boundary_69_violation_census"].update(nonzero_mixed_count=68),
        lambda r, e: r["next_minimal_surviving_pattern"].update(remaining_mixed_violations=60),
        lambda r, e: r["scope"].update(general_off_support_dichotomy_proved=True),
        lambda r, e: e["scope"].update(active_clean_cap_proved=True),
        lambda r, e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_TWO_CELL_ESCAPE_DICHOTOMY_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "all eight minimal two-cell source-labelled escapes",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
