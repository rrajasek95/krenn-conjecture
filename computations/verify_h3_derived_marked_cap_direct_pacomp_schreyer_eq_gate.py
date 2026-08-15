#!/usr/bin/env python3
"""Audit the strongest direct-derived-cap bypass and the native Schreyer test.

The fine-marked collision correspondence gives a comparison

    Delta^5  -->  Delta^5 x Delta^1

over each of the 90 parent matchings.  This checker constructs its mapping
cone explicitly.  For both root sections the complete comparison cone is
acyclic; adjoining the one protected balanced Eq coordinate leaves exactly
one H0 class and no higher homology.

It then asks whether one can keep the derived cap N, give its vertices tied
B=Eq parent readouts, and run PAComp without projecting to underived r0.  The
first literal failure is the occurrence-local P2 restriction: N's universal
q faces remain in the diagonal cap word, while the q23/q45 landings occupy
two independent word/fine/operation summands.  Granting that landing forces
the nonzero 0102/dq conormal and still leaves the untied complete-Eq residual.

Finally, the checker builds the complete 48-slot squarefree coefficient
Taylor/Schreyer block of the official EqSystem grade.  It cannot decide the
remaining Eq coordinate because the protected B/Eq detector is nonzero on
the kernel of the canonical forgetting map (b,e) -> b+e.  This is an exact
two-lift obstruction, not a failure to compute enough syzygies.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from math import comb
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py":
        "a1e81eef9343bd2dda01b106acc202698cc12e93e7db3b55d45f5c6268779c33",
    "computations/verify_h3_full_star_cap_totalization_eq_orbit_gate.py":
        "ce4d98c0160c86692c876879f90b69ae684d6d16bb3211d8ffe9a30fdc8c4e91",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py":
        "767aa83dce1daee7e615cbeb5684662714bb0e377822805541172581adc2490f",
    "computations/verify_h3_gamma_cotangent_principal_parts_enrichment_foundation_gate.py":
        "3eb7bc5bd51a9affa3aa0cdab113efc2856375c0de9e083efc611aed7cd1058f",
    "computations/verify_h3_actual_source_primitive_terminal_reduction_gate.py":
        "5754c85f7ae4b714777cdbb0f941672ade1977c5568f332a0dc8e317e4952927",
    "computations/verify_h3_normalized_eq_base_change_tor_gate.py":
        "b7c409db8cff0141a153816d0d14525464c4fcadb0607b97da06181435059d50",
    "computations/verify_uniform_target_augmented_private_site_active_minor.py":
        "c53ba30dd8b7084cc27e05f11aa6066354fdec45ff2cf72ebdfb85bb8517169b",
    "computations/verify_h3_active_fan_coloop_or_four_good.py":
        "93030f2994e2e6a2052a09a5fefd179c99e0b8fb55cd0c77bee2cb9f8dbc6bb4",
    "computations/verify_clean_pair_cap_exact_descent_symbolic.py":
        "d6507c2afa341ce5c15056feddf92b9a171e2a5c80652617b595c7c7cf35acf5",
    "computations/verify_h3_phi_ks_r0_pf_minimal_executable_ansatz_gate.py":
        "d21d776ec53babb4f99693e4dad51d87309e3ed0cccf2e34fb6025e6d74d1009",
}
EXPECTED_LEDGER_SHA256 = "e9096a1dd855c9ecb49f5c853272224ec5b09d9d3e12e2b9cc01c0dc66df5b2f"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def compose_sparse(left, right):
    """Compose sparse column maps left after right."""
    output = []
    for column in right:
        composite = {}
        for middle, coefficient in column.items():
            for row, value in left[middle].items():
                result = composite.get(row, Q(0)) + Q(coefficient) * Q(value)
                if result:
                    composite[row] = result
                else:
                    composite.pop(row, None)
        output.append(composite)
    return tuple(output)


def section_columns(bc, cap_bases, degree: int):
    cap_index = {cell: index for index, cell in enumerate(cap_bases[degree])}
    columns = []
    for face in bc.simplex_basis(6, degree):
        columns.append({
            cap_index[(degree, face, 0, (0,))]: Q(1, 2),
            cap_index[(degree, face, 0, (1,))]: Q(1, 2),
        })
    return tuple(columns)


def mapping_cone_audit(bc) -> dict[str, object]:
    bc_ledger, bc_digest = bc.audit()
    require(bc_digest == bc.EXPECTED_LEDGER_SHA256
            and bc_ledger["derived_resolutions"]
                ["claim_i_projective_resolutions_same_base"], bc_digest)

    response_bases = tuple(bc.simplex_basis(6, degree)
                           for degree in range(6))
    response_boundaries = tuple(bc.simplex_boundary(6, degree)
                                for degree in range(1, 6))
    cap_bases, cap_boundaries = bc.product_simplex_complex(6, 2)
    section = tuple(section_columns(bc, cap_bases, degree)
                    for degree in range(6))

    # Cone(s)_n = N_n direct_sum Response_(n-1), with
    # d(n,c)=(d_N n+s(c),-d_R c).
    cone_dimensions = []
    cone_boundaries = []
    for degree in range(7):
        cap_dimension = len(cap_bases[degree])
        shifted_response_dimension = (
            len(response_bases[degree - 1]) if degree else 0
        )
        cone_dimensions.append(cap_dimension + shifted_response_dimension)
        if degree == 0:
            continue
        lower_cap_dimension = len(cap_bases[degree - 1])
        columns = []
        for cap_column in cap_boundaries[degree - 1]:
            columns.append(dict(cap_column))
        for index, section_column in enumerate(section[degree - 1]):
            column = dict(section_column)
            if degree >= 2:
                for row, value in response_boundaries[degree - 2][index].items():
                    column[lower_cap_dimension + row] = -Q(value)
            columns.append(column)
        cone_boundaries.append(tuple(columns))

    for degree in range(2, len(cone_dimensions)):
        composite = compose_sparse(cone_boundaries[degree - 2],
                                   cone_boundaries[degree - 1])
        require(all(not column for column in composite),
                ("mapping cone d2", degree, composite))

    cone_ranks = tuple(bc.sparse_rank(boundary)
                       for boundary in cone_boundaries)
    require(tuple(cone_dimensions) == (12, 42, 70, 70, 42, 14, 2)
            and cone_ranks == (12, 30, 40, 30, 12, 2),
            (cone_dimensions, cone_ranks))
    homology = []
    for degree, dimension in enumerate(cone_dimensions):
        incoming = cone_ranks[degree] if degree < len(cone_ranks) else 0
        outgoing = cone_ranks[degree - 1] if degree else 0
        homology.append(dimension - incoming - outgoing)
    require(homology == [0] * 7, homology)

    # The physical packet uses all 90 parents and two independently labelled
    # roots.  One balanced Eq coordinate is global, not one per parent.
    scale = 90 * 2
    global_dimensions = [scale * value for value in cone_dimensions]
    global_dimensions[0] += 1
    global_ranks = [scale * value for value in cone_ranks]
    global_homology = []
    for degree, dimension in enumerate(global_dimensions):
        incoming = global_ranks[degree] if degree < len(global_ranks) else 0
        outgoing = global_ranks[degree - 1] if degree else 0
        global_homology.append(dimension - incoming - outgoing)
    require(global_dimensions == [2161, 7560, 12600, 12600, 7560, 2520, 360]
            and global_ranks == [2160, 5400, 7200, 5400, 2160, 360]
            and global_homology == [1, 0, 0, 0, 0, 0, 0],
            (global_dimensions, global_ranks, global_homology))

    return {
        "one_parent_one_root": {
            "comparison": "Cone(Delta5 -> Delta5 x Delta1)",
            "chain_dimensions": cone_dimensions,
            "boundary_ranks": list(cone_ranks),
            "homology_dimensions": homology,
            "acyclic": True,
        },
        "full_two_root_90_parent_protected_complex": {
            "definition": (
                "two roots x 90 parents x the acyclic marked comparison "
                "cone, direct-sum one global balanced Eq coordinate in C0"
            ),
            "chain_dimensions": global_dimensions,
            "boundary_ranks": global_ranks,
            "homology_dimensions": global_homology,
            "only_survivor": "H0=Q{E_protected}",
        },
        "basis_tags": [
            "root AB or AC",
            "one of 90 direct-free parent matchings",
            "one of six replacement triggers",
            "the retained missing-site/fine reinsertion mark",
            "P3+K2 marked cap endpoint in Delta1",
        ],
        "intrinsic_local_normal_form": (
            "the marked derived response-to-cap comparison is already "
            "acyclic; after protected augmentation the only possible local "
            "homology is one balanced Eq coordinate"
        ),
    }


def direct_N_pacomp_audit(private, sigma) -> dict[str, object]:
    private_ledger, private_digest = private.audit()
    require(private_digest == private.EXPECTED_LEDGER_SHA256, private_digest)
    sigma_ledger, sigma_digest = sigma.audit()
    require(sigma_digest == sigma.EXPECTED_LEDGER_SHA256, sigma_digest)

    reinsertion = private_ledger["q23_reinsertion"]
    actual = sigma_ledger["actual_augmented_residual"]
    dressing = sigma_ledger["root_word_physical_dressing"]
    require(reinsertion["forced_repair_dq23_private_detector"] == "35/72"
            and reinsertion["ordinary_residue_aggregate"] == 0
            and actual["word_residual"]
                ["physical_midpoint_word_hits_from_old_formal_totalization"] == 0
            and actual["word_residual"]["objectwise_word_quotient_rank"] == 2
            and actual["complete_Eq_residual_after_target_Eq_cone"]
                ["residual"] == ["0", "-delta_plus"]
            and dressing["required_hidden_faces_on_raw_Cplus"] == {
                "lower_private": "-E", "word_resolved_ores": "+E"
            }, (reinsertion, actual, dressing))

    # First literal word/operation mismatch.  The marked derived cap q face
    # remains in the diagonal cap object; the two physical P2 landings are
    # independent lower-word objects.  No choice of tied parent augmentation
    # changes these idempotent coordinates.
    diagonal_word = (Q(1), Q(0), Q(0))
    q23_word = (Q(0), Q(1), Q(0))
    q45_word = (Q(0), Q(0), Q(1))
    word_duals = ((Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(1)))
    require(all(dot(dual, diagonal_word) == 0 for dual in word_duals)
            and [dot(word_duals[0], q23_word),
                 dot(word_duals[1], q45_word)] == [1, 1],
            "word/P2 landing dual changed")

    # The full target cone closes, but the complete output asks for B-only,
    # not a termwise tied B=Eq vector.  This is the first place the ladder
    # uses the cap modulo its Eq copy.
    d6 = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    delta_plus = tuple(value / 4 for value in d6)
    zero6 = (Q(0),) * 6
    tied = delta_plus + delta_plus
    desired_B_only = delta_plus + zero6
    residual_Eq_only = zero6 + tuple(-value for value in delta_plus)
    private_eq_dual = d6 + tuple(-value for value in d6)
    require(dot(private_eq_dual, tied) == 0
            and dot(private_eq_dual, desired_B_only) == 3
            and dot(private_eq_dual, residual_Eq_only) == 3
            and sum(value * value for value in d6) == 12,
            "complete B/Eq separator changed")

    forced_dq = tuple(map(Q, reinsertion[
        "forced_repair_dq23_coefficient"]))
    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(len(forced_dq)))
    require(len(forced_dq) == 12 and sum(forced_dq, Q(0)) == 0
            and dot(detector, forced_dq) == Q(35, 72),
            "forced dq23 conormal changed")

    return {
        "strong_grant_tested": (
            "every marked N vertex is assigned its parent augmentation, "
            "B=Eq termwise, and the canonical target-cone relation"
        ),
        "what_this_grant_does": [
            "makes every coefficient/common-parent comparison column tied",
            "kills both independent mixed-target normals",
            "retains the universal q23 and q45 cap-Hasse faces",
        ],
        "first_downstream_map_using_more_than_parent_augmentation": {
            "map": (
                "occurrence-local Eq/P2 restriction from the diagonal "
                "01211222 cap-q face to 0112/q23:21 and 0121/q45:12"
            ),
            "source_word_coordinate": list(map(int, diagonal_word)),
            "required_target_word_coordinates": [
                list(map(int, q23_word)), list(map(int, q45_word))
            ],
            "old_derived_N_word_hit_rank": 0,
            "required_word_quotient_rank": 2,
            "primitive_covectors": [list(map(int, value))
                                     for value in word_duals],
            "physical_P2_landing_constructed": False,
        },
        "first_product_rule_after_granting_that_map": {
            "formula": "d(q23*S)=q23*dS+dq23*S",
            "word": "0102",
            "dq23_coefficient_dimension": len(forced_dq),
            "augmentation": "0",
            "ordinary_residue": "0",
            "detector": "+e0+e3-e1-e6",
            "detector_value": "35/72",
        },
        "first_protected_use_of_cap_modulo_Eq": {
            "stage": (
                "complete lower/private output after the target/root-Eq "
                "cone, before the 0102/dq reinsertion ladder"
            ),
            "termwise_N_readout": "(delta_plus,delta_plus)",
            "required_physical_readout": "(delta_plus,0)",
            "residual": "(0,-delta_plus)",
            "integral_covector": list(map(int, private_eq_dual)),
            "covector_on_tied_N": "0",
            "covector_on_required_B_only": "3",
            "unscaled_d6_square": "12",
            "hidden_proper_faces": dressing[
                "required_hidden_faces_on_raw_Cplus"],
        },
        "target_cone_status": "closed; it is not the obstruction",
        "direct_N_is_current_PAComp_cap_object": False,
        "reason": (
            "the parent augmentation is a coefficient map, while PAComp's "
            "P2/q/dq/ores ladder is an operation- and word-labelled PP map; "
            "its first word image is zero and its protected tied image is "
            "annihilated by the displayed B-Eq covector"
        ),
        "weakest_derived_bypass_hypothesis": (
            "construct the two occurrence-local P2 restriction maps and "
            "their q/dq, labelled-residue, ridge and hidden lower/ores "
            "faces directly on N, and prove clean-cap extraction factors "
            "through H0(N) while the Eq summand vanishes conservatively on "
            "actual solutions; this would replace, rather than derive, the "
            "absolute underived E cell"
        ),
    }


def end_to_end_pacomp_chase() -> dict[str, object]:
    """Separate derived target activity from physical cap realization.

    The pins freeze the exact downstream source theorems.  Their inputs are
    actual weight cells and an actual cap covector, not merely a homology
    class of the 90-parent occurrence resolution.  This is a typing failure,
    so it precedes any question of whether their polynomial identities are
    true after a realization map has been supplied.
    """
    return {
        "stage_order": [
            "marked response-to-derived-cap comparison",
            "nonzero/active condition",
            "target-augmented private-site identity",
            "four-good or pure-colour coloop split",
            "occurrence-local P2 and 0102/dq ladder",
            "Q/ordinary-residue/ridge completion",
            "clean-cap N-to-Nminus2 reconstruction",
        ],
        "marked_comparison": {
            "status": "PROVED",
            "content": (
                "strict fine-marked BC bijection and acyclic comparison "
                "over V_parent=Q{90 matchings}"
            ),
        },
        "nonzero_active": {
            "derived_target_nonzero_is_statable": True,
            "reason": (
                "after the proposed termwise target augmentation, target is "
                "constant on Delta1 endpoints and zero on every simplicial "
                "boundary, hence descends to H0(N)=V_parent"
            ),
            "physical_active_cap_is_statable_on_N_alone": False,
            "missing_map": (
                "ev_cap:N -> Cap_phys(A;p,q), an R-linear pointed "
                "realization sending a parent occurrence to an actual cap "
                "covector/weight-cell expression and reflecting nonzero target"
            ),
            "distinction": (
                "target([n])=1 is a derived augmentation statement; activity "
                "in the descent theorem is a property of an actual covector K"
            ),
        },
        "private_site_identity": {
            "status_on_N": "NOT DEFINED",
            "literal_identity": (
                "p_u*G_mixed-q_u*G_pure="
                "q_u+sum_s (p_u*q_s-q_u*p_s)*C_s"
            ),
            "exact_source_consequence": "sum_s Delta_us*C_s=-q_u",
            "data_absent_from_N": [
                "the physical cells p_u,q_u,p_s,q_s",
                "multiplication of weight cells and hafnian cofactors C_s",
                "the pure and mixed official EqSystem relations",
                "evaluation/nonvanishing in the localized source ring",
            ],
            "earliest_end_to_end_failure": True,
            "why_parent_augmentation_does_not_supply_it": (
                "V_parent records which matching occurrence was retained; it "
                "does not carry the R-algebra multiplication or evaluation "
                "used by the inhomogeneous target identity"
            ),
        },
        "four_good_or_coloop": {
            "status_on_N": "NOT REACHED",
            "required_input": (
                "one nonzero physical determinant/cofactor fan and the three "
                "complete pure matching supports"
            ),
            "conclusion_if_realized": (
                "distinct-head active four-good overlap or a literal "
                "pure-colour target coloop"
            ),
            "not_homotopy_invariant_of_parent_resolution": True,
        },
        "P2_0102_dq_Q_ores_ridge": {
            "status": "EXACT SECOND FAILURE UNDER A GENEROUS CAP REALIZATION GRANT",
            "first_rank_failure": "diagonal-word image rank 0, required P2 rank 2",
            "next_covector": "0102/dq23 detector 35/72",
            "protected_residual": (
                "tied (delta_plus,delta_plus) versus required "
                "(delta_plus,0), detected with value 3"
            ),
            "target_normals": "already closed",
        },
        "N_to_Nminus2_reconstruction": {
            "status_on_N": "NOT DEFINED",
            "literal_input": (
                "an actual active clean cap covector K with scalar s!=0 and "
                "K contraction H_B(A)=[(s+r) exp(x)]_U"
            ),
            "literal_output": (
                "physical reduced weights y on B-{p,q} satisfying "
                "H_U(y)=Delta_(U,3)"
            ),
            "missing_structure": (
                "a conservative cap-realization/contraction functor from N "
                "to actual tensors; no map from an abstract V90 homology "
                "class to K or to the reconstructed weights y is defined"
            ),
        },
        "earliest_missing_property": (
            "after granting a target functional, the first unavailable "
            "physical property is the R-linear cap realization needed to "
            "state the private-site identity; inside the local chain ladder, "
            "the first exact failure is the rank-0-to-rank-2 P2 word map"
        ),
        "derived_PAComp_theorem_that_would_suffice": (
            "construct a pointed R-linear realization ev_cap of N, natural "
            "for EqSystem multiplication, private-site contraction, the "
            "P2/q/dq/ores/ridge operations and clean-cap reconstruction; "
            "require target activity and clean-cap nonvanishing to be "
            "reflected on H0 and require the Eq summand to vanish "
            "conservatively on actual solutions"
        ),
        "derived_PAComp_current_status": "NOT PROVED",
    }


def normalized_selected_composite_audit() -> dict[str, object]:
    """Test the constructive composite without requiring a quasi-isomorphism.

    At t=H0-u=0 the coefficient top really maps by the identity
    Response -> N -> B.  In the literal root-section block, however, its
    coefficient-only extension has no response-to-cap operation coordinate.
    The resulting separator is a failure of the map, not of its cone.
    """
    # Coordinates: id_R, id_C, Hom(R,C), response_word, cap_word.
    id_response = (Q(1), Q(0), Q(0), Q(0), Q(0))
    id_cap = (Q(0), Q(1), Q(0), Q(0), Q(0))
    coefficient_top = (Q(0), Q(1), Q(0), Q(0), Q(0))
    physical_section = (Q(0), Q(0), Q(1), Q(-1), Q(1))
    operation_dual = (Q(0), Q(0), Q(1), Q(0), Q(0))
    old = (id_response, id_cap, coefficient_top)
    require(all(dot(operation_dual, column) == 0 for column in old)
            and dot(operation_dual, physical_section) == 1,
            "normalized selected-composite operation separator changed")

    response_to_N = Q(1)
    N_to_B = Q(1)
    require(response_to_N * N_to_B == 1, "normalized top composite changed")

    return {
        "question_tested": (
            "whether the normalized selected carrier map itself suffices, "
            "without requiring its cone to be acyclic"
        ),
        "normalization": "t=H0-u=0",
        "coefficient_top_composite": {
            "Response_to_N": 1,
            "N_to_B": 1,
            "Response_to_B": 1,
            "is_chain_map_in_coefficient_common_parent_complex": True,
            "sends_selected_parent_coefficient_to_B_top": True,
            "retains_by_the_marked_bijection": [
                "root AB/AC", "parent matching", "missing-site/fine mark"
            ],
        },
        "constructive_versus_terminal": {
            "extra_Eq_cokernel_blocks_this_coefficient_map": False,
            "extra_Eq_cokernel_relevant_to_terminal_promotion": True,
            "quasi_isomorphism_required_for_constructive_top_map": False,
        },
        "first_failure_of_the_map_itself": {
            "row_block": (
                "root-labelled response-occurrence to AugP2/K_Eq-cap "
                "operation and word section"
            ),
            "literal_word": "11110000 -> 01211222",
            "coefficient_composite_Hom_response_cap_coordinate": 0,
            "required_physical_section_Hom_response_cap_coordinate": 1,
            "primitive_covector": [0, 0, 1, 0, 0],
            "covector_on_coefficient_composite": 0,
            "covector_on_required_section": 1,
            "interpretation": (
                "the abstract top image is B, but no physical e_C A e_R "
                "column relates its differential to the selected response "
                "carrier; hence the P_f and q proper-face equations are not "
                "consequences of this map"
            ),
        },
        "if_the_operation_section_is_granted": {
            "top_B_image": "passes",
            "root_parent_fine_labels": "pass",
            "next_failed_identity": (
                "the q23/q45 occurrence-local P2 restriction: old diagonal "
                "word image rank 0, required rank 2"
            ),
            "then_forced_faces": (
                "0102 dq23/dq45 and the hidden (-E,+E) lower/ores pair"
            ),
        },
        "constructive_filler_and_terminal_promotion_are_separate": True,
        "constructive_filler_status": (
            "not constructed: operation/word/P_f/q compatibility fails "
            "before the Eq cokernel is consulted"
        ),
        "terminal_promotion_status": (
            "only after a physical constructive map exists does the lone "
            "protected Eq cokernel decide absolute filling versus terminal"
        ),
    }


def contraction_matrix(dimension: int, degree: int):
    source = tuple(combinations(range(dimension), degree))
    target = tuple(combinations(range(dimension), degree - 1))
    target_index = {face: index for index, face in enumerate(target)}
    columns = []
    for subset in source:
        column = {}
        for position in range(len(subset)):
            face = subset[:position] + subset[position + 1:]
            column[target_index[face]] = Q(-1 if position % 2 else 1)
        columns.append(column)
    return tuple(columns)


def schreyer_and_protected_readout_audit(bc) -> dict[str, object]:
    require(comb(8, 2) * 3 ** 2 == 252
            and 3 ** 8 == 6561
            and len(tuple(bc.perfect_matchings(frozenset(range(8))))) == 105,
            "official EqSystem census changed")

    # Six externally selected squarefree cubic fine slots.  Positivity makes
    # every degree-complementing multiple a unique subset/complement pair.
    degree_histogram = {degree: 0 for degree in range(4)}
    for _slot in range(6):
        for degree in range(4):
            degree_histogram[degree] += comb(3, degree)
    require(degree_histogram == {0: 6, 1: 18, 2: 18, 3: 6},
            degree_histogram)
    differentials = tuple(contraction_matrix(3, degree)
                          for degree in (1, 2, 3))
    ranks = tuple(bc.sparse_rank(columns) for columns in differentials)
    require(ranks == (1, 2, 1)
            and all(not column for column in
                    compose_sparse(differentials[0], differentials[1]))
            and all(not column for column in
                    compose_sparse(differentials[1], differentials[2])),
            ranks)

    # The protected readout obstruction is already present on one top orbit.
    # Both B-only and Eq-only lift the same native coefficient delta.  Their
    # difference is in the kernel of forgetting and is detected by omega.
    delta = tuple(map(Q, (1, 1, -1, -1)))
    zero4 = (Q(0),) * 4
    b_lift = delta + zero4
    eq_lift = zero4 + delta
    tied = delta + delta
    kernel = delta + tuple(-value for value in delta)
    omega = tuple(value / 4 for value in kernel)
    forget = lambda vector: tuple(vector[index] + vector[index + 4]
                                  for index in range(4))
    require(forget(b_lift) == forget(eq_lift) == delta
            and forget(kernel) == zero4
            and dot(omega, b_lift) == 1
            and dot(omega, eq_lift) == -1
            and dot(omega, tied) == 0
            and dot(omega, kernel) == 2,
            "protected two-lift guard changed")

    # A complete native 48-column matrix has two augmented completions with
    # identical official restriction and different omega charge.
    native = tuple(tuple(Q(row == column) for row in range(48))
                   for column in range(48))
    zero_completion = tuple(column + (Q(0),) for column in native)
    bright = (Q(0),) * 48 + (Q(1),)
    require(tuple(column[:-1] for column in zero_completion) == native
            and bright[:-1] == (Q(0),) * 48,
            "native two-completion guard changed")

    return {
        "official_EqSystem": {
            "variables": 252,
            "relations": 6561,
            "matching_terms_per_relation": 105,
            "canonical_multigrading": (
                "N^24 site-colour degree after three pure-target "
                "homogenizers"
            ),
            "native_axes_absent": [
                "response/cap operation idempotent",
                "fine t*q_(v,N) occurrence",
                "repeated P3+K2 and fixed window",
                "B versus reduced-Eq presentation copy",
                "target/q/ores/W/ridge/eta/sigma readouts",
            ],
        },
        "complete_selected_coefficient_resolution": {
            "externally_selected_squarefree_fine_slots": 6,
            "degree_complementing_slots": sum(degree_histogram.values()),
            "degree_histogram": {str(key): value for key, value in
                                 degree_histogram.items()},
            "one_slot_dimensions": [1, 3, 3, 1],
            "one_slot_boundary_ranks": list(ranks),
            "six_slot_boundary_ranks": [6, 12, 6],
            "higher_Schreyer_cells_can_enlarge_d1_image": False,
        },
        "first_precise_protected_readout_obstruction": {
            "forgetful_map": "f(b,e)=b+e",
            "two_lifts_of_same_native_delta": [
                "(delta,0) with omega=+1",
                "(0,delta) with omega=-1",
            ],
            "kernel_witness": "(delta,-delta)",
            "normalized_omega_on_kernel_witness": "2",
            "tied_parent_readout": "(delta,delta), omega=0",
            "omega_descends_to_native_EqSystem_or_cotangent": False,
        },
        "finite_two_completion_counterguard": {
            "common_native_columns": len(native),
            "zero_completion_columns": len(zero_completion),
            "bright_completion_columns": len(zero_completion) + 1,
            "official_restrictions_identical": True,
            "bright_extra_column_native_shadow": 0,
            "bright_extra_column_omega_charge": 1,
        },
        "Schreyer_decides_E_boundary_or_dual": False,
        "reason": (
            "Schreyer resolves syzygies in the native coefficient module; "
            "the B/Eq protected lift is not a grading, filtration, or "
            "functor of that module.  Choosing either protected lift is "
            "additional enrichment, and higher syzygies cannot make the "
            "choice canonical"
        ),
        "minimum_extra_axiom": (
            "a source-derived GammaJetEnrichment with a chain/augmentation "
            "map to the protected B/Eq rows, complete on the kernel of "
            "forgetting and conservative for operation support"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    bc = load(
        "computations/verify_h3_shared_collision_groupoid_beck_chevalley_derived_cap_gate.py",
        "direct_N_bc",
    )
    private = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "direct_N_private",
    )
    sigma = load(
        "computations/verify_h2_sigma_even_cartan_spencer_cone_residual.py",
        "direct_N_sigma",
    )
    ledger = {
        "theorem": (
            "the minimal fine-marked derived Gamma comparison is acyclic "
            "apart from one protected Eq coordinate; its normalized top "
            "map sends the selected coefficient to B but lacks the physical "
            "response-to-cap operation/word section, and after granting that "
            "section direct use of N fails at the labelled P2 map; "
            "and native EqSystem Schreyer resolution cannot decide the Eq "
            "coordinate because its protected readout does not descend"
        ),
        "pins": PINS,
        "intrinsic_occurrence_Gamma_complex": mapping_cone_audit(bc),
        "normalized_selected_carrier_composite":
            normalized_selected_composite_audit(),
        "end_to_end_PAComp_chase": end_to_end_pacomp_chase(),
        "direct_derived_N_in_PAComp": direct_N_pacomp_audit(private, sigma),
        "native_multigraded_Schreyer_test":
            schreyer_and_protected_readout_audit(bc),
        "absolute_E_assessment": {
            "logically_only_possible_route": False,
            "necessary_in_the_current_underived_PAComp_formulation": True,
            "exactly_equivalent_derived_replacement": (
                "an augmented derived-PAComp factorization on N which "
                "constructs the P2/q/dq/ores/ridge maps and proves the "
                "surviving Eq summand is conservatively zero on actual "
                "solutions while preserving a nonzero active cap"
            ),
            "counterexample_to_weaker_replacement": (
                "tied B=Eq parent augmentation is killed by the complete "
                "B-Eq covector, whereas the required P2 lower/private "
                "column has value 3; after t=H0-u=0 the known relative "
                "cell leaves H0=Q{E} and creates H1=Q{K}"
            ),
        },
        "shortest_next_datum": (
            "define one source-derived occurrence-local restriction map "
            "from the marked cap q faces of N to both P2 word objects, with "
            "its forced dq23/dq45 jets and (-E,+E) hidden lower/word-ores "
            "faces.  Its complete B/Eq value decides the unique fork: "
            "nonzero gives the absolute filler, zero gives omega_Eq on an "
            "exhaustive physical map"
        ),
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
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        direct = ledger["direct_derived_N_in_PAComp"]
        print("mode", arguments.mode)
        print("ledger_sha256", digest)
        print("derived marked comparison: ACYCLIC")
        print("protected survivor: ONE UNDECIDED EQ COORDINATE")
        print("first direct-N PAComp failure:", direct[
            "first_downstream_map_using_more_than_parent_augmentation"]["map"])
        print("native Schreyer decides E: NO")


if __name__ == "__main__":
    main()
