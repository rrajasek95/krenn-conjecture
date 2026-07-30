#!/usr/bin/env python3
"""Sparse exact checks for the two-chart diagonal/off-diagonal guards."""

from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations


SITES = ("p", "q", "r", "a", "b", "c", "d", "s")


def key(values):
    return tuple(sorted(values.items()))


def add(*polys):
    out = defaultdict(F)
    for poly in polys:
        for monomial, value in poly.items():
            out[monomial] += value
    return {m: v for m, v in out.items() if v}


def scale(poly, scalar):
    return {m: scalar * v for m, v in poly.items() if scalar * v}


def multiply(left, right):
    out = defaultdict(F)
    for ml, vl in left.items():
        dl = dict(ml)
        for mr, vr in right.items():
            dr = dict(mr)
            if set(dl) & set(dr):
                continue
            out[key(dl | dr)] += vl * vr
    return {m: v for m, v in out.items() if v}


def divided_power(poly, exponent):
    if exponent == 0:
        return {(): F(1)}
    out = defaultdict(F)
    for chosen in combinations(list(poly.items()), exponent):
        product = {(): F(1)}
        for monomial, value in chosen:
            product = multiply(product, {monomial: value})
        for monomial, value in product.items():
            out[monomial] += value
    return {m: v for m, v in out.items() if v}


def local(site, colour, weight=1):
    return {key({site: colour}): F(weight)}


def edge(x, y, colour_x, colour_y, weight=1):
    return {key({x: colour_x, y: colour_y}): F(weight)}


def target(sites, colour):
    return {key({site: colour for site in sites}): F(1)}


def vector_rank(rows):
    coordinates = sorted({m for row in rows for m in row})
    matrix = [[row.get(m, F(0)) for m in coordinates] for row in rows]
    rank = column = 0
    while rank < len(matrix) and column < len(coordinates):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            column += 1
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [x / pivot_value for x in matrix[rank]]
        for i in range(len(matrix)):
            if i != rank and matrix[i][column]:
                factor = matrix[i][column]
                matrix[i] = [x - factor * y for x, y in zip(matrix[i], matrix[rank])]
        rank += 1
        column += 1
    return rank


def proportional(left, right):
    if not left or not right:
        return False
    witness = next(iter(right))
    if witness not in left:
        return False
    ratio = left[witness] / right[witness]
    return left == scale(right, ratio)


def chart(cells, endpoint_x, endpoint_y):
    residual = tuple(s for s in SITES if s not in (endpoint_x, endpoint_y))
    internal = {}
    first = [{} for _ in range(3)]
    second = [{} for _ in range(3)]
    direct = [[F(0) for _ in range(3)] for _ in range(3)]
    for x, y, colour_x, colour_y, weight in cells:
        if (x, y) == (endpoint_x, endpoint_y):
            direct[colour_x][colour_y] += weight
        elif (x, y) == (endpoint_y, endpoint_x):
            direct[colour_y][colour_x] += weight
        elif x == endpoint_x:
            first[colour_x] = add(first[colour_x], local(y, colour_y, weight))
        elif y == endpoint_x:
            first[colour_y] = add(first[colour_y], local(x, colour_x, weight))
        elif x == endpoint_y:
            second[colour_x] = add(second[colour_x], local(y, colour_y, weight))
        elif y == endpoint_y:
            second[colour_y] = add(second[colour_y], local(x, colour_x, weight))
        else:
            internal = add(internal, edge(x, y, colour_x, colour_y, weight))
    return residual, internal, first, second, direct


def audit_chart(cells, endpoints, expected_rows, omega_kind):
    residual, q, first, second, direct = chart(cells, *endpoints)
    q2, q3 = divided_power(q, 2), divided_power(q, 3)
    assert vector_rank(first) == vector_rank(second) == 3
    for i in range(3):
        for j in range(3):
            lhs = add(
                scale(q3, direct[i][j]),
                multiply(multiply(first[i], second[j]), q2),
            )
            marker = expected_rows[i][j]
            if marker is not None:
                expected = target(residual, i) if marker else {}
                assert lhs == expected, (endpoints, i, j, lhs, expected)

    sigma = direct[0][0]
    x = multiply(first[0], second[0])
    response = scale(
        add(multiply(first[1], second[1]), multiply(first[2], second[2])), -1
    )
    effective = add(scale(q, sigma), x)
    binary_target = scale(add(target(residual, 1), target(residual, 2)), -1)
    omega0 = add(
        multiply(response, divided_power(effective, 2)),
        scale(binary_target, -(sigma**2)),
    )
    omega1 = multiply(divided_power(response, 2), effective)
    assert divided_power(effective, 3) == scale(target(residual, 0), sigma**2)
    assert not divided_power(response, 3)
    if omega_kind == "independent":
        assert omega0 and omega1 and not proportional(omega0, omega1)
    else:
        assert omega0 and not omega1
    return q2


def cells(table):
    return [(x, y, colour, colour, F(weight)) for colour, x, y, weight in table]


DIAGONAL_GUARD = cells([
    (0, "p", "q", 1), (0, "p", "r", 1), (0, "p", "a", 1),
    (0, "q", "b", 1), (0, "c", "d", 1), (0, "r", "s", 1),
    (1, "p", "d", 1), (1, "q", "s", 1), (1, "a", "c", 1),
    (1, "b", "r", 1), (2, "p", "c", 1), (2, "q", "r", 1),
    (2, "a", "d", 1), (2, "b", "s", 1),
])

INDEPENDENT_GUARD = cells([
    (0, "p", "q", 6), (0, "p", "r", 6), (0, "p", "a", 1),
    (0, "p", "b", 1), (0, "p", "c", 1), (0, "q", "r", 1),
    (0, "q", "d", 1), (0, "q", "s", 6), (0, "r", "d", 2),
    (0, "r", "s", 3), (1, "p", "a", 1), (1, "q", "r", 1),
    (2, "p", "b", 1), (2, "q", "d", 1), (2, "r", "d", 1),
])

ENDPOINT_GUARD = cells([
    (0, "p", "q", 6), (0, "p", "r", 6), (0, "p", "a", 1),
    (0, "p", "b", 1), (0, "p", "c", 1), (0, "q", "r", 1),
    (0, "q", "d", 1), (0, "q", "s", 6), (0, "r", "d", -1),
    (0, "r", "s", -6), (0, "a", "b", F(-1, 12)),
    (1, "p", "a", 1), (1, "q", "r", 1),
    (2, "p", "b", 1), (2, "q", "r", 1),
])


def main():
    global_guard = {}
    for x, y, colour_x, colour_y, weight in DIAGONAL_GUARD:
        global_guard = add(global_guard, edge(x, y, colour_x, colour_y, weight))
    expected_global = {}
    left_shore = {"p", "a", "c", "d"}
    for i in range(3):
        for j in range(3):
            word = {site: (i if site in left_shore else j) for site in SITES}
            expected_global[key(word)] = F(1)
    assert divided_power(global_guard, 4) == expected_global

    diagonal_rows = [[True if i == j else None for j in range(3)] for i in range(3)]
    off_diagonal_rows = [[False for _ in range(3)] for _ in range(3)]
    unary_and_off_diagonal = [row[:] for row in off_diagonal_rows]
    unary_and_off_diagonal[0][0] = True

    for endpoints in (("p", "q"), ("p", "r")):
        # The diagonal guard deliberately has six nonzero mixed failures.
        residual, q, first, second, direct = chart(DIAGONAL_GUARD, *endpoints)
        q2, q3 = divided_power(q, 2), divided_power(q, 3)
        assert vector_rank(first) == vector_rank(second) == 3
        for i in range(3):
            for j in range(3):
                lhs = add(scale(q3, direct[i][j]), multiply(multiply(first[i], second[j]), q2))
                if i == j:
                    assert lhs == target(residual, i)
                else:
                    assert len(lhs) == 1 and next(iter(lhs.values())) == 1
        audit_chart(DIAGONAL_GUARD, endpoints, diagonal_rows, "independent")

        assert not audit_chart(INDEPENDENT_GUARD, endpoints, off_diagonal_rows, "independent")
        assert audit_chart(ENDPOINT_GUARD, endpoints, unary_and_off_diagonal, "one_zero")

    assert F(6) * F(3) - F(6) * F(6) == -18
    assert F(6) * F(-6) - F(6) * F(6) == -72
    print("PASS: two-chart diagonal/off-diagonal complementarity")


if __name__ == "__main__":
    main()
