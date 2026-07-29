#!/usr/bin/env python3
"""Exact audits for the crossed-double factor boundary on row 011166."""

from __future__ import annotations

import sympy as sp


EYE = sp.eye(3)
E = tuple(EYE[:, i] for i in range(3))
ZERO = sp.zeros(3)
ONES = sp.ones(3, 1)
K = (
    sp.Matrix(((0, 0, 0), (0, 0, 1), (0, -1, 0))),
    sp.Matrix(((0, 0, -1), (0, 0, 0), (1, 0, 0))),
    sp.Matrix(((0, 1, 0), (-1, 0, 0), (0, 0, 0))),
)
ALPHA = sp.Matrix(sp.symbols("alpha0:3"))
BETA = sp.Matrix(sp.symbols("beta0:3"))


def staircase(u, v, w):
    q = E[0] * E[0].T + E[1] * u.T + v * E[2].T
    p = E[1] * E[1].T - E[0] * u.T + w * E[2].T
    g = E[2] * E[2].T - E[0] * v.T - w * E[1].T
    for i in range(3):
        for j in range(3):
            for k in range(3):
                lhs = ((i == 0) * q[j, k]
                       + (j == 1) * p[i, k]
                       + (k == 2) * g[i, j])
                assert sp.expand(lhs - int(i == j == k)) == 0
    return p, q, g


def zero_mask(p, q):
    return sum(1 << color for color in range(3)
               if p * K[color] * q.T == ZERO)


def bilinear(matrix):
    return sp.expand((ALPHA.T * matrix * BETA)[0])


def rank_one(left, row):
    return left * row.T


def singleton_blocks():
    return (
        (rank_one(E[0], E[0]), rank_one(E[0], ONES)),
        (rank_one(E[0], ONES), rank_one(E[0], E[0])),
        (rank_one(E[0], ONES),
         rank_one(E[0], sp.Matrix((2, 1, 1)))),
    )


def audit_case(name, u, v, w, a, b, c, d, expected_cross):
    p_k, q_k, a_pq = staircase(u, v, w)
    assert a_pq.det() == 1
    cross = tuple(p_k * K[color] * q_k.T for color in range(3))
    assert cross == expected_cross
    assert zero_mask(p_k, q_k) == 0

    # Crossed exact-double anchors: x_u=A e_1, y_u=B e_2 and
    # x_v=C e_2, y_v=D e_1.
    p_u, q_u = rank_one(a, E[1]), rank_one(b, E[2])
    p_v, q_v = rank_one(c, E[2]), rank_one(d, E[1])
    assert zero_mask(p_u, q_u) == 6
    assert zero_mask(p_v, q_v) == 6

    singletons = singleton_blocks()
    assert tuple(zero_mask(p, q) for p, q in singletons) == (1, 1, 1)
    assert (zero_mask(p_k, q_k),
            *(zero_mask(p, q) for p, q in singletons),
            zero_mask(p_u, q_u), zero_mask(p_v, q_v)) == (0, 1, 1, 1, 6, 6)

    gamma_k = tuple(bilinear(matrix) for matrix in cross)
    gamma_s = tuple(
        tuple(bilinear(p * K[color] * q.T) for color in range(3))
        for p, q in singletons
    )
    for gamma in gamma_s:
        assert gamma[0] == 0
        assert sp.expand(gamma[2] + gamma[1]) == 0

    form_a = sp.expand((ALPHA.T * a)[0])
    form_b = sp.expand((BETA.T * b)[0])
    form_c = sp.expand((ALPHA.T * c)[0])
    form_d = sp.expand((BETA.T * d)[0])
    singleton_1 = sp.prod(gamma[1] for gamma in gamma_s)
    singleton_2 = sp.prod(gamma[2] for gamma in gamma_s)

    target_1 = ALPHA[1] * BETA[1] * gamma_k[1] * singleton_1
    target_2 = ALPHA[2] * BETA[2] * gamma_k[2] * singleton_2
    # Eliminate h from target_1=h*A*D and target_2=h*B*C.
    identity = sp.expand(
        target_1 * form_b * form_c
        - target_2 * form_a * form_d
    )
    assert identity == 0
    print(name, "PASS")
    print("  det(A_pq)=", a_pq.det(), "masks=(0,1,1,1,6,6)")
    print("  gamma_k,1=", gamma_k[1])
    print("  gamma_k,2=", gamma_k[2])


def main():
    e0, e1, e2 = E
    audit_case(
        "associate branch",
        u=sp.zeros(3, 1),
        v=e0,
        w=e1,
        a=e1,
        b=e2,
        c=e2,
        d=e1,
        expected_cross=(
            e1 * e0.T,
            e1 * e0.T,
            -e1 * e0.T,
        ),
    )
    audit_case(
        "split branch",
        u=sp.zeros(3, 1),
        v=e0,
        w=e0 + e1,
        a=e0 + e1,
        b=e2,
        c=e2,
        d=e1,
        expected_cross=(
            e1 * e0.T,
            (e0 + e1) * e0.T,
            -e1 * e0.T,
        ),
    )
    print("PASS: both UFD allocation branches survive the staircase boundary")


if __name__ == "__main__":
    main()
