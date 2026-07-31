#!/usr/bin/env python3
"""Exact audit for the h=3 pure-nine rank-two hafnian boundary.

This checks only the scope claimed in
``notes/h3-pure-nine-rank-two-hafnian-update-boundary.md``.  In
particular, it verifies every constant-colour coefficient and then checks
an explicit Hamming-one failure; it does not claim a complete source.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import factorial


Q = Fraction
SITES = tuple(range(6))
COLORS = tuple(range(3))
MATCHING = ((0, 1), (2, 3), (4, 5))


def matrix(rows):
    return [[Q(entry) for entry in row] for row in rows]


D = matrix(((0, 1, 0), (0, 0, 1), (1, 0, 0)))
U = matrix(
    (
        (1, 1, 0),
        (1, 0, 0),
        (1, 0, 1),
        (1, 0, 0),
        (1, 0, 0),
        (1, 0, 0),
    )
)
def second_star_two(parameter):
    return matrix(
        (
            (1, 1, 0),
            (0, 0, -1),
            (0, 1, 0),
            (-1, 0, 1),
            (0, parameter, 0),
            (0, -3 - parameter, 0),
        )
    )


SECOND_STARS = (
    matrix(((2, -1, 1), (0, 0, -1), (0, 0, 0), (-1, 0, 0), (0, 0, 0), (0, 0, 0))),
    matrix(((1, -2, 1), (0, 1, -1), (0, 0, 0), (-1, 0, 0), (0, 0, 0), (0, 0, 0))),
    second_star_two(0),
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rank(entries):
    work = [row[:] for row in entries]
    answer = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(answer, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        scale = work[answer][column]
        work[answer] = [entry / scale for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                left - scale * right
                for left, right in zip(work[row], work[answer])
            ]
        answer += 1
    return answer


def zero_matrix(size):
    return [[Q(0) for _ in range(size)] for _ in range(size)]


INTERNAL = zero_matrix(6)
for left, right in MATCHING:
    INTERNAL[left][right] = INTERNAL[right][left] = Q(1)


def hafnian(entries, vertices=SITES):
    vertices = tuple(vertices)

    @lru_cache(maxsize=None)
    def recur(remaining):
        if not remaining:
            return Q(1)
        first = remaining[0]
        answer = Q(0)
        for position, partner in enumerate(remaining[1:], start=1):
            rest = remaining[1:position] + remaining[position + 1 :]
            answer += entries[first][partner] * recur(rest)
        return answer

    return recur(vertices)


COHAF = zero_matrix(6)
for left in SITES:
    for right in SITES:
        if left != right:
            rest = tuple(site for site in SITES if site not in (left, right))
            COHAF[left][right] = hafnian(INTERNAL, rest)


def sandwich(first, middle, second):
    return [
        [
            sum(
                first[x][i] * middle[x][y] * second[y][j]
                for x in SITES
                for y in SITES
            )
            for j in COLORS
        ]
        for i in COLORS
    ]


def matrix_add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def unit(index):
    return [
        [Q(i == index and j == index) for j in COLORS]
        for i in COLORS
    ]


require(hafnian(INTERNAL) == 1, "the pure internal hafnian is not one")
require(rank(U) == 3, "the first star is not good")
for color, second in enumerate(SECOND_STARS):
    require(rank(second) == 3, f"second star is not good in colour {color}")
    pure_rows = matrix_add(D, sandwich(U, COHAF, second))
    require(pure_rows == unit(color), f"pure full-nine rows failed in colour {color}")


def product(values, subset):
    answer = Q(1)
    for index in subset:
        answer *= values[index]
    return answer


def update_layer(k, u, v):
    answer = Q(0)
    for left in combinations(SITES, k):
        left_set = frozenset(left)
        for right in combinations(SITES, k):
            if left_set.intersection(right):
                continue
            rest = tuple(
                site for site in SITES if site not in left_set and site not in right
            )
            answer += product(u, left) * product(v, right) * hafnian(INTERNAL, rest)
    return Q(factorial(k)) * answer


SELECTED_U = [row[0] for row in U]
SELECTED_V = [row[1] for row in SECOND_STARS[2]]
RESPONSE = zero_matrix(6)
for left in SITES:
    for right in SITES:
        if left != right:
            RESPONSE[left][right] = (
                SELECTED_U[left] * SELECTED_V[right]
                + SELECTED_V[left] * SELECTED_U[right]
            )

UPDATED = [
    [INTERNAL[i][j] + RESPONSE[i][j] for j in SITES]
    for i in SITES
]
LAYERS = tuple(update_layer(k, SELECTED_U, SELECTED_V) for k in range(4))
require(LAYERS == (Q(1), Q(-1), Q(-10), Q(-18)), "wrong update layers")
require(LAYERS[0] + LAYERS[1] == 0, "selected top row did not cancel")
require(hafnian(UPDATED) == sum(LAYERS) == Q(-28), "rank-two update mismatch")

for parameter in map(Q, (-3, -2, -1, 0, 1, 2, 3)):
    candidate = second_star_two(parameter)
    require(rank(candidate) == 3, f"parameter star lost rank at t={parameter}")
    require(
        matrix_add(D, sandwich(U, COHAF, candidate)) == unit(2),
        f"pure rows moved at t={parameter}",
    )
    varying_v = [row[1] for row in candidate]
    varying_layers = tuple(
        update_layer(k, SELECTED_U, varying_v) for k in range(4)
    )
    expected_second = -4 * parameter**2 - 12 * parameter - 10
    expected_third = -12 * parameter**2 - 36 * parameter - 18
    require(
        varying_layers
        == (Q(1), Q(-1), expected_second, expected_third),
        f"parameter-layer formula failed at t={parameter}",
    )


# A small square-free site polynomial audit of every literal Segre rectangle.
# A monomial is a length-six tuple: -1 means an empty site, otherwise the
# entry is its physical colour.
EMPTY = (-1,) * 6


def add_term(polynomial, monomial, coefficient):
    if coefficient:
        polynomial[monomial] = polynomial.get(monomial, Q(0)) + coefficient
        if not polynomial[monomial]:
            del polynomial[monomial]


def multiply(left, right):
    answer = {}
    for first, first_value in left.items():
        for second, second_value in right.items():
            if any(first[site] >= 0 and second[site] >= 0 for site in SITES):
                continue
            monomial = tuple(
                first[site] if first[site] >= 0 else second[site]
                for site in SITES
            )
            add_term(answer, monomial, first_value * second_value)
    return answer


def linear_star(entries_by_color, column):
    answer = {}
    for color in COLORS:
        entries = entries_by_color[color]
        for site in SITES:
            monomial = list(EMPTY)
            monomial[site] = color
            add_term(answer, tuple(monomial), entries[site][column])
    return answer


FIRST_BY_COLOR = (U, U, U)
P = tuple(linear_star(FIRST_BY_COLOR, index) for index in COLORS)
S = tuple(linear_star(SECOND_STARS, index) for index in COLORS)
R = tuple(tuple(multiply(P[i], S[j]) for j in COLORS) for i in COLORS)
for i in COLORS:
    for k in COLORS:
        for j in COLORS:
            for ell in COLORS:
                require(
                    multiply(R[i][j], R[k][ell])
                    == multiply(R[i][ell], R[k][j]),
                    f"Segre rectangle failed at {(i, k, j, ell)}",
                )


def selected_row_coefficient(word):
    # q^[3] uses the sole underlying matching 01|23|45.
    direct = Q(all(word[left] == word[right] for left, right in MATCHING))
    response = Q(0)
    for chosen, (left, right) in enumerate(MATCHING):
        if not all(
            word[x] == word[y]
            for position, (x, y) in enumerate(MATCHING)
            if position != chosen
        ):
            continue
        response += (
            U[left][0] * SECOND_STARS[word[right]][right][1]
            + SECOND_STARS[word[left]][left][1] * U[right][0]
        )
    return D[0][1] * direct + response


require(
    selected_row_coefficient((0, 2, 2, 2, 2, 2)) == -1,
    "the claimed Hamming-one failure was not reproduced",
)

print(
    "PASS: all 27 pure rows, good shared stars, rank-two layers "
    "(1,-1,-10,-18), chi_2=-28; first Hamming-one row=-1"
)
