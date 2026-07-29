#!/usr/bin/env python3
"""Exact audit of the cofactor-open color-cloning countermodule.

The four-site binary source is checked coefficient by coefficient.  It is
then cloned into two sitewise-distinct nonzero colors and all 81 ternary
coefficients are compared with the closed product formula.
"""

from __future__ import annotations

from fractions import Fraction
from functools import reduce
from itertools import combinations, product


VERTICES = tuple(range(4))
EDGES = tuple(combinations(VERTICES, 2))
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def edge(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


# The scalar leading source, directed first jet, and binary second part.
C = {
    selected_edge: Fraction(-1) if selected_edge == (0, 1) else Fraction(1)
    for selected_edge in EDGES
}
B = {
    (i, j): Fraction(0)
    for i in VERTICES
    for j in VERTICES
    if i != j
}
B.update(
    {
        (0, 1): Fraction(1),
        (0, 2): Fraction(-1),
        (1, 2): Fraction(1),
        (1, 3): Fraction(-1),
        (2, 0): Fraction(1),
        (2, 3): Fraction(1),
        (3, 0): Fraction(1),
        (3, 1): Fraction(-1),
    }
)
D = {
    (0, 1): Fraction(-1),
    (0, 2): Fraction(-1),
    (0, 3): Fraction(-1),
    (1, 2): Fraction(1),
    (1, 3): Fraction(-1),
    (2, 3): Fraction(-1),
}


def scalar_hafnian(weights, vertices=VERTICES) -> Fraction:
    vertices = tuple(vertices)
    if not vertices:
        return Fraction(1)
    first = vertices[0]
    answer = Fraction(0)
    for position, partner in enumerate(vertices[1:], 1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        answer += weights[edge(first, partner)] * scalar_hafnian(
            weights, remainder
        )
    return answer


def cofactor(i: int, j: int) -> Fraction:
    return scalar_hafnian(
        C, tuple(vertex for vertex in VERTICES if vertex not in (i, j))
    )


def second_lift(left, right):
    """The cofactor-open quadratic lift Q_C(left,right)."""
    answer = {}
    for i, k in EDGES:
        remaining = [vertex for vertex in VERTICES if vertex not in (i, k)]
        j, ell = remaining
        numerator = left[i, j] * right[k, ell] + left[i, ell] * right[k, j]
        answer[i, k] = -numerator / cofactor(i, k)
    return answer


def binary_cells():
    cells = {}
    for i, j in EDGES:
        cells[i, j, 0, 0] = C[i, j]
        cells[i, j, 1, 0] = B[i, j]
        cells[i, j, 0, 1] = B[j, i]
        cells[i, j, 1, 1] = D[i, j]
    return cells


def coefficient(cells, coloring) -> Fraction:
    return sum(
        reduce(
            lambda value, selected_edge: value
            * cells.get(
                selected_edge
                + (coloring[selected_edge[0]], coloring[selected_edge[1]]),
                Fraction(0),
            ),
            matching,
            Fraction(1),
        )
        for matching in MATCHINGS
    )


def cloned_cells(base, scales):
    """Pull a binary source back along 0->0, 1->1, 2->scale_i*1."""

    def collapsed(color):
        return 0 if color == 0 else 1

    def multiplier(vertex, color):
        return scales[vertex] if color == 2 else Fraction(1)

    answer = {}
    for i, j in EDGES:
        for left, right in product(range(3), repeat=2):
            answer[i, j, left, right] = (
                multiplier(i, left)
                * multiplier(j, right)
                * base[i, j, collapsed(left), collapsed(right)]
            )
    return answer


def main() -> None:
    # The leading point is normalized and is in the requested cofactor-open
    # locus.  Its cofactor vector is (1,1,1,1,1,-1).
    assert scalar_hafnian(C) == 1
    assert {selected_edge: cofactor(*selected_edge) for selected_edge in EDGES} == {
        (0, 1): Fraction(1),
        (0, 2): Fraction(1),
        (0, 3): Fraction(1),
        (1, 2): Fraction(1),
        (1, 3): Fraction(1),
        (2, 3): Fraction(-1),
    }

    # B is a nonzero cofactor-kernel direction in every row, and D is its
    # unique second lift.
    for i in VERTICES:
        assert sum(B[i, j] * cofactor(i, j) for j in VERTICES if j != i) == 0
        assert any(B[i, j] for j in VERTICES if j != i)
    assert second_lift(B, B) == D

    base = binary_cells()
    for coloring in product(range(2), repeat=4):
        expected = Fraction(int(coloring in ((0, 0, 0, 0), (1, 1, 1, 1))))
        assert coefficient(base, coloring) == expected, coloring

    scales = (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1))
    assert reduce(lambda value, item: value * item, scales, Fraction(1)) == 1
    cloned = cloned_cells(base, scales)

    # Check the cofactor-jet formulas for both colors.  The second direction
    # is rowwise, but not globally, proportional to the first.
    first_jets = {
        1: B,
        2: {(i, j): scales[i] * B[i, j] for i, j in B},
    }
    active_ratios = {
        first_jets[2][i, j] / first_jets[1][i, j]
        for i, j in B
        if first_jets[1][i, j]
    }
    assert active_ratios == {Fraction(1), Fraction(-1)}
    for color, values in first_jets.items():
        for i in VERTICES:
            assert sum(
                values[i, j] * cofactor(i, j)
                for j in VERTICES
                if j != i
            ) == 0, (color, i)
    for left, right in product((1, 2), repeat=2):
        lift = second_lift(first_jets[left], first_jets[right])
        for i, j in EDGES:
            assert cloned[i, j, left, right] == lift[i, j]

    # This is the exact coefficient formula
    #   H(clone)=X_0 + tensor_i(e_1 + scales_i e_2).
    nonzero = {}
    for coloring in product(range(3), repeat=4):
        value = coefficient(cloned, coloring)
        expected = Fraction(0)
        if coloring == (0, 0, 0, 0):
            expected = Fraction(1)
        elif 0 not in coloring:
            expected = reduce(
                lambda result, vertex: result
                * (scales[vertex] if coloring[vertex] == 2 else 1),
                VERTICES,
                Fraction(1),
            )
        assert value == expected, (coloring, value, expected)
        if value:
            nonzero[coloring] = value

    assert len(nonzero) == 17
    assert all(
        coefficient(cloned, coloring) == 0
        for coloring in product(range(3), repeat=4)
        if 1 <= sum(color != 0 for color in coloring) <= 3
    )
    mixed_cubics = [
        coloring
        for coloring in product(range(3), repeat=4)
        if sum(color != 0 for color in coloring) == 3
        and 1 in coloring
        and 2 in coloring
    ]
    assert len(mixed_cubics) == 24
    assert all(coefficient(cloned, coloring) == 0 for coloring in mixed_cubics)

    # The two requested binary faces are exact.  The omitted 1/2 face is a
    # decomposable full-support tensor and has fourteen mixed errors.
    for color in (1, 2):
        for coloring in product((0, color), repeat=4):
            expected = Fraction(
                int(coloring in ((0, 0, 0, 0), (color,) * 4))
            )
            assert coefficient(cloned, coloring) == expected
    third_face_errors = [
        coloring
        for coloring in product((1, 2), repeat=4)
        if coloring not in ((1, 1, 1, 1), (2, 2, 2, 2))
        and coefficient(cloned, coloring)
    ]
    assert len(third_face_errors) == 14

    print(
        "cofactor-open color clone: binary faces 01/02 exact, "
        "24 genuinely mixed cubics vanish, omitted 12 face has 14 errors: PASS"
    )


if __name__ == "__main__":
    main()
