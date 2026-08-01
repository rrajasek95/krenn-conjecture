#!/usr/bin/env python3
"""Exact audits for the universal two-edge-star cofactor projection.

The proof is in ``notes/star-face-first-lift.md``, Sections 5--8.  This
checker verifies the exact annihilators, the nine-matching decomposition,
the common-pencil permanent identity in characteristic two, the rank-three
projected target minor, and a finite exhaustive shadow of the kernel lemma.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

from explore_star_cofactor_projection import (
    build_map,
    cross_span,
    kernel2,
)
from verify_valuation_rainbow_descent_cycle import perfect_matchings


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


RIGHT = (3, 4, 5)


def audit_exact_annihilator() -> None:
    x0, x1, x2 = sp.symbols("x0 x1 x2")
    row = sp.Matrix([x0, x1, x2])
    quotient = sp.Matrix([[x1, -x0, 0], [x2, 0, -x0]])
    require(
        quotient * row == sp.zeros(2, 1),
        "quotient * row == sp.zeros(2, 1)",
    )
    require(
        sp.factor(quotient[:, :2].det()) == x0 * x2,
        "sp.factor(quotient[:, :2].det()) == x0 * x2",
    )

    # The contraction of X_b B_c + Y_c C_b separates into two products,
    # each containing one of the two annihilator equations.
    xb = sp.symbols("X0:3")
    yc = sp.symbols("Y0:3")
    bc = sp.symbols("B0:3")
    cb = sp.symbols("C0:3")
    alpha = (xb[1], -xb[0], 0)
    beta = (yc[1], -yc[0], 0)
    contracted = sum(
        alpha[b] * beta[c] * (xb[b] * bc[c] + yc[c] * cb[b])
        for b, c in product(range(3), repeat=2)
    )
    require(
        sp.expand(contracted) == 0,
        "sp.expand(contracted) == 0",
    )


def audit_nine_matching_decomposition() -> None:
    nonstar = tuple(
        matching
        for matching in perfect_matchings()
        if (0, 1) not in matching and (0, 2) not in matching
    )
    with_12 = tuple(matching for matching in nonstar if (1, 2) in matching)
    cross = tuple(matching for matching in nonstar if (1, 2) not in matching)
    require(
        len(nonstar) == 9,
        "len(nonstar) == 9",
    )
    require(
        len(with_12) == 3,
        "len(with_12) == 3",
    )
    require(
        len(cross) == 6,
        "len(cross) == 6",
    )
    require(
        {
            tuple(next(v for v in RIGHT if (min(row, v), max(row, v)) in matching) for row in (0, 1, 2))
            for matching in cross
        } == set(permutations(RIGHT)),
        "{ tuple(next(v for v in RIGHT if (min(row, v), max(row, v...",
    )


def audit_common_pencil_identity() -> None:
    # Use three coordinates at each right-hand site.  Equality is checked as
    # a polynomial identity over F_2 for all 27 output coordinates.
    ell = {
        site: sp.symbols(f"l{site}_0:3")
        for site in RIGHT
    }
    em = {
        site: sp.symbols(f"m{site}_0:3")
        for site in RIGHT
    }
    row = {
        site: sp.symbols(f"r{site}_0:3")
        for site in RIGHT
    }
    alpha, beta, gamma, eta = sp.symbols("alpha beta gamma eta")

    def edge(first: int, second: int, i: int, j: int):
        return ell[first][i] * em[second][j] + em[first][i] * ell[second][j]

    def kernel_row(first: int, coordinate: int, left, right):
        return left * ell[first][coordinate] + right * em[first][coordinate]

    for output in product(range(3), repeat=3):
        coordinate = dict(zip(RIGHT, output))
        f_value = (
            row[3][coordinate[3]] * edge(4, 5, coordinate[4], coordinate[5])
            + row[4][coordinate[4]] * edge(3, 5, coordinate[3], coordinate[5])
            + row[5][coordinate[5]] * edge(3, 4, coordinate[3], coordinate[4])
        )
        permanent = 0
        for assigned in permutations(RIGHT):
            permanent += (
                row[assigned[0]][coordinate[assigned[0]]]
                * kernel_row(assigned[1], coordinate[assigned[1]], alpha, beta)
                * kernel_row(assigned[2], coordinate[assigned[2]], gamma, eta)
            )
        difference = sp.Poly(
            permanent + (alpha * eta + beta * gamma) * f_value,
            modulus=2,
        )
        require(
            difference.is_zero,
            "difference.is_zero",
        )

        # A common-pencil row is itself in the shared cofactor kernel.
        kernel_value = (
            kernel_row(3, coordinate[3], alpha, beta)
            * edge(4, 5, coordinate[4], coordinate[5])
            + kernel_row(4, coordinate[4], alpha, beta)
            * edge(3, 5, coordinate[3], coordinate[5])
            + kernel_row(5, coordinate[5], alpha, beta)
            * edge(3, 4, coordinate[3], coordinate[4])
        )
        require(
            sp.Poly(kernel_value, modulus=2).is_zero,
            "sp.Poly(kernel_value, modulus=2).is_zero",
        )


def audit_projected_target_rank() -> None:
    # These quotient matrices annihilate the torus rows x and y in
    # characteristic two.  A displayed 3 by 3 minor proves that the three
    # projected diagonal tensors are independent over every extension field.
    x0, x1, x2, y0, y1, y2 = sp.symbols("x0 x1 x2 y0 y1 y2")
    pi_x = sp.Matrix([[x1, x0, 0], [x2, 0, x0]])
    pi_y = sp.Matrix([[y1, y0, 0], [y2, 0, y0]])
    diagonal_columns = []
    for color in range(3):
        diagonal_columns.append(sp.kronecker_product(pi_x[:, color], pi_y[:, color]))
    flattening = sp.Matrix.hstack(*diagonal_columns)
    minor = sp.factor(flattening[[0, 1, 3], :].det())
    require(
        minor == -x0**2 * x1 * y0**2 * y2,
        "minor == -x0**2 * x1 * y0**2 * y2",
    )
    require(
        sp.expand(minor + x0**2 * x1 * y0**2 * y2) == 0,
        "sp.expand(minor + x0**2 * x1 * y0**2 * y2) == 0",
    )


def audit_kernel_lemma_f2_shadow() -> None:
    # Exhaust every nonzero 2 by 2 tensor triple over F_2.  This is not used
    # as a proof of Lemma 6.1, but independently catches its dimension and
    # permanent-rank conclusions in the smallest nontrivial spaces.
    dimension_counts = {0: 0, 1: 0, 2: 0}
    for r34, r35, r45 in product(range(1, 16), repeat=3):
        kernel = kernel2(build_map(r34, r35, r45), 6)
        dimension = len(kernel)
        require(
            dimension <= 2,
            "dimension <= 2",
        )
        dimension_counts[dimension] += 1
        elements = [0]
        for mask in range(1, 1 << dimension):
            value = 0
            for index, basis_vector in enumerate(kernel):
                if mask >> index & 1:
                    value ^= basis_vector
            elements.append(value)
        for p_family in product(elements, repeat=2):
            for q_family in product(elements, repeat=2):
                require(
                    cross_span(p_family, q_family) <= 1,
                    "cross_span(p_family, q_family) <= 1",
                )
    require(
        dimension_counts == {0: 2340, 1: 648, 2: 387},
        "dimension_counts == {0: 2340, 1: 648, 2: 387}",
    )


def audit_degenerate_incidence() -> None:
    # If a pencil space contained two coordinate axes, its incident torus
    # edge would have a zero row.  Hence each of the three spaces can contain
    # at most one axis, while the double-quotient condition demands that each
    # of three axes occur at least twice.
    for inclusions in product(range(4), repeat=3):
        # 0,1,2 encode the sole possible included axis; 3 encodes none.
        counts = [sum(choice == color for choice in inclusions) for color in range(3)]
        require(
            not all(count >= 2 for count in counts),
            "not all(count >= 2 for count in counts)",
        )


def main() -> None:
    audit_exact_annihilator()
    audit_nine_matching_decomposition()
    audit_common_pencil_identity()
    audit_projected_target_rank()
    audit_kernel_lemma_f2_shadow()
    audit_degenerate_incidence()
    print("verified exact row annihilation and the 3+6 decomposition of G")
    print("verified common-pencil kernel/permanent identities over F_2")
    print("verified projected target rank 3 versus projected hafnian rank 1")
    print("verified degenerate-branch coordinate-incidence contradiction")


if __name__ == "__main__":
    main()
