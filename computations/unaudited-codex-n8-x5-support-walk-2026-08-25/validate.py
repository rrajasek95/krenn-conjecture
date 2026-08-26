#!/usr/bin/env python3
"""Fail-closed validator for the X5 support-walk cycle package."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-successive-minimal-chain-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "6d77153968c4386cd56ab01650c53882efafc15cb9d00cba55d5877ad9dc3717"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert result["status"] == "PASS_CELL_NO_REUSE_EDGE_CYCLE_FOUND"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    pair16 = result["pair16_quotient"]
    assert pair16["ten_cell_sources_checked"] == 36
    assert pair16["quotient_classes"] == 1
    assert pair16["pure_preserving_patterns_per_colour"] == 6
    assert pair16["resulting_sources_after_both_colours"] == 1296
    pair03 = result["pair03_quotient"]
    assert pair03["input_sources_checked"] == 1296
    assert pair03["raw_minimum_cells"] == 1
    assert pair03["raw_patterns_rejected_by_pure_normalization"] == 1
    assert pair03["admissible_minimum_cells"] == 2
    assert pair03["pure_preserving_patterns_per_colour"] == 8
    assert pair03["completed_reference_zero_path_count"] == 82944
    walk = result["no_reuse_and_cycle"]
    assert walk["coordinate_layer_intersections_empty"] is True
    assert walk["source_coordinate_reuse_across_pair45_27_16_03"] is False
    assert walk["edge_level_no_cycle_lemma"] is False
    assert walk["edge_reuse"] == ["04","35"]
    quotient = result["cycle_quotient"]
    assert quotient["branch_triples"] == 288
    assert quotient["return_amplitude_census"] == {"-2":4,"-1":48,"0":140,"1":96}
    assert quotient["cycles"] == 140
    assert quotient["guard_preserving_cycles"] == 18
    cycle = result["smallest_guard_preserving_cycle"]
    assert cycle["new_cell_count"] == 8
    assert cycle["pure_amplitudes"] == [1,1,1]
    assert cycle["outside_response_count_for_K_I"] == 0
    assert cycle["same_source_reciprocity_compatible"] is True
    assert len(cycle["cancelled_walk_terms"]) == 5
    assert cycle["remaining_mixed_violations"] == 132
    assert cycle["first_residual_word"] == "00002200"
    assert cycle["first_residual_amplitude"] == 1
    assert result["scope"]["smallest_cycle_within_successive_minimal_policy"] is True
    assert result["scope"]["global_arbitrary_source_cycle_minimality"] is False
    assert result["scope"]["full_conjecture_claim"] is False
    assert evidence["scope"]["edge_no_cycle_refuted"] is True
    assert evidence["scope"]["active_clean_cap_proved"] is False
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
    result = json.loads((HERE / "results_support_walk_cycle.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r,e: r["pair16_quotient"].update(quotient_classes=2),
        lambda r,e: r["pair03_quotient"].update(raw_patterns_rejected_by_pure_normalization=0),
        lambda r,e: r["no_reuse_and_cycle"].update(edge_level_no_cycle_lemma=True),
        lambda r,e: r["cycle_quotient"].update(cycles=139),
        lambda r,e: r["cycle_quotient"].update(guard_preserving_cycles=0),
        lambda r,e: r["smallest_guard_preserving_cycle"].update(outside_response_count_for_K_I=1),
        lambda r,e: r["smallest_guard_preserving_cycle"].update(first_residual_amplitude=0),
        lambda r,e: r["scope"].update(global_arbitrary_source_cycle_minimality=True),
        lambda r,e: e["scope"].update(active_clean_cap_proved=True),
        lambda r,e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_SUPPORT_WALK_CYCLE_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "reference-zero coordinate no-reuse and smallest successive-minimal edge cycle",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()

