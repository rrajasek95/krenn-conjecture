#!/usr/bin/env python3
"""Exact small audits for the three-copy alternating-invariant formulas."""

from __future__ import annotations

import itertools
from math import prod

import sympy as sp


COLORS = (0, 1, 2)
PERMUTATIONS = tuple(itertools.permutations(COLORS))


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


SIGNS = {permutation: permutation_sign(permutation) for permutation in PERMUTATIONS}


def determinant(columns):
    return int(sp.Matrix.hstack(*map(sp.Matrix, columns)).det())


def direct_phi_rank_one(matchings, local_vectors, vertex_count):
    total = 0
    for vertex_permutations in itertools.product(PERMUTATIONS, repeat=vertex_count):
        term = prod(SIGNS[permutation] for permutation in vertex_permutations)
        for copy, matching in enumerate(matchings):
            for edge in matching:
                for vertex in edge:
                    term *= local_vectors[edge, vertex][vertex_permutations[vertex][copy]]
        total += term
    return total


def factorized_phi_rank_one(matchings, local_vectors, vertex_count):
    incident = []
    for matching in matchings:
        at_vertex = {}
        for edge in matching:
            for vertex in edge:
                at_vertex[vertex] = edge
        incident.append(at_vertex)
    return prod(
        determinant(
            [local_vectors[incident[copy][vertex], vertex] for copy in range(3)]
        )
        for vertex in range(vertex_count)
    )


def direct_phi_matrices(matching, matrices, vertex_count):
    total = 0
    for vertex_permutations in itertools.product(PERMUTATIONS, repeat=vertex_count):
        term = prod(SIGNS[permutation] for permutation in vertex_permutations)
        for copy in range(3):
            for u, v in matching:
                term *= matrices[u, v][
                    vertex_permutations[u][copy], vertex_permutations[v][copy]
                ]
        total += term
    return total


def audit_vertex_determinants_and_repeated_matching():
    matchings = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    local_vectors = {}
    basis = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    for copy, matching in enumerate(matchings):
        for edge in matching:
            for vertex in edge:
                local_vectors[edge, vertex] = basis[copy]
    direct = direct_phi_rank_one(matchings, local_vectors, 4)
    factorized = factorized_phi_rank_one(matchings, local_vectors, 4)
    assert direct == factorized == 1

    matching = ((0, 1), (2, 3))
    matrices = {
        (0, 1): sp.Matrix([[1, 2, 0], [0, 1, 1], [2, 0, 1]]),
        (2, 3): sp.Matrix([[2, 1, 0], [1, 1, 1], [0, 2, 1]]),
    }
    direct_repeated = direct_phi_matrices(matching, matrices, 4)
    expected = 6**2 * prod(int(matrix.det()) for matrix in matrices.values())
    assert direct_repeated == expected
    print("vertex-determinant and repeated-matching formulas verified")


def audit_alternating_exchange():
    first = ((0, 1), (2, 3), (4, 5), (6, 7))
    second = ((0, 2), (1, 3), (4, 6), (5, 7))
    third = ((0, 4), (1, 5), (2, 6), (3, 7))
    switched_first = ((0, 2), (1, 3), (4, 5), (6, 7))
    switched_second = ((0, 1), (2, 3), (4, 6), (5, 7))

    local_vectors = {}
    for edge in first:
        for vertex in edge:
            local_vectors[edge, vertex] = (1, 0, 0)
    for edge in second:
        for vertex in edge:
            local_vectors[edge, vertex] = (0, 1, 0)
    for edge in third:
        for vertex in edge:
            local_vectors[edge, vertex] = (0, 0, 1)

    original = factorized_phi_rank_one((first, second, third), local_vectors, 8)
    switched = factorized_phi_rank_one(
        (switched_first, switched_second, third), local_vectors, 8
    )
    assert original == switched == 1
    print("alternating four-cycle exchange preserves the exact contribution")


def tensor_product(vectors):
    answer = {(0,) * 0: 1}
    for vector in vectors:
        answer = {
            prefix + (color,): coefficient * vector[color]
            for prefix, coefficient in answer.items()
            for color in COLORS
            if coefficient * vector[color]
        }
    return answer


def add_scaled(target, source, scale=1):
    for coloring, coefficient in source.items():
        target[coloring] = target.get(coloring, 0) + scale * coefficient
        if target[coloring] == 0:
            del target[coloring]


def audit_cp_localization_gap(vertex_count=6):
    e0, e1, e2 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    a = (1, 1, 1)
    tensor = {}
    for basis in (e0, e1, e2):
        add_scaled(tensor, tensor_product([basis] * vertex_count))
    tail = [a] * (vertex_count - 1)
    add_scaled(tensor, tensor_product([(1, 0, 1)] + tail))
    add_scaled(tensor, tensor_product([e0] + tail), -1)
    add_scaled(tensor, tensor_product([e2] + tail), -1)
    assert tensor == {
        (0,) * vertex_count: 1,
        (1,) * vertex_count: 1,
        (2,) * vertex_count: 1,
    }
    contribution = determinant([e0, e1, (1, 0, 1)]) * determinant(
        [e0, e1, a]
    ) ** (vertex_count - 1)
    assert contribution == 1
    print("distinct three-term CP cancellation leaves a nonzero rainbow triple")


def main():
    assert sum(SIGNS[p] ** 6 for p in PERMUTATIONS) == 6
    assert sum(SIGNS[p] ** 5 for p in PERMUTATIONS) == 0
    audit_vertex_determinants_and_repeated_matching()
    audit_alternating_exchange()
    audit_cp_localization_gap()


if __name__ == "__main__":
    main()
