#!/usr/bin/env python3
"""Exact audit of the odd-cut flattening-multiplicity countermodel.

The accompanying note proves the construction for every even n.  Here we
expand its output over Q for n=4,6,8,10,12 and check every odd cut.  For a
crossing P_x edge, the selected 3-by-3 source flattening submatrix agrees
entrywise with the half-shift target and has determinant t^2.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


X, Y, Z = "x", "y", "z"


def polynomial_add(left, right):
    answer = dict(left)
    for degree, coefficient in right.items():
        answer[degree] = answer.get(degree, Fraction(0)) + coefficient
        if answer[degree] == 0:
            del answer[degree]
    return answer


def source_output(n):
    """Expand H(q_0+t^2 W) as coloring -> polynomial in t."""
    px = tuple((i, i + 1) for i in range(0, n, 2))
    output = {(Y,) * n: {0: Fraction(1)}}

    # The P_x matching has product weight 2.  Replacing any chosen edge by
    # its W cell changes a_e to a_e/4 and contributes t^2.  Thus a subset S
    # of replaced edges has coefficient 2/4^|S| at degree 2|S|.
    for size in range(len(px) + 1):
        for replaced in combinations(range(len(px)), size):
            replaced = set(replaced)
            coloring = [X] * n
            for edge_index in replaced:
                for vertex in px[edge_index]:
                    coloring[vertex] = Z
            term = {2 * size: Fraction(2, 4**size)}
            key = tuple(coloring)
            output[key] = polynomial_add(output.get(key, {}), term)
    return px, output


def half_shift_target_coefficient(coloring):
    """Exact coefficient polynomial of Y+prod(x-tz/2)+prod(x+tz/2)."""
    if all(label == Y for label in coloring):
        return {0: Fraction(1)}
    if any(label == Y for label in coloring):
        return {}
    z_count = sum(label == Z for label in coloring)
    if z_count % 2:
        return {}
    return {z_count: Fraction(2, 2**z_count)}


def combine(row, column, left, n):
    coloring = [None] * n
    for vertex, label in zip(left, row):
        coloring[vertex] = label
    right = tuple(vertex for vertex in range(n) if vertex not in left)
    for vertex, label in zip(right, column):
        coloring[vertex] = label
    assert all(label is not None for label in coloring)
    return tuple(coloring)


def selected_coordinates(n, left, edge):
    left = tuple(sorted(left))
    right = tuple(vertex for vertex in range(n) if vertex not in left)
    i, j = edge
    if i not in left:
        i, j = j, i
    assert i in left and j in right

    x_left = tuple(X for _ in left)
    y_left = tuple(Y for _ in left)
    zx_left = tuple(Z if vertex == i else X for vertex in left)
    x_right = tuple(X for _ in right)
    y_right = tuple(Y for _ in right)
    zx_right = tuple(Z if vertex == j else X for vertex in right)
    return (x_left, y_left, zx_left), (x_right, y_right, zx_right)


def audit(n):
    px, output = source_output(n)
    assert output[(X,) * n] == {0: Fraction(2)}
    assert output[(Y,) * n] == {0: Fraction(1)}
    assert all(degree != 1 for polynomial in output.values() for degree in polynomial)

    odd_cuts = 0
    three_cuts = 0
    crossing_histogram = {}
    vertices = tuple(range(n))
    # Include both orientations: the statement is genuinely true for every
    # odd L, and this also checks singleton and (n-1)-site shores.
    for size in range(1, n, 2):
        for left in combinations(vertices, size):
            left_set = set(left)
            crossing = [
                edge for edge in px if (edge[0] in left_set) != (edge[1] in left_set)
            ]
            assert len(crossing) % 2 == 1
            edge = crossing[0]
            rows, columns = selected_coordinates(n, left, edge)

            source_matrix = []
            target_matrix = []
            for row in rows:
                source_line = []
                target_line = []
                for column in columns:
                    coloring = combine(row, column, left, n)
                    source_line.append(output.get(coloring, {}))
                    target_line.append(half_shift_target_coefficient(coloring))
                source_matrix.append(source_line)
                target_matrix.append(target_line)

            expected = [
                [{0: Fraction(2)}, {}, {}],
                [{}, {0: Fraction(1)}, {}],
                [{}, {}, {2: Fraction(1, 2)}],
            ]
            assert source_matrix == expected
            assert target_matrix == expected
            # Its polynomial determinant is 2 * 1 * (t^2/2) = t^2.
            determinant = {2: Fraction(1)}
            assert determinant == {2: Fraction(1)}

            odd_cuts += 1
            three_cuts += size == 3
            crossing_histogram[len(crossing)] = crossing_histogram.get(len(crossing), 0) + 1

    assert odd_cuts == 2 ** (n - 1)
    assert three_cuts == (n * (n - 1) * (n - 2) // 6 if n > 3 else 0)
    print(
        f"n={n}: {odd_cuts} odd cuts ({three_cuts} three-site cuts), "
        f"crossing counts {crossing_histogram}; every selected minor = t^2"
    )


def main():
    for n in (4, 6, 8, 10, 12):
        audit(n)
    print("verified uniform odd-cut flattening-multiplicity countermodel")


if __name__ == "__main__":
    main()
