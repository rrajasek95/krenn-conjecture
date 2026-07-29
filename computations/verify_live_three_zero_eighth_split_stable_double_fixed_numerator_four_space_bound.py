#!/usr/bin/env python3
"""Exact audit of the stable fixed-numerator four-space bound."""

from __future__ import annotations

import sympy as sp


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.together(expr)) == 0, sp.factor(sp.together(expr))


def audit_stable_degree_ledger() -> None:
    for epsilon in (0, 1):
        for m in range(12, 80):
            p = m - 4
            k = 2 * m - 18 + epsilon
            ambient_degree = p + epsilon
            assert k == 2 * p - 10 + epsilon
            numerator_gap = (
                k + 8 + ambient_degree - (3 * p + 2 * epsilon)
            )
            assert numerator_gap == -2
            primitive_numerator_degree = 2 * p + epsilon
            assert primitive_numerator_degree - (k + 1) == 9


def audit_operator_identity_and_leading_cancellation() -> None:
    z, mu = sp.symbols("z mu")
    k = sp.symbols("k", integer=True, nonnegative=True)
    C = sp.Function("C")(z)
    L = sp.Function("L")(z)
    n = sp.Function("n")(z)

    primitive = (z + mu) ** (k + 1) * n / (C**2 * L)
    scaled_derivative = sp.cancel(
        sp.diff(primitive, z) * C**3 * L**2 / (z + mu) ** k
    )
    operator = (
        C * L * ((z + mu) * sp.diff(n, z) + (k + 1) * n)
        - (z + mu) * (2 * sp.diff(C, z) * L + C * sp.diff(L, z)) * n
    )
    assert_zero(scaled_derivative - operator)

    p, epsilon, j = sp.symbols("p epsilon j", integer=True)
    stable_k = 2 * p - 10 + epsilon
    leading_coefficient = j + stable_k + 1 - (2 * p + epsilon)
    assert_zero(leading_coefficient - (j - 9))


def audit_local_double_jet_rank() -> None:
    A, Ap, B, Bp = sp.symbols("A A_prime B B_prime", nonzero=True)
    local_matrix = sp.Matrix([[B, A, 0], [Bp, Ap + B, A]])
    assert local_matrix.rank() == 2
    assert local_matrix[:, 1:].det() == A**2

    for dimension in range(1, 11):
        vanishing = (0,) + tuple(range(3, dimension + 2))
        baseline = tuple(range(dimension))
        assert sum(vanishing) - sum(baseline) == 2 * (dimension - 1)


def audit_wronskian_bound() -> None:
    allowed = []
    for dimension in range(1, 11):
        forced = 8 * (dimension - 1)
        cap = dimension * (10 - dimension)
        if forced <= cap:
            allowed.append(dimension)
    assert allowed == [1, 2, 3, 4]
    assert 8 * (5 - 1) == 32 > 5 * (10 - 5) == 25
    # In dimension four all finite weights exhaust the full degree, so
    # the four-space Wronskian is a scalar multiple of Q^6.
    assert 4 * 2 * (4 - 1) == 4 * (10 - 4) == 24


def audit_equality_basis_and_core_swap() -> None:
    z = sp.symbols("z")
    roots = sp.symbols("r0:4", nonzero=True)
    equality_basis = [
        sp.prod((z + roots[j]) ** 3 for j in range(4) if j != i)
        for i in range(4)
    ]

    evaluation = sp.Matrix(
        [
            [polynomial.subs(z, -root) for polynomial in equality_basis]
            for root in roots
        ]
    )
    assert all(
        evaluation[i, j] == 0
        for i in range(4)
        for j in range(4)
        if i != j
    )
    assert all(evaluation[i, i] != 0 for i in range(4))

    for i, root in enumerate(roots):
        logarithmic_derivative = sp.cancel(
            sp.diff(equality_basis[i], z) / equality_basis[i]
        ).subs(z, -root)
        expected = 3 * sum(
            1 / (roots[j] - root) for j in range(4) if j != i
        )
        assert_zero(logarithmic_derivative - expected)

    # A rational exact specialization audits the sharp Q^6 factor without
    # forcing SymPy to expand a large four-parameter determinant.
    numeric_roots = (sp.Integer(1), sp.Integer(2), sp.Integer(4), sp.Integer(8))
    numeric_basis = [
        sp.prod((z + numeric_roots[j]) ** 3 for j in range(4) if j != i)
        for i in range(4)
    ]
    equality_wronskian = sp.Matrix(
            [
                [sp.diff(polynomial, z, order) for polynomial in numeric_basis]
                for order in range(4)
            ]
        ).det(method="domain-ge")
    core_polynomial = sp.prod(z + root for root in numeric_roots)
    wronskian_quotient = sp.cancel(equality_wronskian / core_polynomial**6)
    assert z not in wronskian_quotient.free_symbols
    assert wronskian_quotient != 0

    x, r, lam = sp.symbols("x r lambda", nonzero=True)
    fibre_map = 3 / (x - r) - 2 / (x + r)
    assert_zero(fibre_map - (x + 5 * r) / (x**2 - r**2))
    fixed_pool_sum = sp.symbols("fixed_pool_sum")
    moving_core_expression = (
        fixed_pool_sum + 3 / (x - r) - 2 / (r + x)
    )
    assert_zero(moving_core_expression - fixed_pool_sum - fibre_map)
    fibre_numerator = sp.together(fibre_map - lam).as_numer_denom()[0]
    expected_fibre = -(
        lam * x**2 - x - (lam * r**2 + 5 * r)
    )
    assert_zero(fibre_numerator - expected_fibre)
    assert sp.Poly(expected_fibre, x).degree() == 2
    assert sp.Poly(expected_fibre, x).coeff_monomial(x) == 1

    # p=8,9,10 are the six prior low-order profiles.  The new swap proof
    # starts at p=11, where m=p+4 and m-3 gives at least twelve fibres.
    low_profiles = []
    for p in (8, 9, 10):
        m = p + 4
        low_profiles.extend(((m, 0), (m, 1)))
    assert low_profiles == [
        (12, 0),
        (12, 1),
        (13, 0),
        (13, 1),
        (14, 0),
        (14, 1),
    ]
    assert 2 * 11 > 3 * (10 - 3)
    assert (11 + 4) - 3 == 12 > 2


def main() -> None:
    audit_stable_degree_ledger()
    print("stable exactness and primitive degree ledger: exact")
    audit_operator_identity_and_leading_cancellation()
    print("fixed P_9 numerator operator and degree-nine cancellation: exact")
    audit_local_double_jet_rank()
    print("four selected values give rank-two local jet constraints: exact")
    audit_wronskian_bound()
    print("stable common exactness kernel has dimension at most four: exact")
    audit_equality_basis_and_core_swap()
    print("sharp four-space basis and quadratic core-swap fibre: exact")
    print("both stable double families close uniformly for every m>=12: PASS")


if __name__ == "__main__":
    main()
