#!/usr/bin/env python3
"""Separate the central Eq cell from the Interface-II anchor comparison.

The full-q Interface-II alternative has one survivor

    Lambda in row(A),       H not in row(A).

A bare central cell dK=-E has no source-domain map and therefore cannot
alter either membership.  A source comparison Phi:X->C does close the
survivor once it is anchor-faithful:

    D Phi = B A,            H-h Phi in row(A).

Indeed H not in row(A) supplies xi in ker(A) with H(xi)!=0.  Then Phi(xi)
is a central protected kernel vector and h(Phi(xi))=H(xi)!=0.  Thus the
survivor is exactly a visible central class, not an additional Hall case.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py":
        "f194101187d92255a8396b762769df2d3e058f0adc2072ae822da4881f1a4e3d",
    "computations/verify_h3_interface_ii_central_eq_conditional_assembly.py":
        "98108cd059d935315f78ffec20d9d36d4870baf1a33f9ad7dad9538e5691d855",
    "computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py":
        "a51b8f091a25624d17443c70ac70b60eb257c8b11dafb0b9ad3f17962dc07390",
    "computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py":
        "b30000bfe8383e1f254fb8fee4724cbd99d8f70a5e8447cffb1c9086a179aec0",
}
EXPECTED_LEDGER_SHA256 = (
    "153729f4238ba144abcac2e6ce93418798fb4869480a06e899a259f0c1d6f9bb"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


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


def nullspace(rows, width):
    if not rows:
        return tuple(tuple(Q(index == free) for index in range(width))
                     for free in range(width))
    reduced, pivots = rref(rows, width)
    free = tuple(column for column in range(width) if column not in pivots)
    basis = []
    for column in free:
        vector = [Q(0)] * width
        vector[column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][column]
        basis.append(tuple(vector))
    return tuple(basis)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def in_row_span(rows, target):
    width = len(target)
    old_rank = len(rref(rows, width)[1])
    new_rank = len(rref(tuple(rows) + (tuple(target),), width)[1])
    return old_rank == new_rank


def row_times_matrix(row, matrix):
    # matrix is written by rows: codomain coordinate x domain coordinate.
    if not matrix:
        return ()
    return tuple(sum(Q(row[index]) * Q(matrix[index][column])
                     for index in range(len(row)))
                 for column in range(len(matrix[0])))


def matrix_times_vector(matrix, vector):
    return tuple(dot(row, vector) for row in matrix)


def subtract(left, right):
    return tuple(Q(a) - Q(b) for a, b in zip(left, right, strict=True))


def audit_bare_central_cell_guard():
    # The exact survivor frozen by the full-q theorem.
    A = ((1, 0, 0),)
    H = (0, 1, 0)
    Lambda = (1, 0, 0)
    require(in_row_span(A, Lambda) and not in_row_span(A, H),
            "the Interface-II survivor guard changed")

    # Direct-sum an exact central two-term complex K -> E.  This kills E,
    # but supplies neither a map from X nor a new row on X.
    d_central = ((1,),)
    K = (1,)
    E = (1,)
    require(matrix_times_vector(d_central, K) == E,
            "the independent central Eq cell stopped being exact")
    require(in_row_span(A, Lambda) and not in_row_span(A, H),
            "a disjoint exact summand incorrectly changed source row space")
    return {
        "A": A,
        "H": H,
        "Lambda": Lambda,
        "central_complex": "K -> E is the identity",
        "E_is_exact": True,
        "survivor_after_direct_sum": True,
        "reason": "the bare central cell has no comparison map on X",
    }


def audit_anchor_faithful_landing():
    # X=Q^3, C=Q^2.  This is the smallest positive model of the theorem.
    A = ((1, 0, 0),)
    H = (0, 1, 0)
    Lambda = (1, 0, 0)
    Phi = (
        (1, 0, 0),
        (0, 1, 0),
    )
    D = ((1, 0),)
    B = ((1,),)
    h = (0, 1)

    # D Phi = B A, written rowwise in this one-row model.
    d_phi = row_times_matrix(D[0], Phi)
    b_a = row_times_matrix(B[0], A)
    require(d_phi == b_a, "the protected comparison square stopped commuting")
    h_phi = row_times_matrix(h, Phi)
    require(in_row_span(A, subtract(H, h_phi)),
            "the comparison stopped transporting the anchor modulo A")

    xi = next((vector for vector in nullspace(A, 3) if dot(H, vector)), None)
    require(xi is not None, "H not in row(A) lost its kernel witness")
    phi_xi = matrix_times_vector(Phi, xi)
    require(not any(matrix_times_vector(D, phi_xi))
            and dot(h, phi_xi) == dot(H, xi) != 0,
            "anchor-faithful comparison did not produce a visible central kernel")
    return {
        "Lambda_in_row_A": in_row_span(A, Lambda),
        "H_in_row_A": in_row_span(A, H),
        "chain_square": "D Phi=B A",
        "anchor_quotient_identity": "[H]=Phi^*[h] in X^*/row(A)",
        "xi": tuple(map(str, xi)),
        "Phi_xi_in_ker_D": True,
        "h_Phi_xi": str(dot(h, phi_xi)),
        "outcome": "nonzero central protected-kernel class",
    }


def audit_chain_square_without_anchor_law():
    # The chain square alone may collapse the H direction.  It therefore
    # does not imply the quotient identity or kill the survivor.
    A = ((1, 0, 0),)
    H = (0, 1, 0)
    Phi_dark = (
        (1, 0, 0),
        (0, 0, 0),
    )
    D = ((1, 0),)
    B = ((1,),)
    h = (0, 1)
    require(row_times_matrix(D[0], Phi_dark) == row_times_matrix(B[0], A),
            "the dark comparison square stopped commuting")
    h_phi = row_times_matrix(h, Phi_dark)
    require(not in_row_span(A, subtract(H, h_phi)),
            "the dark comparison unexpectedly transported H")
    xi = (0, 1, 0)
    require(not any(matrix_times_vector(D, matrix_times_vector(Phi_dark, xi)))
            and dot(h, matrix_times_vector(Phi_dark, xi)) == 0
            and dot(H, xi) == 1,
            "the collapse counterguard changed")
    return {
        "chain_square": True,
        "anchor_quotient_identity": False,
        "marked_H_kernel_direction_collapsed": True,
        "survivor_remains": True,
    }


def audit_sources_do_not_already_construct_the_law():
    central = (ROOT / (
        "computations/verify_h3_interface_ii_central_eq_conditional_assembly.py"
    )).read_text()
    hessian = (ROOT / (
        "computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py"
    )).read_text()
    theta = (ROOT / (
        "computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py"
    )).read_text()
    require("symbol_required = symbol_actual" in central
            and "residual[EQ] = Q(1)" in central,
            "the conditional central assembly stopped beginning after symbol comparison")
    require('"pure_Eq_projection": 0' in hessian
            and "off-diagonal response-to-Eq normal/mapping-cone map" in hessian,
            "the pinned response-to-Eq mismatch changed")
    require("K_Eq is central and only corrects" in theta
            and "source-labelled response-to-Eq attachment" in theta,
            "the pinned theta-versus-central distinction changed")
    return {
        "conditional_assembly_starts_after_response_comparison": True,
        "diagonal_Hasse_projection_to_reduced_Eq": 0,
        "theta_cannot_supply_anchor_arrow": True,
        "first_missing_physical_map": "off-diagonal response-to-Eq comparison",
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "Interface-II anchor-faithful central-comparison reduction",
        "pins": PINS,
        "bare_central_cell_guard": audit_bare_central_cell_guard(),
        "anchor_faithful_landing": audit_anchor_faithful_landing(),
        "chain_square_only_guard": audit_chain_square_without_anchor_law(),
        "existing_source_audit": audit_sources_do_not_already_construct_the_law(),
        "shortest_remaining_statement": (
            "construct a source-valid off-diagonal Phi with D Phi=B A and "
            "[H]=Phi^*[h_Eq] in X^*/row(A), in the common word/fine/repeated "
            "grade and with the complete q/terminal typing.  Then the sole "
            "survivor maps to an h_Eq-visible central protected kernel; the "
            "central generator/dual alternative closes it"
        ),
        "logical_scope": (
            "If 'central physical comparison' includes the anchor quotient "
            "identity, no separate Interface-II theorem remains.  A bare "
            "physical K_Eq boundary, the diagonal Hasse symbol, or the theta "
            "grade arrow does not include that identity"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("anchor-faithful comparison ledger changed", digest))
    return ledger, digest


def main():
    _, digest = audit()
    print("h3 Interface-II anchor-faithful central comparison: PASS")
    print("bare central Eq cell: survivor remains")
    print("chain square without anchor quotient law: survivor remains")
    print("anchor-faithful comparison: survivor becomes visible central kernel")
    print("remaining physical statement: [H]=Phi^*[h_Eq] mod row(A)")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
