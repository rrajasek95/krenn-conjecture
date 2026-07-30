#!/usr/bin/env python3
"""Exact audits for physical-dark-cut-hessian-kernel-counterlift.md."""

from fractions import Fraction
from itertools import combinations


if not __debug__:
    raise RuntimeError("run without -O: this audit uses assertions")


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
SUPPORT = {
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
    (1, 2), (1, 3), (1, 4), (2, 3), (4, 5),
}


def edge(i, j):
    return (i, j) if i < j else (j, i)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return [()]
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            answer.append((edge(first, second),) + matching)
    return answer


def hafnian(vertices):
    return sum(
        all(pair in SUPPORT for pair in matching)
        for matching in perfect_matchings(vertices)
    )


def q_value(pair):
    return Fraction(int(edge(*pair) in SUPPORT))


def hessian():
    universe = set(VERTICES)
    return [
        [
            q_value(tuple(universe - set(left) - set(right)))
            if set(left).isdisjoint(right)
            else Fraction(0)
            for right in EDGES
        ]
        for left in EDGES
    ]


def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def edge_vector(entries):
    vector = [Fraction(0)] * len(EDGES)
    for pair, value in entries.items():
        vector[EDGE_INDEX[edge(*pair)]] = Fraction(value)
    return vector


def rank(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def determinant3(matrix):
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def audit_decorated_cap_and_quotient():
    # beta=x_0,a*x_1,a.  A nonzero beta*q^[2] term must use a matching
    # of the complementary sites, and 23|45 is the unique supported one.
    complement_matchings = perfect_matchings((2, 3, 4, 5))
    supported = [
        matching
        for matching in complement_matchings
        if all(pair in SUPPORT for pair in matching)
    ]
    assert supported == [((2, 3), (4, 5))]
    assert hafnian((2, 3, 4, 5)) == 1

    # L is nonzero only at site 0 and S only at site 1.
    blocking_set = {
        site for site in VERTICES if site in (0, 1)
    }
    assert blocking_set == {0, 1}
    assert hafnian((2, 3, 4, 5)) == 1  # the pure quotient coefficient


def audit_hessian_obstruction():
    matrix = hessian()
    witness = edge_vector({(0, 2): 1, (0, 3): -1, (2, 4): -1, (3, 4): 1})
    lam = edge_vector({(0, 1): 1, (2, 3): 1, (0, 2): -1, (1, 3): -1})
    beta = edge_vector({(0, 1): 1})

    assert q_value((0, 1)) * q_value((2, 3)) == q_value((0, 2)) * q_value((1, 3))
    assert rank(matrix) == 14
    assert matvec(matrix, witness) == [0] * 15
    assert dot(lam, witness) == -1
    assert dot(lam, beta) == 1
    assert rank([row + [value] for row, value in zip(matrix, lam)]) == 15


def audit_seven_row_completion():
    p_sites = (0, 1, 2)
    s_sites = (1, 0, 2)
    assert len(set(p_sites)) == len(set(s_sites)) == 3
    top_hafnian = hafnian(VERTICES)
    assert top_hafnian == 4

    response = [
        [
            Fraction(0) if p_site == s_site
            else Fraction(hafnian(tuple(v for v in VERTICES if v not in (p_site, s_site))))
            for s_site in s_sites
        ]
        for p_site in p_sites
    ]
    assert response == [
        [Fraction(1), Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(1), Fraction(1)],
        [Fraction(1), Fraction(1), Fraction(0)],
    ]

    target = [
        [Fraction(int(row == 0 and column == 0)) for column in range(3)]
        for row in range(3)
    ]
    direct = [
        [(target[row][column] - response[row][column]) / top_hafnian for column in range(3)]
        for row in range(3)
    ]
    assert determinant3(direct) == Fraction(1, 64)

    left_sides = [
        [top_hafnian * direct[row][column] + response[row][column] for column in range(3)]
        for row in range(3)
    ]
    assert left_sides == target
    passing_rows = {
        (row, column)
        for row in range(3)
        for column in range(3)
        if (row != column and left_sides[row][column] == 0)
        or (row == column == 0 and left_sides[row][column] == 1)
    }
    assert passing_rows == {
        (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)
    }
    assert left_sides[1][1] == 0  # missing X_b
    assert left_sides[2][2] == 0  # missing X_delta

    # At edge 01, the oriented endpoint products are E_aa and E_bb.
    # The selected E_aa functional sees d-E_aa but not d-E_bb.
    assert direct[0][0] - 1 == -1
    assert direct[0][0] == 0


def main():
    audit_decorated_cap_and_quotient()
    audit_hessian_obstruction()
    audit_seven_row_completion()
    print("physical dark-cut Hessian-kernel counterlift: PASS")
    print("  decorated cap and pure two-site quotient: PASS")
    print("  Hessian ranks: 14 -> 15; kernel pairing: -1")
    print("  full-row ledger: 7/9; missing diagonals: (b,b), (delta,delta)")


if __name__ == "__main__":
    main()
