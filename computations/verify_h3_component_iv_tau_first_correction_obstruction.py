#!/usr/bin/env python3
"""Maximal literal prefix of the five Component-IV tau_v chains.

The checker composes four exact source-labelled calculations:

1. the strict two-chart Cech comparison and its two marked principal parts;
2. the denominator Hom commutator;
3. the full-nine Schur connecting map; and
4. the complete fourth-Hasse correction and its physical ridge defect.

It constructs no new generator.  The output identifies the first attaching
datum required to turn the formal correction into a physical chain.
"""

from hashlib import sha256
import json

import verify_h3_component_iv_physical_definability_gate as GATE
import verify_h3_literal_full_nine_schur_polar_no_go as SCHUR
import verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction as THIRD
import verify_h3_shifted_principal_parts_comparison_obstruction as PP


EXPECTED_DIGEST = "4b673df4aee4935e1751a2a92212d5f53ca61432c8a520a89193db7383149571"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def actual_principal_parts_prefix():
    records, ranks = PP.polar_and_relative_jet_audit()
    require(len(records) == 5,
            "two-chart principal-parts face count changed")
    require(ranks["first_face_columns"] == 10
            and ranks["first_face_rank"] == 10,
            "literal first principal-parts faces lost independence")
    require(ranks["mixed_columns"] == 5
            and ranks["mixed_rank"] == 5,
            "mixed sector-transfer symbols lost independence")
    require(ranks["uniform_shift_sites"] == [PP.X, PP.P, PP.Q]
            and ranks["uniform_shift_weight"] == 3,
            "derived cap shift changed")
    require(all(record["relative_first_jet_boundaries"] == [0, 0]
                and record["relative_target"] == 0
                and record["pq_mixed_sector"] == "direct"
                and record["pr_mixed_sector"] == "two_star"
                for record in records),
            "one source-provenant relative jet changed type")
    return {
        "base_ring": "Q[all labelled source cells]",
        "cover": "two labelled chart presentations pq,pr",
        "relative_cells": [f"K_{record['deleted']}=r_pq-r_pr"
                           for record in records],
        "marked_directions": ["a_xv^00", "a_pq^00"],
        "first_faces": ranks["first_face_columns"],
        "first_face_rank": ranks["first_face_rank"],
        "first_face_boundaries": 0,
        "mixed_symbols": ranks["mixed_columns"],
        "mixed_symbol_rank": ranks["mixed_rank"],
        "sector_transfer": "(h_v)_pq,direct-(h_v)_pr,two-star",
        "physical_target": 0,
        "derived_shift_sites": ranks["uniform_shift_sites"],
    }


def first_attachment():
    denominator = PP.denominator_commutator_audit()
    require(denominator["denominator_columns"] == 15
            and len(denominator["nonzero_commutator_columns"]) == 5,
            "denominator attachment support changed")
    require(denominator["commutator_rank"] == 5
            and denominator["old_pure_image_rank"] == 5
            and denominator["combined_rank"] == 10,
            "denominator attachment cokernel changed")
    require(denominator["chain_map_exists_on_old_denominator_complex"] is False,
            "old denominator complex acquired the tau attachment")

    schur, schur_digest = SCHUR.audit()
    identity = [
        [[1, 1] if row == column else [0, 1] for column in range(5)]
        for row in range(5)
    ]
    require(schur["connecting_matrix"] == identity
            and schur["connecting_rank"] == 5,
            "literal source-relative connecting map is not I_5")
    require(schur["schur_lift_exists"] == [False] * 5
            and schur["full_nine_target_pairing_well_defined"] is False,
            "one bare tau face unexpectedly acquired a full-nine lift")
    return {
        "denominator_columns": denominator["denominator_columns"],
        "nonzero_face_columns": denominator["nonzero_commutator_columns"],
        "commutator": "omega(d_(v,m_v))=h_v*Y_0",
        "old_pure_rank": denominator["old_pure_image_rank"],
        "rank_after_commutator": denominator["combined_rank"],
        "source_relative_connecting_matrix": "I_5",
        "connecting_rank": schur["connecting_rank"],
        "bare_tau_lift_exists": False,
        "schur_ledger": schur_digest,
    }


def complete_first_correction():
    third = THIRD.audit()
    total = third["third_cofactor_total_complex"]
    formal = total["formal_total_complex"]
    bridge = total["source_labelled_bridge"]
    descent = total["descent_obstruction"]

    require(total["selected_cubes"] == 15,
            "complete Hasse correction cube count changed")
    require(formal["tail_signature"] == [-1, 0, 0, 0]
            and formal["total_signature"] == [0, 1, 0, 0]
            and formal["d_total"] == "Yw"
            and formal["d_squared"] == 0,
            "formal corrected tau signature changed")
    require(bridge["nonzero_ridges_per_cube"] == 2
            and bridge["ridge_mismatch_rank"] == 6
            and bridge["primitive_omega_rank"] == 5
            and bridge["omega_terms_per_cube"] == 4,
            "first physical bridge obstruction changed")
    require(descent["fourth_operator_on_source_equation"] == 1
            and descent["pure_conormal_u_coefficient"] == -1,
            "source descent unit obstruction changed")

    return {
        "literal_cubes": total["selected_cubes"],
        "third_cofactor_identity": total["identity"],
        "formal_tail_signature": formal["tail_signature"],
        "formal_total_signature": formal["total_signature"],
        "formal_boundary": formal["d_total"],
        "formal_d_squared": formal["d_squared"],
        "physical_descent": False,
        "nonzero_endpoint_ridges_per_cube": bridge["nonzero_ridges_per_cube"],
        "complete_endpoint_ridge_rank": bridge["ridge_mismatch_rank"],
        "omega_rank": bridge["primitive_omega_rank"],
        "omega_terms": bridge["omega_terms_per_cube"],
        "omega_formula": (
            "(a_pq^22-a_pq^00)-(a_xv^(0,m_v)-a_xv^00)"
        ),
        "fourth_operator_on_H_m":
            descent["fourth_operator_on_source_equation"],
        "equivariant_nonzero_sum": True,
    }


def physical_target_signature():
    physical = GATE.source_relative_gate()["downstairs"]
    require(physical["desired_chain"] == [0, 1, 0, 0]
            and physical["separator"] == [1, 1, 1, -1]
            and physical["separator_value"] == "1",
            "physical Component-IV signature changed")
    return {
        "coordinates": physical["coordinates"],
        "desired_chain": physical["desired_chain"],
        "separator": physical["separator"],
        "separator_value": physical["separator_value"],
    }


def main():
    ledger = {
        "scope": "h=3 Component-IV five-face tau construction through first correction",
        "actual_principal_parts_prefix": actual_principal_parts_prefix(),
        "denominator_attachment": first_attachment(),
        "complete_first_correction": complete_first_correction(),
        "physical_target_signature": physical_target_signature(),
        "verdict": {
            "source_provenant_prefix": (
                "K_v and its two first principal-parts faces are literal cycles"
            ),
            "tau_v_constructed": False,
            "equivariant_sum_supplies_n_c": False,
            "first_obstruction": (
                "five independent primitive endpoint-ridge classes Omega_v"
            ),
            "next_attaching_datum": (
                "a source-labelled endpoint-word-change homotopy with boundary "
                "-Omega_v, zero target and zero ores, compatible with the "
                "denominator face and both chart sectors"
            ),
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, ("ledger changed", digest))

    print("h=3 Component-IV tau first correction: PHYSICAL OBSTRUCTION (exact)")
    print("literal prefix: five K_v Cech cells + ten first PP faces")
    print("denominator attachment: connecting matrix I_5")
    print("complete Hasse correction: formal signature (0,Yw,0,0), d^2=0")
    print("physical descent: five independent primitive endpoint-ridge Omega_v")
    print("equivariant sum supplies n_c: NO")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
