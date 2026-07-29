#!/usr/bin/env python3
"""Exact exchange identities and an n=6 finite-field Robin certificate.

The F_13 calculation is a diagnostic for the proposed uniform complex
classification.  It is not used as a proof over characteristic zero.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def check_gauge_exchange() -> None:
    """Audit the deletion gauge and the two one-anchor lifts."""
    z, a, b, c = sp.symbols("z a b c")

    def g(anchor: sp.Expr) -> sp.Expr:
        return (z - anchor) * (z + anchor) ** 2

    def psi(anchor: sp.Expr, moving: sp.Expr) -> sp.Expr:
        return 1 / (anchor + moving) - 2 / (moving - anchor)

    for moving in (a, b):
        logarithmic_derivative = sp.diff(g(moving), z) / g(moving)
        assert sp.factor(
            logarithmic_derivative.subs(z, -c) + psi(c, moving)
        ) == 0

    # If q has logarithmic derivative -(Y+psi(c,a)) at -c, q/g_a has
    # logarithmic derivative -Y.  Multiplication by g_b instead adds the
    # second anchor contribution to the Robin coefficient.
    Y = sp.symbols("Y")
    q_log = -(Y + psi(c, a))
    deleted_log = q_log - (sp.diff(g(a), z) / g(a)).subs(z, -c)
    lifted_log = q_log + (sp.diff(g(b), z) / g(b)).subs(z, -c)
    assert sp.factor(deleted_log + Y) == 0
    assert sp.factor(lifted_log + Y + psi(c, a) + psi(c, b)) == 0

    # At the newly added anchor b, g_b makes both the value and derivative
    # vanish, so the Robin condition is automatic.
    assert sp.expand(g(b).subs(z, -b)) == 0
    assert sp.expand(sp.diff(g(b), z).subs(z, -b)) == 0


def check_weighted_linear_generalization_fails() -> None:
    """The four-node weighted-linear certificate cannot extend to n=5."""
    c = sp.symbols("c")
    nodes = sp.symbols("t0:5")
    weights = [
        sp.prod(nodes[i] + nodes[j] for j in range(5) if j != i)
        for i in range(5)
    ]

    # h(z)=z-c gives the genuine factor-family translations
    # U_i=-h'(t_i)/h(t_i)=1/(c-t_i).
    weighted_sum = sum(
        weights[i] / (c - nodes[i]) for i in range(5)
    )
    for i in range(5):
        residue = sp.cancel((c - nodes[i]) * weighted_sum).subs(
            c, nodes[i]
        )
        assert sp.factor(residue - weights[i]) == 0

    # A node-only right side would make this function constant in c, which
    # is impossible because every displayed residue is structurally nonzero.
    numerical = weighted_sum.subs(
        dict(zip(nodes, [1, 2, 3, 4, 5]))
    )
    assert sp.factor(numerical.subs(c, 10) - numerical.subs(c, 11)) != 0


def differentiation_matrix(nodes: list[int], prime: int) -> sp.Matrix:
    """Nodal differentiation on polynomials of degree < len(nodes)."""

    def inverse(value: int) -> int:
        return pow(value % prime, -1, prime)

    size = len(nodes)
    derivatives = []
    for i in range(size):
        value = 1
        for j in range(size):
            if i != j:
                value = value * (nodes[i] - nodes[j]) % prime
        derivatives.append(value)

    matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i != j:
                matrix[i][j] = (
                    derivatives[i]
                    * inverse((nodes[i] - nodes[j]) * derivatives[j])
                ) % prime
        matrix[i][i] = -sum(matrix[i]) % prime
    return sp.Matrix(matrix)


def coefficient_polynomials(
    polynomial: sp.Poly,
    x: sp.Symbol,
    translations: tuple[sp.Symbol, ...],
    prime: int,
) -> list[sp.Expr]:
    """Group a multivariate polynomial by its exponent of x."""
    grouped = [sp.Integer(0)] * (polynomial.degree(x) + 1)
    for exponents, coefficient in polynomial.as_dict().items():
        term: sp.Expr = sp.Integer(int(coefficient))
        for variable, exponent in zip(translations, exponents[1:]):
            term *= variable**exponent
        grouped[exponents[0]] += term
    return [
        sp.Poly(value, *translations, modulus=prime).as_expr()
        for value in grouped
    ]


def check_n6_f13_ideal_equality() -> None:
    """Compare the full pencil ideal with the quadratic-kernel ideal."""
    prime = 13
    nodes = [1, 2, 3, 4, 5, 6]
    size = len(nodes)
    x = sp.symbols("x")
    translations = sp.symbols("u0:6")
    derivative = differentiation_matrix(nodes, prime)

    # The cleared row matrix is
    #   R(x)=(x^2-Z^2)(D+diag(U))-xI+3Z.
    cleared = sp.Matrix(
        size,
        size,
        lambda i, j: (x**2 - nodes[i] ** 2)
        * (derivative[i, j] + (translations[i] if i == j else 0))
        + ((-x + 3 * nodes[i]) if i == j else 0),
    )
    determinant = sp.Poly(
        cleared.det(method="domain-ge"),
        x,
        *translations,
        modulus=prime,
    )
    assert determinant.degree(x) <= 2 * size
    determinant_coefficients = coefficient_polynomials(
        determinant, x, translations, prime
    )

    # A factor-family kernel has q_x=g_x h with deg(h)<=2.  Its existence is
    # exactly rank((D+diag(U))|_{P_2})<3, i.e. all twenty 3 by 3 minors vanish.
    low_evaluation = sp.Matrix(
        [[1, node, node**2] for node in nodes]
    )
    low_robin = (derivative + sp.diag(*translations)) * low_evaluation
    low_minors = [
        sp.Poly(
            low_robin[list(rows), :].det(),
            *translations,
            modulus=prime,
        ).as_expr()
        for rows in combinations(range(size), 3)
    ]
    assert len(low_minors) == 20

    determinant_basis = sp.groebner(
        determinant_coefficients,
        *translations,
        modulus=prime,
        order="grevlex",
    )
    low_basis = sp.groebner(
        low_minors,
        *translations,
        modulus=prime,
        order="grevlex",
    )

    # These two exact containments prove equality of the two ideals at this
    # node tuple over F_13; no enumeration or random specialization is used.
    assert all(
        determinant_basis.reduce(minor)[1] == 0
        for minor in low_minors
    )
    assert all(
        low_basis.reduce(coefficient)[1] == 0
        for coefficient in determinant_coefficients
    )
    assert len(determinant_basis.polys) == 20
    assert len(low_basis.polys) == 20
    assert all(poly.total_degree() == 3 for poly in determinant_basis.polys)


def main() -> None:
    check_gauge_exchange()
    check_weighted_linear_generalization_fails()
    check_n6_f13_ideal_equality()
    print("higher-split Robin exchange identities: PASS")
    print("m=5 weighted-linear generalization: REFUTED by factor family")
    print("n=6, nodes 1..6 over F_13: determinant ideal = quadratic-kernel ideal")
    print("characteristic-zero uniform classification: OPEN")


if __name__ == "__main__":
    main()
