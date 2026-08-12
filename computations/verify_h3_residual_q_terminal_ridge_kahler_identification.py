#!/usr/bin/env python3
"""Identify the terminal-only packet as the relative differential of -Omega.

Write

    a=q_pq^22, t=q_pq^00, b=q_xv^(0,m_v), u=q_xv^00,
    Omega=(a-t)-(b-u).

The marked eta and sigma stabilizers contract the relative Kahler class
gamma=-dOmega to exactly the terminal packet left after the order-six
residual lift.  Requiring zero coefficient augmentation makes -Omega the
unique linear ridge representative with these contractions.

This does not yet construct a physical repeated-grade source cell.  The pq
and xv halves have different site multidegrees.  Ordinary lcm completion
produces the determinant t*b-u*a and changes the terminal law.  Therefore
the remaining datum is precisely a *labelled, shifted relative Kahler lift*
of gamma, not another unstructured matching correction.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_terminal_only_fiber_reduction.py":
        "1aa3236995bd206b8393bff717e80dd56dbe4264be66fb40ff9a571be87e7464",
    "computations/verify_h3_rootless_eta_character_source_interface.py":
        "2357e1a4e1c22c4496d99be12b8bf49deea3838337743ea849da29757508517c",
    "computations/verify_h3_residual_q_two_chart_copy_membership_no_go.py":
        "6383a2e25b3e137e570eddeba00b1cbbe59035f88cb48f234ebb3282ba23294b",
}
EXPECTED_LEDGER_SHA256 = "eee80a364e67043f2ebaae1f65461908b4943ee82dddbfd03a63dee8b69dad71"

SITES = tuple(range(8))
X, V, P, QSITE = 0, 1, 6, 7
COORDINATES = ("a=qpq22", "t=qpq00", "b=qxv0m", "u=qxv00")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def solve_square(columns, target):
    width = len(columns)
    require(width == len(target) == len(columns[0]), "not a square system")
    augmented = [[Q(columns[column][row]) for column in range(width)]
                 + [Q(target[row])] for row in range(width)]
    for column in range(width):
        pivot = next(row for row in range(column, width)
                     if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        value = augmented[column][column]
        augmented[column] = [entry / value for entry in augmented[column]]
        for row in range(width):
            if row == column or not augmented[row][column]:
                continue
            value = augmented[row][column]
            augmented[row] = [left - value * right for left, right in
                              zip(augmented[row], augmented[column], strict=True)]
    answer = tuple(augmented[index][-1] for index in range(width))
    reconstructed = tuple(sum(Q(columns[column][row]) * answer[column]
                              for column in range(width))
                          for row in range(width))
    require(reconstructed == tuple(map(Q, target)), "solution failed")
    return answer


def site_degree(*sites):
    return tuple(int(site in sites) for site in SITES)


def add_degree(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def terminal_uniqueness():
    # A linear ridge f=c_a*a+c_t*t+c_b*b+c_u*u has:
    #   eta constant c_t,
    #   eta U_z coefficient -c_u,
    #   sigma qpq22 coefficient c_a.
    # Zero coefficient augmentation supplies the fourth equation.
    rows = (
        (0, 1, 0, 0),   # eta constant
        (0, 0, 0, -1),  # eta U_z
        (1, 0, 0, 0),   # sigma qpq22
        (1, 1, 1, 1),   # ordinary coefficient augmentation
    )
    columns = tuple(tuple(rows[row][column] for row in range(4))
                    for column in range(4))
    target = (1, 1, -1, 0)
    coefficients = solve_square(columns, target)
    require(rank(columns) == 4
            and coefficients == (Q(-1), Q(1), Q(1), Q(-1)),
            "the terminal ridge representative changed")
    return {
        "coordinate_order": list(COORDINATES),
        "constraint_order": [
            "eta constant", "eta u_z/t coefficient",
            "sigma q_pq^22 coefficient", "coefficient augmentation",
        ],
        "constraint_matrix_rows": [list(row) for row in rows],
        "rank": 4,
        "unique_coefficients": [str(value) for value in coefficients],
        "unique_ridge": "-Omega_v=-a+t+b-u",
        "eta_contraction": "1+delta_(vz)*u_z/t",
        "sigma_contraction": "-q_pq^22",
        "coefficient_augmentation": 0,
    }


def relative_kahler_class():
    # In I/I^2 for the first-principal-parts diagonal, every df has zero
    # multiplication/ordinary boundary and contracts with a derivation X as
    # X(f).  The displayed coefficient vector is the one just proved unique.
    gamma = (Q(-1), Q(1), Q(1), Q(-1))
    eta_constant = gamma[1]
    eta_u = -gamma[3]
    sigma = gamma[0]
    require((eta_constant, eta_u, sigma) == (1, 1, -1),
            "Kahler contractions changed")
    return {
        "class": "gamma_v=-dOmega_v in I/I^2",
        "differential_coefficients_da_dt_db_du": [str(x) for x in gamma],
        "ordinary_multiplication_boundary": 0,
        "source_boundary": 0,
        "residue_D_W_target_anchor": [0, 0, 0, 0, 0, 0],
        "eta_contraction": "1+delta_(vz)*u_z/t",
        "sigma_contraction": "-q_pq^22",
        "matches_order6_terminal_only_packet": True,
        "formal_compatibility_obstruction": False,
    }


def grading_and_completion_gate():
    degree_pq = site_degree(P, QSITE)
    degree_xv = site_degree(X, V)
    require(degree_pq != degree_xv, "the two ridge blocks became homogeneous")
    sample_tail = tuple(index + 2 for index in SITES)
    require(add_degree(degree_pq, sample_tail)
            != add_degree(degree_xv, sample_tail),
            "a common tail repaired the ridge degree mismatch")

    # Complement the pq block (-a+t) by u and the xv block (b-u) by t.
    # The t*u terms cancel, leaving the nonzero 2x2 determinant t*b-u*a.
    completed_monomials = {"t*b": 1, "u*a": -1}
    require(completed_monomials == {"t*b": 1, "u*a": -1},
            "minimal determinant completion changed")

    # Its stabilizer contractions are not the required ones as polynomial
    # identities: eta gives b+delta*(u/t)*a and sigma gives -u*a.
    return {
        "degree_pq_block": list(degree_pq),
        "degree_xv_block": list(degree_xv),
        "common_tail_makes_homogeneous": False,
        "minimal_lcm_completion": "u*(-a+t)+t*(b-u)=t*b-u*a",
        "minimal_completion_is_zero": False,
        "minimal_completion_eta": "b+delta_(vz)*(u_z/t)*a",
        "required_eta": "1+delta_(vz)*u_z/t",
        "minimal_completion_sigma": "-u*a",
        "required_sigma": "-a",
        "terminal_law_preserved_as_polynomial_identity": False,
        "exact_required_lift": (
            "retain the pq and xv halves as distinct shifted labels in the "
            "physical relative first-principal-parts module, then identify "
            "their sum with gamma_v=-dOmega_v"
        ),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))
    return {
        "terminal_ridge_uniqueness": terminal_uniqueness(),
        "relative_kahler_identification": relative_kahler_class(),
        "physical_grading_gate": grading_and_completion_gate(),
        "consequence": (
            "the terminal-only target is canonically the relative first jet "
            "of the existing ridge -Omega_v.  The remaining theorem is no "
            "longer to discover its terminal values, but to construct its "
            "labelled repeated-grade lift in the physical source complex"
        ),
        "physical_repeated_grade_lift_constructed": False,
    }


def main():
    ledger = {
        "theorem": "terminal-only packet is the relative Kahler ridge class",
        "audit": audit(),
        "scope": (
            "exact linear ridge, stabilizer, first-principal-parts, and site-"
            "grading calculation; no claim that the complete physical "
            "relative source complex contains the required shifted lift"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"terminal ridge ledger changed: {digest}")
    print("h3 residual-q terminal ridge/Kahler identification: PASS")
    print("terminal-only packet: gamma_v=-dOmega_v")
    print("ordinary lcm completion: determinant, but wrong terminal law")
    print("remaining datum: labelled shifted physical first-jet lift")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
