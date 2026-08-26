#!/usr/bin/env python3
"""Fail-closed small-file validator for the pure-row reciprocity guard."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PARENT = REPO / "computations/unaudited-codex-n8-x5-proof-side-synthesis-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "05e85e32252a31f55c85f6a8ec1e08e6aa2c02674dc98b523c6b99f56509cced"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert result["status"] == "PASS_PURE_ROWS_SURVIVE_ACTIVITY_GUARD_SUPPORT_FULL_X5_CONTRADICTED"
    assert result["parent_manifest_sha256"] == PARENT_SHA256
    minimal = result["minimal_pure_normalized_extension"]
    assert minimal["minimal_new_cell_count_within_frozen_physical_support"] == 4
    assert minimal["pure_amplitudes"] == [1, 1, 1]
    assert minimal["s_L"] == 0 and minimal["kappa_L"] == [1, 0, 0]
    assert minimal["cap_error"] == "zero because r is supported on one edge"
    assert minimal["mixed_violations"] == 78
    assert minimal["first_mixed_violation"] == {
        "amplitude": 1,
        "sole_matching": "03|16|27|45",
        "word": "00001100",
    }
    guard = result["first_off_support_cancellation_guard"]
    assert guard["literal_terms"] == ["+03|16|27|45", "-04|16|27|35"]
    assert guard["pure_amplitudes"] == [1, 1, 1]
    assert guard["formal_triangle_guard_preserved"] is True
    assert guard["remaining_mixed_violations"] == 69
    assert guard["normalized_X5"] is False
    assert set(guard["beta_00000_cofactors"].values()) == {0}
    verdict = result["verdict"]
    assert verdict == {
        "arbitrary_bicoloured_full_X5_routes_to_existing_terminal_theorem": False,
        "pure_rows_exclude_s0_kappa100": False,
        "remaining_missing_input": (
            "a source-labelled identity controlling all off-support mixed-row "
            "cancellations, or proving activity for a different reciprocal covector"
        ),
        "support_preserving_full_X5_routes_to_contradiction": True,
    }
    assert evidence["status"] == "SUPPORT_RESTRICTED_LEMMA_PROVED_GENERAL_X5_NOT_CLOSED"
    assert evidence["terminal_scope"] == {
        "pure_rows_exclude_inactivity": False,
        "support_preserving_full_X5_excluded": True,
        "arbitrary_bicoloured_full_X5_excluded": False,
        "general_conjecture_claim": False,
        "degree_twelve_read": False,
        "broad_solve": False,
    }


def main() -> None:
    assert sha256(PARENT) == PARENT_SHA256
    result_path = HERE / "results_pure_row_guard.json"
    evidence_path = HERE / "EVIDENCE.json"
    result, evidence = json.loads(result_path.read_text()), json.loads(evidence_path.read_text())
    check(result, evidence)

    hostile_tests = 0
    mutations = []
    for name, mutate in (
        ("invent_full_X5", lambda item: item["first_off_support_cancellation_guard"].__setitem__("normalized_X5", True)),
        ("invent_activity", lambda item: item["minimal_pure_normalized_extension"].__setitem__("s_L", 1)),
        ("erase_mixed_violations", lambda item: item["minimal_pure_normalized_extension"].__setitem__("mixed_violations", 0)),
        ("invent_general_theorem", lambda item: item["verdict"].__setitem__("arbitrary_bicoloured_full_X5_routes_to_existing_terminal_theorem", True)),
    ):
        changed = copy.deepcopy(result)
        mutate(changed)
        try:
            check(changed, evidence)
        except AssertionError:
            hostile_tests += 1
            mutations.append(name)
        else:
            raise AssertionError(f"hostile mutation accepted: {name}")
    assert hostile_tests == 4

    output = {
        "schema": "KRENN_X5_RECIPROCITY_PURE_ROW_GUARD_VALIDATION_V1",
        "status": "PASS_FAIL_CLOSED_SCOPE_VALIDATION",
        "hostile_tests_passed": hostile_tests,
        "hostile_mutations": mutations,
        "input_sha256": {
            "parent_manifest": PARENT_SHA256,
            "audit_source": sha256(HERE / "audit_pure_row_guard.py"),
            "result": sha256(result_path),
            "evidence": sha256(evidence_path),
            "report": sha256(HERE / "REPORT.md"),
        },
        "degree_twelve_read": False,
        "broad_solve": False,
    }
    temporary = HERE / "results_validation.json.tmp"
    temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_validation.json")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
