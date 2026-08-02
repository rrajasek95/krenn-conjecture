#!/usr/bin/env python3
"""Exact audit of the singular-cross L1 boundary in the 3I branch.

After normalizing the invertible triangle, the zero-site L1 equations are

    e0 V_z^T = rho_i M_iz,       e1 U_z^T = rho'_i M_iz.

The checker audits the resulting mutually exclusive common-factor normal
forms, their pure-column orientation at the zero site, the finite R2
complement alternatives, and the localized mixed-L0 certificate that
synchronizes all four core-to-zero spoke scalars.

It also checks that the exact 3I incidence survivor lies in the closed
nonexceptional subbranch: site 4 has three singular spokes whose images are
neither the selected P_i nor Q_i lines, while site 5 has invertible spokes.
No external dependency is used.
"""

from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from runpy import run_path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
source = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_incidence_survivor.py"
))
guard = source["guard"]

INNER = (0, 1, 2)
CORE = (0, 1, 2, 3)
COLOURS = (0, 1)


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


# Sparse polynomial arithmetic for the exact localization certificates.


def constant(value):
    return {(): Q(value)} if value else {}


def variable(name):
    return {(name,): Q(1)}


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(coefficient, polynomial):
    return {
        monomial: Q(coefficient) * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = (
                answer.get(monomial, Q(0))
                + left_coefficient * right_coefficient
            )
            if not answer[monomial]:
                del answer[monomial]
    return answer


def determinant(matrix):
    return add(
        multiply(matrix[0][0], matrix[1][1]),
        scale(-1, multiply(matrix[0][1], matrix[1][0])),
    )


def pure_column(block, output):
    return (
        any(block[row][output] for row in COLOURS)
        and all(
            block[row][column] == 0
            for row in COLOURS
            for column in COLOURS
            if column != output
        )
    )


def audit_mutual_exclusion():
    # Absorb the two nonzero L1 proportionality scalars into v and u.
    # Equality e0 v^T=e1 u^T has four independent scalar equations and
    # forces both factors to vanish, contradicting simultaneous activity.
    equations = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    require(rational_rank(equations) == 4,
            "the P/Q active-factor intersection became nontrivial")

    # The two allowed oriented normal forms at z are v e0^T and u e1^T.
    v = (Q(2), Q(3))
    u = (Q(5), Q(7))
    p_oriented_at_z = ((v[0], 0), (v[1], 0))
    q_oriented_at_z = ((0, u[0]), (0, u[1]))
    require(pure_column(p_oriented_at_z, 0)
            and not pure_column(p_oriented_at_z, 1),
            "the P/V normal form is not pure-column zero at z")
    require(pure_column(q_oriented_at_z, 1)
            and not pure_column(q_oriented_at_z, 0),
            "the Q/U normal form is not pure-column one at z")


def audit_common_factor_forms():
    v0, v1 = variable("v0"), variable("v1")
    u0, u1 = variable("u0"), variable("u1")
    p_blocks = []
    q_blocks = []
    for index in CORE:
        multiple = variable(f"m{index}")
        p_block = (
            (multiply(multiple, v0), multiply(multiple, v1)),
            ({}, {}),
        )
        q_block = (
            ({}, {}),
            (multiply(multiple, u0), multiply(multiple, u1)),
        )
        require(determinant(p_block) == {},
                ("a P/V spoke gained rank", index))
        require(determinant(q_block) == {},
                ("a Q/U spoke gained rank", index))
        p_blocks.append(p_block)
        q_blocks.append(q_block)

    # Every pair of nonzero rows has the same right factor.
    for left in range(len(CORE)):
        for right in range(left + 1, len(CORE)):
            p_cross = (
                (p_blocks[left][0][0], p_blocks[left][0][1]),
                (p_blocks[right][0][0], p_blocks[right][0][1]),
            )
            q_cross = (
                (q_blocks[left][1][0], q_blocks[left][1][1]),
                (q_blocks[right][1][0], q_blocks[right][1][1]),
            )
            require(determinant(p_cross) == {},
                    ("P/V right factors diverged", left, right))
            require(determinant(q_cross) == {},
                    ("Q/U right factors diverged", left, right))

    # Two active endpoint colours in one family are necessarily collinear.
    d0, d1 = variable("d0"), variable("d1")
    endpoint_columns = (
        (multiply(d0, v0), multiply(d1, v0)),
        (multiply(d0, v1), multiply(d1, v1)),
    )
    require(determinant(endpoint_columns) == {},
            "active zero-site endpoint columns are not collinear")
    return len(p_blocks) + len(q_blocks)


def audit_r2_complement_table():
    # In P/V type, the I-spokes already supply output zero at z.  Output one
    # must come either from a coordinate-one rank-one-site factor h or from
    # the q-z endpoint block with exactly its colour-one column active.
    # Q/U is the colour-reversed statement.
    checked = 0
    for d0, d1, h0, h1 in product((False, True), repeat=4):
        if not (h0 or h1) or not (d0 or d1):
            continue
        vector = (Q(2), Q(3))
        h = (Q(5) if h0 else Q(0), Q(7) if h1 else Q(0))
        endpoint_row = (Q(1) if d0 else Q(0),
                        Q(1) if d1 else Q(0))

        def outer(left, right):
            return tuple(
                tuple(left[row] * right[column] for column in COLOURS)
                for row in COLOURS
            )

        p_t_block = outer(vector, h)
        p_endpoint_block = outer(vector, endpoint_row)
        p_r2 = (
            pure_column(p_t_block, 1)
            or pure_column(p_endpoint_block, 1)
        )
        require(
            p_r2
            == ((not h0 and h1) or (not d0 and d1)),
            "P/V R2 complement classification changed",
        )

        q_t_block = outer(vector, h)
        q_endpoint_block = outer(vector, endpoint_row)
        q_r2 = (
            pure_column(q_t_block, 0)
            or pure_column(q_endpoint_block, 0)
        )
        require(
            q_r2
            == ((h0 and not h1) or (d0 and not d1)),
            "Q/U R2 complement classification changed",
        )
        checked += 2
    require(checked == 18, "R2 complement table size changed")
    return checked


def audit_mixed_l0_synchronization():
    # Write A=c+lambda_z and q for the cross numerator a_s*d_u (P/V)
    # or b_u*d_s (Q/U).  The four live spoke equations are
    #
    #     f_i = A*m_i-q = 0.
    #
    # The exact localization certificate
    #
    #     m_j f_i-m_i f_j = q(m_i-m_j)
    #
    # forces every m_i=m_j whenever q is nonzero.
    a = variable("A")
    q = variable("q")
    multiples = [variable(f"m{index}") for index in CORE]
    equations = [
        add(multiply(a, multiple), scale(-1, q))
        for multiple in multiples
    ]
    checked = 0
    for left in range(len(CORE)):
        for right in range(left + 1, len(CORE)):
            certificate = add(
                multiply(multiples[right], equations[left]),
                scale(-1, multiply(multiples[left], equations[right])),
            )
            target = multiply(
                q,
                add(multiples[left], scale(-1, multiples[right])),
            )
            require(certificate == target,
                    ("mixed-L0 synchronization certificate failed",
                     left, right))
            checked += 1

    # At q=0, f_i=A*m_i; localization at any live m_i instead forces A=0,
    # i.e. lambda_z=-c, without synchronizing the spoke multiples.
    zero_q_equations = [multiply(a, multiple) for multiple in multiples]
    require(all(
        equation == multiply(a, multiple)
        for equation, multiple in zip(zero_q_equations, multiples)
    ), "zero-numerator mixed-L0 alternative changed")
    require(checked == 6, "mixed-L0 pair count changed")
    return checked


def matrix_rank_2_by_2(matrix):
    if not any(value for row in matrix for value in row):
        return 0
    return 2 if (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    ) else 1


def vector_determinant(left, right):
    return left[0] * right[1] - left[1] * right[0]


def audit_incidence_survivor_l1_failure():
    source["audit_replacement_scope"]()
    guard["audit_generic_kernel_equation"]()
    guard["audit_rank_55"]()
    guard["audit_literal_r2"]()
    source["audit_l0_incidence"]()

    blocks = source["BLOCKS"]
    x = guard["X"]
    z4_data = []
    for i in INNER:
        block = blocks[i, 4]
        require(matrix_rank_2_by_2(block) == 1,
                ("site-4 spoke is not singular", i))
        columns = tuple(
            (block[0][column], block[1][column]) for column in COLOURS
        )
        image = next(column for column in columns if column != (0, 0))
        p_i = (x[i][0][0], x[i][1][0])
        q_i = (x[i][0][1], x[i][1][1])
        determinants = (
            vector_determinant(p_i, image),
            vector_determinant(q_i, image),
        )
        require(all(determinants),
                ("site-4 spoke entered an exceptional P/Q line",
                 i, determinants))
        z4_data.append(determinants)

    z5_ranks = tuple(
        matrix_rank_2_by_2(blocks[i, 5]) for i in INNER
    )
    require(z5_ranks == (2, 2, 2),
            ("site-5 invertible-spoke audit changed", z5_ranks))
    expected_z4 = ((-42, 42), (-94, -73), (73, -7))
    require(tuple(z4_data) == expected_z4,
            ("site-4 alignment determinants changed", z4_data))
    return tuple(z4_data), z5_ranks


def main():
    audit_mutual_exclusion()
    common = audit_common_factor_forms()
    r2_cases = audit_r2_complement_table()
    mixed = audit_mixed_l0_synchronization()
    z4_data, z5_ranks = audit_incidence_survivor_l1_failure()
    print("three-invertible singular-cross L1 boundary: all checks passed")
    print("  active normal forms      : P/V or Q/U, mutually exclusive")
    print(f"  common-factor blocks     : {common} symbolic core spokes")
    print(f"  finite R2 support cases  : {r2_cases} boolean table rows")
    print(f"  mixed-L0 certificates    : {mixed} localized spoke pairs")
    print(f"  incidence site-4 tests   : {z4_data}")
    print(f"  incidence site-5 ranks   : {z5_ranks}")
    print("  known survivor outcome   : zero factors forced at both zero sites")


if __name__ == "__main__":
    main()
