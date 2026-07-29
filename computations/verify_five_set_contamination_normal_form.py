#!/usr/bin/env python3
"""Exact audits for notes/five-set-contamination-normal-form.md.

The proof in the note is general linear algebra.  This script checks its
three coordinate normal forms over the rationals and independently checks
the quotient-rank identity in a nontrivial finite row-space example.
"""

from fractions import Fraction as F
from itertools import product

import sympy as sp


WORDS = tuple(product(range(3), repeat=3))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def zero_tensor():
    return {word: F(0) for word in WORDS}


def add(*tensors):
    out = zero_tensor()
    for tensor in tensors:
        for word, value in tensor.items():
            out[word] += value
    return out


def scale(c, tensor):
    return {word: c * value for word, value in tensor.items()}


def basis(word, value=F(1)):
    out = zero_tensor()
    out[word] = value
    return out


def assert_zero(tensor):
    assert all(value == 0 for value in tensor.values())


def support_in(tensor, center, color):
    return all(value == 0 or word[center] == color
               for word, value in tensor.items())


def audit_quotient_rank():
    # Rows are written as columns in Q^8.  The mixed-row space has dimension
    # three, while the constant high rows contribute exactly two new quotient
    # directions (h_2 is dependent modulo M).
    m_rows = [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0],
    ]
    h_rows = [
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 1, 1, 2, -3, 0, 0],
    ]
    m = sp.Matrix(m_rows)
    mh = sp.Matrix(m_rows + h_rows)
    quotient_rank = mh.rank() - m.rank()

    # beta annihilates all mixed rows.  Evaluation on h_0,h_1,h_2 is the
    # matrix in (8); its rank must equal the quotient rank in (9).
    kernel_basis = m.nullspace()
    evaluation = sp.Matrix(
        [[sp.Matrix(h).dot(beta) for beta in kernel_basis] for h in h_rows]
    )
    assert quotient_rank == 2
    assert evaluation.rank() == quotient_rank
    # An explicit generic beta has all nonzero evaluations of the three
    # nonzero residue vectors, as in Corollary 2.2.
    beta = sum(kernel_basis, sp.zeros(8, 1))
    assert all(sp.Matrix(h).dot(beta) != 0 for h in h_rows)


def audit_three_cross_enumeration():
    # A deterministic arbitrary-matrix K8 source.  No target identity is
    # assumed here: this independently verifies the one-cross rank bound and
    # the coordinate-cap vector-permanent formula (43).
    vertices = tuple(range(8))
    shore = (0, 1, 2)
    exposed = (3, 4, 5, 6, 7)
    matrices = {}
    for u in vertices:
        for v in range(u + 1, 8):
            matrices[u, v] = sp.Matrix(3, 3, lambda i, j:
                ((u + 1) * (i + 2) + (v + 2) * (j + 1) + i * j + 3) % 7 - 3)

    matchings = tuple(perfect_matchings(vertices))
    exposed_words = tuple(product(range(3), repeat=5))
    rows_one = {}
    rows_three = {}
    for left_word in WORDS:
        one = []
        three = []
        for right_word in exposed_words:
            coloring = left_word + right_word
            totals = {1: 0, 3: 0}
            for matching in matchings:
                crossing = sum((u in shore) != (v in shore) for u, v in matching)
                value = 1
                for u, v in matching:
                    value *= matrices[u, v][coloring[u], coloring[v]]
                totals[crossing] += value
            one.append(totals[1])
            three.append(totals[3])
        rows_one[left_word] = one
        rows_three[left_word] = three

    mixed = [word for word in WORDS if word not in ((0, 0, 0), (1, 1, 1), (2, 2, 2))]
    assert sp.Matrix([rows_one[word] for word in mixed]).rank() <= 9

    sigma = (0, 2, 1, 0, 2)
    response_from_rows = {
        word: rows_three[word][exposed_words.index(sigma)] for word in WORDS
    }
    response_from_formula = {word: 0 for word in WORDS}
    for u in exposed:
        xu = matrices[0, u][:, sigma[exposed.index(u)]]
        for v in exposed:
            if v == u:
                continue
            yv = matrices[1, v][:, sigma[exposed.index(v)]]
            for w in exposed:
                if w == u or w == v:
                    continue
                zw = matrices[2, w][:, sigma[exposed.index(w)]]
                remainder = tuple(t for t in exposed if t not in (u, v, w))
                a, b = remainder
                q_ab = matrices[a, b][sigma[exposed.index(a)], sigma[exposed.index(b)]]
                for word in WORDS:
                    response_from_formula[word] += (
                        q_ab * xu[word[0]] * yv[word[1]] * zw[word[2]]
                    )
    assert response_from_formula == response_from_rows


def audit_rank_three():
    # E_r=0 is the pure rainbow triangle (25).
    e = [zero_tensor(), zero_tensor(), zero_tensor()]
    for b in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (2, -3, 5)):
        assert_zero(add(*(scale(F(b[r]), e[r]) for r in range(3))))


def audit_rank_two_three_color_leak():
    theta = (F(2), F(-3), F(5))
    z = basis((0, 1, 2), F(7))
    e = [scale(theta[r], z) for r in range(3)]
    assert support_in(e[0], 0, 0)
    assert support_in(e[1], 1, 1)
    assert support_in(e[2], 2, 2)
    # Two independent vectors spanning ker(theta).
    plane_basis = ((F(3), F(2), F(0)), (F(-5), F(0), F(2)))
    for b in plane_basis:
        assert sum(theta[r] * b[r] for r in range(3)) == 0
        assert_zero(add(*(scale(b[r], e[r]) for r in range(3))))


def audit_rank_two_two_color_leak():
    theta = (F(2), F(-3), F(0))
    w = (F(1), F(4), F(-2))
    z = zero_tensor()
    for k in range(3):
        z[(0, 1, k)] = w[k]
    e = [scale(theta[r], z) for r in range(3)]
    assert support_in(e[0], 0, 0)
    assert support_in(e[1], 1, 1)
    assert_zero(e[2])
    plane_basis = ((F(3), F(2), F(0)), (F(0), F(0), F(1)))
    for b in plane_basis:
        assert sum(theta[r] * b[r] for r in range(3)) == 0
        assert_zero(add(*(scale(b[r], e[r]) for r in range(3))))


def audit_rank_one_transfers():
    b = (F(2), F(3), F(5))
    z01 = zero_tensor()
    z02 = zero_tensor()
    z12 = zero_tensor()
    for k, value in enumerate((F(2), F(-1), F(4))):
        z01[(0, 1, k)] = value
    for j, value in enumerate((F(3), F(5), F(-2))):
        z02[(0, j, 2)] += value
    for i, value in enumerate((F(-3), F(7), F(1))):
        z12[(i, 1, 2)] += value

    e0 = scale(F(1, 2), add(z01, z02))
    e1 = scale(F(1, 3), add(scale(F(-1), z01), z12))
    e2 = scale(F(1, 5), add(scale(F(-1), z02), scale(F(-1), z12)))
    assert support_in(e0, 0, 0)
    assert support_in(e1, 1, 1)
    assert support_in(e2, 2, 2)
    assert_zero(add(scale(b[0], e0), scale(b[1], e1), scale(b[2], e2)))

    # Strip the fixed center factors as in (32b) and audit the three exact
    # determinant formulas (32c).
    u = sp.Matrix([2, 3, 5])
    v = sp.Matrix([7, 11, 13])
    w = sp.Matrix([17, 19, 23])
    es = [sp.eye(3)[:, i] for i in range(3)]
    b0, b1, b2 = map(sp.Rational, (2, 3, 5))
    a_yz = es[0] * es[0].T + (es[1] * u.T + v * es[2].T) / b0
    a_xz = es[1] * es[1].T + (-es[0] * u.T + w * es[2].T) / b1
    a_xy = es[2] * es[2].T + (-es[0] * v.T - w * es[1].T) / b2
    assert a_yz.det() == u[1] * v[2] / b0**2
    assert a_xz.det() == -u[0] * w[2] / b1**2
    assert a_xy.det() == v[0] * w[1] / b2**2
    assert all(sum(entry != 0 for entry in matrix) <= 6
               for matrix in (a_yz, a_xz, a_xy))
    cross = (
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
        sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
    )
    # The fixed (1,0,*) and (0,1,*) rows prevent a common row line, so a
    # staircase third site is not triple-zero for the opposite pair.
    assert any(a_xz * k * a_yz.T != sp.zeros(3) for k in cross)


def main():
    audit_quotient_rank()
    audit_three_cross_enumeration()
    audit_rank_three()
    audit_rank_two_three_color_leak()
    audit_rank_two_two_color_leak()
    audit_rank_one_transfers()
    print("PASS: triple-shore quotient and finite normal forms audited")


if __name__ == "__main__":
    main()
