#!/usr/bin/env python3
"""Exact audits for six-set flag averaging and the complete K8 cap model.

The first audit checks the universal incidence constants for five- and
six-set crossing sectors.  The second builds the integer ternary source in
``notes/six-cap-flag-averaging-countermodel.md`` and verifies that

* its three constant fibres are exactly one and its distance-one mixed
  fibres vanish;
* every coordinate anchor is tensor-active;
* all 56 five-set one-crossing kernel tests fail by three exact rows; and
* all 28 all-colours product pair caps have nonzero top cumulant correction.

All tensor arithmetic is over Q.  SymPy is used only for exact rational
row reduction of the small (at most 30)-row one-crossing matrices.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import comb

from sympy import Matrix


N = 8
Q = 3
VERTICES = tuple(range(N))
ZERO = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
S = ((0, 1, 0), (0, 0, 1), (1, 0, 0))
S2 = ((0, 0, 1), (1, 0, 0), (0, 1, 0))


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def round_robin_factors(n: int):
    """The standard one-factorization on Z/(n-1) union {infinity}."""

    infinity = n - 1
    modulus = n - 1
    factors = []
    for residue in range(modulus):
        factor = [tuple(sorted((infinity, residue)))]
        for offset in range(1, n // 2):
            factor.append(
                tuple(
                    sorted(
                        (
                            (residue + offset) % modulus,
                            (residue - offset) % modulus,
                        )
                    )
                )
            )
        factors.append(tuple(sorted(factor)))
    return tuple(factors)


FACTORS = round_robin_factors(N)
MATCHINGS = perfect_matchings(VERTICES)
WORDS_3 = tuple(product(range(Q), repeat=3))
WORDS_5 = tuple(product(range(Q), repeat=5))


def coordinate_matrix(color: int):
    return tuple(
        tuple(int(left == color and right == color) for right in range(Q))
        for left in range(Q)
    )


def build_source():
    matrices = {}
    for factor_index, matrix in ((0, S), (1, S2), (5, S), (6, S2)):
        for edge in FACTORS[factor_index]:
            matrices[edge] = matrix
    for color, factor_index in enumerate((2, 3, 4)):
        for edge in FACTORS[factor_index]:
            matrices[edge] = coordinate_matrix(color)
    assert set(matrices) == set(combinations(VERTICES, 2))
    return matrices


MATRICES = build_source()


def edge_entry(matrices, left, right, left_color, right_color):
    if left < right:
        return matrices.get((left, right), ZERO)[left_color][right_color]
    return matrices.get((right, left), ZERO)[right_color][left_color]


def matching_coefficient(vertices, matrices, word):
    colors = dict(zip(vertices, word, strict=True))
    answer = 0
    for matching in perfect_matchings(tuple(vertices)):
        term = 1
        for left, right in matching:
            term *= edge_entry(
                matrices,
                left,
                right,
                colors[left],
                colors[right],
            )
            if term == 0:
                break
        answer += term
    return answer


def matching_tensor(vertices, matrices):
    return {
        word: value
        for word in product(range(Q), repeat=len(vertices))
        if (value := matching_coefficient(vertices, matrices, word)) != 0
    }


def crossing_count(matching, subset):
    subset = set(subset)
    return sum((left in subset) != (right in subset) for left, right in matching)


def incidence_constant(m: int, k: int, j: int):
    if not (0 <= j <= min(k, m)) or (k - j) % 2:
        return 0
    whole_edges = (k - j) // 2
    if whole_edges > m - j:
        return 0
    return 2**j * comb(m, j) * comb(m - j, whole_edges)


def audit_crossing_sector_averages():
    # Every perfect matching has the same incidence census, so the canonical
    # matching suffices to check the coefficient multiplying each formal
    # matching monomial.
    for m in range(3, 9):
        vertices = tuple(range(2 * m))
        matching = tuple((2 * index, 2 * index + 1) for index in range(m))
        for k in (5, 6):
            if k > 2 * m:
                continue
            census = Counter(
                crossing_count(matching, subset)
                for subset in combinations(vertices, k)
            )
            expected = Counter(
                {
                    j: incidence_constant(m, k, j)
                    for j in range(k + 1)
                    if incidence_constant(m, k, j)
                }
            )
            assert census == expected
            assert sum(census.values()) == comb(2 * m, k)

    # In particular, the requested five-set one-crossing multiplier is
    # m(m-1)(m-2).
    for m in range(3, 20):
        assert incidence_constant(m, 5, 1) == m * (m - 1) * (m - 2)


def audit_source_fibres_and_anchors():
    tensor = matching_tensor(VERTICES, MATRICES)
    assert len(tensor) == 1544
    assert tensor[(0,) * N] == tensor[(1,) * N] == tensor[(2,) * N] == 1

    distance_histogram = Counter()
    value_histograms = {}
    for word, value in tensor.items():
        distance = min(
            sum(color != constant for color in word)
            for constant in range(Q)
        )
        distance_histogram[distance] += 1
        value_histograms.setdefault(distance, Counter())[value] += 1
    assert distance_histogram == Counter({0: 3, 2: 53, 3: 270, 4: 773, 5: 445})
    assert 1 not in distance_histogram

    # Deleting any E_rr anchor leaves the other three edges of the same
    # one-factor, so its constant-r six-site cofactor is exactly one.
    for color, factor_index in enumerate((2, 3, 4)):
        for edge in FACTORS[factor_index]:
            complement = tuple(vertex for vertex in VERTICES if vertex not in edge)
            assert matching_coefficient(
                complement, MATRICES, (color,) * len(complement)
            ) == 1

    return tensor, distance_histogram


def one_crossing_rows(C):
    C = tuple(C)
    C_set = set(C)
    U = tuple(vertex for vertex in VERTICES if vertex not in C_set)
    selected = tuple(
        matching
        for matching in MATCHINGS
        if crossing_count(matching, C_set) == 1
    )

    rows = []
    for left_word in WORDS_3:
        fixed = dict(zip(C, left_word, strict=True))
        row = []
        for right_word in WORDS_5:
            colors = fixed | dict(zip(U, right_word, strict=True))
            value = 0
            for matching in selected:
                term = 1
                for left, right in matching:
                    term *= edge_entry(
                        MATRICES,
                        left,
                        right,
                        colors[left],
                        colors[right],
                    )
                    if term == 0:
                        break
                value += term
            row.append(value)
        rows.append(row)
    return U, rows


def audit_all_one_crossing_kernel_tests():
    histogram = Counter()
    exceptional = []
    target_rows = [
        [int(word == (color,) * 5) for word in WORDS_5]
        for color in range(Q)
    ]

    for C in combinations(VERTICES, 3):
        _, rows = one_crossing_rows(C)
        rank = Matrix(rows).rank()
        augmented_rank = Matrix(rows + target_rows).rank()
        defect = augmented_rank - rank
        histogram[rank, defect] += 1
        assert defect == 3
        if rank == 8:
            exceptional.append(C)

    assert histogram == Counter({(9, 3): 54, (8, 3): 2})
    assert exceptional == [(0, 2, 3), (1, 2, 7)]
    return histogram


def product_pair_cap(pair, full_tensor):
    p, q = pair
    U = tuple(vertex for vertex in VERTICES if vertex not in pair)
    scalar = sum(
        edge_entry(MATRICES, p, q, left_color, right_color)
        for left_color, right_color in product(range(Q), repeat=2)
    )
    assert scalar in (1, 3)

    C2 = {}
    for u, v in combinations(U, 2):
        matrix = tuple(
            tuple(
                sum(
                    edge_entry(MATRICES, u, p, color_u, color_p)
                    * edge_entry(MATRICES, v, q, color_v, color_q)
                    + edge_entry(MATRICES, u, q, color_u, color_q)
                    * edge_entry(MATRICES, v, p, color_v, color_p)
                    for color_p, color_q in product(range(Q), repeat=2)
                )
                for color_v in range(Q)
            )
            for color_u in range(Q)
        )
        if matrix != ZERO:
            C2[u, v] = matrix

    internal = {
        edge: matrix
        for edge, matrix in MATRICES.items()
        if edge[0] in U and edge[1] in U
    }
    effective = {}
    for edge in combinations(U, 2):
        matrix = tuple(
            tuple(
                Fraction(edge_entry(internal, *edge, a, b))
                + Fraction(edge_entry(C2, *edge, a, b), scalar)
                for b in range(Q)
            )
            for a in range(Q)
        )
        if matrix != ZERO:
            effective[edge] = matrix

    # Direct product-cap marginal of H_8.
    capped = {}
    for word, value in full_tensor.items():
        retained_word = tuple(word[vertex] for vertex in U)
        capped[retained_word] = capped.get(retained_word, 0) + value

    effective_tensor = matching_tensor(U, effective)
    correction = {
        word: Fraction(capped.get(word, 0))
        - scalar * effective_tensor.get(word, 0)
        for word in set(capped) | set(effective_tensor)
    }
    correction = {word: value for word, value in correction.items() if value}

    # Independently expand only terms using at least two C2 edges.  This is
    # -C2^2*A/(2s)-C2^3/(6s^2), with square-free divided powers understood.
    higher = {}
    for word in product(range(Q), repeat=6):
        colors = dict(zip(U, word, strict=True))
        value = Fraction(0)
        for matching in perfect_matchings(U):
            for mask in range(1 << 3):
                number_C2 = mask.bit_count()
                if number_C2 < 2:
                    continue
                term = Fraction(-scalar, scalar**number_C2)
                for index, (left, right) in enumerate(matching):
                    family = C2 if mask & (1 << index) else internal
                    term *= edge_entry(
                        family,
                        left,
                        right,
                        colors[left],
                        colors[right],
                    )
                    if term == 0:
                        break
                value += term
        if value:
            higher[word] = value
    assert correction == higher

    diagonal_trace = sum(
        correction.get((color,) * 6, 0) for color in range(Q)
    )
    return scalar, correction, diagonal_trace


def audit_all_product_pair_caps(full_tensor):
    trace_by_pair = {}
    support_histogram = Counter()
    scalar_histogram = Counter()
    for pair in combinations(VERTICES, 2):
        scalar, correction, diagonal_trace = product_pair_cap(pair, full_tensor)
        assert correction
        assert diagonal_trace < 0
        scalar_histogram[scalar] += 1
        support_histogram[len(correction)] += 1
        trace_by_pair[pair] = diagonal_trace

    assert scalar_histogram == Counter({3: 16, 1: 12})
    assert support_histogram == Counter({697: 16, 729: 8, 665: 2, 616: 2})
    assert Counter(trace_by_pair.values()) == Counter(
        {
            Fraction(-96): 6,
            Fraction(-118): 5,
            Fraction(-6): 4,
            Fraction(-26, 3): 4,
            Fraction(-8): 4,
            Fraction(-32, 3): 2,
            Fraction(-20, 3): 2,
            Fraction(-114): 1,
        }
    )
    assert sum(trace_by_pair.values()) == Fraction(-4216, 3)
    return scalar_histogram, support_histogram, trace_by_pair


def main():
    audit_crossing_sector_averages()
    tensor, distance_histogram = audit_source_fibres_and_anchors()
    rank_histogram = audit_all_one_crossing_kernel_tests()
    scalar_histogram, support_histogram, traces = audit_all_product_pair_caps(tensor)

    print("PASS: universal five-/six-set crossing incidence constants")
    print("source support by distance from a constant word:", dict(distance_histogram))
    print("one-crossing (rank, target-row defect):", dict(rank_histogram))
    print("pair-cap scalar histogram:", dict(scalar_histogram))
    print("pair-cap correction support histogram:", dict(support_histogram))
    print("sum of 28 diagonal correction traces:", sum(traces.values()))


if __name__ == "__main__":
    main()
