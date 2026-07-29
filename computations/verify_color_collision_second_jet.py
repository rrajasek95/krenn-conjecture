#!/usr/bin/env python3
"""Exact color-collision jet audits on two binary GHZ fibers.

Colors are x=0, y=1, z=2.  We verify two claims at n=6:

* the complete first-jet affine solution space over each displayed binary
  base is the hard-coded family below;
* one all-x/z second-jet coefficient is identically 1/2 on that family,
  including every possible Q2 correction, whereas splitting one of the two
  coincident x branches requires coefficient 1.

The script also checks the expected n=4 exception: the three one-factors of
K4 give a regular collision arc to all orders.
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
    u = vertices[0]
    for position, v in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


def edges(n):
    return tuple(itertools.combinations(range(n), 2))


def first_variables(n):
    return tuple(
        (u, v, a, b)
        for u, v in edges(n)
        for a, b in ((Z, X), (Z, Y), (X, Z), (Y, Z))
    )


def first_system(n, q0):
    variables = first_variables(n)
    index = {key: position for position, key in enumerate(variables)}
    matrix = []
    target = []
    for coloring in itertools.product(range(3), repeat=n):
        if coloring.count(Z) != 1:
            continue
        row = [0] * len(variables)
        for matching in perfect_matchings(range(n)):
            for exceptional, (u, v) in enumerate(matching):
                key = (u, v, coloring[u], coloring[v])
                if key not in index:
                    continue
                coefficient = 1
                for position, (a, b) in enumerate(matching):
                    if position != exceptional:
                        coefficient *= q0.get(
                            (a, b, coloring[a], coloring[b]), 0
                        )
                row[index[key]] += coefficient
        matrix.append(row)
        target.append(int(Y not in coloring))
    return variables, matrix, target


def rank_mod(matrix, prime=1_000_003):
    def reduce(value):
        value = Fraction(value)
        return value.numerator * pow(value.denominator, prime - 2, prime) % prime

    rows = [[reduce(value) for value in row] for row in matrix]
    rank = 0
    columns = len(rows[0]) if rows else 0
    for column in range(columns):
        pivot = next(
            (index for index in range(rank, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], prime - 2, prime)
        rows[rank] = [value * inverse % prime for value in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            multiple = rows[index][column]
            rows[index] = [
                (left - multiple * right) % prime
                for left, right in zip(rows[index], rows[rank])
            ]
        rank += 1
    return rank


def affine(constant=0, parameter_count=0, parameter=None, scale=1):
    answer = [Fraction(constant)] + [Fraction(0)] * parameter_count
    if parameter is not None:
        answer[1 + parameter] = Fraction(scale)
    return tuple(answer)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def scale(value, scalar):
    return tuple(Fraction(scalar) * item for item in value)


def verify_first_family(name, n, q0, family, parameter_count, expected_rank):
    variables, matrix, target = first_system(n, q0)
    zero = affine(parameter_count=parameter_count)
    forms = [family.get(variable, zero) for variable in variables]

    # Constant part solves the affine system, and every parameter column is
    # in the homogeneous kernel.
    for row, rhs in zip(matrix, target):
        image = affine(parameter_count=parameter_count)
        for coefficient, form in zip(row, forms):
            image = add(image, scale(form, coefficient))
        assert image[0] == rhs
        assert all(value == 0 for value in image[1:])

    # Modular rank is a rational lower bound.  The displayed independent
    # kernel columns give the matching upper bound, proving exhaustiveness.
    rank = rank_mod(matrix)
    assert rank == expected_rank
    assert len(variables) - rank == parameter_count
    parameter_matrix = [list(form[1:]) for form in forms]
    assert rank_mod(parameter_matrix) == parameter_count
    print(
        f"verified {name} first-jet family: rank={rank}, "
        f"nullity={parameter_count}"
    )


def multiply_affine(left, right):
    size = len(left) - 1
    constant = left[0] * right[0]
    linear = [left[0] * right[i + 1] + right[0] * left[i + 1]
              for i in range(size)]
    quadratic = [[left[i + 1] * right[j + 1] for j in range(size)]
                 for i in range(size)]
    return constant, linear, quadratic


def verify_frozen_second(
    name, n, q0, q1, parameter_count, coloring, expected=Fraction(1, 2)
):
    zero = affine(parameter_count=parameter_count)
    constant = Fraction(0)
    linear = [Fraction(0)] * parameter_count
    quadratic = [
        [Fraction(0)] * parameter_count for _ in range(parameter_count)
    ]
    q2_coefficients = {edge: Fraction(0) for edge in edges(n)}

    for matching in perfect_matchings(range(n)):
        # One Q2 edge and two Q0 edges.
        for exceptional, edge in enumerate(matching):
            u, v = edge
            if (coloring[u], coloring[v]) != (Z, Z):
                continue
            coefficient = 1
            for position, (a, b) in enumerate(matching):
                if position != exceptional:
                    coefficient *= q0.get(
                        (a, b, coloring[a], coloring[b]), 0
                    )
            q2_coefficients[edge] += coefficient

        # Two Q1 edges and one Q0 edge.
        for first, second in itertools.combinations(range(3), 2):
            remaining = 3 - first - second
            a, b = matching[remaining]
            coefficient = q0.get((a, b, coloring[a], coloring[b]), 0)
            if not coefficient:
                continue
            selected = []
            for position in (first, second):
                u, v = matching[position]
                selected.append(
                    q1.get((u, v, coloring[u], coloring[v]), zero)
                )
            c0, c1, c2 = multiply_affine(*selected)
            constant += coefficient * c0
            for i in range(parameter_count):
                linear[i] += coefficient * c1[i]
                for j in range(parameter_count):
                    quadratic[i][j] += coefficient * c2[i][j]

    assert constant == expected
    assert all(value == 0 for value in linear)
    assert all(value == 0 for row in quadratic for value in row)
    assert all(value == 0 for value in q2_coefficients.values())
    assert expected != 1
    print(
        f"verified {name} frozen coefficient {coloring}: "
        f"all Q1 kernels and Q2 corrections give {expected}, target=1"
    )


def hamilton_case():
    n = 6
    px = ((0, 1), (2, 3), (4, 5))
    py = ((1, 2), (3, 4), (0, 5))
    q0 = {}
    for position, edge in enumerate(px):
        q0[edge + (X, X)] = 2 if position == 0 else 1
    for edge in py:
        q0[edge + (Y, Y)] = 1

    chords = ((0, 2), (0, 4), (1, 3), (1, 5), (2, 4), (3, 5))
    parameter_count = 24
    q1 = {}
    for edge in px:
        weight = q0[edge + (X, X)]
        q1[edge + (Z, X)] = affine(Fraction(weight, 2), parameter_count)
        q1[edge + (X, Z)] = affine(Fraction(weight, 2), parameter_count)
    parameter = 0
    for edge in chords:
        for colors in ((Z, X), (Z, Y), (X, Z), (Y, Z)):
            q1[edge + colors] = affine(
                parameter_count=parameter_count, parameter=parameter
            )
            parameter += 1
    assert parameter == parameter_count

    verify_first_family(
        "Hamilton base", n, q0, q1, parameter_count, expected_rank=36
    )
    verify_frozen_second(
        "Hamilton base", n, q0, q1, parameter_count,
        coloring=(X, X, X, Z, X, Z),
    )


def switched_case():
    n = 6
    p0 = ((0, 1), (2, 3), (4, 5))
    p0_prime = ((0, 2), (1, 3), (4, 5))
    py = ((1, 2), (3, 4), (0, 5))
    q0 = {edge + (X, X): 1 for edge in set(p0) | set(p0_prime)}
    q0.update({edge + (Y, Y): 1 for edge in py})
    parameter_count = 14
    z = lambda constant=0, parameter=None, scale=1: affine(
        constant, parameter_count, parameter, scale
    )
    q1 = {
        (0, 1, Z, X): add(z(1), z(parameter=0, scale=-1)),
        (0, 1, X, Z): add(z(1), z(parameter=5, scale=-1)),
        (0, 2, Z, X): z(parameter=0),
        (0, 2, X, Z): add(z(1), z(parameter=6, scale=-1)),
        (0, 4, Z, X): z(parameter=1),
        (0, 4, Z, Y): z(parameter=2),
        (0, 4, X, Z): z(parameter=3),
        (0, 4, Y, Z): z(parameter=4),
        (1, 3, Z, X): z(parameter=5),
        (1, 3, X, Z): add(z(1), z(parameter=7, scale=-1)),
        (1, 4, X, Z): z(parameter=8, scale=-1),
        (1, 5, X, Z): z(parameter=9, scale=-1),
        (2, 3, Z, X): z(parameter=6),
        (2, 3, X, Z): z(parameter=7),
        (2, 4, X, Z): z(parameter=8),
        (2, 5, X, Z): z(parameter=9),
        (3, 5, Z, X): z(parameter=10),
        (3, 5, Z, Y): z(parameter=11),
        (3, 5, X, Z): z(parameter=12),
        (3, 5, Y, Z): z(parameter=13),
        (4, 5, Z, X): z(Fraction(1, 2)),
        (4, 5, X, Z): z(Fraction(1, 2)),
    }

    verify_first_family(
        "switched base", n, q0, q1, parameter_count, expected_rank=46
    )
    verify_frozen_second(
        "switched base", n, q0, q1, parameter_count,
        coloring=(X, X, X, Z, X, Z),
    )


def four_vertex_exception():
    n = 4
    fixed = ((0, 1), (2, 3))
    y_matching = ((0, 2), (1, 3))
    moving = ((0, 3), (1, 2))

    # Each entry is a polynomial in t, represented low degree first.
    tables = {}
    for edge in fixed:
        tables[edge + (X, X)] = (1,)
    for edge in y_matching:
        tables[edge + (Y, Y)] = (1,)
    for edge in moving:
        tables[edge + (X, X)] = (1,)
        tables[edge + (Z, X)] = (0, 1)
        tables[edge + (X, Z)] = (0, 1)
        tables[edge + (Z, Z)] = (0, 0, 1)

    def poly_multiply(left, right):
        answer = [0] * (len(left) + len(right) - 1)
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                answer[i + j] += a * b
        return tuple(answer)

    for coloring in itertools.product(range(3), repeat=n):
        total = [0] * (n + 1)
        for matching in perfect_matchings(range(n)):
            term = (1,)
            for u, v in matching:
                term = poly_multiply(
                    term, tables.get((u, v, coloring[u], coloring[v]), (0,))
                )
            for degree, coefficient in enumerate(term):
                total[degree] += coefficient
        expected = [0] * (n + 1)
        if coloring == (X,) * n:
            expected[0] = 2
        elif coloring == (Y,) * n:
            expected[0] = 1
        elif Y not in coloring and Z in coloring:
            expected[coloring.count(Z)] = 1
        assert total == expected, (coloring, total, expected)
    print("verified n=4 regular collision arc to every order")


def main():
    hamilton_case()
    switched_case()
    four_vertex_exception()


if __name__ == "__main__":
    main()
