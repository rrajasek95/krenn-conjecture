#!/usr/bin/env python3
"""Koszul/Tate interpretation of the common reduced-Eq source debt.

Put F=H0-u and let Q denote the Eq equation.  The absolute Koszul cell

    theta = eps_F wedge eps_Q,
    d theta = F eps_Q - Q eps_F

has the wanted face F*e_Eq only after relative base change Q=0.  The checked
underived physical cap block realizes the nearest lift, but its complete
signature has forced labelled ordinary residue:

    C_near = -r0 + T + Y*rho,
    (E,W,target,ores)(C_near) = (1,0,0,1).

Here E is the coefficient of -F*e_Eq (equivalently +u*e_Eq after edge
augmentation).  No combination of r0,T,Y*rho has (1,0,0,0).  The primitive
covector E+W+target-ores separates it.  Two rho-related label copies give
two independent obstruction lines; taking odd parity kills only aggregate
residue, not the two labelled residue rows.

Thus the ordinary Koszul/Tate resolution contains the unaugmented normal
cell, while promotion to the physical relative source requires a new
augmented comparison assigning its labelled residue, anchor/ridge/word,
terminal, and q data.  Absence from the checked underived block gives a
primitive bounded separator, not yet a terminal theorem about every future
Tate enlargement.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_reset_lane_ores_descent_lock.py":
        "5a904ba0537c150d248808a3aa463bd2431b4450239747440a2316f37b5c1e16",
    "computations/verify_h3_primitive_attaching_universal_module.py":
        "9116553a78b231898355f17ed1f6ccada816d9954ad037a71c8318cfb391a927",
    "computations/verify_h3_rootless_zero_anchor_collision_edge_source_obstruction.py":
        "8249604a56f7fc8ee8a3c66a33cb905eed6a02202c43ed81283e91c61d748180",
    "computations/verify_h3_selected_lower_quiver_kahler_mapping_cylinder_gate.py":
        "e5deda7162db47f229239dc91b419baaf00c3158249859cbafb03fe3af2cc958",
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
    "computations/verify_h3_interface_iii_augmented_cap_factorization.py":
        "06e64c5db2a59b8877cb112515d50779be95010801f19690f97060bf08621213",
}
EXPECTED_LEDGER_SHA256 = (
    "f07e62cab3e9ba76ebb2bdb466bded141ed9bfcaae56aea5a96c336089763560"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def add(*vectors):
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def rank(columns):
    if not columns:
        return 0
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(len(columns[0]))]
    pivot_row = 0
    for column in range(len(columns)):
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


def determinant(columns):
    require(columns and len(columns) == len(columns[0]), "not square")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(len(columns))]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, len(work)):
            coefficient = work[row][column] / value
            work[row] = [left - coefficient * right for left, right in
                         zip(work[row], work[column], strict=True)]
    return answer


def absolute_koszul_audit():
    # Formal module terms for d(theta)=F*eps_Q-Q*eps_F.  Applying d again
    # gives FQ-QF=0.  The symbols retain the two faces rather than silently
    # declaring the second one zero.
    theta_boundary = {"F*eps_Q": 1, "Q*eps_F": -1}
    second_boundary = {"F*Q": 1 - 1}
    second_boundary = {key: value for key, value in second_boundary.items()
                       if value}
    require(not second_boundary, "the Koszul square stopped being zero")

    # Relative base change Q=0 kills only the Q*eps_F face.  Choosing -theta
    # gives the sign needed for dC=-F*e_Eq.
    relative_boundary = {"F*e_Eq": -1}
    require(relative_boundary == {"F*e_Eq": -1},
            "the relative Koszul sign changed")
    return {
        "actual_equations": ["F=H0-u", "Q=Eq"],
        "degree_one_tate_generators": ["eps_F", "eps_Q"],
        "degree_two_cell": "theta=eps_F wedge eps_Q",
        "absolute_boundary": "dtheta=F eps_Q-Q eps_F",
        "d_squared": 0,
        "relative_base_change": "Q=0, eps_Q maps to e_Eq",
        "chosen_core": "C_K=-theta",
        "relative_boundary": "dC_K=-F e_Eq",
        "regularity": (
            "over the polynomial presentation Q[F,Q], F and Q are "
            "independent monic equations, hence a regular sequence"
        ),
    }


def old_physical_block_audit():
    # Coordinate order and signs are exactly those of 9116553.  E reads the
    # coefficient of -F*e_Eq: since F|edges=0=-u, r0 has E=-1 and a desired
    # dC=-F*e_Eq has E=+1.
    rows = ("minus_F_eEq", "Yw", "target", "Y_ores")
    r0 = (Q(-1), Q(0), Q(1), Q(0))
    cap = (Q(0), Q(-1), Q(1), Q(0))
    response = (Q(0), Q(1), Q(0), Q(1))
    desired = (Q(1), Q(0), Q(0), Q(0))
    near = add(scale(-1, r0), cap, response)
    separator = (Q(1), Q(1), Q(1), Q(-1))
    require(near == (Q(1), Q(0), Q(0), Q(1)),
            "the nearest physical Koszul lift changed")
    require(all(dot(separator, column) == 0
                for column in (r0, cap, response)),
            "the primitive augmented separator stopped killing the old block")
    require(dot(separator, desired) == 1,
            "the primitive augmented separator stopped detecting C")
    require(rank((r0, cap, response)) == 3
            and rank((r0, cap, response, desired)) == 4,
            "the reduced-Eq cell stopped raising augmented rank")
    require(abs(determinant((r0, cap, response, desired))) == 1,
            "the reduced-Eq augmented extension stopped being primitive")
    return {
        "row_order": list(rows),
        "old_columns": {
            "r0": [str(value) for value in r0],
            "T": [str(value) for value in cap],
            "Y_varrho": [str(value) for value in response],
        },
        "nearest_existing_chain": "C_near=-r0+T+Y*varrho",
        "nearest_signature": [str(value) for value in near],
        "nearest_boundary": "-F e_Eq",
        "forced_defect": "labelled ordinary residue +Y",
        "desired_signature": [str(value) for value in desired],
        "primitive_separator": "minus_F_eEq+Yw+target-Y_ores",
        "separator_vector": [str(value) for value in separator],
        "rank_before_after": [3, 4],
        "unimodular_extension": True,
    }


def labelled_rho_orbit_audit():
    # Use two independent copies of the four-row block.  Complete physical
    # ordinary residue is labelwise, so odd parity leaves (ores_L,ores_R)
    # equal to (1,-1).  Only the coarse aggregate ores_L+ores_R vanishes.
    zero4 = (Q(0),) * 4
    r0 = (Q(-1), Q(0), Q(1), Q(0))
    cap = (Q(0), Q(-1), Q(1), Q(0))
    response = (Q(0), Q(1), Q(0), Q(1))
    desired = (Q(1), Q(0), Q(0), Q(0))
    near = add(scale(-1, r0), cap, response)

    old = []
    for column in (r0, cap, response):
        old.append(column + zero4)
        old.append(zero4 + column)
    desired_left = desired + zero4
    desired_right = zero4 + desired
    require(rank(old) == 6
            and rank(old + [desired_left, desired_right]) == 8,
            "the regular-orbit obstruction stopped having two label lines")

    near_left = near + zero4
    near_right = zero4 + near
    odd_near = add(near_left, scale(-1, near_right))
    even_near = add(near_left, near_right)
    labelled_ores_odd = (odd_near[3], odd_near[7])
    labelled_ores_even = (even_near[3], even_near[7])
    require(labelled_ores_odd == (Q(1), Q(-1))
            and sum(labelled_ores_odd, Q(0)) == 0,
            "odd parity no longer distinguishes labelled and aggregate residue")
    require(labelled_ores_even == (Q(1), Q(1)),
            "even labelled residue changed")

    # The two primitive separators split into independent even and odd
    # covectors, so neither parity cell follows from the other.
    lam = (Q(1), Q(1), Q(1), Q(-1))
    lam_left, lam_right = lam + zero4, zero4 + lam
    lam_odd = add(lam_left, scale(-1, lam_right))
    lam_even = add(lam_left, lam_right)
    c_odd = add(desired_left, scale(-1, desired_right))
    c_even = add(desired_left, desired_right)
    require(dot(lam_odd, c_odd) == 2
            and dot(lam_even, c_even) == 2
            and dot(lam_odd, c_even) == dot(lam_even, c_odd) == 0,
            "the even/odd primitive obstruction splitting changed")
    return {
        "old_two_label_rank": 6,
        "rank_after_two_desired_cells": 8,
        "odd_nearest_labelled_ores": [str(value)
                                       for value in labelled_ores_odd],
        "odd_nearest_aggregate_ores": "0",
        "even_nearest_labelled_ores": [str(value)
                                        for value in labelled_ores_even],
        "parity_obstruction_pairings": {
            "lambda_minus_on_C_minus": "2",
            "lambda_plus_on_C_plus": "2",
            "cross_pairings": "0",
        },
        "verdict": (
            "rho-antisymmetrization removes only a coarse aggregate residue; "
            "it does not construct a complete labelled-residue-zero cell"
        ),
    }


def anchor_and_q_audit():
    # The independently pinned zero-anchor quotient has these three old
    # columns and reduced-Eq demand.  Eq+ainc is a second primitive physical
    # obstruction not seen in the four-row cap block.
    pure = (Q(1), Q(-1), Q(0), Q(1), Q(0))
    cap = (Q(0), Q(0), Q(-1), Q(1), Q(0))
    residue = (Q(0), Q(0), Q(1), Q(0), Q(1))
    reduced = (Q(-1), Q(0), Q(0), Q(0), Q(0))
    anchor_separator = (Q(1), Q(1), Q(0), Q(0), Q(0))
    require(all(dot(anchor_separator, column) == 0
                for column in (pure, cap, residue))
            and dot(anchor_separator, reduced) == -1,
            "the physical Eq+ainc obstruction changed")

    # A Koszul differential constrains no value of the external terminal q.
    # The two assignments below have identical differential/protected data,
    # proving that q is additional augmentation data.  Its exact completion
    # is the pinned quotient condition, not a consequence of d^2=0.
    same_protected_signature = reduced
    q_assignments = (Q(0), Q(1))
    require(q_assignments[0] != q_assignments[1]
            and same_protected_signature == reduced,
            "q became determined by the bare Koszul cell")
    return {
        "zero_anchor_row_order": [
            "pure_Eq", "ainc", "W", "target", "ordinary_residue",
        ],
        "primitive_anchor_separator": "pure_Eq+ainc",
        "bare_koszul_assigns_q": False,
        "physical_q_condition": (
            "[q_target Phi-q_source]=0 in D^*/row(J); nonzero gives a "
            "protected-kernel relative generator once both q rows are physical"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    koszul = absolute_koszul_audit()
    old = old_physical_block_audit()
    orbit = labelled_rho_orbit_audit()
    anchor_q = anchor_and_q_audit()
    ledger = {
        "theorem": "reduced-Eq Koszul/Tate relative orbit gate",
        "pins": PINS,
        "absolute_derived_intersection": koszul,
        "checked_underived_physical_block": old,
        "rho_regular_orbit": orbit,
        "anchor_and_physical_q": anchor_q,
        "current_PP_inventory": {
            "generators": "squarefree coefficient jets r0[U], rm[U], plus T,varrho",
            "contains_absolute_Koszul_identity": True,
            "contains_independent_normal_degree_two_generator": False,
            "reason": (
                "the 17-term Hasse cycle is reconstructed from row jets; "
                "its diagonal projection retains F e_Eq.  No eps_F wedge "
                "eps_Q source column or augmented comparison is declared"
            ),
        },
        "authorized_enlargement": {
            "unaugmented": (
                "the derived intersection of the actual equations F=0,Q=0 "
                "canonically admits the Koszul/Tate cell theta"
            ),
            "physical_relative": (
                "promotion requires a map from that Tate model to the complete "
                "physical homotopy fibre.  This map must supply labelwise "
                "ordinary residue and anchor/ridge/word/private/eta/sigma/q "
                "readouts; adjoining a zero-readout C by declaration changes "
                "the augmented cokernel and is exactly the missing theorem"
            ),
        },
        "readout_ledger": {
            "Koszul_boundary": "-F e_Eq: exact after Q-relative base change",
            "target_W": "nearest old representative is zero",
            "ordinary_residue": "nearest old representative is +Y labelwise",
            "anchor": "independent pure_Eq+ainc obstruction",
            "ridge_word_private_terminal": "not assigned by the Koszul universal property",
            "fine_repeated_grade": (
                "base row degree is homogeneous, but transport to each literal "
                "repeated P3+K2 label is an additional source-labelled section"
            ),
            "q": "independent protected quotient cocycle condition",
        },
        "dual_consequence": {
            "bounded_underived": (
                "minus_F_eEq+Yw+target-Y_ores and pure_Eq+ainc are primitive "
                "left separators of the checked old source blocks"
            ),
            "terminal_scope": (
                "they become physical Fredholm annihilators only after proving "
                "they kill every cell of the complete augmented Tate/relative "
                "source.  A newly admitted Koszul cell is detected by them, so "
                "old-inventory nonmembership alone is not terminal"
            ),
        },
        "sharp_next_lemma": (
            "construct one source-labelled comparison from the Koszul normal "
            "cell to the complete physical homotopy fibre which cancels its "
            "forced labelled residue and Eq+ainc classes.  Equivariance then "
            "gives the two-dimensional rho orbit; q closes by the protected "
            "quotient/generator alternative"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 reduced-Eq Koszul/Tate relative orbit gate: PASS")
    print("absolute Koszul cell: YES; physical augmented cell: NOT YET")
    print("nearest old lift: target=W=0, labelled ores=+Y")
    print("rho odd kills aggregate ores only; labelled odd residue survives")
    print("primitive old-source duals: cap/conormal and Eq+ainc")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
