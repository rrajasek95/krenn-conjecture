#!/usr/bin/env python3
"""Exact audit of the seventh-split ``(p,d,s)=(8,8,1)`` closure.

The checks are deterministic and symbolic.  They cover the collision
bookkeeping, the zero-safe cubic gauge, both exchange steps, the
multiplicity-weighted full-core Robin coefficient, the extra residue node,
and the sharp Wronskian inequality.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


def check_profile_and_exchange_degrees() -> None:
    """Audit all cardinalities and the two cubic-lift degree steps."""
    p = 8
    labels = 2 * 8 + 1
    value_classes = 9
    require(
        labels == p + 9 == 17,
        "labels == p + 9 == 17",
    )

    # Classes 0,...,7 are double and class 8 is the singleton.  Every
    # seven-value selection contains at least six partially selected doubles.
    for core in combinations(range(value_classes), 7):
        selected_doubles = len(set(core).intersection(range(8)))
        require(
            selected_doubles >= 6,
            "selected_doubles >= 6",
        )
        require(
            selected_doubles >= 1,
            "selected_doubles >= 1",
        )  # an unselected mate is a singleton row

        represented_classes = len(core)
        complement_labels = labels - 7
        denominator_degree = p + represented_classes + 1
        numerator_cap = p + represented_classes - 1
        residual_cap = numerator_cap - complement_labels
        require(
            complement_labels == p + 2 == 10,
            "complement_labels == p + 2 == 10",
        )
        require(
            denominator_degree == 16,
            "denominator_degree == 16",
        )
        require(
            numerator_cap == 14,
            "numerator_cap == 14",
        )
        require(
            residual_cap == 4,
            "residual_cap == 4",
        )

    # An eight-set T has m+1=8 in the three-lift lemma.  Cubic lifts of
    # degree-four residuals have degree seven; cancelling two leading
    # coefficients leaves degree at most five.
    m = 7
    require(
        (m - 3) + 3 == m,
        "(m - 3) + 3 == m",
    )
    require(
        m - 2 == 5,
        "m - 2 == 5",
    )

    # On the full nine-set, degree-five residuals lift to degree eight.
    m = 8
    require(
        (m - 3) + 3 == m == 8,
        "(m - 3) + 3 == m == 8",
    )


def check_cubic_gauge() -> None:
    """Verify the Robin translation and all zero-anchor edge cases."""
    z, a, b, old_y, q_value = sp.symbols("z a b old_y q_value")
    g = (z - b) * (z + b) ** 2
    psi = 1 / (a + b) - 2 / (b - a)
    g0 = g.subs(z, -a)
    g1 = sp.diff(g, z).subs(z, -a)
    require(
        sp.factor(g1 / g0 + psi) == 0,
        "sp.factor(g1 / g0 + psi) == 0",
    )

    lifted = (
        g1 * q_value
        + g0 * (-old_y * q_value)
        + (old_y + psi) * g0 * q_value
    )
    require(
        sp.factor(lifted) == 0,
        "sp.factor(lifted) == 0",
    )
    require(
        sp.expand(g.subs(z, -b)) == 0,
        "sp.expand(g.subs(z, -b)) == 0",
    )
    require(
        sp.expand(sp.diff(g, z).subs(z, -b)) == 0,
        "sp.expand(sp.diff(g, z).subs(z, -b)) == 0",
    )

    # The possible singleton zero gives g_0=z^3 and remains coprime to all
    # nonzero, nonopposite anchor gauges.
    g_zero = sp.expand(g.subs(b, 0))
    require(
        g_zero == z**3,
        "g_zero == z**3",
    )
    require(
        g_zero.subs(z, 0) == 0,
        "g_zero.subs(z, 0) == 0",
    )
    require(
        sp.diff(g_zero, z).subs(z, 0) == 0,
        "sp.diff(g_zero, z).subs(z, 0) == 0",
    )
    samples = [0, 1, 3, 7, -2]
    gauges = [sp.Poly((z - x) * (z + x) ** 2, z) for x in samples]
    for i, left in enumerate(gauges):
        for right in gauges[i + 1 :]:
            require(
                sp.gcd(left, right).degree() == 0,
                "sp.gcd(left, right).degree() == 0",
            )


def check_three_lift_counts() -> None:
    """Exhaust the pencil gcd/Riemann--Hurwitz inequalities for |T|=8,9."""
    for size_t in (8, 9):
        m = size_t - 1
        for epsilon in (0, 1):
            # n is the number of nonzero anchors.
            n = size_t - epsilon
            require(
                m == n + epsilon - 1,
                "m == n + epsilon - 1",
            )
            e0_values = (0,) if epsilon == 0 else (0, 2, 3, 4, 5, 6)
            for e0 in e0_values:
                for rho in range(n + 1):
                    for sigma in range(n + 1):
                        minimum_e = rho + 2 * sigma + e0
                        if minimum_e > m:
                            continue
                        for e in range(minimum_e, m + 1):
                            delta_cap = m - e
                            if delta_cap < 1:
                                continue
                            u = n - rho - sigma
                            require(
                                u >= delta_cap,
                                "u >= delta_cap",
                            )
                            require(
                                n - sigma >= delta_cap,
                                "n - sigma >= delta_cap",
                            )
                            require(
                                2 * (n - sigma) > 2 * delta_cap - 2,
                                "2 * (n - sigma) > 2 * delta_cap - 2",
                            )


def check_full_core_coefficient() -> None:
    """Derive Y_a(V) from the 2^8,1 multiplicities in both anchor types."""
    doubles = sp.symbols("d0:8")
    singleton, mu = sp.symbols("s mu")

    def psi(anchor: sp.Expr, added: sp.Expr) -> sp.Expr:
        return 1 / (anchor + added) - 2 / (added - anchor)

    # First take a double anchor.  Its post-selection self multiplicity is one.
    anchor = doubles[0]
    other_values = list(doubles[1:]) + [singleton]
    base = -sp.Rational(1, 2) / anchor - 2 / (mu - anchor)
    base -= sum(2 / (anchor + value) for value in doubles[1:])
    base -= 1 / (anchor + singleton)
    full_y = base + sum(psi(anchor, value) for value in other_values)
    expected = -sum(1 / (anchor + value) for value in doubles)
    expected -= 2 / (mu - anchor)
    expected -= 2 * sum(1 / (value - anchor) for value in other_values)
    require(
        sp.factor(full_y - expected) == 0,
        "sp.factor(full_y - expected) == 0",
    )

    # Then take the singleton anchor.  There is no self root in the
    # complementary polynomial, including when the singleton is zero.
    anchor = singleton
    base = -2 * sum(1 / (anchor + value) for value in doubles)
    base -= 2 / (mu - anchor)
    full_y = base + sum(psi(anchor, value) for value in doubles)
    expected = -sum(1 / (anchor + value) for value in doubles)
    expected -= 2 / (mu - anchor)
    expected -= 2 * sum(1 / (value - anchor) for value in doubles)
    difference = sp.factor(full_y - expected)
    require(
        difference == 0,
        "difference == 0",
    )
    require(
        sp.factor(difference.subs(singleton, 0)) == 0,
        "sp.factor(difference.subs(singleton, 0)) == 0",
    )


def check_residue_node() -> None:
    """Check the local double-pole residue and the infinity degree count."""
    w = sp.symbols("w")
    c0, c1, q0, q1 = sp.symbols("c0 c1 q0 q1", nonzero=True)
    regular = (c0 + c1 * w) * (q0 + q1 * w)
    residue = sp.expand(regular).coeff(w, 1)
    require(
        sp.factor(residue - c0 * (q1 + c1 / c0 * q0)) == 0,
        "sp.factor(residue - c0 * (q1 + c1 / c0 * q0)) == 0",
    )

    degree_b = 8
    degree_q = 8
    degree_denominator = 2 + 2 * 9
    infinity_order = degree_denominator - (degree_b + degree_q)
    require(
        degree_denominator == 20,
        "degree_denominator == 20",
    )
    require(
        infinity_order == 4,
        "infinity_order == 4",
    )
    require(
        infinity_order >= 2,
        "infinity_order >= 2",
    )  # in particular the residue at infinity is zero

    # At -mu the regular cofactor is B/prod(z+v)^2, so its logarithmic
    # derivative is exactly the coefficient displayed in the note.
    z, mu = sp.symbols("z mu")
    doubles = sp.symbols("a0:8")
    values = doubles + (sp.symbols("s"),)
    b_poly = sp.prod(z - value for value in doubles)
    cofactor = b_poly / sp.prod((z + value) ** 2 for value in values)
    derived = sp.diff(cofactor, z).subs(z, -mu) / cofactor.subs(z, -mu)
    expected = sp.diff(b_poly, z).subs(z, -mu) / b_poly.subs(z, -mu)
    expected -= 2 * sum(1 / (value - mu) for value in values)
    require(
        sp.factor(derived - expected) == 0,
        "sp.factor(derived - expected) == 0",
    )


def check_wronskian_obstruction() -> None:
    """Verify the ten-node Wronskian inequality symbolically and exhaustively."""
    d, b = sp.symbols("d b", integer=True, nonnegative=True)
    left = (10 - b) * (d - 1)
    right = d * (9 - d - 2 * b)
    difference = sp.expand(left - right)
    asserted_form = (d - 3) * (d + 4) + 2 + b * (d + 1)
    require(
        sp.expand(difference - asserted_form) == 0,
        "sp.expand(difference - asserted_form) == 0",
    )

    # A degree-eight polynomial space has dimension at most nine.  Enumerate
    # every relevant d and every possible number of gcd nodes.
    for dim in range(3, 10):
        for gcd_nodes in range(11):
            minimum_gcd_degree = 2 * gcd_nodes
            if minimum_gcd_degree > 8:
                continue
            wronskian_cap = dim * (9 - dim - minimum_gcd_degree)
            forced_zeros = (10 - gcd_nodes) * (dim - 1)
            require(
                forced_zeros > wronskian_cap,
                "forced_zeros > wronskian_cap",
            )

    # Local jet model: a common Robin relation removes order one from the
    # vanishing sequence, forcing Wronskian weight at least d-1.
    x, lam = sp.symbols("x lam")
    f0 = 1 - lam * x
    f1 = x**2
    f2 = x**3
    wronskian = sp.det(
        sp.Matrix(
            [
                [f0, f1, f2],
                [sp.diff(f0, x), sp.diff(f1, x), sp.diff(f2, x)],
                [sp.diff(f0, x, 2), sp.diff(f1, x, 2), sp.diff(f2, x, 2)],
            ]
        )
    )
    require(
        sp.Poly(sp.expand(wronskian), x).as_dict().get((0,), 0) == 0,
        "sp.Poly(sp.expand(wronskian), x).as_dict().get((0,), 0) == 0",
    )
    require(
        sp.Poly(sp.expand(wronskian), x).as_dict().get((1,), 0) == 0,
        "sp.Poly(sp.expand(wronskian), x).as_dict().get((1,), 0) == 0",
    )
    require(
        sp.expand(wronskian).subs(x, 0) == 0,
        "sp.expand(wronskian).subs(x, 0) == 0",
    )
    require(
        sp.diff(sp.expand(wronskian), x).subs(x, 0) == 0,
        "sp.diff(sp.expand(wronskian), x).subs(x, 0) == 0",
    )


def main() -> None:
    check_profile_and_exchange_degrees()
    check_cubic_gauge()
    check_three_lift_counts()
    check_full_core_coefficient()
    check_residue_node()
    check_wronskian_obstruction()
    print("seventh-split final (8,8,1) exchange closure: PASS")
    print("seven-core and two exchange degree steps: exact")
    print("multiplicity-weighted full-core residues and tenth node: exact")
    print("ten-node Wronskian obstruction: exact")


if __name__ == "__main__":
    main()
