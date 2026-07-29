#!/usr/bin/env python3
"""Exact audits for the active n+2 color-collision obstruction.

For both possible monochromatic four-cycle switches, this script computes
the complete one-z tangent kernel over Q, restricts the relevant second
Hessian coefficient to the product of the two site sectors, and proves that
the restricted bilinear form is zero.  Interior and degenerate switch
specializations are both included.
"""

from __future__ import annotations

import itertools
from fractions import Fraction


X, Y, Z = range(3)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, partner),) + tail


def weighted_matchings(q0, vertices, coloring):
    total = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for u, v in matching:
            term *= q0.get((u, v, coloring[u], coloring[v]), 0)
        total += term
    return total


def sector_system(n, q0, z_site):
    """Matrix of the fixed-z_site sector of dH_q0 on one-z cells."""
    columns = tuple(
        (other, color)
        for other in range(n)
        if other != z_site
        for color in (X, Y)
    )
    matrix = []
    colorings = []
    for rest in itertools.product((X, Y), repeat=n - 1):
        coloring = list(rest)
        coloring.insert(z_site, Z)
        coloring = tuple(coloring)
        row = []
        for other, color in columns:
            if coloring[other] != color:
                row.append(Fraction(0))
                continue
            remaining = tuple(
                vertex for vertex in range(n)
                if vertex not in (z_site, other)
            )
            row.append(weighted_matchings(q0, remaining, coloring))
        matrix.append(row)
        colorings.append(coloring)
    return columns, matrix, colorings


def nullspace(matrix):
    rows = [[Fraction(value) for value in row] for row in matrix]
    ncols = len(rows[0])
    pivots = []
    cursor = 0
    for column in range(ncols):
        pivot = next(
            (row for row in range(cursor, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[cursor], rows[pivot] = rows[pivot], rows[cursor]
        divisor = rows[cursor][column]
        rows[cursor] = [value / divisor for value in rows[cursor]]
        for row in range(len(rows)):
            if row == cursor or not rows[row][column]:
                continue
            multiple = rows[row][column]
            rows[row] = [
                left - multiple * right
                for left, right in zip(rows[row], rows[cursor])
            ]
        pivots.append(column)
        cursor += 1
    free = [column for column in range(ncols) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [Fraction(0)] * ncols
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -rows[row][free_column]
        basis.append(vector)
    return basis


def q2_cofactor(n, q0, first, second):
    coloring = tuple(
        Z if vertex in (first, second) else X for vertex in range(n)
    )
    remaining = tuple(
        vertex for vertex in range(n)
        if vertex not in (first, second)
    )
    return weighted_matchings(q0, remaining, coloring)


def hessian_matrix(n, q0, first, second, first_columns, second_columns):
    """Coefficient of z_first z_second X_rest in 1/2 d2H(Z,Z)."""
    matrix = [
        [Fraction(0)] * len(second_columns) for _ in first_columns
    ]
    coloring = tuple(
        Z if vertex in (first, second) else X for vertex in range(n)
    )
    for a, (u, color_u) in enumerate(first_columns):
        if color_u != X or u in (first, second):
            continue
        for b, (v, color_v) in enumerate(second_columns):
            if color_v != X or v in (first, second, u):
                continue
            remaining = tuple(
                vertex for vertex in range(n)
                if vertex not in (first, second, u, v)
            )
            matrix[a][b] = weighted_matchings(q0, remaining, coloring)
    return matrix


def bilinear(left, matrix, right):
    return sum(
        left[i] * matrix[i][j] * right[j]
        for i in range(len(left))
        for j in range(len(right))
    )


def verify_pair(n, q0, first, second):
    left_columns, left_matrix, _ = sector_system(n, q0, first)
    right_columns, right_matrix, _ = sector_system(n, q0, second)
    left_kernel = nullspace(left_matrix)
    right_kernel = nullspace(right_matrix)
    hessian = hessian_matrix(
        n, q0, first, second, left_columns, right_columns
    )
    assert q2_cofactor(n, q0, first, second) == 0
    for left in left_kernel:
        for right in right_kernel:
            assert bilinear(left, hessian, right) == 0
    return len(left_columns) - len(left_kernel), len(right_columns) - len(right_kernel)


def cycle_factors(n):
    px = tuple((i, i + 1) for i in range(0, n, 2))
    py = tuple((i, i + 1) for i in range(1, n - 1, 2)) + ((0, n - 1),)
    return px, py


def x_switch_base(n, r, mode):
    px, py = cycle_factors(n)
    extra_left = (0, 2 * r)
    extra_right = (1, 2 * r + 1)
    q0 = {edge + (X, X): Fraction(1) for edge in px}
    q0.update({edge + (Y, Y): Fraction(1) for edge in py})
    if mode == "interior":
        # The old and switched x matchings each have weight one.
        q0[extra_left + (X, X)] = 1
        q0[extra_right + (X, X)] = 1
    elif mode == "old_endpoint":
        # Old matching has weight two; one inactive switched cell remains.
        q0[(0, 1, X, X)] = 2
        q0[extra_right + (X, X)] = 7
    elif mode == "new_endpoint":
        # Switched matching has weight two; one inactive old cell remains.
        q0.pop((0, 1, X, X))
        q0[(2 * r, 2 * r + 1, X, X)] = 7
        q0[extra_left + (X, X)] = 2
        q0[extra_right + (X, X)] = 1
    else:
        raise ValueError(mode)
    return q0


def y_switch_base(n, r, mode):
    px, py = cycle_factors(n)
    old_left = (0, n - 1)
    old_right = (2 * r - 1, 2 * r)
    extra_left = (2 * r - 1, n - 1)
    extra_right = (0, 2 * r)
    q0 = {edge + (X, X): Fraction(1) for edge in px}
    q0[(0, 1, X, X)] = 2
    q0.update({edge + (Y, Y): Fraction(1) for edge in py})
    if mode == "interior":
        # Give each y matching weight 1/2.
        q0[old_left + (Y, Y)] = Fraction(1, 2)
        q0[extra_left + (Y, Y)] = Fraction(1, 2)
        q0[extra_right + (Y, Y)] = 1
    elif mode == "old_endpoint":
        # Old y matching has weight one; one switched cell remains.
        q0[extra_right + (Y, Y)] = 7
    elif mode == "new_endpoint":
        # Switched y matching has weight one; one old cell remains.
        q0.pop(old_left + (Y, Y))
        q0[old_right + (Y, Y)] = 7
        q0[extra_left + (Y, Y)] = 1
        q0[extra_right + (Y, Y)] = 1
    else:
        raise ValueError(mode)
    return q0


def constant_coefficients(n, q0):
    all_x = (X,) * n
    all_y = (Y,) * n
    vertices = tuple(range(n))
    return (
        weighted_matchings(q0, vertices, all_x),
        weighted_matchings(q0, vertices, all_y),
    )


def main():
    audits = 0
    for n in (6, 8, 10):
        m = n // 2
        for r in range(1, m // 2 + 1):
            for mode in ("interior", "old_endpoint", "new_endpoint"):
                q0 = x_switch_base(n, r, mode)
                assert constant_coefficients(n, q0) == (2, 1)
                ranks = verify_pair(n, q0, 0, n - 2)
                audits += 1
                print(f"x-switch n={n} r={r} mode={mode} ranks={ranks}")

                q0 = y_switch_base(n, r, mode)
                assert constant_coefficients(n, q0) == (2, 1)
                ranks = verify_pair(n, q0, 0, 2 * r)
                audits += 1
                print(f"y-switch n={n} r={r} mode={mode} ranks={ranks}")
    print(f"verified {audits} exact switched-base collision obstructions")


if __name__ == "__main__":
    main()
