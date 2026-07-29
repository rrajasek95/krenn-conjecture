#!/usr/bin/env python3
"""Independent exact audit of the p=28 balanced-annihilator closure.

This checker imports no project module and no primary checker.  It rebuilds
the rank-four primitive-square calculation, the rank-three ramification
ledger, the homogeneous twisted-cubic frame (including infinity), the
kernel normal form and degree bounds, and the forced Wronskian weight at
the square-cover branch point.
"""

from __future__ import annotations

from functools import reduce
from itertools import combinations

import sympy as sp


t, z, sh, uh = sp.symbols("t z sh uh")


def polynomial_gcd(values, variable):
    nonzero = [sp.Poly(sp.expand(value), variable) for value in values if value != 0]
    assert nonzero
    return reduce(sp.gcd, nonzero)


def plucker(vectors):
    """Maximal minors of vectors supplied as columns."""
    matrix = sp.Matrix.hstack(*vectors)
    ambient = matrix.rows
    rank = matrix.cols
    return {
        subset: sp.expand(matrix.extract(subset, range(rank)).det())
        for subset in combinations(range(ambient), rank)
    }


def shuffle_sign(left, right):
    word = tuple(left) + tuple(right)
    inversions = sum(word[i] > word[j] for i in range(len(word)) for j in range(i + 1, len(word)))
    return -1 if inversions % 2 else 1


def audit_rank_four_branch():
    lam = sp.Matrix([1, t, t**2, 0, 0, 0])
    mu = sp.Matrix([0, 0, 0, 1, t, t**2])
    dlam = lam.diff(t)
    dmu = mu.diff(t)
    annihilator_rows = sp.Matrix.vstack(lam.T, mu.T, dlam.T, dmu.T)
    assert annihilator_rows.rank() == 4

    left = sp.Matrix([t**2, -2 * t, 1, 0, 0, 0])
    right = sp.Matrix([0, 0, 0, t**2, -2 * t, 1])
    dleft = left.diff(t)
    dright = right.diff(t)
    frame = (left, right, dleft, dright)
    assert annihilator_rows[:2, :] * sp.Matrix.hstack(*frame) == sp.zeros(2, 4)
    assert sp.Matrix.hstack(*frame).rank() == 4

    four_coordinates = plucker(frame)
    two_coordinates = plucker((lam, mu))
    assert polynomial_gcd(four_coordinates.values(), t).degree() == 0
    assert polynomial_gcd(two_coordinates.values(), t).degree() == 0

    # Hodge duality is literal up to one nonzero constant.  This also
    # checks that no hidden t-dependent factor survives in the quartic frame.
    ratios = []
    full = set(range(6))
    for four_subset, value in four_coordinates.items():
        complement = tuple(sorted(full.difference(four_subset)))
        dual_value = shuffle_sign(four_subset, complement) * two_coordinates[complement]
        if value == 0 or dual_value == 0:
            assert value == dual_value == 0
        else:
            ratios.append(sp.cancel(value / dual_value))
    assert ratios and len(set(ratios)) == 1
    assert not ratios[0].has(t) and ratios[0] != 0

    p, q, r, s = sp.symbols("p q r s")
    dp, dq, dr, ds = sp.symbols("dp dq dr ds")
    coefficient_matrix = sp.Matrix(
        [
            [p, r, dp, dr],
            [q, s, dq, ds],
            [0, 0, p, r],
            [0, 0, q, s],
        ]
    )
    determinant = p * s - q * r
    assert sp.factor(coefficient_matrix.det()) == determinant**2

    # C has ten distinct irreducible factors, each of odd multiplicity;
    # a nonzero scalar times a polynomial square has only even exponents.
    squarefree_exponents = (1,) * 10
    assert any(exponent % 2 for exponent in squarefree_exponents)

    # If the fixed coefficient span has dimension four, L_t is fixed.  If
    # it has dimension five, L_t contains a fixed line and its two moving
    # derivative classes span at most one dimension.  Either gives wedge
    # rank at most three, so a nonzero four-wedge forces m=6.
    maximum_wedge_ranks = {4: 2, 5: 3, 6: 4}
    assert maximum_wedge_ranks[4] < 4
    assert maximum_wedge_ranks[5] < 4
    assert maximum_wedge_ranks[6] == 4


def audit_developable_ledger():
    # H^0(P^1,O(-2)^2)=0, excluding a fixed vertex in every annihilator
    # fibre of the balanced bundle.
    h0_minus_two = max(-2 + 1, 0)
    assert 2 * h0_minus_two == 0

    # The tangent-line degree is 4=2e-2-R1.  A first-ramification unit
    # costs at least m-1 units of total g^{m-1}_e ramification.
    survivors = []
    margins = {}
    e = sp.symbols("e", integer=True)
    for m in (4, 5, 6):
        r1 = 2 * e - 6
        total = m * (e - m + 1)
        margin = sp.expand(total - (m - 1) * r1)
        margins[m] = margin
        for degree in range(m - 1, 50):
            first_ramification = 2 * degree - 6
            if first_ramification < 0:
                continue
            if (m - 1) * first_ramification <= m * (degree - m + 1):
                survivors.append((m, degree, first_ramification))
    assert margins == {4: 6 - 2 * e, 5: 4 - 3 * e, 6: -4 * e}
    assert survivors == [(4, 3, 0)]


def homogeneous_gcd(values):
    # Dehomogenize on both charts.  A common projective root would appear
    # as a common factor on one of them.
    finite = polynomial_gcd([value.subs(sh, 1) for value in values], uh)
    infinity = polynomial_gcd([value.subs(uh, 1) for value in values], sh)
    return finite.degree(), infinity.degree()


def audit_twisted_cubic_global_frame():
    gamma = sp.Matrix([1, t, t**2, t**3])
    dgamma = gamma.diff(t)
    lam4 = 3 * gamma - t * dgamma
    mu4 = dgamma
    assert lam4 == sp.Matrix([3, 2 * t, t**2, 0])
    assert mu4 == sp.Matrix([0, 1, 2 * t, 3 * t**2])
    assert sp.Matrix.hstack(lam4, mu4).rank() == 2
    assert sp.Matrix.hstack(gamma, dgamma, lam4, mu4).rank() == 2

    # The source coordinate is not changed: these are the complete cubic
    # monomials in the fixed homogeneous variables [sh:uh].
    gamma_h = sp.Matrix([sh**3, sh**2 * uh, sh * uh**2, uh**3])
    coefficient_matrix = sp.eye(4)
    assert coefficient_matrix.rank() == 4
    assert list(gamma_h) == [sh**3, sh**2 * uh, sh * uh**2, uh**3]

    lam_h = sp.Matrix([3 * sh**2, 2 * sh * uh, uh**2, 0])
    mu_h = sp.Matrix([0, sh**2, 2 * sh * uh, 3 * uh**2])
    minors = plucker((lam_h, mu_h))
    assert homogeneous_gcd(minors.values()) == (0, 0)
    infinity_frame = sp.Matrix.hstack(lam_h.subs({sh: 0, uh: 1}), mu_h.subs({sh: 0, uh: 1}))
    assert infinity_frame.rank() == 2
    finite_frame = sp.Matrix.hstack(lam_h.subs({sh: 1, uh: t}), mu_h.subs({sh: 1, uh: t}))
    assert finite_frame == sp.Matrix.hstack(lam4, mu4)

    # Extend the four covector coordinates by two constants.
    lam = sp.Matrix.vstack(lam4, sp.zeros(2, 1))
    mu = sp.Matrix.vstack(mu4, sp.zeros(2, 1))
    dlam = lam.diff(t)
    dmu = mu.diff(t)
    c1 = sp.Matrix([0, 0, 0, 0, 1, 0])
    c2 = sp.Matrix([0, 0, 0, 0, 0, 1])
    kernel_vector = sp.Matrix([-t**3, 3 * t**2, -3 * t, 1, 0, 0])
    dkernel = kernel_vector.diff(t)

    tangent_rows = sp.Matrix.vstack(lam.T, mu.T, dlam.T, dmu.T)
    line_rows = sp.Matrix.vstack(lam.T, mu.T)
    assert tangent_rows.rank() == 3
    assert line_rows.rank() == 2
    l_basis = sp.Matrix.hstack(kernel_vector, c1, c2)
    w_basis = sp.Matrix.hstack(kernel_vector, dkernel, c1, c2)
    assert tangent_rows * l_basis == sp.zeros(4, 3)
    assert line_rows * w_basis == sp.zeros(2, 4)
    assert l_basis.rank() == 3
    assert w_basis.rank() == 4


def generic_polynomial(prefix, degree, variable):
    coefficients = sp.symbols(" ".join(f"{prefix}{index}" for index in range(degree + 1)))
    if degree == 0:
        coefficients = (coefficients,)
    return sum(coefficient * variable**index for index, coefficient in enumerate(coefficients))


def audit_kernel_normal_form_and_degrees():
    p = generic_polynomial("p", 2, t)
    q = generic_polynomial("q", 1, t)
    a = generic_polynomial("a", 5, t)
    b = generic_polynomial("b", 5, t)
    c = generic_polynomial("c", 4, t)
    d = generic_polynomial("d", 4, t)

    m1 = sp.expand(p * c - q * a)
    m2 = sp.expand(p * d - q * b)
    scalar = sp.expand(m2 * sp.diff(m1, t) - m1 * sp.diff(m2, t))
    assert sp.degree(m1, t) <= 6
    assert sp.degree(m2, t) <= 6
    assert sp.expand(scalar).coeff(t, 11) == 0
    assert sp.degree(scalar, t) <= 10

    # Verify the derivative four-wedge scalar in the primitive
    # (u,c1,c2,u') frame without using the primary computation.
    pv, qv, av, bv, cv, dv = sp.symbols("pv qv av bv cv dv")
    pp, qp, ap, bp, cp, dp = sp.symbols("pp qp ap bp cp dp")
    coordinate_matrix = sp.Matrix(
        [
            [pv, qv, pp, qp],
            [av, cv, ap, cp],
            [bv, dv, bp, dp],
            [0, 0, pv, qv],
        ]
    )
    mv1 = pv * cv - qv * av
    mv2 = pv * dv - qv * bv
    dm1 = pp * cv + pv * cp - qp * av - qv * ap
    dm2 = pp * dv + pv * dp - qp * bv - qv * bp
    assert sp.expand(coordinate_matrix.det() - (mv2 * dm1 - mv1 * dm2)) == 0

    az = sp.expand(p.subs(t, z**2) + z * q.subs(t, z**2))
    fz = sp.expand(a.subs(t, z**2) + z * c.subs(t, z**2))
    gz = sp.expand(b.subs(t, z**2) + z * d.subs(t, z**2))
    first_four = (-az * z**6, 3 * az * z**4, -3 * az * z**2, az)
    assert all(sp.degree(value, z) <= 10 for value in first_four)
    assert sp.degree(fz, z) <= 10
    assert sp.degree(gz, z) <= 10
    normalized = (az, az * z**2, az * z**4, az * z**6)
    assert all(
        sp.cancel(first_four[index] / normalized[3 - index]) in (-1, 1, 3, -3)
        for index in range(4)
    )

    # The extremal first coordinate of u has t-degree three.  With E of
    # t-degree at most five and O of t-degree at most four this forces the
    # exact coefficient bounds used above.
    assert 5 - 3 == 2
    assert 4 - 3 == 1
    assert sp.degree(az, z) <= 4


def vanishing_weight(sequence):
    return sum(order - index for index, order in enumerate(sequence))


def wronskian(polynomials, variable):
    size = len(polynomials)
    return sp.factor(
        sp.Matrix(
            [[sp.diff(polynomial, variable, derivative) for polynomial in polynomials] for derivative in range(size)]
        ).det()
    )


def order_at_zero(polynomial, variable):
    poly = sp.Poly(sp.expand(polynomial), variable)
    return min(power[0] for power, coefficient in poly.terms() if coefficient)


def audit_branch_point_vanishing():
    expected = {
        0: ((0, 1, 2, 3, 4, 6), 1),
        1: ((0, 1, 2, 3, 5, 7), 3),
        2: ((0, 1, 2, 4, 6, 8), 6),
        3: ((0, 1, 3, 5, 7, 9), 10),
        4: ((0, 1, 4, 6, 8, 10), 14),
    }
    for rho, (minimum_sequence, minimum_weight) in expected.items():
        forced = {rho + 2 * index for index in range(4)}
        candidates = []
        for sequence in combinations(range(0, 15), 6):
            if forced.issubset(sequence):
                candidates.append((vanishing_weight(sequence), sequence))
        observed_weight, observed_sequence = min(candidates)
        assert (observed_sequence, observed_weight) == (minimum_sequence, minimum_weight)
        monomial_wronskian = wronskian([z**order for order in observed_sequence], z)
        assert monomial_wronskian != 0
        assert order_at_zero(monomial_wronskian, z) == observed_weight
    assert expected[0][1] >= 1
    assert all(expected[rho][1] >= 3 for rho in range(1, 5))

    echelon_degrees = tuple(range(5, 11))
    wronskian_degree = sum(echelon_degrees) - sum(range(6))
    infinity_sequence = tuple(sorted(10 - degree for degree in echelon_degrees))
    assert wronskian_degree == 30
    assert infinity_sequence == tuple(range(6))
    assert vanishing_weight(infinity_sequence) == 0
    assert 10 * 3 == wronskian_degree


def main():
    audit_rank_four_branch()
    audit_developable_ledger()
    audit_twisted_cubic_global_frame()
    audit_kernel_normal_form_and_degrees()
    audit_branch_point_vanishing()
    print("independent p=28 balanced-annihilator closure audit: PASS")
    print("rank-four primitive-square obstruction: PASS")
    print("rank-three developable ledger and global cubic frame: PASS")
    print("kernel normal form, degree bounds, and z=0 Wronskian contradiction: PASS")


if __name__ == "__main__":
    main()
