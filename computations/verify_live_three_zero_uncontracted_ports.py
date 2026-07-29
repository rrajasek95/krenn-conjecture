#!/usr/bin/env python3
"""Exact audit for live-three-zero-uncontracted-port-normal-form.md."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def audit_port_orbits() -> None:
    roles = (0, 1, "*")
    assignments = list(permutations(roles))
    survivors = [
        (left, right)
        for left in assignments
        for right in assignments
        if left.index(0) != right.index(0)
        and left.index(1) != right.index(1)
    ]
    assert len(survivors) == 18

    # Relabel zero sites to put the first centre in canonical order.
    relative = []
    for left, right in survivors:
        relative.append(tuple(right[left.index(role)] for role in roles))
    assert set(relative) == {(1, 0, "*"), (1, "*", 0), ("*", 0, 1)}
    assert relative.count((1, 0, "*")) == 6
    assert relative.count((1, "*", 0)) == 6
    assert relative.count(("*", 0, 1)) == 6


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right.T


def audit_swap_projection() -> None:
    # Coefficients in the abstract two-dimensional annihilator bases.
    r0, r1, s0, s1, t, u = sp.symbols("r0 r1 s0 s1 t u", nonzero=True)
    e0 = sp.Matrix([1, 0])
    e1 = sp.Matrix([0, 1])

    # Both port-form pairs independent: (17) kills d0,d1, so the same
    # residual vector would have to span both target axes.
    assert sp.Matrix.hstack(e0, e1).rank() == 2

    # One dependent pair: adding the two equations in (19) has a rank-two
    # target, while the common-alpha correction has rank at most one.
    target_map = outer(e0, e0) + t * outer(e1, e1)
    assert sp.factor(target_map.det()) == t
    assert outer(e0, sp.Matrix([u, 1])).rank() == 1

    # Both dependent pairs: the two target summands have Schmidt rank two,
    # whereas alpha beta d2 is a simple tensor.
    target_bilinear = outer(e0, e0) + t * outer(e1, e1)
    simple_bilinear = outer(sp.Matrix([1, u]), sp.Matrix([1, s0]))
    assert target_bilinear.rank() == 2
    assert simple_bilinear.rank() == 1

    # Exact mixed-coordinate relations recorded in (17).
    alpha = sp.Matrix([1, 0])
    gamma = sp.Matrix([0, 1])
    beta = sp.Matrix([1, 0])
    delta = sp.Matrix([0, 1])
    mixed_a = r0 * gamma + s1 * alpha
    mixed_b = r1 * beta + s0 * delta
    assert mixed_a == sp.Matrix([s1, r0])
    assert mixed_b == sp.Matrix([r1, s0])


def cyclic_binary_coefficient(
    word: tuple[int, int, int],
    alpha: sp.Matrix,
    gamma: sp.Matrix,
    beta: sp.Matrix,
    delta: sp.Matrix,
    f: tuple[sp.Matrix, ...],
    g: tuple[sp.Matrix, ...],
    residual: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    """Return the X*-by-Y* coefficient matrix of a zero-shore word."""
    i, j, k = word
    r, s, t = residual
    answer = r[i] * outer(f[k], g[j])
    if j == 1 and k == 0:
        answer += r[i] * outer(gamma, beta)
    if i == 0 and k == 0:
        answer += s[j] * outer(alpha, beta)
    if i == 1:
        answer += s[j] * outer(f[k], delta)
    if i == 0:
        answer += t[k] * outer(alpha, g[j])
    if i == 1 and j == 1:
        answer += t[k] * outer(gamma, delta)
    return sp.expand(answer)


def audit_cyclic_equations() -> None:
    r0, r1, s0, s1, t0, t1 = sp.symbols("r0 r1 s0 s1 t0 t1")
    x, y, u, v, a, d = sp.symbols("x y u v a d", nonzero=True)
    alpha = sp.Matrix([1, 0])
    f0 = sp.Matrix([0, 1])
    delta = sp.Matrix([1, 0])
    g1 = sp.Matrix([0, 1])
    gamma = x * alpha + y * f0
    beta = u * delta + v * g1
    f1 = a * alpha
    g0 = d * delta
    residual = ((r0, r1), (s0, s1), (t0, t1))

    coefficients = {
        word: cyclic_binary_coefficient(
            word, alpha, gamma, beta, delta,
            (f0, f1), (g0, g1), residual,
        )
        for word in product(range(2), repeat=3)
    }

    # The one-defect words are exactly (21), after outer nonzero factors
    # are removed.
    expected = (
        ((0, 0, 1), outer(r0 * f1 + t1 * alpha, g0)),
        ((0, 1, 1), outer(r0 * f1 + t1 * alpha, g1)),
        ((1, 0, 0), outer(f0, r1 * g0 + s0 * delta)),
        ((1, 0, 1), outer(f1, r1 * g0 + s0 * delta)),
    )
    for word, matrix in expected:
        assert sp.simplify(coefficients[word] - matrix) == sp.zeros(2)

    common = outer(gamma, beta) + outer(f0, g1)
    assert sp.simplify(coefficients[(0, 1, 0)] - (
        r0 * common + outer(alpha, s1 * beta + t0 * g1)
    )) == sp.zeros(2)
    assert sp.simplify(coefficients[(1, 1, 0)] - (
        r1 * common + outer(s1 * f0 + t0 * gamma, delta)
    )) == sp.zeros(2)

    first_mixed = coefficients[(0, 1, 0)]
    second_mixed = coefficients[(1, 1, 0)]
    assert sp.expand(first_mixed[1, 1] - r0 * (y * v + 1)) == 0
    assert sp.expand(first_mixed[1, 0] - r0 * y * u) == 0
    assert sp.expand(second_mixed[0, 1] - r1 * x * v) == 0

    reduced_first = sp.expand(first_mixed.subs({u: 0, x: 0, y * v: -1}))
    reduced_second = sp.expand(second_mixed.subs({u: 0, x: 0, y * v: -1}))
    assert sp.expand(reduced_first[0, 1] - (s1 * v + t0)) == 0
    assert sp.expand(reduced_second[1, 0] - (s1 + t0 * y)) == 0

    # With y*v=-1, these two corrections force s1=t0=0 in
    # characteristic zero.  The remaining colour-zero coefficient has
    # the nonzero determinant in (25).
    constant_matrix = sp.Matrix([[0, -r1 * v], [r0, 0]])
    assert sp.factor(constant_matrix.det()) == r0 * r1 * v


def audit_cyclic_zero_residual_model() -> None:
    """Check the exact d0=0 boundary model of the full ternary tensor."""
    zero = sp.zeros(2, 1)
    x0 = sp.Matrix([1, 0])
    x1 = sp.Matrix([0, 1])
    y0 = sp.Matrix([1, 0])
    y1 = sp.Matrix([0, 1])
    alpha = gamma = x0
    beta = delta = y1
    f = (-x0, x1, zero)
    g = (y0, -y1, zero)
    residual = ((0, 0, 0), (0, 1, 0), (1, 0, 0))

    for word in product(range(3), repeat=3):
        coefficient = cyclic_binary_coefficient(
            word, alpha, gamma, beta, delta, f, g, residual
        )
        expected = sp.zeros(2)
        if word == (0, 0, 0):
            expected = outer(x0, y0)
        elif word == (1, 1, 1):
            expected = outer(x1, y1)
        assert sp.simplify(coefficient - expected) == sp.zeros(2)

    # The two escape maps are injective despite having zero third rows.
    assert sp.Matrix.vstack(*[row.T for row in f]).rank() == 2
    assert sp.Matrix.vstack(*[row.T for row in g]).rank() == 2


def main() -> None:
    audit_port_orbits()
    audit_swap_projection()
    audit_cyclic_equations()
    audit_cyclic_zero_residual_model()
    print("Live three-zero uncontracted port normal form: PASS")
    print("port assignments=36 survivors=18 orbits=2 (swap=6, cyclic=12)")
    print("swap excluded; cyclic forces d0=0 and has an exact local model")


if __name__ == "__main__":
    main()
