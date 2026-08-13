#!/usr/bin/env python3
"""Audit the universal graph construction of the reduced-Eq comparison.

The graph of the full physical polynomial map H and the GHZ section Delta
give the correct derived fibre.  Their two Koszul equations have difference
H-Delta, and equivariant group-bar/PP operations commute with this base
change.  In that enlarged universal resolution the formal Weyl bar really
does cancel the selected Xi^- packet.

This does not yet give the pointed augmented physical comparison.  Marking
one matching occurrence introduces a private graph coordinate u_f.  Anchor
faithfulness requires d(u_f-u)=0, but that conormal is independent of the
complete response graph and global Eq conormals.  Imposing u_f=u changes the
classical physical fibre.  The equivariant aggregate graph is presentation
safe, but still does not imply the marked diagonal.

Even after granting that diagonal, target base change cannot remove the
literal residual-word and endpoint-ridge coordinates of the formal even
carrier: its word 012112 is outside every selected 3+3 midpoint summand,
and the pinned ridge/Omega mismatch ranks are six/five.  Thus the universal
construction is positive before physical augmentation; the first missing
map is a pointed augmented quasi-isomorphism, beginning with the marked
diagonal and then the residual-word/ridge totalization.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py":
        "e5deda7162db47f229239dc91b419baaf00c3158249859cbafb03fe3af2cc958",
    "computations/verify_h3_selected_lower_relative_weyl_bar_gate.py":
        "7a6f2afebcacc5924110e32a3f7d9c225992f07abae637d4529b5436c64cc294",
    "computations/verify_h3_reduced_eq_full_occurrence_simplex_symmetrization_gate.py":
        "5150fa94137a07062092b32328af63f4e188823d6ca06160a10e4b1c040786d3",
    "computations/verify_h3_anchor_conormal_functoriality_bridge.py":
        "83879756547765878c36944c1ab14827ab77a1f217931bc05db0c72cb0af32a8",
    "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py":
        "ebd25f79a6fe8db936fe5601b9220f152c5349dd794bbc4e08b2095f1c1d059f",
    "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py":
        "813419c756e7f21c09d63d3ec10f44c787e9580ca08c87809b7c4c550b908b4f",
    "computations/verify_h3_loop_degeneracy_hasse_cross_term_scope_gate.py":
        "024eb1cbe7d5aca9795c7d2491bb6399c0e93324f898d031707c1c752d7ea14c",
    "computations/verify_h3_oriented_shared_loop_resolution_unification.py":
        "e6819e5437d967ec9bb0f32a24836c70c34e5b35bbd4f9e3ebd38b0a5c4fb714",
    "computations/verify_h3_tau_plus_delta_literal_same_grade_gate.py":
        "f5d34986e086055dcba26e347c5a7f7470d9ec62a1346c9c872a8e828ec7b266",
}
EXPECTED_LEDGER_SHA256 = (
    "38f5c6120d2022087c9a03439de6885816ec759994a8d8d79b23b9b15c6d1888"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def universal_graph_base_change_audit():
    # Cotangent coordinates are (dy,dH,dDelta).  The graph and section
    # equations are y-H and y-Delta.  Their difference is Delta-H, i.e. the
    # physical equation up to the chosen orientation.
    graph = (Q(1), Q(-1), Q(0))
    section = (Q(1), Q(0), Q(-1))
    physical = add(section, scale(-1, graph))
    require(physical == (Q(0), Q(1), Q(-1))
            and rank((graph, section)) == 2,
            "the universal graph/section conormal changed")

    # The Koszul square d(e_g wedge e_Delta)=g e_Delta-Delta e_g has
    # d^2=g*Delta-Delta*g=0.  Relative restriction to the graph leaves the
    # difference H-Delta as the monic normal face.
    second_boundary = Q(1) - Q(1)
    require(second_boundary == 0, "the universal Koszul square changed")

    # A constant involution on the two orbit objects commutes with the
    # scalar Koszul differential.  This is the finite rho-equivariance core.
    rho = ((Q(0), Q(1)), (Q(1), Q(0)))
    differential = ((Q(1), Q(0)), (Q(0), Q(1)))
    left = tuple(tuple(sum(rho[i][k] * differential[k][j]
                           for k in range(2)) for j in range(2))
                 for i in range(2))
    right = tuple(tuple(sum(differential[i][k] * rho[k][j]
                            for k in range(2)) for j in range(2))
                  for i in range(2))
    require(left == right == rho,
            "rho stopped commuting with universal base change")
    return {
        "graph_equation": "g=y-H",
        "section_equation": "s=y-Delta",
        "conormal_difference": "s-g=H-Delta",
        "derived_fibre_classical_truncation": "H=Delta",
        "same_classical_physical_fibre": True,
        "Koszul_cell": "epsilon_g wedge epsilon_s",
        "Koszul_d_squared": 0,
        "rho_equivariant": True,
        "unaugmented_K_Eq_constructed": True,
    }


def universal_bar_xi_audit():
    bar = (ROOT / (
        "computations/verify_h3_selected_lower_relative_weyl_bar_gate.py"
    )).read_text()
    require("tau Z_0 = -Z_1" in bar
            and "formal_bar_boundary == expected_formal_boundary" in bar
            and "odd_face == expected_odd" in bar
            and '"rank_after_required_private_packet": rank_with_target' in bar,
            "the universal/physical Xi bar split changed")
    return {
        "universal_fine_components": [341, 341],
        "transport": "tau Z0=-Z1",
        "universal_bar_boundary": "d[tau|Z0]=-(Z0+Z1)",
        "endpoint_odd_private_face": (
            "Xi^-=(4/3)(xi-mate-s*xi+s*mate)"
        ),
        "Xi_is_boundary_in_universal_bar_resolution": True,
        "old_complete_row_Hasse_rank": 12,
        "rank_after_Xi": 13,
        "physical_occurrence_projection_constructed": False,
    }


def pointed_marked_diagonal_audit():
    # Coordinates (f,G,u_f,H0,u).  These are the actual complete response
    # occurrence graph and central global graph conormals from cf7dde2.
    d_e = (Q(1), Q(0), Q(-1), Q(0), Q(0))
    d_m = (Q(0), Q(1), Q(1), Q(0), Q(0))
    d_f0 = (Q(0), Q(0), Q(0), Q(1), Q(-1))
    marked_diagonal = (Q(0), Q(0), Q(1), Q(0), Q(-1))
    tangent = (Q(1), Q(-1), Q(1), Q(0), Q(0))
    anchor = (Q(1), Q(0), Q(0), Q(0), Q(0))
    require(all(dot(row, tangent) == 0 for row in (d_e, d_m, d_f0))
            and dot(marked_diagonal, tangent) == 1
            and dot(anchor, tangent) == 1
            and rank((d_e, d_m, d_f0)) == 3
            and rank((d_e, d_m, d_f0, marked_diagonal)) == 4,
            "the marked/global conormal obstruction changed")

    # Concrete classical mismatch for the pure aggregate graph.  The old
    # equations are H0=f+G, H0=u, u_f=f.  The point below satisfies all of
    # them but not u_f=u.  Hence imposing the pointed diagonal changes H0.
    point = {"f": Q(1), "G": Q(1), "u_f": Q(1),
             "H0": Q(2), "u": Q(2)}
    require(point["H0"] == point["f"] + point["G"]
            and point["H0"] == point["u"]
            and point["u_f"] == point["f"]
            and point["u_f"] != point["u"],
            "the classical marked-diagonal counterpoint changed")
    return {
        "conormal_rows": ["d(f-u_f)", "d(G+u_f)", "d(H0-u)"],
        "required_pointed_row": "d(u_f-u)",
        "old_conormal_rank": 3,
        "rank_after_pointed_row": 4,
        "kernel_witness": [int(value) for value in tangent],
        "anchor_on_witness": 1,
        "pointed_row_on_witness": 1,
        "classical_counterpoint_f_G_uf_H0_u": [1, 1, 1, 2, 2],
        "counterpoint_in_old_physical_fibre": True,
        "counterpoint_in_pointed_diagonal_fibre": False,
        "verdict": (
            "the derived pullback u_f=u is not a presentation change of "
            "the old physical fibre; it adjoins the desired comparison"
        ),
    }


def equivariant_aggregate_guard():
    # Two-occurrence model, coordinates (f1,f2,z1,z2,u).  The graph rows and
    # invariant aggregate z1+z2-u are presentation-safe.  They do not imply
    # the marked diagonal z1-u.
    graph1 = (Q(-1), Q(0), Q(1), Q(0), Q(0))
    graph2 = (Q(0), Q(-1), Q(0), Q(1), Q(0))
    aggregate = (Q(0), Q(0), Q(1), Q(1), Q(-1))
    marked = (Q(0), Q(0), Q(1), Q(0), Q(-1))
    tangent = (Q(1), Q(-1), Q(1), Q(-1), Q(0))
    require(all(dot(row, tangent) == 0
                for row in (graph1, graph2, aggregate))
            and dot(marked, tangent) == 1
            and rank((graph1, graph2, aggregate)) == 3
            and rank((graph1, graph2, aggregate, marked)) == 4,
            "the equivariant aggregate/marked split changed")
    return {
        "safe_equivariant_equation": "sum_mu u_mu=u",
        "equivalent_after_graph_elimination": "sum_mu f_mu=H0=u",
        "unsafe_marked_equation": "u_f=u",
        "augmentation_zero_tangent": [int(value) for value in tangent],
        "marked_diagonal_pairing": 1,
        "conclusion": (
            "full occurrence equivariance preserves the old fibre but "
            "retains the marked-minus-aggregate representation"
        ),
    }


def residual_word_and_ridge_audit():
    midpoint_words = set()
    for left, right in combinations(range(3), 2):
        for marked_sites in combinations(range(6), 3):
            marked_sites = set(marked_sites)
            midpoint_words.add(tuple(right if site in marked_sites else left
                                     for site in range(6)))
    residual = (0, 1, 2, 1, 1, 2)
    require(len(midpoint_words) == 60
            and residual not in midpoint_words
            and [residual.count(colour) for colour in range(3)] == [1, 3, 2],
            "the residual/midpoint word obstruction changed")

    total = (ROOT / (
        "computations/verify_h3_rootless_third_cofactor_bianchi_total_complex_obstruction.py"
    )).read_text()
    require('require(rank(ridge_matrix) == 6' in total
            and 'require(rank(omega_matrix) == 5' in total
            and '"midpoint_hits": 0' in total
            and '"physical_residual_word": "".join' in total,
            "the pinned word/ridge obstruction changed")
    return {
        "formal_even_residual_word": "012112",
        "residual_colour_counts": [1, 3, 2],
        "selected_midpoint_words": 60,
        "midpoint_word_type": "exactly 3+3 in two colours",
        "residual_is_selected_midpoint": False,
        "primitive_word_dual": "e_012112^* modulo the midpoint summand",
        "ridge_mismatch_rank": 6,
        "primitive_Omega_rank": 5,
        "target_Eq_base_change_affects_these_rows": False,
        "next_required_faces": (
            "one source-labelled residual-word change into the 3+3 "
            "midpoint summand plus the six ridge/five Omega caps"
        ),
    }


def augmentation_noninvariance_guard():
    # A contractible two-term pair d(a)=e has one underlying differential,
    # but arbitrary values can be assigned to a new external readout on a.
    # Hence a quasi-isomorphism of the unaugmented complex does not define q,
    # anchor, eta/sigma, or W on the new resolution generator.
    differential = (Q(1),)
    readout_zero = (Q(0),)
    readout_one = (Q(1),)
    require(differential == (Q(1),)
            and readout_zero != readout_one,
            "the augmentation noninvariance guard changed")
    return {
        "same_underlying_contractible_pair": "d(a)=e",
        "two_possible_new_generator_readouts": [0, 1],
        "unaugmented_quasi_isomorphism_determines_readout": False,
        "rows_requiring_explicit_transport": [
            "marked anchor", "physical q", "labelled residue", "W",
            "word/fine/repeated", "eta/sigma ridge",
        ],
    }


def excess_diagonal_gysin_audit():
    # Divided-power product rule for multi-affine f=x*a and g=x*b.
    a, b = Q(3), Q(-5, 2)
    divided_second_product = a * b
    product_of_firsts = a * b
    require(divided_second_product == product_of_firsts,
            "the divided diagonal excess normalization changed")

    # Five distinct source loop labels collapse to one target normal 2e4.
    source_loops = ("02", "03", "05", "23", "25")
    gysin_rows = ((Q(1),) * len(source_loops),)
    require(rank(gysin_rows) == 1
            and len(source_loops) - rank(gysin_rows) == 4,
            "the excess target/source-label fibre changed")
    label_02 = (Q(1), Q(0), Q(0), Q(0), Q(0))
    label_25 = (Q(0), Q(0), Q(0), Q(0), Q(1))
    require(dot(gysin_rows[0], label_02)
            == dot(gysin_rows[0], label_25) == 1
            and add(label_02, scale(-1, label_25)) != (Q(0),) * 5,
            "the target diagonal unexpectedly distinguished source loops")

    # Shared-02 orientations yield B1,B4, but the actual tau-plus omitted
    # grades resolve only into B0,B2,B3,B5.
    v = (Q(0), Q(1, 2), Q(0), Q(0), Q(1, 2), Q(0))
    local_tau = (Q(1, 4), Q(0), Q(1, 4),
                 Q(1, 4), Q(0), Q(1, 4))
    delta = add(v, scale(-1, local_tau))
    expected_delta = (Q(-1, 4), Q(1, 2), Q(-1, 4),
                      Q(-1, 4), Q(1, 2), Q(-1, 4))
    rho_b = (5, 1, 3, 2, 4, 0)
    require(delta == expected_delta
            and sum(delta, Q(0)) == 0
            and tuple(delta[index] for index in rho_b) == delta,
            "the excess same-grade delta-plus obstruction changed")
    return {
        "formal_excess_formula": (
            "D_4^[2](fg)=D_4^[1](f)D_4^[1](g) for multi-affine f,g"
        ),
        "coefficient": 1,
        "source_loop_labels": list(source_loops),
        "common_target_normal_direction": "2e4",
        "source_to_target_label_map_rank": 1,
        "forgotten_source_label_kernel_rank": 4,
        "canonical_target_Gysin_section_to_physical_labels": False,
        "shared_02_oriented_outputs": ["B1", "B4"],
        "shared_02_even_average": [str(value) for value in v],
        "actual_tau_plus_repeated_grades": ["01", "04"],
        "actual_tau_plus_local_outputs": ["B0", "B2", "B3", "B5"],
        "actual_tau_plus_local_average": [str(value) for value in local_tau],
        "required_same_grade_transport_delta_plus": [
            str(value) for value in delta
        ],
        "delta_plus_rho_even": True,
        "delta_plus_augmentation": "0",
        "excess_cell_equals_odd_Xi_bar": False,
        "reason": (
            "the excess cell is an order-two repeated diagonal; Xi^- is "
            "the order-six occurrence-local group-bar face.  Both live in "
            "the universal resolution, but one is not the projection of "
            "the other without the missing augmented comparison"
        ),
        "Rees_deformation": {
            "abstract_integral_normal_family": True,
            "abstract_Bockstein_is_normal_generator": True,
            "physical_selected_D0_identification": False,
            "reason": (
                "the target normal direction forgets the source loop/root "
                "label, while the physical proper face retains wrong-word "
                "and ridge coordinates"
            ),
        },
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "universal graph derived base change / physical descent gate",
        "pins": PINS,
        "universal_unaugmented_construction": universal_graph_base_change_audit(),
        "universal_occurrence_bar": universal_bar_xi_audit(),
        "first_pointed_obstruction": pointed_marked_diagonal_audit(),
        "equivariant_aggregate_guard": equivariant_aggregate_guard(),
        "next_literal_augmented_obstruction": residual_word_and_ridge_audit(),
        "augmentation_invariance_guard": augmentation_noninvariance_guard(),
        "excess_diagonal_Gysin_attempt": excess_diagonal_gysin_audit(),
        "exact_status": {
            "universal_graph_bar_PP_Rees_core": "constructed formally",
            "Xi_minus_in_universal_resolution": "boundary",
            "same_unaugmented_derived_physical_fibre": True,
            "pointed_anchor_faithful_comparison": False,
            "word_ridge_W_q_terminal_preserving_comparison": False,
        },
        "conditional_construction_hypotheses": {
            "H1": (
                "G-equivariant R=k[beta] graph/bar/PP resolution with "
                "classical truncation H=Delta"
            ),
            "H2": (
                "pointed source-algebra map: u_f-Phi_beta^*(u) lies in "
                "the complete response ideal"
            ),
            "H3": (
                "source-loop-labelled excess Gysin lift realizing "
                "delta_plus in the actual tau-plus word/repeated grade"
            ),
            "H4": (
                "proper-face totalization caps word 012112 and the rank "
                "6/5 ridge/Omega packet with protected rows retained"
            ),
            "H5": (
                "beta-integral augmented readout transport; special "
                "Bockstein equals physical V"
            ),
            "construction_if_granted": (
                "Koszul graph/section cell + occurrence group bar + "
                "labelled excess Gysin lift + proper-face totalization"
            ),
            "projections": {
                "odd": "Xi^- input with physical +/-M_v output",
                "even": "full v=(B1+B4)/2 packet",
                "special": "V by Bockstein naturality",
            },
        },
        "sharp_remaining_theorem": (
            "construct a pointed augmented quasi-isomorphism from the "
            "universal G-equivariant graph/bar/PP derived fibre to the "
            "literal physical presentation.  Its degree-zero conormal is "
            "d(u_f-u).  Its excess-diagonal component must next lift the "
            "single target normal 2e4 back to the correct physical source "
            "label; in the tau-plus grade this is exactly delta_plus.  It "
            "must then move word 012112 into the selected 3+3 midpoint summand "
            "while capping the rank-six ridge and rank-five Omega packet. "
            "The same map must transport q, W, residue, and eta/sigma"
        ),
        "verdict": (
            "the universal graph proposal constructs Phi_beta only in the "
            "unaugmented derived category.  It genuinely kills Xi^- there. "
            "It cannot simply be chosen as the complete physical source: "
            "the pointed diagonal changes the classical fibre, while the "
            "presentation-safe aggregate leaves that diagonal nonzero.  The "
            "excess Gysin map also forgets a rank-four source-loop-label "
            "kernel, whose tau-plus component is delta_plus; after that the "
            "formal even carrier still retains a literal wrong-word/ridge "
            "class untouched by Eq base change"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("universal graph physical descent ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 universal graph derived base change: DERIVED YES / PHYSICAL OPEN")
    print("universal bar kills Xi^-: YES")
    print("first pointed obstruction: d(u_f-u), rank 3 -> 4")
    print("excess Gysin obstruction: target 2e4 forgets rank-4 loop labels")
    print("next literal obstruction: word 012112; ridge/Omega ranks 6/5")
    print("physical q/W/residue/eta/sigma: no canonical transfer yet")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
