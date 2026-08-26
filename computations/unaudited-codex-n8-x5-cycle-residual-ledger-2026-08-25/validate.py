#!/usr/bin/env python3
"""Fail-closed validator for the X5 cycle residual ledger."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-support-walk-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "45e9e0de636bba080efc34b4005ed4a8a62b5c0fc37f15419d670275dfa4df1f"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert result["status"] == "PASS_SCALAR_INVARIANTS_REFUTED_RESIDUAL_NONVANISHING_PROVED"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    cycle = result["cycle_ledger"]
    assert cycle["cycles"] == len(cycle["records"]) == 140
    assert cycle["guard_preserving_cycles"] == 18
    assert cycle["distribution_classes"] == 12
    assert cycle["guard_distribution_classes"] == 3
    verdict = result["invariant_verdict"]
    assert verdict["nonzero_count_invariant"] is False
    assert verdict["signed_sum_invariant"] is False
    assert verdict["unique_base_count_invariant"] is False
    assert verdict["unique_base_parity_invariant"] is False
    assert verdict["flattening_rank_invariant"] is False
    assert set(verdict["change_witnesses"]) == {
        "nonzero_mixed","signed_sum","unique_base_count","unique_base_parity","flattening_rank"
    }
    assert verdict["repaired_sources_checked"] == 1120
    repairs = result["canonical_first_residual_repairs"]
    assert repairs["raw_minimum_cells"] == 1
    assert repairs["raw_patterns_rejected_by_pure_normalization"] == 1
    assert repairs["admissible_minimum_cells"] == 2
    assert len(repairs["repair_patterns"]) == 8
    assert repairs["all_cycle_repair_moves"] == 1120
    assert repairs["all_cycle_repair_quotient_classes"] == 1
    assert repairs["common_unique_base_residual"] == "Phi(00200002)=+1 from 03|16|27|45"
    assert repairs["zero_residual_sources"] == 0
    saturated = result["colour_saturated_cycle"]
    assert saturated["offdiagonal_new_cells"] == 24
    assert saturated["pure_amplitudes"] == [1,1,1]
    assert saturated["outside_response_count"] == 0
    assert saturated["ledger"]["nonzero_mixed"] == saturated["ledger"]["unique_base_count"] == 6
    assert len(saturated["unique_base_residual_words"]) == 6
    assert saturated["identity"] == "Phi(a,b,b,a,a,a,b,b)=1 for all a!=b"
    assert saturated["mixed_violations"] == 1680
    assert saturated["normalized_X5"] is False
    assert result["scope"]["residual_nonvanishing_after_every_classified_move"] is True
    assert result["scope"]["arbitrary_nonminimal_repairs_exhausted"] is False
    assert result["scope"]["full_conjecture_claim"] is False
    assert evidence["scope"]["zero_residual_cycle_found"] is False
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
    result = json.loads((HERE / "results_cycle_residual_ledger.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r,e: r["cycle_ledger"].update(distribution_classes=1),
        lambda r,e: r["invariant_verdict"].update(signed_sum_invariant=True),
        lambda r,e: r["invariant_verdict"].update(flattening_rank_invariant=True),
        lambda r,e: r["canonical_first_residual_repairs"].update(all_cycle_repair_moves=1119),
        lambda r,e: r["canonical_first_residual_repairs"].update(zero_residual_sources=1),
        lambda r,e: r["colour_saturated_cycle"].update(unique_base_residual_words=[]),
        lambda r,e: r["colour_saturated_cycle"].update(normalized_X5=True),
        lambda r,e: r["scope"].update(arbitrary_nonminimal_repairs_exhausted=True),
        lambda r,e: e["scope"].update(zero_residual_cycle_found=True),
        lambda r,e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_CYCLE_RESIDUAL_LEDGER_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "all 140 first-residual minimal repair quotients and colour-saturated endpoint",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()

