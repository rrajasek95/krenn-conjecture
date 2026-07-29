#!/usr/bin/env python3
"""Exact K8 countermodel to compressed witness-incidence counting."""

from __future__ import annotations

from itertools import product

import sympy as sp


PAIRS = ((0, 1), (2, 3), (4, 5), (6, 7))
GROUP = {vertex: group for group, pair in enumerate(PAIRS) for vertex in pair}
LABEL = {
    0: {2: 2, 3: 1, 4: 0, 5: 1, 6: 2, 7: 0},
    1: {0: 2, 1: 0, 4: 2, 5: 1, 6: 0, 7: 1},
    2: {0: 1, 1: 0, 2: 1, 3: 2, 6: 0, 7: 2},
    3: {0: 1, 1: 0, 2: 2, 3: 2, 4: 0, 5: 1},
}
PIVOT_ROWS = (
    (0, 2193, 2196, 2200, 2520, 2916, 4707, 4941, 5832),
    (0, 2193, 2196, 2200, 2520, 2601, 2835, 2916, 5832),
    (0, 324, 415, 468, 648, 649, 658, 2835, 4941),
    (0, 324, 415, 416, 468, 648, 658, 2520, 4707),
    (0, 11, 36, 72, 415, 468, 469, 2196, 2520),
    (0, 11, 36, 72, 415, 468, 469, 2196, 2574),
    (0, 4, 8, 11, 415, 416, 649, 2193, 2528),
    (0, 4, 8, 11, 415, 416, 649, 2193, 2520),
)

K = (
    sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]]),
    sp.Matrix([[0, 0, -1], [0, 0, 0], [1, 0, 0]]),
    sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]]),
)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for j in range(1, len(vertices)):
        second = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def matrix(u: int, v: int):
    if GROUP[u] == GROUP[v]:
        return sp.eye(3)
    left = sp.eye(3)[:, LABEL[GROUP[v]][u]]
    right = sp.eye(3)[:, LABEL[GROUP[u]][v]]
    return left * right.T


def oriented(u: int, v: int):
    return matrix(u, v) if u < v else matrix(v, u).T


def nonzero_entries(u: int, v: int):
    block = oriented(u, v)
    return [(i, j, int(block[i, j])) for i in range(3) for j in range(3) if block[i, j]]


def cofactor(deleted: tuple[int, int]):
    remaining = tuple(v for v in range(8) if v not in deleted)
    tensor = {}
    for matching in perfect_matchings(remaining):
        terms = [((), 1)]
        for u, v in matching:
            new_terms = []
            for assignment, value in terms:
                for i, j, coefficient in nonzero_entries(u, v):
                    new_terms.append(
                        (assignment + ((u, i), (v, j)), value * coefficient)
                    )
            terms = new_terms
        for assignment, value in terms:
            key = tuple(sorted(assignment))
            tensor[key] = tensor.get(key, 0) + value
    return {key: value for key, value in tensor.items() if value}


def coloring_index(coloring):
    index = 0
    for color in coloring:
        index = 3 * index + color
    return index


def main():
    cofactors = {
        (u, v): cofactor((u, v)) for u in range(8) for v in range(u + 1, 8)
    }
    assert all(cofactors.values())

    # Every vertex/color port has two active anchor-form blocks.
    for p in range(8):
        for r in range(3):
            anchors = []
            for u in range(8):
                if u == p:
                    continue
                block = oriented(p, u)
                other_columns = [c for c in range(3) if c != r]
                if block.rank() == 1 and block[:, other_columns] == sp.zeros(3, 2):
                    anchors.append(u)
            assert len(anchors) == 2

    # Every identity edge has all six outside vertices as zero witnesses.
    for p, q in PAIRS:
        assert oriented(p, q) == sp.eye(3)
        for u in range(8):
            if u in (p, q):
                continue
            for r in range(3):
                assert oriented(p, u) * K[r] * oriented(q, u).T == sp.zeros(3, 3)

    # Complete rank-one factor-witness audit in both endpoint directions.
    for p in range(8):
        for q in range(p + 1, 8):
            deleted = oriented(p, q)
            if deleted.rank() != 1:
                continue
            i, j = next((i, j) for i in range(3) for j in range(3) if deleted[i, j])
            for r in range(3):
                crosses = [
                    oriented(p, u) * K[r] * oriented(q, u).T
                    for u in range(8)
                    if u not in (p, q)
                ]
                if r != i:
                    assert sum(
                        cross[[row for row in range(3) if row != i], :] == sp.zeros(2, 3)
                        for cross in crosses
                    ) >= 2
                if r != j:
                    assert sum(
                        cross[:, [column for column in range(3) if column != j]] == sp.zeros(3, 2)
                        for cross in crosses
                    ) >= 2

    determinants = []
    for p in range(8):
        atoms = []
        for u in range(8):
            if u == p:
                continue
            x, y = sorted((p, u))
            for i, j, _ in nonzero_entries(x, y):
                color_p, color_u = (i, j) if p < u else (j, i)
                vector = {}
                for assignment, value in cofactors[(x, y)].items():
                    coloring = [0] * 8
                    coloring[p] = color_p
                    coloring[u] = color_u
                    for vertex, color in assignment:
                        coloring[vertex] = color
                    index = coloring_index(coloring)
                    vector[index] = vector.get(index, 0) + value
                atoms.append(vector)
        assert len(atoms) == 9
        minor = sp.Matrix(
            [[atoms[column].get(row, 0) for column in range(9)] for row in PIVOT_ROWS[p]]
        )
        determinants.append(int(minor.det()))
    assert determinants == [4, -4, 1, -4, -2, 2, -1, 1]

    print("verified K8 complete-support witness-incidence countermodel")
    print("verified forced anchors, active cofactors, and all witness alternatives")
    print("verified exact star-minor determinants", determinants)


if __name__ == "__main__":
    main()
