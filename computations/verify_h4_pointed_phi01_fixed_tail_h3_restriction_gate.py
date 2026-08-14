#!/usr/bin/env python3
"""Reduce the missing fixed-tail h=4 phi01 to the h=3 mixed comparison.

The common squarefree edge 67 gives a literal relative restriction.  Write
``x`` for its coefficient and ``dx`` for its first principal-parts face.
On the fixed-tail summand

    rho_67(x tensor z) = z,       rho_67(dx tensor z) = 0.

This is a chain retraction.  Insertion is a chain map only after quotienting
the displayed ``dx tensor z`` spectator face; in the absolute totalization
that face is exactly the ordinary Leibniz/Hasse debt.

The operation-changing projection of a normalized physical phi01 therefore
restricts to the unique normalized h=3 map Phi_KS,r0.  Conversely Phi_KS,r0,
together with the already explicit spectator Hasse face, gives the relative
fixed-tail prolongation.  Thus this phi01 gate is not an independent all-h
input: its new source datum is precisely the h=3 mixed comparison.

The checker also audits the tempting coefficient-selector construction.  It
isolates the desired top coefficient but does not supply its two odd cut
faces; even after granting them, selected db01 raises rank 183 -> 184 and is
read by the centered dual with value 174.  Finally, the checker lists the six
literal q67*db01 terms and their conditional cap-r0 readouts.
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
    "computations/verify_h4_collision_ks_physical_site_permutation_tree_gate.py":
        "7245dadf4e358efb3a6b63bfb4d33508c031ef468ff50f3eefdc60a000d41228",
    "notes/h4-collision-ks-physical-site-permutation-tree-gate.md":
        "0dc83a1457e6531851e7b907a27bddde74ad0f34ee7cc0be93e3b14123839562",
    "computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py":
        "ac7f88b21976cae557ed6b4cacaeca19d5799ef7a30ac53df6dc0f0ab08b0f93",
    "notes/h3-quadratic-occurrence-selector-hasse-odd-cut-no-go.md":
        "9e8c208ff1526008cf049f45f9b63a5518e54660a2a84eab7f355d11b40dcb23",
    "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py":
        "02a28ec54b83b2f786e47b0fdc992f5f28dd95a04ba16219f0e24482d4999097",
    "notes/h3-response-ks-to-cap-r0-multiplicative-comparison-gate.md":
        "b87cccff771337fc7ed6d0092f958303084c1be8326a9faf46efb7fa751ed8f6",
    "computations/verify_h3_b01_r0_macaulay_product_crossword_gate.py":
        "03b3c0b0d0ce5a3dcba581a6a1b252d746994d9a396e9fb3ba5318d6e7f33f31",
    "notes/h3-b01-r0-macaulay-product-crossword-gate.md":
        "1fa4ec041803225a284cbe9f4ed7f01409001781e09d975f8791ccabf39295f4",
    "computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py":
        "a8dfe952ce4fbbaf71ffd4ef748e456d5284dbf6b71655cce6f2f10576db0d06",
    "notes/h3-pointed-occurrence-primitive-cap-p2-propagation-gate.md":
        "c1cac29cabc30d13b4b2a30d882e1b8e01268423be7b29d7748744ebecaf60ff",
    "computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py":
        "3b2cf3aa1cd6ee46f60c0e3621342f4eb15420d6d5d302546b2403d966703ba8",
    "notes/h3-phi-ks-r0-word-operation-reachability-no-go.md":
        "ad115e787a15ad913a014bc652dd13d54eb46e971cff500e0b7821f46f2f513c",
    "computations/verify_h3_balanced_square_private_eq_projection_gate.py":
        "bbfb690a73844169574351ad019171a6d9c5fe332e59cc9694a1f67dcf31cf8e",
    "notes/h3-balanced-square-private-eq-projection-gate.md":
        "6d740e7e30231204dbe1b79c4b7c21fe5f5b5ac45122ac714be3c7626afa7c31",
}
EXPECTED_LEDGER_SHA256 = (
    "59a2438ecb98f2b1373838b8e9144655a84a40a66600f3819bcf812da7e2181c"
)

Vector = tuple[Q, ...]
Matrix = tuple[Vector, ...]  # rows


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def transpose(matrix: Matrix) -> Matrix:
    require(matrix, "empty transpose")
    width = len(matrix[0])
    require(all(len(row) == width for row in matrix), "matrix width")
    return tuple(tuple(row[column] for row in matrix)
                 for column in range(width))


def matmul(left: Matrix, right: Matrix) -> Matrix:
    require(left and right and len(left[0]) == len(right), "matmul shape")
    columns = transpose(right)
    return tuple(tuple(sum((a * b for a, b in zip(row, column, strict=True)),
                           Q(0))
                       for column in columns)
                 for row in left)


def identity(size: int) -> Matrix:
    return tuple(tuple(Q(row == column) for column in range(size))
                 for row in range(size))


def zero(height: int, width: int) -> Matrix:
    return tuple((Q(0),) * width for _ in range(height))


def hstack(left: Matrix, right: Matrix) -> Matrix:
    require(len(left) == len(right), "hstack height")
    return tuple(a + b for a, b in zip(left, right, strict=True))


def vstack(top: Matrix, bottom: Matrix) -> Matrix:
    require(top and bottom and len(top[0]) == len(bottom[0]), "vstack width")
    return top + bottom


def scale(value: Q, matrix: Matrix) -> Matrix:
    return tuple(tuple(value * entry for entry in row) for row in matrix)


def rank(vectors: tuple[Vector, ...]) -> int:
    if not vectors:
        return 0
    work = [list(map(Q, vector)) for vector in vectors]
    width = len(work[0])
    require(all(len(vector) == width for vector in work), "rank width")
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
            work[row] = [entry - value * base for entry, base in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def selector_attempt_audit() -> dict[str, object]:
    selector = load(
        "computations/verify_h3_quadratic_occurrence_selector_hasse_odd_cut_no_go.py",
        "phi01_selector_dependency",
    )
    ledger, digest = selector.audit()
    require(digest == selector.EXPECTED_LEDGER_SHA256,
            "quadratic selector dependency ledger changed")
    coefficient = ledger["quadratic_coefficient_top_and_physical_faces"]
    odd = ledger["first_restriction_obstruction"]
    db01 = ledger["second_selected_db01_projection"]
    require(coefficient["coefficient_identity"] ==
                "Q_(0,1)*X_23=Q_(0,1)*X_45=e_f"
            and coefficient["selected_db01_terms"] == 6
            and [record["dual_on_required_restriction"]
                 for record in odd["cut_records"]] == [90, 90]
            and db01["direct_sum_rank_before_after_db01"] == [183, 184]
            and db01["centered_flag_dual_on_selected_db01"] == 174,
            "the pointed-selector obstruction changed")
    return {
        "coefficient_selector": coefficient["coefficient_identity"],
        "coefficient_top_selected_exactly": True,
        "physical_lift_constructed": False,
        "two_labelled_odd_cut_dual_values": [90, 90],
        "after_granting_both_odd_cut_fillers_rank": [183, 184],
        "centered_dual_on_selected_six_term_db01": 174,
        "protected_rows_were_granted_arbitrarily":
            odd["protected_rows_granted_arbitrarily"],
        "conclusion": (
            "multiplication/projection of the known centered occurrence "
            "carrier selects the coefficient but does not construct phi01"
        ),
    }


def orbit_relative_pacomp_audit() -> dict[str, object]:
    # In the action groupoid the bar joins m0 in source object S to m1 in
    # the relabelled object gS.  There are two possible maps back to a fixed
    # object.  Honest inverse transport identifies the second endpoint with
    # m0, so the bar has zero fixed-fibre boundary.  Forgetting the object
    # label instead calls it m1 and imposes the raw fold m1-m0; this lowers
    # fixed-source H0 from dimension two to one.
    fixed_m0 = (Q(1), Q(0))
    fixed_m1 = (Q(0), Q(1))
    desired_boundary = tuple(right - left for left, right in
                             zip(fixed_m0, fixed_m1, strict=True))
    inverse_transport_boundary = tuple(left - left for left in fixed_m0)
    require(desired_boundary == (Q(-1), Q(1))
            and inverse_transport_boundary == (Q(0), Q(0))
            and rank((fixed_m0, fixed_m1)) == 2
            and rank((desired_boundary,)) == 1,
            "orbit-relative/fixed-fibre dichotomy changed")

    # H0 of a two-dimensional degree-zero fixed fibre is dimension two.
    # Adjoining the raw fold gives quotient dimension one.
    fixed_h0 = 2
    folded_h0 = 2 - rank((desired_boundary,))
    require(folded_h0 == 1, "raw site fold stopped lowering H0")
    return {
        "groupoid_bar_boundary": "(gS,m1)-(S,m0)",
        "honest_inverse_transport_to_S": [0, 0],
        "honest_transport_constructs_fixed_phi01": False,
        "object_label_forgetting_boundary": [-1, 1],
        "fixed_source_H0_before_after_raw_fold": [fixed_h0, folded_h0],
        "raw_fold_is_quasi_isomorphism_on_fixed_source": False,
        "PAComp_requires": (
            "a boundary/terminal or active cap in the actual complete "
            "pointed source complex, with literal word/fine/operation rows"
        ),
        "orbit_relative_transport_sufficient_for_current_PAComp": False,
        "possible_alternative_theorem": (
            "a conservative equivariant descent from the orbit-relative "
            "comparison to an objectwise terminal/active cap"
        ),
        "alternative_theorem_currently_proved": False,
        "why_relabel_invariance_alone_is_insufficient": (
            "it transports an already obtained cap between isomorphic "
            "sources; it does not turn an orbit-groupoid bar into an "
            "objectwise physical boundary"
        ),
    }


def fixed_tail_chain_retraction_audit() -> dict[str, object]:
    # h=3 basis: (epsilon_s, r0, c_f, E), with d epsilon_s=-c_f,
    # d r0=E.  Matrices act on column vectors.
    d3 = (
        (Q(0), Q(0), Q(0), Q(0)),
        (Q(0), Q(0), Q(0), Q(0)),
        (Q(-1), Q(0), Q(0), Q(0)),
        (Q(0), Q(1), Q(0), Q(0)),
    )
    require(matmul(d3, d3) == zero(4, 4), "h3 differential squared")

    # h=4 order: q67 tensor h3 basis, dq67 tensor h3 basis.
    # d(q67*z)=q67*dz+dq67*z and d(dq67*z)=-dq67*dz.
    d4 = vstack(
        hstack(d3, zero(4, 4)),
        hstack(identity(4), scale(Q(-1), d3)),
    )
    insertion = vstack(identity(4), zero(4, 4))
    restriction = hstack(identity(4), zero(4, 4))
    require(matmul(d4, d4) == zero(8, 8), "fixed-tail total d squared")
    require(matmul(restriction, insertion) == identity(4),
            "rho67 insertion is not identity")
    require(matmul(restriction, d4) == matmul(d3, restriction),
            "rho67 stopped being a chain map")

    insertion_defect = tuple(
        tuple(left - right for left, right in zip(row_left, row_right,
                                                   strict=True))
        for row_left, row_right in zip(matmul(d4, insertion),
                                       matmul(insertion, d3), strict=True)
    )
    expected_defect = vstack(zero(4, 4), identity(4))
    require(insertion_defect == expected_defect,
            "the spectator Leibniz defect changed")
    return {
        "h3_basis": ["epsilon_s", "r0", "c_f", "E"],
        "h4_basis": [
            "q67*epsilon_s", "q67*r0", "q67*c_f", "q67*E",
            "dq67*epsilon_s", "dq67*r0", "dq67*c_f", "dq67*E",
        ],
        "rho67": "q67*z -> z; dq67*z -> 0",
        "rho67_is_chain_map": True,
        "rho67_after_insertion": "identity",
        "absolute_insertion_chain_defect": "dq67 tensor identity",
        "relative_insertion_mod_spectator_face_is_chain_map": True,
        "interpretation": (
            "restriction is unconditional; prolongation adds only the "
            "literal spectator Leibniz/Hasse face"
        ),
    }


def normalized_mixed_map_audit() -> dict[str, object]:
    comparison = load(
        "computations/verify_h3_response_ks_to_cap_r0_multiplicative_comparison_gate.py",
        "phi01_h3_comparison_dependency",
    )
    ledger, digest = comparison.audit()
    require(digest == comparison.EXPECTED_LEDGER_SHA256,
            "h3 comparison dependency ledger changed")
    algebraic = ledger["ungraded_two_term_chain_map"]
    require(algebraic["ungraded_chain_map_parameter_dimension"] == 1
            and algebraic["normalized_solution"] == {"a": 1, "b": -1},
            "normalized mixed map changed")

    reachability = load(
        "computations/verify_h3_phi_ks_r0_word_operation_reachability_no_go.py",
        "phi01_h3_reachability_dependency",
    )
    route_ledger, route_digest = reachability.audit()
    require(route_digest == reachability.EXPECTED_LEDGER_SHA256,
            "h3 reachability dependency ledger changed")
    generous = route_ledger["maximally_generous_root_closure"]
    require(generous["word_only_cap_landing_after_roots"]
            and not generous["typed_cap_r0_reached_without_new_edge"],
            "the word/operation separation changed")

    # Coefficients (a,b) obey a+b=0.  rho67 is identity on the q67 block,
    # so a normalized h4 mixed edge restricts to the unique (1,-1) solution.
    relation = (Q(1), Q(1))
    normalized = (Q(1), Q(-1))
    require(sum((a * b for a, b in zip(relation, normalized, strict=True)),
                Q(0)) == 0,
            "mixed chain-map sign changed")
    return {
        "h3_chain_map_equation": "a+b=0",
        "unique_monic_solution": {
            "Phi_1(epsilon_s)": "r0",
            "Phi_0(c_f)": "-E",
        },
        "word_roots_can_reach_cap_word": True,
        "word_roots_change_operation_parent": False,
        "exact_forward_implication": (
            "pi_mix*rho67(phi01) is the root-labelled naturality instance "
            "of Phi_KS,r0/P_f"
        ),
        "exact_reverse_implication": (
            "q67*Phi_KS,r0/P_f plus its dq67 Leibniz/Hasse face is the "
            "relative fixed-tail phi01 instance"
        ),
        "new_unknown_source_datum_count": 1,
        "independent_all_h_theorem_needed": False,
    }


def selected_db01_and_cap_readout_audit() -> dict[str, object]:
    matchings = (("23", "45"), ("24", "35"), ("25", "34"))
    h3_terms = tuple(
        f"p0*s1*dq{edge}*q{mate}"
        for left, right in matchings
        for edge, mate in ((left, right), (right, left))
    )
    h4_terms = tuple(f"q67*{term}" for term in h3_terms)
    spectator_terms = tuple(f"dq67*p0*s1*q{left}*q{right}"
                            for left, right in matchings)
    require(len(h3_terms) == len(set(h3_terms)) == 6
            and len(spectator_terms) == len(set(spectator_terms)) == 3,
            "selected fixed-tail support changed")

    # The restriction matrix on the selected q67*db01 packet is I_6.  The
    # separate dq67*b01 packet is killed.
    rho_selected = identity(6)
    require(rank(rho_selected) == 6, "selected restriction lost rank")

    # At one selected corner the committed r0 column has the following
    # augmented signature.  q=M-ainc is therefore zero.  Every one of the
    # six conditional db01*r0 faces carries this same local signature.
    row_order = (
        "B", "Eq", "target", "M", "ainc", "q", "P_f",
        "ores", "W", "ridge", "eta", "sigma",
    )
    per_term = tuple(map(Q, (1, 1, 1, -1, -1, 0, 1, 0, 0, 0, 0, 0)))
    require(per_term[row_order.index("q")] ==
                per_term[row_order.index("M")] -
                per_term[row_order.index("ainc")],
            "physical q identity changed")
    aggregate = tuple(6 * value for value in per_term)

    # Do not silently identify the pointed conormal P_f with the primitive
    # cap p.  Their smallest exact quotient is already rank two.
    p_f = tuple(map(Q, (1, 0, 0)))
    primitive_p = tuple(map(Q, (0, -1, -1)))
    invisible_n = tuple(map(Q, (0, 1, 0)))
    require(rank((p_f, primitive_p)) == 2
            and rank((p_f, primitive_p, invisible_n)) == 3,
            "pointed conormal/primitive cap quotient changed")
    return {
        "h3_selected_db01_terms": list(h3_terms),
        "h4_common_tail_terms": list(h4_terms),
        "spectator_Leibniz_terms_killed_by_rho67": list(spectator_terms),
        "rho67_on_six_term_packet": "6 by 6 identity",
        "six_term_rank_preserved": 6,
        "conditional_cap_r0_row_order": list(row_order),
        "conditional_cap_r0_readout_per_term": list(map(int, per_term)),
        "conditional_six_term_aggregate": list(map(int, aggregate)),
        "readout_status": (
            "exact for the cap-internal r0 packet, conditional as the image "
            "of phi01 because phi01/Phi is not yet constructed"
        ),
        "pointed_quotient_row_order": ["P_f", "Q", "ores"],
        "pointed_conormal_P_f": list(map(int, p_f)),
        "primitive_cap_p": list(map(int, primitive_p)),
        "P_f_equals_primitive_p": False,
    }


def tree_gate_audit() -> dict[str, object]:
    tree = load(
        "computations/verify_h4_collision_ks_physical_site_permutation_tree_gate.py",
        "phi01_h4_tree_dependency",
    )
    ledger, digest = tree.audit()
    require(digest == tree.EXPECTED_LEDGER_SHA256,
            "h4 physical tree dependency ledger changed")
    root = ledger["root_Weyl_target_safe_aggregate"]
    require(root["target_safe_root_combination_rank"] == 14
            and root["chi_on_desired_fixed_tail_phi01"] == 1,
            "fixed-tail root aggregate changed")
    return {
        "existing_target_safe_root_rank_over_15_matchings": 14,
        "chi_match_on_existing_target_safe_roots": 0,
        "chi_match_on_fixed_tail_phi01": 1,
        "selector_construction_succeeds": False,
        "shortest_positive_input": "one source-valid Phi_KS,r0/P_f schema",
        "logical_scope": (
            "equivalence of the new operation-changing datum after exact "
            "fixed-tail restriction; canonical spectator Hasse faces are "
            "not counted as a second unknown theorem"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "h4 pointed phi01 fixed-tail h3 restriction gate",
        "pins": PINS,
        "pointed_selector_attempt": selector_attempt_audit(),
        "orbit_relative_PAComp_gate": orbit_relative_pacomp_audit(),
        "fixed_tail_chain_retraction": fixed_tail_chain_retraction_audit(),
        "normalized_mixed_map": normalized_mixed_map_audit(),
        "selected_db01_and_cap_readouts":
            selected_db01_and_cap_readout_audit(),
        "h4_tree_consequence": tree_gate_audit(),
        "verdict": (
            "The centered occurrence selector isolates the desired top "
            "coefficient but cannot build a physical phi01: two odd cut "
            "faces have dual value 90 and, even after granting both, the "
            "selected six-term db01 packet raises rank 183->184 with dual "
            "value 174.  Restriction along the common squarefree edge 67 is "
            "an exact chain retraction, preserves the six selected terms and "
            "all cap-r0 readouts, and kills only the explicit dq67 spectator "
            "Leibniz packet.  Orbit-relative site transport does not replace "
            "this fixed-source edge: honest pullback has zero boundary, while "
            "forgetting the object label imposes a fold that lowers H0.  "
            "Hence the operation-changing part of any monic "
            "fixed-tail phi01 is exactly a labelled instance of the unique "
            "h3 Phi_KS,r0/P_f map.  Conversely that map plus the displayed "
            "spectator Hasse face gives its relative fixed-tail prolongation."
        ),
        "scope": (
            "exact rational fixed-tail 67 restriction on one h4 overlap "
            "packet, retaining selected db01, operation, pointed-conormal and "
            "augmented cap rows.  It proves equivalence of the missing new "
            "source datum, not existence of Phi, a full absolute h4 cell "
            "without its known spectator Hasse totalization, or an all-h "
            "spectator-suspension theorem.  The six cap readouts are "
            "conditional images because the mixed physical map remains open."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h4 pointed phi01 restriction ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "selector", "restriction",
                                           "db01", "comparison"),
                        default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h4 pointed phi01 fixed-tail restriction ({arguments.mode}): PASS")
        print("centered selector physical lift: NO (db01 rank 183 -> 184)")
        print("orbit-relative transport sufficient for fixed PAComp: NO")
        print("rho67: exact chain retraction; six-term rank 6 -> 6")
        print("new phi01 datum: exactly one h3 Phi_KS,r0/P_f instance")
        print("Phi existence: OPEN")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
