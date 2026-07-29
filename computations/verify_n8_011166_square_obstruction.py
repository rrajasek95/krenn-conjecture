#!/usr/bin/env python3
"""Symbolic audit of the arbitrary-parameter square obstruction for 011166.

The exceptional union-five row has two crossed exact-double sites and a
four-site core consisting of the nonwitness and three singleton-0 sites.
After the common scalar-core reduction, the only possible two-support
escape in the four-cross response is a repeated source ``R`` satisfying

    Per_3(X,Y,R) = nu * e0^3

on the singleton triple.  This checker keeps every singleton-plane
parameter symbolic, verifies the unique solution, and verifies a mixed
word which rules out ``Per_4(X,Y,R,R) = lambda * e0^4``.  It also audits
the characteristic-zero injectivity used in the scalar-support argument.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def permanent_tensor(rows, alphabet_size: int):
    """Coefficient dictionary for one labeled source per row family."""

    site_count = len(rows)
    answer = {
        word: sp.Integer(0)
        for word in product(range(alphabet_size), repeat=site_count)
    }
    for assignment in permutations(range(site_count)):
        for word in answer:
            answer[word] += sp.prod(
                rows[assignment[site]][site][word[site]]
                for site in range(site_count)
            )
    return {word: sp.factor(value) for word, value in answer.items()}


def audit_triangle_map_injectivity() -> None:
    """Audit injectivity after putting each independent X,Y pair in a basis."""

    variables = sp.symbols("r0:6")
    X = ((1, 0),) * 3
    Y = ((0, 1),) * 3
    R = tuple(
        (variables[2 * site], variables[2 * site + 1])
        for site in range(3)
    )
    coefficients = permanent_tensor((X, Y, R), 2)
    matrix = sp.Matrix(
        [
            [sp.expand(coefficients[word]).coeff(variable)
             for variable in variables]
            for word in product(range(2), repeat=3)
        ]
    )
    assert matrix.rank() == 6
    # A fixed maximal minor makes the characteristic-zero point explicit.
    assert matrix[[1, 2, 3, 4, 5, 6], :].det() == -4


def audit_arbitrary_singleton_parameters() -> None:
    """Verify the pure triangle solution and every extra-anchor boundary."""

    A, B, C, D, U, V, nu = sp.symbols("A B C D U V nu")
    delta = C * V - D * U

    # Local coordinates are (e0,w), where w spans the common nonzero
    # quotient line at a singleton-0 site.  Site a is the selected p-side
    # 0-anchor, site b the selected q-side 0-anchor, and site c is entirely
    # general.  delta != 0 is exactly independence of X_c,Y_c.
    X = ((1, 0), (B, 1), (C, U))
    Y = ((A, 1), (1, 0), (D, V))
    R = (
        (nu * (A * U + V) / (2 * delta),
         U * nu / (2 * delta)),
        (-nu * (B * V + U) / (2 * delta),
         -V * nu / (2 * delta)),
        (nu / 2, 0),
    )

    triangle = permanent_tensor((X, Y, R), 2)
    for word, coefficient in triangle.items():
        expected = nu if word == (0, 0, 0) else 0
        assert sp.factor(coefficient - expected) == 0

    # Solve independently and verify that the displayed row is unique over
    # the field Q(A,B,C,D,U,V), subject only to delta != 0.
    variables = sp.symbols("z0:6")
    Z = tuple(
        (variables[2 * site], variables[2 * site + 1])
        for site in range(3)
    )
    generic = permanent_tensor((X, Y, Z), 2)
    equations = [
        sp.together(
            generic[word] - (nu if word == (0, 0, 0) else 0)
        )
        for word in product(range(2), repeat=3)
    ]
    solution = sp.solve(equations, variables, dict=True, simplify=False)
    assert len(solution) == 1
    for site in range(3):
        for coordinate in range(2):
            variable = variables[2 * site + coordinate]
            assert sp.factor(solution[0][variable] - R[site][coordinate]) == 0

    YRR = permanent_tensor((Y, R, R), 2)
    XRR = permanent_tensor((X, R, R), 2)
    all_transverse = (1, 1, 1)
    assert sp.factor(
        YRR[all_transverse]
        + U * V**2 * nu**2 / (2 * delta**2)
    ) == 0
    assert sp.factor(
        XRR[all_transverse]
        + U**2 * V * nu**2 / (2 * delta**2)
    ) == 0

    # If U,V are both nonzero, the corresponding open-k vector is a
    # nonzero scalar multiple of V X_k + U Y_k.  When the third singleton
    # itself is an additional p- or q-anchor, U=0 or V=0; the word 110
    # supplies a one-sided nonzero coefficient instead.
    boundary_word = (1, 1, 0)
    assert sp.factor(
        YRR[boundary_word].subs(U, 0) + nu**2 / (2 * C)
    ) == 0
    assert sp.factor(XRR[boundary_word].subs(U, 0)) == 0
    assert sp.factor(YRR[boundary_word].subs(V, 0)) == 0
    assert sp.factor(
        XRR[boundary_word].subs(V, 0) + nu**2 / (2 * D)
    ) == 0


def audit_squarefree_core_algebra() -> None:
    """Audit (7), the ``d=0`` certificate, and the final core collapse."""

    sites = tuple(range(4))
    q = {
        (i, j): sp.symbols(f"q{i}{j}")
        for i in sites for j in sites if i < j
    }
    p = sp.symbols("p0:4")
    r = sp.symbols("s0:4")
    edge_uv = sp.symbols("a")

    # A square-free polynomial is stored by its site-support bit mask.  This
    # keeps the zero-divisor step in Section 2 honest: overlapping monomials
    # are killed rather than treated as ordinary polynomial products.
    def sf_add(*polynomials):
        answer = {}
        for polynomial in polynomials:
            for mask, coefficient in polynomial.items():
                answer[mask] = sp.expand(answer.get(mask, 0) + coefficient)
        return {mask: coefficient for mask, coefficient in answer.items()
                if coefficient != 0}

    def sf_scale(scalar, polynomial):
        return {
            mask: sp.expand(scalar * coefficient)
            for mask, coefficient in polynomial.items()
            if coefficient != 0
        }

    def sf_mul(left, right):
        answer = {}
        for left_mask, left_coefficient in left.items():
            for right_mask, right_coefficient in right.items():
                if left_mask & right_mask:
                    continue
                mask = left_mask | right_mask
                answer[mask] = sp.expand(
                    answer.get(mask, 0)
                    + left_coefficient * right_coefficient
                )
        return {mask: coefficient for mask, coefficient in answer.items()
                if coefficient != 0}

    def sf_equal(left, right):
        masks = set(left) | set(right)
        return all(
            sp.expand(left.get(mask, 0) - right.get(mask, 0)) == 0
            for mask in masks
        )

    q_c = {
        (1 << i) | (1 << j): coefficient
        for (i, j), coefficient in q.items()
    }
    ell = {1 << i: p[i] for i in sites}
    emm = {1 << i: r[i] for i in sites}
    q_c_squared = sf_mul(q_c, q_c)
    q_c_ell = sf_mul(q_c, ell)
    ell_m = sf_mul(ell, emm)
    mixed_core = sf_add(ell_m, sf_scale(edge_uv, q_c))

    # Coefficients of Q_C L_u are exactly the four hafnians on u plus a
    # three-subset of C.
    for triple in product((0, 1), repeat=4):
        chosen = tuple(i for i, bit in enumerate(triple) if bit)
        if len(chosen) != 3:
            continue
        i, j, k = chosen
        mask = sum(1 << site for site in chosen)
        coefficient = q_c_ell[mask]
        expected = (
            q[min(i, j), max(i, j)] * p[k]
            + q[min(i, k), max(i, k)] * p[j]
            + q[min(j, k), max(j, k)] * p[i]
        )
        assert sp.expand(coefficient - expected) == 0

    # Coefficients of L_u L_v+a_uv Q_C are the four-site hafnians on
    # {u,v,i,j}.
    for i in sites:
        for j in sites:
            if i >= j:
                continue
            mask = (1 << i) | (1 << j)
            coefficient = mixed_core[mask]
            expected = p[i] * r[j] + p[j] * r[i] + edge_uv * q[i, j]
            assert sp.expand(coefficient - expected) == 0

    # Q_C^2/2 has the ordinary four-vertex hafnian as its sole coefficient.
    top = q[0, 1] * q[2, 3] + q[0, 2] * q[1, 3] + q[0, 3] * q[1, 2]
    assert q_c_squared == {15: 2 * top}

    # Exact ideal-membership certificate for the zero-divisor-sensitive
    # step in (8):
    #
    #   d Q_C^2 = Q_C(ell m+d Q_C) - (Q_C ell)m.
    #
    # Hence the last three equations of (7) imply d Q_C^2=0.  Since the
    # top coefficient of Q_C^2 is 2h != 0, they force d=0 and then ell m=0.
    d_q_squared = sf_scale(edge_uv, q_c_squared)
    certificate = sf_add(
        sf_mul(q_c, mixed_core),
        sf_scale(-1, sf_mul(q_c_ell, emm)),
    )
    assert sf_equal(d_q_squared, certificate)

    # Exhaust all nonempty support pairs for ell,m.  A coefficient with
    # exactly one structurally nonzero summand is already impossible when
    # all entries on the declared supports are nonzero.  The only pairs
    # without such a monomial obstruction have equal supports.  Three or
    # more common indices then give the inconsistent ratio cycle
    # r_i=-r_j=-r_k=-r_i in characteristic zero.
    nonempty_supports = tuple(
        frozenset(i for i in sites if mask >> i & 1)
        for mask in range(1, 1 << len(sites))
    )

    def has_monomial_obstruction(left_support, right_support):
        for i in sites:
            for j in sites:
                if i >= j:
                    continue
                first = i in left_support and j in right_support
                second = j in left_support and i in right_support
                if first != second:
                    return True
        return False

    structurally_possible = tuple(
        (left, right)
        for left in nonempty_supports
        for right in nonempty_supports
        if not has_monomial_obstruction(left, right)
    )
    assert all(left == right for left, right in structurally_possible)
    feasible_supports = tuple(
        (left, right)
        for left, right in structurally_possible
        if len(left) <= 2
    )
    assert feasible_supports == tuple(
        (support, support)
        for support in nonempty_supports
        if len(support) <= 2
    )
    # On a two-support {i,j}, the sole equation is precisely (22).
    li, lj, mi, mj = sp.symbols("li lj mi mj", nonzero=True)
    assert sp.solve(sp.Eq(li * mj + lj * mi, 0), li)[0] == -lj * mi / mj
    # On any three-support, the three pair equations force 2*r_i=0.
    ratio_matrix = sp.Matrix(((1, 1, 0), (1, 0, 1), (0, 1, 1)))
    assert ratio_matrix.det() == -2

    # Finally audit (25)--(26).  If ell=ell_k t_k with ell_k nonzero,
    # Q_C ell=0 has the three independent coefficients ell_k*q_ab,
    # ell_k*q_ac,ell_k*q_bc.  Killing them annihilates the sole coefficient
    # of Q_C^2/2.
    ell_k = sp.symbols("ell_k", nonzero=True)
    q_c_ell_k = sf_mul(q_c, {1: ell_k})
    assert q_c_ell_k == {
        0b0111: ell_k * q[1, 2],
        0b1011: ell_k * q[1, 3],
        0b1101: ell_k * q[2, 3],
    }
    assert sp.expand(top.subs({q[1, 2]: 0, q[1, 3]: 0, q[2, 3]: 0})) == 0


def main() -> None:
    audit_triangle_map_injectivity()
    audit_arbitrary_singleton_parameters()
    audit_squarefree_core_algebra()
    print("011166 triangle-map injectivity: exact PASS")
    print("arbitrary singleton-parameter square obstruction: exact PASS")
    print("square-free common-core coefficient algebra: exact PASS")


if __name__ == "__main__":
    main()
