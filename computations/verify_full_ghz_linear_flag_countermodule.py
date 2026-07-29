#!/usr/bin/env python3
"""Exact full-GHZ countermodule for every linear cut-averaging argument.

This script audits two statements from
``notes/full-ghz-linear-flag-countermodule.md``.

1.  In the formal matching-term relaxation at n=8, there are rational
    tensors Z_M with sum_M Z_M = Delta_(8,3), while the one-crossing map of
    every one of the 56 five-cuts fails the target-kernel inclusion by all
    three rows.  Consequently every linear incidence/averaging identity is
    satisfied but selects no good cut.
2.  Two complete rational scalar K8 sources have the identical full tensor
    H_8=1 and nonzero scalar on every pair cap, but different sums of the 28
    nonlinear pair-cap corrections.  Thus the correction sum is not a
    function of the output tensor alone.

The formal module deliberately drops the common-edge factorization
Z_M=tensor_product_{e in M} A_e.  That is exactly the nonlinear information
which a successful proof must use.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product

from sympy import Matrix, SparseMatrix


N = 8
Q = 3
VERTICES = tuple(range(N))
CUTS = tuple(combinations(VERTICES, 3))
EDGES = tuple(combinations(VERTICES, 2))
MASK64 = (1 << 64) - 1


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


MATCHINGS = perfect_matchings(VERTICES)
assert len(MATCHINGS) == 105


def crossing_count(matching, subset):
    subset = set(subset)
    return sum((left in subset) != (right in subset) for left, right in matching)


def one_cross_incidence():
    return [
        [int(crossing_count(matching, C) == 1) for matching in MATCHINGS]
        for C in CUTS
    ]


INCIDENCE = one_cross_incidence()


def audit_incidence_factorization():
    edge_index = {edge: index for index, edge in enumerate(EDGES)}
    edge_matching = Matrix(
        len(EDGES),
        len(MATCHINGS),
        lambda row, column: int(EDGES[row] in MATCHINGS[column]),
    )
    triple_edge = Matrix(
        len(CUTS),
        len(EDGES),
        lambda row, column: int(
            set(EDGES[column]).issubset(CUTS[row])
        ),
    )
    incidence = Matrix(INCIDENCE)
    assert incidence == triple_edge * edge_matching
    assert edge_matching.rank() == 21
    assert triple_edge.rank() == 28
    assert incidence.rank() == 21

    # Every matching is one-crossing on 24 five-sets, and every five-set has
    # 45 one-crossing matchings.
    assert {sum(incidence[row, column] for row in range(56)) for column in range(105)} == {24}
    assert {sum(incidence[row, column] for column in range(105)) for row in range(56)} == {45}

    # At n=8 the complementary sector is exactly the three-crossing sector.
    for row, C in enumerate(CUTS):
        for column, matching in enumerate(MATCHINGS):
            assert INCIDENCE[row][column] + int(
                crossing_count(matching, C) == 3
            ) == 1


def splitmix64(value: int):
    value = (value + 0x9E3779B97F4A7C15) & MASK64
    value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
    value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & MASK64
    return value ^ (value >> 31)


def word_code(word):
    answer = 0
    for color in word:
        answer = Q * answer + color
    return answer


def formal_perturbation():
    """Return the 120 words and their 105 zero-sum integer weights."""

    seed = 14
    mixed_words = [
        word
        for word in product(range(Q), repeat=N)
        if len(set(word)) > 1
    ]
    selected = sorted(
        mixed_words,
        key=lambda word: splitmix64(
            word_code(word) + seed * 0x123456789ABCDEF
        ),
    )[:120]
    weights = []
    for word in selected:
        code = word_code(word)
        row = [
            int(
                splitmix64(seed * 1_000_003 + code * 1009 + index * 9176)
                % 7
            )
            - 3
            for index in range(104)
        ]
        row.append(-sum(row))
        assert len(row) == len(MATCHINGS)
        assert sum(row) == 0
        weights.append(row)

    assert len({word_code(word) for word in selected}) == 120
    assert [word_code(word) for word in selected[:8]] == [
        3130,
        2626,
        4457,
        5545,
        5906,
        3688,
        3177,
        1665,
    ]
    return tuple(selected), tuple(tuple(row) for row in weights)


def base_three_word_index(color, length):
    answer = 0
    for _ in range(length):
        answer = Q * answer + color
    return answer


def formal_one_crossing_matrix(cut_index, selected, weights):
    C = CUTS[cut_index]
    C_set = set(C)
    U = tuple(vertex for vertex in VERTICES if vertex not in C_set)
    entries = {}

    # We clear the common denominator 105.  Each formal matching term has a
    # copy of Delta, and exactly 45 of the 105 matchings cross this cut once.
    for color in range(Q):
        entries[
            base_three_word_index(color, 3),
            base_three_word_index(color, 5),
        ] = 45

    for word, matching_weights in zip(selected, weights, strict=True):
        value = sum(
            INCIDENCE[cut_index][matching_index]
            * matching_weights[matching_index]
            for matching_index in range(len(MATCHINGS))
        )
        if value == 0:
            continue
        left_word = tuple(word[vertex] for vertex in C)
        right_word = tuple(word[vertex] for vertex in U)
        key = word_code(left_word), word_code(right_word)
        entries[key] = entries.get(key, 0) + value
        if entries[key] == 0:
            del entries[key]

    return SparseMatrix(Q**3, Q**5, entries)


def audit_full_ghz_formal_countermodule():
    selected, weights = formal_perturbation()

    # Define Z_M=(Delta + sum_w z_(M,w)e_w)/105.  These assertions are the
    # full output equation, coefficient by coefficient: constants sum to
    # one and every selected mixed coefficient sums to zero.  All unselected
    # mixed coefficients are identically zero.
    assert Fraction(len(MATCHINGS), 105) == 1
    for matching_weights in weights:
        assert Fraction(sum(matching_weights), 105) == 0

    target_rows = SparseMatrix(
        Q,
        Q**5,
        {
            (color, base_three_word_index(color, 5)): 1
            for color in range(Q)
        },
    )

    rank_histogram = Counter()
    for cut_index in range(len(CUTS)):
        one_crossing = formal_one_crossing_matrix(
            cut_index, selected, weights
        )
        rank = one_crossing.rank()
        augmented_rank = one_crossing.col_join(target_rows).rank()
        defect = augmented_rank - rank
        assert defect == 3
        rank_histogram[rank, defect] += 1

    assert rank_histogram == Counter({(27, 3): 46, (26, 3): 8, (25, 3): 2})
    return rank_histogram


def scalar_hafnian(edge_weights, vertices=VERTICES):
    return sum(
        product_value(edge_weights[edge] for edge in matching)
        for matching in perfect_matchings(tuple(vertices))
    )


def product_value(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def scalar_pair_corrections(edge_weights):
    full_value = scalar_hafnian(edge_weights)
    answer = {}
    for p, q in EDGES:
        U = tuple(vertex for vertex in VERTICES if vertex not in (p, q))
        scalar = edge_weights[p, q]
        assert scalar
        induced = {}
        for u, v in combinations(U, 2):
            induced[u, v] = (
                edge_weights[tuple(sorted((u, p)))]
                * edge_weights[tuple(sorted((v, q)))]
                + edge_weights[tuple(sorted((u, q)))]
                * edge_weights[tuple(sorted((v, p)))]
            )
        effective = {
            edge: edge_weights[edge] + induced[edge] / scalar
            for edge in combinations(U, 2)
        }
        answer[p, q] = full_value - scalar * scalar_hafnian(effective, U)
    return answer


def normalize_at_vertex_zero(edge_weights):
    normalized = dict(edge_weights)
    for edge in EDGES:
        if 0 in edge:
            normalized[edge] /= 105
    return normalized


def audit_nonlinear_cap_sum_not_output_determined():
    complete = normalize_at_vertex_zero(
        {edge: Fraction(1) for edge in EDGES}
    )

    canonical = {(0, 1), (2, 3), (4, 5), (6, 7)}
    signed = {
        edge: Fraction(1) if edge in canonical else Fraction(-1)
        for edge in EDGES
    }
    signed[0, 1] = Fraction(-63)
    signed = normalize_at_vertex_zero(signed)

    assert scalar_hafnian(complete) == scalar_hafnian(signed) == 1
    assert all(complete[edge] and signed[edge] for edge in EDGES)

    complete_corrections = scalar_pair_corrections(complete)
    signed_corrections = scalar_pair_corrections(signed)
    assert all(complete_corrections.values())
    assert all(signed_corrections.values())
    assert Counter(complete_corrections.values()) == Counter(
        {Fraction(-20, 7): 28}
    )
    assert sum(complete_corrections.values()) == -80
    assert sum(signed_corrections.values()) == Fraction(-2_118_320, 27_783)
    assert sum(complete_corrections.values()) != sum(signed_corrections.values())
    return sum(complete_corrections.values()), sum(signed_corrections.values())


def main():
    audit_incidence_factorization()
    rank_histogram = audit_full_ghz_formal_countermodule()
    first_sum, second_sum = audit_nonlinear_cap_sum_not_output_determined()

    print("PASS: full-GHZ formal matching-term countermodule")
    print("one-crossing (rank, target-row defect):", dict(rank_histogram))
    print("PASS: equal-output complete scalar cap sources")
    print("28-cap correction sums:", first_sum, "and", second_sum)


if __name__ == "__main__":
    main()
