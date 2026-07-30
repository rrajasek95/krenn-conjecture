#!/usr/bin/env python3
"""Exact audits for the all-cycle seven-row Hessian guard."""

from fractions import Fraction
from itertools import combinations


if not __debug__:
    raise RuntimeError("run without -O: this audit uses assertions")


VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
SUPPORT = {
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (0, 5),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 5),
    (3, 4),
}


def edge(left, right):
    return (left, right) if left < right else (right, left)


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


def supported_matchings(vertices):
    return [
        matching
        for matching in perfect_matchings(vertices)
        if all(pair in SUPPORT for pair in matching)
    ]


def hafnian(vertices):
    return len(supported_matchings(vertices))


def q_value(pair, support=SUPPORT):
    return Fraction(int(edge(*pair) in support))


def edge_vector(entries):
    answer = [Fraction(0)] * len(EDGES)
    for pair, value in entries.items():
        answer[EDGE_INDEX[edge(*pair)]] += Fraction(value)
    return answer


def hessian(support=SUPPORT):
    universe = set(VERTICES)
    return [
        [
            q_value(tuple(universe - set(left) - set(right)), support)
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


def audit_decorated_rows():
    top_matchings = supported_matchings(VERTICES)
    assert top_matchings == [
        ((0, 1), (2, 5), (3, 4)),
        ((0, 3), (1, 4), (2, 5)),
        ((0, 4), (1, 3), (2, 5)),
        ((0, 5), (1, 4), (2, 3)),
    ]
    assert hafnian(VERTICES) == 4

    p_sites = (0, 1, 2)
    s_sites = (1, 0, 3)
    assert len(set(p_sites)) == len(set(s_sites)) == 3
    response = [
        [
            Fraction(0)
            if p_site == s_site
            else Fraction(
                hafnian(
                    vertex
                    for vertex in VERTICES
                    if vertex not in (p_site, s_site)
                )
            )
            for s_site in s_sites
        ]
        for p_site in p_sites
    ]
    assert response == [
        [Fraction(1), Fraction(0), Fraction(1)],
        [Fraction(0), Fraction(1), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(1)],
    ]

    target = [
        [Fraction(int(row == column == 0)) for column in range(3)]
        for row in range(3)
    ]
    direct = [
        [(target[row][column] - response[row][column]) / 4 for column in range(3)]
        for row in range(3)
    ]
    assert direct == [
        [Fraction(0), Fraction(0), Fraction(-1, 4)],
        [Fraction(0), Fraction(-1, 4), Fraction(-1, 4)],
        [Fraction(-1, 4), Fraction(0), Fraction(-1, 4)],
    ]
    assert determinant3(direct) == Fraction(1, 64)
    assert direct[0][0] == 0

    left_sides = [
        [4 * direct[row][column] + response[row][column] for column in range(3)]
        for row in range(3)
    ]
    assert left_sides == target
    passing = {
        (row, column)
        for row in range(3)
        for column in range(3)
        if (row != column and left_sides[row][column] == 0)
        or (row == column == 0 and left_sides[row][column] == 1)
    }
    assert passing == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1),
    }
    assert left_sides[1][1] == left_sides[2][2] == 0

    # Track the actual top-tensor basis, rather than only its a-coordinate.
    # Every constructed left side lies on X_a; the desired diagonal rows
    # lie on the three independent lines X_a, X_b, X_delta.
    top_basis = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    )
    actual_tensors = [
        [tuple(left_sides[row][column] * value for value in top_basis[0])
         for column in range(3)]
        for row in range(3)
    ]
    desired_tensors = [
        [top_basis[row] if row == column else (Fraction(0),) * 3
         for column in range(3)]
        for row in range(3)
    ]
    failures = {
        (row, column): tuple(
            actual - desired
            for actual, desired in zip(
                actual_tensors[row][column], desired_tensors[row][column]
            )
        )
        for row in range(3)
        for column in range(3)
        if actual_tensors[row][column] != desired_tensors[row][column]
    }
    assert failures == {
        (1, 1): (Fraction(0), Fraction(-1), Fraction(0)),
        (2, 2): (Fraction(0), Fraction(0), Fraction(-1)),
    }

    # Even granting three nonzero scalar targets on the single X_a line
    # does not change the cap or Hessian data.  Only the direct diagonal
    # coefficients change.  The sample (1,2,3) ledger remains invertible.
    scalar_targets = (Fraction(1), Fraction(2), Fraction(3))
    scalar_direct = [row[:] for row in direct]
    scalar_direct[1][1] += scalar_targets[1] / 4
    scalar_direct[2][2] += scalar_targets[2] / 4
    scalar_left_sides = [
        [4 * scalar_direct[row][column] + response[row][column]
         for column in range(3)]
        for row in range(3)
    ]
    assert scalar_left_sides == [
        [scalar_targets[row] if row == column else Fraction(0)
         for column in range(3)]
        for row in range(3)
    ]
    assert scalar_direct[0][0] == 0
    assert determinant3(scalar_direct) == Fraction(-1, 64)

    # The E_00 selector has cap factors only at sites zero and one.
    assert {0, 1} == {p_sites[0], s_sites[0]}
    complement = supported_matchings((2, 3, 4, 5))
    assert complement == [((2, 5), (3, 4))]

    # At 01 the two assignment matrices are E_00 and E_11.  E_00 sees
    # q_01*d-E_00 with value -1, and the selected direct coefficient is zero.
    assert q_value((0, 1)) * direct[0][0] - 1 == -1
    assert q_value((0, 1)) * direct[0][0] == 0


def curvature_covector(matched_edge, reverse):
    r, s = 0, 1
    u, v = matched_edge
    if reverse:
        u, v = v, u
    return edge_vector(
        {
            (r, s): q_value((u, v)),
            (u, v): q_value((r, s)),
            (r, u): -q_value((s, v)),
            (s, v): -q_value((r, u)),
        }
    )


def audit_all_dark_cycles():
    matrix = hessian()
    witness = edge_vector({(0, 1): 1, (0, 4): -1, (1, 2): -1, (2, 4): 1})
    beta = edge_vector({(0, 1): 1})
    assert rank(matrix) == 14
    assert matvec(matrix, witness) == [0] * len(EDGES)

    observed = {}
    for matched_edge in ((2, 5), (3, 4)):
        assert q_value(matched_edge) == 1
        for reverse in (False, True):
            covector = curvature_covector(matched_edge, reverse)
            pairing = dot(covector, witness)
            observed[(matched_edge, int(reverse))] = pairing
            assert dot(covector, beta) == 1
            assert pairing
            assert rank([row + [covector[index]] for index, row in enumerate(matrix)]) == 15
    assert observed == {
        ((2, 5), 0): Fraction(1),
        ((2, 5), 1): Fraction(2),
        ((3, 4), 0): Fraction(1),
        ((3, 4), 1): Fraction(2),
    }


def audit_older_guard_has_an_escape():
    old_support = {
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (4, 5),
    }
    matrix = hessian(old_support)
    witness = edge_vector({(0, 2): 1, (0, 3): -1, (2, 4): -1, (3, 4): 1})
    alternative = edge_vector({(0, 1): 1, (4, 5): 1, (1, 5): -1})
    assert rank(matrix) == 14
    assert matvec(matrix, witness) == [0] * len(EDGES)
    assert dot(alternative, witness) == 0
    assert rank([row + [alternative[index]] for index, row in enumerate(matrix)]) == 14


def main():
    audit_older_guard_has_an_escape()
    audit_decorated_rows()
    audit_all_dark_cycles()
    print("two-anchor all-cycle seven-row Hessian guard: PASS")
    print("  older corank-one packet's 01|45 alternative: compatible")
    print("  endpoint ranks: 3 and 3; det(d): 1/64")
    print("  unique dark matching: 25|34; Hessian rank: 14")
    print("  four kernel pairings: 1, 2, 1, 2")
    print("  full-row ledger: 7/9; missing diagonals: (b,b), (delta,delta)")
    print("  all-nine scalar shadow targets: (1,2,3); det(d): -1/64")


if __name__ == "__main__":
    main()
