#!/usr/bin/env python3
"""Exact order-six countermodel to Hessian/support-only elimination.

Every aggregate block is a nonzero rank-one nonnegative integer matrix, and
the model satisfies all eighteen active coordinate-anchor incidences forced
by exact one-slice covering.  For each of the fifteen deleted pairs, the
four-site Hessian has rank 51 modulo
1,000,003.  Its 54-dimensional domain has the universal three-dimensional
gauge kernel, so this is an exact characteristic-zero gauge-rigidity
certificate for all pairs simultaneously.

The model is deliberately not an exact GHZ matching source: a displayed
mixed coefficient is strictly positive.  It isolates the need to use more
of the target equations than the coordinate-anchor consequence alone.
"""

from __future__ import annotations

from itertools import combinations

from verify_source_hessian_bipartite_rankdrop import (
    PRIME,
    apply_hessian,
    gauge_vectors,
    hessian_columns,
    rank_mod,
)


VERTICES = tuple(range(6))
FACTORS = {
    (0, 1): ((0, 0, 1), (23, 33, 85)),
    (0, 2): ((1, 0, 0), (0, 1, 0)),
    (0, 3): ((28, 35, 30), (0, 0, 1)),
    (0, 4): ((0, 1, 0), (87, 16, 73)),
    (0, 5): ((31, 34, 11), (1, 0, 0)),
    (1, 2): ((0, 1, 0), (81, 27, 71)),
    (1, 3): ((1, 0, 0), (68, 61, 48)),
    (1, 4): ((55, 94, 67), (1, 0, 0)),
    (1, 5): ((0, 0, 1), (0, 1, 0)),
    (2, 3): ((30, 94, 92), (40, 65, 13)),
    (2, 4): ((0, 0, 1), (0, 0, 1)),
    (2, 5): ((1, 0, 0), (23, 88, 40)),
    (3, 4): ((1, 0, 0), (0, 1, 0)),
    (3, 5): ((0, 1, 0), (0, 0, 1)),
    (4, 5): ((76, 95, 65), (40, 98, 40)),
}

ANCHORS = {
    0: {0: 5, 1: 2, 2: 3},
    1: {0: 4, 1: 5, 2: 0},
    2: {0: 0, 1: 1, 2: 4},
    3: {0: 1, 1: 4, 2: 5},
    4: {0: 3, 1: 0, 2: 2},
    5: {0: 2, 1: 3, 2: 1},
}


def outer(left, right):
    return [[x * y % PRIME for y in right] for x in left]


def proportional(left, right):
    return all(
        left[i] * right[j] == left[j] * right[i]
        for i in range(3)
        for j in range(i + 1, 3)
    )


def determinant(columns):
    first, second, third = columns
    return (
        first[0] * (second[1] * third[2] - second[2] * third[1])
        - second[0] * (first[1] * third[2] - first[2] * third[1])
        + third[0] * (first[1] * second[2] - first[2] * second[1])
    )


def internal_quadratic(deleted):
    remaining = tuple(vertex for vertex in VERTICES if vertex not in deleted)
    local_index = {vertex: index for index, vertex in enumerate(remaining)}
    quadratic = {}
    for left, right in combinations(remaining, 2):
        left_factor, right_factor = FACTORS[left, right]
        quadratic[local_index[left], local_index[right]] = outer(
            left_factor, right_factor
        )
    return quadratic


def endpoint_factor(left, right, endpoint):
    edge = (min(left, right), max(left, right))
    factors = FACTORS[edge]
    return factors[0] if endpoint == edge[0] else factors[1]


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(remainder):
            yield ((min(first, second), max(first, second)),) + matching


def coloring_coefficient(word):
    total = 0
    for matching in perfect_matchings(VERTICES):
        monomial = 1
        for left, right in matching:
            left_factor, right_factor = FACTORS[left, right]
            monomial *= left_factor[word[left]] * right_factor[word[right]]
        total += monomial
    return total


def main():
    assert set(FACTORS) == set(combinations(VERTICES, 2))
    assert all(all(entry >= 0 for factor in factors for entry in factor)
               for factors in FACTORS.values())
    assert all(any(entry for entry in factor)
               for factors in FACTORS.values() for factor in factors)

    coordinate = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    for tail, color_neighbors in ANCHORS.items():
        assert set(color_neighbors) == {0, 1, 2}
        assert len(set(color_neighbors.values())) == 3
        for color, neighbor in color_neighbors.items():
            assert endpoint_factor(tail, neighbor, neighbor) == coordinate[color]

    for color in range(3):
        images = [ANCHORS[tail][color] for tail in VERTICES]
        assert sorted(images) == list(VERTICES)
        assert all(images[tail] != tail for tail in VERTICES)

    for vertex in VERTICES:
        local_factors = [
            endpoint_factor(vertex, neighbor, vertex)
            for neighbor in VERTICES
            if neighbor != vertex
        ]
        assert all(
            not proportional(local_factors[first], local_factors[second])
            for first, second in combinations(range(5), 2)
        )
        assert all(
            determinant(tuple(local_factors[index] for index in indices)) != 0
            for indices in combinations(range(5), 3)
        )

    mixed_word = (2, 0, 0, 0, 0, 0)
    mixed_coefficient = coloring_coefficient(mixed_word)
    assert mixed_coefficient > 0

    audited = 0
    for deleted in combinations(VERTICES, 2):
        quadratic = internal_quadratic(set(deleted))
        columns = hessian_columns(quadratic)
        gauges = gauge_vectors(quadratic)
        assert rank_mod(columns) == 51
        assert rank_mod(gauges) == 3
        assert all(not any(apply_hessian(columns, gauge)) for gauge in gauges)
        audited += 1

    assert audited == 15
    print(
        "verified 18 active coordinate anchors and six five-line projective arcs; "
        f"mixed coefficient={mixed_coefficient}"
    )
    print("verified 15/15 rank-one pair Hessians: rank 51/54, gauge dimension 3")
    print("PASS: exact Hessian/support-only countermodel")


if __name__ == "__main__":
    main()
