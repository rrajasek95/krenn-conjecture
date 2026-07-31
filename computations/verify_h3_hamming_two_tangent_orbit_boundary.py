#!/usr/bin/env python3
"""Exact low-Hamming boundary for the h=3 global tangent-orbit proposal."""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product


Q = Fraction
SITES = tuple(range(6))
COLORS = tuple(range(3))


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in matchings(rest):
            answer.append(((first, partner),) + matching)
    return tuple(answer)


# Three pure eight-site perfect matchings, after deleting endpoints p,q.
# Physical colors equal the displayed labels.
INTERNAL = {
    (2, 3, 0, 0): Q(1),
    (4, 5, 0, 0): Q(1),
    (0, 2, 1, 1): Q(1),
    (1, 4, 1, 1): Q(1),
    (0, 4, 2, 2): Q(1),
    (1, 3, 2, 2): Q(1),
}
FIRST = {
    (0, 0, 0): Q(1),
    (1, 5, 1): Q(1),
    (2, 2, 2): Q(1),
}
SECOND = {
    (0, 1, 0): Q(1),
    (1, 3, 1): Q(1),
    (2, 5, 2): Q(1),
}
DIRECT = {(0, 1): Q(1)}


def q_entry(x, y, cx, cy):
    if x > y:
        x, y, cx, cy = y, x, cy, cx
    return INTERNAL.get((x, y, cx, cy), Q(0))


def hafnian(word, vertices=SITES):
    return sum(
        (
            product_value(q_entry(x, y, word[x], word[y]) for x, y in matching)
            for matching in matchings(tuple(vertices))
        ),
        Q(0),
    )


def product_value(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def response(i, j, word):
    total = Q(0)
    for x in SITES:
        p_value = FIRST.get((i, x, word[x]), Q(0))
        if not p_value:
            continue
        for y in SITES:
            if x == y:
                continue
            s_value = SECOND.get((j, y, word[y]), Q(0))
            if not s_value:
                continue
            complement = tuple(site for site in SITES if site not in (x, y))
            total += p_value * s_value * hafnian(word, complement)
    return total


def row(i, j, word):
    return DIRECT.get((i, j), Q(0)) * hafnian(word) + response(i, j, word)


def target(i, j, word):
    return Q(i == j and all(color == i for color in word))


def hamming_distance(word):
    return min(sum(entry != color for entry in word) for color in COLORS)


def matrix_rank(rows):
    work = [list(map(Q, row)) for row in rows]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((r for r in range(rank, len(work)) if work[r][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for r in range(len(work)):
            if r == rank or not work[r][column]:
                continue
            scale = work[r][column]
            work[r] = [left - scale * right for left, right in zip(work[r], work[rank])]
        rank += 1
    return rank


def audit_rows():
    admitted = 0
    failures = []
    selected_failures = []
    for word in product(COLORS, repeat=6):
        distance = hamming_distance(word)
        for i, j in product(COLORS, repeat=2):
            residual = row(i, j, word) - target(i, j, word)
            if distance <= 2:
                require(residual == 0, ("low-Hamming row failed", distance, word, i, j, residual))
                admitted += 1
            if residual:
                failures.append((distance, word, i, j, residual))
                if (i, j) == (0, 1):
                    selected_failures.append((distance, word, residual))
    require(admitted == 1971, ("wrong distance-at-most-two count", admitted))
    require(
        failures
        == [
            (3, (0, 1, 0, 0, 1, 2), 0, 2, Q(1)),
            (4, (1, 2, 1, 2, 0, 0), 0, 1, Q(1)),
            (3, (2, 0, 0, 0, 2, 1), 1, 0, Q(1)),
        ],
        ("full residual ledger changed", failures),
    )
    require(
        selected_failures == [(4, (1, 2, 1, 2, 0, 0), Q(1))],
        ("selected residual ledger changed", selected_failures),
    )


def response_quadratic(i, j):
    result = {}
    for x, y in combinations(SITES, 2):
        for cx, cy in product(COLORS, repeat=2):
            value = (
                FIRST.get((i, x, cx), Q(0)) * SECOND.get((j, y, cy), Q(0))
                + FIRST.get((i, y, cy), Q(0)) * SECOND.get((j, x, cx), Q(0))
            )
            if value:
                result[((x, cx), (y, cy))] = value
    return result


def multiply_quadratics(left, right):
    result = {}
    for monomial_left, coefficient_left in left.items():
        sites_left = {site for site, _ in monomial_left}
        for monomial_right, coefficient_right in right.items():
            if sites_left.intersection(site for site, _ in monomial_right):
                continue
            monomial = tuple(sorted(monomial_left + monomial_right))
            result[monomial] = result.get(monomial, Q(0)) + coefficient_left * coefficient_right
    return {monomial: value for monomial, value in result.items() if value}


def union_is_hamilton(first, second):
    adjacency = {vertex: [] for vertex in range(8)}
    for matching in (first, second):
        for x, y in matching:
            adjacency[x].append(y)
            adjacency[y].append(x)
    seen = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                frontier.append(neighbor)
    return len(seen) == 8


def audit_goodness_and_tangent_obstruction():
    first_rows = [
        [FIRST.get((label, site, color), Q(0)) for label in COLORS]
        for site in SITES for color in COLORS
    ]
    second_rows = [
        [SECOND.get((label, site, color), Q(0)) for label in COLORS]
        for site in SITES for color in COLORS
    ]
    require(matrix_rank(first_rows) == 3, "first star is not good")
    require(matrix_rank(second_rows) == 3, "second star is not good")
    require(DIRECT == {(0, 1): Q(1)}, "direct block is not exactly E_01")

    responses = {
        (i, j): response_quadratic(i, j)
        for i, j in product(COLORS, repeat=2)
    }
    for i, k, j, ell in product(COLORS, repeat=4):
        require(
            multiply_quadratics(responses[i, j], responses[k, ell])
            == multiply_quadratics(responses[i, ell], responses[k, j]),
            ("literal Segre rectangle failed", i, k, j, ell),
        )

    # Selected (a,b)=(0,1): R=p_0s_1 is the nonzero 03 block, while q_03=0.
    require(FIRST[(0, 0, 0)] * SECOND[(1, 3, 1)] == 1, "selected R_03 moved")
    require(
        all(q_entry(0, 3, cx, cy) == 0 for cx in COLORS for cy in COLORS),
        "q_03 ceased to be the zero block",
    )

    # R q^[2] vanishes identically; the first selected-row detector is q^[3].
    for word in product(COLORS, repeat=6):
        require(response(0, 1, word) == 0, ("selected response acquired a cofactor", word))

    selected_response = responses[0, 1]
    require(
        selected_response == {((0, 0), (3, 1)): Q(1)},
        ("selected response support changed", selected_response),
    )
    require(
        multiply_quadratics(selected_response, selected_response) == {},
        "R^[2] is no longer zero",
    )

    factors = (
        ((0, 6), (1, 7), (2, 3), (4, 5)),
        ((0, 2), (1, 4), (3, 7), (5, 6)),
        ((0, 4), (1, 3), (2, 6), (5, 7)),
    )
    require(
        all(union_is_hamilton(factors[i], factors[j]) for i, j in combinations(COLORS, 2)),
        "the three pure factors lost pairwise Hamilton separation",
    )


def audit_mutations():
    pure_zero = (0,) * 6
    key = (2, 3, 0, 0)
    saved = INTERNAL.pop(key)
    try:
        require(row(0, 0, pure_zero) == 0, "deleted pure cofactor edge was not detected")
    finally:
        INTERNAL[key] = saved

    key = (0, 0, 0)
    saved = FIRST.pop(key)
    try:
        require(row(0, 0, pure_zero) == 0, "deleted first-star anchor was not detected")
    finally:
        FIRST[key] = saved

    selected_word = (1, 2, 1, 2, 0, 0)
    saved = DIRECT.pop((0, 1))
    try:
        require(row(0, 1, selected_word) == 0, "deleted live direct scalar was not detected")
    finally:
        DIRECT[(0, 1)] = saved


def main():
    audit_rows()
    audit_goodness_and_tangent_obstruction()
    audit_mutations()
    print(
        "PASS: all 1971 distance<=2 full-nine coefficients and all anchors; "
        "good Segre stars; d=E_01; q_03=0<R_03; no site derivation; "
        "R^[2]=chi=0; exact three-residual ledger"
    )


if __name__ == "__main__":
    main()
