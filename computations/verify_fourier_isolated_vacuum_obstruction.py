#!/usr/bin/env python3
"""Exact audit for the isolated-vacuum Fourier/Wick obstruction.

The proof is uniform.  This script independently checks its two finite
combinatorial kernels:

* disrupted isolated base pairs are indexed exactly by permutations; and
* no tournament on four vertices has every triple cyclic.

It also checks the sharp directed-three-cycle example at three base pairs.
"""

from __future__ import annotations

import itertools
import math


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def audit_permutation_fibers(m=4):
    vertices = tuple((side, i) for i in range(m) for side in ("a", "b"))
    matchings = tuple(perfect_matchings(vertices))
    for size in range(m + 1):
        for chosen_tuple in itertools.combinations(range(m), size):
            chosen = set(chosen_tuple)

            def allowed(edge):
                (side_u, i), (side_v, j) = edge
                states = {
                    (side_u, i): int(side_u == "a" and i in chosen),
                    (side_v, j): int(side_v == "a" and j in chosen),
                }
                if states[(side_u, i)] == states[(side_v, j)] == 0:
                    return i == j and side_u != side_v
                # Entries involving at least one flipped endpoint are
                # completely arbitrary.  The permutation structure must be
                # forced solely by the zero-zero support condition.
                return True

            survivors = [
                matching
                for matching in matchings
                if all(allowed(edge) for edge in matching)
            ]
            expected = 1
            for factor in range(2, size + 1):
                expected *= factor
            assert len(survivors) == expected, (chosen, len(survivors), expected)


def is_cyclic(bits, triple, pairs):
    oriented = {}
    for pair, bit in zip(pairs, bits):
        i, j = pair
        oriented[i, j] = not bit
        oriented[j, i] = bit
    i, j, k = triple
    return (
        oriented[i, j] and oriented[j, k] and oriented[k, i]
    ) or (
        oriented[i, k] and oriented[k, j] and oriented[j, i]
    )


def audit_four_vertex_tournaments():
    vertices = range(4)
    pairs = tuple(itertools.combinations(vertices, 2))
    triples = tuple(itertools.combinations(vertices, 3))
    count = 0
    for bits in itertools.product((0, 1), repeat=len(pairs)):
        count += 1
        assert not all(is_cyclic(bits, triple, pairs) for triple in triples)
    assert count == 64


def permanent(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    return sum(
        prod(matrix[i][permutation[i]] for i in range(n))
        for permutation in itertools.permutations(range(n))
    )


def prod(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def audit_sharp_three_cycle():
    matrix = ((0, 1, 0), (0, 0, 1), (1, 0, 0))
    for size in range(4):
        for subset in itertools.combinations(range(3), size):
            principal = tuple(tuple(matrix[i][j] for j in subset) for i in subset)
            assert permanent(principal) == int(size % 3 == 0)


def audit_one_shore_multiplicity(maximum_m=7):
    """Check the exact k!(m-k)! multiplicity used in equation (20)."""
    for m in range(1, maximum_m + 1):
        columns = tuple(range(m))
        for k in range(m + 1):
            selected_rows = set(range(k))
            image_counts = {
                subset: 0 for subset in itertools.combinations(columns, k)
            }
            for permutation in itertools.permutations(columns):
                image = tuple(sorted(permutation[i] for i in selected_rows))
                image_counts[image] += 1
            expected = math.factorial(k) * math.factorial(m - k)
            assert set(image_counts.values()) == {expected}

    # For m=4, (x_1,x_2,x_3,x_4)=(a,a*w,a*w^2,0), with
    # w^2+w+1=0 and a^3=4, has elementary symmetric values below.
    elementary = (1, 0, 0, 4, 0)
    coefficients = tuple(
        math.factorial(k) * math.factorial(4 - k) * elementary[k] // 24
        for k in range(5)
    )
    assert coefficients == (1, 0, 0, 1, 0)


if __name__ == "__main__":
    audit_permutation_fibers()
    audit_four_vertex_tournaments()
    audit_sharp_three_cycle()
    audit_one_shore_multiplicity()
    print(
        "verified permutation fibers, all 64 four-vertex tournaments, "
        "the sharp directed-three-cycle example, and one-shore multiplicities"
    )
