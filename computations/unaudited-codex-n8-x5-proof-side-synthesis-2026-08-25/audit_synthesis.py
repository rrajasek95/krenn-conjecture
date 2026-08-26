#!/usr/bin/env python3
"""Fail-closed, small-file audit for the X5 proof-side synthesis."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def load(path: Path) -> dict:
    with path.open() as stream:
        return json.load(stream)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    evidence = load(HERE / "EVIDENCE.json")
    templates = load(HERE / "results_template_identity_audit.json")
    contractions = load(HERE / "results_d10_direct_contraction_audit.json")
    reciprocity = load(HERE / "results_same_source_reciprocity.json")

    d10_path = ROOT / "computations/unaudited-codex-n8-x5-four-d10-seeded-support-repair-2026-08-25/results_final_audit.json"
    d11_path = ROOT / "computations/unaudited-codex-n8-x5-four-d11-seeded-support-repair-2026-08-25/results_final_audit.json"
    recurrence_path = ROOT / "computations/unaudited-codex-n8-x5-four-dual-degree-recurrence-audit-2026-08-25/THEOREM_AUDIT.json"
    partial_path = ROOT / "computations/unaudited-codex-n8-x5-d11-triangle-partial-batch-production-held-2026-08-25/production_partial_batch_p107/checkpoint_audit.json"
    cross_path = ROOT / "computations/unaudited-codex-n8-x5-d11-triangle-transport-diagnostic-2026-08-25/results_audit.json"

    d10 = load(d10_path)
    d11 = load(d11_path)
    recurrence = load(recurrence_path)
    partial = load(partial_path)
    cross = load(cross_path)

    assert evidence["status"] == "EXACT_BOUNDED_CHAIN_COMPLETE_D6_D10_DIRECT_D11_ONLY"
    assert evidence["scope"]["degree_twelve_read"] is False
    assert evidence["scope"]["new_heavy_solve"] is False

    # Characteristic-zero coverage already accepted upstream.
    assert d10["status"] == "PASS_FOUR_EXACT_CHARACTERISTIC_ZERO_D10_OBSTRUCTIONS"
    assert len(d10["records"]) == 4
    assert d10["total_pairing_failures"] == 0
    assert d11["status"] == "FAIL_CLOSED_COLOURED_D11_UNRESOLVED"
    assert d11["accepted_exact_branches"] == ["direct"]
    assert d11["direct_literal_incident_columns_replayed"] == 326
    assert d11["unresolved_branches"] == [
        "triangle_endpoint_colour",
        "third_colour",
        "cap_endpoint_colour",
    ]

    # The recurrence theorem is positive, but every retained base fails the
    # identities needed for unrestricted iteration.
    assert recurrence["status"] == "PASS_DIRECT_D9_PROOF_AND_PRECISE_NO_GLOBAL_RECURRENCE_DIAGNOSIS"
    assert recurrence["all_degree_induction_result"]["proved"] is False
    assert templates["status"] == "PASS_EXACT_SMALL_TEMPLATE_TESTS"
    assert templates["direct_d10_to_d11_pure_transport_equal"] is True
    assert templates["d10_common_t_free_correction_decomposition"]["common_core"] == {
        "coefficient_set": [-1, 1],
        "l1_norm": 168,
        "max_abs": 1,
        "support": 168,
        "t_valuation_histogram": {"0": 168},
    }
    tails = templates["d10_common_t_free_correction_decomposition"]["branch_tails"]
    assert {branch: value["support"] for branch, value in tails.items()} == {
        "cap_endpoint_colour": 16,
        "third_colour": 16,
        "triangle_endpoint_colour": 14,
    }
    assert all(value["matching_shifted_d8_carrier_rows"] == 0 for value in tails.values())
    assert set(templates["d11_identity_coordinate_offender_intersections"].values()) == {0}
    seed_failures = {
        branch: audit["exact_transport_pairing_failures"]
        for branch, audit in templates["d11_transport_seed_audits"].items()
    }
    assert seed_failures == {
        "cap_endpoint_colour": 70,
        "direct": 0,
        "third_colour": 76,
        "triangle_endpoint_colour": 76,
    }
    assert all(audit["all_offenders_t_free_c1"] for audit in templates["d11_transport_seed_audits"].values())

    # New exact negative finite-contraction test: C1 explains D11, but C2/C4
    # explicitly prevent promoting direct D10 to an all-degree base.
    assert contractions["status"] == "PASS_EXACT_NEGATIVE_ALL_DEGREE_TEST"
    assert contractions["direct_d10_to_d11_c1_transport_failures"] == 0
    assert contractions["by_contraction"] == {
        "2": {"candidates": 491, "failures": 491},
        "4": {"candidates": 615, "failures": 615},
    }
    assert contractions["total_contraction_failures"] == 1106
    assert contractions["all_iterated_t_extensions_proved"] is False

    # Exact same-source pair-switching identity and its precise limitation.
    assert reciprocity["status"] == "PASS_EXACT_RECIPROCITY_AND_FIRST_FALSE_CLEAN_CAP_EQUATION"
    assert reciprocity["proved_lemma"]["physical_pair_configurations"] == 420
    assert reciprocity["proved_lemma"]["basis_coordinate_identities"] == 34_020
    assert reciprocity["conditional_diagonal_branch_corollary"]["branches"] == [
        "triangle_endpoint_colour",
        "cap_endpoint_colour",
        "third_colour",
    ]
    false_clean = reciprocity["first_false_clean_cap_strengthening"]
    assert false_clean["s_L"] == 0
    assert false_clean["kappa_L"] == [1, 0, 0]
    assert false_clean["nonzero_response_edges"] == ["67"]
    assert false_clean["r_squared_and_cap_error"] == "zero by single-edge support"
    assert reciprocity["direct_branch_first_missing_term"] == {
        "consequence": (
            "the five-set annihilator kills every direct-pair term before the "
            "opposite-edge survivor is formed; no s=<K,A_pq> cancellation row exists"
        ),
        "crossing_sector": "T1 only",
        "direct_pq_matchings": 15,
        "first_literal_matching": "67|01|23|45",
    }

    # Current D11 triangle state is an exact modular restart checkpoint only.
    assert partial["status"] == "PASS_EXACT_RESTART_CHECKPOINT"
    assert partial["prime"] == 1073741827
    assert partial["selected_columns"] == 1_250_001
    assert partial["dual_support"] == 1_378_456
    assert partial["selected_pairings_replayed"] == 1_250_001
    assert partial["pairing_failures"] == 0
    assert partial["target_coefficient"] == 1
    assert partial["mathematical_verdict"] is None
    assert partial["second_prime_launched"] is False

    # Identity-coordinate cross-branch transport is an exact negative test,
    # not a proof against a still-unsearched nontrivial variable permutation.
    assert cross["status"] == "PASS"
    assert cross["coordinate_identity_exact"] is True
    assert cross["small_support_repair_available"] is False
    assert cross["repair_consistency_evaluated"] is False
    assert {record["violation_columns"] for record in cross["branches"].values()} == {208_088}
    assert cross["global_dual_claim"] is False

    result = {
        "schema": "KRENN_X5_PROOF_SIDE_SYNTHESIS_AUDIT_V1",
        "status": "PASS_EXACT_SCOPE_AND_IDENTITY_AUDIT",
        "accepted_scope": "four frozen branches D6-D10 plus direct D11",
        "unresolved_scope": [
            "three coloured D11 branches",
            "all-degree induction",
            "full conjecture",
        ],
        "new_supported_identity": {
            "certificate_template": {
                "description": "common t-free coloured D10 correction core",
                "support": 168,
                "branch_tail_supports": {
                    "triangle_endpoint_colour": 14,
                    "third_colour": 16,
                    "cap_endpoint_colour": 16,
                },
            },
            "same_source_algebra": {
                "identity": "<L,R_ab^pq(K)> = <K,R_pq^ab(L)>",
                "coordinate_identities": 34_020,
                "clean_cap_activity_follows": False,
            },
        },
        "new_contradicted_identity": {
            "description": "direct D10 as an all-degree t-extension base",
            "C2_failures": 491,
            "C4_failures": 615,
        },
        "current_partial_checkpoint": {
            "field": 1073741827,
            "selected_columns": 1_250_001,
            "dual_support": 1_378_456,
            "global_or_characteristic_zero": False,
        },
        "input_sha256": {
            "evidence": sha256(HERE / "EVIDENCE.json"),
            "template_audit": sha256(HERE / "results_template_identity_audit.json"),
            "contraction_audit": sha256(HERE / "results_d10_direct_contraction_audit.json"),
            "same_source_reciprocity_audit": sha256(HERE / "results_same_source_reciprocity.json"),
            "d10_final_audit": sha256(d10_path),
            "d11_final_audit": sha256(d11_path),
            "recurrence_theorem_audit": sha256(recurrence_path),
            "partial_checkpoint_audit": sha256(partial_path),
            "cross_branch_transport_audit": sha256(cross_path),
        },
        "guards": {
            "new_heavy_solve": False,
            "degree_twelve_read": False,
            "global_D11_claim": False,
            "all_degree_claim": False,
        },
    }
    output = HERE / "results_synthesis_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
