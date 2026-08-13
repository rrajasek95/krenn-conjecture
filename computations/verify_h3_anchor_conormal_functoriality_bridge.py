#!/usr/bin/env python3
"""Audit when the Interface-II anchor law follows functorially.

For a pointed algebra comparison phi^#:Q/J -> P/I carrying a central
function a to the marked occurrence f modulo I, differentiation gives

    [df] = dphi^*[da]  in  Omega_P/(dI).

This is exactly the anchor-faithful quotient law.  A chain comparison on
the K_Eq cell does not contain the required degree-zero function identity.
The complete response does canonically give a private graph coordinate
u_f with [df]=[du_f], while the central Eq cell uses the global target u.
The first missing class is therefore [d(u_f-u)].
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py":
        "813419c756e7f21c09d63d3ec10f44c787e9580ca08c87809b7c4c550b908b4f",
    "computations/verify_h3_interface_ii_anchor_faithful_central_comparison.py":
        "fe77afbafa23656d8afd6aaa0218e6134776205ffe4525658273de80f9f004a6",
    "computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py":
        "ce28ff5d25bf575c280a21c0e35c6dc1ebef54eb039ac94cdc25932a61b95829",
    "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py":
        "f194101187d92255a8396b762769df2d3e058f0adc2072ae822da4881f1a4e3d",
}
EXPECTED_LEDGER_SHA256 = (
    "d12c576a1bad5a3ad25974fb35580ebaa703bb5150e4c2b076c3cbbf8f957df4"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def rref(rows, width=None):
    work = [list(map(Q, row)) for row in rows]
    if width is None:
        width = len(work[0]) if work else 0
    require(all(len(row) == width for row in work), "ragged matrix")
    pivots = []
    pivot_row = 0
    for column in range(width):
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
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def in_row_span(rows, target):
    width = len(target)
    return (len(rref(rows, width)[1])
            == len(rref(tuple(rows) + (tuple(target),), width)[1]))


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def subtract(left, right):
    return tuple(Q(a) - Q(b) for a, b in zip(left, right, strict=True))


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def pointed_conormal_lemma_audit():
    # Nonlinear product-rule sample at x=(1,1,1):
    # F1=x*y-z, F2=y^2-1, c1=x+y, c2=x-z, g=x*z, and
    # f=g+c1*F1+c2*F2.  Since F1(x)=F2(x)=0, the dc_i*F_i terms vanish and
    # d(f-g)=c1(x)dF1+c2(x)dF2=2*dF1.
    d_f1 = (Q(1), Q(1), Q(-1))
    d_f2 = (Q(0), Q(2), Q(0))
    c1_at_point = Q(2)
    c2_at_point = Q(0)
    predicted = add(
        tuple(c1_at_point * value for value in d_f1),
        tuple(c2_at_point * value for value in d_f2),
    )
    # Direct differentiation of the displayed polynomial identity at the
    # point gives the same row.
    direct_d_f_minus_g = (Q(2), Q(2), Q(-2))
    require(predicted == direct_d_f_minus_g
            and in_row_span((d_f1, d_f2), direct_d_f_minus_g),
            "the pointed conormal/product-rule identity changed")
    return {
        "algebra_identity": "f-phi^*(a)=sum_j c_j F_j",
        "point_condition": "F_j(x)=0",
        "differentiated_identity": (
            "df-dphi^*(da)=sum_j c_j(x)dF_j; terms F_j(x)dc_j vanish"
        ),
        "conormal_conclusion": "[df]=dphi^*[da] in Omega_P/(dI)",
        "nonlinear_sample": {
            "dF1": tuple(map(str, d_f1)),
            "dF2": tuple(map(str, d_f2)),
            "d(f-g)": tuple(map(str, direct_d_f_minus_g)),
        },
    }


def occurrence_private_graph_audit():
    # Coordinates (f,G,u_f,H0,u).  The complete response graph has
    # E=f-u_f and M=G+u_f.  The central Eq graph has F0=H0-u.
    d_e = (Q(1), Q(0), Q(-1), Q(0), Q(0))
    d_m = (Q(0), Q(1), Q(1), Q(0), Q(0))
    d_f0 = (Q(0), Q(0), Q(0), Q(1), Q(-1))
    rows = (d_e, d_m, d_f0)
    H = (Q(1), Q(0), Q(0), Q(0), Q(0))
    du_f = (Q(0), Q(0), Q(1), Q(0), Q(0))
    du = (Q(0), Q(0), Q(0), Q(0), Q(1))
    require(subtract(H, du_f) == d_e,
            "the complete response stopped transporting df to du_f")
    bridge = subtract(du_f, du)
    desired = subtract(H, du)
    require(not in_row_span(rows, bridge)
            and not in_row_span(rows, desired),
            "the private/global diagonal bridge unexpectedly became conormal-zero")

    # The tangent changes the marked occurrence while keeping both the
    # response graph and the global Eq graph fixed.
    xi = (Q(1), Q(-1), Q(1), Q(0), Q(0))
    require(all(dot(row, xi) == 0 for row in rows)
            and dot(H, xi) == 1 and dot(du, xi) == 0,
            "the private/global anchor counterguard changed")

    # Either literal degree-zero bridge suffices.  The direct bridge is
    # u_f-u; the two-step bridge u_f-H0 plus F0 gives the same result.
    d_private_to_global = bridge
    d_private_to_h0 = (Q(0), Q(0), Q(1), Q(-1), Q(0))
    require(in_row_span(rows + (d_private_to_global,), desired)
            and in_row_span(rows + (d_private_to_h0,), desired),
            "a literal private/global bridge stopped proving anchor faithfulness")
    return {
        "coordinates": ["f", "G", "u_f", "H0", "u"],
        "complete_response_graph": ["E=f-u_f", "M=G+u_f"],
        "central_Eq_graph": "F0=H0-u",
        "functorial_private_law": "[df]=[du_f]",
        "desired_global_law": "[df]=[du]",
        "first_missing_class": "[d(u_f-u)]",
        "equivalent_two_step_class": "[d(u_f-H0)] (because d(H0-u)=0)",
        "counterguard_tangent": tuple(map(str, xi)),
        "H_on_tangent": "1",
        "du_on_tangent": "0",
        "complete_response_plus_central_Eq_force_law": False,
        "law_after_either_literal_bridge": True,
    }


def current_phi_beta_type_audit():
    master = (ROOT / (
        "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py"
    )).read_text()
    graph = (ROOT / (
        "computations/verify_h3_trapped_carrier_occurrence_graph_hessian_cone_gate.py"
    )).read_text()
    require('"source_orbit": "R[rho]{K_Eq}, rho^2=1"' in master
            and '"equivariant_map_data": "one object image Phi_beta(K_Eq)"'
            in master
            and "an R-linear rho-equivariant chain comparison" in master,
            "the pinned Phi_beta type changed")
    require('"equations": ["E=f-u=0", "M=G+u=0"]' in graph
            and "private u pivot" in graph,
            "the pinned occurrence graph type changed")
    return {
        "committed_Phi_beta_domain": "rank-two regular orbit R[rho]{K_Eq}",
        "committed_Phi_beta_structure": "R-linear rho-equivariant chain map",
        "anchor_law_domain": "complete 171-column response tangent X",
        "type_match_without_source_presentation_map": False,
        "missing_degree_zero_datum": (
            "a pointed algebra/source-presentation map carrying the central "
            "anchor function to f modulo the complete response ideal"
        ),
        "why_augmented_output_rows_do_not_suffice": (
            "target/anchor/q values of Phi_beta(K_Eq) are chain-output "
            "readouts; they do not define the pullback of a function on X"
        ),
    }


def universal_graph_derived_base_change_audit():
    # Reuse coordinates (f,G,u_f,H0,u).  Pulling the occurrence graph back
    # to the diagonal u_f=u appends exactly the missing conormal row.
    d_e = (Q(1), Q(0), Q(-1), Q(0), Q(0))
    d_m = (Q(0), Q(1), Q(1), Q(0), Q(0))
    d_f0 = (Q(0), Q(0), Q(0), Q(1), Q(-1))
    d_delta = (Q(0), Q(0), Q(1), Q(0), Q(-1))
    old_rows = (d_e, d_m, d_f0)
    new_rows = old_rows + (d_delta,)
    old_rank = len(rref(old_rows, 5)[1])
    new_rank = len(rref(new_rows, 5)[1])
    require((old_rank, new_rank) == (3, 4),
            "the diagonal base change stopped adding the missing conormal")
    H_minus_du = (Q(1), Q(0), Q(0), Q(0), Q(-1))
    require(not in_row_span(old_rows, H_minus_du)
            and in_row_span(new_rows, H_minus_du),
            "the diagonal pullback no longer has the expected anchor effect")

    # A marked occurrence is not a vector in the trivial G representation.
    # In the three-point permutation shadow its average is invariant and the
    # marked-minus-average debt is a nonzero augmentation-zero direction.
    marked = (Q(1), Q(0), Q(0))
    average = (Q(1, 3), Q(1, 3), Q(1, 3))
    debt = subtract(marked, average)
    require(sum(debt, Q(0)) == 0 and any(debt),
            "the marked occurrence stopped having nontrivial orbit debt")
    return {
        "universal_graph": "Gamma_f: u_f=f is isomorphic to the source",
        "anchor_is_actual_source_function": True,
        "derived_diagonal": "Delta: u_f=u",
        "cotangent_naturality_on_derived_pullback": True,
        "old_conormal_rank": old_rank,
        "rank_after_diagonal": new_rank,
        "projection_back_to_original_source_is_quasi_isomorphism": False,
        "relative_conormal": "d(u_f-u), exactly the missing anchor class",
        "G_equivariance": {
            "marked_occurrence_invariant": False,
            "invariant_projection": tuple(map(str, average)),
            "marked_minus_invariant": tuple(map(str, debt)),
            "interpretation": (
                "the full orbit graph is equivariant, but a map to the "
                "trivial global target sees the aggregate; selecting one "
                "occurrence needs a stabilizer section/augmentation-zero bar"
            ),
        },
        "terminal_descent_needed": (
            "an augmented quasi-isomorphism preserving the literal six-term, "
            "q, ainc, word/fine/repeated, eta/sigma and protected rows"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "anchor conormal functoriality and private/global bridge",
        "pins": PINS,
        "pointed_conormal_lemma": pointed_conormal_lemma_audit(),
        "actual_occurrence_bridge": occurrence_private_graph_audit(),
        "current_Phi_beta_type": current_phi_beta_type_audit(),
        "universal_graph_derived_base_change": (
            universal_graph_derived_base_change_audit()
        ),
        "exact_positive_statement": (
            "If Phi_beta is upgraded to a morphism of pointed source "
            "presentations and f-Phi_beta^*(a_Eq) belongs to the complete "
            "response ideal, then differentiating this identity proves "
            "[H]=Phi_beta^*[h_Eq] modulo row(A), over k[beta] and after "
            "every specialization"
        ),
        "sharp_negative_statement": (
            "The presently specified R-linear rho chain map, even with all "
            "output augmentations, does not contain the degree-zero anchor "
            "identity.  Complete response product rule gives only the "
            "private law [H]=[du_f]; central Eq gives [dH0]=[du].  Their "
            "first unforced difference is [d(u_f-u)]"
        ),
        "shortest_new_clause": (
            "add the anchored-section condition u_f-Phi_beta^*(u) in I "
            "(equivalently u_f-Phi_beta^*(H0) in I, modulo F0), or just its "
            "first-order conormal form [d(u_f-u)]=0"
        ),
        "categorical_route_scope": (
            "Gamma_f and cotangent base-change prove the law on the derived "
            "diagonal fibre.  To use the existing physical terminal theorem, "
            "one must still prove that this replacement descends by an "
            "augmented quasi-isomorphism.  The diagonal raises conormal rank "
            "in the sharp guard, so such descent is not formal"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("anchor conormal functoriality ledger changed", digest))
    return ledger, digest


def main():
    _, digest = audit()
    print("h3 anchor conormal functoriality bridge: PASS")
    print("pointed source-algebra comparison => anchor law functorially")
    print("current Phi_beta chain map alone => anchor law NOT forced")
    print("complete response gives [H]=[du_f], not [du]")
    print("first missing class: [d(u_f-u)]")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
