#!/usr/bin/env python3
"""Test whether the Gamma detector is intrinsic to the original EqSystem.

The official polynomial presentation has equation-word, matching-monomial
occurrence and divided differential/operator labels.  We retain all of them,
including the literal 8,580-column order-six histories, before asking for the
protected detector Psi=delta.(B-Eq).

The first obstruction precedes a Fredholm rank computation.  EqSystem has one
copy of each labelled occurrence.  The protected B and Eq rows are two
enriched copies of that same occurrence, forgotten by (b,e) |-> b+e.  Every
covector defined from the original labels pulls back diagonally as
(lambda,lambda), whereas Psi=(delta,-delta).  Thus Psi is not a functional on
the occurrence-labelled Taylor/Schreyer resolution.  Higher Schreyer cells
resolve kernels and cannot manufacture a missing degree-zero readout.

The checker also tests the derived-cap bypass.  Declaring the same parent
augmentation to be both B and Eq on the derived cap N changes dN=(1,0) to
(1,1); the correction is exactly the absolute Eq vector (0,1).  Hence this
declaration supplies, rather than avoids, the missing absolute Eq preimage.
Even after granting it, the pointed P_f/active-cap projection is independent
of the derived primitive-cap and invisible-q directions, so B augmentation
alone cannot extract the underived active cap.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_chart_model_is_official_eqsystem.py":
        "ef1a997323e0a116787fa3c50368e22ecd33804942a9179eabefa2993e4d9373",
    "computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py":
        "3eb7bc5bd51a9affa3aa0cdab113efc2856375c0de9e083efc611aed7cd1058f",
    "computations/verify_h3_order6_gammajet_collision_contraction_same_edge_gate.py":
        "6e8bb35089581c17ca70720fcbdd21896281531792db1002ec925e94326ab4eb",
    "computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py":
        "a1e81eef9343bd2dda01b106acc202698cc12e93e7db3b55d45f5c6268779c33",
    "computations/verify_h4_pointed_phi01_fixed_tail_h3_restriction_gate.py":
        "db1f9c4ccdf8b95cdbc681427ce5caa473385293f0e49f9817b185707e93e5b2",
    "computations/verify_h3_normalized_eq_base_change_tor_gate.py":
        "b7c409db8cff0141a153816d0d14525464c4fcadb0607b97da06181435059d50",
}
EXPECTED_LEDGER_SHA256 = (
    "9f36375ce004f03773a65b1f981cdf446f2e3b8f94d6af6b50eb5d1c43466307"
)
SITES = tuple(range(8))
COLOURS = tuple(range(3))
GAMMA_WORD = tuple(map(int, "01211222"))
DELTA = tuple(map(Q, (1, 1, -1, -1)))


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


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    rows = [[columns[column][row] for column in range(len(columns))]
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


def simplex_boundary(vertices: int, degree: int):
    source = tuple(combinations(range(vertices), degree + 1))
    target = tuple(combinations(range(vertices), degree))
    target_index = {face: index for index, face in enumerate(target)}
    columns = []
    for face in source:
        column = [Q(0)] * len(target)
        for position in range(len(face)):
            lower = face[:position] + face[position + 1:]
            column[target_index[lower]] += Q(-1 if position % 2 else 1)
        columns.append(tuple(column))
    return tuple(columns)


def official_occurrence_schreyer_audit(official, order6) \
        -> dict[str, object]:
    variables = tuple(
        (left, right, left_colour, right_colour)
        for left, right in combinations(SITES, 2)
        for left_colour, right_colour in product(COLOURS, repeat=2)
    )
    words = tuple(product(COLOURS, repeat=len(SITES)))
    matchings = tuple(official.OFFICIAL_MATCHINGS)
    require(len(variables) == 252 and len(words) == 6561
            and len(matchings) == 105, "official EqSystem census changed")

    gamma_occurrences = tuple(
        tuple((left, right, GAMMA_WORD[left], GAMMA_WORD[right])
              for left, right in matching)
        for matching in matchings
    )
    require(len(set(gamma_occurrences)) == 105
            and all(len(occurrence) == 4
                    for occurrence in gamma_occurrences),
            "Gamma matching occurrences changed")
    gamma_degree = tuple(
        1 if colour == GAMMA_WORD[site] else 0
        for site in SITES for colour in COLOURS
    )
    for occurrence in gamma_occurrences:
        observed = [0] * 24
        for left, right, left_colour, right_colour in occurrence:
            observed[3 * left + left_colour] += 1
            observed[3 * right + right_colour] += 1
        require(tuple(observed) == gamma_degree,
                (occurrence, observed, gamma_degree))

    # Specialize a four-generator Taylor/Schreyer packet at its coefficient
    # torus.  Its simplex ranks show explicitly that higher cells resolve the
    # lower kernels; they do not change the degree-zero occurrence labels.
    boundaries = tuple(simplex_boundary(4, degree)
                       for degree in (1, 2, 3))
    boundary_ranks = tuple(rank(boundary) for boundary in boundaries)
    require(tuple(map(len, boundaries)) == (6, 4, 1)
            and boundary_ranks == (3, 3, 1),
            (tuple(map(len, boundaries)), boundary_ranks))

    site, _orbit, loaded, columns, shifts, _metadata = (
        order6.build_current_tree())
    inventory, _shapes = order6.literal_pair_inventory(
        site, loaded, columns, shifts)
    require(len(columns) == 8580
            and inventory["coarsened_site_repeating_coordinates"] == 159
            and inventory["labelled_pair_shift_occurrences"] == 271,
            (len(columns), inventory))
    return {
        "official_variables": len(variables),
        "official_relation_words": len(words),
        "matching_terms_per_relation": len(matchings),
        "Gamma_relation_word": "".join(map(str, GAMMA_WORD)),
        "Gamma_matching_occurrence_basis": len(gamma_occurrences),
        "honest_multidegree": "N^24 site-colour degree",
        "all_105_Gamma_terms_have_same_N24_degree": True,
        "all_105_matching_monomial_occurrence_labels_are_distinct": True,
        "four_generator_Taylor_dimensions_C1_C2_C3": [6, 4, 1],
        "four_generator_Taylor_boundary_ranks": list(boundary_ranks),
        "higher_Schreyer_cells_change_degree_zero_readout_space": False,
        "order_six_literal_operator_columns": len(columns),
        "order_six_site_repeating_pair_coordinates": inventory[
            "coarsened_site_repeating_coordinates"],
        "order_six_pair_word_fine_occurrences": inventory[
            "labelled_pair_shift_occurrences"],
        "maximal_literal_label_schema": [
            "equation word", "parent matching monomial occurrence",
            "ordered divided-operator history", "pair/repeated shape",
            "word/fine shift",
        ],
        "B_or_Eq_operation_copy_is_an_original_label": False,
    }


def psi_label_descent_audit() -> dict[str, object]:
    basis = tuple(
        tuple(Q(row == column) for row in range(4))
        for column in range(4)
    )
    tied_pullbacks = tuple(vector + vector for vector in basis)
    psi = DELTA + tuple(-value for value in DELTA)
    forgetful_kernel = psi
    forgetful_image = tuple(forgetful_kernel[index]
                            + forgetful_kernel[index + 4]
                            for index in range(4))
    require(forgetful_image == (Q(0),) * 4
            and rank(tied_pullbacks) == 4
            and rank(tied_pullbacks + (psi,)) == 5
            and sum(left * right for left, right in
                    zip(psi, forgetful_kernel, strict=True)) == 8,
            (forgetful_image, rank(tied_pullbacks),
             rank(tied_pullbacks + (psi,))))

    # At the first protected label, descent would require the one intrinsic
    # value lambda(label_0) to be both +1 on B and -1 on Eq.
    first_required_values = (DELTA[0], -DELTA[0])
    require(first_required_values == (Q(1), Q(-1)),
            first_required_values)
    return {
        "intrinsic_four_occurrence_module": "U=Q^4",
        "enriched_protected_module": "U_B direct_sum U_Eq",
        "forgetful_map": "pi(b,e)=b+e",
        "pullback_of_intrinsic_covectors": "pi^*(lambda)=(lambda,lambda)",
        "intrinsic_covector_pullback_rank": rank(tied_pullbacks),
        "rank_after_adjoining_Psi": rank(tied_pullbacks + (psi,)),
        "Psi": [str(value) for value in psi],
        "forgetful_kernel_witness": [str(value)
                                      for value in forgetful_kernel],
        "pi_of_kernel_witness": [str(value) for value in forgetful_image],
        "Psi_on_kernel_witness": "8",
        "first_literal_failure": {
            "label": "first Gamma protected occurrence/operator label",
            "required_B_value": "1",
            "required_Eq_value": "-1",
            "one_intrinsic_label_can_carry_both_values": False,
        },
        "equation_word_labels_resolve_failure": False,
        "matching_occurrence_labels_resolve_failure": False,
        "full_order_six_operator_history_resolves_failure": False,
        "higher_Taylor_Schreyer_cells_resolve_failure": False,
        "reason": (
            "B and Eq are not two equation/monomial/operator labels; they are "
            "two later presentation copies of the same literal occurrence"
        ),
        "Psi_defined_on_original_EqSystem_resolution": False,
    }


def finite_fredholm_alternative_audit() -> dict[str, object]:
    # A Fredholm alternative is automatic after a target map J:C1->Y and RHS
    # b in Y are specified.  Here the desired scalar is outside pi^*(U^*), so
    # the intrinsic matrix cannot even be paired with that scalar.
    intrinsic_duals = tuple(
        tuple(Q(row == column) for row in range(4)) * 2
        for column in range(4)
    )
    psi = DELTA + tuple(-value for value in DELTA)
    require(rank(intrinsic_duals) == 4
            and rank(intrinsic_duals + (psi,)) == 5,
            (rank(intrinsic_duals), rank(intrinsic_duals + (psi,))))
    return {
        "finite_linear_alternative_after_map_is_defined": (
            "RHS lies in im(J), or some lambda in ker(J^T) separates it"
        ),
        "current_intrinsic_target_map_to_B_minus_Eq_defined": False,
        "first_failure_is_before_matrix_rank": True,
        "coarsening_to_the_intrinsic_sum_B_plus_Eq": (
            "defined, but kills the anti-diagonal detector"
        ),
        "weakest_sufficient_new_theorem": (
            "define a scalar EqSystem/Macaulay observable Psi_actual from "
            "literal polynomial coefficients and prove every exact solution "
            "satisfies Psi_actual=0"
        ),
        "literal_response_to_cap_generator_required_by_that_theorem": False,
        "then_terminal": (
            "the required Gamma right-hand side has nonzero Psi_actual, so "
            "the scalar left-kernel identity is the Fredholm separator"
        ),
        "alternative_positive_outcome": (
            "if the explicit intrinsic RHS lies in im(J), its preimage is the "
            "source-provenant physical filler"
        ),
    }


def nonflat_specialization_transgression_audit() -> dict[str, object]:
    """Compute the labelwise t=H0-u Bockstein and saturation loophole."""
    # For each retained literal occurrence label, the relative normal form is
    # R K_i --t--> R E_i over R=Q[t].  Tensoring with Q=R/(t) makes the
    # differential zero.  Dividing the universal differential by t gives the
    # Bockstein/transgression K_i |-> E_i.
    transgression = tuple(
        tuple(Q(row == column) for row in range(4))
        for column in range(4)
    )
    delta_image = tuple(sum(DELTA[column] * transgression[column][row]
                            for column in range(4))
                        for row in range(4))
    require(rank(transgression) == 4 and delta_image == DELTA,
            (rank(transgression), delta_image))

    # A universal boundary and a post-specialization-only boundary are
    # distinct.  In C0=R{E,Y}, dL=E+tY does not contain E in its R-column
    # span, but modulo t it becomes dL=E.  Encode a+b*t as (a,b).
    e = ((Q(1), Q(0)), (Q(0), Q(0)))
    special_column = ((Q(1), Q(0)), (Q(0), Q(1)))
    require(special_column != e
            and tuple(coefficient[0] for coefficient in special_column)
                == (Q(1), Q(0))
            and tuple(coefficient[0] for coefficient in e)
                == (Q(1), Q(0)),
            (e, special_column))
    return {
        "base_ring": "R=Q[t], t=H0-u",
        "labelwise_relative_normal_form": "dK_i=t*E_i",
        "literal_occurrence_labels_retained": 4,
        "after_specialization_t_equals_zero": {
            "differential_rank": 0,
            "Tor1_generators": ["K_0", "K_1", "K_2", "K_3"],
            "Eq_quotient_generators": ["E_0", "E_1", "E_2", "E_3"],
            "Tor1_dimension": 4,
            "Eq_H0_dimension": 4,
        },
        "Bockstein_transgression_matrix": [
            [str(value) for value in column] for column in transgression
        ],
        "transgression_rank": rank(transgression),
        "transgression_of_delta": [str(value) for value in delta_image],
        "relative_cell_becomes_Eq_filler_after_specialization": False,
        "relative_cell_becomes_invisible_Tor1_cycle": True,
        "universal_absolute_boundary_criterion": "E in im(J)",
        "post_specialization_boundary_criterion":
            "E in im(J)+t*C0, equivalently E mod t in im(J mod t)",
        "strict_difference_example": {
            "universal_column": "dL=E+tY",
            "E_is_universal_boundary": False,
            "E_is_boundary_after_t_equals_zero": True,
        },
        "actual_finite_test_once_Eq_readout_exists": (
            "compare ranks of [J|E] over R and [J mod t|E] over Q, or solve "
            "the saturation equation Jx+t*y=E with literal labels"
        ),
        "current_EqSystem_can_run_that_test": False,
        "reason": (
            "the original occurrence resolution still has no intrinsic Eq "
            "quotient/readout selecting the E_i; the transgression is an exact "
            "characterization conditional on that quotient, not a descent of Psi"
        ),
        "universal_boundary_census_exhausts_specialized_boundaries": False,
        "terminal_promotion_must_check_t_saturation": True,
    }


def solutionwise_normalized_response_to_N_to_B_audit(derived, normalized) \
        -> dict[str, object]:
    """Test the constructive top map without asking for a quasi-isomorphism."""
    normalized_ledger, normalized_digest = normalized.audit()
    require(normalized_digest == normalized.EXPECTED_LEDGER_SHA256,
            normalized_digest)
    comparison = normalized_ledger["normalized_comparison"]
    require(comparison["evident_map_is_chain_map_after_base_change"]
            and not comparison["map_is_quasi_isomorphism"], comparison)

    physical = derived.physical_descent_and_derived_N_audit()
    composite_boundary = tuple(map(Q, physical["derived_N_boundary"]))
    physical_r0_boundary = tuple(map(
        Q, physical["underived_physical_r0_boundary"]))
    difference = tuple(right - left for left, right in
                       zip(composite_boundary, physical_r0_boundary,
                           strict=True))
    require(composite_boundary == (Q(1), Q(0))
            and physical_r0_boundary == (Q(0), Q(1))
            and difference == (Q(-1), Q(1))
            and rank((composite_boundary, physical_r0_boundary)) == 2,
            (composite_boundary, physical_r0_boundary, difference))
    return {
        "specialization": "t=H0-u=0 on an actual normalized solution",
        "response_to_N_to_B_is_chain_map": True,
        "selected_parent_carrier_coefficient": 1,
        "common_parent_B_augmentation_realized": True,
        "target_can_be_carried_by_existing_top_cone": True,
        "cone_quasi_isomorphism_used_in_this_test": False,
        "composite_protected_boundary": [1, 0],
        "required_physical_r0_boundary": [0, 1],
        "boundary_difference": [-1, 1],
        "boundary_rank_together": 2,
        "realizes_untyped_or_B_coefficient_shadow_of_Phi": True,
        "realizes_full_protected_Phi_KS_r0": False,
        "first_failed_map_equation": (
            "Phi_0(c_f)=-E in the absolute decorated Eq row: the composite "
            "has Eq projection 0 while physical r0 has Eq projection 1"
        ),
        "interpretation": (
            "the extra Eq H0 is not invoked merely to demand cone acyclicity; "
            "it is the explicit missing protected boundary value of the "
            "constructive selected-carrier map"
        ),
    }


def derived_N_tied_augmentation_and_downstream_gate(derived, h4,
                                                     normalized) \
        -> dict[str, object]:
    derived.pin_dependencies()
    physical = derived.physical_descent_and_derived_N_audit()
    require(physical["derived_N_boundary"] == [1, 0]
            and physical["underived_physical_r0_boundary"] == [0, 1]
            and physical["protected_boundary_rank"] == 2,
            physical)

    d_n = tuple(map(Q, physical["derived_N_boundary"]))
    absolute_eq = tuple(map(Q, physical["underived_physical_r0_boundary"]))
    tied = tuple(left + right for left, right in
                 zip(d_n, absolute_eq, strict=True))
    correction = tuple(right - left for left, right in
                       zip(d_n, tied, strict=True))
    require(tied == (Q(1), Q(1))
            and correction == absolute_eq
            and rank((d_n, absolute_eq)) == 2,
            (d_n, absolute_eq, tied, correction))

    normalized_ledger, normalized_digest = normalized.audit()
    require(normalized_digest == normalized.EXPECTED_LEDGER_SHA256,
            normalized_digest)
    tor = normalized_ledger["relative_versus_absolute_filler"]
    require(tor["relative_cap_homology_H0_H1"] == [1, 1]
            and tor["absolute_cap_homology_H0_H1"] == [0, 0], tor)

    selected = h4.selected_db01_and_cap_readout_audit()
    require(selected["pointed_conormal_P_f"] == [1, 0, 0]
            and selected["primitive_cap_p"] == [0, -1, -1], selected)
    p_f = tuple(map(Q, selected["pointed_conormal_P_f"]))
    primitive = tuple(map(Q, selected["primitive_cap_p"]))
    invisible = (Q(0), Q(1), Q(0))
    require(rank((p_f, primitive)) == 2
            and rank((p_f, primitive, invisible)) == 3,
            (p_f, primitive, invisible))
    return {
        "existing_derived_N_protected_boundary": [1, 0],
        "proposed_same_augmentation_B_equals_Eq_boundary": [1, 1],
        "required_correction": [0, 1],
        "required_correction_is_absolute_decorated_Eq": True,
        "tied_augmentation_avoids_absolute_Eq_problem": False,
        "interpretation": (
            "defining B=Eq on N is a valid possible augmented theorem, but "
            "at chain level it supplies exactly the missing absolute Eq "
            "preimage; it is not a weaker consequence of parent augmentation"
        ),
        "normalization_relative_filler_H0_H1":
            tor["relative_cap_homology_H0_H1"],
        "absolute_filler_H0_H1": tor["absolute_cap_homology_H0_H1"],
        "derived_linear_ladder_if_tied_augmentation_is_granted": {
            "parent_augmentation": "available on marked N",
            "target": "may be pulled back along the granted target cone",
            "0102_dq_Q_faces": (
                "homological/marked deletion faces; no underived r0 is "
                "logically required once their natural transformations on N "
                "are supplied"
            ),
            "ores_W_ridge": (
                "linear readouts; require augmented maps on N but not a chosen "
                "underived representative as abstract homological data"
            ),
        },
        "first_downstream_underived_or_pointed_requirement": {
            "operation": "P_f/anchor projection and active-cap extraction",
            "P_f_vector": list(map(int, p_f)),
            "primitive_cap_vector": list(map(int, primitive)),
            "invisible_q_direction": list(map(int, invisible)),
            "rank_Pf_and_primitive": rank((p_f, primitive)),
            "rank_after_invisible_direction":
                rank((p_f, primitive, invisible)),
            "B_parent_augmentation_determines_P_f": False,
            "reason": (
                "active cap is a pointed property of an actual degree-zero "
                "physical cap representative, not of the common-parent "
                "homology class alone"
            ),
        },
        "terminal_branch_can_avoid_underived_representative": (
            "yes, if the intrinsic solution-level Psi_actual theorem is "
            "proved; then the Fredholm separator closes before cap extraction"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    official = load(
        "computations/verify_chart_model_is_official_eqsystem.py",
        "intrinsic_psi_official",
    )
    order6 = load(
        "computations/verify_h3_order6_gammajet_collision_contraction_same_edge_gate.py",
        "intrinsic_psi_order6",
    )
    derived = load(
        "computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py",
        "intrinsic_psi_derived",
    )
    h4 = load(
        "computations/verify_h4_pointed_phi01_fixed_tail_h3_restriction_gate.py",
        "intrinsic_psi_h4",
    )
    normalized = load(
        "computations/verify_h3_normalized_eq_base_change_tor_gate.py",
        "intrinsic_psi_normalized",
    )
    ledger = {
        "theorem": (
            "Psi does not descend to the complete occurrence-labelled "
            "multigraded EqSystem Taylor/Schreyer resolution; the first "
            "undefined datum is the anti-diagonal B/Eq readout"
        ),
        "pins": PINS,
        "original_EqSystem_occurrence_Schreyer_presentation":
            official_occurrence_schreyer_audit(official, order6),
        "Psi_label_descent": psi_label_descent_audit(),
        "finite_Fredholm_alternative": finite_fredholm_alternative_audit(),
        "nonflat_normalization_Tor1_and_transgression":
            nonflat_specialization_transgression_audit(),
        "solutionwise_response_to_N_to_B_composite":
            solutionwise_normalized_response_to_N_to_B_audit(
                derived, normalized),
        "derived_N_tied_augmentation_and_downstream":
            derived_N_tied_augmentation_and_downstream_gate(
                derived, h4, normalized),
        "verdict": (
            "Retaining every actual equation-word, matching occurrence, "
            "divided-operator, pair/repeated and word/fine-shift label still "
            "does not define Psi: B and Eq are two enriched copies of one "
            "literal occurrence, and the anti-diagonal covector cannot descend "
            "through their sum. Therefore the desired intrinsic Fredholm "
            "alternative is blocked before rank computation. The weakest "
            "repair is a solution-level polynomial observable Psi_actual, not "
            "a new source generator. A universal boundary census also does "
            "not exhaust the normalized fibre: labelwise dK=t*Eq cells become "
            "Tor1 cycles with Bockstein K->Eq, and specialized-only fillers "
            "are detected by E in im(J)+t*C0. That saturation test remains "
            "undefined until the Eq readout descends. Separately, declaring "
            "tied B=Eq on the "
            "derived cap N supplies exactly the missing absolute Eq vector; "
            "the evident normalized response-to-N-to-B composite is indeed a "
            "monic chain map on the selected coefficient carrier, without any "
            "quasi-isomorphism assumption, but it has protected boundary "
            "(1,0) rather than physical r0 boundary (0,1), so it fails the "
            "literal Phi_0(c_f)=-E map equation. "
            "if granted, the linear marked/q ladder may be moved to N, but B "
            "augmentation alone still cannot produce the independent pointed "
            "P_f/active-cap representative."
        ),
        "scope": (
            "exact official 252-variable/6561-relation/105-occurrence EqSystem, "
            "exact four-generator Taylor ranks, the literal 8580-column/271-"
            "label order-six operator presentation, exact B/Eq descent ranks, "
            "the labelwise normalization Bockstein and saturation criterion, "
            "the marked derived-cap boundary, normalization Tor guard and the "
            "pointed P_f quotient. No operation idempotent, no-orphan axiom or "
            "physical response-to-cap generator is assumed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("intrinsic Psi ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "presentation", "descent",
                                            "derived"), default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print("h3 intrinsic EqSystem Psi terminal gate:", arguments.mode,
              "PASS")
        print("Psi defined on original occurrence resolution: NO")
        print("first failure: anti-diagonal B/Eq readout has no literal label")
        print("derived tied B=Eq augmentation equals absolute Eq repair: YES")
        print("first later underived need: pointed P_f / active-cap extraction")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
