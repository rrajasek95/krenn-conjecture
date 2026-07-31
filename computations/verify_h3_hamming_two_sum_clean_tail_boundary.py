#!/usr/bin/env python3
"""Show that the unweighted Hamming-two sum is not the h=3 clean tail."""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product


Q = Fraction
SITES = tuple(range(6))
COLORS = tuple(range(3))
PURE_MATCHING = ((0, 1), (2, 3), (4, 5))


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


def product_value(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


INTERNAL = {
    (x, y, color, color): Q(1)
    for x, y in PURE_MATCHING
    for color in COLORS
}
INTERNAL[(0, 1, 1, 0)] = Q(1)

FIRST = {
    (0, 0, 0): Q(1),
    (0, 1, 0): Q(1),
    (0, 1, 1): Q(1),
    (0, 2, 2): Q(2),
    (0, 4, 2): Q(3, 2),
    (0, 5, 2): Q(1),
    (1, 0, 1): Q(1),
    (2, 3, 2): Q(1),
}

SECOND = {
    (0, 0, 1): Q(-1),
    (0, 3, 2): Q(-1),
    (0, 4, 2): Q(1),
    (1, 0, 0): Q(-1),
    (1, 0, 1): Q(-1),
    (1, 1, 1): Q(1),
    (1, 3, 2): Q(1),
    (1, 5, 2): Q(-2),
    (2, 2, 2): Q(1),
}

DIRECT = {(0, 0): Q(1), (0, 1): Q(1)}


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


def audit_admitted_rows():
    checked = 0
    for base in COLORS:
        pure = (base,) * 6
        for i, j in product(COLORS, repeat=2):
            require(row(i, j, pure) == target(i, j, pure), ("pure row", base, i, j))
            checked += 1
        for site in SITES:
            for defect in COLORS:
                if defect == base:
                    continue
                word = tuple(defect if x == site else base for x in SITES)
                for i, j in product(COLORS, repeat=2):
                    require(row(i, j, word) == 0, ("Hamming-one row", word, i, j))
                    checked += 1
    require(checked == 351, ("wrong admitted count", checked))


def selected_layers():
    color = 2
    u = [FIRST.get((0, site, color), Q(0)) for site in SITES]
    v = [SECOND.get((1, site, color), Q(0)) for site in SITES]
    internal = {
        (x, y): q_entry(x, y, color, color)
        for x, y in combinations(SITES, 2)
    }
    response_edges = {
        (x, y): u[x] * v[y] + v[x] * u[y]
        for x, y in combinations(SITES, 2)
    }
    layers = [Q(0)] * 4
    for matching in matchings(SITES):
        for flags in product((0, 1), repeat=3):
            layer = sum(flags)
            layers[layer] += product_value(
                response_edges[edge] if flag else internal[edge]
                for flag, edge in zip(flags, matching)
            )
    return u, v, layers


def audit_sum_is_not_tail():
    u, v, layers = selected_layers()
    require(u == [0, 0, 2, 0, Q(3, 2), 1], ("selected u moved", u))
    require(v == [0, 0, 0, 1, 0, -2], ("selected v moved", v))
    require(layers == [1, -1, -12, 0], ("response layers moved", layers))
    require(layers[0] + layers[1] == 0, "selected pure top row failed")
    clean_tail = layers[2] + layers[3]

    residuals = []
    for word in product(COLORS, repeat=6):
        if sum(color != 2 for color in word) != 2:
            continue
        value = row(0, 1, word)
        if value:
            residuals.append((word, value))
    hamming_two_sum = sum((value for _, value in residuals), Q(0))
    require(
        residuals
        == [
            ((0, 0, 2, 2, 2, 2), Q(-1)),
            ((1, 0, 2, 2, 2, 2), Q(-1)),
            ((1, 1, 2, 2, 2, 2), Q(-1)),
            ((2, 2, 0, 0, 2, 2), Q(-2)),
            ((2, 2, 1, 1, 2, 2), Q(-2)),
            ((2, 2, 2, 2, 0, 0), Q(3)),
            ((2, 2, 2, 2, 1, 1), Q(3)),
        ],
        ("Hamming-two residual ledger changed", residuals),
    )
    require(hamming_two_sum == -1, ("Hamming-two sum moved", hamming_two_sum))
    require(clean_tail == -12, ("clean tail moved", clean_tail))
    require(4 * hamming_two_sum == -4, "wrong scaled Hamming-two sum")
    require(4 * hamming_two_sum != clean_tail, "unweighted sum accidentally became the tail")


def audit_goodness_segre_and_mutations():
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
    require(DIRECT == {(0, 0): Q(1), (0, 1): Q(1)}, "wrong direct block")

    responses = {
        (i, j): response_quadratic(i, j)
        for i, j in product(COLORS, repeat=2)
    }
    for i, k, j, ell in product(COLORS, repeat=4):
        require(
            multiply_quadratics(responses[i, j], responses[k, ell])
            == multiply_quadratics(responses[i, ell], responses[k, j]),
            ("Segre rectangle", i, k, j, ell),
        )

    saved = SECOND.pop((0, 4, 2))
    try:
        failures = sum(
            row(i, j, word) != target(i, j, word)
            for base in COLORS
            for word in [(base,) * 6]
            for i, j in product(COLORS, repeat=2)
        )
        require(failures > 0, "removing the added s_0 component was not detected")
    finally:
        SECOND[(0, 4, 2)] = saved

    saved = FIRST[(0, 4, 2)]
    FIRST[(0, 4, 2)] = Q(1)
    try:
        require(row(0, 1, (2,) * 6) != 0, "3/2 coefficient mutation was not detected")
    finally:
        FIRST[(0, 4, 2)] = saved


def main():
    audit_admitted_rows()
    audit_sum_is_not_tail()
    audit_goodness_segre_and_mutations()
    print(
        "PASS: 351 pure/Hamming-one full-nine coefficients; good Segre stars; "
        "layers (1,-1,-12,0); unweighted H2 sum=-1, so 4*sum=-4 != chi=-12"
    )


if __name__ == "__main__":
    main()
