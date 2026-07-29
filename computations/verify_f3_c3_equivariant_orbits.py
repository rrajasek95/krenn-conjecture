#!/usr/bin/env python3
"""Solver-free audit of the exact joint-C3 n=8 search reduction.

This script independently regenerates the coupled cell action, all colouring
orbits, the centralizer of ``(012)(345)``, and its perfect-matching orbits.
It then compares those objects with the exact SAT search and with the older
84-parameter numerical parametrization.  No SAT solver is constructed or
called.
"""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import search_c3_equivariant_n8 as numerical  # noqa: E402
import search_f3_c3_equivariant_n8 as exact  # noqa: E402


N = 8
Q = 3
VERTICES = tuple(range(N))
G = (1, 2, 0, 4, 5, 3, 6, 7)


def independent_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in independent_matchings(remainder):
            yield ((first, second),) + tail


MATCHINGS = tuple(independent_matchings(VERTICES))


def canonical_cell(u, v, left, right):
    if u < v:
        return u, v, left, right
    return v, u, right, left


def independent_cell_step(cell):
    u, v, left, right = cell
    return canonical_cell(
        G[u], G[v], (left + 1) % Q, (right + 1) % Q,
    )


def independent_cell_orbit(cell):
    cell = canonical_cell(*cell)
    answer = []
    for _ in range(3):
        answer.append(cell)
        cell = independent_cell_step(cell)
    assert cell == answer[0]
    return frozenset(answer)


def independent_cell_key(cell):
    return min(independent_cell_orbit(cell))


def independent_colouring_step(colouring):
    image = [None] * N
    for old_vertex, colour in enumerate(colouring):
        image[G[old_vertex]] = (colour + 1) % Q
    return tuple(image)


def independent_colouring_orbit(colouring):
    answer = []
    for _ in range(3):
        answer.append(colouring)
        colouring = independent_colouring_step(colouring)
    assert colouring == answer[0]
    return frozenset(answer)


def canonical_matching(matching):
    return tuple(sorted(
        (min(u, v), max(u, v)) for u, v in matching
    ))


def matching_image(matching, permutation):
    return canonical_matching(
        (permutation[u], permutation[v]) for u, v in matching
    )


def monomial(colouring, matching):
    return tuple(sorted(
        independent_cell_key((u, v, colouring[u], colouring[v]))
        for u, v in matching
    ))


def audit_cells():
    assert tuple(G[G[G[v]]] for v in VERTICES) == VERTICES
    all_cells = tuple(
        (u, v, left, right)
        for u, v in combinations(VERTICES, 2)
        for left, right in product(range(Q), repeat=2)
    )
    orbit_by_key = {}
    for cell in all_cells:
        orbit_by_key.setdefault(
            independent_cell_key(cell), independent_cell_orbit(cell)
        )
    assert len(all_cells) == 252
    assert len(orbit_by_key) == 84
    assert {len(orbit) for orbit in orbit_by_key.values()} == {3}
    assert set().union(*orbit_by_key.values()) == set(all_cells)
    assert sum(map(len, orbit_by_key.values())) == len(all_cells)

    independent_keys = tuple(sorted(orbit_by_key))
    assert exact.GENERATOR == G
    assert exact.CELL_KEYS == independent_keys
    for cell in all_cells:
        key = independent_cell_key(cell)
        assert exact.cell_orbit_key(*cell) == key
        assert exact.CELL_KEYS[exact.CELL_TO_INDEX[cell]] == key

    # On the fixed edge 67, the three orbit parameters are exactly b-a mod 3.
    fixed_classes = {}
    for left, right in product(range(Q), repeat=2):
        key = independent_cell_key((6, 7, left, right))
        fixed_classes.setdefault(key, set()).add((right - left) % Q)
    assert len(fixed_classes) == 3
    assert sorted(next(iter(values)) for values in fixed_classes.values()) == [0, 1, 2]
    assert all(len(values) == 1 for values in fixed_classes.values())

    # Compare the equality partition with the pre-existing numerical expand().
    assert numerical.G == G and numerical.PARAMETERS == 84
    parameter_labels = np.arange(1, numerical.PARAMETERS + 1, dtype=np.int64)
    matrices = numerical.expand(parameter_labels)
    labels_by_key = {}
    for cell in all_cells:
        u, v, left, right = cell
        label = int(matrices[numerical.EDGE_INDEX[u, v], left, right])
        labels_by_key.setdefault(independent_cell_key(cell), set()).add(label)
    assert all(len(labels) == 1 for labels in labels_by_key.values())
    assert len({next(iter(labels)) for labels in labels_by_key.values()}) == 84
    return orbit_by_key


def audit_colourings_and_covariance():
    all_colourings = tuple(product(range(Q), repeat=N))
    reps = tuple(
        colouring for colouring in all_colourings
        if colouring == min(independent_colouring_orbit(colouring))
    )
    assert len(all_colourings) == 6561
    assert len(reps) == 2187
    assert all(len(independent_colouring_orbit(c)) == 3 for c in reps)
    assert set().union(*(independent_colouring_orbit(c) for c in reps)) == set(all_colourings)
    assert reps == exact.COLOURING_REPS
    for colouring in all_colourings:
        assert exact.transform_colouring(colouring) == independent_colouring_step(colouring)
        transformed = independent_colouring_step(colouring)
        assert (len(set(colouring)) == 1) == (len(set(transformed)) == 1)

        # Matching-by-matching covariance is stronger than merely comparing
        # the final coefficient sums: g(M) has exactly the same cell-orbit
        # monomial at the transformed colouring.
        for matching in MATCHINGS:
            transformed_matching = matching_image(matching, G)
            assert transformed_matching in MATCHING_SET
            assert monomial(colouring, matching) == monomial(
                transformed, transformed_matching
            )

    # Independently collect the 105 matching monomials modulo 3 and compare
    # every representative equation used by the SAT search.
    independent_index = {
        key: index for index, key in enumerate(sorted({
            independent_cell_key(cell)
            for cell in (
                (u, v, left, right)
                for u, v in combinations(VERTICES, 2)
                for left, right in product(range(Q), repeat=2)
            )
        }))
    }
    for index, colouring in enumerate(reps):
        counts = Counter(
            tuple(independent_index[cell] for cell in monomial(colouring, matching))
            for matching in MATCHINGS
        )
        reduced = tuple(sorted(
            (term, multiplicity % Q)
            for term, multiplicity in counts.items()
            if multiplicity % Q
        ))
        assert reduced == exact.REPRESENTATIVE_TERMS[index]
        assert exact.TARGETS[index] == (1 if len(set(colouring)) == 1 else 0)
    return reps


def audit_centralizer_and_branches(cell_orbits):
    centralizer = tuple(
        permutation
        for permutation in permutations(VERTICES)
        if all(permutation[G[v]] == G[permutation[v]] for v in VERTICES)
    )
    assert len(centralizer) == 36
    assert tuple(range(N)) in centralizer
    assert set(centralizer) == set(exact.CENTRALIZER)

    # Every commuting relabeling gives a well-defined permutation of the 84
    # coupled cell orbits.  This is precisely why it may normalize a supported
    # pure matching without leaving the ansatz.
    for permutation in centralizer:
        orbit_image = {}
        for key, orbit in cell_orbits.items():
            images = {
                independent_cell_key(canonical_cell(
                    permutation[u], permutation[v], left, right
                ))
                for u, v, left, right in orbit
            }
            assert len(images) == 1
            orbit_image[key] = next(iter(images))
        assert len(set(orbit_image.values())) == 84

    unseen = set(MATCHINGS)
    matching_orbits = []
    while unseen:
        representative = min(unseen)
        orbit = frozenset(
            matching_image(representative, permutation)
            for permutation in centralizer
        )
        assert orbit <= MATCHING_SET
        matching_orbits.append(orbit)
        unseen -= orbit
    matching_orbits.sort(key=min)
    assert len(matching_orbits) == 7
    assert [len(orbit) for orbit in matching_orbits] == [9, 36, 18, 3, 18, 3, 18]
    assert tuple(min(orbit) for orbit in matching_orbits) == exact.PURE_MATCHING_REPS
    assert set().union(*matching_orbits) == MATCHING_SET
    assert sum(map(len, matching_orbits)) == len(MATCHINGS)

    # Check that the four branch assumptions really refer to four distinct
    # pure-zero cell variables in every representative matching.
    for representative in exact.PURE_MATCHING_REPS:
        indices = {
            exact.CELL_TO_INDEX[(u, v, 0, 0)] for u, v in representative
        }
        assert len(indices) == 4
    residual_sizes = []
    for branch, matching in enumerate(exact.PURE_MATCHING_REPS):
        first_three = frozenset(matching[:3])
        last = matching[3]
        residual = tuple(
            permutation for permutation in centralizer
            if frozenset(
                canonical_matching(((permutation[u], permutation[v]),))[0]
                for u, v in matching[:3]
            ) == first_three
            and canonical_matching(
                ((permutation[last[0]], permutation[last[1]]),)
            )[0] == last
        )
        assert set(residual) == set(exact.RESIDUAL_RELABELINGS[branch])
        residual_sizes.append(len(residual))
    assert tuple(residual_sizes) == (4, 1, 1, 12, 1, 12, 1)
    return centralizer, matching_orbits


def audit_equivariant_gauge(cell_orbits):
    inverse = [None] * N
    for vertex, image in enumerate(G):
        inverse[image] = vertex
    inverse = tuple(inverse)

    def inverse_power(vertex, power):
        for _ in range(power):
            vertex = inverse[vertex]
        return vertex

    gauges = []
    for base_signs in product((1, 2), repeat=N):
        total = 1
        for sign in base_signs:
            total = total * sign % Q
        if total != 1:
            continue
        signs = tuple(
            tuple(base_signs[inverse_power(vertex, colour)]
                  for colour in range(Q))
            for vertex in VERTICES
        )
        # This relation is exactly what keeps the edge multiplier constant on
        # each coupled cell orbit.
        assert all(
            signs[G[vertex]][(colour + 1) % Q] == signs[vertex][colour]
            for vertex in VERTICES for colour in range(Q)
        )
        assert all(
            np.prod([signs[vertex][colour] for vertex in VERTICES]) % Q == 1
            for colour in range(Q)
        )
        for orbit in cell_orbits.values():
            multipliers = {
                signs[u][left] * signs[v][right] % Q
                for u, v, left, right in orbit
            }
            assert len(multipliers) == 1
        gauges.append(signs)
    assert len(gauges) == 128

    # Explicitly realize the normalization used by each SAT branch for every
    # possible nonzero value pattern on its four supported entries.
    for matching in exact.PURE_MATCHING_REPS:
        for old_values in product((1, 2), repeat=4):
            base_signs = [1] * N
            for position, (u, v) in enumerate(matching[:3]):
                base_signs[u] = 1
                base_signs[v] = old_values[position]
            u, v = matching[3]
            partial_product = 1
            for sign in base_signs:
                partial_product = partial_product * sign % Q
            base_signs[u] = 1
            base_signs[v] = partial_product  # inverse equals itself in F_3^*.
            assert np.prod(base_signs) % Q == 1
            transformed = tuple(
                old_values[position] * base_signs[u] * base_signs[v] % Q
                for position, (u, v) in enumerate(matching)
            )
            assert transformed[:3] == (1, 1, 1)
            assert transformed[3] in (1, 2)
    return gauges


MATCHING_SET = set(MATCHINGS)


def main():
    assert len(MATCHINGS) == 105
    assert set(MATCHINGS) == set(exact.MATCHINGS)
    cell_orbits = audit_cells()
    reps = audit_colourings_and_covariance()
    centralizer, matching_orbits = audit_centralizer_and_branches(cell_orbits)
    gauges = audit_equivariant_gauge(cell_orbits)
    print(
        "PASS "
        f"cells=252 cell_orbits={len(cell_orbits)} orbit_size=3 "
        f"colourings=6561 colouring_orbits={len(reps)} matchings={len(MATCHINGS)} "
        f"centralizer={len(centralizer)} matching_orbits={len(matching_orbits)} "
        f"matching_orbit_sizes={[len(orbit) for orbit in matching_orbits]} "
        f"residual_groups={[len(group) for group in exact.RESIDUAL_RELABELINGS]} "
        f"equivariant_gauges={len(gauges)} "
        "numerical_partition=matched covariance=all_6561x105"
    )


if __name__ == "__main__":
    main()
