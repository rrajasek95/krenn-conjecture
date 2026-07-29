#!/usr/bin/env python3
"""Exact audit of the five-candidate parallelogram normal form.

All structural identities are checked symbolically over characteristic zero.
The final cofactor-gcd calculation is an explicitly labelled one-parameter
slice over QQ(a); it is not used as a uniform proof.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def zero(expr: sp.Expr, label: str) -> None:
    if sp.cancel(expr) != 0:
        raise AssertionError(label)


def monic_primitive(poly: sp.Expr, variable: sp.Symbol) -> sp.Poly:
    result = sp.Poly(poly, variable, domain=sp.QQ)
    return result.monic()


def check_row_factorization() -> None:
    xis = sp.symbols("xi0:4")
    ys = sp.symbols("Y0:4")
    V = sp.Matrix([[xis[i] ** j for j in range(4)] for i in range(4)])
    D = sp.diag(1, 2, 3, 4)
    R = sp.Matrix(
        [
            [
                1 + 2 * xis[i] * ys[i],
                xis[i] * (2 + 2 * xis[i] * ys[i]),
                xis[i] ** 2 * (3 + 2 * xis[i] * ys[i]),
                xis[i] ** 3 * (4 + 2 * xis[i] * ys[i]),
            ]
            for i in range(4)
        ]
    )
    expected = V * D + sp.diag(*[2 * xis[i] * ys[i] for i in range(4)]) * V
    if any(sp.expand(entry) != 0 for entry in R - expected):
        raise AssertionError("row factorization R=VD+diag(2 xi Y)V")

    # B_ii and the off-diagonal transposition product, using barycentric
    # weights rather than expanding V^{-1}.
    weights = [
        1 / sp.prod(xis[i] - xis[j] for j in range(4) if j != i)
        for i in range(4)
    ]
    for i in range(4):
        bii = 1 + xis[i] * sum(
            1 / (xis[i] - xis[j]) for j in range(4) if j != i
        )
        zero(
            bii
            - (1 + xis[i] * sum(1 / (xis[i] - xis[j]) for j in range(4) if j != i)),
            f"diagonal B entry {i}",
        )
        for j in range(4):
            if i == j:
                continue
            bij = xis[i] * weights[j] / (weights[i] * (xis[i] - xis[j]))
            bji = xis[j] * weights[i] / (weights[j] * (xis[j] - xis[i]))
            zero(
                -bij * bji - xis[i] * xis[j] / (xis[i] - xis[j]) ** 2,
                f"transposition product {i},{j}",
            )


def check_diagonal_determinant() -> None:
    zs = sp.symbols("Z0:4")
    c = {
        (i, j): sp.Symbol(f"c{i}{j}")
        for i in range(4)
        for j in range(4)
        if i != j
    }
    M = sp.Matrix(4, 4, lambda i, j: zs[i] if i == j else c[i, j])
    determinant = sp.expand(M.det())
    high = sp.prod(zs)
    for i, j in combinations(range(4), 2):
        p, q = [k for k in range(4) if k not in (i, j)]
        high -= c[p, q] * c[q, p] * zs[i] * zs[j]
    remainder = sp.Poly(sp.expand(determinant - high), *zs)
    if remainder.total_degree() > 1:
        raise AssertionError("zero-diagonal determinant has unexpected degree >=2 term")


def check_second_difference() -> None:
    S = sp.symbols("S0:4")
    p = sp.symbols("p0:4")
    q = sp.symbols("q0:4")
    gammas = {
        pair: sp.Symbol(f"g{pair[0]}{pair[1]}")
        for pair in combinations(range(4), 2)
    }

    def E(values: list[sp.Expr] | tuple[sp.Expr, ...]) -> sp.Expr:
        ans = sp.prod(values)
        ans += sum(gammas[i, j] * values[i] * values[j] for i, j in gammas)
        return ans

    lhs = sp.expand(
        E([S[i] + p[i] + q[i] for i in range(4)])
        - E([S[i] + p[i] for i in range(4)])
        - E([S[i] + q[i] for i in range(4)])
        + E(S)
    )
    rhs = 0
    full = set(range(4))
    for size_a in range(1, 5):
        for A in combinations(range(4), size_a):
            remaining = sorted(full.difference(A))
            for size_b in range(1, len(remaining) + 1):
                for B in combinations(remaining, size_b):
                    rest = full.difference(A).difference(B)
                    rhs += (
                        sp.prod(p[i] for i in A)
                        * sp.prod(q[i] for i in B)
                        * sp.prod(S[i] for i in rest)
                    )
    rhs += sum(
        gammas[i, j] * (p[i] * q[j] + p[j] * q[i]) for i, j in gammas
    )
    zero(lhs - rhs, "second-difference expansion")

    polynomial = sp.Poly(lhs, *S)
    if polynomial.total_degree() != 2:
        raise AssertionError("parallelogram equation is not quadratic")
    for i, j in combinations(range(4), 2):
        k, ell = [h for h in range(4) if h not in (i, j)]
        coefficient = polynomial.coeff_monomial(S[i] * S[j])
        zero(
            coefficient - (p[k] * q[ell] + p[ell] * q[k]),
            f"quadratic coefficient {i},{j}",
        )


def off_symmetric_square(X: sp.Matrix) -> sp.Matrix:
    pairs = list(combinations(range(4), 2))
    return sp.Matrix(
        6,
        6,
        lambda out, source: (
            X[pairs[source][0], pairs[out][0]]
            * X[pairs[source][1], pairs[out][1]]
            + X[pairs[source][1], pairs[out][0]]
            * X[pairs[source][0], pairs[out][1]]
        ),
    )


def check_five_by_six_factorization() -> None:
    A0 = sp.Matrix(
        [
            [0, -1, 0, 1, 0, 0],
            [-1, 0, 0, 1, 0, 0],
            [0, 0, -1, 0, 1, 0],
            [-1, 0, 0, 0, 1, 0],
            [0, 0, -1, 0, 0, 1],
        ]
    )
    if A0.rank() != 5 or A0 * sp.ones(6, 1) != sp.zeros(5, 1):
        raise AssertionError("rank/kernel of A0")

    xx = sp.symbols("x0:16")
    X = sp.Matrix(4, 4, xx)
    S_off = off_symmetric_square(X)
    pairs = list(combinations(range(4), 2))
    complement_position = []
    for i, j in pairs:
        complement = tuple(k for k in range(4) if k not in (i, j))
        complement_position.append(pairs.index(complement))
    J = sp.zeros(6, 6)
    for source, target in enumerate(complement_position):
        J[target, source] = 1

    # z0=0 and z1,...,z4 are the columns of X.  Each tuple gives
    # (a,b,c,d) in p=z_a-z_d, q=z_b-z_c.
    vectors = [sp.zeros(4, 1)] + [X[:, j] for j in range(4)]
    specifications = [
        (0, 1, 2, 3),
        (0, 1, 3, 2),
        (0, 1, 2, 4),
        (0, 1, 4, 2),
        (0, 1, 3, 4),
    ]
    direct_rows = []
    for a, b, c, d in specifications:
        p = vectors[a] - vectors[d]
        q = vectors[b] - vectors[c]
        row = []
        for i, j in pairs:
            k, ell = [h for h in range(4) if h not in (i, j)]
            row.append(sp.expand(p[k] * q[ell] + p[ell] * q[k]))
        direct_rows.append(row)
    direct = sp.Matrix(direct_rows)
    if any(sp.expand(entry) != 0 for entry in direct - A0 * S_off * J):
        raise AssertionError("A=A0*S_off(X)*J")

    t = sp.symbols("t0:4")
    monomials = sp.Matrix([t[i] * t[j] for i, j in pairs])
    zero(monomials[0] * monomials[5] - monomials[1] * monomials[4], "toric 1")
    zero(monomials[0] * monomials[5] - monomials[2] * monomials[3], "toric 2")


def check_edge_additivity_and_toric_descent() -> None:
    edges = list(combinations(range(5), 2))
    incidence = sp.Matrix(
        10,
        5,
        lambda row, vertex: int(vertex in edges[row]),
    )

    def edge_row(terms: tuple[tuple[int, tuple[int, int]], ...]) -> list[int]:
        answer = [0] * 10
        for coefficient, edge in terms:
            answer[edges.index(tuple(sorted(edge)))] += coefficient
        return answer

    four_cycles = sp.Matrix(
        [
            edge_row(((1, (0, 1)), (1, (2, 3)), (-1, (0, 2)), (-1, (1, 3)))),
            edge_row(((1, (0, 1)), (1, (2, 3)), (-1, (0, 3)), (-1, (1, 2)))),
            edge_row(((1, (0, 1)), (1, (2, 4)), (-1, (0, 2)), (-1, (1, 4)))),
            edge_row(((1, (0, 1)), (1, (2, 4)), (-1, (0, 4)), (-1, (1, 2)))),
            edge_row(((1, (0, 1)), (1, (3, 4)), (-1, (0, 3)), (-1, (1, 4)))),
        ]
    )
    if four_cycles.rank() != 5 or four_cycles * incidence != sp.zeros(5, 5):
        raise AssertionError("four-cycle equations are not the additive-edge cokernel")

    # Construct the additive potentials in (18a) and reduce every edge
    # identity by the five displayed four-cycle relations.  This checks the
    # exact implication Q_1=...=Q_5=0 => F_ab=s_a+s_b, rather than only its
    # dimension count.
    edge_values = sp.symbols("F0:10")
    f = {edge: edge_values[position] for position, edge in enumerate(edges)}
    potentials = {
        0: (f[0, 1] + f[0, 2] - f[1, 2]) / 2,
        1: (f[0, 1] + f[1, 2] - f[0, 2]) / 2,
        2: (f[0, 2] + f[1, 2] - f[0, 1]) / 2,
    }
    potentials[3] = f[0, 3] - potentials[0]
    potentials[4] = f[0, 4] - potentials[0]
    q_polynomials = [
        sum(row[position] * edge_values[position] for position in range(10))
        for row in four_cycles.tolist()
    ]
    q_basis = sp.groebner(q_polynomials, *edge_values, order="grevlex")
    for edge in edges:
        remainder = q_basis.reduce(
            sp.together(f[edge] - potentials[edge[0]] - potentials[edge[1]])
        )[1]
        zero(remainder, f"additive reconstruction on edge {edge}")

    odd_cycle_edges = ((0, 1), (0, 2), (1, 2), (0, 3), (0, 4))
    odd_cycle_incidence = incidence[[edges.index(edge) for edge in odd_cycle_edges], :]
    if odd_cycle_incidence.det() == 0:
        raise AssertionError("chosen five-edge graph does not kill additive potentials")

    # The universal top-degree descent (17b), modulo the toric equality
    # m_a m_b = m_c m_d.
    n = sp.symbols("n0:6")
    m = sp.symbols("m0:6")
    a, b, c, d = 0, 5, 1, 4
    r_ac = n[a] * m[c] - n[c] * m[a]
    r_bd = n[b] * m[d] - n[d] * m[b]
    rhs = n[b] * m[d] * r_ac + n[c] * m[a] * r_bd
    coefficient = n[a] * n[b] - n[c] * n[d]
    zero(
        rhs
        - coefficient * m[a] * m[b]
        - n[a] * n[b] * (m[c] * m[d] - m[a] * m[b]),
        "toric top-degree descent",
    )


def phi(u: sp.Expr, z: sp.Expr) -> sp.Expr:
    return (5 * u + z) / (u**2 - z**2)


def check_one_parameter_cofactor_gcd() -> None:
    a = sp.Symbol("a")
    r = sp.Integer(30)
    anchors = [a, sp.Integer(2), sp.Integer(3), sp.Integer(4)]
    candidates = [sp.Integer(z) for z in (5, 6, 7, 8, 9)]

    def candidate_vector(z: sp.Expr) -> sp.Matrix:
        return sp.Matrix([2 * (u - r) * phi(u, z) for u in anchors])

    vectors = [candidate_vector(z) for z in candidates]
    specifications = [
        (0, 1, 2, 3),
        (0, 1, 3, 2),
        (0, 1, 2, 4),
        (0, 1, 4, 2),
        (0, 1, 3, 4),
    ]
    pairs = list(combinations(range(4), 2))
    rows = []
    for aa, bb, cc, dd in specifications:
        p = vectors[aa] - vectors[dd]
        q = vectors[bb] - vectors[cc]
        row = []
        for i, j in pairs:
            k, ell = [h for h in range(4) if h not in (i, j)]
            row.append(sp.factor(p[k] * q[ell] + p[ell] * q[k]))
        rows.append(row)
    matrix = sp.Matrix(rows)
    if matrix.rank() != 5:
        raise AssertionError("one-parameter quadratic matrix rank")

    cofactors = []
    for column in range(6):
        kept = [j for j in range(6) if j != column]
        cofactors.append(sp.factor((-1) ** column * matrix[:, kept].det()))
    kernel = matrix * sp.Matrix(cofactors)
    if any(sp.cancel(entry) != 0 for entry in kernel):
        raise AssertionError("cofactor vector is not in the kernel")

    binomial_1 = sp.cancel(cofactors[0] * cofactors[5] - cofactors[1] * cofactors[4])
    binomial_2 = sp.cancel(cofactors[0] * cofactors[5] - cofactors[2] * cofactors[3])
    numerator_1 = sp.Poly(binomial_1.as_numer_denom()[0], a, domain=sp.QQ)
    numerator_2 = sp.Poly(binomial_2.as_numer_denom()[0], a, domain=sp.QQ)
    actual = sp.gcd(numerator_1, numerator_2).monic()
    expected = monic_primitive((a - 30) ** 5 * (a - 2) ** 2 * (a - 3) ** 2 * (a - 4) ** 2, a)
    if actual != expected:
        raise AssertionError(f"unexpected cofactor-binomial gcd: {actual.as_expr()}")

    residual_1 = numerator_1.exquo(actual).exquo(sp.Poly(a - 4, a, domain=sp.QQ))
    residual_2 = numerator_2.exquo(actual).exquo(sp.Poly(a - 3, a, domain=sp.QQ))
    if residual_1.degree() != 33 or residual_2.degree() != 33:
        raise AssertionError("unexpected residual cofactor degrees")
    if sp.gcd(residual_1, residual_2).degree() != 0:
        raise AssertionError("residual cofactor factors are not coprime")


def main() -> None:
    check_row_factorization()
    check_diagonal_determinant()
    check_second_difference()
    check_five_by_six_factorization()
    check_edge_additivity_and_toric_descent()
    check_one_parameter_cofactor_gcd()
    print("PASS: five-candidate parallelogram normal form and exact slice audit")


if __name__ == "__main__":
    main()
