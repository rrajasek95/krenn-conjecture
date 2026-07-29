#!/usr/bin/env python3
"""Exact audits for notes/two-vertex-annihilation-identities.md.

The script does not assume a numerical solution of the conjecture.  It
checks the matching decompositions for deterministic dense integer edge
matrices, checks the conditional target identities on the exact K4
three-color construction, and verifies the stated symbolic cross-product
and local factor formulas.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for j in range(1, len(vertices)):
        second = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def oriented(edges: dict[tuple[int, int], sp.Matrix], u: int, v: int):
    if u < v:
        return edges[(u, v)]
    return edges[(v, u)].T


def pair_value(
    edges: dict[tuple[int, int], sp.Matrix],
    covectors: dict[int, sp.Matrix],
    u: int,
    v: int,
):
    return (covectors[u].T * oriented(edges, u, v) * covectors[v])[0]


def contracted_hafnian(
    vertices: tuple[int, ...],
    edges: dict[tuple[int, int], sp.Matrix],
    covectors: dict[int, sp.Matrix],
):
    total = sp.Integer(0)
    for matching in perfect_matchings(vertices):
        term = sp.Integer(1)
        for u, v in matching:
            term *= pair_value(edges, covectors, u, v)
        total += term
    return sp.expand(total)


def partially_contracted_two_site(
    vertices: tuple[int, ...],
    holes: tuple[int, int],
    edges: dict[tuple[int, int], sp.Matrix],
    covectors: dict[int, sp.Matrix],
):
    """Contract all modes except two and return rows-at-hole0/cols-at-hole1."""
    w, z = holes
    out = sp.zeros(3, 3)
    for matching in perfect_matchings(vertices):
        term = sp.Integer(1)
        open_vectors: dict[int, sp.Matrix] = {}
        for u, v in matching:
            A = oriented(edges, u, v)
            if u in holes and v in holes:
                # This can only be the edge wz.
                open_vectors[-1] = A if (u, v) == (w, z) else A.T
            elif u in holes:
                open_vectors[u] = A * covectors[v]
            elif v in holes:
                open_vectors[v] = A.T * covectors[u]
            else:
                term *= (covectors[u].T * A * covectors[v])[0]
        if -1 in open_vectors:
            out += term * open_vectors[-1]
        else:
            out += term * open_vectors[w] * open_vectors[z].T
    return sp.expand(out)


K = (
    sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
    sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
    sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
)


def cross(a: sp.Matrix, b: sp.Matrix):
    """Cross product of two 3 by 1 coordinate columns."""
    return sp.Matrix(
        [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        ]
    )


def dense_integer_edges(vertices: tuple[int, ...]):
    edges = {}
    for u in vertices:
        for v in vertices:
            if u >= v:
                continue
            edges[(u, v)] = sp.Matrix(
                3,
                3,
                lambda i, j: ((11 * u + 7 * v + 5 * i + 3 * j + i * j) % 13)
                - 6,
            )
    return edges


def audit_orientation():
    alpha = sp.Matrix(sp.symbols("alpha0:3"))
    beta = sp.Matrix(sp.symbols("beta0:3"))
    ps = sp.symbols("p0:9")
    qs = sp.symbols("q0:9")
    P = sp.Matrix(3, 3, ps)
    Q = sp.Matrix(3, 3, qs)
    a = P.T * alpha
    b = Q.T * beta
    gamma = cross(a, b)
    assert sp.expand(a.dot(gamma)) == 0
    assert sp.expand(b.dot(gamma)) == 0
    for r in range(3):
        rhs = (alpha.T * P * K[r] * Q.T * beta)[0]
        assert sp.expand(gamma[r] - rhs) == 0


def audit_matching_decompositions():
    vertices = tuple(range(8))
    p, q = 0, 1
    outside = tuple(v for v in vertices if v not in (p, q))
    edges = dense_integer_edges(vertices)
    alpha = sp.Matrix([2, -1, 3])
    beta = sp.Matrix([-2, 5, 1])
    covectors = {p: alpha, q: beta}
    for u in outside:
        a = oriented(edges, p, u).T * alpha
        b = oriented(edges, q, u).T * beta
        covectors[u] = cross(a, b)

    g = pair_value(edges, covectors, p, q)
    full = contracted_hafnian(vertices, edges, covectors)
    residual = contracted_hafnian(outside, edges, covectors)
    assert full == sp.expand(g * residual)

    # One arbitrary hole: equation (14) on the matching side.
    w = outside[0]
    one_hole_covectors = dict(covectors)
    one_hole_covectors[w] = sp.Matrix([4, -3, 2])
    full_one = contracted_hafnian(vertices, edges, one_hole_covectors)
    residual_one = contracted_hafnian(outside, edges, one_hole_covectors)
    assert full_one == sp.expand(g * residual_one)

    # Two holes: equation (26) on the matching side.
    w, z = outside[:2]
    rest_covectors = {u: covectors[u] for u in outside[2:]}
    all_fixed = {p: alpha, q: beta, **rest_covectors}
    lhs = partially_contracted_two_site(vertices, (w, z), edges, all_fixed)
    quotient = partially_contracted_two_site(outside, (w, z), edges, rest_covectors)
    residual_vertices = outside[2:]
    h_s = contracted_hafnian(residual_vertices, edges, rest_covectors)
    xw = oriented(edges, p, w).T * alpha
    xz = oriented(edges, p, z).T * alpha
    yw = oriented(edges, q, w).T * beta
    yz = oriented(edges, q, z).T * beta
    correction = xw * yz.T + yw * xz.T
    rhs = sp.expand(g * quotient + h_s * correction)
    assert lhs == rhs
    assert correction.rank() <= 2


def k4_exact_solution():
    """The standard 1-factorization realization H_4=Delta_4,3."""
    edges = {(u, v): sp.zeros(3, 3) for u in range(4) for v in range(u + 1, 4)}
    matchings = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    for r, matching in enumerate(matchings):
        E = sp.zeros(3, 3)
        E[r, r] = 1
        for edge in matching:
            edges[edge] = E
    return edges


def audit_conditional_target_identities_on_k4():
    vertices = tuple(range(4))
    p, q = 0, 1
    outside = (2, 3)
    edges = k4_exact_solution()
    alpha = sp.Matrix([2, 3, 5])
    beta = sp.Matrix([7, 11, 13])
    gamma = {}
    for u in outside:
        a = oriented(edges, p, u).T * alpha
        b = oriented(edges, q, u).T * beta
        gamma[u] = cross(a, b)
    covectors = {p: alpha, q: beta, **gamma}
    g = pair_value(edges, covectors, p, q)

    target_no_hole = sum(
        alpha[r] * beta[r] * sp.prod(gamma[u][r] for u in outside)
        for r in range(3)
    )
    residual = contracted_hafnian(outside, edges, gamma)
    assert sp.expand(target_no_hole - g * residual) == 0

    for w in outside:
        delta_symbols = sp.symbols(f"d{w}_0:3")
        delta = sp.Matrix(delta_symbols)
        one = {outside[1] if w == outside[0] else outside[0]: gamma[outside[1] if w == outside[0] else outside[0]], w: delta}
        target = sum(
            alpha[r]
            * beta[r]
            * delta[r]
            * sp.prod(gamma[u][r] for u in outside if u != w)
            for r in range(3)
        )
        residual_one = contracted_hafnian(outside, edges, one)
        assert sp.expand(target - g * residual_one) == 0
        # Coefficient form (15).
        for r in range(3):
            lhs_coeff = alpha[r] * beta[r] * sp.prod(
                gamma[u][r] for u in outside if u != w
            )
            rhs_coeff = g * sp.expand(residual_one).coeff(delta_symbols[r])
            assert sp.expand(lhs_coeff - rhs_coeff) == 0

    # With both outside sites open, S is empty and h_empty=1.
    target_matrix = sp.diag(*[alpha[r] * beta[r] for r in range(3)])
    quotient = oriented(edges, outside[0], outside[1])
    xw = oriented(edges, p, outside[0]).T * alpha
    xz = oriented(edges, p, outside[1]).T * alpha
    yw = oriented(edges, q, outside[0]).T * beta
    yz = oriented(edges, q, outside[1]).T * beta
    correction = xw * yz.T + yw * xz.T
    assert target_matrix == sp.expand(g * quotient + correction)


def audit_cyclic_local_factorization():
    alpha = sp.Matrix(sp.symbols("x0:3"))
    beta = sp.Matrix(sp.symbols("y0:3"))
    I = sp.eye(3)
    R = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    star = (I, I, R, R, R**2, R**2)
    gammas = [cross(P.T * alpha, P.T * beta) for P in star]
    z = cross(alpha, beta)
    common = sp.prod(z[r] ** 2 for r in range(3))
    products = [sp.factor(sp.prod(gamma[r] for gamma in gammas)) for r in range(3)]
    assert all(sp.expand(value - common) == 0 for value in products)
    F = sum(alpha[r] * beta[r] * products[r] for r in range(3))
    assert sp.expand(F - common * alpha.dot(beta)) == 0


def audit_rank_factor_formulas():
    alpha = sp.Matrix(sp.symbols("a0:3"))
    beta = sp.Matrix(sp.symbols("b0:3"))
    left = sp.Matrix([2, -1, 3])
    right = sp.Matrix([1, 4, -2])
    d = sp.Matrix([5, 0, -3])
    c = sp.Matrix([-2, 7, 1])
    C_left = left * d.T
    C_right = c * right.T
    assert sp.expand((alpha.T * C_left * beta)[0] - alpha.dot(left) * d.dot(beta)) == 0
    assert sp.expand((alpha.T * C_right * beta)[0] - alpha.dot(c) * right.dot(beta)) == 0

    # Exhaustive small exact audit of the Sylvester consequence C=0 =>
    # rank(P[:,I])+rank(Q[:,I])<=2 for 2-column matrices.
    columns = [sp.Matrix(v) for v in product((-1, 0, 1), repeat=3)]
    J = sp.Matrix([[0, 1], [-1, 0]])
    checked = 0
    # A representative but exhaustive family with first columns selected
    # from all 27 possibilities and second columns from a fixed spanning set.
    seconds = [sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1]), sp.zeros(3, 1)]
    for p0 in columns:
        for p1 in seconds:
            P = p0.row_join(p1)
            for q0 in columns:
                for q1 in seconds:
                    Q = q0.row_join(q1)
                    if P * J * Q.T == sp.zeros(3, 3):
                        assert P.rank() + Q.rank() <= 2
                        checked += 1
    assert checked > 0


def audit_minimal_three_vertex_pattern():
    # sigma is the identity and tau is a derangement.  The cross matrix at
    # each shared neighbor vanishes in exactly the two assigned colors.
    sigma = (0, 1, 2)
    tau = (1, 2, 0)
    left_vectors = (
        sp.Matrix([1, 2, 0]),
        sp.Matrix([-1, 1, 3]),
        sp.Matrix([2, 0, 1]),
    )
    right_vectors = (
        sp.Matrix([3, -1, 1]),
        sp.Matrix([0, 2, 1]),
        sp.Matrix([1, 1, -2]),
    )
    for w in range(3):
        P = sp.zeros(3, 3)
        Q = sp.zeros(3, 3)
        P[:, sigma[w]] = left_vectors[w]
        Q[:, tau[w]] = right_vectors[w]
        zero_colors = []
        for r in range(3):
            C = P * K[r] * Q.T
            if C == sp.zeros(3, 3):
                zero_colors.append(r)
            else:
                assert C.rank() == 1
        assert set(zero_colors) == {sigma[w], tau[w]}


def main():
    audit_orientation()
    audit_matching_decompositions()
    audit_conditional_target_identities_on_k4()
    audit_cyclic_local_factorization()
    audit_rank_factor_formulas()
    audit_minimal_three_vertex_pattern()
    print("verified exact two-vertex annihilation identities")


if __name__ == "__main__":
    main()
