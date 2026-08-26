#!/usr/bin/env python3
"""Fail-closed validation for the four-cell colour escalation package."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "dca3d614af5203d5dc2e1b6adb4c2c3f1621d3b0cf368f68d079a376f979f779"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert result["status"] == "PASS_MINIMAL_FOUR_TO_SIX_CELL_ESCALATION"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    first = result["exact_first_escalation"]
    assert first["unique_pure_preserving_repair"] == "A45[1,2]=+1"
    assert len(first["all_one_cell_repairs"]) == 2
    assert sum(item["pure_preserving"] for item in first["all_one_cell_repairs"]) == 1
    assert first["next_forced_word"] == "00002100" and first["next_forced_amplitude"] == -1
    second = result["exact_second_escalation"]
    assert second["unique_pure_preserving_repair"] == "A45[2,1]=+1"
    assert second["simultaneous_matching_pairs_checked"] == 7
    assert second["distinct_at_most_two_cell_supports"] == 5
    assert second["unique_pure_preserving_two_cell_support"] == ["A45[1,2]", "A45[2,1]"]
    six = result["smallest_surviving_six_cell_support"]
    assert six["pure_amplitudes"] == [1,1,1]
    assert six["mixed_census"]["count"] == 96
    assert six["unique_base_forced_word"] == "00100001"
    assert six["unique_base_forced_amplitude"] == 1
    assert six["one_cell_repairs"] == 0
    boundary = result["next_minimal_boundary"]
    assert boundary["two_missing_cell_matchings"] == 12
    assert boundary["pure_preserving_patterns"] == 6
    assert boundary["response_branch_patterns"] == boundary["guard_preserving_patterns"] == 3
    assert len(boundary["patterns"]) == 6
    assert all(item["common_forced_word"] == "00200002" for item in boundary["patterns"])
    assert all(item["common_forced_amplitude"] == 1 for item in boundary["patterns"])
    assert result["restricted_monovariant"]["values"] == [2,1,0]
    assert result["restricted_monovariant"]["general_nonminimal_chain_proved"] is False
    assert result["scope"]["minimal_four_to_six_cell_chain_proved"] is True
    assert result["scope"]["active_clean_cap_proved"] is False
    assert result["scope"]["full_conjecture_claim"] is False
    assert evidence["residual_identity"]["identity"] == "Phi(w)=A45[d,e]-1"
    assert evidence["scope"]["general_off_support_monovariant_proved"] is False
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
    result = json.loads((HERE / "results_four_cell_escalation.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r,e: r["exact_first_escalation"].update(unique_pure_preserving_repair="A12[0,0]=-1"),
        lambda r,e: r["exact_second_escalation"].update(distinct_at_most_two_cell_supports=4),
        lambda r,e: r["smallest_surviving_six_cell_support"].update(one_cell_repairs=1),
        lambda r,e: r["next_minimal_boundary"].update(pure_preserving_patterns=7),
        lambda r,e: r["next_minimal_boundary"]["patterns"][0].update(common_forced_amplitude=0),
        lambda r,e: r["restricted_monovariant"].update(general_nonminimal_chain_proved=True),
        lambda r,e: r["scope"].update(active_clean_cap_proved=True),
        lambda r,e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_FOUR_CELL_COLOUR_ESCALATION_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "minimal four-to-six-cell colour escalation",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()

