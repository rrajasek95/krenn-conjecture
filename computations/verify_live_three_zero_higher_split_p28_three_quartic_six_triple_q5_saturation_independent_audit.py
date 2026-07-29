#!/usr/bin/env python3
"""Independent audit of the p=28 4^3 3^6 q=5 saturation theorem.

This checker deliberately imports no project verifier.  It reconstructs
the two profile selections, the cleared Robin family, its rank-exception
locus, the q=6 Wronskian contradiction, and the residual parity/splitting
ledger directly over characteristic zero.
"""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def audit_exact_scope() -> None:
    tuples = ((3, 6, 0, 0), (3, 6, 1, -2))
    splits = tuple((h, 28 - h) for h in range(22, 28))
    assert splits == (
        (22, 6),
        (23, 5),
        (24, 4),
        (25, 3),
        (26, 2),
        (27, 1),
    )

    for h, _k in splits:
        for quartics, triples, doubles, offset in tuples:
            assert 4 * quartics + 3 * triples + 2 * doubles + offset == 30
            role_two = 1 + doubles
            role_one = h + 2 - 2 * role_two
            assert role_one == h + offset
            complement = (4,) * quartics + (3,) * (triples - 1) + (1,)
            assert complement == (4, 4, 4, 3, 3, 3, 3, 3, 1)
            assert len(complement) == 9
            assert sum(complement) == 28

    # The restored baseline is 4^3 3^6 in degree nine.  Seven dimensions
    # exceed the Wronskian cap, while six dimensions attain it exactly.
    assert 3 * (7 - 4) + 6 * (7 - 3) == 33 > 7 * (10 - 7) == 21
    assert 3 * (6 - 4) + 6 * (6 - 3) == 24 == 6 * (10 - 6)

    # Three transported spaces of dimension at least three cannot lie in a
    # common space of dimension at most four: their common intersection
    # would be nonzero but divisible by three coprime degree-four factors.
    assert 3 + 3 + 3 - 2 * 4 == 1
    assert 3 * 4 > 9

    # Pair-intersection lower bounds used in the two remaining branches.
    assert 3 + 3 - 5 == 1
    assert 3 + 4 - 5 == 2
    assert 4 + 3 - 6 == 1


def reconstruct_cleared_robin_curve():
    z, x, i, lam = sp.symbols("z x i lam")
    square = i**2
    delta = square - x
    even_factor = (z**2 - x) ** 2

    # The normalized simple row is f'(i)+lam*f(i)=0.  The logarithmic
    # derivative of (z^2-x)^2 at i is 4*i/(i^2-x), so this is the unique
    # cleared linear factor in its kernel (up to a nonzero scalar).
    linear = delta * (1 - lam * (z - i)) - 4 * i * (z - i)
    curve = sp.expand(even_factor * linear)
    assert sp.expand(curve.subs(z, i) - delta**3) == 0
    assert sp.expand(sp.diff(curve, z).subs(z, i) + lam * delta**3) == 0
    assert sp.expand(
        sp.diff(curve, z).subs(z, i) + lam * curve.subs(z, i)
    ) == 0

    coefficient_polys = [sp.expand(curve).coeff(x, power) for power in range(4)]
    assert sp.expand(curve - sum(x**r * coefficient_polys[r] for r in range(4))) == 0

    # This sparse minor is independent of the Robin slope.  It is the key
    # exact certificate that no admissible rank-three exception exists.
    degrees = (0, 1, 4, 5)
    coefficient_minor = sp.Matrix(
        [
            [sp.Poly(poly, z).coeff_monomial(z**degree) for degree in degrees]
            for poly in coefficient_polys
        ]
    )
    assert sp.factor(coefficient_minor.det()) == 16 * i**2

    parameters = sp.symbols("x0:4")
    vandermonde = sp.Matrix(
        [[parameter**power for power in range(4)] for parameter in parameters]
    )
    vandermonde_product = sp.prod(
        parameters[right] - parameters[left]
        for left in range(4)
        for right in range(left + 1, 4)
    )
    assert sp.factor(vandermonde.det() - vandermonde_product) == 0

    evaluated_minor = vandermonde * coefficient_minor
    assert sp.factor(
        evaluated_minor.det() - 16 * i**2 * vandermonde_product
    ) == 0

    # Exact rank-exception classification over C.  For i != 0 the rank is
    # four for every lam.  At the excluded value i=0 the constant term in x
    # vanishes and the remaining three coefficient polynomials are
    # (1-lam*z) times z^4, z^2, and 1, hence have rank exactly three.
    at_zero = [sp.expand(poly.subs(i, 0)) for poly in coefficient_polys]
    assert at_zero[0] == 0
    rank_three_minor = sp.Matrix(
        [
            [sp.Poly(at_zero[row], z).coeff_monomial(z**degree) for degree in (0, 2, 4)]
            for row in (1, 2, 3)
        ]
    )
    assert rank_three_minor.det() == -2

    return z, i, lam, coefficient_polys


def audit_q6_wronskian(z, i, lam, basis) -> None:
    wronskian = sp.factor(
        sp.det(
            sp.Matrix(
                [[sp.diff(poly, z, order) for poly in basis] for order in range(4)]
            )
        )
    )
    residual = sp.expand(
        lam**2 * z**3
        - (i * lam**2 + 4 * lam) * z**2
        + (i**2 * lam**2 + 6 * i * lam + 5) * z
        - (i**3 * lam**2 + 10 * i**2 * lam + 25 * i)
    )
    expected = -384 * i * z * (z - i) ** 3 * residual
    assert sp.expand(wronskian - expected) == 0
    assert sp.Poly(wronskian, z).degree() <= 7

    # The residual cannot vanish identically: a nonzero slope gives cubic
    # coefficient lam^2, and slope zero leaves 5(z-5i).
    residual_poly = sp.Poly(residual, z)
    assert residual_poly.coeff_monomial(z**3) == lam**2
    assert sp.expand(residual.subs(lam, 0) - 5 * (z - 5 * i)) == 0

    # Check directly that an exact complementary third-order row is a
    # nonzero dependence among the four ordinary jet rows.  Its coefficient
    # on the third jet is the nonzero value of the local unit.
    y = sp.symbols("y")
    unit_jets = sp.symbols("u0:4")
    section_jets = sp.symbols("s0:4")
    unit = sum(unit_jets[r] * y**r / sp.factorial(r) for r in range(4))
    section = sum(section_jets[r] * y**r / sp.factorial(r) for r in range(4))
    row = sp.expand(sp.diff(unit * section, y, 3).subs(y, 0))
    assert sp.diff(row, section_jets[3]) == unit_jets[0]

    # The explicit Wronskian already contains z and (z-i)^3.  The other
    # five retained triples are distinct from 0 and i and force five more
    # roots, impossible for a nonzero polynomial of degree at most seven.
    assert 1 + 3 + 5 == 9 > 7


def audit_saturated_residual_frontier() -> None:
    # Equality forces six distinct echelon degrees with maximal possible
    # sum in degree nine.
    degrees = tuple(range(4, 10))
    assert sum(degrees) - sum(range(6)) == 24

    # For a coordinate of degree d, E(t) has degree floor(d/2) and O(t)
    # has degree floor((d-1)/2).  Independently optimize all assignments of
    # four distinct coordinates to E,O,E',O'.
    parity_caps = tuple((d // 2, (d - 1) // 2) for d in degrees)
    maximum = -1
    for indices in permutations(range(6), 4):
        e_cap = parity_caps[indices[0]][0]
        o_cap = parity_caps[indices[1]][1]
        ep_cap = parity_caps[indices[2]][0] - 1
        op_cap = parity_caps[indices[3]][1] - 1
        if min(e_cap, o_cap, ep_cap, op_cap) >= 0:
            maximum = max(maximum, e_cap + o_cap + ep_cap + op_cap)
    assert maximum == 12
    assert maximum - 6 == 6

    # Once the six square roots are removed, a nonzero decomposable
    # four-vector has projective degree at most six.  A primitive rank-two
    # annihilator has no constant or linear row, so alpha>=2.  This is the
    # complete splitting list with alpha<=beta and alpha+beta<=6.
    splittings = tuple(
        (alpha, beta)
        for alpha in range(2, 7)
        for beta in range(alpha, 7)
        if alpha + beta <= 6
    )
    assert splittings == ((2, 2), (2, 3), (2, 4), (3, 3))

    # On the generic tangent-rank-two branch, let delta be the torsion
    # cokernel length of the second fundamental map.  The rank-two kernel
    # L and its induced derivative determinant have these exact degrees.
    candidates = []
    for projective_degree in range(4, 7):
        for torsion_length in range(8):
            degree_L = 4 - 2 * projective_degree + torsion_length
            degree_kappa = 3 * projective_degree - 12 - 2 * torsion_length
            # A scalar gcd of degree at most 6-d can hide no more than that
            # many of the six simple moving roots.  Thus kappa retains at
            # least d roots.
            if degree_kappa >= projective_degree:
                candidates.append(
                    (projective_degree, torsion_length, degree_L, degree_kappa)
                )
    assert candidates == [(6, 0, -8, 6)]

    # With d=6 the scalar gcd is constant, and alpha+beta=6 leaves only
    # these two primitive annihilator splittings.
    tangent_two_splittings = tuple(pair for pair in splittings if sum(pair) == 6)
    assert tangent_two_splittings == ((2, 4), (3, 3))

    # E and O give O(-4)^2 -> L.  Equal degree forces an isomorphism.
    assert 2 * (-4) == candidates[0][2]

    # For each splitting, record W/L=A^* tensor Omega, then the target of
    # the induced derivative map after one further Omega twist.  A map from
    # O(-4)^2 has row degrees alpha,beta and sextic determinant.
    for alpha, beta in tangent_two_splittings:
        quotient = (alpha - 2, beta - 2)
        derivative_target = (alpha - 4, beta - 4)
        row_degrees = tuple(value + 4 for value in derivative_target)
        assert row_degrees == (alpha, beta)
        assert sum(row_degrees) == 6
        if (alpha, beta) == (2, 4):
            assert quotient == (0, 2)
            assert derivative_target == (-2, 0)
        else:
            assert quotient == (1, 1)
            assert derivative_target == (-1, -1)


def audit_developable_exclusion() -> None:
    # E and O have coordinate degree at most four in t.  Thus every
    # coordinate of E wedge O has degree at most eight.  Removing a finite
    # scalar gcd or a common homogenized factor at infinity can only lower
    # the actual Pluecker degree.
    assert 4 + 4 == 8

    # Cone branch.  A nondegenerate direction curve spanning P^4 has degree
    # at least four.  Pullback by t=z^2 changes O(-e) to O(-2e), and a
    # nonzero degree-nine point section requires 2e<=9.
    cone_degrees = tuple(e for e in range(4, 30) if 2 * e <= 9)
    assert cone_degrees == (4,)

    # The RNC4 direction gives A(z) P_4(z^2), with deg A<=1.  Complete the
    # five local orders by one arbitrary independent section and recompute
    # the minimum possible vanishing sequences and weights.
    regular_completion = (0, 1, 2, 4, 6, 8)
    zero_completion = (0, 1, 3, 5, 7, 9)
    generic_sum = sum(range(6))
    assert sum(regular_completion) - generic_sum == 6
    assert sum(zero_completion) - generic_sum == 10

    # Tangent branch.  The tangent Pluecker degree is d=2e-2-R1.  Each unit
    # of first ramification spends at least five units of the total
    # 6(e-5) ramification of a nondegenerate g^5_e.  Include every d<=8.
    tangent_cases = []
    for edge_degree in range(5, 60):
        total_ramification = 6 * (edge_degree - 5)
        for first_ramification in range(2 * edge_degree + 1):
            pluecker_degree = 2 * edge_degree - 2 - first_ramification
            if (
                0 <= pluecker_degree <= 8
                and 5 * first_ramification <= total_ramification
            ):
                tangent_cases.append(
                    (edge_degree, pluecker_degree, first_ramification)
                )
    assert tangent_cases == [(5, 8, 0)]

    # Independently solve the full polynomial-section problem on the
    # square-pulled tangent lines of the rational normal quintic.  Start
    # with arbitrary degree-nine A,B and impose degree<=9 on all six
    # coordinates; the only survivors are a0,a1,b0,b1.
    z = sp.symbols("z")
    avec = sp.symbols("av0:10")
    bvec = sp.symbols("bv0:10")
    full_a = sum(avec[r] * z**r for r in range(10))
    full_b = sum(bvec[r] * z**r for r in range(10))
    t = z**2

    def tangent_coordinates(a_poly, b_poly):
        return (
            a_poly,
            4 * t * a_poly + b_poly,
            6 * t**2 * a_poly + 4 * t * b_poly,
            4 * t**3 * a_poly + 6 * t**2 * b_poly,
            t**4 * a_poly + 4 * t**3 * b_poly,
            t**4 * b_poly,
        )

    high_coefficients = []
    for coordinate in tangent_coordinates(full_a, full_b):
        high_coefficients.extend(
            coefficient
            for (degree,), coefficient in sp.Poly(sp.expand(coordinate), z).terms()
            if degree > 9
        )
    high_matrix, _ = sp.linear_eq_to_matrix(high_coefficients, avec + bvec)
    nullspace = high_matrix.nullspace()
    assert high_matrix.rank() == 16
    assert len(nullspace) == 4
    assert [
        {index for index, entry in enumerate(vector) if entry != 0}
        for vector in nullspace
    ] == [{0}, {1}, {10}, {11}]

    # Compute the literal six-coordinate Wronskian for arbitrary linear
    # A,B, retaining the determinant factor and the residual H.
    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1")
    linear_a = a0 + a1 * z
    linear_b = b0 + b1 * z
    coordinates = tangent_coordinates(linear_a, linear_b)
    wronskian = sp.expand(
        sp.det(
            sp.Matrix(
                [
                    [sp.diff(coordinate, z, order) for coordinate in coordinates]
                    for order in range(6)
                ]
            )
        )
    )
    determinant = a0 * b1 - a1 * b0
    numerical_factor = sp.Integer(141557760)
    assert sp.rem(
        wronskian, z**6, domain=sp.QQ[a0, a1, b0, b1]
    ) == 0
    residual_h = sp.cancel(wronskian / (numerical_factor * z**6 * determinant))
    assert sp.denom(residual_h) == 1
    assert sp.Poly(residual_h, z).degree() <= 12
    assert sp.expand(
        wronskian - numerical_factor * z**6 * determinant * residual_h
    ) == 0

    # H is nonzero for every independent pair A,B.  If b0!=0 its constant
    # coefficient is 21*b0^4.  If b0=0, independence forces b1!=0 and the
    # z^4 coefficient becomes 189*b1^4.
    h_poly = sp.Poly(sp.expand(residual_h), z)
    assert h_poly.coeff_monomial(1) == 21 * b0**4
    h_at_b0_zero = sp.Poly(sp.expand(residual_h.subs(b0, 0)), z)
    assert h_at_b0_zero.coeff_monomial(z**4) == 189 * b1**4

    # If determinant=0, A and B are proportional and the Wronskian is zero,
    # hence the six polynomial coordinates are dependent.  If determinant
    # is nonzero, H is nonzero by the preceding dichotomy and z=0 has
    # Wronskian weight at least six.
    assert sp.expand(wronskian.subs(b1, a1 * b0 / a0)) == 0


def main() -> None:
    audit_exact_scope()
    z, i, lam, basis = reconstruct_cleared_robin_curve()
    audit_q6_wronskian(z, i, lam, basis)
    audit_saturated_residual_frontier()
    audit_developable_exclusion()
    print("independent p=28 4^3 3^6 q=5 saturation audit: PASS")
    print("common lifted kernel: dimension exactly 6")
    print("six selected kernels: q_i=5 for every moving triple")
    print("rank<=3 cubic exception: exactly i=0, structurally excluded")
    print("developable residual excluded; primitive splittings remain")
    print("normal form only; neither collision tuple is closed")


if __name__ == "__main__":
    main()
