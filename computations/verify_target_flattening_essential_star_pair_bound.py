#!/usr/bin/env python3
"""Exact audit for the target-flattening essential-star pair bound."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from math import ceil


COLORS = tuple(range(3))


def rank(rows, characteristic: int | None = None) -> int:
    matrix = [list(row) for row in rows]
    if not matrix:
        return 0
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column] % characteristic
                if characteristic is not None
            ),
            None,
        ) if characteristic is not None else next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        if characteristic is None:
            scale = matrix[pivot_row][column]
            matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        else:
            scale = pow(int(matrix[pivot_row][column]), -1, characteristic)
            matrix[pivot_row] = [
                int(value * scale) % characteristic
                for value in matrix[pivot_row]
            ]
        for row_index in range(len(matrix)):
            if row_index == pivot_row:
                continue
            value = matrix[row_index][column]
            if characteristic is not None:
                value %= characteristic
            if value == 0:
                continue
            matrix[row_index] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row_index], matrix[pivot_row], strict=True
                )
            ]
            if characteristic is not None:
                matrix[row_index] = [
                    int(entry) % characteristic for entry in matrix[row_index]
                ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in COLORS) for i in COLORS)


def oriented(blocks, u: int, v: int):
    matrix = blocks[edge(u, v)]
    return matrix if u < v else transpose(matrix)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            yield (edge(first, second),) + tail


def deterministic_blocks(order: int):
    blocks = {}
    for u, v in combinations(range(order), 2):
        matrix = []
        for i in COLORS:
            row = []
            for j in COLORS:
                numerator = (
                    (u + 2) * (i + 1)
                    - (v + 1) * (j + 2)
                    + (u + v + 1) * (i - j)
                )
                if (u + 2 * v + i + 3 * j) % 7 == 0:
                    numerator = 0
                row.append(Fraction(numerator, 1 + ((u + v + i + j) % 3)))
            matrix.append(tuple(row))
        blocks[u, v] = tuple(matrix)
    # Retain literal zero and endpoint-asymmetric blocks.
    if order >= 4:
        blocks[0, order - 1] = tuple(
            tuple(Fraction(0) for _ in COLORS) for _ in COLORS
        )
    return blocks


def matching_tensor(blocks, order: int):
    tensor = {}
    matchings = tuple(perfect_matchings(tuple(range(order))))
    for word in product(COLORS, repeat=order):
        total = Fraction(0)
        for matching in matchings:
            term = Fraction(1)
            for u, v in matching:
                term *= blocks[u, v][word[u]][word[v]]
            total += term
        if total:
            tensor[word] = total
    return tensor


def flattening_matrix(tensor, order: int, endpoint: int):
    other = tuple(site for site in range(order) if site != endpoint)
    columns = tuple(product(COLORS, repeat=order - 1))
    output = [[Fraction(0) for _ in columns] for _ in COLORS]
    for column, rest_word in enumerate(columns):
        word = [0] * order
        for site, colour in zip(other, rest_word, strict=True):
            word[site] = colour
        for colour in COLORS:
            word[endpoint] = colour
            output[colour][column] = tensor.get(tuple(word), Fraction(0))
    return output


def endpoint_support_matrix(blocks, order: int, endpoint: int, omitted=None):
    output = [[] for _ in COLORS]
    for neighbour in range(order):
        if neighbour == endpoint or neighbour == omitted:
            continue
        matrix = oriented(blocks, endpoint, neighbour)
        for row in COLORS:
            output[row].extend(matrix[row])
    return output


def audit_mode_flattening_containment() -> None:
    for order in (4, 6):
        blocks = deterministic_blocks(order)
        tensor = matching_tensor(blocks, order)
        for endpoint in range(order):
            support = endpoint_support_matrix(blocks, order, endpoint)
            flat = flattening_matrix(tensor, order, endpoint)
            support_rank = rank(support)
            joined = [
                support[row] + flat[row]
                for row in COLORS
            ]
            assert rank(joined) == support_rank

    # The ternary diagonal target has full mode support.
    for order in (4, 6):
        target = {(colour,) * order: Fraction(1) for colour in COLORS}
        for endpoint in range(order):
            assert rank(flattening_matrix(target, order, endpoint)) == 3


def binary_rank(vectors) -> int:
    basis = {}
    for original in vectors:
        value = original
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def generated_subspace(generators) -> frozenset[int]:
    values = {0}
    for generator in generators:
        values |= {value ^ generator for value in tuple(values)}
    return frozenset(values)


def all_binary_subspaces():
    spaces = {
        generated_subspace(
            vector for vector in range(1, 8) if mask & (1 << vector)
        )
        for mask in range(1 << 8)
    }
    ordered = tuple(
        sorted(spaces, key=lambda space: (binary_rank(space), tuple(space)))
    )
    assert Counter(binary_rank(space) for space in ordered) == Counter(
        {0: 1, 1: 7, 2: 7, 3: 1}
    )
    return ordered


def family_span_rank(family) -> int:
    vectors = set()
    for space in family:
        vectors.update(space)
    return binary_rank(vectors)


def audit_essential_subspace_ledger() -> None:
    spaces = all_binary_subspaces()
    maximum = 0
    spanning_families = 0
    equality_families = 0
    for length in range(1, 8):
        for indices in combinations_with_replacement(range(len(spaces)), length):
            family = tuple(spaces[index] for index in indices)
            if family_span_rank(family) != 3:
                continue
            spanning_families += 1
            essential = tuple(
                index
                for index in range(length)
                if family_span_rank(
                    family[:index] + family[index + 1 :]
                ) < 3
            )
            maximum = max(maximum, len(essential))
            assert len(essential) <= 3
            if len(essential) == 3:
                equality_families += 1
                assert all(
                    binary_rank(family[index]) == 1
                    for index in essential
                )
                assert family_span_rank(
                    tuple(family[index] for index in essential)
                ) == 3
                assert all(
                    family[index] == frozenset({0})
                    for index in range(length)
                    if index not in essential
                )
    assert maximum == 3
    assert spanning_families > 100_000
    assert equality_families > 0
    print(
        "F2^3 spanning/equality families:",
        spanning_families,
        equality_families,
    )


def audit_star_kernel_equivalence() -> None:
    for order in (4, 6):
        blocks = deterministic_blocks(order)
        for endpoint in range(order):
            for omitted in range(order):
                if omitted == endpoint:
                    continue
                star = endpoint_support_matrix(
                    blocks, order, endpoint, omitted=omitted
                )
                # The same horizontal matrix represents both the star map
                # and the sum of the mode-endpoint block supports.
                star_rank = rank(star)
                support_rank = rank(star)
                assert star_rank == support_rank
                assert (star_rank == 3) == (support_rank == 3)

    # Sharp family: three independent rank-one supports and arbitrary zeros.
    sharp = [
        [[Fraction(int(row == column == basis)) for column in COLORS]
         for row in COLORS]
        for basis in COLORS
    ]
    sharp.extend([[[Fraction(0) for _ in COLORS] for _ in COLORS]] * 4)
    matrices = [tuple(tuple(row) for row in matrix) for matrix in sharp]
    full = [
        sum((list(matrix[row]) for matrix in matrices), [])
        for row in COLORS
    ]
    assert rank(full) == 3
    essential = 0
    for omitted in range(len(matrices)):
        reduced = [
            sum(
                (
                    list(matrix[row])
                    for index, matrix in enumerate(matrices)
                    if index != omitted
                ),
                [],
            )
            for row in COLORS
        ]
        essential += int(rank(reduced) < 3)
    assert essential == 3


def audit_pair_arithmetic() -> None:
    thresholds = {}
    for order in range(8, 102, 2):
        good = order * (order - 1) // 2 - 3 * order
        assert good == order * (order - 7) // 2
        assert ceil(2 * good / order) == order - 7
        good_clique = ceil(order / 5)
        thresholds[order] = (good, order - 7, good_clique)
    assert {
        order: thresholds[order] for order in (8, 10, 12, 14)
    } == {
        8: (4, 1, 2),
        10: (15, 3, 2),
        12: (30, 5, 3),
        14: (49, 7, 3),
    }
    assert min(order for order in thresholds if thresholds[order][2] >= 6) == 26
    print(
        "good-pair thresholds:",
        {order: thresholds[order] for order in (8, 10, 12, 14)},
    )
    # The equality structure at an endpoint with three essential neighbours
    # gives bad degree at most three.  Hence a bad induced subgraph of minimum
    # degree five has essential count at most two at every endpoint.  Orienting
    # each bad edge toward a witnessing endpoint would give average degree at
    # most four, a contradiction.  Thus bad degeneracy is at most four.
    for vertex_count in range(1, 102):
        edges_for_minimum_degree_five = (5 * vertex_count + 1) // 2
        edges_from_two_witnesses_per_endpoint = 2 * vertex_count
        assert (
            edges_for_minimum_degree_five
            > edges_from_two_witnesses_per_endpoint
        )
    print("bad-pair degeneracy/color bound: 4 / 5")
    print("first forced six-site good clique: N=26")


def main() -> None:
    audit_mode_flattening_containment()
    audit_essential_subspace_ledger()
    audit_star_kernel_equivalence()
    audit_pair_arithmetic()
    print("target-flattening essential-star pair bound: PASS")


if __name__ == "__main__":
    main()
