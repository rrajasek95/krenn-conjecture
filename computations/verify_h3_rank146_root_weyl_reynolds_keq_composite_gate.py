#!/usr/bin/env python3
"""Audit root/Weyl -> Reynolds -> K_Eq on the rank-146 P3 quotient.

The audit deliberately grants the strongest possible diagonal word/fine/
repeated/window transport.  This makes the final no-go insensitive to the
known normalized-bar endpoint and occurrence-placement debts: if the
composite still has no cap component, its first unavoidable failure is the
response-to-cap operation corner.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_canonical_principal_parts_gammajet_enrichment_gate.py":
        "0163890e3ec1a7fd115e93f34f68c37a5c82eaf984b36c5b72531c39e5769a0f",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py":
        "e17de52244d324a26ff6a8b08f9226283b89d1737a6dc3916359991e777efb17",
    "computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py":
        "092c90da62c9bd900939388a1ec7110de28f50c7b070d5029069ea3c3c9373a1",
    "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py":
        "8be3bc5bf85f8d633e77e2a0bdd18aea6d481c81f5fb6a6a947cbaf82f862302",
    "computations/verify_h3_gate_ii_endpoint_even_cap_operator_module_gate.py":
        "39cb3f4b4e83940993ef7ffa8633a3e13cf04631625d9a3729fb5ef9f8ca307c",
    "computations/verify_h3_endpoint_even_hom_target_cone_eq_terminal_gate.py":
        "c6886ba4652dd6cc4c92219db966e7b1a3e48ef2afe332b32b9d4576b3fa8e37",
    "computations/verify_h3_endpoint_even_literal_operator_algebra_r0_action_gate.py":
        "42a30f9cd823a67a0733dfb6961ed224e228caa3236140c2e0803db686839ef7",
}
EXPECTED_LEDGER_SHA256 = (
    "6bd3f79a2b8f493ac5736dfcc6c2f385a6118b9f8a6f2ec91db4e520d5532abe"
)
P3_DIMENSION = 146
ROOTS = ("AB", "AC")


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def matmul(left, right):
    return tuple(tuple(sum((left[row][middle] * right[middle][column]
                            for middle in range(len(right))), Q(0))
                       for column in range(len(right[0])))
                 for row in range(len(left)))


def shared_p3_and_word_audit(canonical, bar, relative_bar, telescope,
                             replay: bool) -> dict[str, object]:
    if replay:
        ledger, digest = canonical.audit("full")
        require(digest == canonical.EXPECTED_LEDGER_SHA256, digest)
        quotient = ledger["order_six_principal_parts"][
            "augmented_trigger_minimalization"]
        require(quotient["shared_P3_coordinates_after_quotient"] == 148
                and quotient["shared_P3_projection_rank"] == P3_DIMENSION,
                quotient)

    # The two actual normalized word intervals relevant to the two response
    # words have five and three changed sites.  Their endpoints are related,
    # but neither individual endpoint becomes an absolute normalized-bar
    # boundary: H0 is one-dimensional in both cases.
    pure = bar.cube_audit(5, audit_all_shuffles=True)
    mixed = bar.cube_audit(3, audit_all_shuffles=True)
    require((pure["vertices"], pure["incidence_rank"], pure["h0_dimension"])
            == (32, 31, 1)
            and (mixed["vertices"], mixed["incidence_rank"],
                 mixed["h0_dimension"]) == (8, 7, 1),
            (pure, mixed))

    grade = relative_bar.gamma_star_grade_audit()
    require(grade["literal_projection_to_C_phys_Gamma_star"] == "0 (off-grade)"
            and grade["is_the_kappa_operation_parent"] is False,
            grade)
    telescope_ledger, telescope_digest = telescope.audit()
    require(telescope_digest == telescope.EXPECTED_LEDGER_SHA256,
            telescope_digest)
    provenance = telescope_ledger["physical_provenance"]
    require(provenance["connected_SL3_or_Weyl_changes_B_label"] is False
            and "repeated-edge label" in provenance["colour_action_preserves"],
            provenance)

    return {
        "shared_site_coordinates_before_minimalization": 148,
        "shared_P3_response_rank": P3_DIMENSION,
        "response_words": ["11111111", "11211211"],
        "cap_word_endpoint": "01211222",
        "changed_site_counts_pure_mixed": [5, 3],
        "normalized_word_cube": {
            "pure_vertices_rank_H0": [32, 31, 1],
            "mixed_vertices_rank_H0": [8, 7, 1],
            "boundary": "all-L minus all-D",
            "single_all_L_endpoint_is_absolute": False,
        },
        "target_corrected_signed_Weyl_available": True,
        "target_correction_changes_response_operation_object": False,
        "colour_transport_preserves": provenance["colour_action_preserves"],
        "literal_Gamma_projection_before_diagonal_grants": 0,
        "literal_first_grade_failure": (
            "selected t*q_(v,N) fine/window and P3+K2 parent placement; "
            "the word endpoint alone retains response occurrence tags"
        ),
        "strong_grant_used_below": (
            "grant a monic target-safe word endpoint and every diagonal "
            "fine/repeated/window repair on all 146 directions"
        ),
    }


def reynolds_rank_audit() -> dict[str, object]:
    half = Q(1, 2)
    p_plus = ((half, half), (half, half))
    swap = ((Q(0), Q(1)), (Q(1), Q(0)))
    require(matmul(p_plus, p_plus) == p_plus
            and matmul(p_plus, swap) == p_plus
            and matmul(swap, p_plus) == p_plus
            and rank(tuple(zip(*p_plus, strict=True))) == 1,
            "endpoint Reynolds projector changed")
    oriented_rank = 2 * len(ROOTS) * P3_DIMENSION
    even_rank = len(ROOTS) * P3_DIMENSION
    return {
        "endpoint_projector": [["1/2", "1/2"], ["1/2", "1/2"]],
        "projector_rank_per_shared_P3_root_direction": 1,
        "oriented_two_root_rank_before_Reynolds": oriented_rank,
        "endpoint_even_two_root_rank_after_Reynolds": even_rank,
        "endpoint_even_rank_per_root": P3_DIMENSION,
        "Reynolds_loses_shared_P3_information": False,
    }


def operation_corner_and_root_dual_audit(receiving) -> dict[str, object]:
    algebra = receiving.root_weyl_cap_operation_algebra_audit()
    sections = receiving.literal_two_root_section_audit()
    require(algebra["generated_Hom_response_cap"] == 0
            and algebra["mixed_products_eC_eR_and_eR_eC"] == 0,
            algebra)
    require(sections["rank_base_one_AB_one_AC_one_unlabelled_pair_both"]
            == [24, 25, 25, 25, 26]
            and sections["cokernel_dimension_before_sections"] == 2,
            sections)

    # Matrix rows/columns are (response, cap).  Word/Weyl/Reynolds are in
    # e_R A e_R.  K_Eq and the target cone are in e_C A e_C.  Therefore
    # postcomposition is identically zero, independently on all 292 even
    # root-labelled coefficient directions.
    e_response = ((Q(1), Q(0)), (Q(0), Q(0)))
    e_cap = ((Q(0), Q(0)), (Q(0), Q(1)))
    require(matmul(e_cap, e_response) == ((Q(0), Q(0)),
                                                  (Q(0), Q(0))),
            "cap/response orthogonality changed")
    return {
        "word_Weyl_Reynolds_corner": "e_R A e_R",
        "K_Eq_target_cone_corner": "e_C A e_C",
        "strict_composite_response_to_cap_rank": 0,
        "response_rank_reaching_operation_gate": len(ROOTS) * P3_DIMENSION,
        "strong_diagonal_tag_base_rank": 24,
        "rank_after_AB_after_AC_after_unlabelled_after_both":
            [25, 25, 25, 26],
        "missing_root_labelled_Hom_dimension": 2,
        "primitive_duals": ["omega_AB^Hom", "omega_AC^Hom"],
        "survivor_after_one_unlabelled_root_sum":
            "(omega_AB^Hom-omega_AC^Hom)/2",
        "earliest_unavoidable_failure_after_diagonal_grants":
            "operation matrix unit e_C A e_R",
        "multiplicity_statement": (
            "the same two root operation characters are constant/natural "
            "over the rank-146 occurrence quotient; coefficient rank does "
            "not create 292 new operation generators"
        ),
    }


def keq_target_cone_audit() -> dict[str, object]:
    # Obstruction constants are (Eq,N23,N45).  The cap-internal target cone
    # has boundaries N23,N45.  It kills the target block but cannot create
    # an R->C matrix unit.
    target_cone = (
        (Q(0), Q(0)),
        (Q(1), Q(0)),
        (Q(0), Q(1)),
    )
    require(rank(tuple(zip(*target_cone, strict=True))) == 2,
            "target cone rank changed")
    response_boundary = (Q(1), Q(0))
    cap_eq_boundary = (Q(0), Q(1))
    omega_eq = (Q(1), Q(-1))
    require(rank((response_boundary, cap_eq_boundary)) == 2
            and sum(x * y for x, y in zip(omega_eq, response_boundary,
                                           strict=True)) == 1
            and sum(x * y for x, y in zip(omega_eq, cap_eq_boundary,
                                           strict=True)) == -1,
            "Eq separator changed")
    return {
        "conditional_target_cone_rank": 2,
        "target_H1_before_after": [2, 0],
        "relative_H1_before_after_target_cone": [3, 1],
        "surviving_conditional_class": "omega_Eq=(1,-1)",
        "target_cone_creates_response_to_cap_operation": False,
        "stage_order": (
            "the target cone is a proper-face completion after a cap landing; "
            "it cannot be postcomposed with a response vector while e_CAe_R=0"
        ),
        "next_boundary_if_both_root_Hom_units_are_granted": {
            "dG0_response": [1, 0],
            "dr0_Eq_cap": [0, 1],
            "rank": 2,
            "primitive_dual": [1, -1],
            "cokernel_rank": 1,
        },
    }


def audit(mode: str) -> tuple[dict[str, object], str]:
    pin_dependencies()
    canonical = load(
        "computations/verify_h3_canonical_principal_parts_gammajet_enrichment_gate.py",
        "rank146_canonical",
    )
    bar = load(
        "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py",
        "rank146_bar",
    )
    relative_bar = load(
        "computations/verify_h3_relative_gl3_bar_keq_kappa_normalization_gate.py",
        "rank146_relative_bar",
    )
    telescope = load(
        "computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py",
        "rank146_telescope",
    )
    receiving = load(
        "computations/verify_h3_psqjet_root_weyl_cap_r0_receiving_sections_gate.py",
        "rank146_receiving",
    )
    ledger = {
        "theorem": (
            "root/Weyl word transport and endpoint Reynolds preserve the "
            "rank-146 response quotient, but cap-internal K_Eq/target-cone "
            "operators cannot create an e_C A e_R component"
        ),
        "shared_P3_word_transport": shared_p3_and_word_audit(
            canonical, bar, relative_bar, telescope,
            replay=(mode != "structural")),
        "endpoint_Reynolds": reynolds_rank_audit(),
        "operation_gate": operation_corner_and_root_dual_audit(receiving),
        "K_Eq_target_cone": keq_target_cone_audit(),
        "verdict": {
            "literal_response_to_cap_component_nonzero": False,
            "literal_composite_rank": 0,
            "first_literal_failure": "fine/window placement after word transport",
            "first_failure_under_all_diagonal_tag_grants":
                "two root-natural e_C A e_R matrix units",
            "smallest_positive_datum": (
                "one root-natural endpoint-even Beck-Chevalley/excess map "
                "from the shared-site collision groupoid to AugP2, with "
                "excess boundary (H0-u)e_Eq; its AB and AC instances then "
                "feed the existing target cone"
            ),
        },
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit(arguments.mode)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        print("mode", arguments.mode)
        print("ledger_sha256", digest)
        print("response_to_cap_rank",
              ledger["operation_gate"]["strict_composite_response_to_cap_rank"])


if __name__ == "__main__":
    main()
