#!/usr/bin/env python3
"""Exact certificate for the generic mixed-linear dense-top branch.

At n=6 fix the rational complete scalar top endpoint W with
``w_01=-383/96``.  The top tangent equations leave 24 coordinates in each
of K^x and K^y, and the top pair equations uniquely eliminate q0.  Bottom
coefficients with exactly one x (and otherwise y, with optionally one z)
are homogeneous linear equations in K^x.  This checker verifies that a
specified 24 by 24 minor of that 36 by 24 linear system is a nonzero
polynomial in K^y.  Consequently the open branch where this minor is
nonzero forces K^x=0, after which the all-x bottom coefficient is the wrong
rational number ``-119/145924`` rather than 2.

The checker deliberately makes no claim on the determinantal boundary of
that minor, or on scalar W for which a deleted-pair cofactor vanishes.
"""

from __future__ import annotations

import itertools
from fractions import Fraction


N = 6
X, Y, Z = range(3)
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))


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


MATCHINGS = tuple(perfect_matchings(VERTICES))


def coefficient(source, vertices, coloring):
    answer = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for u, v in matching:
            term *= source.get((u, v, coloring[u], coloring[v]), 0)
        answer += term
    return answer


def scalar_hafnian(weights, vertices):
    answer = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for edge in matching:
            term *= weights[edge]
        answer += term
    return answer


WEIGHTS = {edge: Fraction(1) for edge in EDGES}
WEIGHTS[(0, 1)] = Fraction(-383, 96)
COFACTORS = {
    edge: scalar_hafnian(
        WEIGHTS, tuple(vertex for vertex in VERTICES if vertex not in edge)
    )
    for edge in EDGES
}
assert scalar_hafnian(WEIGHTS, VERTICES) == Fraction(1, 32)
assert all(COFACTORS.values())

SECTORS = tuple((site, color) for site in VERTICES for color in (X, Y))
FREE = []
PIVOTS = {}
for sector in SECTORS:
    site, _ = sector
    neighbors = tuple(vertex for vertex in VERTICES if vertex != site)
    PIVOTS[sector] = neighbors[0]
    FREE.extend((site, sector[1], neighbor) for neighbor in neighbors[1:])
X_FREE = tuple(index for index, entry in enumerate(FREE) if entry[1] == X)
Y_FREE = tuple(index for index, entry in enumerate(FREE) if entry[1] == Y)
assert len(X_FREE) == len(Y_FREE) == 24


def add_directed_cell(source, binary_site, color, z_site, value):
    u, v = sorted((binary_site, z_site))
    colors = (color, Z) if binary_site == u else (Z, color)
    key = (u, v, *colors)
    source[key] = source.get(key, 0) + value


def decode_k(parameters):
    source = {}
    values = {sector: {} for sector in SECTORS}
    for value, (site, color, neighbor) in zip(parameters, FREE):
        values[(site, color)][neighbor] = value
    for site, color in SECTORS:
        pivot = PIVOTS[(site, color)]
        numerator = sum(
            COFACTORS[tuple(sorted((site, neighbor)))] * value
            for neighbor, value in values[(site, color)].items()
        )
        values[(site, color)][pivot] = -numerator / COFACTORS[
            tuple(sorted((site, pivot)))
        ]
        for neighbor, value in values[(site, color)].items():
            add_directed_cell(source, site, color, neighbor, value)
    return source


def eliminate_q0(parameters):
    k = decode_k(parameters)
    top = dict(k)
    for edge, value in WEIGHTS.items():
        top[edge + (Z, Z)] = value
    q0 = {}
    for first, second in EDGES:
        for first_color, second_color in itertools.product((X, Y), repeat=2):
            coloring = [Z] * N
            coloring[first] = first_color
            coloring[second] = second_color
            hessian = coefficient(top, VERTICES, tuple(coloring))
            target = (
                Fraction(1, 8)
                if first_color == second_color == X
                else Fraction(0)
            )
            q0[(first, second, first_color, second_color)] = (
                target - hessian
            ) / COFACTORS[(first, second)]
    return k, q0


BOTTOM_ONE_X = tuple(
    coloring
    for coloring in itertools.product((X, Y), repeat=N)
    if coloring.count(X) == 1
)
TANGENT_ONE_X = tuple(
    coloring
    for coloring in itertools.product((X, Y, Z), repeat=N)
    if coloring.count(X) == 1 and coloring.count(Z) == 1
)
MIXED_COLORINGS = BOTTOM_ONE_X + TANGENT_ONE_X
assert len(MIXED_COLORINGS) == 36

# Six one-x bottom rows plus eighteen one-x/one-z tangent rows.  The order
# is the canonical order in MIXED_COLORINGS above.
MINOR_ROWS = (
    35, 34, 33, 27, 13, 32, 14, 20, 12, 23, 7, 18,
    9, 2, 29, 24, 0, 1, 5, 4, 6, 26, 3, 15,
)

CORRECTION_COLUMNS = (
    0, 1, 2, 3, 4, 5, 8, 9, 12, 13, 16, 17,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
    32, 33, 34, 35, 36, 37, 38, 39,
)
TRANSPORT_PIVOT_ROWS = tuple(range(1, 33))
TRANSPORT_OBSTRUCTION_ROWS = (0, 49, 53, 57, 69)


def mixed_values(parameters):
    k, q0 = eliminate_q0(parameters)
    source = dict(q0)
    for key, value in k.items():
        source[key] = source.get(key, 0) + value
    values = []
    for row, coloring in enumerate(MIXED_COLORINGS):
        if row < len(BOTTOM_ONE_X):
            values.append(coefficient(q0, VERTICES, coloring))
        else:
            values.append(coefficient(source, VERTICES, coloring))
    return values


def matrix_rank_and_det(matrix, determinant_rows=None):
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    determinant = Fraction(1)
    sign = 1
    square = determinant_rows is not None
    if square:
        work = [work[row] for row in determinant_rows]
        row_count = len(work)
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            if square:
                return pivot_row, Fraction(0)
            continue
        if pivot != pivot_row:
            work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
            sign *= -1
        pivot_value = work[pivot_row][column]
        if square:
            determinant *= pivot_value
        for row in range(pivot_row + 1, row_count):
            if not work[row][column]:
                continue
            scale = work[row][column] / pivot_value
            for later in range(column, column_count):
                work[row][later] -= scale * work[pivot_row][later]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row, sign * determinant if square else Fraction(0)


def solve_square(matrix, right_hand_side):
    size = len(matrix)
    width = len(right_hand_side[0])
    work = [
        list(matrix[row]) + list(right_hand_side[row]) for row in range(size)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [entry / scale for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                left - scale * right
                for left, right in zip(work[row], work[column])
            ]
    return [row[size : size + width] for row in work]


def transport_matrix(parameters, star=0):
    k, q0 = eliminate_q0(parameters)
    source = dict(q0)
    source.update(k)
    for edge, value in WEIGHTS.items():
        source[edge + (Z, Z)] = value
    columns = []
    decorations = (
        (0, ((Z, Z),)),
        (1, ((Z, X), (Z, Y), (X, Z), (Y, Z))),
        (2, ((X, X), (X, Y), (Y, X), (Y, Y))),
    )
    for grade, cells in decorations:
        for neighbor in VERTICES:
            if neighbor == star:
                continue
            first, _ = sorted((star, neighbor))
            for star_color, neighbor_color in cells:
                colors = (
                    (star_color, neighbor_color)
                    if star == first
                    else (neighbor_color, star_color)
                )
                columns.append((grade, neighbor, *colors))
    rows = []
    for binary_count in (0, 1, 2):
        for binary_sites in itertools.combinations(VERTICES, binary_count):
            for binary_colors in itertools.product((X, Y), repeat=binary_count):
                coloring = [Z] * N
                for site, color in zip(binary_sites, binary_colors):
                    coloring[site] = color
                row = []
                for _, neighbor, first_color, second_color in columns:
                    first, second = sorted((star, neighbor))
                    if (coloring[first], coloring[second]) != (
                        first_color,
                        second_color,
                    ):
                        row.append(Fraction(0))
                        continue
                    remaining = tuple(
                        vertex
                        for vertex in VERTICES
                        if vertex not in (star, neighbor)
                    )
                    row.append(coefficient(source, remaining, coloring))
                rows.append(row)
    return rows


def verify_mixed_minor():
    # A rational evaluation witness for the determinant polynomial Delta.
    base = [Fraction(0) for _ in FREE]
    for value, index in enumerate(Y_FREE, 1):
        base[index] = Fraction(value)
    zero = mixed_values(base)
    assert zero == [0] * len(zero)
    matrix = [[Fraction(0) for _ in X_FREE] for _ in MIXED_COLORINGS]
    for column, parameter_index in enumerate(X_FREE):
        probe = list(base)
        probe[parameter_index] = 1
        values = mixed_values(probe)
        for row, (value, constant) in enumerate(zip(values, zero)):
            matrix[row][column] = value - constant
    rank, _ = matrix_rank_and_det(matrix)
    minor_rank, determinant = matrix_rank_and_det(matrix, MINOR_ROWS)
    assert rank == minor_rank == 24
    assert determinant
    print(
        "verified mixed one-x rank witness: rank=24, "
        f"minor determinant={determinant}"
    )


def verify_forced_kx_zero_contradiction():
    parameters = [Fraction(0) for _ in FREE]
    _, q0 = eliminate_q0(parameters)
    all_x = coefficient(q0, VERTICES, (X,) * N)
    assert all_x == Fraction(-119, 145924)
    assert all_x != 2
    print(f"verified Kx=0 gives [X]H(q0)={all_x}, not 2")


def verify_five_star_classes_at_kx_zero():
    parameters = [Fraction(0) for _ in FREE]
    matrix = transport_matrix(parameters)
    d0 = [row[:5] for row in matrix]
    correction = [row[5:] for row in matrix]
    basis = [
        [row[column] for column in CORRECTION_COLUMNS] for row in correction
    ]
    pivot = [basis[row] for row in TRANSPORT_PIVOT_ROWS]
    right = [d0[row] for row in TRANSPORT_PIVOT_ROWS]
    lift = solve_square(pivot, right)
    obstruction = []
    for row in TRANSPORT_OBSTRUCTION_ROWS:
        obstruction.append(
            [
                d0[row][column]
                - sum(basis[row][index] * lift[index][column] for index in range(32))
                for column in range(5)
            ]
        )
    unit = Fraction(-12, 191)
    expected = [
        [3, 3, 3, 3, 3],
        [unit, 0, 0, unit, unit],
        [unit, 0, unit, 0, unit],
        [unit, 0, unit, unit, 0],
        [unit, unit, unit, 0, 0],
    ]
    assert obstruction == expected
    rank, determinant = matrix_rank_and_det(obstruction, range(5))
    assert rank == 5
    assert determinant == Fraction(124416, 1330863361)
    print(f"verified five D0 classes remain independent: det={determinant}")


def main():
    verify_mixed_minor()
    verify_forced_kx_zero_contradiction()
    verify_five_star_classes_at_kx_zero()
    print("verified generic dense-top mixed-linear obstruction")


if __name__ == "__main__":
    main()
