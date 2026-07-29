#!/usr/bin/env python3
"""Exact audit for notes/overlap-complex-common-factor-countermodel.md.

The checker uses the smallest dense member, s=5.  It performs sparse
site-square-zero arithmetic over Fraction; it does not search for a model
or use a computer-algebra package.
"""

from fractions import Fraction
from itertools import combinations, permutations
from math import factorial


S = 5
COLOURS = range(3)
L = tuple(range(S))
R = tuple(range(S, 2 * S))
P = L[0]
FAN = L[1:]
LAMBDA = Fraction(1, factorial(S))
EMPTY = -1


def unit(site, colour):
    word = [EMPTY] * (2 * S)
    word[site] = colour
    return {tuple(word): Fraction(1)}


def add_term(out, word, coefficient):
    if coefficient:
        out[word] = out.get(word, Fraction(0)) + coefficient
        if not out[word]:
            del out[word]


def multiply(left, right):
    out = {}
    for u, cu in left.items():
        for v, cv in right.items():
            word = list(u)
            for site, colour in enumerate(v):
                if colour == EMPTY:
                    continue
                if word[site] != EMPTY:
                    break
                word[site] = colour
            else:
                add_term(out, tuple(word), cu * cv)
    return out


def add(left, right):
    out = dict(left)
    for word, coefficient in right.items():
        add_term(out, word, coefficient)
    return out


def scale(poly, scalar):
    return {
        word: scalar * coefficient
        for word, coefficient in poly.items()
        if scalar * coefficient
    }


def restrict(poly, sites):
    sites = set(sites)
    return {
        word: coefficient
        for word, coefficient in poly.items()
        if all(
            colour == EMPTY or site in sites
            for site, colour in enumerate(word)
        )
    }


def linear(sites, colour, coefficients=None):
    coefficients = coefficients or {}
    out = {}
    for site in sites:
        out = add(
            out,
            scale(unit(site, colour), coefficients.get(site, Fraction(1))),
        )
    return out


def edge_cell(i, a, j, b, coefficient=Fraction(1)):
    return scale(multiply(unit(i, a), unit(j, b)), coefficient)


def internal_quadratic(q):
    """The chart on W_q: I on L_q-L_q and L_q-R, zero on R-R."""
    lq = tuple(i for i in L if i not in (P, q))
    out = {}
    for i, j in combinations(lq, 2):
        for colour in COLOURS:
            out = add(out, edge_cell(i, colour, j, colour))
    for i in lq:
        for j in R:
            for colour in COLOURS:
                out = add(out, edge_cell(i, colour, j, colour))
    return out


def divided_power(poly, exponent):
    out = {tuple([EMPTY] * (2 * S)): Fraction(1)}
    for _ in range(exponent):
        out = multiply(out, poly)
    return scale(out, Fraction(1, factorial(exponent)))


def q_star(q, colour, sites):
    # Every block from q into a chart common complement is I_3.
    del q
    return linear(sites, colour)


def common_factor(colour, sites):
    return linear(tuple(i for i in sites if i in L and i != P), colour)


def correction(q, a, b):
    wq = tuple(i for i in range(2 * S) if i not in (P, q))
    return multiply(common_factor(a, wq), q_star(q, b, wq))


def supported(i, j):
    return not (i in R and j in R)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    i = vertices[0]
    for offset, j in enumerate(vertices[1:], start=1):
        if not supported(i, j):
            continue
        rest = vertices[1:offset] + vertices[offset + 1 :]
        for tail in perfect_matchings(rest):
            yield ((i, j),) + tail


def matching_coefficient(colouring):
    total = Fraction(0)
    for image in permutations(R):
        if all(colouring[i] == colouring[j] for i, j in zip(L, image)):
            total += LAMBDA  # Every bijection uses one p-R block.
    return total


def determinant3(matrix):
    return (
        matrix[0][0] * matrix[1][1] * matrix[2][2]
        + matrix[0][1] * matrix[1][2] * matrix[2][0]
        + matrix[0][2] * matrix[1][0] * matrix[2][1]
        - matrix[0][2] * matrix[1][1] * matrix[2][0]
        - matrix[0][1] * matrix[1][0] * matrix[2][2]
        - matrix[0][0] * matrix[1][2] * matrix[2][1]
    )


def graph_audit(q):
    wq = tuple(i for i in range(2 * S) if i not in (P, q))
    adjacency = {
        i: {j for j in wq if j != i and supported(i, j)}
        for i in wq
    }
    seen = {wq[0]}
    frontier = [wq[0]]
    while frontier:
        i = frontier.pop()
        for j in adjacency[i] - seen:
            seen.add(j)
            frontier.append(j)
    assert seen == set(wq)

    lq = tuple(i for i in L if i not in (P, q))
    assert len(lq) >= 2
    i, j = lq[:2]
    k = R[0]
    assert j in adjacency[i] and k in adjacency[i] and k in adjacency[j]
    return (
        len(wq),
        sum(len(neighbours) for neighbours in adjacency.values()) // 2,
    )


def rank(matrix):
    matrix = [list(map(Fraction, row)) for row in matrix]
    if not matrix:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    pivot_row = 0
    for column in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def gauge(q, alpha):
    wq = tuple(i for i in range(2 * S) if i not in (P, q))
    out = {}
    for i, j in combinations(wq, 2):
        if i in R and j in R:
            continue
        for colour in COLOURS:
            out = add(
                out,
                edge_cell(
                    i,
                    colour,
                    j,
                    colour,
                    Fraction(alpha.get(i, 0) + alpha.get(j, 0)),
                ),
            )
    return out


def column_rank(polynomials):
    words = sorted({word for poly in polynomials for word in poly})
    matrix = [
        [poly.get(word, Fraction(0)) for poly in polynomials]
        for word in words
    ]
    return rank(matrix)


def audit_normalization_and_activity():
    pure = []
    for colour in COLOURS:
        pure.append(matching_coefficient({i: colour for i in L + R}))
    assert pure == [Fraction(1)] * 3

    mixed = {i: 0 for i in L + R}
    mixed[L[1]] = 1
    mixed[R[0]] = 1
    assert P != L[1]
    mixed_coefficient = matching_coefficient(mixed)
    assert mixed_coefficient == Fraction(1, S)

    matchings = list(perfect_matchings(L + R))
    assert len(matchings) == factorial(S)
    assert all(
        all((i in L) != (j in L) for i, j in matching)
        for matching in matchings
    )
    return tuple(pure), mixed_coefficient, len(matchings)


def audit_charts_and_annihilators():
    annihilators = 0
    graph_signature = None
    for q in FAN:
        wq = tuple(i for i in range(2 * S) if i not in (P, q))
        lq = tuple(i for i in L if i not in (P, q))

        # One R-site projection is I for q and lambda I for p.
        identity = [
            [Fraction(i == j) for j in COLOURS] for i in COLOURS
        ]
        p_projection = [
            [LAMBDA * Fraction(i == j) for j in COLOURS]
            for i in COLOURS
        ]
        assert determinant3(identity) == 1
        assert determinant3(p_projection) == LAMBDA ** 3
        assert len(lq) == S - 2 >= 3

        signature = graph_audit(q)
        graph_signature = graph_signature or signature
        assert signature == graph_signature

        qpower = divided_power(internal_quadratic(q), S - 2)
        assert qpower
        for a in COLOURS:
            for b in COLOURS:
                n_ab = correction(q, a, b)
                assert n_ab
                assert not multiply(n_ab, qpower)
                annihilators += 1

        # The internal top power itself vanishes by shore imbalance.
        assert not list(perfect_matchings(wq))

        # Pair-complement activity fails after one L and one R deletion.
        complement = tuple(i for i in wq if i not in (lq[0], R[0]))
        assert not list(perfect_matchings(complement))
    return annihilators, graph_signature


def audit_overlaps():
    rows = 0
    for q, r in combinations(FAN, 2):
        common = tuple(i for i in range(2 * S) if i not in (P, q, r))
        for a in COLOURS:
            for b in COLOURS:
                for c in COLOURS:
                    left = multiply(
                        restrict(correction(q, a, b), common),
                        q_star(r, c, common),
                    )
                    right = multiply(
                        restrict(correction(r, a, c), common),
                        q_star(q, b, common),
                    )
                    assert left == right
                    rows += 1
    assert rows == len(tuple(combinations(FAN, 2))) * 27
    return rows


def audit_gauge_quotients():
    q = FAN[0]
    wq = tuple(i for i in range(2 * S) if i not in (P, q))
    n_columns = [
        correction(q, a, b) for a in COLOURS for b in COLOURS
    ]
    assert column_rank(n_columns) == 9

    full_gauges = [gauge(q, {site: 1}) for site in wq]
    last = wq[-1]
    zero_sum_gauges = [
        gauge(q, {site: 1, last: -1}) for site in wq[:-1]
    ]
    full_rank = column_rank(full_gauges)
    zero_sum_rank = column_rank(zero_sum_gauges)
    assert (full_rank, zero_sum_rank) == (len(wq), len(wq) - 1)

    assert column_rank(zero_sum_gauges + n_columns) == zero_sum_rank + 9
    assert column_rank(full_gauges + n_columns) == full_rank + 8

    scalar_cocycle = {}
    for colour in COLOURS:
        scalar_cocycle = add(scalar_cocycle, correction(q, colour, colour))
    lq = tuple(i for i in L if i not in (P, q))
    alpha = {site: 1 for site in lq}
    assert scalar_cocycle == gauge(q, alpha)
    assert sum(alpha.values()) == S - 2
    return zero_sum_rank, full_rank, 9, 8


def main():
    pure, mixed, matching_count = audit_normalization_and_activity()
    annihilator_count, graph_signature = audit_charts_and_annihilators()
    overlap_rows = audit_overlaps()
    gauge_ranks = audit_gauge_quotients()

    print(f"s={S}, sites={2 * S}, fan charts={len(FAN)}")
    print(f"pure coefficients={pure}, mixed residual={mixed}")
    print(f"supported top matchings={matching_count}")
    print(
        "rank-three graph per chart: "
        f"vertices={graph_signature[0]}, edges={graph_signature[1]}, "
        "connected/spanning/nonbipartite"
    )
    print(f"literal pair-Hessian annihilators={annihilator_count}")
    print(f"literal overlap rows={overlap_rows}")
    print(
        "gauge ranks (zero-sum, full, correction mod zero-sum, "
        f"correction mod full)={gauge_ranks}"
    )
    print("overlap-complex common-factor countermodel: PASS")


if __name__ == "__main__":
    main()
