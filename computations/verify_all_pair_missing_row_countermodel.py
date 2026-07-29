#!/usr/bin/env python3
"""Exact audit of an all-pair missing-row globalization countermodel.

The source is not a ternary GHZ realization.  It is a countermodel to a
purely graph/rank globalization of the pair trichotomy: it simultaneously
has forced anchors, matching-covered 3-connected support, active cells,
normalized constant coefficients, two universal matching monomials in every
fiber, star derivative irredundancy, and a missing-row witness for every
deleted pair.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


VERTICES = tuple(range(8))
COLORS = tuple(range(3))
INFINITY = 7


def one_factor(round_index):
    edges = [tuple(sorted((INFINITY, round_index)))]
    for offset in range(1, 4):
        left = (round_index + offset) % 7
        right = (round_index - offset) % 7
        edges.append(tuple(sorted((left, right))))
    return tuple(sorted(edges))


FACTORS = tuple(one_factor(index) for index in range(5))
P0, P1, Q0, Q1, Q2 = FACTORS


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            yield (tuple(sorted((first, second))),) + tail


ALL_MATCHINGS = tuple(perfect_matchings(VERTICES))


def base_matrices():
    matrices = {}
    full = (
        (Fraction(2), Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(2), Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(2)),
    )
    for edge in P0 + P1:
        matrices[edge] = full
    for colour, matching in enumerate((Q0, Q1, Q2)):
        for edge in matching:
            matrix = [[Fraction(0) for _ in COLORS] for _ in COLORS]
            matrix[colour][colour] = Fraction(1)
            matrices[edge] = tuple(tuple(row) for row in matrix)
    return matrices


def oriented_entry(matrices, edge, left_colour, right_colour):
    left, right = edge
    matrix = matrices[edge]
    return matrix[left_colour][right_colour]


def coefficient(matrices, vertices, colouring):
    total = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for edge in matching:
            if edge not in matrices:
                term = Fraction(0)
                break
            i, j = edge
            term *= oriented_entry(matrices, edge, colouring[i], colouring[j])
            if not term:
                break
        total += term
    return total


def normalized_matrices():
    matrices = base_matrices()
    constants = [
        coefficient(matrices, VERTICES, {vertex: colour for vertex in VERTICES})
        for colour in COLORS
    ]
    assert all(value > 0 for value in constants)

    # Apply an invertible diagonal map at vertex 0.  Every perfect matching
    # uses exactly one incident source cell, so this divides the constant-c
    # output coefficient by constants[c].
    normalized = {}
    for edge, matrix in matrices.items():
        values = [list(row) for row in matrix]
        if edge[0] == 0:
            for colour in COLORS:
                values[colour] = [entry / constants[colour] for entry in values[colour]]
        elif edge[1] == 0:
            for row in COLORS:
                for colour in COLORS:
                    values[row][colour] /= constants[colour]
        normalized[edge] = tuple(tuple(row) for row in values)
    return normalized, tuple(constants)


def supported_cells_at(matrices, vertex):
    cells = []
    for edge, matrix in matrices.items():
        if vertex not in edge:
            continue
        other = edge[1] if edge[0] == vertex else edge[0]
        for local_colour, other_colour in product(COLORS, repeat=2):
            value = (
                matrix[local_colour][other_colour]
                if edge[0] == vertex
                else matrix[other_colour][local_colour]
            )
            if value:
                cells.append((other, local_colour, other_colour))
    return tuple(cells)


def cofactor(matrices, deleted_pair):
    remaining = tuple(vertex for vertex in VERTICES if vertex not in deleted_pair)
    values = {}
    for word in product(COLORS, repeat=len(remaining)):
        colouring = dict(zip(remaining, word, strict=True))
        value = coefficient(matrices, remaining, colouring)
        if value:
            values[word] = value
    return remaining, values


def derivative_atom(matrices, vertex, cell, cofactor_cache):
    other, local_colour, other_colour = cell
    deleted = tuple(sorted((vertex, other)))
    remaining, values = cofactor_cache[deleted]
    outside = tuple(site for site in VERTICES if site != vertex)
    atom = {}
    for word, value in values.items():
        assignment = dict(zip(remaining, word, strict=True))
        assignment[other] = other_colour
        outside_word = tuple(assignment[site] for site in outside)
        atom[outside_word] = value
    return local_colour, atom


def sparse_rank(columns):
    pivots = {}
    for original in columns:
        column = dict(original)
        while column:
            pivot = min(column)
            if pivot not in pivots:
                scale = Fraction(1, 1) / column[pivot]
                pivots[pivot] = {
                    key: value * scale for key, value in column.items() if value
                }
                break
            factor = column[pivot]
            base = pivots[pivot]
            for key, value in base.items():
                updated = column.get(key, Fraction(0)) - factor * value
                if updated:
                    column[key] = updated
                elif key in column:
                    del column[key]
    return len(pivots)


def connected_after_deleting(graph, deleted):
    remaining = set(VERTICES) - set(deleted)
    if not remaining:
        return True
    seen = {next(iter(remaining))}
    frontier = list(seen)
    while frontier:
        vertex = frontier.pop()
        for neighbour in graph[vertex] & remaining:
            if neighbour not in seen:
                seen.add(neighbour)
                frontier.append(neighbour)
    return seen == remaining


def audit_graph(matrices):
    factor_edges = [edge for matching in FACTORS for edge in matching]
    assert len(factor_edges) == len(set(factor_edges)) == 20
    graph = {vertex: set() for vertex in VERTICES}
    for edge in matrices:
        i, j = edge
        graph[i].add(j)
        graph[j].add(i)
    assert all(len(graph[vertex]) == 5 for vertex in VERTICES)
    assert all(connected_after_deleting(graph, deleted) for size in (0, 1, 2) for deleted in combinations(VERTICES, size))
    assert all(all(edge in matrices for edge in matching) for matching in FACTORS)


def audit_fibres_and_anchors(matrices):
    # The two full factors give two nonzero matching monomials in every
    # colouring fibre, including all mixed fibres.
    for colouring_word in product(COLORS, repeat=8):
        colouring = dict(zip(VERTICES, colouring_word, strict=True))
        for matching in (P0, P1):
            assert all(
                oriented_entry(matrices, edge, colouring[edge[0]], colouring[edge[1]])
                for edge in matching
            )

    for colour, matching in enumerate((Q0, Q1, Q2)):
        for vertex in VERTICES:
            edge = next(edge for edge in matching if vertex in edge)
            matrix = matrices[edge]
            assert sum(bool(entry) for row in matrix for entry in row) == 1
            assert matrix[colour][colour]

    for colour in COLORS:
        colouring = {vertex: colour for vertex in VERTICES}
        assert coefficient(matrices, VERTICES, colouring) == 1

    mixed = {vertex: (1 if vertex == 0 else 0) for vertex in VERTICES}
    assert coefficient(matrices, VERTICES, mixed) > 0


def audit_all_pair_missing_rows(matrices):
    anchor_matchings = (Q0, Q1, Q2)
    for p, q in combinations(VERTICES, 2):
        internal = set(VERTICES) - {p, q}
        for endpoint in (p, q):
            witnesses = []
            for colour, matching in enumerate(anchor_matchings):
                edge = next(edge for edge in matching if endpoint in edge)
                other = edge[1] if edge[0] == endpoint else edge[0]
                if other not in internal:
                    continue
                # An E_cc block has two literal zero endpoint rows in either
                # orientation.
                matrix = matrices[edge]
                zero_rows = []
                for local_colour in COLORS:
                    row = (
                        matrix[local_colour]
                        if edge[0] == endpoint
                        else tuple(matrix[r][local_colour] for r in COLORS)
                    )
                    if not any(row):
                        zero_rows.append(local_colour)
                assert len(zero_rows) == 2
                witnesses.append((other, colour, tuple(zero_rows)))
            assert len(witnesses) >= 2


def audit_activity_and_star_irredundancy(matrices):
    cofactor_cache = {
        edge: cofactor(matrices, edge) for edge in matrices
    }
    for edge, matrix in matrices.items():
        _, cofactor_values = cofactor_cache[edge]
        assert cofactor_values
        assert any(entry for row in matrix for entry in row)

    for vertex in VERTICES:
        cells = supported_cells_at(matrices, vertex)
        assert len(cells) == 21
        atoms_by_row = {colour: [] for colour in COLORS}
        for cell in cells:
            local_colour, atom = derivative_atom(
                matrices, vertex, cell, cofactor_cache
            )
            atoms_by_row[local_colour].append(atom)
        assert all(len(atoms_by_row[colour]) == 7 for colour in COLORS)
        ranks = [sparse_rank(atoms_by_row[colour]) for colour in COLORS]
        assert ranks == [7, 7, 7], (vertex, ranks)


def main():
    matrices, constants_before_normalization = normalized_matrices()
    audit_graph(matrices)
    audit_fibres_and_anchors(matrices)
    audit_all_pair_missing_rows(matrices)
    audit_activity_and_star_irredundancy(matrices)
    print(f"normalized constant coefficients from {constants_before_normalization} to (1,1,1)")
    print("verified: 5-regular, 3-vertex-connected, matching-covered support")
    print("verified: two supported monomials in every fibre and three anchors per vertex")
    print("verified: every deleted pair has >=2 missing-row witnesses at each endpoint")
    print("verified: all active cofactors nonzero and every star has derivative rank 21/21")


if __name__ == "__main__":
    main()
