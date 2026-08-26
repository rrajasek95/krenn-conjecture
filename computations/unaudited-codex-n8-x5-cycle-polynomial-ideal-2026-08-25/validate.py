#!/usr/bin/env python3
"""Fail-closed validator for the X5 cycle polynomial ideal certificate."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-cycle-residual-ledger-2026-08-25/MANIFEST.sha256"
CORE = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25/audit_two_cell_dichotomy.py"
PARENT_SHA256 = "a8de425bbe54221874b4c75cb45b8dd4a465f628c881536d2e4d785a9afe4ab1"
CORE_SHA256 = "f8305d4b514ac6dc0a2b28b359dbca62929667248596beee48804eb43109e876"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def check(result, evidence):
    assert sha256(PARENT) == PARENT_SHA256
    assert sha256(CORE) == CORE_SHA256
    assert result["status"] == "PASS_RESIDUAL_IDEAL_IS_UNIT_IN_CYCLE_FAMILY"
    assert evidence["status"] == "PROVED_UNIT_IDEAL_FOR_ARBITRARY_CYCLE_BLOCK_FAMILY"
    assert result["parent_manifest_sha256"] == evidence["parent_manifest_sha256"] == PARENT_SHA256
    assert result["core_sha256"] == evidence["core_source_sha256"] == CORE_SHA256
    factorization = result["factorization"]
    assert factorization["words_verified_symbolically"] == len(factorization["records"]) == 81
    assert len({tuple(record["pair_colours"]) for record in factorization["records"]}) == 81
    assert factorization["identity"] == "Phi(w)=(1+X[a,d]*Y[a,d])*(1+U[b,c]*V[b,c])"
    assert result["pure_normalization"]["equations"] == ["P_0*Q_0=1", "P_1*Q_1=1", "P_2*Q_2=1"]
    ideal = result["six_residual_ideal"]
    assert len(ideal["certificates"]) == 6
    assert {tuple(item["colours"]) for item in ideal["certificates"]} == {
        (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)
    }
    assert all("-1 = " in item["certificate"] for item in ideal["certificates"])
    assert ideal["ideal_in_pure_quotient"] == "unit ideal"
    assert ideal["common_zero_over_nonzero_unital_ring"] is False
    replay = result["rational_replay"]
    assert replay["samples"] == 257
    assert replay["all_81_literal_amplitudes_per_sample"] is True
    assert replay["all_pure_rows"] == [1, 1, 1]
    assert replay["all_residual_inverse_certificates"] is True
    assert replay["records_sha256"] == evidence["exact_replay"]["rational_records_sha256"]
    family = result["arbitrary_24_offdiagonal_guard_family"]
    assert family["variables"] == 24
    assert family["six_residual_polynomials"] == ["1"] * 6
    assert family["pure_rows_automatic"] == [1, 1, 1]
    assert family["formal_triangle_response_guard_preserved"] is True
    assert family["samples_replayed"] == 257
    assert family["common_zero"] is False
    assert evidence["arbitrary_24_cell_specialization"]["residuals"] == [1] * 6
    assert result["scope"]["arbitrary_24_cell_saturated_family_proved"] is True
    assert result["scope"]["diagonal_cycle_extension_under_pure_normalization_proved"] is True
    assert result["scope"]["arbitrary_cells_outside_four_cycle_blocks_exhausted"] is False
    assert result["scope"]["full_conjecture_claim"] is False
    assert evidence["scope"]["full_X5_guard_exhausted"] is False
    assert evidence["scope"]["full_conjecture_claim"] is False
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
    result = json.loads((HERE / "results_cycle_polynomial_ideal.json").read_text())
    evidence = json.loads((HERE / "EVIDENCE.json").read_text())
    assert check(result, evidence)
    hostiles = [
        lambda r, e: r["factorization"].update(words_verified_symbolically=80),
        lambda r, e: r["factorization"]["records"].pop(),
        lambda r, e: r["pure_normalization"].update(equations=[]),
        lambda r, e: r["six_residual_ideal"]["certificates"].pop(),
        lambda r, e: r["six_residual_ideal"].update(common_zero_over_nonzero_unital_ring=True),
        lambda r, e: r["rational_replay"].update(samples=256),
        lambda r, e: r["arbitrary_24_offdiagonal_guard_family"].update(six_residual_polynomials=["0"] * 6),
        lambda r, e: r["arbitrary_24_offdiagonal_guard_family"].update(formal_triangle_response_guard_preserved=False),
        lambda r, e: r["scope"].update(arbitrary_cells_outside_four_cycle_blocks_exhausted=True),
        lambda r, e: e["scope"].update(full_X5_guard_exhausted=True),
        lambda r, e: e.update(parent_manifest_sha256="00" * 32),
    ]
    assert all(must_reject(mutator, result, evidence) for mutator in hostiles)
    output = {
        "schema": "KRENN_X5_CYCLE_POLYNOMIAL_IDEAL_VALIDATION_V1",
        "status": "PASS",
        "hostile_mutations_rejected": len(hostiles),
        "parent_manifest_sha256": PARENT_SHA256,
        "proved_scope": "arbitrary four-cycle-block family under pure normalization, including arbitrary 24-cell offdiagonal specialization",
    }
    (HERE / "results_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
